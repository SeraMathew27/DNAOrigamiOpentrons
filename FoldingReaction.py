from opentrons import protocol_api
import math
from dataclasses import dataclass
from typing import Union, List

metadata = {
    'protocolName': 'Folding Reaction',
    'author': 'Sera Mathew, OpentronsAI',
    'description': (
        'Prepare and run DNA origami folding reactions using pre-made working stocks. '
        'Adds buffer, scaffold, and staple mixes to a PCR plate, then runs a thermocycler ramp.'
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

# Reference reaction volume that all reagent ratios are based on.
# Scaling factor is calculated as (user volume / REF_RXN_VOL).
REF_RXN_VOL = 100

# Volume dispensed into each PCR plate well when distributing folding reactions
DISPENSE_VOL_PER_WELL = 100

# Thermocycler profiles — temperatures in °C, hold times in minutes
THERMOCYCLER_PROFILES = {
    # 14-hour freeform ramp (Kehao protocol)
    "freeform_profile": [
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
    ],
    # 24-hour overnight ramp (Kehao protocol)
    "overnight_profile": [
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
    ],
}


@dataclass
class Transfer:
    ws_name: str     # Name of the working stock this transfer belongs to
    ps_name: str     # Name of the prestock part
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
    Returns the number of 1000uL tip racks needed.
    Accounts for one tip per transfer plus reagent additions
    (water, MgCl2, FOB, scaffold, staple mix) per working stock.
    """
    num_working_stocks = len({t.dest_well for t in transfers})
    # 4 reagent transfers per working stock (water uses once tip, MgCl2, FOB, scaffold always)
    # plus staple mix transfer
    reagent_tips = num_working_stocks * 5
    prestock_tips = len(transfers)
    return math.ceil((prestock_tips + reagent_tips) / 96)


def add_parameters(parameters: protocol_api.ParameterContext):
    """Add runtime parameters to the protocol."""

    # simulate-use: "C:\Users\seram\Downloads\WS_Prep_Track(Working Stock).csv"
    parameters.add_csv_file(
        variable_name="transfer_csv",
        display_name="Transfer CSV File",
        description="Working Stock, Part, Prestock Well, Num Oligos, Transfer Volume, Destination Tube, Reaction Volume"
    )

    # simulate-use: A1
    parameters.add_str(
        variable_name="folding_plate_start_well",
        display_name="Folding Plate Start Well",
        description="First open well of the PCR plate to add folding reactions into",
        choices=[
            {"display_name": f"{r}{c}", "value": f"{r}{c}"}
            for r in "ABCDEFGH"
            for c in range(1, 13)
        ],
        default="A1"
    )

    # simulate-use: 100.0
    parameters.add_float(
        variable_name="folding_reaction_volume",
        display_name="Folding Reaction Volume",
        description="Total volume of each folding reaction (uL)",
        default=100.0,
        minimum=50.0,
        maximum=1000.0
    )

    # simulate-use: freeform_profile
    parameters.add_str(
        variable_name="thermocycler_protocol",
        display_name="Thermocycler Protocol",
        description="Choose between the 14-hour freeform and overnight folding protocols",
        choices=[
            {"display_name": "14-Hour Freeform", "value": "freeform_profile"},
            {"display_name": "Overnight Folding Protocol", "value": "overnight_profile"},
        ],
        default="freeform_profile",
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

    parameters.add_bool(
        variable_name="tip_refill",
        display_name="Allow Tip Refill",
        description="Allow protocol to pause to manually refill tips",
        default=True,
    )


def run(protocol: protocol_api.ProtocolContext):

    # --- Parse CSV ---
    csv_data = protocol.params.transfer_csv.parse_as_csv()

    # Strip BOM character if present (common in Windows-exported CSVs)
    if csv_data[0][0].startswith("\ufeff"):
        csv_data[0][0] = csv_data[0][0][1:]

    transfers = read_transfers(csv_data)

    # --- Runtime parameters ---
    thermocycler_protocol = protocol.params.thermocycler_protocol
    folding_reaction_volume = float(protocol.params.folding_reaction_volume)
    rxn_vol_ratio = folding_reaction_volume / REF_RXN_VOL

    # --- Thermocycler setup ---
    # Open lid before run so PCR plate can be loaded manually
    thermocycler = protocol.load_module("thermocyclerModuleV2", "B1")
    thermocycler.open_lid()

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

    # Working stock rack: rows A-B hold working stocks, rows C-D hold folding reactions
    tube_rack_ws = protocol.load_labware(
        "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
        location="C1",
        label="Working Stock Tube Rack",
        namespace="opentrons",
        version=3,
    )

    # Reagents rack: D1=Water, D2=MgCl2, D3=FOB, D4=Scaffold
    tube_rack_reagents = protocol.load_labware(
        "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
        location="D1",
        label="Reagents Rack",
        namespace="opentrons",
        version=3,
    )

    # PCR plate loaded inside thermocycler
    folding_plate = thermocycler.load_labware(
        "nest_96_wellplate_100ul_pcr_full_skirt",
    )

    # --- Liquid definitions for deck visualisation ---
    liquid_water = protocol.define_liquid("Water", description="ddH2O", display_color="#9dffd8")
    liquid_mgcl = protocol.define_liquid("MgCl2", description="200mM MgCl2", display_color="#ff80f5")
    liquid_fob = protocol.define_liquid("FOB", description="10x FOB", display_color="#7eff42")
    liquid_scaffold = protocol.define_liquid("Scaffold", description="100nM Scaffold", display_color="#ff4f4f")

    tube_rack_reagents.load_liquid(wells=["D1"], liquid=liquid_water, volume=1000)
    tube_rack_reagents.load_liquid(wells=["D2"], liquid=liquid_mgcl, volume=1000)
    tube_rack_reagents.load_liquid(wells=["D3"], liquid=liquid_fob, volume=1000)
    tube_rack_reagents.load_liquid(wells=["D4"], liquid=liquid_scaffold, volume=1000)

    # --- Determine working stock and reaction well positions ---
    # Working stocks occupy the first N wells of the rack (rows A-B)
    # Matching folding reaction tubes are in rows C-D of the same rack
    last_ws_well = transfers[-1].dest_well
    ws_wells = expand_well_range("A1", last_ws_well)

    # Map working stock rows (A, B) to their corresponding reaction rows (C, D)
    ws_to_rxn_row = {"A": "C", "B": "D"}
    rxn_wells = [ws_to_rxn_row[well[0]] + well[1:] for well in ws_wells]

    # --- Build folding reaction tubes ---
    # Reagent volumes are all scaled relative to REF_RXN_VOL (100uL)

    # Add water (+5uL overage to account for pipetting loss)
    pipette.transfer(
        volume=(50 * rxn_vol_ratio) + 5,
        source=tube_rack_reagents.wells_by_name()["D1"],
        dest=[tube_rack_ws.wells_by_name()[well] for well in rxn_wells],
        new_tip='once'
    )
    protocol.comment(f"Added ddH2O to reaction wells: {rxn_wells}")

    # Add MgCl2
    pipette.transfer(
        volume=10 * rxn_vol_ratio,
        source=tube_rack_reagents.wells_by_name()["D2"],
        dest=[tube_rack_ws.wells_by_name()[well] for well in rxn_wells],
        new_tip='always'
    )
    protocol.comment(f"Added MgCl2 to reaction wells: {rxn_wells}")

    # Add 10x FOB buffer
    pipette.transfer(
        volume=10 * rxn_vol_ratio,
        source=tube_rack_reagents.wells_by_name()["D3"],
        dest=[tube_rack_ws.wells_by_name()[well] for well in rxn_wells],
        new_tip='always'
    )
    protocol.comment(f"Added 10x FOB to reaction wells: {rxn_wells}")

    # Add scaffold
    pipette.transfer(
        volume=10 * rxn_vol_ratio,
        source=tube_rack_reagents.wells_by_name()["D4"],
        dest=[tube_rack_ws.wells_by_name()[well] for well in rxn_wells],
        new_tip='always'
    )
    protocol.comment(f"Added scaffold to reaction wells: {rxn_wells}")

    # Add staple mix from working stock tubes (rows A-B) into reaction tubes (rows C-D)
    pipette.transfer(
        volume=20 * rxn_vol_ratio,
        source=[tube_rack_ws.wells_by_name()[well] for well in ws_wells],
        dest=[tube_rack_ws.wells_by_name()[well] for well in rxn_wells],
        new_tip='always'
    )
    protocol.comment(f"Added staple mix from {ws_wells} to reaction wells {rxn_wells}")

    # --- Distribute folding reactions into PCR plate ---
    # Each reaction tube is distributed across multiple PCR plate wells
    # (e.g. a 200uL reaction fills 2 x 100uL wells)
    first_open_well = protocol.params.folding_plate_start_well
    start_row = first_open_well[0]
    start_col = int(first_open_well[1:])

    # Map reaction tube rows (C, D) to PCR plate row pairs
    rxn_to_plate_rows = {"C": ["C", "D"], "D": ["E", "F"]}

    for well in rxn_wells:
        source_row = well[0]
        row_1, row_2 = rxn_to_plate_rows[source_row]

        wells_needed = math.ceil(folding_reaction_volume / DISPENSE_VOL_PER_WELL)
        dest_wells = []
        col = start_col
        i = 0
        while len(dest_wells) < wells_needed:
            dest_wells.append(f"{row_1 if i % 2 == 0 else row_2}{col}")
            if i % 2 == 1:
                col += 1
            i += 1

        pipette.distribute(
            volume=DISPENSE_VOL_PER_WELL,
            source=tube_rack_ws.wells_by_name()[well],
            dest=[folding_plate.wells_by_name()[w] for w in dest_wells],
            new_tip="always"
        )
        protocol.comment(f"Distributed reaction from {well} into PCR plate wells: {dest_wells}")

    protocol.pause(
        "Folding reactions loaded into PCR plate. "
        "Remove reagent tubes and close thermocycler lid to begin ramp."
    )

    # --- Run thermocycler ---
    thermocycler.close_lid()
    thermocycler.set_lid_temperature(95)

    thermocycler.execute_profile(
        steps=THERMOCYCLER_PROFILES[thermocycler_protocol],
        repetitions=1,
        block_max_volume=50,
    )

    # Hold at 20°C for 2 hours after ramp completes
    thermocycler.set_block_temperature(20, hold_time_minutes=120)
    protocol.comment("Thermocycler ramp complete. Samples held at 20°C.")