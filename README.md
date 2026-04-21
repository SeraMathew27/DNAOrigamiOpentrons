**Optimize your DNA Origami Folding Workflow w/Opentrons**

To complete your workflow, this project contains the following protocols that can be uploaded into the Opentrons App for customization
1. Prestock Protocol (Pooled oligos from IDT plates)
2. Working Stock Protocol (Complete staple mix)
3. Folding Reaction (staples + scaffold + folding reagents preparations added to the Opentrons thermocycler to complete folding)
+ option of combining WS Protocol + Folding Reaction

Requirements:


User Guide:
Robot: Opentrons Flex
API Level: 2.25
Pipette: flex_1channel_1000 
Tips: Opentrons Flex 1000 µL tip racks
Custom Labware: Fisher Scientific 96 Well Plate 1200 µL (fisherscientific_96_wellplate_1200ul)
Destination Labware: Opentrons 24 Tube Rack with Eppendorf 1.5 mL Safelock Snapcap tubes

**Prestock Protocol**


Deck Layout:
<img width="741" height="560" alt="image" src="https://github.com/user-attachments/assets/ef33f2fd-ac4c-4fd4-9a58-6fe9c86b27b0" />

Labware:
* Pipette: flex_1channel_1000
* Tips: Opentrons Flex 1000 µL tip racks
* Source: 96-Well Plate (upload options to Python file and select labware at runtime)
* Destination:
<img width="1509" height="303" alt="image" src="https://github.com/user-attachments/assets/ddd286a0-500b-4c90-9769-eb171b1c50a2" />

How To Use:
1. Input transfer into the CSV file:
   * In between the water row and the header, insert rows with the name of your prestock, source plate, wells, destination well, and transfer amount. 
   * Make sure the water row is kept in and its values are unchanged! This row is kept so that the Working Stock sheet can reference its source location.
2. Download the _Prestock_Prep_with_CSV_Import.py_
3. Upload 

Run-Time Parameters:
* Transfers CSV File: Contains the wells corresponding to each prestock, and the amount to transfer per well
  *  the source rack for water.
* Source Labware: 96-well plate containing oligos
  * Options (edit Python script to add more options/upload custom labware): Custom 1200ul Fisher Scientific 96 Well Plate
* Pipette Mount: Mount for 1000ul Pipette (left, right)


