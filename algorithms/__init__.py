"""
XOR_dist Algorithms Package
"""

from .core import (
    xor_dist, popcount, v2, vp,
    trailing_ones, odd_part,
    sieve_of_eratosthenes, is_prime,
    twin_primes, prime_pairs_with_gap,
    verify_theorem_single, verify_theorem_batch,
    xor_dist_distribution, distribution_stats,
    mersenne_primes, high_xor_dist_twins,
    demonstrate_theorem
)

__all__ = [
    'xor_dist', 'popcount', 'v2', 'vp',
    'trailing_ones', 'odd_part',
    'sieve_of_eratosthenes', 'is_prime',
    'twin_primes', 'prime_pairs_with_gap',
    'verify_theorem_single', 'verify_theorem_batch',
    'xor_dist_distribution', 'distribution_stats',
    'mersenne_primes', 'high_xor_dist_twins',
    'demonstrate_theorem'
]
