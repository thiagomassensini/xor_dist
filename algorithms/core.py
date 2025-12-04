"""
XOR_dist Core Algorithms
========================

Implementações fundamentais para a teoria do xor_dist.

Autor: Thiago Fernandes Motta
Data: Dezembro 2025
"""

from typing import Iterator, Tuple, List, Dict
from functools import lru_cache
import math


# =============================================================================
# FUNÇÕES FUNDAMENTAIS
# =============================================================================

def xor_dist(a: int, b: int) -> int:
    """
    Calcula a distância de Hamming (xor_dist) entre dois inteiros.
    
    xor_dist(a, b) = popcount(a ⊕ b)
    
    Args:
        a, b: Inteiros não-negativos
        
    Returns:
        Número de bits diferentes entre a e b
        
    Example:
        >>> xor_dist(5, 7)  # 101 vs 111
        1
        >>> xor_dist(239, 241)  # 11101111 vs 11110001
        4
    """
    return bin(a ^ b).count('1')


def popcount(n: int) -> int:
    """
    Conta o número de bits 1 na representação binária de n.
    
    Args:
        n: Inteiro não-negativo
        
    Returns:
        Número de bits 1 (peso de Hamming)
        
    Example:
        >>> popcount(7)   # 111
        3
        >>> popcount(8)   # 1000
        1
    """
    return bin(n).count('1')


def v2(n: int) -> int:
    """
    Calcula a valorização 2-ádica de n.
    
    v₂(n) = max{k ≥ 0 : 2^k | n}
    
    Equivalente ao número de zeros à direita em binário.
    
    Args:
        n: Inteiro positivo
        
    Returns:
        Valorização 2-ádica
        
    Example:
        >>> v2(12)   # 1100 -> 2 zeros à direita
        2
        >>> v2(8)    # 1000 -> 3 zeros à direita
        3
        >>> v2(7)    # 111 -> 0 zeros à direita
        0
    """
    if n == 0:
        return float('inf')
    k = 0
    while n % 2 == 0:
        k += 1
        n //= 2
    return k


def vp(n: int, p: int) -> int:
    """
    Calcula a valorização p-ádica de n para primo p.
    
    v_p(n) = max{k ≥ 0 : p^k | n}
    
    Args:
        n: Inteiro positivo
        p: Primo
        
    Returns:
        Valorização p-ádica
    """
    if n == 0:
        return float('inf')
    k = 0
    while n % p == 0:
        k += 1
        n //= p
    return k


def trailing_ones(n: int) -> int:
    """
    Conta o número de bits 1 consecutivos no final de n (em binário).
    
    Para n ímpar, este é exatamente v₂(n+1).
    
    Args:
        n: Inteiro positivo
        
    Returns:
        Número de trailing ones
        
    Example:
        >>> trailing_ones(7)   # 111 -> 3 uns
        3
        >>> trailing_ones(11)  # 1011 -> 2 uns
        2
        >>> trailing_ones(5)   # 101 -> 1 um
        1
    """
    if n == 0:
        return 0
    count = 0
    while n & 1:
        count += 1
        n >>= 1
    return count


def odd_part(n: int) -> int:
    """
    Retorna a parte ímpar de n: K₂(n) = n / 2^{v₂(n)}.
    
    Args:
        n: Inteiro positivo
        
    Returns:
        Parte ímpar de n
        
    Example:
        >>> odd_part(12)  # 12 = 4 * 3
        3
        >>> odd_part(8)   # 8 = 8 * 1
        1
    """
    while n % 2 == 0:
        n //= 2
    return n


# =============================================================================
# GERAÇÃO DE PRIMOS
# =============================================================================

def sieve_of_eratosthenes(limit: int) -> List[int]:
    """
    Crivo de Eratóstenes para gerar primos até limit.
    
    Args:
        limit: Limite superior (inclusivo)
        
    Returns:
        Lista de primos até limit
    """
    if limit < 2:
        return []
    
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    
    return [i for i, prime in enumerate(is_prime) if prime]


def is_prime(n: int) -> bool:
    """
    Teste de primalidade (determinístico para n pequeno).
    
    Args:
        n: Inteiro a testar
        
    Returns:
        True se n é primo
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    if n < 9:
        return True
    if n % 3 == 0:
        return False
    
    # Teste até √n
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def prime_pairs_with_gap(primes: List[int], gap: int) -> List[Tuple[int, int]]:
    """
    Encontra todos os pares de primos consecutivos com gap específico.
    
    Args:
        primes: Lista de primos
        gap: Diferença desejada
        
    Returns:
        Lista de tuplas (p, p+gap) onde ambos são primos consecutivos
    """
    prime_set = set(primes)
    pairs = []
    
    for i in range(len(primes) - 1):
        if primes[i+1] - primes[i] == gap:
            pairs.append((primes[i], primes[i+1]))
    
    return pairs


def twin_primes(primes: List[int]) -> List[Tuple[int, int]]:
    """
    Encontra todos os primos gêmeos (gap = 2) na lista.
    
    Args:
        primes: Lista de primos
        
    Returns:
        Lista de tuplas (p, p+2) de primos gêmeos
    """
    prime_set = set(primes)
    return [(p, p+2) for p in primes if p + 2 in prime_set]


# =============================================================================
# VERIFICAÇÃO DO TEOREMA
# =============================================================================

def verify_theorem_single(p: int) -> Tuple[bool, Dict]:
    """
    Verifica o teorema xor_dist(p, p+2) = v₂(p+1) para um primo p.
    
    Args:
        p: Primo ímpar
        
    Returns:
        (sucesso, detalhes)
    """
    xd = xor_dist(p, p + 2)
    v2_val = v2(p + 1)
    
    details = {
        'p': p,
        'p_binary': bin(p),
        'p_plus_2': p + 2,
        'p_plus_2_binary': bin(p + 2),
        'xor': p ^ (p + 2),
        'xor_binary': bin(p ^ (p + 2)),
        'xor_dist': xd,
        'v2_p_plus_1': v2_val,
        'p_plus_1': p + 1,
        'trailing_ones_p': trailing_ones(p),
    }
    
    return xd == v2_val, details


def verify_theorem_batch(pairs: List[Tuple[int, int]], verbose: bool = False) -> Dict:
    """
    Verifica o teorema para uma lista de pares de primos.
    
    Args:
        pairs: Lista de pares (p, p+2)
        verbose: Se True, mostra progresso
        
    Returns:
        Dicionário com estatísticas
    """
    total = len(pairs)
    matches = 0
    failures = []
    
    for i, (p, q) in enumerate(pairs):
        success, details = verify_theorem_single(p)
        if success:
            matches += 1
        else:
            failures.append(details)
        
        if verbose and (i + 1) % 10000 == 0:
            print(f"Verificado: {i+1}/{total} ({100*(i+1)/total:.1f}%)")
    
    return {
        'total': total,
        'matches': matches,
        'failures': failures,
        'success_rate': matches / total if total > 0 else 0,
        'all_verified': matches == total
    }


# =============================================================================
# ANÁLISE DE DISTRIBUIÇÃO
# =============================================================================

def xor_dist_distribution(pairs: List[Tuple[int, int]]) -> Dict[int, int]:
    """
    Calcula a distribuição de xor_dist para uma lista de pares.
    
    Args:
        pairs: Lista de pares (p, q)
        
    Returns:
        Dicionário {xor_dist: contagem}
    """
    dist = {}
    for p, q in pairs:
        d = xor_dist(p, q)
        dist[d] = dist.get(d, 0) + 1
    return dict(sorted(dist.items()))


def distribution_stats(pairs: List[Tuple[int, int]]) -> Dict:
    """
    Calcula estatísticas da distribuição de xor_dist.
    
    Args:
        pairs: Lista de pares
        
    Returns:
        Estatísticas (média, desvio, entropia, etc.)
    """
    if not pairs:
        return {}
    
    distances = [xor_dist(p, q) for p, q in pairs]
    n = len(distances)
    
    # Média
    mean = sum(distances) / n
    
    # Variância e desvio padrão
    variance = sum((d - mean)**2 for d in distances) / n
    std = math.sqrt(variance)
    
    # Distribuição
    dist = {}
    for d in distances:
        dist[d] = dist.get(d, 0) + 1
    
    # Entropia de Shannon
    entropy = 0
    for count in dist.values():
        p = count / n
        if p > 0:
            entropy -= p * math.log2(p)
    
    return {
        'count': n,
        'mean': mean,
        'std': std,
        'variance': variance,
        'min': min(distances),
        'max': max(distances),
        'entropy': entropy,
        'distribution': dict(sorted(dist.items()))
    }


# =============================================================================
# CASOS ESPECIAIS
# =============================================================================

def mersenne_primes(max_exp: int = 20) -> List[Tuple[int, int, int]]:
    """
    Gera primos de Mersenne conhecidos até expoente max_exp.
    
    Returns:
        Lista de (expoente, primo, v₂(primo+1))
    """
    # Expoentes conhecidos para primos de Mersenne
    known_exponents = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607]
    
    result = []
    for n in known_exponents:
        if n <= max_exp:
            p = 2**n - 1
            result.append((n, p, v2(p + 1)))
    
    return result


def high_xor_dist_twins(primes: List[int], threshold: int = 4) -> List[Tuple[int, int, int]]:
    """
    Encontra primos gêmeos com xor_dist alto.
    
    Args:
        primes: Lista de primos
        threshold: Mínimo xor_dist
        
    Returns:
        Lista de (p, p+2, xor_dist)
    """
    twins = twin_primes(primes)
    result = []
    
    for p, q in twins:
        d = xor_dist(p, q)
        if d >= threshold:
            result.append((p, q, d))
    
    return sorted(result, key=lambda x: -x[2])


# =============================================================================
# DEMONSTRAÇÃO VISUAL
# =============================================================================

def demonstrate_theorem(p: int) -> str:
    """
    Gera uma demonstração visual do teorema para um primo específico.
    
    Args:
        p: Primo ímpar
        
    Returns:
        String formatada mostrando a demonstração
    """
    q = p + 2
    xor = p ^ q
    
    # Determina o número de bits necessário
    bits = max(p.bit_length(), q.bit_length(), xor.bit_length())
    
    p_bin = format(p, f'0{bits}b')
    q_bin = format(q, f'0{bits}b')
    xor_bin = format(xor, f'0{bits}b')
    
    lines = [
        f"Demonstração para p = {p}:",
        f"",
        f"  p     = {p_bin}  ({p})",
        f"  p+2   = {q_bin}  ({q})",
        f"  ─" + "─" * bits + "──────",
        f"  XOR   = {xor_bin}  ({xor})",
        f"",
        f"  popcount(XOR) = {popcount(xor)}",
        f"  v₂(p+1) = v₂({p+1}) = {v2(p+1)}",
        f"",
        f"  Trailing ones em p: {trailing_ones(p)}",
        f"",
        f"  ✓ xor_dist(p, p+2) = v₂(p+1) = {v2(p+1)}"
    ]
    
    return '\n'.join(lines)


# =============================================================================
# MAIN - EXEMPLOS
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("XOR_dist Core Algorithms - Demonstração")
    print("=" * 60)
    
    # Gerar primos
    print("\n1. Gerando primos até 10^6...")
    primes = sieve_of_eratosthenes(10**6)
    print(f"   Total de primos: {len(primes)}")
    
    # Encontrar twins
    print("\n2. Encontrando primos gêmeos...")
    twins = twin_primes(primes)
    print(f"   Total de twins: {len(twins)}")
    
    # Verificar teorema
    print("\n3. Verificando teorema xor_dist(p, p+2) = v₂(p+1)...")
    result = verify_theorem_batch(twins)
    print(f"   Matches: {result['matches']}/{result['total']}")
    print(f"   Taxa de sucesso: {100*result['success_rate']:.4f}%")
    
    # Demonstrar para alguns exemplos
    print("\n4. Demonstrações visuais:")
    for p in [11, 71, 239]:
        if is_prime(p) and is_prime(p + 2):
            print()
            print(demonstrate_theorem(p))
    
    # Estatísticas
    print("\n5. Estatísticas da distribuição de xor_dist:")
    stats = distribution_stats(twins)
    print(f"   Média: {stats['mean']:.3f}")
    print(f"   Desvio padrão: {stats['std']:.3f}")
    print(f"   Entropia: {stats['entropy']:.3f} bits")
    print(f"   Min/Max: {stats['min']}/{stats['max']}")
    
    print("\n" + "=" * 60)
    print("Demonstração concluída!")
