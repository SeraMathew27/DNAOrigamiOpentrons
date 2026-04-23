#!/usr/bin/env python3
import argparse
import ast
import pathlib
import re
import sys

from opentrons.simulate import main, get_arguments
from opentrons.protocol_runner.python_protocol_wrappers import PythonProtocolExecutor


PARSER = {
    'add_int': int,
    'add_float': float,
    'add_bool': lambda x: {'false': False, 'true': True}[str(x).lower()],
    'add_str': str,
    'add_csv_file': lambda x: pathlib.Path(str(x).strip().strip('"\'')),
}


def parse_protocol_annotation(handle):
    """parse annotation that takes form of either:
    `# simulate-use: xxx`
    `# simulate_use: xxx`
    `_simulate_use = xxx`

    Args:
        handle: handle of opened protocol file in binary mode

    Returns:
        tuple of two dict, for literal overrides and path overrides
    """
    content = handle.read().decode('utf-8')
    lines = content.splitlines()
    parsed = ast.parse(content, handle.name, mode='exec')
    *_, func = (obj for obj in parsed.body if isinstance(obj, ast.FunctionDef) and obj.name == 'add_parameters')

    prev_end = func.lineno
    prev_use_val = None
    override_values = {}
    override_files = {}

    for obj in func.body:
        for line in lines[prev_end:obj.lineno - 1]:
            if m := re.match(r'\s*#\s*simulate[-_]use\s*:(.+)', line):
                prev_use_val = m[1].strip()

        if prev_use_val and isinstance(obj, ast.Expr) and isinstance(obj.value, ast.Call):
            if isinstance(obj.value.func, ast.Attribute) and (parser := PARSER.get(obj.value.func.attr)):
                variable_name = obj.value.args[1] if len(obj.value.args) >= 2 else next(
                    k.value for k in obj.value.keywords if k.arg == 'variable_name')
                if not isinstance(variable_name, ast.Constant):
                    print('unable to handle dynamic variable_name')
                else:
                    try:
                        value = parser(prev_use_val)
                        if obj.value.func.attr == 'add_csv_file':
                            override_files[variable_name.value] = value
                        else:
                            override_values[variable_name.value] = value
                    except Exception:
                        print(f'failed to parse value={prev_use_val} for variable {variable_name.value}')

        prev_use_val = None
        if isinstance(obj, ast.Assign) and len(obj.targets) == 1:
            target = obj.targets[0]
            if isinstance(target, ast.Name) and target.id == '_simulate_use':
                if not isinstance(obj.value, ast.Constant):
                    print('only plain literal value is supported: ' + ('\n'.join(lines[obj.lineno-1:obj.end_lineno])))
                else:
                    prev_use_val = obj.value.value

        prev_end = obj.end_lineno
    return override_values, override_files


def hook_exec(values, files):
    _original_exec = PythonProtocolExecutor.extract_run_parameters

    @staticmethod
    def _hooked(protocol, parameter_context,
                run_time_param_overrides, run_time_param_file_overrides):
        return _original_exec(protocol, parameter_context,
                              {**values, **(run_time_param_overrides or {})},
                              {**files, **(run_time_param_file_overrides or {})})
    PythonProtocolExecutor.extract_run_parameters = _hooked


if __name__ == '__main__':
    handle = get_arguments(argparse.ArgumentParser()).parse_args().protocol
    values, files = parse_protocol_annotation(handle)
    if overrides := {**values, **files}:
        print('Using parameters:')
        for key, value in overrides.items():
            print(f'    {key}={repr(value)}')
        print()
    hook_exec(values, files)
    sys.exit(main())
