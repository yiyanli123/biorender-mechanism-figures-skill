# BioRender Mechanism Figures Skill

[English](./README.md) | [中文](./README.zh-CN.md)

An Agent Skill for creating BioRender-inspired, publication-quality biomedical mechanism figure prompts for GPT Image models and other image-generation workflows.

This project helps agents turn paper paragraphs, hypotheses, pathway descriptions, review topics, or grant ideas into clear scientific schematics: mechanism figures, graphical abstracts, review diagrams, pathway maps, and experimental workflows.

> Not affiliated with BioRender. This skill aims for an original, BioRender-inspired scientific visual language and explicitly avoids copying BioRender assets, templates, logos, or proprietary icons.

## Preview

Example output generated from the tumor immune microenvironment gallery prompt:

![Tumor immune microenvironment mechanism figure preview](./assets/tumor-immune-microenvironment-preview.png)

## Repository Name

Recommended GitHub repository name:

```text
biorender-mechanism-figures-skill
```

## What It Does

- Converts biomedical content into structured image-generation prompts
- Enforces mechanism-first figure planning: story, compartments, actors, arrows, labels
- Produces high-resolution, print-ready prompt language by default
- Encourages SVG/PDF-ready layouts for journal, poster, and slide workflows
- Includes reusable gallery examples for oncology, neuroscience, microbiome, pharmacology, single-cell methods, and immunology
- Works as a Codex skill and can be adapted for Claude Code or OpenCode

## Publication-Quality Output

The skill defaults to publication-ready clarity:

- Ultra-high-resolution, print-ready schematic prompts
- Sharp vector-like edges and consistent line weights
- Large readable labels and generous whitespace
- SVG/PDF-ready composition when the image tool supports vector output
- Highest-resolution PNG fallback for 300-600 DPI print workflows

For journal figures, the recommended workflow is to generate an unlabeled or lightly labeled figure, then add final text in Illustrator, Inkscape, PowerPoint, Affinity Designer, or BioRender. This avoids AI-rendered small-text artifacts and makes the final figure easier to revise.

## Repository Structure

```text
.
├── biorender-mechanism-figures/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/visual-language.md
│   └── scripts/build_prompt.py
├── gallery/
│   ├── README.md
│   └── examples/
└── README.md
```

## Use In Codex

Install as a personal Codex skill:

```bash
rsync -a ./biorender-mechanism-figures/ ~/.codex/skills/biorender-mechanism-figures/
```

Restart Codex, then invoke:

```text
Use $biorender-mechanism-figures to create a publication-ready mechanism figure prompt for ...
```

## Use In Claude Code

The core skill uses the standard `SKILL.md` folder pattern, so it can also be used in Claude Code.

Personal install:

```bash
rsync -a ./biorender-mechanism-figures/ ~/.claude/skills/biorender-mechanism-figures/
```

Project install:

```bash
mkdir -p .claude/skills
rsync -a ./biorender-mechanism-figures/ .claude/skills/biorender-mechanism-figures/
```

Restart Claude Code after installing or updating.

## Use In OpenCode

OpenCode supports Agent Skills defined by `SKILL.md`.

Global install:

```bash
mkdir -p ~/.config/opencode/skills
rsync -a ./biorender-mechanism-figures/ ~/.config/opencode/skills/biorender-mechanism-figures/
```

Project install:

```bash
mkdir -p .opencode/skills
rsync -a ./biorender-mechanism-figures/ .opencode/skills/biorender-mechanism-figures/
```

OpenCode can also read Claude-compatible skill locations such as `.claude/skills/` and `~/.claude/skills/`, so one shared install may be enough if you use both Claude Code and OpenCode.

## Example

This example creates a tumor immune microenvironment mechanism figure for an oncology review.

```text
Use $biorender-mechanism-figures to create a landscape 16:9 oncology review mechanism figure: hypoxia-driven tumor-associated macrophage polarization and T cell exhaustion. Show three left-to-right zones: hypoxic tumor core, immune remodeling, immunotherapy response.

Include tumor cells, HIF-1alpha, CCL2/CSF1, recruited monocytes, M2 TAMs, exhausted CD8+ T cells, PD-1/PD-L1, and anti-PD-1 therapy.

Style: original BioRender-inspired biomedical schematic, ultra-high-resolution, print-ready, clean white background, crisp vector-like cells, sharp edges, muted teal/coral/blue/gold/gray palette, clear arrows, large readable labels, generous whitespace, SVG/PDF-ready composition, no copied icons, no watermark.
```

More examples are available in the [gallery](./gallery/README.md).

## Prompt Builder

You can also generate a reusable prompt from the command line:

```bash
python biorender-mechanism-figures/scripts/build_prompt.py \
  --topic "Tumor-associated macrophage polarization in the hypoxic tumor microenvironment" \
  --figure-type mechanism \
  --audience "review article" \
  --canvas "landscape 16:9" \
  --output-target "SVG/PDF-ready publication figure, or 4K+ PNG suitable for 300-600 DPI print" \
  --elements "tumor cell,hypoxia,HIF-1alpha,M2 macrophage,T cell exhaustion,anti-PD-1 therapy" \
  --flow "Hypoxia stabilizes HIF-1alpha; tumor cells secrete CCL2 and CSF1; monocytes enter tumor; macrophages polarize toward M2; exhausted T cells reduce killing; anti-PD-1 partially restores cytotoxicity" \
  --labels "Hypoxia,HIF-1alpha,CCL2/CSF1,M2 TAM,Exhausted T cell,anti-PD-1"
```

## Portability Notes

- The core skill is portable because it is plain Markdown plus a `SKILL.md` frontmatter block.
- `scripts/build_prompt.py` is portable anywhere Python 3 is available.
- `agents/openai.yaml` is Codex-specific UI metadata; other platforms can ignore it.
- Image generation depends on the platform's available tools. If SVG/PDF export is not directly supported, generate the highest-resolution raster output and convert or rebuild the final figure in a vector editor.
