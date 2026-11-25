# Editable Biomedical Figures

## Inventory Before Assembly

Plan the scientific story, then list the distinct visual assets it needs. Match each entry to an existing icon, a variant, or a new drawing. Use one standalone file for multiple instances of the same icon. For a two-state comparison, keep the underlying silhouette consistent and vary only what communicates the state. Use labels for distinctions the morphology cannot convey.

- Look in `assets/icons/cells/`, `assets/icons/equipment/`, and `assets/icons/tumor-immune/` within the installed skill. The last directory includes tumor cells, monocytes, CD8+ T cells and macrophages, vessels, DNA, signals and checkpoint components.
- Copy the used icons and write new icons into the writable figure project's `icons/` directory. Use lower-case filenames such as `bile-duct.svg`. Each asset should have a `viewBox="0 0 128 128"`, a `<title>`, a transparent canvas, and native SVG shapes organized in meaningful groups. Keep molecule and cell-type labels in the figure layout.
- Draw figure-specific connections, compartment geometry, titles, labels, and legend swatches in the layout as native paths, shapes, or text. Distinguish each repeated instance with a unique ID. Follow [the visual guide](visual-language.md) and use the user's language for labels unless a reference or other instruction specifies it.

## Assemble the Figure

Create `layout.svg` next to `icons/` in the figure's output folder. Draw the composition at its intended aspect ratio, with editable `<text>` elements and named groups for panels. Place an empty group with `data-icon` for each icon instance. The attribute names the file in `icons/` without `.svg`. Position and scale the group for a 128-unit icon.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 200">
  <title>Illustrative icon placement</title>
  <g id="panel-a">
    <g id="t-cell-left" data-icon="t-cell" transform="translate(42 22) scale(0.85)"/>
    <g id="t-cell-right" data-icon="t-cell" transform="translate(280 22) scale(0.85)"/>
    <path id="connector" d="M172 67H257" fill="none" stroke="#526871" stroke-width="3"/>
    <text id="left-label" x="96" y="145" text-anchor="middle">T cell</text>
    <text id="right-label" x="335" y="145" text-anchor="middle">T cell</text>
  </g>
</svg>
```

From the output folder, run the bundled helper by its installed path:

```bash
python3 /path/to/biorender-mechanism-figures/scripts/assemble_svg.py layout.svg --output figure.svg
```

The helper uses the Python 3.9+ standard library. It inserts a separate copy of every icon's vector geometry, prefixes internal IDs and local fragment references, and checks for duplicate IDs, missing references and unsupported elements. Keep styles on SVG elements or in inline `style` attributes. Use local `url(#id)` references for gradient fills, clipping and arrowheads. The assembler expects direct native SVG elements. Expand clones and convert foreign or raster components into equivalent native vector shapes before assembly. If Python is unavailable, assemble the same native groups directly in an SVG editor or in markup.

## Validate the Deliverables

- Confirm that `figure.svg` can be opened or rendered independently of `icons/`, and that the axis, arrow or annotation labels remain SVG text. Check the figure at the intended display or print width.
- In a temporary copy, remove a repeated icon instance or its label to verify independent editing. Check that other instances remain in place. In a vector editor, enter the group or ungroup it to edit the icon's internal paths.
- Deliver the self-contained figure and the icon files used. Keep `layout.svg` when delivering a reproducible assembly; manual changes belong in an edited copy of `figure.svg`. Supply a PNG preview when available. For vector PDF export, use a vector-capable editor and inspect the export for unintended rasterization.
