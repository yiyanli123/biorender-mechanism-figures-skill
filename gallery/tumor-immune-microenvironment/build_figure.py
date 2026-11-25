#!/usr/bin/env python3
"""Assemble the editable tumor microenvironment SVG from standalone icons."""

from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
ICONS = ROOT.parents[1] / "biorender-mechanism-figures" / "assets" / "icons" / "tumor-immune"
SVG = "http://www.w3.org/2000/svg"
INK = "http://www.inkscape.org/namespaces/inkscape"
ET.register_namespace("", SVG)
ET.register_namespace("inkscape", INK)

NAVY = "#213842"
MUTED = "#526871"
CORAL = "#974e50"
TEAL = "#286b68"
BLUE = "#345982"
LINE = "#afbdc1"
W, H = 1680, 956


def node(parent, tag, name, **attrs):
    attributes = {key.replace("_", "-"): str(value) for key, value in attrs.items()}
    attributes["id"] = name
    return ET.SubElement(parent, f"{{{SVG}}}{tag}", attributes)


def layer(parent, name, title):
    group = node(parent, "g", name)
    group.set(f"{{{INK}}}groupmode", "layer")
    group.set(f"{{{INK}}}label", title)
    return group


def label(parent, name, value, x, y, size=20, *, color=NAVY, bold=False, center=False):
    node(parent, "text", name, x=x, y=y, font_size=size, fill=color,
         font_weight="700" if bold else "400",
         text_anchor="middle" if center else "start").text = value


def box(parent, name, x, y, width, height, fill, *, stroke="none", radius=10):
    return node(parent, "rect", name, x=x, y=y, width=width, height=height,
                rx=radius, fill=fill, stroke=stroke, stroke_width=1.4)


def arrow(parent, name, d, *, dash=False, head=True, color=MUTED, width=2.8):
    path = node(parent, "path", name, d=d, fill="none", stroke=color,
                stroke_width=width, stroke_linecap="round", stroke_linejoin="round")
    if dash:
        path.set("stroke-dasharray", "6 6")
    if head:
        path.set("marker-end", "url(#arrowhead)")
    return path


def icon(parent, name, slug, x, y, size, *, flip=False, rotate=0, opacity=1):
    source = ET.parse(ICONS / f"{slug}.svg").getroot()
    scale = size / 128
    offset = x + size if flip else x
    transform = f"translate({offset} {y}) scale({-scale if flip else scale} {scale})"
    if rotate:
        transform += f" rotate({rotate} 64 64)"
    group = node(parent, "g", name, transform=transform, opacity=opacity)
    group.set(f"{{{INK}}}label", name.replace("-", " "))
    for child in source.findall(f"{{{SVG}}}g"):
        part = deepcopy(child)
        for element in part.iter():
            if "id" in element.attrib:
                element.set("id", f"{name}--{element.get('id')}")
        group.append(part)
    return group


def panel(root, letter, title, subtitle, x, width, color, tint):
    group = layer(root, f"panel-{letter}", f"{letter.upper()}  {title}")
    box(group, f"{letter}-background", x, 146, width, 596, tint, stroke="#d6dfe1", radius=14)
    box(group, f"{letter}-badge", x + 24, 169, 36, 36, color, radius=8)
    label(group, f"{letter}-letter", letter.upper(), x + 42, 195, 21,
          color="#ffffff", bold=True, center=True)
    label(group, f"{letter}-heading", title, x + 73, 195, 29, bold=True)
    label(group, f"{letter}-subtitle", subtitle, x + 24, 226, 18, color=MUTED)
    return group


def build():
    root = ET.Element(f"{{{SVG}}}svg", width=str(W), height=str(H), viewBox=f"0 0 {W} {H}",
                      attrib={"font-family": "Arial, Helvetica, sans-serif", "role": "img",
                              "aria-labelledby": "figure-title figure-description"})
    node(root, "title", "figure-title").text = "Tumor immune microenvironment"
    node(root, "desc", "figure-description").text = (
        "Three-panel schematic of hypoxia, immune remodeling, and PD-1 checkpoint blockade."
    )
    defs = node(root, "defs", "definitions")
    marker = node(defs, "marker", "arrowhead", viewBox="0 0 10 10", refX=9, refY=5,
                  markerWidth=8, markerHeight=8, markerUnits="userSpaceOnUse", orient="auto")
    node(marker, "path", "arrow-tip", d="M0 0 10 5 0 10Z", fill=MUTED)

    header = layer(root, "header", "Figure title and page")
    box(header, "page-background", 0, 0, W, H, "#ffffff", radius=0)
    label(header, "main-title", "Tumor immune microenvironment", 36, 71, 47, bold=True)
    label(header, "main-subtitle", "Hypoxia, macrophage remodeling, and PD-1 checkpoint blockade",
          38, 110, 23, color=MUTED)

    a = panel(root, "a", "Hypoxic tumor core", "Oxygen availability and local signaling",
              36, 462, CORAL, "#fff8f5")
    for i, (x, y, size, rotation) in enumerate([
        (74, 320, 102, 22), (128, 293, 104, -36), (205, 309, 112, 35),
        (253, 357, 113, 65), (244, 436, 111, 20), (188, 476, 105, -16),
        (100, 466, 101, 10), (63, 388, 118, -31),
    ], 1):
        icon(a, f"tumor-cluster-cell-{i}", "tumor-cell", x, y, size, rotate=rotation, opacity=.50)
    icon(a, "branching-vessel", "blood-vessel", 63, 437, 208)
    icon(a, "foreground-tumor-cell", "tumor-cell", 104, 320, 207)
    box(a, "hypoxia-tag", 70, 249, 131, 41, "#f8e3df", stroke="#e6b9b3", radius=20)
    label(a, "hypoxia-label", "Hypoxia", 135, 277, 21, color=CORAL, bold=True, center=True)
    arrow(a, "hypoxia-to-tumor", "M149 296C153 316 169 331 179 344")
    box(a, "hif-tag", 150, 385, 122, 34, "#fff4ec", stroke="#d49691", radius=8)
    label(a, "hif-label", "HIF-1α", 211, 409, 22, color=CORAL, bold=True, center=True)
    icon(a, "nuclear-dna", "dna", 163, 388, 96)
    arrow(a, "tumor-to-signals", "M299 416C318 412 339 400 356 383", dash=True)
    for i, (slug, x, y, size) in enumerate([
        ("ccl2", 350, 352, 19), ("ccl2", 386, 374, 23), ("ccl2", 363, 409, 20),
        ("ccl2", 409, 426, 16), ("csf1", 380, 337, 22), ("csf1", 419, 347, 20),
        ("csf1", 425, 393, 24), ("csf1", 384, 416, 18),
    ], 1):
        icon(a, f"niche-{slug}-particle-{i}", slug, x, y, size)
    label(a, "ccl2-particle-label", "CCL2", 365, 480, 20, color=TEAL, bold=True)
    label(a, "csf1-particle-label", "CSF1", 425, 480, 20, color="#865921", bold=True)
    label(a, "tumor-cell-label", "Tumor cells", 221, 609, 21, color=CORAL, bold=True, center=True)
    arrow(a, "a-caption-rule", "M61 639H473", head=False, color="#e8ccc7", width=1.3)
    label(a, "a-caption-line-1", "Low oxygen stabilizes HIF-1α.", 61, 671, 18, bold=True)
    label(a, "a-caption-line-2", "Niche signals can support myeloid recruitment", 61, 699, 17, color=MUTED)
    label(a, "a-caption-line-3", "and survival, depending on tumor context.", 61, 721, 17, color=MUTED)

    b = panel(root, "b", "Immune remodeling", "Monocyte recruitment and local suppression",
              514, 536, TEAL, "#f3faf7")
    label(b, "monocyte-label", "Monocyte", 624, 277, 21, bold=True, center=True)
    label(b, "tam-label", "M2-like TAM", 849, 277, 21, color=TEAL, bold=True, center=True)
    icon(b, "recruited-monocyte", "monocyte", 566, 294, 116)
    icon(b, "polarized-macrophage", "m2-like-tam", 780, 287, 137)
    arrow(b, "context-to-recruitment", "M461 372C490 372 505 351 532 351H573", dash=True)
    arrow(b, "monocyte-to-tam", "M677 351H785")
    label(b, "differentiation-label", "Differentiation", 730, 329, 15, color=MUTED, center=True)
    arrow(b, "tam-to-arg1", "M849 412V429H908V442")
    for name, value, x, width in [
        ("il-10", "IL-10", 582, 79), ("tgf-beta", "TGF-β", 669, 81),
        ("arg1", "ARG1 activity", 840, 136),
    ]:
        box(b, f"{name}-pill", x, 450, width, 37, "#e5f3ed", stroke="#bfd9cd", radius=17)
        label(b, f"{name}-label", value, x + width / 2, 475, 17, color=TEAL, bold=True, center=True)
    label(b, "cytokines-label", "Secreted factors", 665, 512, 16, color=MUTED, center=True)
    label(b, "enzyme-label", "Enzymatic pathway", 908, 512, 16, color=MUTED, center=True)
    arrow(b, "tam-mediator-branch", "M849 429H665V445", head=True, width=1.8)
    arrow(b, "soluble-factors-to-t-cell", "M665 520Q689 535 777 532H839Q880 532 896 549", dash=True, width=1.8)
    arrow(b, "arg1-pathway-to-t-cell", "M908 521V548", dash=True, width=1.8)
    icon(b, "effector-t-cell", "cd8-t-cell", 570, 535, 113)
    icon(b, "exhausted-effector-t-cell", "exhausted-t-cell", 855, 536, 106)
    arrow(b, "t-cell-dysfunction-arrow", "M684 592H862", dash=True)
    label(b, "dysfunction-label", "May impair function", 770, 570, 16, color=MUTED, center=True)
    label(b, "effector-t-cell-label", "CD8⁺ T cell", 626, 669, 20, color=BLUE, bold=True, center=True)
    label(b, "exhausted-t-cell-label", "Exhausted CD8⁺ T cell", 908, 669, 19, color=BLUE, bold=True, center=True)
    arrow(b, "b-caption-rule", "M539 688H1024", head=False, color="#c9ded6", width=1.3)
    label(b, "b-caption", "TAM-mediated suppression can involve multiple pathways.", 539, 718, 17, color=MUTED)

    c = panel(root, "c", "PD-1 checkpoint blockade", "Comparison of signaling states",
              1066, 578, BLUE, "#f5f8fd")
    label(c, "engaged-state-title", "Checkpoint engaged", 1094, 269, 23, color=BLUE, bold=True)
    icon(c, "untreated-macrophage", "m2-like-tam", 1092, 310, 118)
    icon(c, "untreated-t-cell", "cd8-t-cell", 1320, 311, 116)
    icon(c, "bound-pd-l1", "pd-l1", 1194, 319, 100)
    icon(c, "bound-pd-1", "pd-1", 1242, 317, 104, flip=True)
    label(c, "pd-l1-interaction-label", "PD-L1", 1232, 312, 18, color="#865921", bold=True, center=True)
    label(c, "pd-1-interaction-label", "PD-1", 1311, 312, 18, color=BLUE, bold=True, center=True)
    arrow(c, "engaged-to-suppression", "M1428 369H1490")
    icon(c, "reduced-cytotoxicity-symbol", "cytotoxicity-suppressed", 1500, 335, 67)
    label(c, "reduced-cytotoxicity-line-1", "Reduced", 1534, 424, 20, color=CORAL, bold=True, center=True)
    label(c, "reduced-cytotoxicity-line-2", "cytotoxicity", 1534, 448, 19, color=CORAL, center=True)
    label(c, "untreated-macrophage-label", "M2-like TAM", 1151, 445, 17, color=TEAL, center=True)
    label(c, "untreated-t-cell-label", "CD8⁺ T cell", 1378, 445, 17, color=BLUE, center=True)

    arrow(c, "checkpoint-state-divider", "M1094 470H1616", dash=True, head=False, color=LINE, width=1.8)
    label(c, "blocked-state-title", "Checkpoint blocked", 1094, 508, 23, color=BLUE, bold=True)
    label(c, "anti-pd-1-label", "Anti-PD-1", 1291, 533, 18, color="#6c4879", bold=True, center=True)
    icon(c, "treated-macrophage", "m2-like-tam", 1092, 550, 118)
    icon(c, "treated-t-cell", "cd8-t-cell", 1320, 551, 116)
    icon(c, "unbound-pd-l1", "pd-l1", 1194, 565, 88)
    icon(c, "antibody-bound-pd-1", "pd-1", 1253, 563.5, 91, flip=True)
    icon(c, "therapeutic-antibody", "anti-pd-1", 1274, 542, 58, rotate=153)
    arrow(c, "blockade-cross", "M1271 605l10 10m0-10-10 10", head=False, color="#a84c54", width=2.8)
    arrow(c, "blockade-to-recovery", "M1428 609H1490")
    icon(c, "partial-recovery-symbol", "cytotoxicity-partial-recovery", 1500, 575, 67)
    label(c, "recovery-line-1", "Possible partial", 1534, 664, 18, color="#37674c", bold=True, center=True)
    label(c, "recovery-line-2", "recovery", 1534, 688, 19, color="#37674c", center=True)
    label(c, "treated-macrophage-label", "M2-like TAM", 1151, 684, 17, color=TEAL, center=True)
    label(c, "treated-t-cell-label", "CD8⁺ T cell", 1378, 684, 17, color=BLUE, center=True)
    label(c, "checkpoint-caption", "The antibody binds PD-1 on the CD8⁺ T cell.", 1094, 718, 17, color=MUTED)

    legend = layer(root, "legend", "Legend")
    box(legend, "legend-background", 36, 767, 1608, 148, "#f8fafb", stroke="#dbe3e5", radius=12)
    label(legend, "legend-title", "Legend", 61, 798, 20, bold=True)
    for row, entries in enumerate([
        [("tumor-cell", "Tumor cell"), ("monocyte", "Monocyte"), ("m2-like-tam", "M2-like TAM"),
         ("cd8-t-cell", "CD8⁺ T cell"), ("exhausted-t-cell", "Exhausted CD8⁺ T cell")],
        [("ccl2", "CCL2"), ("csf1", "CSF1"), ("pd-l1", "PD-L1"),
         ("pd-1", "PD-1"), ("anti-pd-1", "Anti-PD-1")],
    ]):
        for index, (slug, value) in enumerate(entries):
            x, y = 61 + index * 313, 806 + row * 48
            size = 40 if row == 0 or slug == "anti-pd-1" else 34
            icon(legend, f"key-icon-{slug}", slug, x, y + (40 - size) / 2, size)
            label(legend, f"key-label-{slug}", value, x + 49, y + 26, 18)

    label(header, "figure-scale-note", "Conceptual schematic · Cell sizes and molecular shapes are illustrative.",
          37, 941, 16, color=MUTED)
    ET.indent(root, space="  ")
    return ET.ElementTree(root)


if __name__ == "__main__":
    build().write(ROOT / "figure.svg", encoding="utf-8", xml_declaration=True)
