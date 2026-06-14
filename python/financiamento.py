# financiamento.py
# ============================================================
# Sistema AgroCalc Web — Módulo 03: Financiamento Agrícola
# Disciplina: Matemática Aplicada — Matemática Financeira (UC3)
# ============================================================
#
# Este script simula o financiamento de máquinas e equipamentos
# agrícolas utilizando o Sistema de Amortização Francês (SAF),
# também conhecido como Tabela Price, onde as parcelas são fixas
# e calculadas pela fórmula PMT (Payment) de juros compostos.
#
# Fórmula PMT:
#   PMT = PV × [i × (1+i)ⁿ] / [(1+i)ⁿ − 1]
#
# Onde:
#   PV = Valor presente (principal financiado)
#   i  = Taxa de juros mensal (decimal)
#   n  = Número de parcelas (meses)


def calcular_parcela(pv: float, taxa: float, n: int) -> float:
    """
    Calcula o valor da parcela mensal pelo método Price (SAF).

    A fórmula PMT garante parcelas iguais durante todo o período,
    variando apenas a proporção entre juros e amortização mês a mês.

    Parâmetros:
        pv   : valor financiado em reais (Present Value)
        taxa : taxa de juros mensal em decimal
               Ex: 1.5% a.m. → taxa = 0.015
        n    : número de parcelas (meses)

    Retorna:
        float: valor da parcela mensal em reais

    Exceção:
        ValueError: quando taxa ou n são inválidos
    """
    # Validação dos parâmetros
    if pv <= 0:
        raise ValueError("O valor financiado deve ser positivo.")
    if taxa < 0:
        raise ValueError("A taxa de juros não pode ser negativa.")
    if n <= 0:
        raise ValueError("O número de parcelas deve ser positivo.")

    # Caso especial: taxa zero (sem juros)
    if taxa == 0:
        return pv / n

    # Fórmula PMT: PV × [i × (1+i)^n] / [(1+i)^n − 1]
    fator = (1 + taxa) ** n          # (1 + i)^n — fator de capitalização
    pmt   = pv * (taxa * fator) / (fator - 1)
    return pmt


def tabela_amortizacao(pv: float, taxa: float, n: int,
                        imprimir: bool = True) -> list:
    """
    Gera a tabela de amortização completa do financiamento.

    Em cada período:
        Juros        = Saldo devedor × taxa
        Amortização  = PMT − Juros
        Saldo final  = Saldo anterior − Amortização

    Parâmetros:
        pv       : valor financiado (R$)
        taxa     : taxa de juros mensal (decimal)
        n        : número de parcelas
        imprimir : se True, imprime a tabela no terminal

    Retorna:
        list: lista de dicionários com dados de cada parcela
    """
    parcela    = calcular_parcela(pv, taxa, n)
    saldo      = pv
    total_pago = 0
    total_juro = 0
    registros  = []

    if imprimir:
        # Cabeçalho da tabela
        print("\n" + "=" * 66)
        print("        TABELA DE AMORTIZAÇÃO — Sistema Price (SAF)")
        print("=" * 66)
        print(f"{'Mês':>4} | {'Parcela (R$)':>12} | {'Juros (R$)':>10} | "
              f"{'Amort. (R$)':>11} | {'Saldo (R$)':>12}")
        print("-" * 66)

    for mes in range(1, n + 1):
        # Cálculo das componentes da parcela
        juros       = saldo * taxa          # parte dos juros neste mês
        amortizacao = parcela - juros       # parte que reduz o saldo
        saldo      -= amortizacao           # novo saldo devedor
        saldo_real  = max(saldo, 0.0)       # evita valores negativos por arredondamento

        # Acumuladores
        total_pago += parcela
        total_juro += juros

        # Armazenar registro
        registro = {
            "mes"         : mes,
            "parcela"     : parcela,
            "juros"       : juros,
            "amortizacao" : amortizacao,
            "saldo"       : saldo_real,
        }
        registros.append(registro)

        if imprimir:
            print(f"{mes:>4} | {parcela:>12,.2f} | {juros:>10,.2f} | "
                  f"{amortizacao:>11,.2f} | {saldo_real:>12,.2f}")

    if imprimir:
        # Totalizadores
        print("=" * 66)
        print(f"\n📊 RESUMO DO FINANCIAMENTO:")
        print(f"   Valor financiado (PV):  R$ {pv:>12,.2f}")
        print(f"   Parcela mensal (PMT):   R$ {parcela:>12,.2f}")
        print(f"   Total pago:             R$ {total_pago:>12,.2f}")
        print(f"   Total de juros:         R$ {total_juro:>12,.2f}")
        print(f"   Custo efetivo total:       {(total_pago/pv - 1)*100:>11.2f}%")
        print("=" * 66)

    return registros


def comparar_cenarios(pv: float, taxas: list, prazos: list) -> None:
    """
    Compara múltiplos cenários de financiamento.

    Parâmetros:
        pv    : valor financiado (R$)
        taxas : lista de taxas mensais (decimal)
        prazos: lista de números de parcelas
    """
    print(f"\n{'Taxa':>8} | {'Prazo':>8} | {'PMT':>12} | {'Total':>12} | {'Juros':>12}")
    print("-" * 62)

    for taxa in taxas:
        for n in prazos:
            try:
                pmt   = calcular_parcela(pv, taxa, n)
                total = pmt * n
                juros = total - pv
                print(f"{taxa*100:>7.2f}% | {n:>5} meses | "
                      f"R${pmt:>10,.2f} | R${total:>10,.2f} | R${juros:>10,.2f}")
            except ValueError as e:
                print(f"   Erro no cenário (taxa={taxa}, n={n}): {e}")


# ── Bloco principal de execução ──────────────────────────────
if __name__ == "__main__":
    print("╔══════════════════════════════════════════════╗")
    print("║      AgroCalc Web — Financiamento Agrícola   ║")
    print("╚══════════════════════════════════════════════╝")
    print("Fórmula PMT: parcela = PV × [i×(1+i)ⁿ] / [(1+i)ⁿ−1]\n")

    try:
        # Entrada de dados
        vm = float(input("Valor da máquina/equipamento (R$): "))
        en = float(input("Valor da entrada (R$, 0 se não houver): "))
        if en >= vm:
            raise ValueError("A entrada não pode ser maior ou igual ao valor da máquina.")

        pv   = vm - en     # valor efetivamente financiado
        taxa = float(input("Taxa de juros mensal (%): ")) / 100
        n    = int(input("Número de parcelas (meses): "))

        print(f"\nValor financiado (PV = VM − Entrada): R$ {pv:,.2f}")

        # Gerar tabela de amortização
        tabela_amortizacao(pv, taxa, n, imprimir=True)

        # Comparação de cenários (exemplo com taxas e prazos variados)
        print("\n\n📋 COMPARATIVO DE CENÁRIOS (mesmo valor financiado):")
        comparar_cenarios(pv, taxas=[taxa], prazos=[12, 24, 36, 48, 60])

    except ValueError as e:
        # Tratamento de entradas não numéricas ou fora do domínio
        print(f"\n⚠️  ERRO DE ENTRADA: {e}")
        print("Verifique os valores informados e tente novamente.")
    except ZeroDivisionError:
        print("\n⚠️  ERRO: Divisão por zero. Taxa ou número de parcelas inválidos.")
