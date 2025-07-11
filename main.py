import os
import glob
from src.config_parser import parse_zg_config, parse_mapgroupproto
from src.generator import create_blank_mask, paint_mask, save_mask
import xml.etree.ElementTree as ET

CONFIG_DIR = "data/config"
GROUPPOS_PATH = "data/mapgrouppos.xml"
PROTO_PATH = "data/mapgroupproto.xml"
OUTPUT_DIR = "output"

EXCLUDED_LAYERS = {
    "keyPoint-Churches",
    "usgFlg_Paint-Contamination",
    "usgFlg_Paint-Historical",
    "usgFlg_Paint-Lunapark",
    "valueFlg_Tier1",
    "valueFlg_Tier2",
    "valueFlg_Tier3",
    "valueFlg_Tier4",
    "valueFlg_Unique",
    "water-fresh",
    "water-sea"
}

def ensure_setup():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    missing = []
    if not glob.glob(os.path.join(CONFIG_DIR, "*.xml")):
        missing.append("CE config XML (e.g., chernarusplus.xml) in data/config/")
    if not os.path.exists(GROUPPOS_PATH):
        missing.append("mapgrouppos.xml in data/")
    if not os.path.exists(PROTO_PATH):
        missing.append("mapgroupproto.xml in data/")

    if missing:
        print("Setup incomplete. Please add the following files:")
        for item in missing:
            print(f" - {item}")
        input("\nPress Enter to exit...")
        exit()

def find_config_file():
    xml_files = glob.glob(os.path.join(CONFIG_DIR, "*.xml"))
    return xml_files[0]

def parse_building_positions(path):
    tree = ET.parse(path)
    root = tree.getroot()
    buildings = []
    for group in root.findall("group"):
        pos_str = group.get("pos")
        rot_str = group.get("a")
        if not pos_str or rot_str is None:
            continue
        parts = pos_str.strip().split()
        if len(parts) != 3:
            continue
        x = float(parts[0])
        z = float(parts[2])
        rotation = float(rot_str)
        group_name = group.get("name")
        buildings.append({"x": x, "z": z, "rotation": rotation, "group": group_name})
    return buildings

def group_by_tag(buildings, group_tags, layers):
    tag_groups = {tag: [] for tag in layers.keys()}
    unmatched_groups = set()
    tag_usage_count = {}

    def_all_key = "usgFlg_Def-All"
    if def_all_key in layers:
        tag_groups[def_all_key] = []

    # Create case-insensitive lookup for proto groups
    matched_keys = {k.lower(): k for k in group_tags}

    for b in buildings:
        group = b["group"]
        group_lower = group.lower()

        if group_lower in matched_keys:
            actual_key = matched_keys[group_lower]
            tags = group_tags[actual_key]["usages"] + group_tags[actual_key]["values"]
            loot_points = group_tags[actual_key]["points"]

            # Add to Def-All if enabled
            if def_all_key in layers:
                for lx, lz in loot_points:
                    tag_groups[def_all_key].append({
                        "x": b["x"],
                        "z": b["z"],
                        "rotation": b["rotation"],
                        "offset_x": lx,
                        "offset_z": lz
                    })

            for tag in tags:
                matching_layers = [lname for lname in layers if lname.endswith(f"-{tag}") or lname.endswith(f"_{tag}")]
                for layer_name in matching_layers:
                    for lx, lz in loot_points:
                        tag_groups[layer_name].append({
                            "x": b["x"],
                            "z": b["z"],
                            "rotation": b["rotation"],
                            "offset_x": lx,
                            "offset_z": lz
                        })
                    tag_usage_count[layer_name] = tag_usage_count.get(layer_name, 0) + 1
        else:
            unmatched_groups.add(group)

    print(f"\n✅ Tag assignment summary:")
    for layer, count in tag_usage_count.items():
        print(f" - {layer}: {count} buildings")

    if def_all_key in tag_groups:
        print(f"\n🗺️ Def-All: {len(tag_groups[def_all_key])} total loot points")

    if unmatched_groups:
        print(f"\n⚠️ Unmatched groups: {len(unmatched_groups)}")
        for g in list(unmatched_groups)[:10]:
            print(f" - {g}")
        if len(unmatched_groups) > 10:
            print(" - ...")

    return tag_groups

def main():
    ensure_setup()

    config_path = find_config_file()
    print(f"Using config file: {os.path.basename(config_path)}")

    config = parse_zg_config(config_path)
    group_tags = parse_mapgroupproto(PROTO_PATH)
    buildings = parse_building_positions(GROUPPOS_PATH)

    print(f"\n📦 Loaded {len(buildings)} buildings")
    print(f"📄 Loaded {len(group_tags)} group tag profiles")

    world_size = config["world_size"]
    layer_size = config["layer_size"]
    layers = config["layers"]

    tag_groups = group_by_tag(buildings, group_tags, layers)

    # Remove excluded layers
    tag_groups = {
        layer: positions
        for layer, positions in tag_groups.items()
        if layer not in EXCLUDED_LAYERS
    }

    for layer_name, positions in tag_groups.items():
        print(f"\n🖼️ Generating mask for layer: {layer_name} with {len(positions)} positions")
        mask = create_blank_mask(layer_size)
        paint_mask(mask, positions, world_size, layer_size)
        output_path = os.path.join(OUTPUT_DIR, f"{layer_name}.tga")
        save_mask(mask, output_path)

    print("\n✅ Done! Masks saved to output/")

if __name__ == "__main__":
    main()
