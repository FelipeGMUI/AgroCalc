# custo_producao.py
# ============================================================
# Sistema AgroCalc Web — Módulo 02: Calculadora de Custo
# Disciplina: Matemática Aplicada — Funções Lineares (UC3)
# ============================================================
#
# Este script calcula o custo total de produção de uma lavoura
# utilizando a função afim C(x) = cf + cv * x, onde:
#   x  = sacas produzidas
#   cf = custo fixo (independe da produção)
#   cv = custo variável por saca
# Também determina o ponto de equilíbrio e o lucro/prejuízo.


def custo_total(sacas: float, custo_fixo: float, custo_variavel: float) -> float:
    """
    Calcula o custo total de produção pela função afim C(x).

    Parâmetros:
        sacas         : quantidade produzida em sacas (x)
        custo_fixo    : custos fixos independentes da produção (R$)
                        Ex: arrendamento, salários, depreciação
        custo_variavel: custo por saca produzida (R$/saca)
                        Ex: sementes, defensivos, colheita

    Retorna:
        float: custo total em reais — C(x) = cf + cv * x
    """
    # Aplicação direta da função afim
    return custo_fixo + custo_variavel * sacas


def ponto_equilibrio(custo_fixo: float, preco_venda: float,
                     custo_variavel: float) -> float:
    """
    Calcula o ponto de equilíbrio: quantidade mínima de sacas
    para que a receita cubra todos os custos (lucro = 0).

    Derivação:
        Receita = Custo Total
        pv * x  = cf + cv * x
        x * (pv - cv) = cf
        x* = cf / (pv - cv)

    Parâmetros:
        custo_fixo    : valor dos custos fixos (R$)
        preco_venda   : preço de venda por saca (R$)
        custo_variavel: custo variável por saca (R$)

    Retorna:
        float: quantidade de sacas no ponto de equilíbrio

    Exceção:
        ValueError: quando preço de venda <= custo variável
                    (inviável economicamente)
    """
    # Validação: margem de contribuição deve ser positiva
    if preco_venda <= custo_variavel:
        raise ValueError(
            "O preço de venda deve ser maior que o custo variável. "
            "Caso contrário, cada saca vendida gera prejuízo adicional."
        )

    # Fórmula do ponto de equilíbrio
    margem_contribuicao = preco_venda - custo_variavel
    return custo_fixo / margem_contribuicao


def calcular_lucro(sacas: float, custo_fixo: float,
                   custo_variavel: float, preco_venda: float) -> float:
    """
    Calcula o lucro ou prejuízo total da lavoura.

    Lucro = Receita - Custo Total
          = (pv * x) - (cf + cv * x)
          = x * (pv - cv) - cf

    Parâmetros:
        sacas         : quantidade produzida (x)
        custo_fixo    : custos fixos (R$)
        custo_variavel: custo por saca (R$)
        preco_venda   : preço de venda por saca (R$)

    Retorna:
        float: lucro (positivo) ou prejuízo (negativo) em reais
    """
    receita = preco_venda * sacas
    custo   = custo_total(sacas, custo_fixo, custo_variavel)
    return receita - custo


def imprimir_relatorio(cf: float, cv: float, pv: float, x: float) -> None:
    """
    Imprime relatório completo de análise de custo da lavoura.

    Parâmetros:
        cf: custo fixo (R$)
        cv: custo variável por saca (R$)
        pv: preço de venda por saca (R$)
        x : sacas produzidas
    """
    # Cálculos principais
    ct     = custo_total(x, cf, cv)
    rec    = pv * x
    lucro  = rec - ct
    pe     = ponto_equilibrio(cf, pv, cv)
    mc     = pv - cv    # margem de contribuição unitária

    # Cabeçalho do relatório
    print("\n" + "=" * 55)
    print("   RELATÓRIO DE CUSTO DE PRODUÇÃO — AgroCalc Web")
    print("=" * 55)

    # Parâmetros de entrada
    print("\n📋 PARÂMETROS INFORMADOS:")
    print(f"   Custo fixo (cf):        R$ {cf:>12,.2f}")
    print(f"   Custo variável (cv):    R$ {cv:>12,.2f}/saca")
    print(f"   Preço de venda (pv):    R$ {pv:>12,.2f}/saca")
    print(f"   Sacas produzidas (x):      {x:>12,.1f} sacas")

    # Função de custo
    print("\n📐 FUNÇÃO DE CUSTO: C(x) = cf + cv × x")
    print(f"   C({x:.0f}) = {cf:,.2f} + {cv:.2f} × {x:.0f}")
    print(f"   C({x:.0f}) = R$ {ct:,.2f}")

    # Resultados
    print("\n💰 RESULTADOS:")
    print(f"   Custo total:             R$ {ct:>12,.2f}")
    print(f"   Receita total:           R$ {rec:>12,.2f}")
    sinal = "+" if lucro >= 0 else ""
    print(f"   Lucro / Prejuízo:        R$ {sinal}{lucro:>11,.2f}")

    # Análise do ponto de equilíbrio
    print("\n⚖️  PONTO DE EQUILÍBRIO:")
    print(f"   Margem de contribuição: R$ {mc:>12,.2f}/saca")
    print(f"   x* = cf / (pv - cv) = {cf:,.2f} / {mc:.2f}")
    print(f"   x* = {pe:,.1f} sacas")

    # Diagnóstico
    print("\n🩺 DIAGNÓSTICO:")
    if x > pe:
        folga = x - pe
        print(f"   ✅ PRODUÇÃO ACIMA DO EQUILÍBRIO")
        print(f"   Folga de {folga:.1f} sacas ({folga/pe*100:.1f}% acima do PE)")
    elif x < pe:
        deficit = pe - x
        print(f"   ❌ PRODUÇÃO ABAIXO DO EQUILÍBRIO")
        print(f"   Faltam {deficit:.1f} sacas para atingir o PE")
    else:
        print("   ⚖️  PRODUÇÃO NO PONTO EXATO DE EQUILÍBRIO")

    print("=" * 55)


# ── Bloco principal de execução ──────────────────────────────
if __name__ == "__main__":
    print("╔══════════════════════════════════════════════╗")
    print("║      AgroCalc Web — Custo de Produção        ║")
    print("╚══════════════════════════════════════════════╝")
    print("Função afim: C(x) = Custo Fixo + Custo Variável × Sacas\n")

    try:
        # Entrada de dados com validação
        cf = float(input("Custo fixo total (R$): "))
        if cf < 0:
            raise ValueError("Custo fixo não pode ser negativo.")

        cv = float(input("Custo variável por saca (R$/saca): "))
        if cv < 0:
            raise ValueError("Custo variável não pode ser negativo.")

        pv = float(input("Preço de venda por saca (R$/saca): "))
        if pv <= 0:
            raise ValueError("Preço de venda deve ser positivo.")

        x = float(input("Sacas produzidas (x): "))
        if x < 0:
            raise ValueError("Quantidade de sacas não pode ser negativa.")

        # Gerar relatório completo
        imprimir_relatorio(cf, cv, pv, x)

    except ValueError as e:
        # Tratamento de entradas inválidas (não numéricas ou fora do domínio)
        print(f"\n⚠️  ERRO DE ENTRADA: {e}")
        print("Verifique os valores informados e tente novamente.")
    except ZeroDivisionError:
        print("\n⚠️  ERRO: Divisão por zero. Verifique os parâmetros.")
