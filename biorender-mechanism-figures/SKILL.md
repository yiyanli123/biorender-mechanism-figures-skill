---
name: biorender-mechanism-figures
description: Create original BioRender-inspired mechanism figures, pathway diagrams, graphical abstracts, and review or methods schematics. Use for drawing biomedical figures from editable SVG icons, recoloring, redrawing or replacing individual icons and icon styles, or preparing an image prompt or raster draft on request.
---

# Biorender Mechanism Figures

## Overview

Turn biomedical concepts into original scientific schematics with clear reading order, generous spacing, and legible labels. For a request to make, redraw, or revise a figure, default to delivering an editable SVG assembled from individual native SVG icons. Use the prompt or raster workflow only when the user requests those outputs or explicitly selects a raster image generator.

## Icon-First Workflow

1. Plan the panels and inventory the distinct elements. Read [the visual guide](references/visual-language.md) for BioRender-inspired composition. For a reference figure, inspect the panels, repeated elements, labels, and directional links before drawing.
2. Inspect the bundled `assets/icons/` library. Copy suitable icons to an `icons/` subdirectory in the task's output folder. Draw missing icons and variants there as separate, transparent SVGs with named editable parts. Finish the required icon files before assembling the figure. For icon-only requests, deliver those SVG files without composing a figure.
3. Draw a figure layout and inline the icons. Use [the editable SVG guide](references/editable-figures.md) and bundled `scripts/assemble_svg.py` to generate a self-contained `figure.svg`. Keep each icon instance, arrow, compartment, legend entry, and text label editable on its own. Use a different filename or folder when revising a manually edited figure.
4. Verify and deliver. Render the final figure when a renderer is available. Inspect scientific directionality, text, alignment, and readability. Test that removing one repeated icon or label in a temporary copy leaves other instances intact. Deliver `figure.svg`, `layout.svg` when used for assembly, and the used standalone `icons/`. Include a PNG preview when available and export vector PDF when requested and supported.

## Revise an Icon or Its Style

Identify the target by its name, object ID, panel, or location. Apply a localized request to the indicated instance. Apply a global request to the matching instances and their associated legend icons. Follow [the revision workflow](references/editable-figures.md#revise-an-icon-or-its-style) to edit parts, draw a new style, or import a user-supplied SVG, while keeping manual figure edits. Deliver the revised standalone icon. Also return an updated figure when the user asks to apply the change to it.

## Prompt and Raster Workflow

Use this workflow for prompt-only or raster requests. Steps 1-3 also inform the figure plan for vector work.

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
   - Choose the largest suitable native raster size and quality through the tool's actual settings when available. Request sharp edges, readable labels, and generous spacing in the prompt.
   - Prefer unlabeled or lightly labeled raster generation when the final target is a journal figure, then add final text in Illustrator, Inkscape, PowerPoint, or BioRender to avoid image-model text artifacts.
   - Verify the delivered pixel dimensions against the journal's requirements at the final print size. Divide the available pixels by the final printed size in inches on each axis to calculate effective PPI. For example, 180 mm wide at 300 PPI requires at least 2,126 pixels in width.
   - If the user requests editability or a vector PDF, use the editable route above. A PDF or SVG wrapper preserves the resolution and editability limits of embedded raster artwork.

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
Output target: largest suitable native raster output, with enough pixels for the intended print size.
Style: crisp vector-like shapes, sharp edges, soft scientific color palette, subtle shadows, consistent line weight, rounded biological forms, clear arrows, generous whitespace, large readable labels, minimal decorative elements.
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
  --output-target "PNG draft with sharp edges and space for vector labels" \
  --elements "tumor cell,hypoxia,HIF-1alpha,M2 macrophage,T cell exhaustion,anti-PD-1 therapy" \
  --flow "Hypoxia stabilizes HIF-1alpha; tumor cells secrete CCL2 and CSF1; monocytes enter tumor; macrophages polarize toward M2; exhausted T cells reduce killing; anti-PD-1 partially restores cytotoxicity" \
  --labels "Hypoxia,HIF-1alpha,CCL2/CSF1,M2 TAM,Exhausted T cell,anti-PD-1"
```

The script prints a ready-to-use prompt. Edit the resulting prompt before generation if the user provided extra constraints.

## References

- Read `references/visual-language.md` for visual style, composition, label, output clarity, and iteration rules.
- Read `references/editable-figures.md` for the icon inventory, workspace layout, assembly helper, and editability checks. Resolve bundled paths relative to this `SKILL.md`.
- For implementation details of OpenAI image APIs or model names, check current official OpenAI documentation before claiming a specific latest model or parameter.
