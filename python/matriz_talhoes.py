# matriz_talhoes.py
# ============================================================
# Sistema AgroCalc Web — Módulo 05: Mapa de Talhões
# Disciplina: Matemática Aplicada — Matrizes (UC3)
# ============================================================
#
# Este script representa a produtividade agrícola de uma fazenda
# como uma matriz NumPy, onde cada elemento M[i][j] corresponde
# à produtividade (sacas/ha) do setor j na zona i.
#
# Estrutura da matriz (3 × 4):
#   - 3 linhas  = zonas geográficas (Norte, Centro, Sul)
#   - 4 colunas = setores (A, B, C, D)
#
# Operações realizadas:
#   - Média geral (talhoes.mean())
#   - Valor máximo e mínimo (max, min)
#   - Média por zona (axis=1)
#   - Soma de matrizes (comparação com meta)
#   - Estimativa de produção total

import numpy as np


def criar_matriz_talhoes(dados: list) -> np.ndarray:
    """
    Cria e valida a matriz de produtividade de talhões.

    Parâmetro:
        dados: lista de listas com produtividades (sacas/ha)

    Retorna:
        np.ndarray: matriz NumPy de float64

    Exceção:
        ValueError: se os dados contiverem valores negativos
    """
    # Criação da matriz NumPy com dtype float para precisão decimal
    matriz = np.array(dados, dtype=float)

    # Validação: produtividade não pode ser negativa
    if np.any(matriz < 0):
        raise ValueError("Produtividades não podem ser negativas.")

    return matriz


def analisar_produtividade(talhoes: np.ndarray, zonas: list,
                            setores: list, ha_total: float = 300.0) -> dict:
    """
    Executa análise completa de produtividade da fazenda.

    Parâmetros:
        talhoes  : matriz NumPy de produtividades (sacas/ha)
        zonas    : nomes das linhas (zonas geográficas)
        setores  : nomes das colunas (setores da fazenda)
        ha_total : área total da fazenda em hectares

    Retorna:
        dict: dicionário com todos os indicadores calculados
    """
    n_linhas, n_colunas = talhoes.shape
    ha_por_setor        = ha_total / talhoes.size

    # Operações matriciais com NumPy
    media_geral    = talhoes.mean()          # média de todos os elementos
    max_prod       = talhoes.max()           # maior produtividade
    min_prod       = talhoes.min()           # menor produtividade
    media_zonas    = talhoes.mean(axis=1)    # média por linha (zona)
    media_setores  = talhoes.mean(axis=0)    # média por coluna (setor)
    soma_total     = talhoes.sum()           # soma de todos os elementos

    # Estimativa de produção total (sacas × hectares por setor)
    producao_est   = (talhoes * ha_por_setor).sum()

    # Matriz de desvio em relação à meta de 70 sc/ha
    meta           = np.full_like(talhoes, 70.0)
    desvio         = talhoes - meta

    # Classificação por setor (alto, médio, baixo)
    classificacao  = np.where(talhoes >= 70, "ALTO",
                     np.where(talhoes >= 55, "MÉDIO", "BAIXO"))

    return {
        "media_geral"   : media_geral,
        "max_prod"      : max_prod,
        "min_prod"      : min_prod,
        "media_zonas"   : media_zonas,
        "media_setores" : media_setores,
        "producao_est"  : producao_est,
        "ha_por_setor"  : ha_por_setor,
        "desvio"        : desvio,
        "classificacao" : classificacao,
        "soma_total"    : soma_total,
    }


def imprimir_mapa(talhoes: np.ndarray, zonas: list, setores: list) -> None:
    """
    Imprime o mapa visual de produtividade no terminal.

    Parâmetros:
        talhoes : matriz de produtividades
        zonas   : nomes das zonas (linhas)
        setores : nomes dos setores (colunas)
    """
    print("\n" + "=" * 55)
    print("      MAPA DE PRODUÇÃO — AgroCalc Web (sacas/ha)")
    print("=" * 55)

    # Cabeçalho das colunas
    header = f"{'Zona':<12}" + "".join(f"{s:>10}" for s in setores) + f"{'Média':>10}"
    print(header)
    print("-" * 55)

    # Linhas da matriz
    for i, zona in enumerate(zonas):
        linha  = talhoes[i]
        media  = linha.mean()
        cells  = "".join(f"{v:>10.1f}" for v in linha)
        print(f"{zona:<12}{cells}{media:>10.1f}")

    print("-" * 55)

    # Média por setor (última linha)
    medias_col = talhoes.mean(axis=0)
    cells_med  = "".join(f"{v:>10.1f}" for v in medias_col)
    print(f"{'Média':<12}{cells_med}{talhoes.mean():>10.1f}")
    print("=" * 55)


def imprimir_relatorio(talhoes: np.ndarray, zonas: list,
                        setores: list, ha_total: float) -> None:
    """
    Imprime relatório analítico completo da fazenda.

    Parâmetros:
        talhoes  : matriz de produtividades
        zonas    : nomes das zonas
        setores  : nomes dos setores
        ha_total : área total em hectares
    """
    res = analisar_produtividade(talhoes, zonas, setores, ha_total)

    print("\n📊 ANÁLISE MATRICIAL DE PRODUTIVIDADE:")
    print(f"   Média geral:             {res['media_geral']:.1f} sacas/ha")
    print(f"   Maior produtividade:     {res['max_prod']:.1f} sacas/ha")
    print(f"   Menor produtividade:     {res['min_prod']:.1f} sacas/ha")
    print(f"   Área por setor:          {res['ha_por_setor']:.1f} ha")
    print(f"   Estimativa total:        {res['producao_est']:,.0f} sacas")

    print("\n📍 MÉDIA POR ZONA (axis=1):")
    for zona, med in zip(zonas, res['media_zonas']):
        barra = "█" * int(med / 5)
        print(f"   {zona:<10}: {med:5.1f} sc/ha  {barra}")

    print("\n📍 MÉDIA POR SETOR (axis=0):")
    for setor, med in zip(setores, res['media_setores']):
        barra = "█" * int(med / 5)
        print(f"   Setor {setor}: {med:5.1f} sc/ha  {barra}")

    print("\n⚖️  DESVIO EM RELAÇÃO À META (70 sc/ha):")
    print(res['desvio'])

    print("\n🏷️  CLASSIFICAÇÃO DOS SETORES:")
    print(res['classificacao'])


# ── Bloco principal de execução ──────────────────────────────
if __name__ == "__main__":
    print("╔══════════════════════════════════════════════╗")
    print("║       AgroCalc Web — Mapa de Talhões         ║")
    print("╚══════════════════════════════════════════════╝")
    print("Representação matricial de produtividade (sacas/ha)\n")

    # ── Definição dos dados da fazenda ──────────────────────
    # Matriz 3 × 4: 3 zonas × 4 setores
    # Fonte: levantamento de produtividade da safra 2024/25
    DADOS = [
        [62, 58, 71, 65],   # Zona Norte
        [70, 80, 75, 68],   # Zona Centro
        [55, 60, 58, 63],   # Zona Sul
    ]

    ZONAS   = ["Norte", "Centro", "Sul"]
    SETORES = ["A", "B", "C", "D"]
    HA_TOTAL = 300.0   # hectares totais da fazenda

    try:
        # Criação da matriz NumPy
        talhoes = criar_matriz_talhoes(DADOS)

        print("Matriz criada com sucesso:")
        print(f"   Shape: {talhoes.shape} ({talhoes.shape[0]} zonas × {talhoes.shape[1]} setores)")
        print(f"   Dtype: {talhoes.dtype}\n")

        # Imprimir mapa visual
        imprimir_mapa(talhoes, ZONAS, SETORES)

        # Relatório completo de análise
        imprimir_relatorio(talhoes, ZONAS, SETORES, HA_TOTAL)

        # Demonstração adicional: operação de soma de matrizes
        print("\n➕ OPERAÇÃO MATRICIAL — Soma com outra safra (2023/24):")
        safra_anterior = np.array([
            [60, 55, 68, 62],
            [68, 77, 72, 65],
            [52, 57, 55, 60],
        ])
        media_bianual = (talhoes + safra_anterior) / 2
        print("   Média bianual (2023/24 + 2024/25):")
        print(media_bianual)

    except ValueError as e:
        # Tratamento de dados inválidos na matriz
        print(f"\n⚠️  ERRO NOS DADOS: {e}")
