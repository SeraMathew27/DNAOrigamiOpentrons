from typing import List
import itertools

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


def set_source_plate_slots(names) -> dict[str, str]:
    source_slots = ['A2', 'B2', 'C2', 'D2']
    source_plate_names = set(names)  # CHECK IF THIS WORKS
    # TODO: Check
    pairs = dict(itertools.zip_longest(source_slots, source_plate_names))
    filtered = {slot: plate for slot, plate in pairs.items() if plate is not None}
    source_plates_slots = {plate: slot for slot, plate in filtered.items()}

    return source_plates_slots

names = ['OMD1', 'OMD2', 'OMD1']
print(set_source_plate_slots(names))


tip_racks_1000 = [
        protocol.load_labware('opentrons_flex_96_tiprack_1000ul', slot)
        for slot in ['B3', 'C3', 'D3'][:total_tip_racks_1000]
    ]

table = [["Str", "Str", "A1", "A12"], ["Str", "Str", "B1", "B11"], ["Str", "Str", "C1", "C1"]]
list = [expand_well_range(row[2], row[3]) for row in table]
print(list)

