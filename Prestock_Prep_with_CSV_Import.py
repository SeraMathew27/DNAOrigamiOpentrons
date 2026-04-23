

from opentrons import protocol_api
import math
import json
from dataclasses import dataclass
from typing import Union, Any, List
import itertools
import csv


# TODO: Check if labware names give Protocol Designer and issue with uploads

metadata = {
    'protocolName': 'Prestock Preparation with CSV import',
    'author': 'Sera Mathew, OpentronsAI',
    'description': 'Use CSV import to pool oligonucleotides from source plates to Eppendorf tubes to create prestocks for origami components',
}

requirements = {
    'robotType': 'Flex',
    'apiLevel': '2.25'
}

# Define the expected headers for the CSV file
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
    destination_slot: str = "D1" # For prestock transfer

    def set_source_slot(self, source_plate_slots: dict[str, str]):
        """
        Set the source slot for this transfer from mapping of source plate names to slot on deck
        :param source_plate_slots: dictionary of source plate slots to plate names
        """
        try:
            self.source_slot = source_plate_slots[self.source_name]
        except KeyError:
            raise KeyError(f"Source plate '{self.source_name}' not found in plate mapping")

@dataclass
class Prestock:
    ps_name: str
    tube_location: str
    volume: float
    num_oligos: int

    def update_volume(self, transfer_amount: float):
        if transfer_amount < 0:
            raise ValueError("transfer_amount must be non-negative")
        if transfer_amount > self.volume:
            raise ValueError("transfer_amount exceeds current volume")
        self.volume -= transfer_amount
        return self.volume


# Need to fix source labware
def parse_csv_as_lists(
        file_path: str,
        detect_dialect: bool = True,
        **kwargs: Any,
) -> List[List[str]]:
    """Parse a CSV file into List[List[str]], mimicking CSVParameter.parse_as_csv()."""
    with open(file_path, "r", encoding="utf-8", newline="") as f:
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

        # Remove trailing empty rows
    while rows and rows[-1] == []:
        rows.pop()
    return rows


def read_transfers(csv_data:List[List[Union[str, int, float]]], src_labware, src_slot: dict[str,str]) -> List[Transfer]:
    """
    Converts list of transfers into a list of Transfer objects so that each unique transfer has
    addressable properties that will be called during the run. Also creates a prestock object
    which is like a simplified transfer object.
    """

    # Check if headers match the correct file formate
    headers = csv_data[0]
    assert headers == HEADERS, f"Expected: {HEADERS}, got: {headers}"
    #TODO: Validate Data


    transfers = []
    transfer_data = csv_data[1:]
    for row in transfer_data:

        transfer = Transfer(
            source_name=row[0],
            source_part=row[1],
            source_labware = src_labware,
            source_well = expand_well_range(row[2], row[3]),
            dest_name = row[4],
            dest_well = row[5],
            volume = float(row[6]),
            source_slot = src_slot[row[0]]
        )
        transfers.append(transfer)
    return transfers


# TODO:
def add_parameters(parameters: protocol_api.ParameterContext):
    """
    Add runtime parameters to protocol
    """
    # Input CSV file
    # simulate-use: "C:\Users\seram\Downloads\PS_WS_prep_Remaining_Track(Prestock).csv"
    parameters.add_csv_file(
        variable_name="transfer_csv",
        display_name="Transfer CSV File",
        description="SOURCE PLATE, PART, WELL START, WELL END, DESTINATION RACK, DESTINATION WELL, VOLUME"
    )


    # Input Source Plate Type
    # simulate-use: fisherscientific_96_wellplate_1200ul
    parameters.add_str(
        variable_name="source_labware",
        display_name="Source Labware",
        description="Select source plate model",
        default="fisherscientific_96_wellplate_1200ul",
        choices=[{"display_name": "ThermoScientific 1200ul", "value": "fisherscientific_96_wellplate_1200ul"}]
    )

    # Input Transfer Volume
    # simulate-use: 5.0
    parameters.add_float(
        variable_name="transfer_volume",
        display_name="Transfer Volume",
        description="Volume to transfer from source plate to prestock tube (uL)",
        default = 5.0,
        minimum = 1.0,
        maximum = 10.0
    )

    # Allow Tip Refill
    # parameters.add_bool(
    #     variable_name="tip_refill",
    #     display_name="Allow Tip Refill",
    #     description="Allow protocol to pause to manually refill tips",
    #     default = True,
    # )

def set_source_plate_slots(csv_data: List[List[str]]) -> dict[str, str]:
    source_slots = ['D2', 'C2', 'B2', 'A2']
    source_plate_names = {row[0]: 0 for row in csv_data[1:]} #



    print(list(source_plate_names.keys()))

    source_plates_slots = {}

    # Iterate through the source_plate_names and assign locations to a repeating list
    for i, plate in enumerate(source_plate_names.keys()):
        source_plates_slots[plate] = source_slots[i % len(source_slots)]

    return source_plates_slots

def expand_well_range(start_well, end_well):
    """
    Expands a well range (e.g., 'A1' to 'B12') into a list of individual wells.
    Assumes standard 96-well plate format (A-H rows, 1-12 columns).
    """
    # Parse start well
    wells = []

    # Water does not have a start location, so ignore empty cell
    if (start_well != ''):
        # Parse start well
        start_row = ord(start_well[0]) - ord('A')  # Convert letter to number (A=0, B=1, etc.)
        start_col = int(start_well[1:]) - 1  # Convert to 0-indexed

        # Parse end well
        end_row = ord(end_well[0]) - ord('A')
        end_col = int(end_well[1:]) - 1

        # Generate list of wells

        for row in range(start_row, end_row):
            for col in range(12):
                well_name = f"{chr(ord('A') + row)}{col + 1}"
                wells.append(well_name)
        for col in range(0, end_col + 1):
            well_name = f"{chr(ord('A') + end_row)}{col + 1}"
            wells.append(well_name)

    return wells

def calculate_tips(transfers):
    """
    Calculates the number of tips used in the protocol, assuming only single transfers
    and returns the number of 1000ul tip boxes needed
    :argument: list of transfers (np array)
    :return: number of 1000ul tip boxes (int)
    """

    total_tips_1000 = sum(len(expand_well_range(row[2], row[3]))for row in transfers)

    return math.ceil(total_tips_1000 / 96)

def update_deck(on_deck_plates, off_deck_plates, on_deck_tips, off_deck_tips, protocol):
    """
    Once all the plates on the deck have been used and tip boxes are empty
    replaces on_deck_plates and its corresponding tips with new plates and tips from
    off the deck
    
    :param on_deck_plates:
    :param off_deck_plates:
    :param on_deck_tips:
    :param off_deck_tips:
    :return:
    """

    ps_rack_location = "4"
    for slot in protocol.loaded_labware.keys():
        labware_at_slot = str(protocol.deck[slot]) # Returns labware or none if empty
        #
        if labware_at_slot != 'None' and slot != ps_rack_location:
            protocol.move_labware(labware = labware_at_slot, location = slot)


# TODO: def validate_data_rows(data_rows):
"""
for each row, ensure row length matches # of headers or locate rows with empty
values (destination, source etc.) 
"""


def run(protocol: protocol_api.ProtocolContext):
    # Input runtime arguments

    source_labware = protocol.params.source_labware

    csv_data = protocol.params.transfer_csv.parse_as_csv()
    csv_data = [row[:7] for row in csv_data]
    if csv_data[0][0].startswith("\ufeff"):
        csv_data[0][0] = csv_data[0][0][1:]  # Removes \ufeff (BOM) character

    # Fisher Scientific Plates
    CUSTOM_LABWARE = json.loads(
        """{"custom_beta/fisherscientific_96_wellplate_1200ul/1":{"ordering":[["A1","B1","C1","D1","E1","F1","G1","H1"],["A2","B2","C2","D2","E2","F2","G2","H2"],["A3","B3","C3","D3","E3","F3","G3","H3"],["A4","B4","C4","D4","E4","F4","G4","H4"],["A5","B5","C5","D5","E5","F5","G5","H5"],["A6","B6","C6","D6","E6","F6","G6","H6"],["A7","B7","C7","D7","E7","F7","G7","H7"],["A8","B8","C8","D8","E8","F8","G8","H8"],["A9","B9","C9","D9","E9","F9","G9","H9"],["A10","B10","C10","D10","E10","F10","G10","H10"],["A11","B11","C11","D11","E11","F11","G11","H11"],["A12","B12","C12","D12","E12","F12","G12","H12"]],"brand":{"brand":"Fisher Scientific","brandId":["SP-1081"]},"metadata":{"displayName":"Fisher Scientific 96 Well Plate 1200 µL","displayCategory":"wellPlate","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.76,"yDimension":85.48,"zDimension":42.5},"wells":{"A1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":74.24,"z":3.15},"B1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":65.24,"z":3.15},"C1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":56.24,"z":3.15},"D1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":47.24,"z":3.15},"E1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":38.24,"z":3.15},"F1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":29.24,"z":3.15},"G1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":20.24,"z":3.15},"H1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":11.24,"z":3.15},"A2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":74.24,"z":3.15},"B2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":65.24,"z":3.15},"C2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":56.24,"z":3.15},"D2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":47.24,"z":3.15},"E2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":38.24,"z":3.15},"F2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":29.24,"z":3.15},"G2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":20.24,"z":3.15},"H2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":11.24,"z":3.15},"A3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":74.24,"z":3.15},"B3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":65.24,"z":3.15},"C3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":56.24,"z":3.15},"D3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":47.24,"z":3.15},"E3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":38.24,"z":3.15},"F3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":29.24,"z":3.15},"G3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":20.24,"z":3.15},"H3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":11.24,"z":3.15},"A4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":74.24,"z":3.15},"B4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":65.24,"z":3.15},"C4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":56.24,"z":3.15},"D4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":47.24,"z":3.15},"E4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":38.24,"z":3.15},"F4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":29.24,"z":3.15},"G4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":20.24,"z":3.15},"H4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":11.24,"z":3.15},"A5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":74.24,"z":3.15},"B5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":65.24,"z":3.15},"C5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":56.24,"z":3.15},"D5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":47.24,"z":3.15},"E5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":38.24,"z":3.15},"F5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":29.24,"z":3.15},"G5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":20.24,"z":3.15},"H5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":11.24,"z":3.15},"A6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":74.24,"z":3.15},"B6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":65.24,"z":3.15},"C6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":56.24,"z":3.15},"D6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":47.24,"z":3.15},"E6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":38.24,"z":3.15},"F6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":29.24,"z":3.15},"G6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":20.24,"z":3.15},"H6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":11.24,"z":3.15},"A7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":74.24,"z":3.15},"B7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":65.24,"z":3.15},"C7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":56.24,"z":3.15},"D7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":47.24,"z":3.15},"E7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":38.24,"z":3.15},"F7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":29.24,"z":3.15},"G7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":20.24,"z":3.15},"H7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":11.24,"z":3.15},"A8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":74.24,"z":3.15},"B8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":65.24,"z":3.15},"C8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":56.24,"z":3.15},"D8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":47.24,"z":3.15},"E8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":38.24,"z":3.15},"F8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":29.24,"z":3.15},"G8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":20.24,"z":3.15},"H8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":11.24,"z":3.15},"A9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":74.24,"z":3.15},"B9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":65.24,"z":3.15},"C9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":56.24,"z":3.15},"D9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":47.24,"z":3.15},"E9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":38.24,"z":3.15},"F9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":29.24,"z":3.15},"G9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":20.24,"z":3.15},"H9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":11.24,"z":3.15},"A10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":74.24,"z":3.15},"B10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":65.24,"z":3.15},"C10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":56.24,"z":3.15},"D10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":47.24,"z":3.15},"E10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":38.24,"z":3.15},"F10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":29.24,"z":3.15},"G10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":20.24,"z":3.15},"H10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":11.24,"z":3.15},"A11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":74.24,"z":3.15},"B11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":65.24,"z":3.15},"C11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":56.24,"z":3.15},"D11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":47.24,"z":3.15},"E11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":38.24,"z":3.15},"F11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":29.24,"z":3.15},"G11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":20.24,"z":3.15},"H11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":11.24,"z":3.15},"A12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":74.24,"z":3.15},"B12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":65.24,"z":3.15},"C12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":56.24,"z":3.15},"D12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":47.24,"z":3.15},"E12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":38.24,"z":3.15},"F12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":29.24,"z":3.15},"G12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":20.24,"z":3.15},"H12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":11.24,"z":3.15}},"groups":[{"metadata":{"wellBottomShape":"u"},"wells":["A1","B1","C1","D1","E1","F1","G1","H1","A2","B2","C2","D2","E2","F2","G2","H2","A3","B3","C3","D3","E3","F3","G3","H3","A4","B4","C4","D4","E4","F4","G4","H4","A5","B5","C5","D5","E5","F5","G5","H5","A6","B6","C6","D6","E6","F6","G6","H6","A7","B7","C7","D7","E7","F7","G7","H7","A8","B8","C8","D8","E8","F8","G8","H8","A9","B9","C9","D9","E9","F9","G9","H9","A10","B10","C10","D10","E10","F10","G10","H10","A11","B11","C11","D11","E11","F11","G11","H11","A12","B12","C12","D12","E12","F12","G12","H12"]}],"parameters":{"format":"irregular","quirks":[],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"fisherscientific_96_wellplate_1200ul"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}}}""")

    # Load trash bin
    trash = protocol.load_trash_bin('A3')

    # Load Tip Racks
    # Calculate number of tips used in transfers and number of tip racks
    # Note: For this protocol, we assume all transfers are with 1-channel
    total_tip_racks_1000 = calculate_tips(csv_data[1:])

    # Available slots for 1000 µL tip racks (max 4)
    available_slots_1000 = ['B3', 'C3', 'D3', 'C1']
    num_tip_racks_to_load = min(total_tip_racks_1000, len(available_slots_1000))
    off_deck_tips = total_tip_racks_1000 - num_tip_racks_to_load

    # 1000ul Tip Racks, occupy the far right column and one slot at D1 (bottom left)
    tip_racks_1000 = [
        protocol.load_labware('opentrons_flex_96_tiprack_1000ul', slot)
        for slot in available_slots_1000[:num_tip_racks_to_load]
    ]

    # Load remaining tip racks "Off-Deck"
    load_off_deck = [
        protocol.load_labware('opentrons_flex_96_tiprack_1000ul', protocol_api.OFF_DECK)
        for i in range(off_deck_tips)
    ]

    #Include both on_deck and off deck tip_racks
    tip_racks_1000.extend(load_off_deck)

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

    # Dictionary to store loaded labware
    source_plates = {}
    source_plate_slots = set_source_plate_slots(csv_data)

    # Set starting locations for source plates
    # Plates 1-4 (on-deck) and 5+ are off-deck
    off_deck_plates = []
    for i, (plate, slot) in enumerate(source_plate_slots.items()):
        if i < 4:
            loc = slot
        else:
            loc = protocol_api.OFF_DECK
            off_deck_plates.append(plate) # Add plate to off_deck

        source_plates[plate] = protocol.load_labware_from_definition(
                CUSTOM_LABWARE["custom_beta/fisherscientific_96_wellplate_1200ul/1"],  # Adjust labware type as needed
                location= loc,
                label=plate
        )

    # Prestock Tube Rack and Reagents
    tube_rack_1 = protocol.load_labware(
        "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
        location="D1",
        label="Pre-Stock Tube Rack",
        namespace="opentrons",
        version=3,
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
    # Process csv list into Transfers object with inputted source labware and mapped source slots
    transfers = read_transfers(csv_data, source_labware, source_plate_slots)
    labwares = {slot:item for slot, item in protocol.deck.items()}
    slots_to_remove = ['A1', 'B1', 'A3', 'A4', 'B4', 'C4', 'D4']
    filtered_labwares = {slot:item for slot, item in labwares.items() if slot not in slots_to_remove}
    sorted_labwares = sorted(labwares.items(), key=lambda item: item[0])

    validate_labware = [f"{slot}: {item}" for slot, item in filtered_labwares.items()]

    protocol.pause(f"This protocol requires ({total_tip_racks_1000}) 1000ul tip racks. Press continue to confirm or try protocol again with less transfers.")
    protocol.pause(f"Confirm Deck Layout: {str(validate_labware)}")

    i = 0
    for transfer in transfers:
        # Set source and destination slots
        source = source_plates[transfer.source_name] # Get source plate object
        destination = tube_rack_1

        # Transfer liquid
        pipette_left.transfer(
            volume=transfer.volume,
            source=[source.wells_by_name()[well] for well in transfer.source_well],
            dest=destination.wells_by_name()[transfer.dest_well],
            new_tip='always'
        )

        # If tips run out & plates run out, pause and reconfigure set up (ex. load 4 tip racks and 4 plates.
        # Do a test protocol with just the pause and move
        # protocol.pause("Tips have run out. Please replace with tip boxes and plates from off-deck." source plate to position)
        # For the first four plates, protocol.move_labware(labware=source
        # update off_deck plates
        # move off_deck to on update on_deck plates
        # To put a new tip box inside the robot, print a message

        protocol.comment(
            f"Transferred {transfer.volume} µL from {transfer.source_name} "
            f"wells {transfer.source_well[0]}-{transfer.source_well[-1]} ({len(transfer.source_well)} wells) "
            f"to {transfer.dest_name} well {transfer.dest_well} for {transfer.source_part} prestock"
        )

        i += 1

## Add Pause
    protocol.pause("Continue to make working stock")
