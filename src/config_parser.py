from lxml import etree

def parse_zg_config(config_path):
    tree = etree.parse(config_path)
    root = tree.getroot()

    global_node = root.find("global")
    world_size = int(global_node.find("world").get("size"))
    layer_size = int(global_node.find("layer").get("size"))

    usages = [u.get("name") for u in root.find("areas").find("usages").findall("usage")]
    values = [v.get("name") for v in root.find("areas").find("values").findall("value")]

    layers = {}
    for layer in root.find("layers").findall("layer"):
        name = layer.get("name")
        color = int(layer.get("color"))
        usage_flags = int(layer.get("usage_flags"))
        value_flags = int(layer.get("value_flags"))
        layers[name] = {
            "color": color,
            "usage_flags": usage_flags,
            "value_flags": value_flags
        }

    return {
        "world_size": world_size,
        "layer_size": layer_size,
        "usages": usages,
        "values": values,
        "layers": layers
    }

def parse_mapgroupproto(proto_path):
    tree = etree.parse(proto_path)
    root = tree.getroot()

    group_tags = {}

    for group in root.findall("group"):
        group_name = group.get("name")
        usages = set()
        values = set()
        loot_points = []

        for usage in group.findall("usage"):
            name = usage.get("name")
            if name:
                usages.add(name)

        for value in group.findall("value"):
            name = value.get("name")
            if name:
                values.add(name)

        for container in group.findall("container"):
            for point in container.findall("point"):
                pos_str = point.get("pos")
                if pos_str:
                    parts = pos_str.strip().split()
                    if len(parts) == 3:
                        x = float(parts[0])
                        z = float(parts[2])  # ignore Y
                        loot_points.append((x, z))

        group_tags[group_name] = {
            "usages": list(usages),
            "values": list(values),
            "points": loot_points
        }

    return group_tags
