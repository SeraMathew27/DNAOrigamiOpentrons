from opentrons import protocol_api
import math
import json
from dataclasses import dataclass
from typing import Union, Set, List, Optional
import itertools

metadata = {
    'protocolName': 'Folding Reaction',
    'author': 'Sera Mathew, OpentronsAI',
    'description': "Prepare and run folding reactions with pre-made working stocks.",
}

requirements = {
    'robotType': 'Flex',
    'apiLevel': '2.25'
}

# Define the expected headers for the CSV file
HEADERS = [
    "Working Stock",
    "Part",
    "Prestock Well",
    "Num Oligos",
    "Transfer Volume",
    "Destination Tube",
    "Working Stock Volume"
]

@dataclass
class Transfer:
    ws_name: str
    ps_name: str
    ps_well: str
    num_oligos: int
    dest_well: str
    volume: float


def read_transfers(csv_data:List[List[Union[str, int, float]]]) -> List[Transfer]:
    """
    Converts list of transfers into a list of Transfer objects so that each unique transfer has
    addressable properties that will be called during the run. Also creates a prestock object
    which is like a simplified transfer object.
    """

    # Check if headers match the correct file formate
    headers = csv_data[0]
    #assert headers == HEADERS, f"Expected: {HEADERS}, got: {headers}"
    #TODO: Validate Data


    transfers = []
    transfer_data = csv_data[1:]
    for row in transfer_data:

        transfer = Transfer(
            ws_name=row[0],
            ps_name=row[1],
            ps_well = row[2],
            num_oligos =int(row[3]),
            dest_well = row[5],
            volume = float(row[4])
        )
        transfers.append(transfer)
    return transfers


def expand_well_range(start_well, end_well):
    """
    Expands a well range (e.g., 'A1' to 'B12') into a list of individual wells.

    Assumes standard 96-well plate format (A-H rows, 1-12 columns).
    """
    # Parse start well
    start_row = ord(start_well[0]) - ord('A')  # Convert letter to number (A=0, B=1, etc.)
    start_col = int(start_well[1:]) - 1  # Convert to 0-indexed

    # Parse end well
    end_row = ord(end_well[0]) - ord('A')
    end_col = int(end_well[1:]) - 1

    # Generate list of wells
    wells = []
    for row in range(start_row, end_row):
        for col in range(12):
            well_name = f"{chr(ord('A') + row)}{col + 1}"
            wells.append(well_name)
    for col in range(0, end_col + 1):
        well_name = f"{chr(ord('A') + end_row)}{col + 1}"
        wells.append(well_name)

    return wells

def add_parameters(parameters: protocol_api.ParameterContext):
    """
    Add runtime parameters to protocol
    """
    # simulate-use: "C:\Users\seram\Downloads\WS_Prep_Track(Working Stock).csv"
    parameters.add_csv_file(
        variable_name="transfer_csv",
        display_name="Transfer CSV File",
        description="Working Stock, Part, Prestock Well, Num Oligos, Transfer Volume, Destination Tube, Reaction Volume"

    )


    # simulate_use: "C1"
    parameters.add_str(
        variable_name="folding_plate_start_well",
        display_name="Folding Plate Start Well",
        description="First open well of the plate to add folding reaction",
        choices=[
{"display_name": "A1", "value": "A1"}, {"display_name": "A2", "value": "A2"}, {"display_name": "A3", "value": "A3"}, {"display_name": "A4", "value": "A4"}, {"display_name": "A5", "value": "A5"}, {"display_name": "A6", "value": "A6"}, {"display_name": "A7", "value": "A7"}, {"display_name": "A8", "value": "A8"}, {"display_name": "A9", "value": "A9"}, {"display_name": "A10", "value": "A10"}, {"display_name": "A11", "value": "A11"}, {"display_name": "A12", "value": "A12"},

{"display_name": "B1", "value": "B1"}, {"display_name": "B2", "value": "B2"}, {"display_name": "B3", "value": "B3"}, {"display_name": "B4", "value": "B4"}, {"display_name": "B5", "value": "B5"}, {"display_name": "B6", "value": "B6"}, {"display_name": "B7", "value": "B7"}, {"display_name": "B8", "value": "B8"}, {"display_name": "B9", "value": "B9"}, {"display_name": "B10", "value": "B10"}, {"display_name": "B11", "value": "B11"}, {"display_name": "B12", "value": "B12"},

{"display_name": "C1", "value": "C1"}, {"display_name": "C2", "value": "C2"}, {"display_name": "C3", "value": "C3"}, {"display_name": "C4", "value": "C4"}, {"display_name": "C5", "value": "C5"}, {"display_name": "C6", "value": "C6"}, {"display_name": "C7", "value": "C7"}, {"display_name": "C8", "value": "C8"}, {"display_name": "C9", "value": "C9"}, {"display_name": "C10", "value": "C10"}, {"display_name": "C11", "value": "C11"}, {"display_name": "C12", "value": "C12"},

{"display_name": "D1", "value": "D1"}, {"display_name": "D2", "value": "D2"}, {"display_name": "D3", "value": "D3"}, {"display_name": "D4", "value": "D4"}, {"display_name": "D5", "value": "D5"}, {"display_name": "D6", "value": "D6"}, {"display_name": "D7", "value": "D7"}, {"display_name": "D8", "value": "D8"}, {"display_name": "D9", "value": "D9"}, {"display_name": "D10", "value": "D10"}, {"display_name": "D11", "value": "D11"}, {"display_name": "D12", "value": "D12"},

{"display_name": "E1", "value": "E1"}, {"display_name": "E2", "value": "E2"}, {"display_name": "E3", "value": "E3"}, {"display_name": "E4", "value": "E4"}, {"display_name": "E5", "value": "E5"}, {"display_name": "E6", "value": "E6"}, {"display_name": "E7", "value": "E7"}, {"display_name": "E8", "value": "E8"}, {"display_name": "E9", "value": "E9"}, {"display_name": "E10", "value": "E10"}, {"display_name": "E11", "value": "E11"}, {"display_name": "E12", "value": "E12"},

{"display_name": "F1", "value": "F1"}, {"display_name": "F2", "value": "F2"}, {"display_name": "F3", "value": "F3"}, {"display_name": "F4", "value": "F4"}, {"display_name": "F5", "value": "F5"}, {"display_name": "F6", "value": "F6"}, {"display_name": "F7", "value": "F7"}, {"display_name": "F8", "value": "F8"}, {"display_name": "F9", "value": "F9"}, {"display_name": "F10", "value": "F10"}, {"display_name": "F11", "value": "F11"}, {"display_name": "F12", "value": "F12"},

{"display_name": "G1", "value": "G1"}, {"display_name": "G2", "value": "G2"}, {"display_name": "G3", "value": "G3"}, {"display_name": "G4", "value": "G4"}, {"display_name": "G5", "value": "G5"}, {"display_name": "G6", "value": "G6"}, {"display_name": "G7", "value": "G7"}, {"display_name": "G8", "value": "G8"}, {"display_name": "G9", "value": "G9"}, {"display_name": "G10", "value": "G10"}, {"display_name": "G11", "value": "G11"}, {"display_name": "G12", "value": "G12"},

{"display_name": "H1", "value": "H1"}, {"display_name": "H2", "value": "H2"}, {"display_name": "H3", "value": "H3"}, {"display_name": "H4", "value": "H4"}, {"display_name": "H5", "value": "H5"}, {"display_name": "H6", "value": "H6"}, {"display_name": "H7", "value": "H7"}, {"display_name": "H8", "value": "H8"}, {"display_name": "H9", "value": "H9"}, {"display_name": "H10", "value": "H10"}, {"display_name": "H11", "value": "H11"}, {"display_name": "H12", "value": "H12"}
],
        default = "A1" #CHANGE
    )

    # simulate_use: 500.0
    parameters.add_float(
        variable_name="folding_reaction_volume",
        display_name="Folding Reaction Volume",
        description="Volume of Folding Reaction",
        default=100.0, #Change
        minimum=50.0,
        maximum=1000.0
    )

    # Allow Tip Refill
    parameters.add_bool(
        variable_name="tip_refill",
        display_name="Allow Tip Refill",
        description="Allow protocol to pause to manually refill tips",
        default = True,
    )

    # simulate_use: "freeform_profile"
    parameters.add_str(
        variable_name="thermocycler_protocol",
        display_name="Thermocycler Protocol",
        description="Choose Between a 14-hour and Overnight Folding Protocol",
        choices=[
            {"display_name": "14-Hour Freeform", "value": "freeform_profile"},
            {"display_name": "Overnight Folding Protocol", "value": "overnight_profile"},
        ],
        default="freeform_profile",
    )

def calculate_tips(transfers):
    """
    Calculates the number of tips used in the protocol, assuming only single transfers
    and returns the number of 1000ul tip boxes needed
    :argument: list of transfers (np array)
    :return: number of 1000ul tip boxes (int)
    """
    total_tips_1000 = sum(1 for row in transfers)
    return math.ceil(total_tips_1000 / 96)


def run(protocol: protocol_api.ProtocolContext):
    # Add Runtime Parameters
    try:
        csv_data = protocol.params.transfer_csv.parse_as_csv()
    except:
        with open(r"C:\Users\seram\Downloads\Opentron Automation\gear_track_csv_PS_WS_prep.csv") as csv_file:
            csv_data = [line.split(',') for line in csv_file.read().strip().splitlines()]
            # splitlines() rows into ist, strip() removes newline, .split()

    thermocycler_protocol = protocol.params.thermocycler_protocol
    thermocycler_module_1 = protocol.load_module("thermocyclerModuleV2", "B1")
    thermocycler_module_1.open_lid() # Load the PCR plate here before starting the protocol

    # Fisher Scientific Plates
    CUSTOM_LABWARE = json.loads(
        """{"custom_beta/fisherscientific_96_wellplate_1200ul/1":{"ordering":[["A1","B1","C1","D1","E1","F1","G1","H1"],["A2","B2","C2","D2","E2","F2","G2","H2"],["A3","B3","C3","D3","E3","F3","G3","H3"],["A4","B4","C4","D4","E4","F4","G4","H4"],["A5","B5","C5","D5","E5","F5","G5","H5"],["A6","B6","C6","D6","E6","F6","G6","H6"],["A7","B7","C7","D7","E7","F7","G7","H7"],["A8","B8","C8","D8","E8","F8","G8","H8"],["A9","B9","C9","D9","E9","F9","G9","H9"],["A10","B10","C10","D10","E10","F10","G10","H10"],["A11","B11","C11","D11","E11","F11","G11","H11"],["A12","B12","C12","D12","E12","F12","G12","H12"]],"brand":{"brand":"Fisher Scientific","brandId":["SP-1081"]},"metadata":{"displayName":"Fisher Scientific 96 Well Plate 1200 µL","displayCategory":"wellPlate","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.76,"yDimension":85.48,"zDimension":42.5},"wells":{"A1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":74.24,"z":3.15},"B1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":65.24,"z":3.15},"C1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":56.24,"z":3.15},"D1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":47.24,"z":3.15},"E1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":38.24,"z":3.15},"F1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":29.24,"z":3.15},"G1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":20.24,"z":3.15},"H1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":11.24,"z":3.15},"A2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":74.24,"z":3.15},"B2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":65.24,"z":3.15},"C2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":56.24,"z":3.15},"D2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":47.24,"z":3.15},"E2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":38.24,"z":3.15},"F2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":29.24,"z":3.15},"G2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":20.24,"z":3.15},"H2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":11.24,"z":3.15},"A3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":74.24,"z":3.15},"B3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":65.24,"z":3.15},"C3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":56.24,"z":3.15},"D3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":47.24,"z":3.15},"E3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":38.24,"z":3.15},"F3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":29.24,"z":3.15},"G3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":20.24,"z":3.15},"H3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":11.24,"z":3.15},"A4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":74.24,"z":3.15},"B4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":65.24,"z":3.15},"C4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":56.24,"z":3.15},"D4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":47.24,"z":3.15},"E4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":38.24,"z":3.15},"F4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":29.24,"z":3.15},"G4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":20.24,"z":3.15},"H4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":11.24,"z":3.15},"A5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":74.24,"z":3.15},"B5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":65.24,"z":3.15},"C5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":56.24,"z":3.15},"D5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":47.24,"z":3.15},"E5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":38.24,"z":3.15},"F5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":29.24,"z":3.15},"G5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":20.24,"z":3.15},"H5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":11.24,"z":3.15},"A6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":74.24,"z":3.15},"B6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":65.24,"z":3.15},"C6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":56.24,"z":3.15},"D6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":47.24,"z":3.15},"E6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":38.24,"z":3.15},"F6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":29.24,"z":3.15},"G6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":20.24,"z":3.15},"H6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":11.24,"z":3.15},"A7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":74.24,"z":3.15},"B7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":65.24,"z":3.15},"C7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":56.24,"z":3.15},"D7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":47.24,"z":3.15},"E7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":38.24,"z":3.15},"F7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":29.24,"z":3.15},"G7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":20.24,"z":3.15},"H7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":11.24,"z":3.15},"A8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":74.24,"z":3.15},"B8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":65.24,"z":3.15},"C8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":56.24,"z":3.15},"D8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":47.24,"z":3.15},"E8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":38.24,"z":3.15},"F8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":29.24,"z":3.15},"G8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":20.24,"z":3.15},"H8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":11.24,"z":3.15},"A9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":74.24,"z":3.15},"B9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":65.24,"z":3.15},"C9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":56.24,"z":3.15},"D9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":47.24,"z":3.15},"E9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":38.24,"z":3.15},"F9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":29.24,"z":3.15},"G9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":20.24,"z":3.15},"H9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":11.24,"z":3.15},"A10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":74.24,"z":3.15},"B10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":65.24,"z":3.15},"C10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":56.24,"z":3.15},"D10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":47.24,"z":3.15},"E10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":38.24,"z":3.15},"F10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":29.24,"z":3.15},"G10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":20.24,"z":3.15},"H10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":11.24,"z":3.15},"A11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":74.24,"z":3.15},"B11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":65.24,"z":3.15},"C11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":56.24,"z":3.15},"D11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":47.24,"z":3.15},"E11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":38.24,"z":3.15},"F11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":29.24,"z":3.15},"G11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":20.24,"z":3.15},"H11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":11.24,"z":3.15},"A12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":74.24,"z":3.15},"B12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":65.24,"z":3.15},"C12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":56.24,"z":3.15},"D12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":47.24,"z":3.15},"E12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":38.24,"z":3.15},"F12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":29.24,"z":3.15},"G12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":20.24,"z":3.15},"H12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":11.24,"z":3.15}},"groups":[{"metadata":{"wellBottomShape":"u"},"wells":["A1","B1","C1","D1","E1","F1","G1","H1","A2","B2","C2","D2","E2","F2","G2","H2","A3","B3","C3","D3","E3","F3","G3","H3","A4","B4","C4","D4","E4","F4","G4","H4","A5","B5","C5","D5","E5","F5","G5","H5","A6","B6","C6","D6","E6","F6","G6","H6","A7","B7","C7","D7","E7","F7","G7","H7","A8","B8","C8","D8","E8","F8","G8","H8","A9","B9","C9","D9","E9","F9","G9","H9","A10","B10","C10","D10","E10","F10","G10","H10","A11","B11","C11","D11","E11","F11","G11","H11","A12","B12","C12","D12","E12","F12","G12","H12"]}],"parameters":{"format":"irregular","quirks":[],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"fisherscientific_96_wellplate_1200ul"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}}}""")

    # Load trash bin
    trash = protocol.load_trash_bin('A3')


    # Load Tip Racks
    # Calculate number of tips used in transfers and number of tip racks
    # Note: For this protocol, we assume all transfers are with 1-channel
    total_tip_racks_1000 = calculate_tips(csv_data[1:])

    # 1000ul Tip Racks
    tip_racks_1000 = [
        protocol.load_labware('opentrons_flex_96_tiprack_1000ul', slot)
        for slot in ['D3', 'C3', 'B3'][:total_tip_racks_1000]
    ]

    # 500ul Tip Racks
    # Note: This protocol does not use any 500ul tips, adjust as needed
    tip_racks_500 = [
        protocol.load_labware('opentrons_flex_96_tiprack_500ul', slot)
        for slot in []
    ]

    pipette_left = protocol.load_instrument(
        'flex_1channel_1000',
        mount='left',
        tip_racks=tip_racks_1000
    )

    # Working Stock Tube Rack
    # Note: Currently uses two tube racks, based on WS_FoldingRxn protocol
    tube_rack_1 = protocol.load_labware(
        "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
        location="C1",
        label="Working Stock Tube Rack",
        namespace="opentrons",
        version=3,
    )

    # Prestock and WS Reagents Tube Rack
    tube_rack_2 = protocol.load_labware(
        "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
        location="D1",
        label="Pre-Stock Tube Rack",
        namespace="opentrons",
        version=3,
    )

    # Folding Plate
    well_plate_1 = thermocycler_module_1.load_labware(
        "nest_96_wellplate_100ul_pcr_full_skirt",
    )

    # Liquid Definitions
    liquid_1 = protocol.define_liquid(
        "Water",
        description = "water",
        display_color="#9dffd8",
    )
    liquid_2 = protocol.define_liquid(
        "MgCl",
        description="200nM MgCl",
        display_color="#ff80f5",
    )
    liquid_3 = protocol.define_liquid(
        "FOB",
        description="10x FOB",
        display_color="#7eff42",
    )
    liquid_4 = protocol.define_liquid(
        "Scaffold",
        description="100nM Scaffold",
        display_color="#ff4f4f",
    )

    # TODO: Load Working Stock liquids from CSV sheet
    # load working stock reagents into tube rack (Default 200ul)

    # Load Water
    tube_rack_2.load_liquid(
        wells = ["D1"],
        liquid = liquid_1,
        volume = 1000
    )

    #Load MgCl2
    tube_rack_2.load_liquid(
        wells=["D2"],
        liquid=liquid_2,
        volume=1000
    )

    #Load FOB
    tube_rack_2.load_liquid(
        wells=["D3"],
        liquid=liquid_3,
        volume=1000
    )

    #Load Scaffold
    tube_rack_2.load_liquid(
        wells=["D4"],
        liquid=liquid_4,
        volume=1000
    )


    # Set source and destination racks
    source = tube_rack_2
    dest = tube_rack_1

    # Create transfer objects
    transfers = read_transfers(csv_data)
    # Establish working stock wells
    last_ws_well = transfers[-1].dest_well
    ws_wells = expand_well_range("A1", last_ws_well)

    # For the WS tubes located in the first two rows, create matching Folding Reaction tubes in the 2nd two rows
    map = {"A": "C", "B":"D"}
    rxn_wells = [map[well[0]] + well[1:] for well in ws_wells]

    # Begin Making Folding Reactions
    source = tube_rack_2
    dest = tube_rack_1

    ref_rxn_vol = 100
    print(protocol.params.folding_reaction_volume)
    rxn_vol_ratio = protocol.params.folding_reaction_volume/ref_rxn_vol
    # Add Water
    pipette_left.transfer(
        volume=50*rxn_vol_ratio +5,
        source=source.wells_by_name()["D1"],
        dest=[dest.wells_by_name()[well] for well in rxn_wells],
        new_tip='once'
    )
    protocol.comment(f">>Added ddH2O to {[dest.wells_by_name()[well] for well in rxn_wells]}")

    # TODO: Add method for different magnesium concentrations
    # Add MgCl
    pipette_left.transfer(
        volume=10*rxn_vol_ratio,
        source=source.wells_by_name()["D2"],
        dest=[dest.wells_by_name()[well] for well in rxn_wells],
        new_tip='always'
    )
    protocol.comment(f">>Added MgCl2 to {[dest.wells_by_name()[well] for well in rxn_wells]}")

    # Add 10X FOB
    pipette_left.transfer(
        volume=10*rxn_vol_ratio,
        source=source.wells_by_name()["D3"],
        dest=[dest.wells_by_name()[well] for well in rxn_wells],
        new_tip='always'
    )
    protocol.comment(f">>Added 10X FOB to {[dest.wells_by_name()[well] for well in rxn_wells]}")

    # Add 100nM Scaffold
    pipette_left.transfer(
        volume=10*rxn_vol_ratio,
        source=source.wells_by_name()["D4"],
        dest=[dest.wells_by_name()[well] for well in rxn_wells],
        new_tip='always'
    )
    protocol.comment(f">>Added 100nM Scaffold from {[source.wells_by_name()[well] for well in ws_wells]} to {[dest.wells_by_name()[well] for well in rxn_wells]}")

    source = tube_rack_1
    # Add 20ul Staple Mix (from WS row to Rxn row on same tube rack)
    pipette_left.transfer(
            volume= 20*rxn_vol_ratio,
            source=[source.wells_by_name()[well] for well in ws_wells],
            dest=[dest.wells_by_name()[well] for well in rxn_wells],
            new_tip='always'
    )
    protocol.comment(f">>Added Staple Mix from {[source.wells_by_name()[well] for well in ws_wells]} to {[dest.wells_by_name()[well] for well in rxn_wells]}")

    # Update Source and Destination
    source = tube_rack_1
    destination = well_plate_1

    # Create mapping to transfer 50ul each of folding reaction form eppendorf tube to
    # thermocycler plate. (ex. A1 (200ul source) -> A1, B1 (100ul each)
    rack_to_plate = {"C": ["C", "D"], "D": ["E", "F"]}  ## TODO: Fix this!

    # Update the starting location to add samples to the folding reaction plate based on what wells have already been used.
    first_open_well = protocol.params.folding_plate_start_well # e.g. "A1"

    # Create list of wells to distribute 100ul into each well per Folding Reaction
    start_row = first_open_well[0]
    start_col = int(first_open_well[1:])

    dispense_vol = 100
    for well in rxn_wells:

        source_row = well[0]
        row_1, row_2 = rack_to_plate[source_row]

        reaction_volume = float(protocol.params.folding_reaction_volume) # user defined per reaction
        wells_needed = math.ceil(reaction_volume / dispense_vol)
        dest_wells = []
        col = start_col
        i = 0
        while len(dest_wells) < wells_needed:
            if i % 2 == 0:
                dest_wells.append(f"{row_1}{col}")
            else:
                dest_wells.append(f"{row_2}{col}")
                col += 1
            i += 1

    pipette_left.distribute(
        volume=dispense_vol,
        source=source.wells_by_name()[well],
        dest=[destination.wells_by_name()[w] for w in dest_wells],
        new_tip="always"
    )


    protocol.pause("Remove reagents and begin folding ramp.")

    thermocycler_module_1.close_lid()
    thermocycler_module_1.set_lid_temperature(95)

    profile_dict = {}
    # Change these based on your protocol, or add more options

    # Kehao: 14-Hour Freeform Protocol
    freeform_profile = [
        {"temperature": 65, "hold_time_minutes": 15},
        {"temperature": 64, "hold_time_minutes": 3},
        {"temperature": 63, "hold_time_minutes": 3},
        {"temperature": 62, "hold_time_minutes": 3},
        {"temperature": 61, "hold_time_minutes": 3},
        {"temperature": 60, "hold_time_minutes": 5},
        {"temperature": 59, "hold_time_minutes": 10},
        {"temperature": 58, "hold_time_minutes": 10},
        {"temperature": 57, "hold_time_minutes": 10},
        {"temperature": 56, "hold_time_minutes": 25},
        {"temperature": 55, "hold_time_minutes": 30},
        {"temperature": 54, "hold_time_minutes": 45},
        {"temperature": 53, "hold_time_minutes": 60},
        {"temperature": 52, "hold_time_minutes": 60},
        {"temperature": 51, "hold_time_minutes": 60},
        {"temperature": 50, "hold_time_minutes": 60},
        {"temperature": 49, "hold_time_minutes": 60},
        {"temperature": 48, "hold_time_minutes": 42},
        {"temperature": 47, "hold_time_minutes": 42},
        {"temperature": 46, "hold_time_minutes": 42},
        {"temperature": 45, "hold_time_minutes": 42},
        {"temperature": 44, "hold_time_minutes": 36},
        {"temperature": 43, "hold_time_minutes": 32},
        {"temperature": 42, "hold_time_minutes": 32},
        {"temperature": 41, "hold_time_minutes": 20},
        {"temperature": 40, "hold_time_minutes": 20},
        {"temperature": 39, "hold_time_minutes": 20},
        {"temperature": 38, "hold_time_minutes": 15},
        {"temperature": 37, "hold_time_minutes": 10},
        {"temperature": 36, "hold_time_minutes": 5},
        {"temperature": 35, "hold_time_minutes": 5},
        {"temperature": 34, "hold_time_minutes": 22},
        {"temperature": 33, "hold_time_minutes": 22},
        {"temperature": 32, "hold_time_minutes": 2},
        {"temperature": 31, "hold_time_minutes": 2},
        {"temperature": 30, "hold_time_minutes": 2},
    ]
    profile_dict["freeform_profile"] = freeform_profile

    # Kehao: 24-Hour Overnight Protocol
    overnight_profile = [
        {"temperature": 70, "hold_time_minutes": 30},
        {"temperature": 69, "hold_time_minutes": 3},
        {"temperature": 68, "hold_time_minutes": 3},
        {"temperature": 67, "hold_time_minutes": 3},
        {"temperature": 66, "hold_time_minutes": 3},
        {"temperature": 65, "hold_time_minutes": 3},
        {"temperature": 65, "hold_time_minutes": 3},
        {"temperature": 64, "hold_time_minutes": 3},
        {"temperature": 63, "hold_time_minutes": 3},
        {"temperature": 62, "hold_time_minutes": 3},
        {"temperature": 61, "hold_time_minutes": 6},
        {"temperature": 60, "hold_time_minutes": 10},
        {"temperature": 59, "hold_time_minutes": 20},
        {"temperature": 58, "hold_time_minutes": 20},
        {"temperature": 57, "hold_time_minutes": 20},
        {"temperature": 56, "hold_time_minutes": 50},
        {"temperature": 55, "hold_time_minutes": 60},
        {"temperature": 54, "hold_time_minutes": 90},
        {"temperature": 53, "hold_time_minutes": 120},
        {"temperature": 52, "hold_time_minutes": 120},
        {"temperature": 51, "hold_time_minutes": 120},
        {"temperature": 50, "hold_time_minutes": 120},
        {"temperature": 49, "hold_time_minutes": 120},
        {"temperature": 48, "hold_time_minutes": 84},
        {"temperature": 47, "hold_time_minutes": 84},
        {"temperature": 46, "hold_time_minutes": 84},
        {"temperature": 45, "hold_time_minutes": 42},
        {"temperature": 44, "hold_time_minutes": 36},
        {"temperature": 43, "hold_time_minutes": 32},
        {"temperature": 42, "hold_time_minutes": 32},
        {"temperature": 41, "hold_time_minutes": 20},
        {"temperature": 40, "hold_time_minutes": 20},
        {"temperature": 39, "hold_time_minutes": 20},
        {"temperature": 38, "hold_time_minutes": 15},
        {"temperature": 37, "hold_time_minutes": 10},
        {"temperature": 36, "hold_time_minutes": 5},
        {"temperature": 35, "hold_time_minutes": 5},
        {"temperature": 34, "hold_time_minutes": 22},
        {"temperature": 33, "hold_time_minutes": 22},
        {"temperature": 32, "hold_time_minutes": 2},
        {"temperature": 31, "hold_time_minutes": 2},
        {"temperature": 30, "hold_time_minutes": 2},
    ]
    profile_dict["overnight_profile"]=overnight_profile

    thermocycler_module_1.execute_profile(
        steps = profile_dict[thermocycler_protocol],
        repetitions=1,
        block_max_volume=50,
    )
    thermocycler_module_1.set_block_temperature(20, hold_time_minutes=120)


