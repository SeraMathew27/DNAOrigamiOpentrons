import json
from opentrons import protocol_api, types

metadata = {
    "protocolName": "Gear Pre-stock Protocol",
    "description": "Pre-stock protocol for gear structure using OMD1 and OMD2 for Gear Overhang Rep and Gear Core. This protocol transfer 10ul from wells to make 4 pre-stock tubes in 1.5ml Eppendorf Tubes. \n\nKehao Huang",
    "created": "2025-12-05T15:13:21.558Z",
    "internalAppBuildDate": "Tue, 16 Dec 2025 16:02:03 GMT",
    "lastModified": "2025-12-19T15:27:13.213Z",
    "protocolDesigner": "8.7.1",
    "source": "Protocol Designer",
}

requirements = {"robotType": "Flex", "apiLevel": "2.27"}

def run(protocol: protocol_api.ProtocolContext) -> None:
    # Load Modules:
    thermocycler_module_1 = protocol.load_module("thermocyclerModuleV2", "B1")

    # Load Labware:
    tip_rack_1 = protocol.load_labware(
        "opentrons_flex_96_tiprack_1000ul",
        location="D1",
        namespace="opentrons",
        version=1,
    )
    tip_rack_2 = protocol.load_labware(
        "opentrons_flex_96_tiprack_50ul",
        location="C1",
        namespace="opentrons",
        version=1,
    )
    well_plate_2 = protocol.load_labware_from_definition(
        CUSTOM_LABWARE["custom_beta/fisherscientific_96_wellplate_1200ul/1"],
        location="B2",
        label="OMD 1",
    )
    well_plate_3 = protocol.load_labware_from_definition(
        CUSTOM_LABWARE["custom_beta/fisherscientific_96_wellplate_1200ul/1"],
        location="C2",
        label="OMD 2",
    )
    well_plate_1 = protocol.load_labware(
        "thermoscientificnunc_96_wellplate_2000ul",
        location="B3",
        label="Transfer Plate",
        namespace="opentrons",
        version=3,
    )
    tube_rack_1 = protocol.load_labware(
        "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
        location="C3",
        label="Pre-Stock Tube Rack",
        namespace="opentrons",
        version=3,
    )
    tip_rack_3 = protocol.load_labware(
        "opentrons_flex_96_tiprack_50ul",
        location="D2",
        label="Opentrons Flex 96 Tip Rack 50 µL (2)",
        namespace="opentrons",
        version=1,
    )
    tube_rack_2 = protocol.load_labware(
        "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",
        location="D3",
        label="Working Stock Reagents",
        namespace="opentrons",
        version=3,
    )

    # Load Pipettes:
    pipette_left = protocol.load_instrument("flex_1channel_1000", "left")
    pipette_right = protocol.load_instrument("flex_8channel_50", "right")

    # Load Trash Bins:
    trash_bin_1 = protocol.load_trash_bin("A3")

    # Define Liquids:
    liquid_1 = protocol.define_liquid(
        "Gear Overhang Rep L",
        description="Gear Overhang Replacemetns Left Side",
        display_color="#7eff42ff",
    )
    liquid_2 = protocol.define_liquid(
        "Gear Overhang Rep Mid",
        description="Gear Overhang Replacements Middle",
        display_color="#50d5ffff",
    )
    liquid_3 = protocol.define_liquid(
        "Water",
        display_color="#9dffd8",
    )
    liquid_4 = protocol.define_liquid(
        "Gear Overhang Rep R",
        description="Gear Overhang Replacements Right Side",
        display_color="#ff4f4fff",
    )
    liquid_5 = protocol.define_liquid(
        "Gear Core",
        description="Gear Core",
        display_color="#b925ffff",
    )
    liquid_6 = protocol.define_liquid(
        "MgCl",
        description="200nM MgCl",
        display_color="#ff80f5",
    )
    liquid_7 = protocol.define_liquid(
        "FOB",
        description="10x FOB",
        display_color="#7eff42",
    )
    liquid_8 = protocol.define_liquid(
        "Scaffold",
        description="100nM Scaffold",
        display_color="#ff4f4f",
    )

    # Load Liquids:
    well_plate_2.load_liquid(
        wells=[
            "A1", "B1", "A2", "B2", "A3", "B3", "A4", "B4",
            "A5", "B5", "A6", "B6", "A7", "B7", "A8", "B8",
            "A9", "B9", "A10", "B10", "A11", "B11", "A12", "B12"
        ],
        liquid=liquid_1,
        volume=100,
    )
    well_plate_2.load_liquid(
        wells=[
            "C1", "D1", "C2", "D2", "C3", "D3", "C4", "D4",
            "C5", "D5", "C6", "D6", "C7", "D7", "C8", "D8",
            "C9", "D9", "C10", "D10", "C11", "D11", "C12", "D12"
        ],
        liquid=liquid_2,
        volume=100,
    )
    well_plate_2.load_liquid(
        wells=[
            "E1", "F1", "E2", "F2", "E3", "F3", "E4", "F4",
            "E5", "F5", "E6", "F6", "E7", "F7", "E8", "F8",
            "E9", "F9", "E10", "F10", "E11", "F11", "E12", "F12"
        ],
        liquid=liquid_4,
        volume=100,
    )
    well_plate_2.load_liquid(
        wells=[
            "G1", "H1", "G2", "H2", "G3", "H3", "G4", "H4",
            "G5", "H5", "G6", "H6", "G7", "H7", "G8", "H8",
            "G9", "G10", "G11", "G12"
        ],
        liquid=liquid_5,
        volume=100,
    )
    well_plate_3.load_liquid(
        wells=[
            "A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1",
            "A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2",
            "A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3",
            "A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4",
            "A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5",
            "A6", "B6", "C6", "D6", "E6", "F6", "G6", "H6",
            "A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7",
            "A8", "B8", "C8", "D8", "E8", "F8", "G8", "A9",
            "B9", "C9", "D9", "E9", "F9", "G9", "A10", "B10",
            "C10", "D10", "E10", "F10", "G10", "A11", "B11", "C11",
            "D11", "E11", "F11", "G11", "A12", "B12", "C12", "D12",
            "E12", "F12", "G12"
        ],
        liquid=liquid_5,
        volume=100,
    )
    tube_rack_2.load_liquid(
        wells=["A1"],
        liquid=liquid_3,
        volume=1000,
    )
    tube_rack_2.load_liquid(
        wells=["A2"],
        liquid=liquid_6,
        volume=1000,
    )
    tube_rack_2.load_liquid(
        wells=["A3"],
        liquid=liquid_7,
        volume=1000,
    )
    tube_rack_2.load_liquid(
        wells=["A4"],
        liquid=liquid_8,
        volume=1000,
    )

    # Load Liquid Classes:
    water_base_class = protocol.get_liquid_class("water")

    # PROTOCOL STEPS

    # Step 1: OMD 1 Col 1-8
    # Columns A to H with 8-channel pipette
    # 10ul Each 
    pipette_right.configure_nozzle_layout(
        protocol_api.ALL,
        start="A1",
    )
    pipette_right.transfer_with_liquid_class(
        volume=10,
        source=[well_plate_2["A1"], well_plate_2["A2"], well_plate_2["A3"], well_plate_2["A4"], well_plate_2["A5"], well_plate_2["A6"], well_plate_2["A7"], well_plate_2["A8"]],
        dest=[well_plate_1["A1"], well_plate_1["A1"], well_plate_1["A1"], well_plate_1["A1"], well_plate_1["A1"], well_plate_1["A1"], well_plate_1["A1"], well_plate_1["A1"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        group_wells=False,
        tip_racks=[tip_rack_2, tip_rack_3],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_1",
            base_liquid_class=water_base_class,
            properties={"flex_8channel_50": {"opentrons/opentrons_flex_96_tiprack_50ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 24)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 50)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 2)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_right.drop_tip()

    # Step 2: OMD 1 Col 9
    # I1 to I8 with 8-channel partial tip pick up. 10ul each
    pipette_right.configure_nozzle_layout(
        protocol_api.SINGLE,
        start="H1",
    )
    pipette_right.transfer_with_liquid_class(
        volume=10,
        source=[well_plate_2["A9"], well_plate_2["B9"], well_plate_2["C9"], well_plate_2["D9"], well_plate_2["E9"], well_plate_2["F9"], well_plate_2["G9"]],
        dest=[well_plate_1["A1"], well_plate_1["B1"], well_plate_1["C1"], well_plate_1["D1"], well_plate_1["E1"], well_plate_1["F1"], well_plate_1["G1"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        group_wells=False,
        tip_racks=[tip_rack_2, tip_rack_3],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_2",
            base_liquid_class=water_base_class,
            properties={"flex_8channel_50": {"opentrons/opentrons_flex_96_tiprack_50ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 24)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 50)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 2)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_right.drop_tip()

    # Step 3: OMD1 Col 10
    pipette_right.configure_nozzle_layout(
        protocol_api.SINGLE,
        start="H1",
    )
    pipette_right.transfer_with_liquid_class(
        volume=10,
        source=[well_plate_2["A10"], well_plate_2["B10"], well_plate_2["C10"], well_plate_2["D10"], well_plate_2["E10"], well_plate_2["F10"], well_plate_2["G10"]],
        dest=[well_plate_1["A1"], well_plate_1["B1"], well_plate_1["C1"], well_plate_1["D1"], well_plate_1["E1"], well_plate_1["F1"], well_plate_1["G1"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        group_wells=False,
        tip_racks=[tip_rack_2, tip_rack_3],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_3",
            base_liquid_class=water_base_class,
            properties={"flex_8channel_50": {"opentrons/opentrons_flex_96_tiprack_50ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 24)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 50)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 2)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_right.drop_tip()

    # Step 4: OMD 1 Col 11
    pipette_right.configure_nozzle_layout(
        protocol_api.SINGLE,
        start="H1",
    )
    pipette_right.transfer_with_liquid_class(
        volume=10,
        source=[well_plate_2["A11"], well_plate_2["B11"], well_plate_2["C11"], well_plate_2["D11"], well_plate_2["E11"], well_plate_2["F11"], well_plate_2["G11"]],
        dest=[well_plate_1["A1"], well_plate_1["B1"], well_plate_1["C1"], well_plate_1["D1"], well_plate_1["E1"], well_plate_1["F1"], well_plate_1["G1"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        group_wells=False,
        tip_racks=[tip_rack_2, tip_rack_3],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_4",
            base_liquid_class=water_base_class,
            properties={"flex_8channel_50": {"opentrons/opentrons_flex_96_tiprack_50ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 24)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 50)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 2)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_right.drop_tip()

    # Step 5: OMD 1 Col 12
    pipette_right.configure_nozzle_layout(
        protocol_api.SINGLE,
        start="H1",
    )
    pipette_right.transfer_with_liquid_class(
        volume=10,
        source=[well_plate_2["A12"], well_plate_2["B12"], well_plate_2["C12"], well_plate_2["D12"], well_plate_2["E12"], well_plate_2["F12"], well_plate_2["G12"]],
        dest=[well_plate_1["A1"], well_plate_1["B1"], well_plate_1["C1"], well_plate_1["D1"], well_plate_1["E1"], well_plate_1["F1"], well_plate_1["G1"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        group_wells=False,
        tip_racks=[tip_rack_2, tip_rack_3],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_5",
            base_liquid_class=water_base_class,
            properties={"flex_8channel_50": {"opentrons/opentrons_flex_96_tiprack_50ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 24)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 50)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 2)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_right.drop_tip()

    # Step 6: H1 - G1
    pipette_left.transfer_with_liquid_class(
        volume=80,
        source=[well_plate_1["H1"]],
        dest=[well_plate_1["G1"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_6",
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 5)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 5)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 2)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 7: OMD 2 Col 1-7
    pipette_right.configure_nozzle_layout(
        protocol_api.ALL,
        start="A1",
    )
    pipette_right.transfer_with_liquid_class(
        volume=10,
        source=[well_plate_3["A1"], well_plate_3["A2"], well_plate_3["A3"], well_plate_3["A4"], well_plate_3["A5"], well_plate_3["A6"], well_plate_3["A7"]],
        dest=[well_plate_1["A2"], well_plate_1["A2"], well_plate_1["A2"], well_plate_1["A2"], well_plate_1["A2"], well_plate_1["A2"], well_plate_1["A2"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        group_wells=False,
        tip_racks=[tip_rack_2, tip_rack_3],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_7",
            properties={"flex_8channel_50": {"opentrons/opentrons_flex_96_tiprack_50ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 24)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 50)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 2)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_right.drop_tip()

    # Step 8: OMD 2 Col 8
    pipette_right.configure_nozzle_layout(
        protocol_api.SINGLE,
        start="H1",
    )
    pipette_right.configure_nozzle_layout(
        protocol_api.SINGLE,
        start="H1",
    )
    pipette_right.transfer_with_liquid_class(
        volume=10,
        source=[well_plate_3["A8"], well_plate_3["B8"], well_plate_3["C8"], well_plate_3["D8"], well_plate_3["E8"], well_plate_3["F8"], well_plate_3["G8"]],
        dest=[well_plate_1["A2"], well_plate_1["B2"], well_plate_1["C2"], well_plate_1["D2"], well_plate_1["E2"], well_plate_1["F2"], well_plate_1["G2"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        group_wells=False,
        tip_racks=[tip_rack_2, tip_rack_3],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_8",
            properties={"flex_8channel_50": {"opentrons/opentrons_flex_96_tiprack_50ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 24)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 50)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 2)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_right.drop_tip()

    # Step 9: OMD 2 Col 9
    pipette_right.configure_nozzle_layout(
        protocol_api.SINGLE,
        start="H1",
    )
    pipette_right.transfer_with_liquid_class(
        volume=10,
        source=[well_plate_3["A9"], well_plate_3["B9"], well_plate_3["C9"], well_plate_3["D9"], well_plate_3["E9"], well_plate_3["F9"], well_plate_3["G9"]],
        dest=[well_plate_1["A2"], well_plate_1["B2"], well_plate_1["C2"], well_plate_1["D2"], well_plate_1["E2"], well_plate_1["F2"], well_plate_1["G2"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        group_wells=False,
        tip_racks=[tip_rack_2, tip_rack_3],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_9",
            properties={"flex_8channel_50": {"opentrons/opentrons_flex_96_tiprack_50ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 24)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 50)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 2)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_right.drop_tip()

    # Step 10: OMD 2 Col 10
    pipette_right.configure_nozzle_layout(
        protocol_api.SINGLE,
        start="H1",
    )
    pipette_right.transfer_with_liquid_class(
        volume=10,
        source=[well_plate_3["A10"], well_plate_3["B10"], well_plate_3["C10"], well_plate_3["D10"], well_plate_3["E10"], well_plate_3["F10"], well_plate_3["G10"]],
        dest=[well_plate_1["A2"], well_plate_1["B2"], well_plate_1["C2"], well_plate_1["D2"], well_plate_1["E2"], well_plate_1["F2"], well_plate_1["G2"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        group_wells=False,
        tip_racks=[tip_rack_2, tip_rack_3],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_10",
            properties={"flex_8channel_50": {"opentrons/opentrons_flex_96_tiprack_50ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 24)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 50)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 2)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_right.drop_tip()

    # Step 11: OMD 2 Col 11
    pipette_right.configure_nozzle_layout(
        protocol_api.SINGLE,
        start="H1",
    )
    pipette_right.transfer_with_liquid_class(
        volume=10,
        source=[well_plate_3["A11"], well_plate_3["B11"], well_plate_3["C11"], well_plate_3["D11"], well_plate_3["E11"], well_plate_3["F11"], well_plate_3["G11"]],
        dest=[well_plate_1["A2"], well_plate_1["B2"], well_plate_1["C2"], well_plate_1["D2"], well_plate_1["E2"], well_plate_1["F2"], well_plate_1["G2"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        group_wells=False,
        tip_racks=[tip_rack_2, tip_rack_3],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_11",
            properties={"flex_8channel_50": {"opentrons/opentrons_flex_96_tiprack_50ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 24)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 50)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 2)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_right.drop_tip()

    # Step 12: OMD 2 Col 12
    pipette_right.configure_nozzle_layout(
        protocol_api.SINGLE,
        start="H1",
    )
    pipette_right.transfer_with_liquid_class(
        volume=10,
        source=[well_plate_3["A12"], well_plate_3["B12"], well_plate_3["C12"], well_plate_3["D12"], well_plate_3["E12"], well_plate_3["F12"], well_plate_3["G12"]],
        dest=[well_plate_1["A2"], well_plate_1["B2"], well_plate_1["C2"], well_plate_1["D2"], well_plate_1["E2"], well_plate_1["F2"], well_plate_1["G2"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        group_wells=False,
        tip_racks=[tip_rack_2, tip_rack_3],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_12",
            properties={"flex_8channel_50": {"opentrons/opentrons_flex_96_tiprack_50ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 24)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 50)],
                    "delay": {"enabled": True, "duration": 0.2},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0.1)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 2)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_right.drop_tip()

    # Step 13: Prestock OH Reps Left
    pipette_left.consolidate_with_liquid_class(
        volume=120,
        source=[well_plate_1["A1"], well_plate_1["B1"]],
        dest=[tube_rack_1["A1"]],
        new_tip="once",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="consolidate_step_13",
            base_liquid_class=water_base_class,
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 0.5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.5},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 14: Prestock OH Reps Mid
    pipette_left.consolidate_with_liquid_class(
        volume=120,
        source=[well_plate_1["C1"], well_plate_1["D1"]],
        dest=[tube_rack_1["B1"]],
        new_tip="once",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="consolidate_step_14",
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 0.5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 15: Prestock OH Reps Right
    pipette_left.consolidate_with_liquid_class(
        volume=120,
        source=[well_plate_1["E1"], well_plate_1["F1"]],
        dest=[tube_rack_1["C1"]],
        new_tip="once",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="consolidate_step_15",
            base_liquid_class=water_base_class,
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 0.5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.5},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 16: Prestock Core 1
    pipette_left.transfer_with_liquid_class(
        volume=200,
        source=[well_plate_1["G1"]],
        dest=[tube_rack_1["D1"]],
        new_tip="once",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_16",
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 0.5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.5},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 17: Prestock Core 2
    pipette_left.consolidate_with_liquid_class(
        volume=120,
        source=[well_plate_1["A2"], well_plate_1["B2"]],
        dest=[tube_rack_1["A2"]],
        new_tip="once",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="consolidate_step_17",
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 0.5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.5},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 18: Prestock Core 3
    pipette_left.consolidate_with_liquid_class(
        volume=120,
        source=[well_plate_1["C2"], well_plate_1["D2"]],
        dest=[tube_rack_1["B2"]],
        new_tip="once",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="consolidate_step_18",
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 0.5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.5},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 19: Prestock Core 4
    pipette_left.consolidate_with_liquid_class(
        volume=120,
        source=[well_plate_1["E2"], well_plate_1["F2"]],
        dest=[tube_rack_1["C2"]],
        new_tip="once",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="consolidate_step_19",
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 0.5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.5},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 20: Prestock Core 5 premix
    pipette_left.transfer_with_liquid_class(
        volume=70,
        source=[well_plate_1["H2"]],
        dest=[well_plate_1["G2"]],
        new_tip="once",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_20",
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 0.5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 21: Prestock Core 5
    pipette_left.transfer_with_liquid_class(
        volume=190,
        source=[well_plate_1["G2"]],
        dest=[tube_rack_1["D2"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_21",
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 0.5},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 22: pause
    protocol.pause("Pre-stocks are completed! Remove tube racks from deck and continue to make working stocks.")

    # Step 23: Core 1 to WS
    pipette_left.transfer_with_liquid_class(
        volume=20,
        source=[tube_rack_1["D1"]],
        dest=[tube_rack_1["A6"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_23",
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 24: Core 2-4 to WS
    pipette_left.transfer_with_liquid_class(
        volume=24,
        source=[tube_rack_1["A2"], tube_rack_1["B2"], tube_rack_1["C2"]],
        dest=[tube_rack_1["A6"], tube_rack_1["A6"], tube_rack_1["A6"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_24",
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 25: Core 5 to WS
    pipette_left.transfer_with_liquid_class(
        volume=19,
        source=[tube_rack_1["D2"], tube_rack_1["A6"]],
        dest=[tube_rack_1["A6"], tube_rack_1["A6"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_25",
            base_liquid_class=water_base_class,
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 26: Water to WS + Mix
    pipette_left.transfer_with_liquid_class(
        volume=17,
        source=[tube_rack_2["A1"]],
        dest=[tube_rack_1["A6"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_26",
            base_liquid_class=water_base_class,
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.5},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": True, "repetitions": 3, "volume": 100},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 27: Water to folding rxn
    pipette_left.transfer_with_liquid_class(
        volume=50,
        source=[tube_rack_2["A1"]],
        dest=[tube_rack_2["D1"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_27",
            base_liquid_class=water_base_class,
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.5},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 28: Salts to folding rxn
    pipette_left.transfer_with_liquid_class(
        volume=10,
        source=[tube_rack_1["B1"], tube_rack_1["C1"]],
        dest=[tube_rack_2["D1"], tube_rack_2["D1"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_28",
            base_liquid_class=water_base_class,
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.5},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 29: pause
    protocol.pause("Folding buffer ready. Proceed to add staples and scaffold!")

    # Step 30: Add Scaffold to folding rxn
    pipette_left.transfer_with_liquid_class(
        volume=10,
        source=[tube_rack_2["A4"]],
        dest=[tube_rack_2["D1"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_30",
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": False},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 1},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 0)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 31: Add Staples to folding rxn
    pipette_left.transfer_with_liquid_class(
        volume=20,
        source=[tube_rack_1["A6"]],
        dest=[tube_rack_2["D1"]],
        new_tip="always",
        trash_location=trash_bin_1,
        keep_last_tip=True,
        tip_racks=[tip_rack_1],
        liquid_class=protocol.define_liquid_class(
            name="transfer_step_31",
            base_liquid_class=water_base_class,
            properties={"flex_1channel_1000": {"opentrons/opentrons_flex_96_tiprack_1000ul/1": {
                "aspirate": {
                    "aspirate_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "pre_wet": False,
                    "correction_by_volume": [(0, 0)],
                    "delay": {"enabled": True, "duration": 0.5},
                    "mix": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                    },
                },
                "dispense": {
                    "dispense_position": {
                        "offset": {"x": 0, "y": 0, "z": 2},
                        "position_reference": "well-bottom",
                    },
                    "flow_rate_by_volume": [(0, 716)],
                    "delay": {"enabled": False},
                    "submerge": {
                        "delay": {"enabled": False},
                        "speed": 100,
                        "start_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                    },
                    "retract": {
                        "air_gap_by_volume": [(0, 10)],
                        "delay": {"enabled": False},
                        "end_position": {
                            "offset": {"x": 0, "y": 0, "z": 2},
                            "position_reference": "well-top",
                        },
                        "speed": 50,
                        "touch_tip": {"enabled": False},
                        "blowout": {"enabled": False},
                    },
                    "correction_by_volume": [(0, 0)],
                    "push_out_by_volume": [(0, 20)],
                    "mix": {"enabled": False},
                },
            }}},
        ),
    )
    pipette_left.drop_tip()

    # Step 32: pause
    protocol.pause("Working stock is complete. Proceed to set up folding reaction")

CUSTOM_LABWARE = json.loads("""{"custom_beta/fisherscientific_96_wellplate_1200ul/1":{"ordering":[["A1","B1","C1","D1","E1","F1","G1","H1"],["A2","B2","C2","D2","E2","F2","G2","H2"],["A3","B3","C3","D3","E3","F3","G3","H3"],["A4","B4","C4","D4","E4","F4","G4","H4"],["A5","B5","C5","D5","E5","F5","G5","H5"],["A6","B6","C6","D6","E6","F6","G6","H6"],["A7","B7","C7","D7","E7","F7","G7","H7"],["A8","B8","C8","D8","E8","F8","G8","H8"],["A9","B9","C9","D9","E9","F9","G9","H9"],["A10","B10","C10","D10","E10","F10","G10","H10"],["A11","B11","C11","D11","E11","F11","G11","H11"],["A12","B12","C12","D12","E12","F12","G12","H12"]],"brand":{"brand":"Fisher Scientific","brandId":["SP-1081"]},"metadata":{"displayName":"Fisher Scientific 96 Well Plate 1200 µL","displayCategory":"wellPlate","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.76,"yDimension":85.48,"zDimension":42.5},"wells":{"A1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":74.24,"z":3.15},"B1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":65.24,"z":3.15},"C1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":56.24,"z":3.15},"D1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":47.24,"z":3.15},"E1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":38.24,"z":3.15},"F1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":29.24,"z":3.15},"G1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":20.24,"z":3.15},"H1":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":14.38,"y":11.24,"z":3.15},"A2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":74.24,"z":3.15},"B2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":65.24,"z":3.15},"C2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":56.24,"z":3.15},"D2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":47.24,"z":3.15},"E2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":38.24,"z":3.15},"F2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":29.24,"z":3.15},"G2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":20.24,"z":3.15},"H2":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":23.38,"y":11.24,"z":3.15},"A3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":74.24,"z":3.15},"B3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":65.24,"z":3.15},"C3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":56.24,"z":3.15},"D3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":47.24,"z":3.15},"E3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":38.24,"z":3.15},"F3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":29.24,"z":3.15},"G3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":20.24,"z":3.15},"H3":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":32.38,"y":11.24,"z":3.15},"A4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":74.24,"z":3.15},"B4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":65.24,"z":3.15},"C4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":56.24,"z":3.15},"D4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":47.24,"z":3.15},"E4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":38.24,"z":3.15},"F4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":29.24,"z":3.15},"G4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":20.24,"z":3.15},"H4":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":41.38,"y":11.24,"z":3.15},"A5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":74.24,"z":3.15},"B5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":65.24,"z":3.15},"C5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":56.24,"z":3.15},"D5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":47.24,"z":3.15},"E5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":38.24,"z":3.15},"F5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":29.24,"z":3.15},"G5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":20.24,"z":3.15},"H5":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":50.38,"y":11.24,"z":3.15},"A6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":74.24,"z":3.15},"B6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":65.24,"z":3.15},"C6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":56.24,"z":3.15},"D6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":47.24,"z":3.15},"E6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":38.24,"z":3.15},"F6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":29.24,"z":3.15},"G6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":20.24,"z":3.15},"H6":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":59.38,"y":11.24,"z":3.15},"A7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":74.24,"z":3.15},"B7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":65.24,"z":3.15},"C7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":56.24,"z":3.15},"D7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":47.24,"z":3.15},"E7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":38.24,"z":3.15},"F7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":29.24,"z":3.15},"G7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":20.24,"z":3.15},"H7":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":68.38,"y":11.24,"z":3.15},"A8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":74.24,"z":3.15},"B8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":65.24,"z":3.15},"C8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":56.24,"z":3.15},"D8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":47.24,"z":3.15},"E8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":38.24,"z":3.15},"F8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":29.24,"z":3.15},"G8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":20.24,"z":3.15},"H8":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":77.38,"y":11.24,"z":3.15},"A9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":74.24,"z":3.15},"B9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":65.24,"z":3.15},"C9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":56.24,"z":3.15},"D9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":47.24,"z":3.15},"E9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":38.24,"z":3.15},"F9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":29.24,"z":3.15},"G9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":20.24,"z":3.15},"H9":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":86.38,"y":11.24,"z":3.15},"A10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":74.24,"z":3.15},"B10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":65.24,"z":3.15},"C10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":56.24,"z":3.15},"D10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":47.24,"z":3.15},"E10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":38.24,"z":3.15},"F10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":29.24,"z":3.15},"G10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":20.24,"z":3.15},"H10":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":95.38,"y":11.24,"z":3.15},"A11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":74.24,"z":3.15},"B11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":65.24,"z":3.15},"C11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":56.24,"z":3.15},"D11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":47.24,"z":3.15},"E11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":38.24,"z":3.15},"F11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":29.24,"z":3.15},"G11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":20.24,"z":3.15},"H11":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":104.38,"y":11.24,"z":3.15},"A12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":74.24,"z":3.15},"B12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":65.24,"z":3.15},"C12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":56.24,"z":3.15},"D12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":47.24,"z":3.15},"E12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":38.24,"z":3.15},"F12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":29.24,"z":3.15},"G12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":20.24,"z":3.15},"H12":{"depth":39.35,"totalLiquidVolume":1200,"shape":"circular","diameter":7,"x":113.38,"y":11.24,"z":3.15}},"groups":[{"metadata":{"wellBottomShape":"u"},"wells":["A1","B1","C1","D1","E1","F1","G1","H1","A2","B2","C2","D2","E2","F2","G2","H2","A3","B3","C3","D3","E3","F3","G3","H3","A4","B4","C4","D4","E4","F4","G4","H4","A5","B5","C5","D5","E5","F5","G5","H5","A6","B6","C6","D6","E6","F6","G6","H6","A7","B7","C7","D7","E7","F7","G7","H7","A8","B8","C8","D8","E8","F8","G8","H8","A9","B9","C9","D9","E9","F9","G9","H9","A10","B10","C10","D10","E10","F10","G10","H10","A11","B11","C11","D11","E11","F11","G11","H11","A12","B12","C12","D12","E12","F12","G12","H12"]}],"parameters":{"format":"irregular","quirks":[],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"fisherscientific_96_wellplate_1200ul"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}}}""")

DESIGNER_APPLICATION = """{"robot":{"model":"OT-3 Standard"},"designerApplication":{"name":"opentrons/protocol-designer","version":"8.7.0","data":{"pipetteTiprackAssignments":{"3def0e45-a408-486d-8786-b6c2c43df782":["opentrons/opentrons_flex_96_tiprack_1000ul/1"],"6271d084-b692-4b40-b2aa-ca408d25380e":["opentrons/opentrons_flex_96_tiprack_50ul/1"]},"dismissedWarnings":{"form":[],"timeline":["ASPIRATE_MORE_THAN_WELL_CONTENTS"]},"ingredients":{"0":{"displayName":"Gear Overhang Rep L","displayColor":"#7eff42ff","liquidClass":"water","description":"Gear Overhang Replacemetns Left Side","liquidGroupId":"0"},"1":{"displayName":"Gear Overhang Rep Mid","displayColor":"#50d5ffff","description":"Gear Overhang Replacements Middle","liquidGroupId":"1"},"2":{"displayName":"Water","displayColor":"#9dffd8","description":null,"liquidGroupId":"2"},"3":{"displayName":"Gear Overhang Rep R","displayColor":"#ff4f4fff","liquidClass":"water","description":"Gear Overhang Replacements Right Side","liquidGroupId":"3"},"4":{"displayName":"Gear Core","displayColor":"#b925ffff","description":"Gear Core","liquidGroupId":"4"},"5":{"displayName":"MgCl","displayColor":"#ff80f5","description":"200nM MgCl","liquidGroupId":"5"},"6":{"displayName":"FOB","displayColor":"#7eff42","description":"10x FOB","liquidGroupId":"6"},"7":{"displayName":"Scaffold","displayColor":"#ff4f4f","description":"100nM Scaffold","liquidGroupId":"7"}},"ingredLocations":{"5f862063-d2f9-4a59-a13a-90bb1f263046:custom_beta/fisherscientific_96_wellplate_1200ul/1":{"A1":{"0":{"volume":100}},"B1":{"0":{"volume":100}},"A2":{"0":{"volume":100}},"B2":{"0":{"volume":100}},"A3":{"0":{"volume":100}},"B3":{"0":{"volume":100}},"A4":{"0":{"volume":100}},"B4":{"0":{"volume":100}},"A5":{"0":{"volume":100}},"B5":{"0":{"volume":100}},"A6":{"0":{"volume":100}},"B6":{"0":{"volume":100}},"A7":{"0":{"volume":100}},"B7":{"0":{"volume":100}},"A8":{"0":{"volume":100}},"B8":{"0":{"volume":100}},"A9":{"0":{"volume":100}},"B9":{"0":{"volume":100}},"A10":{"0":{"volume":100}},"B10":{"0":{"volume":100}},"A11":{"0":{"volume":100}},"B11":{"0":{"volume":100}},"A12":{"0":{"volume":100}},"B12":{"0":{"volume":100}},"C1":{"1":{"volume":100}},"D1":{"1":{"volume":100}},"C2":{"1":{"volume":100}},"D2":{"1":{"volume":100}},"C3":{"1":{"volume":100}},"D3":{"1":{"volume":100}},"C4":{"1":{"volume":100}},"D4":{"1":{"volume":100}},"C5":{"1":{"volume":100}},"D5":{"1":{"volume":100}},"C6":{"1":{"volume":100}},"D6":{"1":{"volume":100}},"C7":{"1":{"volume":100}},"D7":{"1":{"volume":100}},"C8":{"1":{"volume":100}},"D8":{"1":{"volume":100}},"C9":{"1":{"volume":100}},"D9":{"1":{"volume":100}},"C10":{"1":{"volume":100}},"D10":{"1":{"volume":100}},"C11":{"1":{"volume":100}},"D11":{"1":{"volume":100}},"C12":{"1":{"volume":100}},"D12":{"1":{"volume":100}},"E1":{"3":{"volume":100}},"F1":{"3":{"volume":100}},"E2":{"3":{"volume":100}},"F2":{"3":{"volume":100}},"E3":{"3":{"volume":100}},"F3":{"3":{"volume":100}},"E4":{"3":{"volume":100}},"F4":{"3":{"volume":100}},"E5":{"3":{"volume":100}},"F5":{"3":{"volume":100}},"E6":{"3":{"volume":100}},"F6":{"3":{"volume":100}},"E7":{"3":{"volume":100}},"F7":{"3":{"volume":100}},"E8":{"3":{"volume":100}},"F8":{"3":{"volume":100}},"E9":{"3":{"volume":100}},"F9":{"3":{"volume":100}},"E10":{"3":{"volume":100}},"F10":{"3":{"volume":100}},"E11":{"3":{"volume":100}},"F11":{"3":{"volume":100}},"E12":{"3":{"volume":100}},"F12":{"3":{"volume":100}},"G1":{"4":{"volume":100}},"H1":{"4":{"volume":100}},"G2":{"4":{"volume":100}},"H2":{"4":{"volume":100}},"G3":{"4":{"volume":100}},"H3":{"4":{"volume":100}},"G4":{"4":{"volume":100}},"H4":{"4":{"volume":100}},"G5":{"4":{"volume":100}},"H5":{"4":{"volume":100}},"G6":{"4":{"volume":100}},"H6":{"4":{"volume":100}},"G7":{"4":{"volume":100}},"H7":{"4":{"volume":100}},"G8":{"4":{"volume":100}},"H8":{"4":{"volume":100}},"G9":{"4":{"volume":100}},"G10":{"4":{"volume":100}},"G11":{"4":{"volume":100}},"G12":{"4":{"volume":100}}},"61950488-605c-4c0c-a941-f85d908c0ec3:custom_beta/fisherscientific_96_wellplate_1200ul/1":{"A1":{"4":{"volume":100}},"B1":{"4":{"volume":100}},"C1":{"4":{"volume":100}},"D1":{"4":{"volume":100}},"E1":{"4":{"volume":100}},"F1":{"4":{"volume":100}},"G1":{"4":{"volume":100}},"H1":{"4":{"volume":100}},"A2":{"4":{"volume":100}},"B2":{"4":{"volume":100}},"C2":{"4":{"volume":100}},"D2":{"4":{"volume":100}},"E2":{"4":{"volume":100}},"F2":{"4":{"volume":100}},"G2":{"4":{"volume":100}},"H2":{"4":{"volume":100}},"A3":{"4":{"volume":100}},"B3":{"4":{"volume":100}},"C3":{"4":{"volume":100}},"D3":{"4":{"volume":100}},"E3":{"4":{"volume":100}},"F3":{"4":{"volume":100}},"G3":{"4":{"volume":100}},"H3":{"4":{"volume":100}},"A4":{"4":{"volume":100}},"B4":{"4":{"volume":100}},"C4":{"4":{"volume":100}},"D4":{"4":{"volume":100}},"E4":{"4":{"volume":100}},"F4":{"4":{"volume":100}},"G4":{"4":{"volume":100}},"H4":{"4":{"volume":100}},"A5":{"4":{"volume":100}},"B5":{"4":{"volume":100}},"C5":{"4":{"volume":100}},"D5":{"4":{"volume":100}},"E5":{"4":{"volume":100}},"F5":{"4":{"volume":100}},"G5":{"4":{"volume":100}},"H5":{"4":{"volume":100}},"A6":{"4":{"volume":100}},"B6":{"4":{"volume":100}},"C6":{"4":{"volume":100}},"D6":{"4":{"volume":100}},"E6":{"4":{"volume":100}},"F6":{"4":{"volume":100}},"G6":{"4":{"volume":100}},"H6":{"4":{"volume":100}},"A7":{"4":{"volume":100}},"B7":{"4":{"volume":100}},"C7":{"4":{"volume":100}},"D7":{"4":{"volume":100}},"E7":{"4":{"volume":100}},"F7":{"4":{"volume":100}},"G7":{"4":{"volume":100}},"H7":{"4":{"volume":100}},"A8":{"4":{"volume":100}},"B8":{"4":{"volume":100}},"C8":{"4":{"volume":100}},"D8":{"4":{"volume":100}},"E8":{"4":{"volume":100}},"F8":{"4":{"volume":100}},"G8":{"4":{"volume":100}},"A9":{"4":{"volume":100}},"B9":{"4":{"volume":100}},"C9":{"4":{"volume":100}},"D9":{"4":{"volume":100}},"E9":{"4":{"volume":100}},"F9":{"4":{"volume":100}},"G9":{"4":{"volume":100}},"A10":{"4":{"volume":100}},"B10":{"4":{"volume":100}},"C10":{"4":{"volume":100}},"D10":{"4":{"volume":100}},"E10":{"4":{"volume":100}},"F10":{"4":{"volume":100}},"G10":{"4":{"volume":100}},"A11":{"4":{"volume":100}},"B11":{"4":{"volume":100}},"C11":{"4":{"volume":100}},"D11":{"4":{"volume":100}},"E11":{"4":{"volume":100}},"F11":{"4":{"volume":100}},"G11":{"4":{"volume":100}},"A12":{"4":{"volume":100}},"B12":{"4":{"volume":100}},"C12":{"4":{"volume":100}},"D12":{"4":{"volume":100}},"E12":{"4":{"volume":100}},"F12":{"4":{"volume":100}},"G12":{"4":{"volume":100}}},"4d883151-3381-4672-8ce1-83c63dfc3e86:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3":{"A1":{"2":{"volume":1000}},"A2":{"5":{"volume":1000}},"A3":{"6":{"volume":1000}},"A4":{"7":{"volume":1000}}}},"savedStepForms":{"__INITIAL_DECK_SETUP_STEP__":{"stepType":"manualIntervention","id":"__INITIAL_DECK_SETUP_STEP__","labwareLocationUpdate":{"bdd5ce09-3a12-4782-bd5b-0480508e4dcd:opentrons/opentrons_flex_96_tiprack_1000ul/1":"D1","f06ce940-053b-4051-a8ec-c08c3e7524f3:opentrons/opentrons_flex_96_tiprack_50ul/1":"C1","5f862063-d2f9-4a59-a13a-90bb1f263046:custom_beta/fisherscientific_96_wellplate_1200ul/1":"B2","61950488-605c-4c0c-a941-f85d908c0ec3:custom_beta/fisherscientific_96_wellplate_1200ul/1":"C2","3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3":"B3","20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3":"C3","f44be508-e0a6-4598-9d20-b54685447fea:opentrons/opentrons_flex_96_tiprack_50ul/1":"D2","4d883151-3381-4672-8ce1-83c63dfc3e86:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3":"D3"},"pipetteLocationUpdate":{"3def0e45-a408-486d-8786-b6c2c43df782":"left","6271d084-b692-4b40-b2aa-ca408d25380e":"right"},"moduleLocationUpdate":{"25f9bdc0-f76c-4a75-8379-0291edcd6c17:thermocyclerModuleType":"B1"},"trashBinLocationUpdate":{"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin":"cutoutA3"},"wasteChuteLocationUpdate":{},"stagingAreaLocationUpdate":{},"gripperLocationUpdate":{"2d17ae5e-fb85-4362-a380-4b52e8de57ca:gripper":"mounted"}},"966880bf-dfbe-4023-90fe-320f0ffa846c":{"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"0.1","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.2","aspirate_flowRate":"24","aspirate_labware":"5f862063-d2f9-4a59-a13a-90bb1f263046:custom_beta/fisherscientific_96_wellplate_1200ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":"50","aspirate_mmFromBottom":2,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1","A2","A3","A4","A5","A6","A7","A8"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"50","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"0.1","dispense_delay_checkbox":true,"dispense_delay_seconds":"0.2","dispense_flowRate":"50","dispense_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"water","nozzles":"ALL","path":"single","pipette":"6271d084-b692-4b40-b2aa-ca408d25380e","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"2","tipRack":"opentrons/opentrons_flex_96_tiprack_50ul/1","tip_tracking":"automatic","tiprack_selected":"f06ce940-053b-4051-a8ec-c08c3e7524f3:opentrons/opentrons_flex_96_tiprack_50ul/1","tips_selected":[["A2","B2","C2","D2","E2","F2","G2","H2"],["A3","B3","C3","D3","E3","F3","G3","H3"],["A4","B4","C4","D4","E4","F4","G4","H4"],["A5","B5","C5","D5","E5","F5","G5","H5"],["A6","B6","C6","D6","E6","F6","G6","H6"],["A7","B7","C7","D7","E7","F7","G7","H7"],["A8","B8","C8","D8","E8","F8","G8","H8"],["A9","B9","C9","D9","E9","F9","G9","H9"]],"volume":"10","id":"966880bf-dfbe-4023-90fe-320f0ffa846c","stepType":"moveLiquid","stepName":"OMD 1 Col 1-8","stepDetails":"Columns A to H with 8-channel pipette\n10ul Each ","stepNumber":0},"8b141246-49e4-45ef-a8ee-b96a3849d45b":{"id":"8b141246-49e4-45ef-a8ee-b96a3849d45b","stepType":"moveLiquid","stepName":"OMD 1 Col 9","stepDetails":"I1 to I8 with 8-channel partial tip pick up. 10ul each","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"0.1","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.2","aspirate_flowRate":"24","aspirate_labware":"5f862063-d2f9-4a59-a13a-90bb1f263046:custom_beta/fisherscientific_96_wellplate_1200ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":"50","aspirate_mmFromBottom":2,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A9","B9","C9","D9","E9","F9","G9"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"50","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"0.1","dispense_delay_checkbox":true,"dispense_delay_seconds":"0.2","dispense_flowRate":"50","dispense_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","B1","C1","D1","E1","F1","G1"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"water","nozzles":"SINGLE","path":"single","pipette":"6271d084-b692-4b40-b2aa-ca408d25380e","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"2","tipRack":"opentrons/opentrons_flex_96_tiprack_50ul/1","tip_tracking":"automatic","tiprack_selected":"f06ce940-053b-4051-a8ec-c08c3e7524f3:opentrons/opentrons_flex_96_tiprack_50ul/1","tips_selected":[["A9"],["B9"],["C9"],["D9"],["E9"],["F9"],["G9"]],"volume":"10"},"cd2f611c-a231-4ced-bfa7-29c8a2b49784":{"id":"cd2f611c-a231-4ced-bfa7-29c8a2b49784","stepType":"moveLiquid","stepName":"OMD1 Col 10","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"0.1","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.2","aspirate_flowRate":"24","aspirate_labware":"5f862063-d2f9-4a59-a13a-90bb1f263046:custom_beta/fisherscientific_96_wellplate_1200ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":"50","aspirate_mmFromBottom":2,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A10","B10","C10","D10","E10","F10","G10"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"50","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"0.1","dispense_delay_checkbox":true,"dispense_delay_seconds":"0.2","dispense_flowRate":"50","dispense_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","B1","C1","D1","E1","F1","G1"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"water","nozzles":"SINGLE","path":"single","pipette":"6271d084-b692-4b40-b2aa-ca408d25380e","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"2","tipRack":"opentrons/opentrons_flex_96_tiprack_50ul/1","tip_tracking":"automatic","tiprack_selected":"f06ce940-053b-4051-a8ec-c08c3e7524f3:opentrons/opentrons_flex_96_tiprack_50ul/1","tips_selected":[],"volume":"10"},"fc97397e-29bb-4407-808e-28e0bbb077a0":{"id":"fc97397e-29bb-4407-808e-28e0bbb077a0","stepType":"moveLiquid","stepName":"OMD 1 Col 11","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"0.1","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.2","aspirate_flowRate":"24","aspirate_labware":"5f862063-d2f9-4a59-a13a-90bb1f263046:custom_beta/fisherscientific_96_wellplate_1200ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":"50","aspirate_mmFromBottom":2,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A11","B11","C11","D11","E11","F11","G11"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"50","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"0.1","dispense_delay_checkbox":true,"dispense_delay_seconds":"0.2","dispense_flowRate":"50","dispense_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","B1","C1","D1","E1","F1","G1"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"water","nozzles":"SINGLE","path":"single","pipette":"6271d084-b692-4b40-b2aa-ca408d25380e","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"2","tipRack":"opentrons/opentrons_flex_96_tiprack_50ul/1","tip_tracking":"automatic","tiprack_selected":"f06ce940-053b-4051-a8ec-c08c3e7524f3:opentrons/opentrons_flex_96_tiprack_50ul/1","tips_selected":[],"volume":"10"},"e72b6f8f-ba5b-4231-9b3e-f68700657fde":{"id":"e72b6f8f-ba5b-4231-9b3e-f68700657fde","stepType":"moveLiquid","stepName":"OMD 1 Col 12","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"0.1","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.2","aspirate_flowRate":"24","aspirate_labware":"5f862063-d2f9-4a59-a13a-90bb1f263046:custom_beta/fisherscientific_96_wellplate_1200ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":"50","aspirate_mmFromBottom":2,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A12","B12","C12","D12","E12","F12","G12"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"50","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"0.1","dispense_delay_checkbox":true,"dispense_delay_seconds":"0.2","dispense_flowRate":"50","dispense_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1","B1","C1","D1","E1","F1","G1"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"water","nozzles":"SINGLE","path":"single","pipette":"6271d084-b692-4b40-b2aa-ca408d25380e","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"2","tipRack":"opentrons/opentrons_flex_96_tiprack_50ul/1","tip_tracking":"automatic","tiprack_selected":"f06ce940-053b-4051-a8ec-c08c3e7524f3:opentrons/opentrons_flex_96_tiprack_50ul/1","tips_selected":[],"volume":"10"},"2f8958ca-5e0b-4e01-832c-eb54f9c8b375":{"id":"2f8958ca-5e0b-4e01-832c-eb54f9c8b375","stepType":"moveLiquid","stepName":"Prestock OH Reps Left","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"10","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.5","aspirate_flowRate":"716","aspirate_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":0.5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1","B1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":"dest_well","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"10","dispense_delay_checkbox":false,"dispense_delay_seconds":"0","dispense_flowRate":"716","dispense_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A1"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"water","nozzles":null,"path":"multiAspirate","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"120"},"fd5139d4-5097-4baf-ba4e-ca057d9e3779":{"id":"fd5139d4-5097-4baf-ba4e-ca057d9e3779","stepType":"moveLiquid","stepName":"Prestock OH Reps Mid","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":"716","aspirate_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":0.5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["C1","D1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":null,"changeTip":"once","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":false,"dispense_airGap_volume":"","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":"716","dispense_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":false,"dispense_mix_times":"","dispense_mix_volume":"","dispense_mmFromBottom":1,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["B1"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":null,"path":"multiAspirate","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"120"},"96e3414c-97d0-4ac5-bb8b-bc9e7d9dbe98":{"id":"96e3414c-97d0-4ac5-bb8b-bc9e7d9dbe98","stepType":"moveLiquid","stepName":"Prestock OH Reps Right","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"10","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.5","aspirate_flowRate":"716","aspirate_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":0.5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["E1","F1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":"dest_well","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"10","dispense_delay_checkbox":false,"dispense_delay_seconds":"0","dispense_flowRate":"716","dispense_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["C1"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"water","nozzles":null,"path":"multiAspirate","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"120"},"854cebbc-8bf5-4d9e-90b3-9f36d6c9e3bc":{"id":"854cebbc-8bf5-4d9e-90b3-9f36d6c9e3bc","stepType":"moveLiquid","stepName":"OMD 2 Col 1-7","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"0.1","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.2","aspirate_flowRate":"24","aspirate_labware":"61950488-605c-4c0c-a941-f85d908c0ec3:custom_beta/fisherscientific_96_wellplate_1200ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":"50","aspirate_mmFromBottom":null,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1","A2","A3","A4","A5","A6","A7"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"50","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"0.1","dispense_delay_checkbox":true,"dispense_delay_seconds":"0.2","dispense_flowRate":"50","dispense_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A2"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":"ALL","path":"single","pipette":"6271d084-b692-4b40-b2aa-ca408d25380e","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"2","tipRack":"opentrons/opentrons_flex_96_tiprack_50ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"10"},"063d3964-dcf2-4fd6-86aa-65d39e74f595":{"id":"063d3964-dcf2-4fd6-86aa-65d39e74f595","stepType":"moveLiquid","stepName":"OMD 2 Col 8","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"0.1","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.2","aspirate_flowRate":"24","aspirate_labware":"61950488-605c-4c0c-a941-f85d908c0ec3:custom_beta/fisherscientific_96_wellplate_1200ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":"50","aspirate_mmFromBottom":null,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A8","B8","C8","D8","E8","F8","G8"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"50","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"0.1","dispense_delay_checkbox":true,"dispense_delay_seconds":"0.2","dispense_flowRate":"50","dispense_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A2","B2","C2","D2","E2","F2","G2"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":"SINGLE","path":"single","pipette":"6271d084-b692-4b40-b2aa-ca408d25380e","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"2","tipRack":"opentrons/opentrons_flex_96_tiprack_50ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"10"},"9261dede-9d97-45a3-abfa-5603b1759bf3":{"id":"9261dede-9d97-45a3-abfa-5603b1759bf3","stepType":"pause","stepName":"pause","stepDetails":"","stepNumber":0,"moduleId":null,"pauseAction":"untilResume","pauseMessage":"Pre-stocks are completed! Remove tube racks from deck and continue to make working stocks.","pauseTemperature":null,"pauseTime":null},"fcd9284f-9102-4520-b15f-39e1b72445b1":{"id":"fcd9284f-9102-4520-b15f-39e1b72445b1","stepType":"moveLiquid","stepName":"Water to folding rxn","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"10","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.5","aspirate_flowRate":"716","aspirate_labware":"4d883151-3381-4672-8ce1-83c63dfc3e86:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":"50","aspirate_mmFromBottom":2,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"10","dispense_delay_checkbox":false,"dispense_delay_seconds":"0","dispense_flowRate":"716","dispense_labware":"4d883151-3381-4672-8ce1-83c63dfc3e86:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["D1"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"water","nozzles":null,"path":"single","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"50"},"9fceb603-31e9-42b8-9bae-46e4b9f104f3":{"id":"9fceb603-31e9-42b8-9bae-46e4b9f104f3","stepType":"moveLiquid","stepName":"Salts to folding rxn","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"10","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.5","aspirate_flowRate":"716","aspirate_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":"50","aspirate_mmFromBottom":2,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["B1","C1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"10","dispense_delay_checkbox":false,"dispense_delay_seconds":"0","dispense_flowRate":"716","dispense_labware":"4d883151-3381-4672-8ce1-83c63dfc3e86:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["D1"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"water","nozzles":null,"path":"single","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"10"},"d4dc7827-0c73-4e86-8dff-24b9d0a469e4":{"id":"d4dc7827-0c73-4e86-8dff-24b9d0a469e4","stepType":"moveLiquid","stepName":"H1 - G1","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"5","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.2","aspirate_flowRate":"716","aspirate_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":null,"aspirate_mmFromBottom":null,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["H1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"50","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"5","dispense_delay_checkbox":true,"dispense_delay_seconds":"0.2","dispense_flowRate":null,"dispense_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":null,"dispense_mmFromBottom":null,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["G1"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":true,"disposalVolume_volume":null,"dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":null,"path":"single","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"2","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"80"},"a9081e0d-28a3-4265-95b1-fc26571f09a2":{"id":"a9081e0d-28a3-4265-95b1-fc26571f09a2","stepType":"moveLiquid","stepName":"Prestock Core 2","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"10","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.5","aspirate_flowRate":"716","aspirate_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":0.5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A2","B2"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":"dest_well","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"10","dispense_delay_checkbox":false,"dispense_delay_seconds":"0","dispense_flowRate":"716","dispense_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A2"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":null,"path":"multiAspirate","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"120"},"4151c8e2-12b0-48ee-9111-3220d13f5ffd":{"id":"4151c8e2-12b0-48ee-9111-3220d13f5ffd","stepType":"moveLiquid","stepName":"Prestock Core 3","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"10","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.5","aspirate_flowRate":"716","aspirate_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":0.5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["C2","D2"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":"dest_well","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"10","dispense_delay_checkbox":false,"dispense_delay_seconds":"0","dispense_flowRate":"716","dispense_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["B2"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":null,"path":"multiAspirate","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"120"},"915ad6f0-466b-4930-bf48-dfd01ea96440":{"id":"915ad6f0-466b-4930-bf48-dfd01ea96440","stepType":"moveLiquid","stepName":"Prestock Core 4","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"10","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.5","aspirate_flowRate":"716","aspirate_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":0.5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["E2","F2"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":"dest_well","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"10","dispense_delay_checkbox":false,"dispense_delay_seconds":"0","dispense_flowRate":"716","dispense_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["C2"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":null,"path":"multiAspirate","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"120"},"80474435-7454-47e8-9496-08009ca1a219":{"id":"80474435-7454-47e8-9496-08009ca1a219","stepType":"moveLiquid","stepName":"Prestock Core 5","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":"716","aspirate_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":0.5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["G2"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":null,"changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":false,"dispense_airGap_volume":"","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":"716","dispense_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":false,"dispense_mix_times":"","dispense_mix_volume":"","dispense_mmFromBottom":1,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["D2"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":null,"path":"single","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"190"},"efea65a1-182e-4294-9052-f45d175c7ce2":{"id":"efea65a1-182e-4294-9052-f45d175c7ce2","stepType":"moveLiquid","stepName":"Prestock Core 1","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"10","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.5","aspirate_flowRate":"716","aspirate_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","aspirate_mix_checkbox":false,"aspirate_mix_times":null,"aspirate_mix_volume":null,"aspirate_mmFromBottom":0.5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["G1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":"dest_well","changeTip":"once","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"10","dispense_delay_checkbox":false,"dispense_delay_seconds":"0","dispense_flowRate":"716","dispense_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["D1"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":null,"path":"single","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"200"},"d54c4fa7-82e7-49b5-8b18-1efd038d7100":{"id":"d54c4fa7-82e7-49b5-8b18-1efd038d7100","stepType":"moveLiquid","stepName":"Core 2-4 to WS","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":"716","aspirate_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","aspirate_mix_checkbox":false,"aspirate_mix_times":"","aspirate_mix_volume":"","aspirate_mmFromBottom":1,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A2","B2","C2"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":null,"changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":false,"dispense_airGap_volume":"","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":"716","dispense_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":false,"dispense_mix_times":"","dispense_mix_volume":"","dispense_mmFromBottom":1,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A6"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":null,"path":"single","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"24"},"7b08adb8-75d9-4f1f-8c59-d216be11987d":{"id":"7b08adb8-75d9-4f1f-8c59-d216be11987d","stepType":"moveLiquid","stepName":"Core 5 to WS","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":"716","aspirate_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","aspirate_mix_checkbox":false,"aspirate_mix_times":"","aspirate_mix_volume":"","aspirate_mmFromBottom":1,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["D2","A6"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":null,"changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":false,"dispense_airGap_volume":"","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":"716","dispense_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":false,"dispense_mix_times":"","dispense_mix_volume":"","dispense_mmFromBottom":1,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A6"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"water","nozzles":null,"path":"single","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"19"},"0327cf3b-b1a6-4a23-ba8b-e996a28b5600":{"id":"0327cf3b-b1a6-4a23-ba8b-e996a28b5600","stepType":"pause","stepName":"pause","stepDetails":"","stepNumber":0,"moduleId":null,"pauseAction":"untilResume","pauseMessage":"Working stock is complete. Proceed to set up folding reaction","pauseTemperature":null,"pauseTime":null},"5cefa9fe-400c-4547-95f2-6038389d2729":{"id":"5cefa9fe-400c-4547-95f2-6038389d2729","stepType":"moveLiquid","stepName":"Add Scaffold to folding rxn","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":"716","aspirate_labware":"4d883151-3381-4672-8ce1-83c63dfc3e86:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","aspirate_mix_checkbox":false,"aspirate_mix_times":"","aspirate_mix_volume":"","aspirate_mmFromBottom":1,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A4"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":null,"changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":false,"dispense_airGap_volume":"","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":"716","dispense_labware":"4d883151-3381-4672-8ce1-83c63dfc3e86:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":false,"dispense_mix_times":"","dispense_mix_volume":"","dispense_mmFromBottom":1,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["D1"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":null,"path":"single","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"10"},"0f06ea9e-6302-41a4-ba2a-dea48e999bfb":{"id":"0f06ea9e-6302-41a4-ba2a-dea48e999bfb","stepType":"moveLiquid","stepName":"OMD 2 Col 9","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"0.1","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.2","aspirate_flowRate":"24","aspirate_labware":"61950488-605c-4c0c-a941-f85d908c0ec3:custom_beta/fisherscientific_96_wellplate_1200ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":"50","aspirate_mmFromBottom":null,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A9","B9","C9","D9","E9","F9","G9"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"50","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"0.1","dispense_delay_checkbox":true,"dispense_delay_seconds":"0.2","dispense_flowRate":"50","dispense_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A2","B2","C2","D2","E2","F2","G2"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":"SINGLE","path":"single","pipette":"6271d084-b692-4b40-b2aa-ca408d25380e","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"2","tipRack":"opentrons/opentrons_flex_96_tiprack_50ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"10"},"cb7ddf89-5732-435a-9160-e07714416d9c":{"id":"cb7ddf89-5732-435a-9160-e07714416d9c","stepType":"moveLiquid","stepName":"OMD 2 Col 10","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"0.1","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.2","aspirate_flowRate":"24","aspirate_labware":"61950488-605c-4c0c-a941-f85d908c0ec3:custom_beta/fisherscientific_96_wellplate_1200ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":"50","aspirate_mmFromBottom":null,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A10","B10","C10","D10","E10","F10","G10"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"50","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"0.1","dispense_delay_checkbox":true,"dispense_delay_seconds":"0.2","dispense_flowRate":"50","dispense_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A2","B2","C2","D2","E2","F2","G2"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":"SINGLE","path":"single","pipette":"6271d084-b692-4b40-b2aa-ca408d25380e","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"2","tipRack":"opentrons/opentrons_flex_96_tiprack_50ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"10"},"16381780-7d0b-4c67-a287-f4f9b99be02a":{"id":"16381780-7d0b-4c67-a287-f4f9b99be02a","stepType":"moveLiquid","stepName":"OMD 2 Col 11","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"0.1","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.2","aspirate_flowRate":"24","aspirate_labware":"61950488-605c-4c0c-a941-f85d908c0ec3:custom_beta/fisherscientific_96_wellplate_1200ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":"50","aspirate_mmFromBottom":null,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A11","B11","C11","D11","E11","F11","G11"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"50","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"0.1","dispense_delay_checkbox":true,"dispense_delay_seconds":"0.2","dispense_flowRate":"50","dispense_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A2","B2","C2","D2","E2","F2","G2"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":"SINGLE","path":"single","pipette":"6271d084-b692-4b40-b2aa-ca408d25380e","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"2","tipRack":"opentrons/opentrons_flex_96_tiprack_50ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"10"},"522d2fcf-28e0-4a40-821c-38bc1ab5f00c":{"id":"522d2fcf-28e0-4a40-821c-38bc1ab5f00c","stepType":"moveLiquid","stepName":"OMD 2 Col 12","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"0.1","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.2","aspirate_flowRate":"24","aspirate_labware":"61950488-605c-4c0c-a941-f85d908c0ec3:custom_beta/fisherscientific_96_wellplate_1200ul/1","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":"50","aspirate_mmFromBottom":null,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":null,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A12","B12","C12","D12","E12","F12","G12"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"50","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"0.1","dispense_delay_checkbox":true,"dispense_delay_seconds":"0.2","dispense_flowRate":"50","dispense_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A2","B2","C2","D2","E2","F2","G2"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":"SINGLE","path":"single","pipette":"6271d084-b692-4b40-b2aa-ca408d25380e","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"2","tipRack":"opentrons/opentrons_flex_96_tiprack_50ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"10"},"b5f099bd-3415-4927-94de-4787a3c2a516":{"id":"b5f099bd-3415-4927-94de-4787a3c2a516","stepType":"moveLiquid","stepName":"Core 1 to WS","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":"716","aspirate_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","aspirate_mix_checkbox":false,"aspirate_mix_times":"","aspirate_mix_volume":"","aspirate_mmFromBottom":1,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["D1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":null,"changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":false,"dispense_airGap_volume":"","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":"716","dispense_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":false,"dispense_mix_times":"","dispense_mix_volume":"","dispense_mmFromBottom":1,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A6"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":null,"path":"single","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"20"},"9237ef9d-e0f6-469c-bd17-d21b910766a4":{"id":"9237ef9d-e0f6-469c-bd17-d21b910766a4","stepType":"moveLiquid","stepName":"Add Staples to folding rxn","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"10","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.5","aspirate_flowRate":"716","aspirate_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":"50","aspirate_mmFromBottom":2,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A6"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"10","dispense_delay_checkbox":false,"dispense_delay_seconds":"0","dispense_flowRate":"716","dispense_labware":"4d883151-3381-4672-8ce1-83c63dfc3e86:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":false,"dispense_mix_times":"1","dispense_mix_volume":"50","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["D1"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"water","nozzles":null,"path":"single","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"20"},"c543f576-d7af-44fa-bf1b-8e6f2f02dfe2":{"id":"c543f576-d7af-44fa-bf1b-8e6f2f02dfe2","stepType":"moveLiquid","stepName":"Water to WS + Mix","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":true,"aspirate_airGap_volume":"10","aspirate_delay_checkbox":true,"aspirate_delay_seconds":"0.5","aspirate_flowRate":"716","aspirate_labware":"4d883151-3381-4672-8ce1-83c63dfc3e86:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","aspirate_mix_checkbox":false,"aspirate_mix_times":"1","aspirate_mix_volume":"50","aspirate_mmFromBottom":2,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["A1"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":"dest_well","changeTip":"always","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":true,"dispense_airGap_volume":"10","dispense_delay_checkbox":false,"dispense_delay_seconds":"0","dispense_flowRate":"716","dispense_labware":"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3","dispense_mix_checkbox":true,"dispense_mix_times":"3","dispense_mix_volume":"100","dispense_mmFromBottom":2,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["A6"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"water","nozzles":null,"path":"single","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"17"},"2c5d1523-7d07-4e3c-9ffa-d644c55c2ecc":{"id":"2c5d1523-7d07-4e3c-9ffa-d644c55c2ecc","stepType":"moveLiquid","stepName":"Prestock Core 5 premix","stepDetails":"","stepNumber":0,"aspirate_airGap_checkbox":false,"aspirate_airGap_volume":"","aspirate_delay_checkbox":false,"aspirate_delay_seconds":"1","aspirate_flowRate":"716","aspirate_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","aspirate_mix_checkbox":false,"aspirate_mix_times":"","aspirate_mix_volume":"","aspirate_mmFromBottom":0.5,"aspirate_position_reference":"well-bottom","aspirate_retract_delay_seconds":"0","aspirate_retract_mmFromBottom":2,"aspirate_retract_speed":"50","aspirate_retract_x_position":0,"aspirate_retract_y_position":0,"aspirate_retract_position_reference":"well-top","aspirate_submerge_delay_seconds":"0","aspirate_submerge_speed":"100","aspirate_submerge_mmFromBottom":2,"aspirate_submerge_x_position":0,"aspirate_submerge_y_position":0,"aspirate_submerge_position_reference":"well-top","aspirate_touchTip_checkbox":false,"aspirate_touchTip_mmFromTop":-1,"aspirate_touchTip_speed":"30","aspirate_touchTip_mmFromEdge":"0.5","aspirate_wellOrder_first":"t2b","aspirate_wellOrder_second":"l2r","aspirate_wells_grouped":false,"aspirate_wells":["H2"],"aspirate_x_position":0,"aspirate_y_position":0,"blowout_checkbox":false,"blowout_flowRate":"716","blowout_location":null,"changeTip":"once","conditioning_checkbox":false,"conditioning_volume":"","dispense_airGap_checkbox":false,"dispense_airGap_volume":"","dispense_delay_checkbox":false,"dispense_delay_seconds":"1","dispense_flowRate":"716","dispense_labware":"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3","dispense_mix_checkbox":false,"dispense_mix_times":"","dispense_mix_volume":"","dispense_mmFromBottom":1,"dispense_position_reference":"well-bottom","dispense_retract_delay_seconds":"0","dispense_retract_mmFromBottom":2,"dispense_retract_speed":"50","dispense_retract_x_position":0,"dispense_retract_y_position":0,"dispense_retract_position_reference":"well-top","dispense_submerge_delay_seconds":"0","dispense_submerge_speed":"100","dispense_submerge_mmFromBottom":2,"dispense_submerge_x_position":0,"dispense_submerge_y_position":0,"dispense_submerge_position_reference":"well-top","dispense_touchTip_checkbox":false,"dispense_touchTip_mmFromTop":-1,"dispense_touchTip_speed":"30","dispense_touchTip_mmFromEdge":"0.5","dispense_wellOrder_first":"t2b","dispense_wellOrder_second":"l2r","dispense_wells":["G2"],"dispense_x_position":0,"dispense_y_position":0,"disposalVolume_checkbox":false,"disposalVolume_volume":"","dropTip_location":"6dcb38b1-bffd-4702-b5c2-1650be676a4c:trashBin","liquidClassesSupported":true,"liquidClass":"none","nozzles":null,"path":"single","pipette":"3def0e45-a408-486d-8786-b6c2c43df782","preWetTip":false,"pushOut_checkbox":true,"pushOut_volume":"20","tipRack":"opentrons/opentrons_flex_96_tiprack_1000ul/1","tip_tracking":"automatic","tiprack_selected":null,"tips_selected":[],"volume":"70"},"01e15f4b-df3a-4dc9-9221-a76f336b08cc":{"id":"01e15f4b-df3a-4dc9-9221-a76f336b08cc","stepType":"pause","stepName":"pause","stepDetails":"","stepNumber":0,"moduleId":null,"pauseAction":"untilResume","pauseMessage":"Folding buffer ready. Proceed to add staples and scaffold!","pauseTemperature":null,"pauseTime":null}},"orderedStepIds":["966880bf-dfbe-4023-90fe-320f0ffa846c","8b141246-49e4-45ef-a8ee-b96a3849d45b","cd2f611c-a231-4ced-bfa7-29c8a2b49784","fc97397e-29bb-4407-808e-28e0bbb077a0","e72b6f8f-ba5b-4231-9b3e-f68700657fde","d4dc7827-0c73-4e86-8dff-24b9d0a469e4","854cebbc-8bf5-4d9e-90b3-9f36d6c9e3bc","063d3964-dcf2-4fd6-86aa-65d39e74f595","0f06ea9e-6302-41a4-ba2a-dea48e999bfb","cb7ddf89-5732-435a-9160-e07714416d9c","16381780-7d0b-4c67-a287-f4f9b99be02a","522d2fcf-28e0-4a40-821c-38bc1ab5f00c","2f8958ca-5e0b-4e01-832c-eb54f9c8b375","fd5139d4-5097-4baf-ba4e-ca057d9e3779","96e3414c-97d0-4ac5-bb8b-bc9e7d9dbe98","efea65a1-182e-4294-9052-f45d175c7ce2","a9081e0d-28a3-4265-95b1-fc26571f09a2","4151c8e2-12b0-48ee-9111-3220d13f5ffd","915ad6f0-466b-4930-bf48-dfd01ea96440","2c5d1523-7d07-4e3c-9ffa-d644c55c2ecc","80474435-7454-47e8-9496-08009ca1a219","9261dede-9d97-45a3-abfa-5603b1759bf3","b5f099bd-3415-4927-94de-4787a3c2a516","d54c4fa7-82e7-49b5-8b18-1efd038d7100","7b08adb8-75d9-4f1f-8c59-d216be11987d","c543f576-d7af-44fa-bf1b-8e6f2f02dfe2","fcd9284f-9102-4520-b15f-39e1b72445b1","9fceb603-31e9-42b8-9bae-46e4b9f104f3","01e15f4b-df3a-4dc9-9221-a76f336b08cc","5cefa9fe-400c-4547-95f2-6038389d2729","9237ef9d-e0f6-469c-bd17-d21b910766a4","0327cf3b-b1a6-4a23-ba8b-e996a28b5600"],"pipettes":{"3def0e45-a408-486d-8786-b6c2c43df782":{"pipetteName":"p1000_single_flex"},"6271d084-b692-4b40-b2aa-ca408d25380e":{"pipetteName":"p50_multi_flex"}},"modules":{"25f9bdc0-f76c-4a75-8379-0291edcd6c17:thermocyclerModuleType":{"model":"thermocyclerModuleV2"}},"labware":{"bdd5ce09-3a12-4782-bd5b-0480508e4dcd:opentrons/opentrons_flex_96_tiprack_1000ul/1":{"displayName":"Opentrons Flex 96 Tip Rack 1000 µL","labwareDefURI":"opentrons/opentrons_flex_96_tiprack_1000ul/1"},"f06ce940-053b-4051-a8ec-c08c3e7524f3:opentrons/opentrons_flex_96_tiprack_50ul/1":{"displayName":"Opentrons Flex 96 Tip Rack 50 µL","labwareDefURI":"opentrons/opentrons_flex_96_tiprack_50ul/1"},"5f862063-d2f9-4a59-a13a-90bb1f263046:custom_beta/fisherscientific_96_wellplate_1200ul/1":{"displayName":"OMD 1","labwareDefURI":"custom_beta/fisherscientific_96_wellplate_1200ul/1"},"61950488-605c-4c0c-a941-f85d908c0ec3:custom_beta/fisherscientific_96_wellplate_1200ul/1":{"displayName":"OMD 2","labwareDefURI":"custom_beta/fisherscientific_96_wellplate_1200ul/1"},"3c025f8e-7f46-4d99-a398-9dd1a8fb3285:opentrons/thermoscientificnunc_96_wellplate_2000ul/3":{"displayName":"Transfer Plate","labwareDefURI":"opentrons/thermoscientificnunc_96_wellplate_2000ul/3"},"20703b15-e4a7-4f5a-8d8a-6cf04086e761:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3":{"displayName":"Pre-Stock Tube Rack","labwareDefURI":"opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3"},"f44be508-e0a6-4598-9d20-b54685447fea:opentrons/opentrons_flex_96_tiprack_50ul/1":{"displayName":"Opentrons Flex 96 Tip Rack 50 µL (2)","labwareDefURI":"opentrons/opentrons_flex_96_tiprack_50ul/1"},"4d883151-3381-4672-8ce1-83c63dfc3e86:opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3":{"displayName":"Working Stock Reagents","labwareDefURI":"opentrons/opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap/3"}}}},"metadata":{"protocolName":"Gear Pre-stock Protocol","author":"","description":"Pre-stock protocol for gear structure using OMD1 and OMD2 for Gear Overhang Rep and Gear Core. This protocol transfer 10ul from wells to make 4 pre-stock tubes in 1.5ml Eppendorf Tubes. \n\nKehao Huang","source":"Protocol Designer","created":1764947601558,"lastModified":1766158033213}}"""
