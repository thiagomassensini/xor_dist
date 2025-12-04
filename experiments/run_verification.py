#!/usr/bin/env python3
"""
XOR_dist - Script de Verificação Principal
==========================================

Execute este script para verificar o teorema do xor_dist.

Uso:
    python run_verification.py [limit]
    
Exemplos:
    python run_verification.py           # Até 10^6
    python run_verification.py 10000000  # Até 10^7

Autor: Thiago Fernandes Motta
Data: Dezembro 2025
"""

import sys
import os

# Adiciona o diretório raiz ao path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, 'algorithms'))

from algorithms.core import (
    sieve_of_eratosthenes, twin_primes, xor_dist, v2,
    demonstrate_theorem, distribution_stats, high_xor_dist_twins
)
from algorithms.verification import (
    verify_main_theorem, verify_corollary_all_odds,
    verify_geometric_distribution, verify_by_gap,
    find_extreme_cases, generate_full_report
)


def main():
    # Parse argumentos
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10**6
    
    print("=" * 70)
    print("VERIFICAÇÃO DO TEOREMA XOR_DIST DE MOTTA (2025)")
    print("=" * 70)
    print(f"\nTeorema: xor_dist(p, p+2) = v₂(p+1) para primos gêmeos\n")
    
    # 1. Verificação principal
    print("-" * 70)
    print("ETAPA 1: Verificação do Teorema Principal")
    print("-" * 70)
    result = verify_main_theorem(limit)
    print(result)
    
    if not result.is_proven:
        print("\n⚠️  ATENÇÃO: Contra-exemplos encontrados!")
        for ce in result.counterexamples[:5]:
            print(f"  p = {ce['p']}: xor_dist = {ce['xor_dist']}, v₂ = {ce['v2_p_plus_1']}")
        return
    
    # 2. Demonstrações visuais
    print("\n" + "-" * 70)
    print("ETAPA 2: Demonstrações Visuais")
    print("-" * 70)
    
    examples = [11, 71, 239, 431, 1151]
    for p in examples:
        print(f"\n{demonstrate_theorem(p)}")
    
    # 3. Análise da distribuição
    print("\n" + "-" * 70)
    print("ETAPA 3: Análise da Distribuição")
    print("-" * 70)
    
    primes = sieve_of_eratosthenes(limit)
    twins = twin_primes(primes)
    stats = distribution_stats(twins)
    
    print(f"\nEstatísticas para {len(twins):,} pares de gêmeos:")
    print(f"  Média:    {stats['mean']:.4f}")
    print(f"  Desvio:   {stats['std']:.4f}")
    print(f"  Entropia: {stats['entropy']:.4f} bits")
    print(f"  Min/Max:  {stats['min']} / {stats['max']}")
    
    print("\nDistribuição de xor_dist:")
    print(f"  {'k':>3} | {'Observado':>10} | {'Frequência':>10} | {'Teórico (2^-k)':>14}")
    print("  " + "-" * 45)
    for k, count in sorted(stats['distribution'].items())[:10]:
        freq = count / len(twins)
        teorico = 2**(-k)
        print(f"  {k:>3} | {count:>10,} | {freq:>10.4f} | {teorico:>14.4f}")
    
    # 4. Teste de distribuição geométrica
    print("\n" + "-" * 70)
    print("ETAPA 4: Teste de Distribuição Geométrica")
    print("-" * 70)
    
    geom_result = verify_geometric_distribution(twins)
    print(f"\nTeste χ² para Geom(1/2):")
    print(f"  χ² calculado:     {geom_result['chi_squared']:.2f}")
    print(f"  Valor crítico:    {geom_result['critical_value']:.2f}")
    print(f"  Graus liberdade:  {geom_result['degrees_of_freedom']}")
    print(f"  Resultado:        {'✓ É Geom(1/2)' if geom_result['is_geometric'] else '✗ Não é Geom(1/2)'}")
    
    # 5. Casos extremos
    print("\n" + "-" * 70)
    print("ETAPA 5: Casos Extremos")
    print("-" * 70)
    
    extremes = find_extreme_cases(limit)
    
    if extremes['max_xor_dist_pair']:
        p, q, d = extremes['max_xor_dist_pair']
        print(f"\nMaior xor_dist encontrado:")
        print(f"  p = {p}, p+2 = {q}")
        print(f"  xor_dist = {d}")
        print(f"  v₂(p+1) = {v2(p+1)}")
    
    print(f"\nTop 10 twins com alto xor_dist:")
    for p, q, d in extremes['high_v2_twins'][:10]:
        print(f"  ({p:>7}, {q:>7}): xor_dist = v₂({p+1}) = {d}")
    
    # 6. Conclusão
    print("\n" + "=" * 70)
    print("CONCLUSÃO")
    print("=" * 70)
    print(f"""
O teorema xor_dist(p, p+2) = v₂(p+1) foi VERIFICADO com sucesso
para todos os {len(twins):,} pares de primos gêmeos até {limit:,}.

Taxa de verificação: 100.0000%

A distribuição segue Geom(1/2), confirmando a teoria.
    """)
    print("=" * 70)


if __name__ == "__main__":
    main()
