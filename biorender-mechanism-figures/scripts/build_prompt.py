#!/usr/bin/env python3
"""Build a GPT Image prompt for biomedical mechanism figures."""

from __future__ import annotations

import argparse
import textwrap


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- None specified"


def build_prompt(args: argparse.Namespace) -> str:
    elements = split_csv(args.elements)
    labels = split_csv(args.labels)
    avoid = split_csv(args.avoid)

    flow_steps = [
        step.strip(" .")
        for step in args.flow.replace("\n", ";").split(";")
        if step.strip()
    ]
    numbered_flow = "\n".join(
        f"{index}. {step}." for index, step in enumerate(flow_steps, start=1)
    )

    negative_defaults = [
        "photorealistic rendering",
        "3D glossy plastic style",
        "copied BioRender icons or templates",
        "logos, watermarks, or branded UI elements",
        "excessive text or fake tiny labels",
        "overlapping arrows or crowded panels",
        "decorative gradients or dark background",
    ]
    avoid_items = avoid or negative_defaults

    prompt = f"""
Create a publication-ready biomedical schematic, BioRender-inspired but fully original.

Topic: {args.topic}
Figure type: {args.figure_type}
Audience/context: {args.audience}
Canvas: {args.canvas}
Output target: {args.output_target}

Layout:
{args.layout}

Main visual elements:
{bullet_list(elements)}

Mechanism flow:
{numbered_flow or "1. Show the supplied biological process as a clear causal sequence."}

Labels to include exactly:
{bullet_list(labels)}

Visual style:
Ultra-high-resolution, print-ready, crisp vector-like biomedical illustration,
clean white or very light neutral background, sharp edges, consistent line weights,
smooth cellular and molecular shapes, subtle shadows, restrained multi-hue scientific palette,
clear activation arrows and inhibition bars, generous whitespace, balanced spacing,
large readable labels, SVG/PDF-ready composition, and journal-review polish.

Avoid:
{bullet_list(avoid_items)}
"""
    return textwrap.dedent(prompt).strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a prompt for GPT Image biomedical mechanism figures."
    )
    parser.add_argument("--topic", required=True)
    parser.add_argument("--figure-type", default="mechanism figure")
    parser.add_argument("--audience", default="scientific review article")
    parser.add_argument("--canvas", default="landscape 16:9")
    parser.add_argument(
        "--output-target",
        default=(
            "SVG/PDF-ready publication figure, or the highest-resolution PNG "
            "available suitable for 300-600 DPI print at final size"
        ),
    )
    parser.add_argument(
        "--layout",
        default=(
            "One clean left-to-right mechanism with 2-3 visual zones and a dominant "
            "causal path."
        ),
    )
    parser.add_argument("--elements", default="")
    parser.add_argument("--flow", default="")
    parser.add_argument("--labels", default="")
    parser.add_argument("--avoid", default="")
    args = parser.parse_args()
    print(build_prompt(args))


if __name__ == "__main__":
    main()
