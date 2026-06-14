# blend_fertilizante.py
# ============================================================
# Sistema AgroCalc Web — Módulo 06: Blend de Fertilizante
# Disciplina: Matemática Aplicada — Sistemas Lineares (UC3)
# ============================================================
#
# Este script resolve o problema de blend de fertilizantes:
# dadas as metas de NPK (Nitrogênio, Fósforo, Potássio) em
# kg/ha, calcular as quantidades necessárias de cada produto.
#
# O problema resulta em um sistema linear 3×3:
#
#   A · x = b
#
#   Onde:
#   A = matriz de composição (3 fertilizantes × 3 nutrientes)
#   x = vetor de quantidades a determinar (kg/ha de cada produto)
#   b = vetor de metas de NPK (kg/ha)
#
# Composição dos fertilizantes (frações decimais):
#   Ureia       : 45% N, 10% P, 5% K  → linha [0.45, 0.10, 0.05]
#   Superfosfato:  0% N, 46% P, 0% K  → linha [0.00, 0.46, 0.00]
#   KCl         :  0% N,  0% P, 60% K → linha [0.00, 0.00, 0.60]
#
# Sistema resultante:
#   0.45·u + 0.00·s + 0.00·k = N_meta   (equação do N)
#   0.10·u + 0.46·s + 0.00·k = P_meta   (equação do P)
#   0.05·u + 0.00·s + 0.60·k = K_meta   (equação do K)

import numpy as np


# ── Matriz de composição dos fertilizantes ───────────────────
# A_comp: cada LINHA = fertilizante, cada COLUNA = nutriente (N, P, K)
A_comp = np.array([
    [0.45, 0.10, 0.05],   # Ureia:        45%N, 10%P,  5%K
    [0.00, 0.46, 0.00],   # Superfosfato:  0%N, 46%P,  0%K
    [0.00, 0.00, 0.60],   # KCl:           0%N,  0%P, 60%K
], dtype=float)

# ── Matriz do sistema linear A (equações por nutriente) ──────
# Para resolver A·x = b, onde x = [ureia, superfosfato, KCl]:
#   Equação N: 0.45·u + 0·s + 0·k = N_meta
#   Equação P: 0.10·u + 0.46·s + 0·k = P_meta
#   Equação K: 0.05·u + 0·s + 0.60·k = K_meta
#
# A matriz do sistema é a TRANSPOSTA de A_comp:
A = A_comp.T   # shape (3,3): linhas = nutrientes, colunas = fertilizantes

# Nomes dos fertilizantes e nutrientes
FERTILIZANTES = ["Ureia", "Superfosfato", "KCl"]
NUTRIENTES    = ["Nitrogênio (N)", "Fósforo (P)", "Potássio (K)"]


def calcular_determinante(matriz: np.ndarray) -> float:
    """
    Calcula o determinante da matriz de composição.

    O determinante verifica se o sistema tem solução única:
    - det(A) ≠ 0 → sistema determinado (solução única)
    - det(A) = 0 → sistema indeterminado ou impossível

    Parâmetro:
        matriz: matriz NumPy quadrada n×n

    Retorna:
        float: valor do determinante
    """
    return float(np.linalg.det(matriz))


def resolver_sistema(matriz: np.ndarray, meta: np.ndarray) -> np.ndarray:
    """
    Resolve o sistema linear A·x = b usando numpy.linalg.solve().

    O método utiliza eliminação de Gauss com pivotamento parcial,
    que é numericamente estável para sistemas 3×3 como este.

    Parâmetros:
        matriz: matriz de coeficientes A (3×3)
        meta  : vetor de termos independentes b (metas NPK)

    Retorna:
        np.ndarray: vetor x com as quantidades de cada fertilizante

    Exceção:
        np.linalg.LinAlgError: sistema singular (det = 0)
        ValueError: solução com valores negativos (inviável)
    """
    # Verificação prévia do determinante
    det = calcular_determinante(matriz)
    if abs(det) < 1e-10:
        raise np.linalg.LinAlgError(
            f"Sistema singular (det = {det:.6f}). "
            "Os fertilizantes escolhidos não formam uma base independente."
        )

    # Resolução do sistema linear
    x = np.linalg.solve(matriz, meta)

    # Verificação: x não pode ter valores negativos (quantidade física)
    if np.any(x < -0.01):
        raise ValueError(
            "Solução inviável: a meta NPK não pode ser atingida com "
            "esses fertilizantes nas proporções definidas. "
            "Considere ajustar as metas ou os produtos disponíveis."
        )

    # Arredondar valores muito próximos de zero
    x = np.where(np.abs(x) < 0.001, 0.0, x)
    return x


def verificar_solucao(matriz: np.ndarray, x: np.ndarray,
                       meta: np.ndarray) -> np.ndarray:
    """
    Verifica a solução calculando A·x e comparando com b.

    A·x deve ser igual ao vetor de metas b.
    Esta verificação confirma a corretude numérica do resultado.

    Parâmetros:
        matriz: matriz de composição A
        x     : solução calculada (quantidades de fertilizantes)
        meta  : vetor de metas NPK

    Retorna:
        np.ndarray: vetor de diferenças (A·x − b), idealmente ≈ 0
    """
    # Calcular NPK entregue: A·x (sistema já está na forma nutriente × fertilizante)
    entregue = matriz @ x
    diferenca = entregue - meta
    return entregue, diferenca


def imprimir_relatorio(meta: np.ndarray, x: np.ndarray,
                        det: float) -> None:
    """
    Imprime relatório completo do blend calculado.

    Parâmetros:
        meta: vetor de metas NPK (kg/ha)
        x   : solução (quantidades de fertilizantes em kg/ha)
        det : determinante da matriz de composição
    """
    print("\n" + "=" * 55)
    print("    RELATÓRIO DE BLEND DE FERTILIZANTE — AgroCalc Web")
    print("=" * 55)

    # Parâmetros de entrada
    print("\n🎯 METAS DE NPK (kg/ha):")
    for nutriente, valor in zip(NUTRIENTES, meta):
        print(f"   {nutriente:<20}: {valor:8.2f} kg/ha")

    # Verificação do determinante
    print(f"\n🔢 VERIFICAÇÃO DO SISTEMA LINEAR:")
    print(f"   det(A) = {det:.6f}")
    if abs(det) > 1e-10:
        print(f"   ✅ Sistema com solução única (det ≠ 0)")
    else:
        print(f"   ❌ Sistema sem solução única (det ≈ 0)")
        return

    # Solução: quantidades de fertilizantes
    print("\n⚗️  QUANTIDADES NECESSÁRIAS DE FERTILIZANTES:")
    total = 0.0
    for fert, qtd in zip(FERTILIZANTES, x):
        print(f"   {fert:<15}: {qtd:8.2f} kg/ha")
        total += qtd
    print(f"   {'TOTAL':<15}: {total:8.2f} kg/ha")

    # Verificação da solução
    entregue, diferenca = verificar_solucao(A, x, meta)
    print("\n✅ VERIFICAÇÃO (A·x vs. meta):")
    print(f"   {'Nutriente':<22} {'Meta':>8} {'Entregue':>10} {'Δ':>8}")
    print("   " + "-" * 52)
    for nut, m, e, d in zip(NUTRIENTES, meta, entregue, diferenca):
        status = "✓" if abs(d) < 0.01 else "✗"
        print(f"   {nut:<22} {m:>8.2f} {e:>10.4f} {d:>+8.4f} {status}")

    # Custo estimado
    print("\n💰 CUSTO ESTIMADO DO BLEND (preços de referência):")
    precos_ref = {"Ureia": 2.85, "Superfosfato": 3.20, "KCl": 2.50}  # R$/kg
    custo_total = 0.0
    for fert, qtd in zip(FERTILIZANTES, x):
        custo = qtd * precos_ref[fert]
        custo_total += custo
        print(f"   {fert:<15}: {qtd:.2f} kg × R${precos_ref[fert]:.2f}/kg = R${custo:.2f}/ha")
    print(f"   {'Custo total':<15}: R${custo_total:.2f}/ha")

    print("=" * 55)


def imprimir_matriz_composicao() -> None:
    """Exibe a matriz de composição dos fertilizantes para referência."""
    print("\n📋 MATRIZ DE COMPOSIÇÃO (A_comp — fertilizante × nutriente):")
    print(f"   {'':15} {'N':>8} {'P':>8} {'K':>8}")
    print("   " + "-" * 35)
    for fert, linha in zip(FERTILIZANTES, A_comp):
        print(f"   {fert:<15}" + "".join(f"{v:>8.2f}" for v in linha))
    print(f"\n   Matriz do sistema A = A_comp.T (nutriente × fertilizante):")
    print(f"   Dimensão: {A.shape[0]}×{A.shape[1]} — sistema 3×3")


# ── Bloco principal de execução ──────────────────────────────
if __name__ == "__main__":
    print("╔══════════════════════════════════════════════╗")
    print("║    AgroCalc Web — Blend de Fertilizante NPK  ║")
    print("╚══════════════════════════════════════════════╝")
    print("Sistema linear A·x = b (numpy.linalg.solve)\n")

    # Exibir matriz de composição
    imprimir_matriz_composicao()

    try:
        # Entrada das metas de NPK
        print("\n📝 INFORME AS METAS DE NPK:")
        n_meta = float(input("   Meta de Nitrogênio (N) em kg/ha: "))
        p_meta = float(input("   Meta de Fósforo (P) em kg/ha: "))
        k_meta = float(input("   Meta de Potássio (K) em kg/ha: "))

        # Validação das metas
        if any(v < 0 for v in [n_meta, p_meta, k_meta]):
            raise ValueError("As metas de NPK não podem ser negativas.")

        # Vetor de metas b
        b = np.array([n_meta, p_meta, k_meta])

        # Cálculo do determinante
        det = calcular_determinante(A)

        # Resolução do sistema
        x = resolver_sistema(A, b)

        # Relatório completo
        imprimir_relatorio(b, x, det)

    except np.linalg.LinAlgError as e:
        # Sistema singular: sem solução única
        print(f"\n⚠️  ERRO MATEMÁTICO: {e}")
    except ValueError as e:
        # Dados de entrada inválidos ou solução inviável
        print(f"\n⚠️  ERRO DE DADOS: {e}")
    except Exception as e:
        # Qualquer outro erro inesperado
        print(f"\n⚠️  ERRO INESPERADO: {e}")
