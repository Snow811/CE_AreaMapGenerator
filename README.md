# AreaMapGenerator

AreaMapGenerator is a tool for generating `.tga` masks for DayZ Community Edition (CE) loot zone layers. It uses building placement and loot point data to produce rotation-aware, tag-specific masks compatible with CE's `usgFlg_Def-*` layers.

## Features

- Parses `mapgrouppos.xml` for building positions and rotation
- Parses `mapgroupproto.xml` for loot tags and spawn points
- Applies rotation and translation to loot points
- Converts world coordinates to pixel space
- Generates `.tga` masks for CE layer import
- Supports `usgFlg_Def-All` as a global loot mask
- Case-insensitive group name matching
- Excludes non-relevant layers from output

## Directory Structure

AreaMapGenerator/
├── main.py
├── src/
│   ├── config_parser.py
│   ├── generator.py
│   ├── mapper.py
├── data/
│   ├── config/
│   │   └── chernarusplus.xml
│   ├── mapgrouppos.xml
│   └── mapgroupproto.xml
├── output/
│   └── *.tga



## Setup

1. Place CE config XML (e.g., `chernarusplus.xml`) in `data/config/`
2. Place `mapgrouppos.xml` and `mapgroupproto.xml` in `data/`
3. Install dependencies:

```bash
pip install lxml pillow numpy
```
Run the tool:

```bash
python main.py
```
Excluded Layers
The following layers are excluded from mask generation:

keyPoint-Churches

usgFlg_Paint-Contamination

usgFlg_Paint-Historical

usgFlg_Paint-Lunapark

valueFlg_Tier1

valueFlg_Tier2

valueFlg_Tier3

valueFlg_Tier4

valueFlg_Unique

water-fresh

water-sea

Build Executable (Optional)
To compile into a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --name AreaMapGenerator main.py
```
Notes
Loot points are rotated using the a attribute from mapgrouppos.xml

Only X and Z coordinates are used for mask generation

Masks are saved as grayscale .tga files in the output/ directory

Group name matching is case-insensitive
