# Teorema do xor_dist para Primos Gêmeos

**Versão Revisada — Dezembro 2025**

---

## Enunciado

**Teorema (Motta, 2025).** Para todo primo ímpar $p$ tal que $p+2$ também é primo, vale:

$$\boxed{\operatorname{xor\_dist}(p, p+2) = v_2(p+1)}$$

onde:
- $\operatorname{xor\_dist}(a,b) = \operatorname{popcount}(a \oplus b)$ é a distância de Hamming,
- $v_2(n)$ é a valorização 2-ádica de $n$.

---

## Demonstração Formal

### Definições Preliminares

**Definição 1 (Representação binária).** Para $n \in \mathbb{Z}_{\geq 0}$, a representação binária é:
$$n = \sum_{i=0}^{k} b_i \cdot 2^i, \quad b_i \in \{0,1\}$$

Denotamos $\operatorname{bit}_i(n) := b_i$.

**Definição 2 (Popcount).** O peso de Hamming é:
$$\operatorname{popcount}(n) = \sum_{i \geq 0} \operatorname{bit}_i(n)$$

**Definição 3 (Valorização 2-ádica).** 
$$v_2(n) = \max\{k \geq 0 : 2^k \mid n\}$$

Equivalente ao número de zeros à direita na representação binária de $n$.

---

## Lema 1 — Ímpares terminam com bit 1

**Lema.** Se $n$ é ímpar, então $\operatorname{bit}_0(n) = 1$.

**Prova.** Imediato pelo critério de paridade: $n \equiv 1 \pmod{2}$ se e somente se $b_0 = 1$. $\square$

---

## Lema 2 — Relação entre trailing ones e $v_2(n+1)$

**Lema.** Seja $n$ um inteiro ímpar com exatamente $k \geq 1$ bits 1 consecutivos ao final (trailing ones):
$$n = \ldots b_m \, 0 \, \underbrace{1\,1\,\cdots\,1}_{k}$$

Então:

1. $n + 1 = \ldots b_m \, 1 \, \underbrace{0\,0\,\cdots\,0}_{k}$

2. $v_2(n+1) = k$

**Prova.** 

Como $n$ termina com $k$ uns consecutivos e o bit na posição $k$ é necessariamente 0 (caso contrário, teríamos mais trailing ones), podemos escrever:
$$n = N \cdot 2^{k+1} + (2^k - 1)$$

para algum $N \geq 0$, onde $N$ codifica os bits nas posições $k+1, k+2, \ldots$

O termo $(2^k - 1) = \underbrace{1\,1\,\cdots\,1}_{k}$ representa os $k$ trailing ones.

Somando 1:
$$n + 1 = N \cdot 2^{k+1} + 2^k = (2N + 1) \cdot 2^k$$

Observe que $2N + 1$ é **sempre ímpar** (independente do valor de $N$). Portanto, a maior potência de 2 que divide $n+1$ é exatamente $2^k$, logo:
$$v_2(n+1) = k$$

*Nota:* O fator $(2N+1)$ ser ímpar é o que garante que o carry "não sobe mais" — ele para exatamente na posição $k$. $\square$

---

## Lema 3 — Estrutura de $n+2$

**Lema.** Se $n$ é ímpar e possui $k \geq 1$ trailing ones, então:
$$n + 2 = \ldots b_m \, 1 \, \underbrace{0\,0\,\cdots\,0}_{k-1} \, 1$$

**Caso especial:** Para $k = 1$, a expressão reduz-se a $\ldots b_m \, 1 \, 1$ (sem zeros intermediários).

**Prova.** 

Somar $2 = (10)_2$ a $n = \ldots 0\,\underbrace{1\,1\,\cdots\,1}_{k}$ produz:

| Posição | Bit de $n$ | Soma | Resultado | Carry out |
|---------|------------|------|-----------|-----------|
| 0 | 1 | 1 + 0 = 1 | **1** | 0 |
| 1 | 1 | 1 + 1 = 2 | **0** | 1 |
| 2 | 1 | 1 + 0 + 1 = 2 | **0** | 1 |
| $\vdots$ | 1 | 1 + 0 + 1 = 2 | **0** | 1 |
| $k-1$ | 1 | 1 + 0 + 1 = 2 | **0** | 1 |
| $k$ | 0 | 0 + 0 + 1 = 1 | **1** | 0 |
| $> k$ | $b_j$ | $b_j$ + 0 + 0 | $b_j$ | 0 |

Análise:
- **Bit 0:** permanece 1 (não recebe carry de lugar nenhum)
- **Bits 1 a $k-1$:** recebem carry e viram 0, propagando carry adiante
- **Bit $k$:** era 0, recebe carry e vira 1, **sem propagar** (0+1=1)
- **Bits $> k$:** inalterados (carry não chega)

Resultado: $n + 2 = \ldots b_m \, 1 \, \underbrace{0\,0\,\cdots\,0}_{k-1} \, 1$

Para $k = 1$: não há bits entre as posições 0 e 1, então $n + 2 = \ldots b_m \, 1 \, 1$. $\square$

---

## Prova do Teorema Principal

**Teorema.** Para primo ímpar $p$ com $p+2$ também primo: $\operatorname{xor\_dist}(p, p+2) = v_2(p+1)$.

**Prova.**

Seja $p$ primo ímpar e defina $k := v_2(p+1)$.

**Passo 1:** Determinação dos trailing ones de $p$.

Como $v_2(p+1) = k$, temos que $p+1$ possui exatamente $k$ zeros à direita. Equivalentemente, $p$ termina com exatamente $k$ bits 1 consecutivos (trailing ones). Isso decorre diretamente do Lema 2, lido "de trás para frente": se $v_2(n+1) = k$, então $n$ tem $k$ trailing ones.

Portanto:
$$p = \ldots b_m \, 0 \, \underbrace{1\,1\,\cdots\,1}_{k}$$

**Passo 2:** Aplicação do Lema 3.

Pelo Lema 3:
$$p + 2 = \ldots b_m \, 1 \, \underbrace{0\,0\,\cdots\,0}_{k-1} \, 1$$

**Passo 3:** Cálculo do XOR bit a bit.

$$p \oplus (p+2):$$

| Posição | Bit de $p$ | Bit de $p+2$ | XOR |
|---------|------------|--------------|-----|
| 0 | 1 | 1 | **0** |
| 1 | 1 | 0 | **1** |
| 2 | 1 | 0 | **1** |
| $\vdots$ | 1 | 0 | **1** |
| $k-1$ | 1 | 0 | **1** |
| $k$ | 0 | 1 | **1** |
| $> k$ | $b_j$ | $b_j$ | **0** |

**Passo 4:** Contagem dos bits 1 no XOR.

- Posição 0: contribui **0** (ambos têm bit 1)
- Posições 1 a $k-1$: contribuem **$k-1$** (cada uma tem $1 \oplus 0 = 1$)
- Posição $k$: contribui **1** (temos $0 \oplus 1 = 1$)
- Posições $> k$: contribuem **0** (bits idênticos, $b_j \oplus b_j = 0$)

Total:
$$\operatorname{popcount}(p \oplus (p+2)) = 0 + (k-1) + 1 + 0 = k$$

**Conclusão:**
$$\operatorname{xor\_dist}(p, p+2) = k = v_2(p+1)$$

$\blacksquare$

---

## Observação Importante

> **Remark.** A primalidade de $p$ e $p+2$ **não aparece em nenhum passo** da demonstração. O argumento é puramente aritmético-binário, baseado apenas na paridade de $p$.

**Corolário.** O resultado vale para **todo inteiro ímpar positivo**:
$$\operatorname{xor\_dist}(n, n+2) = v_2(n+1) \quad \forall\, n \equiv 1 \pmod{2}$$

A menção a primos gêmeos serve apenas para destacar um caso de interesse na teoria dos números.

---

## Casos Especiais

### Primos de Mersenne

Se $p = 2^n - 1$ é primo de Mersenne:
- $p = \underbrace{1\,1\,\cdots\,1}_{n}$ (todos os bits são 1)
- $p + 1 = 2^n$
- $v_2(p+1) = n$
- Se $p+2 = 2^n + 1$ fosse primo: $\operatorname{xor\_dist}(p, p+2) = n$

*(Nota: $2^n + 1$ só é primo se $n$ é potência de 2 — primos de Fermat)*

### Máximo xor_dist observado até $10^7$

O recorde entre primos gêmeos:
- $p = 786431$, $p+2 = 786433$
- $v_2(786432) = v_2(2^{18} \cdot 3) = 18$
- $\operatorname{xor\_dist}(786431, 786433) = 18$

---

## Status

- [x] Demonstração formal completa (versão revisada)
- [x] Verificação computacional (100% até $10^7$ — 58,980 pares)
- [ ] Publicação arXiv
