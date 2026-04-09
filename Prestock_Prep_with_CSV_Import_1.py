from opentrons import protocol_api

metadata = {
    'protocolName': 'Prestock Preparation with CSV import',
    'author': 'Sera Mathew, OpentronsAI',
    'description': 'Use CSV import to pool oligonucleotides from source plates to Eppendorf tubes to create prestocks for origami components',
}

requirements = {
    'robotType': 'Flex',
    'apiLevel': '2.25'
}


def add_parameters(parameters):
    parameters.add_csv_file(
        variable_name="transfer_csv",
        display_name="Transfer CSV File",
        description="CSV with columns: SOURCE PLATE, PART, WELL START, WELL END, DESTINATION RACK, DESTINATION WELL, TRANSFER VOLUME (ul)"
    )


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
    for col in range(start_col, end_col + 1):
        for row in range(8):  # Always iterate through all rows (A-H)
            if (col == start_col and row < start_row):
                continue  # Skip rows before start in first column
            if (col == end_col and row > end_row):
                break  # Stop after end row in last column

            well_name = f"{chr(ord('A') + row)}{col + 1}"
            wells.append(well_name)

    return wells


def run(protocol: protocol_api.ProtocolContext):
    # Parse CSV file
    csv_data = protocol.params.transfer_csv.parse_as_csv()

    # Skip header row
    transfer_data = csv_data[1:]

    # Load trash bin
    trash = protocol.load_trash_bin('A3')

    # Load tip racks - adjust quantity based on your needs
    tip_racks = [
        protocol.load_labware('opentrons_flex_96_tiprack_50ul', slot)
        for slot in ['C1', 'C2', 'C3']
    ]

    # Load pipette
    pipette = protocol.load_instrument(
        'flex_1channel_1000',
        mount='left',
        tip_racks=tip_racks
    )

    # Dictionary to store loaded labware
    loaded_plates = {}

    # Process each row in the CSV
    for row in transfer_data:
        source_plate_name = row[0].strip()
        part_name = row[1].strip()
        well_start = row[2].strip()
        well_end = row[3].strip()
        dest_rack_name = row[4].strip()
        dest_well = row[5].strip()
        transfer_volume = float(row[6].strip())

        # Skip rows with empty destination wells (like the last row in your CSV)
        # if not dest_well:
        #   continue

        # Load source plate if not already loaded
        if source_plate_name not in loaded_plates:
            # Assign deck slots dynamically - adjust as needed
            slot = f'D{len(loaded_plates) + 1}'
            loaded_plates[source_plate_name] = protocol.load_labware(
                'nest_96_wellplate_2ml_deep',  # Adjust labware type as needed
                slot,
                label=source_plate_name
            )

        # Load destination rack if not already loaded
        if dest_rack_name not in loaded_plates:
            # Assign deck slots dynamically - adjust as needed
            slot = f'B{len([k for k in loaded_plates.keys() if "Rack" in k]) + 1}'
            loaded_plates[dest_rack_name] = protocol.load_labware(
                'opentrons_24_tuberack_nest_2ml_snapcap',  # Adjust labware type as needed
                slot,
                label=dest_rack_name
            )

        # Get labware objects
        source_plate = loaded_plates[source_plate_name]
        dest_rack = loaded_plates[dest_rack_name]

        # Expand well range into individual wells
        source_wells = expand_well_range(well_start, well_end)

        # Transfer from each source well to destination well (pooling)
        for well in source_wells:
            pipette.transfer(
                volume=transfer_volume,
                source=source_plate[well],
                dest=dest_rack[dest_well],
                new_tip='always'
            )

        # Add a comment for tracking
        protocol.comment(
            f"Transferred {transfer_volume} µL from {source_plate_name} "
            f"wells {well_start}-{well_end} ({len(source_wells)} wells) "
            f"to {dest_rack_name} well {dest_well} for {part_name} prestock"
        )