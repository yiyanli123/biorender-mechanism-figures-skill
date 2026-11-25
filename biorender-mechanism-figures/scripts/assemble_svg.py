#!/usr/bin/env python3
"""Inline standalone icons into a native, editable SVG figure layout."""

import argparse
from copy import deepcopy
from pathlib import Path
import re
import xml.etree.ElementTree as ET


SVG = "http://www.w3.org/2000/svg"
INKSCAPE = "http://www.inkscape.org/namespaces/inkscape"
ET.register_namespace("", SVG)
ET.register_namespace("inkscape", INKSCAPE)

SHAPES = {"path", "rect", "circle", "ellipse", "line", "polygon", "polyline"}
EDITABLE_TAGS = SHAPES | {
    "svg", "g", "title", "desc", "defs", "text", "tspan", "marker", "clipPath",
    "linearGradient", "radialGradient", "stop",
}
TOKEN = re.compile(r"[a-zA-Z_][a-zA-Z0-9_.-]*")
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
URL = re.compile(r"url\(\s*(['\"]?)(#[a-zA-Z_][a-zA-Z0-9_.-]*)\1\s*\)")
URL_START = re.compile(r"url\s*\(", re.IGNORECASE)
ID_LIST_ATTRIBUTES = {"aria-labelledby", "aria-describedby"}
ICON_METADATA = {"id", "viewBox", "width", "height", "x", "y", "version", "role"}


def validate_document(root, source):
    if root.tag != f"{{{SVG}}}svg":
        raise ValueError(f"{source}: expected an SVG root")
    ids = set()
    references = set()
    for node in root.iter():
        tag = node.tag.removeprefix(f"{{{SVG}}}")
        if node.tag != f"{{{SVG}}}{tag}" or tag not in EDITABLE_TAGS:
            raise ValueError(f"{source}: unsupported element <{tag}>")
        name = node.get("id")
        if name is not None:
            if not TOKEN.fullmatch(name) or name in ids:
                raise ValueError(f"{source}: invalid or duplicate ID {name!r}")
            ids.add(name)
        for attr, value in node.attrib.items():
            local_name = attr.rsplit("}", 1)[-1].lower()
            if local_name in {"href", "base"} or local_name.startswith("on"):
                raise ValueError(f"{source}: unsupported attribute {attr!r}")
            if attr in ID_LIST_ATTRIBUTES:
                references.update(value.split())
            references.update(match[1][1:] for match in URL.findall(value))
            if URL_START.search(URL.sub("", value)):
                raise ValueError(f"{source}: only local SVG references are supported")
    missing = references - ids
    if missing:
        raise ValueError(f"{source}: unresolved reference(s): {', '.join(sorted(missing))}")


def inline_icon(slot, icon):
    prefix = f"{slot.get('id')}--"
    group = ET.Element(f"{{{SVG}}}g", {
        attr: value for attr, value in icon.attrib.items() if attr not in ICON_METADATA
    })
    if "id" in icon.attrib:
        group.set("id", icon.get("id"))
    group.extend(deepcopy(child) for child in icon)
    for element in group.iter():
        for attr, value in element.attrib.items():
            if attr == "id":
                element.set(attr, prefix + value)
            elif attr in ID_LIST_ATTRIBUTES:
                element.set(attr, " ".join(prefix + item for item in value.split()))
            else:
                element.set(attr, URL.sub(lambda match: f"url(#{prefix}{match[2][1:]})", value))
    slot.append(group)
    del slot.attrib["data-icon"]


def assemble(layout, output):
    tree = ET.parse(layout)
    root = tree.getroot()
    validate_document(root, layout)
    icons = layout.parent / "icons"
    if output.resolve() == layout.resolve() or output.resolve().is_relative_to(icons.resolve()):
        raise ValueError("Output must be separate from the layout and icon files")
    sources = {}
    for slot in list(root.iter()):
        slug = slot.get("data-icon")
        if slug is None:
            continue
        if slot.tag != f"{{{SVG}}}g" or not slot.get("id") or len(slot) or (slot.text or "").strip():
            raise ValueError("Each icon placeholder must be an empty <g> with a unique ID")
        if not SLUG.fullmatch(slug):
            raise ValueError(f"Invalid icon name {slug!r}; use a lowercase hyphenated filename stem")
        if slug not in sources:
            path = icons / f"{slug}.svg"
            icon = ET.parse(path).getroot()
            validate_document(icon, path)
            if icon.get("viewBox", "").split() != ["0", "0", "128", "128"]:
                raise ValueError(f"{path}: expected viewBox='0 0 128 128'")
            if not any(element.tag.removeprefix(f"{{{SVG}}}") in SHAPES for element in icon.iter()):
                raise ValueError(f"{path}: icon needs at least one vector shape")
            if any("data-icon" in element.attrib for element in icon.iter()):
                raise ValueError(f"{path}: icon files must be standalone")
            sources[slug] = icon
        inline_icon(slot, sources[slug])
    validate_document(root, output)
    tree.write(output, encoding="utf-8", xml_declaration=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("layout", type=Path, help="SVG layout with data-icon placeholders and a sibling icons/ directory")
    parser.add_argument("--output", type=Path, required=True, help="Path to the finished SVG")
    args = parser.parse_args()
    try:
        assemble(args.layout, args.output)
    except (ValueError, OSError, ET.ParseError) as error:
        parser.exit(1, f"assemble_svg: {error}\n")


if __name__ == "__main__":
    main()
