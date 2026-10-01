# Manual validation of top-20 alerts

The model is unsupervised, so there are no ground-truth labels. Each of the 20
highest-scoring alerts was reviewed by hand in the dashboard drill-down and labelled:

- **Suspicious**: clear attacker-like behaviour (AccessDenied bursts, access-key creation, region sweeps, logging tampering)
- **Plausible**: unusual but could be legitimate
- **Noise**: normal activity flagged by mistake

| # | Identity | Hour (UTC) | Top feature | Label | Notes |
|---|----------|------------|-------------|-------|-------|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |
| 6 |  |  |  |  |  |
| 7 |  |  |  |  |  |
| 8 |  |  |  |  |  |
| 9 |  |  |  |  |  |
| 10 |  |  |  |  |  |
| 11 |  |  |  |  |  |
| 12 |  |  |  |  |  |
| 13 |  |  |  |  |  |
| 14 |  |  |  |  |  |
| 15 |  |  |  |  |  |
| 16 |  |  |  |  |  |
| 17 |  |  |  |  |  |
| 18 |  |  |  |  |  |
| 19 |  |  |  |  |  |
| 20 |  |  |  |  |  |

**Result:** X / 20 suspicious, Y / 20 plausible, Z / 20 noise.
