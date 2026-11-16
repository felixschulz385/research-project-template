---
type: rule
state: current
updated: 2026-11-16
area: modules
applies: opt-in: geospatial
summary: "Gridded data: one canonical grid, one path module per tile, explicit resampling per variable"
---

# Geospatial data

## Decision

- **One canonical grid** for the project (an equal-area grid such as EASE-Grid 2.0 for global
  work), stated in a design record, with tiles of a fixed size. Every source is prepared onto
  it; coarser grids are exact block aggregations whose blocks restart at each tile origin, and
  anything keyed to a coarse grid uses the project's own cell id, not a regular global grid.
- **Resampling is chosen per variable** (mean for continuous, mode or shares for classes, sum for
  counts) and recorded in the source's data page.
- **Tiles that cross the antimeridian** are clipped explicitly; test the edge tiles, since a bug
  there silently empties a few percent of the globe.
- **Conda binaries** (GDAL, PROJ) come from conda-forge through the lock file.

## Why

In the source project, a clipping bug at the antimeridian left edge tiles empty in several
sources for weeks; a per-variable resampling rule kept class variables from being averaged.

## How

Write the grid's design record first (`python scripts/docs.py new design grid`).

## Per-project choices

- The grid, its resolution and tile size.

## Checked by

Tests of the grid and of edge tiles.
