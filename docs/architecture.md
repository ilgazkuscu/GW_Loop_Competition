# Architecture

- `plot.ipynb` owns the narrative, colors, annotations, and final visualization.
- `gw_loop.analysis` owns deterministic donation normalization and group aggregation.
- `tests/` verifies category mapping, means, relative change, and zero-denominator behavior with synthetic visits.
- `data/` contains the competition workbook and provenance notes.

The module does not render charts, so the core comparison can be reviewed independently from notebook state.
