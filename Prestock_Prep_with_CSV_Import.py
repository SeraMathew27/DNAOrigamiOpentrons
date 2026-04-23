from opentrons import protocol_api
import math
import json
from dataclasses import dataclass
from typing import Union, List
import csv

metadata = {
    'protocolName': 'Prestock Preparation with CSV import',
    'author': 'Sera Mathew, OpentronsAI',
    'description': 'Use CSV import to pool oligonucleotides from source plates to Eppendorf tubes to create prestocks for origami components',
}

requirements = {
    'robotType': 'Flex',
    'apiLevel': '2.25'
}

HEADERS = [
    "Source Plate",
    "Part",
    "Well Start",
    "Well End",
    "Destination Rack",
    "Destination Well",
    "Transfer Volume (ul)"
]


@dataclass
class Transfer:
    source_name: str
    source_part: str
    source_labware: str
    source_well: list
    dest_name: str
    dest_well: str
    volume: float
    source_slot: str = ""


def parse_csv_as_lists(
        file_path: str,
        detect_dialect: bool = True,
        **kwargs,
) -> List[List[str]]:
    """Parse a CSV file into List[List[str]], mimicking CSVParameter.parse_as_csv()."""
    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        content = f.read()

    rows: List[List[str]] = []
    if detect_dialect:
        try:
            dialect = csv.Sniffer().sniff(content[:1024])
            reader = csv.reader(content.splitlines(), dialect, **kwargs)
        except (csv.Error, UnicodeDecodeError) as e:
            raise ValueError("Cannot parse dialect or contents") from e
    else:
        try:
            reader = csv.reader(content.splitlines(), **kwargs)
        except (csv.Error, UnicodeDecodeError) as e:
            raise ValueError("Cannot parse contents") from e

    for row in reader:
        rows.append(row)

    while rows and rows[-1] == []:
        rows.pop()

    return rows


def read_transfers(csv_data: List[List[Union[str, int, float]]], src_labware: str, src_slot: dict) -> List[Transfer]:
    """
    Converts CSV rows into Transfer objects with addressable properties for use during the run.
    """
    headers = csv_data[0]
    assert headers == HEADERS, f"Expected: {HEADERS}, got: {headers}"

    transfers = []
    for row in csv_data[1:]:
        transfer = Transfer(
            source_name=row[0],
            source_part=row[1],
            source_labware=src_labware,
            source_well=expand_well_range(row[2], row[3]),
            dest_name=row[4],
            dest_well=row[5],
            volume=float(row[6]),
            source_slot=src_slot[row[0]]
        )
        transfers.append(transfer)
    return transfers


def add_parameters(parameters: protocol_api.ParameterContext):
    """Add runtime parameters to protocol."""

    # simulate-use: "C:\Users\seram\Downloads\PS_WS_prep_Remaining_Track(Prestock).csv"
    parameters.add_csv_file(
        variable_name="transfer_csv",
        display_name="Transfer CSV File",
        description="SOURCE PLATE, PART, WELL START, WELL END, DESTINATION RACK, DESTINATION WELL, VOLUME"
    )

    # simulate-use: fisherscientific_96_wellplate_1200ul
    parameters.add_str(
        variable_name="source_labware",
        display_name="Source Labware",
        description="Select source plate model",
        default="fisherscientific_96_wellplate_1200ul",
        choices=[{"display_name": "ThermoScientific 1200ul", "value": "fisherscientific_96_wellplate_1200ul"}]
    )

    # simulate-use: left
    parameters.add_str(
        variable_name="pipette_mount",
        display_name="1000ul Pipette Mount",
        description="Location of mount for 1000ul Pipette",
        default="left",
        choices=[{"display_name": "Right", "value": "right"}, {"display_name": "Left", "value": "left"}]
    )


def set_source_plate_slots(csv_data: List[List[str]]) -> dict:
    """
    Assigns on-deck slots to unique source plates found in the CSV.
    Raises an error if more than 4 unique source plates are present.
    """
    source_slots = ['D2', 'C2', 'B2', 'A2']
    source_plate_names = list(dict.fromkeys(row[0] for row in csv_data[1:]))

    if len(source_plate_names) > len(source_slots):
        raise ValueError(
            f"CSV contains {len(source_plate_names)} unique source plates, "
            f"but only {len(source_slots)} on-deck slots are available. "
            f"Split your CSV into batches of {len(source_slots)} plates."
        )

    return {plate: source_slots[i] for i, plate in enumerate(source_plate_names)}


def expand_well_range(start_well: str, end_well: str) -> list:
    """
    Expands a well range (e.g., 'A1' to 'B12') into a list of individual wells.
    Assumes standard 96-well plate format (A-H rows, 1-12 columns).
    """
    if not start_well:
        return []

    start_row = ord(start_well[0]) - ord('A')
    start_col = int(start_well[1:]) - 1
    end_row = ord(end_well[0]) - ord('A')
    end_col = int(end_well[1:]) - 1

    wells = []
    for row in range(start_row, end_row + 1):
        col_start = start_col if row == start_row else 0
        col_end = end_col if row == end_row else 11
        for col in range(col_start, col_end + 1):
            wells.append(f"{chr(ord('A') + row)}{col + 1}")

    return wells


def calculate_tips(transfers: List[Transfer]) -> int:
    """
    Returns the number of 1000ul tip racks needed for the protocol,
    based on one tip per source well across all transfers.
    """
    total_tips = sum(len(t.source_well) for t in transfers)
    return math.ceil(total_tips / 96)


def validate_transfers(transfers: List[Transfer], source_plate_slots: dict):
    """
    Checks transfer data for common errors before the run starts.
    Raises ValueError with a descriptive message if any issue is found.
    """
    valid_dest_wells = {
        f"{r}{c}" for r in "ABCD" for c in range(1, 7)
    }

    for i, t in enumerate(transfers):
        row_num = i + 2  # account for header row

        if t.source_name not in source_plate_slots:
            raise ValueError(f"Row {row_num}: Source plate '{t.source_name}' not in deck slot mapping.")

        if not t.source_well:
            raise ValueError(f"Row {row_num}: Well range is empty for part '{t.source_part}'.")

        if t.dest_well not in valid_dest_wells:
            raise ValueError(f"Row {row_num}: Destination well '{t.dest_well}' is not valid for a 24-tube rack.")

        if t.volume <= 0:
            raise ValueError(f"Row {row_num}: Transfer volume must be positive, got {t.volume}.")


def run(protocol: protocol_api.ProtocolContext):

    source_labware = protocol.params.source_labware
    csv_data = protocol.params.transfer_csv.parse_as_csv()
    csv_data = [row[:7] for row in csv_data]

    # Strip BOM character if present (common in Windows-exported CSVs)
    if csv_data[0][0].startswith("\ufeff"):
        csv_data[0][0] = csv_data[0][0][1:]

    CUSTOM_LABWARE = json.loads(
        """{"custom_beta/fisherscientific_96_wellplate_1200ul/1":{"ordering":[["A1","B1","C1","D1","E1","F1","G1","H1"],["A2","B2","C2","D2","E2","F2","G2","H2"],["A3","B3","C3","D3","E3","F3","G3","H3"],["A4","B4","C4","D4","E4","F4","G4","H4"],["A5","B5","C5","D5","E5","F5","G5","H5"],["A6","B6","C6","D6","E6","F6","G6","H6"],["A7","B7","C7","D7","E7","F7","G7","H7"],["A8","B8","C8","D8","E8","F8","G8","H8"],["A9","B9","C9","D9","E9","F9","G9","H9"],["A10","B10","C10","D10","E10","F10","G10","H10"],["A11","B11","C11","D11","E11","F11","G11","H11"],["A12","B12","C12","D12","E12","F12","G12","H12"]],"brand":{"brand":"Fisher Scientific","brandId":["SP-1081"]},"metadata":{"displayName":"Fisher Scientific 96 Well Plate 1200 µL","displayCategory":"wellPlate","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.76,"yDimension":85.48,"zDimension":42.5},"wells":{"A1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":74.24,"z":3.15},"B1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":65.24,"z":3.15},"C1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":56.24,"z":3.15},"D1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":47.24,"z":3.15},"E1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":38.24,"z":3.15},"F1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":29.24,"z":3.15},"G1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":20.24,"z":3.15},"H1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":11.24,"z":3.15},"A2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":74.24,"z":3.15},"B2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":65.24,"z":3.15},"C2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":56.24,"z":3.15},"D2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":47.24,"z":3.15},"E2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":38.24,"z":3.15},"F2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":29.24,"z":3.15},"G2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":20.24,"z":3.15},"H2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":11.24,"z":3.15},"A3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":74.24,"z":3.15},"B3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":65.24,"z":3.15},"C3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":56.24,"z":3.15},"D3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":47.24,"z":3.15},"E3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":38.24,"z":3.15},"F3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":29.24,"z":3.15},"G3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":20.24,"z":3.15},"H3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":11.24,"z":3.15},"A4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":74.24,"z":3.15},"B4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":65.24,"z":3.15},"C4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":56.24,"z":3.15},"D4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":47.24,"z":3.15},"E4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":38.24,"z":3.15},"F4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":29.24,"z":3.15},"G4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":20.24,"z":3.15},"H4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":11.24,"z":3.15},"A5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":74.24,"z":3.15},"B5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":65.24,"z":3.15},"C5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":56.24,"z":3.15},"D5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":47.24,"z":3.15},"E5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":38.24,"z":3.15},"F5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":29.24,"z":3.15},"G5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":20.24,"z":3.15},"H5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":11.24,"z":3.15},"A6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":74.24,"z":3.15},"B6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":65.24,"z":3.15},"C6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":56.24,"z":3.15},"D6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":47.24,"z":3.15},"E6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":38.24,"z":3.15},"F6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":29.24,"z":3.15},"G6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":20.24,"z":3.15},"H6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":11.24,"z":3.15},"A7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":74.24,"z":3.15},"B7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":65.24,"z":3.15},"C7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":56.24,"z":3.15},"D7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":47.24,"z":3.15},"E7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":38.24,"z":3.15},"F7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":29.24,"z":3.15},"G7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":20.24,"z":3.15},"H7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":11.24,"z":3.15},"A8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":74.24,"z":3.15},"B8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":65.24,"z":3.15},"C8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":56.24,"z":3.15},"D8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":47.24,"z":3.15},"E8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":38.24,"z":3.15},"F8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":29.24,"z":3.15},"G8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":20.24,"z":3.15},"H8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":11.24,"z":3.15},"A9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":74.24,"z":3.15},"B9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":65.24,"z":3.15},"C9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":56.24,"z":3.15},"D9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":47.24,"z":3.15},"E9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":38.24,"z":3.15},"F9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":29.24,"z":3.15},"G9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":20.24,"z":3.15},"H9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":11.24,"z":3.15},"A10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":74.24,"z":3.15},"B10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":65.24,"z":3.15},"C10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":56.24,"z":3.15},"D10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":47.24,"z":3.15},"E10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":38.24,"z":3.15},"F10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":29.24,"z":3.15},"G10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":20.24,"z":3.15},"H10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":11.24,"z":3.15},"A11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":74.24,"z":3.15},"B11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":65.24,"z":3.15},"C11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":56.24,"z":3.15},"D11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":47.24,"z":3.15},"E11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":38.24,"z":3.15},"F11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":29.24,"z":3.15},"G11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":20.24,"z":3.15},"H11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":11.24,"z":3.15},"A12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":74.24,"z":3.15},"B12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":65.24,"z":3.15},"C12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":56.24,"z":3.15},"D12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":47.24,"z":3.15},"E12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":38.24,"z":3.15},"F12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":29.24,"z":3.15},"G12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":20.24,"z":3.15},"H12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":11.24,"z":3.15}},"groups":[{"metadata":{"wellBottomShape":"u"},"wells":["A1","B1","C1","D1","E1","F1","G1","H1","A2","B2","C2","D2","E2","F2","G2","H2","A3","B3","C3","D3","E3","F3","G3","H3","A4","B4","C4","D4","E4","F4","G4","H4","A5","B5","C5","D5","E5","F5","G5","H5","A6","B6","C6","D6","E6","F6","G6","H6","A7","B7","C7","D7","E7","F7","G7","H7","A8","B8","C8","D8","E8","F8","G8","H8","A9","B9","C9","D9","E9","F9","G9","H9","A10","B10","C10","D10","E10","F10","G10","H10","A11","B11","C11","D11","E11","F11","G11","H11","A12","B12","C12","D12","E12","F12","G12","H12"]}],"parameters":{"format":"irregular","quirks":[],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"fisherscientific_96_wellplate_1200ul"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}}}""")

    # Load trash bin
    trash = protocol.load_trash_bin('A3')

    # Parse CSV and determine source plate layout
    source_plate_slots = set_source_plate_slots(csv_data)

    # Build Transfer objects and validate before loading any labware
    transfers = read_transfers(csv_data, source_labware, source_plate_slots)
    validate_transfers(transfers, source_plate_slots)

    # Calculate tip rack requirements
    total_tip_racks_1000 = calculate_tips(transfers)
    available_slots_1000 = ['B3', 'C3', 'D3', 'C1']
    num_tip_racks_to_load = min(total_tip_racks_1000, len(available_slots_1000))
    off_deck_tip_count = total_tip_racks_1000 - num_tip_racks_to_load

    tip_racks_1000 = [
        protocol.load_labware('opentrons_flex_96_tiprack_1000ul', slot)
        for slot in available_slots_1000[:num_tip_racks_to_load]
    ]
    off_deck_tips = [
        protocol.load_labware('opentrons_flex_96_tiprack_1000ul', protocol_api.OFF_DECK)
        for _ in range(off_deck_tip_count)
    ]
    tip_racks_1000.extend(off_deck_tips)

    pipette_left = protocol.load_instrument(
        'flex_1channel_1000',
        mount='left',
        tip_racks=tip_racks_1000
    )

    # Load source plates onto deck
    source_plates = {}
    for plate_name, slot in source_plate_slots.items():
        source_plates[plate_name] = protocol.load_labware_from_definition(
            CUSTOM_LABWARE["custom_beta/fisherscientific_96_wellplate_1200ul/1"],
            location=slot,
            label=plate_name
        )

    # Load prestock tube rack
    tube_rack_1 = protocol.load_labware(
        "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
        location="D1",
        label="Pre-Stock Tube Rack",
        namespace="opentrons",
        version=3,
    )

    # Confirm deck layout and tip requirements before starting
    deck_summary = [f"{slot}: {name}" for name, slot in source_plate_slots.items()]
    protocol.pause(
        f"This protocol requires {total_tip_racks_1000} x 1000ul tip rack(s). "
        f"Deck layout: {deck_summary}. Press continue to start."
    )

    # Execute transfers
    for transfer in transfers:
        source = source_plates[transfer.source_name]
        destination = tube_rack_1

        pipette_left.transfer(
            volume=transfer.volume,
            source=[source.wells_by_name()[well] for well in transfer.source_well],
            dest=destination.wells_by_name()[transfer.dest_well],
            new_tip='always'
        )

        protocol.comment(
            f"Transferred {transfer.volume} µL from {transfer.source_name} "
            f"wells {transfer.source_well[0]}-{transfer.source_well[-1]} "
            f"({len(transfer.source_well)} wells) "
            f"to {transfer.dest_name} well {transfer.dest_well} "
            f"for {transfer.source_part} prestock"
        )

    protocol.pause("Prestock preparation complete. Continue to make working stock.")
