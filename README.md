# XOR Distance Theorem for Twin Primes

A formal proof and computational verification of the exact identity relating Hamming distance to 2-adic valuation.

## Main Theorem

For any odd integer `n`:

```
xor_dist(n, n+2) = v₂(n+1)
```

Where:
- `xor_dist(a,b) = popcount(a ⊕ b)` — Hamming distance (number of differing bits)
- `v₂(n)` — 2-adic valuation (largest k such that 2^k divides n)

The identity holds universally for all odd integers. The restriction to twin primes highlights a case of number-theoretic interest.

## Verification Results

| Limit | Twin Pairs | Success Rate |
|-------|------------|--------------|
| 10⁵   | 1,224      | 100.0000%    |
| 10⁶   | 8,169      | 100.0000%    |
| 10⁷   | 58,980     | 100.0000%    |

## Project Structure

```
├── paper/                          # Publication
│   ├── xor_dist_theorem_motta_2025.tex
│   └── xor_dist_theorem_motta_2025.pdf
├── proofs/                         # Formal proofs (Markdown)
├── algorithms/                     # Python implementation
│   ├── core.py                    # Core functions
│   └── verification.py            # Verification suite
├── experiments/                    # Scripts
│   └── run_verification.py
└── data/                          # Generated data
```

## Quick Start

```bash
# Run verification
cd experiments
python run_verification.py 10000000
```

```python
from algorithms.core import xor_dist, v2

# Example: twin primes (239, 241)
xor_dist(239, 241)  # → 4
v2(240)             # → 4
```

## Citation

If you use this work, please cite:

> Silva, T.F.M.M. (2025). *The XOR Distance Theorem for Twin Primes: A Binary Topological Characterization of Prime Gaps*.

## License

MIT

## Author

**Thiago Fernandes Motta Massensini Silva**  
[![ORCID](https://img.shields.io/badge/ORCID-0009--0002--3415--9805-green)](https://orcid.org/0009-0002-3415-9805)
