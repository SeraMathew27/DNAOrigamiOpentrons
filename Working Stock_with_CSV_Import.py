from opentrons import protocol_api
import math
from dataclasses import dataclass
from typing import Union, List

metadata = {
    'protocolName': 'Working Stock Preparation with CSV Import',
    'author': 'Sera Mathew, OpentronsAI',
    'description': (
        'Use CSV import to pool prestocks into working stock tubes. '
        'Supports creating variations of multiple structures.'
    ),
}

requirements = {
    'robotType': 'Flex',
    'apiLevel': '2.25'
}

# Expected CSV column headers — order matters
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
    ws_name: str     # Name of the working stock this transfer belongs to
    ps_name: str     # Name of the prestock part (or "Water" for water additions)
    ps_well: str     # Source well in the prestock rack
    num_oligos: int  # Number of oligos in this prestock
    dest_well: str   # Destination well in the working stock rack
    volume: float    # Volume to transfer in uL


def read_transfers(csv_data: List[List[Union[str, int, float]]]) -> List[Transfer]:
    """
    Converts CSV rows into Transfer objects for use during the run.
    Skips the header row and parses each data row into a Transfer.
    """
    headers = csv_data[0]
    assert headers == HEADERS, f"CSV header mismatch.\nExpected: {HEADERS}\nGot: {headers}"

    transfers = []
    for row in csv_data[1:]:
        transfer = Transfer(
            ws_name=row[0],
            ps_name=row[1],
            ps_well=row[2],
            num_oligos=int(row[3]),
            dest_well=row[5],
            volume=float(row[4])
        )
        transfers.append(transfer)
    return transfers


def expand_well_range(start_well: str, end_well: str) -> list:
    """
    Expands a well range (e.g. 'A1' to 'B3') into a list of individual wells
    in row-major order (A1, A2, ... A12, B1, B2, ...), matching standard
    96-well plate layout.
    Returns an empty list if start_well is empty.
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
    Returns the number of 1000uL tip racks needed for the protocol.
    Assumes one tip per transfer row.
    """
    return math.ceil(len(transfers) / 96)


def validate_transfers(transfers: List[Transfer]):
    """
    Checks transfer data for common errors before the run starts.
    Raises ValueError with a descriptive message if any issue is found.
    """
    valid_rack_wells = {f"{r}{c}" for r in "ABCD" for c in range(1, 7)}

    for i, t in enumerate(transfers):
        row_num = i + 2  # account for header row

        if not t.ps_well and t.ps_name != "Water":
            raise ValueError(f"Row {row_num}: Prestock well is empty for part '{t.ps_name}'.")

        if t.dest_well not in valid_rack_wells:
            raise ValueError(
                f"Row {row_num}: Destination well '{t.dest_well}' is not valid for a 24-tube rack."
            )

        if t.volume <= 0:
            raise ValueError(f"Row {row_num}: Transfer volume must be positive, got {t.volume}.")


def add_parameters(parameters: protocol_api.ParameterContext):
    """Add runtime parameters to the protocol."""

    # simulate-use: "C:\Users\seram\Downloads\WS_Prep_Track(Working Stock).csv"
    parameters.add_csv_file(
        variable_name="transfer_csv",
        display_name="Transfer CSV File",
        description="Working Stock, Part, Prestock Well, Num Oligos, Transfer Volume, Destination Tube, Working Stock Volume"
    )

    # simulate-use: 200.0
    parameters.add_float(
        variable_name="working_stock_volume",
        display_name="Working Stock Volume",
        description="Total volume of each working stock tube (uL)",
        default=200.0,
        minimum=100.0,
        maximum=1000.0
    )

    # simulate-use: left
    parameters.add_str(
        variable_name="pipette_mount",
        display_name="1000uL Pipette Mount",
        description="Mount location of the 1000uL pipette",
        default="left",
        choices=[
            {"display_name": "Left", "value": "left"},
            {"display_name": "Right", "value": "right"}
        ]
    )

    # Allow Tip Refill
    parameters.add_bool(
        variable_name="tip_refill",
        display_name="Allow Tip Refill",
        description="Allow protocol to pause to manually refill tips",
        default=True,
    )


def run(protocol: protocol_api.ProtocolContext):

    # --- Parse and validate CSV ---
    csv_data = protocol.params.transfer_csv.parse_as_csv()

    # Strip BOM character if present (common in Windows-exported CSVs)
    if csv_data[0][0].startswith("\ufeff"):
        csv_data[0][0] = csv_data[0][0][1:]

    transfers = read_transfers(csv_data)
    validate_transfers(transfers)

    # --- Tip rack setup ---
    total_tip_racks = calculate_tips(transfers)
    available_slots = ['D3', 'C3', 'B3']
    num_to_load = min(total_tip_racks, len(available_slots))

    tip_racks_1000 = [
        protocol.load_labware('opentrons_flex_96_tiprack_1000ul', slot)
        for slot in available_slots[:num_to_load]
    ]

    # --- Pipette setup ---
    pipette = protocol.load_instrument(
        'flex_1channel_1000',
        mount=protocol.params.pipette_mount,
        tip_racks=tip_racks_1000
    )

    # --- Load trash ---
    trash = protocol.load_trash_bin('A3')

    # --- Load labware ---

    # Working stock destination rack (rows A-B used for working stocks)
    tube_rack_ws = protocol.load_labware(
        "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
        location="C1",
        label="Working Stock Tube Rack",
        namespace="opentrons",
        version=3,
    )

    # Prestock source rack and reagents rack (rows C-D used for water, MgCl2, FOB, scaffold)
    tube_rack_ps = protocol.load_labware(
        "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
        location="D1",
        label="Pre-Stock and Reagents Rack",
        namespace="opentrons",
        version=3,
    )

    # --- Liquid definitions for deck visualisation ---
    liquid_water = protocol.define_liquid("Water", description="ddH2O", display_color="#9dffd8")
    liquid_mgcl = protocol.define_liquid("MgCl2", description="200mM MgCl2", display_color="#ff80f5")
    liquid_fob = protocol.define_liquid("FOB", description="10x FOB", display_color="#7eff42")
    liquid_scaffold = protocol.define_liquid("Scaffold", description="100nM Scaffold", display_color="#ff4f4f")

    # Load reagent volumes into prestock rack (wells D1-D4)
    tube_rack_ps.load_liquid(wells=["D1"], liquid=liquid_water, volume=1000)
    tube_rack_ps.load_liquid(wells=["D2"], liquid=liquid_mgcl, volume=1000)
    tube_rack_ps.load_liquid(wells=["D3"], liquid=liquid_fob, volume=1000)
    tube_rack_ps.load_liquid(wells=["D4"], liquid=liquid_scaffold, volume=1000)

    # --- Confirm deck layout before starting ---
    protocol.pause(
        f"Confirm deck layout: "
        f"Prestock + Reagents rack at D1 (Water=D1, MgCl2=D2, FOB=D3, Scaffold=D4), "
        f"Working Stock rack at C1. "
        f"Tip racks loaded at {available_slots[:num_to_load]}. "
        f"Press continue to start."
    )

    # --- Working stock transfers ---
    # Water is handled separately with a mix step after addition.
    # All other rows are straightforward prestock-to-working-stock transfers.
    for transfer in transfers:

        if transfer.ps_name == "Water":
            # Add water first so it's ready to mix after all prestocks are added
            pipette.transfer(
                volume=transfer.volume,
                source=tube_rack_ps.wells_by_name()["D1"],
                dest=tube_rack_ws.wells_by_name()[transfer.dest_well],
                new_tip='always'
            )
            # Mix to ensure even distribution after water addition
            pipette.pick_up_tip()
            pipette.mix(
                repetitions=3,
                location=tube_rack_ws.wells_by_name()[transfer.dest_well],
                volume=100,
            )
            pipette.drop_tip()

        else:
            # Standard prestock transfer: one tip per transfer to avoid cross-contamination
            pipette.transfer(
                volume=transfer.volume,
                source=tube_rack_ps.wells_by_name()[transfer.ps_well],
                dest=tube_rack_ws.wells_by_name()[transfer.dest_well],
                new_tip='always'
            )

        protocol.comment(
            f"Transferred {transfer.volume} uL of '{transfer.ps_name}' "
            f"to {transfer.ws_name} working stock at well {transfer.dest_well}"
        )

    protocol.pause(
        "Working stock preparation complete. "
        "Verify working stock tubes before proceeding to folding reaction setup."
    )