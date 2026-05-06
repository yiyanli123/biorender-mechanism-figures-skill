# Biomedical Schematic Visual Language

## Style Target

Create original, publication-ready biomedical schematics with a clean vector-like look commonly expected in review articles, graphical abstracts, grants, and scientific posters. Use "BioRender-inspired" only as a shorthand for clarity, polish, soft biomedical shapes, and organized mechanism storytelling. Do not copy BioRender templates, proprietary icons, logos, watermarks, or exact compositions.

## Composition

- Use a clear reading direction: left-to-right for mechanisms, top-to-bottom for workflows, radial only for cycles or feedback loops.
- Give each biological compartment a stable zone: extracellular space, plasma membrane, cytoplasm, nucleus, tissue niche, vasculature, organ, or assay readout.
- Use 2-4 panels for review summaries. Avoid more than 6 major visual groups in one generated image.
- Make the main causal flow visually dominant. Secondary modulators should be smaller and lighter.
- Use arrows for activation or movement, blunt-ended bars for inhibition, dashed arrows for indirect or uncertain effects.

## Biomedical Iconography

- Cells: smooth membrane outlines, lightly textured cytoplasm, distinct nucleus when relevant.
- Proteins and cytokines: small labeled dots, dimers, receptors, or simplified ligand shapes.
- DNA/RNA: simple helix, transcript line, or gene locus block only when central to the story.
- Drugs: small molecule hexagon/ring, antibody Y-shape, nanoparticle sphere, or syringe only when needed.
- Organs/tissues: simplified silhouettes; avoid anatomical realism unless the user asks for it.
- Assays: plate wells, flow cytometry plot, sequencing reads, microscope, or bar chart as simplified icons.

## Color

- Prefer a restrained, multi-hue scientific palette: muted teal, blue, coral, gold, green, and neutral gray.
- Use color semantics consistently: activation/warm, inhibition/cool or gray, disease/stress/red-orange, therapy/blue-green.
- Keep the background white or very light neutral. Avoid dark gradients, decorative blobs, and heavy texture.
- Use contrast high enough for labels and arrows to remain legible after export.

## Labels and Text

- Keep labels short and exact. Use supplied gene/protein/drug capitalization.
- Limit generated-image labels to essential names. Put long explanations in a separate legend or caption.
- Ask for an unlabeled version when the user needs journal-grade editable text in Illustrator, PowerPoint, or BioRender later.
- Avoid tiny placeholder text, paragraph labels, fake axis text, and dense callouts.

## Publication-Quality Output

- Request "ultra-high-resolution", "print-ready", "sharp vector-like edges", "large readable labels", "generous whitespace", and "export-quality clarity" in every final-generation prompt.
- Prefer SVG or PDF when the generation/editing tool supports vector output. Vector output is best for journal figures, posters, slides, and downstream editing.
- If the image tool only returns raster output, request the highest resolution available and plan for 300-600 DPI at final print size.
- For publication submissions, avoid relying on AI-rendered small text. Generate either an unlabeled figure or a lightly labeled figure, then add final text in Illustrator, Inkscape, PowerPoint, Affinity Designer, or BioRender.
- For SVG/PDF-ready composition, use flat color regions, clean outlines, simple gradients only when necessary, consistent strokes, and separated objects that are easy to trace or redraw.
- If converting raster to vector, use vector tracing only for simple icon-like regions; manually rebuild arrows, labels, and key shapes when scientific accuracy matters.

## Prompt Details That Improve Results

- State the scientific narrative in numbered steps.
- Name the visual hierarchy: primary pathway, secondary pathway, context cells, readouts.
- Specify panel titles only when truly needed.
- Include "ultra-high-resolution, print-ready, crisp vector-like biomedical illustration, clean white background, sharp edges, consistent line weights, subtle shadows, large legible short labels".
- Include negative constraints: "no photorealism, no 3D glossy rendering, no copied commercial icons, no logos, no watermark, no excessive labels, no overlapping arrows".

## Iteration Checklist

1. Confirm biological directionality and compartment placement.
2. Confirm all required labels are present and spelled correctly.
3. Remove or regenerate any invented molecules, arrows, or text.
4. Reduce label count if text quality is poor.
5. Request wider spacing when arrows overlap.
6. Ask for a transparent or white background depending on downstream use.
7. Ask for SVG/PDF-ready composition or highest-resolution raster output before final export.
