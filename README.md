# GW Loop Reuse Analysis

A compact data-visualization case study prepared for the GW Loop campus reuse competition. The analysis compares the average number of clothing items taken per visit for visitors who did and did not bring donations.

## Repository map

```text
plot.ipynb                  Original analysis and final dumbbell chart
src/gw_loop/analysis.py     Tested donation normalization and aggregation
tests/                      Synthetic-data checks
data/README.md              Source, schema, and privacy notes
FinalPlot2.png              Submitted visualization output
```

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
jupyter notebook plot.ipynb
```

The notebook expects `data/loop-data-ldw-2026.xlsx` and records 877 visits from January through October 2025. The reusable module makes the donor mapping and group aggregation independently testable.

## Interpretation limits

- The chart reports an observational association, not the causal effect of donating.
- Group means can be influenced by visitor composition and repeated visits.
- Relative change is undefined when the non-donor mean is zero.
- Visit-level timestamps should not be published beyond the competition context without confirming the source's sharing terms.
