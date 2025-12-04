"""
XOR_dist Verification Suite
===========================

Algoritmos de verificação formal e testes exaustivos para o teorema do xor_dist.

Autor: Thiago Fernandes Motta
Data: Dezembro 2025
"""

import time
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from core import (
    xor_dist, v2, popcount, trailing_ones,
    sieve_of_eratosthenes, twin_primes, prime_pairs_with_gap,
    verify_theorem_single, verify_theorem_batch,
    distribution_stats
)


@dataclass
class VerificationResult:
    """Resultado de uma verificação."""
    theorem: str
    total_cases: int
    verified_cases: int
    counterexamples: List[Dict]
    execution_time: float
    is_proven: bool
    
    def __str__(self):
        status = "✓ VERIFICADO" if self.is_proven else "✗ FALHOU"
        return (
            f"\n{'='*60}\n"
            f"Teorema: {self.theorem}\n"
            f"{'='*60}\n"
            f"Status: {status}\n"
            f"Casos testados: {self.total_cases:,}\n"
            f"Casos verificados: {self.verified_cases:,}\n"
            f"Taxa de sucesso: {100*self.verified_cases/self.total_cases:.6f}%\n"
            f"Contra-exemplos: {len(self.counterexamples)}\n"
            f"Tempo de execução: {self.execution_time:.2f}s\n"
            f"{'='*60}"
        )


# =============================================================================
# VERIFICAÇÃO DO TEOREMA PRINCIPAL
# =============================================================================

def verify_main_theorem(limit: int = 10**6, verbose: bool = True) -> VerificationResult:
    """
    Verifica o teorema principal: xor_dist(p, p+2) = v₂(p+1) para twins.
    
    Args:
        limit: Limite superior para busca de primos
        verbose: Mostrar progresso
        
    Returns:
        Resultado da verificação
    """
    start_time = time.time()
    
    if verbose:
        print(f"Gerando primos até {limit:,}...")
    primes = sieve_of_eratosthenes(limit)
    
    if verbose:
        print(f"Encontrando primos gêmeos...")
    twins = twin_primes(primes)
    
    if verbose:
        print(f"Verificando teorema para {len(twins):,} pares...")
    
    verified = 0
    counterexamples = []
    
    for i, (p, q) in enumerate(twins):
        success, details = verify_theorem_single(p)
        if success:
            verified += 1
        else:
            counterexamples.append(details)
        
        if verbose and (i + 1) % 10000 == 0:
            print(f"  Progresso: {i+1:,}/{len(twins):,}")
    
    elapsed = time.time() - start_time
    
    return VerificationResult(
        theorem="xor_dist(p, p+2) = v₂(p+1) para primos gêmeos",
        total_cases=len(twins),
        verified_cases=verified,
        counterexamples=counterexamples,
        execution_time=elapsed,
        is_proven=(verified == len(twins))
    )


# =============================================================================
# VERIFICAÇÃO DO COROLÁRIO (TODOS OS ÍMPARES)
# =============================================================================

def verify_corollary_all_odds(limit: int = 10**5, verbose: bool = True) -> VerificationResult:
    """
    Verifica o corolário: xor_dist(n, n+2) = v₂(n+1) para TODO n ímpar.
    
    Este é mais forte que o teorema (não requer primalidade).
    
    Args:
        limit: Limite superior
        verbose: Mostrar progresso
        
    Returns:
        Resultado da verificação
    """
    start_time = time.time()
    
    if verbose:
        print(f"Verificando para todos os ímpares até {limit:,}...")
    
    verified = 0
    counterexamples = []
    total = limit // 2
    
    for n in range(1, limit, 2):  # Todos os ímpares
        xd = xor_dist(n, n + 2)
        v2_val = v2(n + 1)
        
        if xd == v2_val:
            verified += 1
        else:
            counterexamples.append({
                'n': n,
                'xor_dist': xd,
                'v2': v2_val
            })
        
        if verbose and verified % 10000 == 0:
            print(f"  Progresso: {verified:,}/{total:,}")
    
    elapsed = time.time() - start_time
    
    return VerificationResult(
        theorem="xor_dist(n, n+2) = v₂(n+1) para todo n ímpar",
        total_cases=total,
        verified_cases=verified,
        counterexamples=counterexamples,
        execution_time=elapsed,
        is_proven=(verified == total)
    )


# =============================================================================
# VERIFICAÇÃO DA EQUIVALÊNCIA COM TRAILING ONES
# =============================================================================

def verify_trailing_ones_equivalence(limit: int = 10**5) -> VerificationResult:
    """
    Verifica que v₂(n+1) = trailing_ones(n) para todo n ímpar.
    
    Esta é uma propriedade fundamental usada na demonstração.
    """
    start_time = time.time()
    
    verified = 0
    counterexamples = []
    total = limit // 2
    
    for n in range(1, limit, 2):
        v2_val = v2(n + 1)
        to_val = trailing_ones(n)
        
        if v2_val == to_val:
            verified += 1
        else:
            counterexamples.append({
                'n': n,
                'v2(n+1)': v2_val,
                'trailing_ones(n)': to_val
            })
    
    elapsed = time.time() - start_time
    
    return VerificationResult(
        theorem="v₂(n+1) = trailing_ones(n) para todo n ímpar",
        total_cases=total,
        verified_cases=verified,
        counterexamples=counterexamples,
        execution_time=elapsed,
        is_proven=(verified == total)
    )


# =============================================================================
# VERIFICAÇÃO DA DISTRIBUIÇÃO GEOMÉTRICA
# =============================================================================

def verify_geometric_distribution(twins: List[Tuple[int, int]], 
                                   alpha: float = 0.01) -> Dict:
    """
    Testa se a distribuição de xor_dist segue Geom(1/2).
    
    Usa teste qui-quadrado para comparar com distribuição teórica.
    
    Args:
        twins: Lista de pares de primos gêmeos
        alpha: Nível de significância
        
    Returns:
        Resultado do teste estatístico
    """
    n = len(twins)
    
    # Distribuição observada
    observed = {}
    for p, q in twins:
        d = xor_dist(p, q)
        observed[d] = observed.get(d, 0) + 1
    
    # Distribuição teórica: P(k) = 2^{-k}
    max_k = max(observed.keys())
    expected = {k: n * (2**(-k)) for k in range(1, max_k + 1)}
    
    # Qui-quadrado
    chi2 = 0
    details = []
    for k in range(1, max_k + 1):
        obs = observed.get(k, 0)
        exp = expected.get(k, 0)
        if exp > 5:  # Condição padrão para qui-quadrado
            contribution = (obs - exp)**2 / exp
            chi2 += contribution
            details.append({
                'k': k,
                'observed': obs,
                'expected': exp,
                'obs_freq': obs/n,
                'exp_freq': exp/n,
                'chi2_contrib': contribution
            })
    
    # Graus de liberdade
    df = len([d for d in details if d['expected'] > 5]) - 1
    
    # Valor crítico aproximado para α = 0.01
    # Para grandes df, χ² ~ N(df, 2*df)
    critical_value = df + 2.33 * (2*df)**0.5  # Aproximação
    
    return {
        'chi_squared': chi2,
        'degrees_of_freedom': df,
        'critical_value': critical_value,
        'is_geometric': chi2 < critical_value,
        'details': details,
        'n_samples': n
    }


# =============================================================================
# VERIFICAÇÃO POR GAPS DIFERENTES
# =============================================================================

def verify_by_gap(limit: int = 10**6, gaps: List[int] = None) -> Dict[int, Dict]:
    """
    Analisa o comportamento do xor_dist para diferentes gaps.
    
    Args:
        limit: Limite para geração de primos
        gaps: Lista de gaps a analisar (default: [2, 4, 6, 8, 10, 12, 18, 30])
        
    Returns:
        Dicionário com análise por gap
    """
    if gaps is None:
        gaps = [2, 4, 6, 8, 10, 12, 18, 30]
    
    print(f"Gerando primos até {limit:,}...")
    primes = sieve_of_eratosthenes(limit)
    
    results = {}
    
    for gap in gaps:
        print(f"\nAnalisando gap = {gap}...")
        pairs = prime_pairs_with_gap(primes, gap)
        
        if not pairs:
            results[gap] = {'count': 0, 'error': 'Nenhum par encontrado'}
            continue
        
        stats = distribution_stats(pairs)
        
        # Verifica se xor_dist mínimo corresponde a alguma propriedade do gap
        xor_min = stats['min']
        gap_popcount = popcount(gap)
        gap_v2 = v2(gap)
        
        results[gap] = {
            'count': len(pairs),
            'mean': stats['mean'],
            'std': stats['std'],
            'entropy': stats['entropy'],
            'xor_min': xor_min,
            'xor_max': stats['max'],
            'gap_popcount': gap_popcount,
            'gap_v2': gap_v2,
            'distribution': stats['distribution']
        }
    
    return results


# =============================================================================
# GERAÇÃO DE CASOS DE TESTE ESPECIAIS
# =============================================================================

def find_extreme_cases(limit: int = 10**7) -> Dict:
    """
    Encontra casos extremos para análise.
    
    Returns:
        Dicionário com casos interessantes
    """
    print(f"Gerando primos até {limit:,}...")
    primes = sieve_of_eratosthenes(limit)
    twins = twin_primes(primes)
    
    # Maior xor_dist
    max_xor = 0
    max_xor_pair = None
    
    # Distribuição por v2(p+1)
    v2_dist = {}
    
    for p, q in twins:
        d = xor_dist(p, q)
        v2_val = v2(p + 1)
        
        if d > max_xor:
            max_xor = d
            max_xor_pair = (p, q, d)
        
        v2_dist[v2_val] = v2_dist.get(v2_val, 0) + 1
    
    # Primos com v2(p+1) >= 5 (alto)
    high_v2_twins = [(p, q, v2(p+1)) for p, q in twins if v2(p+1) >= 5]
    
    return {
        'max_xor_dist_pair': max_xor_pair,
        'v2_distribution': dict(sorted(v2_dist.items())),
        'high_v2_twins': sorted(high_v2_twins, key=lambda x: -x[2])[:20],
        'total_twins': len(twins)
    }


# =============================================================================
# RELATÓRIO COMPLETO
# =============================================================================

def generate_full_report(limit: int = 10**6) -> str:
    """
    Gera um relatório completo de verificação.
    """
    lines = [
        "=" * 70,
        "RELATÓRIO DE VERIFICAÇÃO DO TEOREMA XOR_DIST",
        "=" * 70,
        f"Limite de verificação: {limit:,}",
        f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ]
    
    # Teorema principal
    lines.append("\n" + "-" * 70)
    lines.append("1. TEOREMA PRINCIPAL (Primos Gêmeos)")
    lines.append("-" * 70)
    result = verify_main_theorem(limit, verbose=False)
    lines.append(str(result))
    
    # Corolário (todos os ímpares)
    lines.append("\n" + "-" * 70)
    lines.append("2. COROLÁRIO (Todos os Ímpares)")
    lines.append("-" * 70)
    result = verify_corollary_all_odds(min(limit, 10**5), verbose=False)
    lines.append(str(result))
    
    # Equivalência trailing ones
    lines.append("\n" + "-" * 70)
    lines.append("3. EQUIVALÊNCIA v₂(n+1) = trailing_ones(n)")
    lines.append("-" * 70)
    result = verify_trailing_ones_equivalence(min(limit, 10**5))
    lines.append(str(result))
    
    lines.append("\n" + "=" * 70)
    lines.append("FIM DO RELATÓRIO")
    lines.append("=" * 70)
    
    return '\n'.join(lines)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10**6
    
    print(generate_full_report(limit))
