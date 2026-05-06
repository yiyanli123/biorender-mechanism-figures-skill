---
name: biorender-mechanism-figures
description: Create polished biomedical mechanism figures, graphical abstracts, review schematics, pathway diagrams, cell/tissue process illustrations, and publication-quality scientific visuals using GPT Image models or other image-generation tools. Use when the user asks for BioRender-like, BioRender-inspired, high-resolution, print-ready, SVG/PDF-ready, mechanism, review, graphical abstract, pathway, molecular/cellular, immunology, oncology, neuroscience, microbiome, pharmacology, or biology schematic images; when converting a paper paragraph, hypothesis, pathway, or bullet list into a figure prompt; or when refining generated scientific figures for clarity, labeling, and journal-ready composition.
---

# Biorender Mechanism Figures

## Overview

Use this skill to turn biomedical concepts into publication-ready schematic prompts and iteration plans for GPT Image models. Aim for clean vector-like scientific illustration, not a direct copy of BioRender assets, templates, icons, or branding. Default to print-ready clarity: sharp edges, generous spacing, readable labels, and export paths that can produce SVG/PDF when possible.

## Workflow

1. Extract the scientific story.
   - Identify the central biological question, system, compartments, actors, causal sequence, and intended audience.
   - Preserve exact gene, protein, drug, disease, and pathway names supplied by the user.
   - Ask for missing essentials only when the mechanism cannot be inferred safely.

2. Choose the figure type.
   - Mechanism figure: left-to-right or top-to-bottom causal flow with arrows.
   - Review summary: 2-4 panels comparing pathways, cell states, disease stages, or therapeutic strategies.
   - Graphical abstract: one dominant visual narrative with minimal labels.
   - Pathway map: organized nodes and edges, grouped by compartment.
   - Experimental workflow: samples, assays, perturbations, readouts, and analysis outputs.

3. Draft the layout before image generation.
   - Specify canvas orientation: `landscape 16:9` for review figures, `square` for graphical abstracts, `portrait` for covers or vertical workflows.
   - Define panel count, reading order, and the exact visual hierarchy.
   - Keep labels short. Prefer 1-4 word labels and reserve sentence-length text for legends outside the image.

4. Generate the image prompt.
   - Use `scripts/build_prompt.py` when the request has enough structured details or when a repeatable prompt is useful.
   - Otherwise write a concise prompt directly, using the visual rules in `references/visual-language.md`.
   - Include a negative prompt section for clutter, photorealism, decorative backgrounds, illegible labels, fake text, and brand mimicry.

5. Use the right image-generation path.
   - For one-shot figure creation, use the Image API or the available image generation tool with the latest supported GPT Image model.
   - For iterative figure refinement, use a conversational or edit-capable flow and keep prior image context.
   - If the user says `image2`, interpret it as the current GPT Image generation model family and check official model availability before hard-coding a model name.

6. Set publication-quality output requirements.
   - Add `ultra-high-resolution`, `print-ready`, `sharp vector-like edges`, `large readable labels`, `generous whitespace`, and `export-quality clarity` to the prompt by default.
   - Prefer unlabeled or lightly labeled raster generation when the final target is a journal figure, then add final text in Illustrator, Inkscape, PowerPoint, or BioRender to avoid image-model text artifacts.
   - If the tool supports vector output, request SVG first. If not, generate the highest-resolution PNG available, then trace/rebuild simple shapes as SVG or place the high-resolution PNG into a PDF.
   - For journal or grant submission, target either editable vector output (`.svg`, `.pdf`) or raster output at 300-600 DPI at final print size.

7. Review and iterate.
   - Check scientific accuracy first: compartments, directionality, molecule names, and cell types.
   - Check visual quality second: balanced spacing, consistent icon scale, legible labels, no overlapping arrows, no crowded legends.
   - For text errors in generated images, prefer regeneration with fewer labels or create an unlabeled figure plus a separate editable annotation layer.

## Prompt Pattern

Use this compact structure:

```text
Create a publication-ready biomedical schematic, BioRender-inspired but original.
Topic: <mechanism or review subject>.
Audience: <journal/review/grant/lab meeting>.
Canvas: <landscape/square/portrait>, clean white or very light background.
Layout: <panel count and reading order>.
Main visual elements: <cells, organs, molecules, pathways, drugs, assays>.
Mechanism flow: <numbered causal sequence>.
Labels to include exactly: <short labels>.
Output target: publication-quality figure; prefer SVG/PDF-ready composition, or ultra-high-resolution PNG suitable for 300-600 DPI print.
Style: ultra-high-resolution, print-ready, crisp vector-like shapes, sharp edges, soft scientific color palette, subtle shadows, consistent line weight, rounded biological forms, clear arrows, generous whitespace, large readable labels, minimal decorative elements.
Avoid: photorealistic rendering, 3D glossy plastic, brand logos, copied BioRender icons, excessive text, fake tiny labels, crowded arrows, decorative gradients, dark backgrounds.
```

## Script

Use the prompt builder for structured requests:

```bash
python scripts/build_prompt.py \
  --topic "Tumor-associated macrophage polarization in the hypoxic tumor microenvironment" \
  --figure-type mechanism \
  --audience "review article" \
  --canvas "landscape 16:9" \
  --output-target "SVG/PDF-ready publication figure, or 4K+ PNG suitable for 300-600 DPI print" \
  --elements "tumor cell,hypoxia,HIF-1alpha,M2 macrophage,T cell exhaustion,anti-PD-1 therapy" \
  --flow "Hypoxia stabilizes HIF-1alpha; tumor cells secrete CCL2 and CSF1; monocytes enter tumor; macrophages polarize toward M2; exhausted T cells reduce killing; anti-PD-1 partially restores cytotoxicity" \
  --labels "Hypoxia,HIF-1alpha,CCL2/CSF1,M2 TAM,Exhausted T cell,anti-PD-1"
```

The script prints a ready-to-use prompt. Edit the resulting prompt before generation if the user provided extra constraints.

## References

- Read `references/visual-language.md` for visual style, composition, label, output clarity, and iteration rules.
- For implementation details of OpenAI image APIs or model names, check current official OpenAI documentation before claiming a specific latest model or parameter.
