import numpy as np
import matplotlib.pyplot as plt


def calcular_distribuicao_por_intervalo(P_max, afundamento, eficiencia):
    """
    Calcula a distribuição de energia para cada intervalo de meia hora.
    """
    # Converter porcentagens para decimais
    afundamento_dec = afundamento / 100
    eficiencia_dec = eficiencia / 100

    # Criar intervalos de meia hora (0 a 24 horas, com passo de 0.5)
    horas = np.arange(0, 24.5, 0.5)
    n_intervalos = len(horas) - 1

    # Parâmetros da curva gaussiana (pico ao meio-dia)
    mu = 12  # pico ao meio-dia
    sigma = 2  # largura da curva

    # Pico da curva é a potência do sistema dividido por 1.20
    P_pico = P_max / 1.20

    # Calcular potência média em cada intervalo de meia hora
    P_intervalo = np.zeros(n_intervalos)

    for i in range(n_intervalos):
        # Ponto médio do intervalo
        t_medio = horas[i] + 0.25
        # Potência no ponto médio (kW) - curva gaussiana
        P_calculada = P_pico * np.exp(-((t_medio - mu) ** 2) / (2 * sigma ** 2))

        # Aplicar restrição: considerar apenas potência acima de 36kW
        if P_calculada > 36:
            P_intervalo[i] = P_calculada
        else:
            P_intervalo[i] = 0

    # Calcular energia em cada intervalo (kWh) - potência média * 0.5 horas
    energia_intervalo = P_intervalo * 0.5

    # Calcular energia total
    energia_total = np.sum(energia_intervalo)

    # Calcular as componentes para cada intervalo
    # Armazenado: eficiência * potência
    energia_armazenada_intervalo = energia_intervalo * eficiencia_dec

    # Perdas: (1 - eficiência) * potência
    energia_perdas_intervalo = energia_intervalo * (1 - eficiencia_dec)

    # Reserva: (1 - afundamento) * eficiência * potência
    energia_afundamento_intervalo = energia_intervalo * (1 - afundamento_dec) * eficiencia_dec

    return (horas, P_intervalo, energia_armazenada_intervalo,
            energia_afundamento_intervalo, energia_perdas_intervalo, energia_total)


def plot_grafico_barras_seccionadas(P_max, afundamento, eficiencia):
    """
    Gera gráfico de barras seccionadas para cada intervalo de meia hora.
    """
    # Calcular distribuições
    (horas, P_intervalo, energia_armazenada,
     energia_afundamento, energia_perdas, energia_total) = calcular_distribuicao_por_intervalo(
        P_max, afundamento, eficiencia
    )

    # Converter energia para potência (kW) - dividir pelo tempo (0.5 horas)
    potencia_armazenada = energia_armazenada / 0.5
    potencia_afundamento = energia_afundamento / 0.5
    potencia_perdas = energia_perdas / 0.5

    # Criar figura
    fig, ax = plt.subplots(figsize=(16, 8))

    # Configurar posições das barras
    n_intervalos = len(P_intervalo)
    x = np.arange(n_intervalos)
    largura = 0.8

    # Criar barras empilhadas (potência em kW)
    bars1 = ax.bar(x, potencia_armazenada, largura,
                   label=f'Energia Armazenada ({eficiencia}% eficiência)',
                   color='#2ecc71', edgecolor='black', linewidth=0.5)

    bars2 = ax.bar(x, potencia_afundamento, largura,
                   bottom=potencia_armazenada,
                   label=f'Reserva (Afundamento {afundamento}%)',
                   color='#f39c12', edgecolor='black', linewidth=0.5)

    bars3 = ax.bar(x, potencia_perdas, largura,
                   bottom=potencia_armazenada + potencia_afundamento,
                   label='Perdas',
                   color='#e74c3c', edgecolor='black', linewidth=0.5)

    # Configurar eixo x
    horas_mostrar = np.arange(0, 25, 2)
    indices_mostrar = [int(h * 2) for h in horas_mostrar if h * 2 < n_intervalos]
    ax.set_xticks(indices_mostrar)
    ax.set_xticklabels([f'{h:.0f}h' for h in horas_mostrar if h * 2 < n_intervalos])

    # Configurar título e labels
    ax.set_title(f'Distribuição de Potência por Intervalo de Meia Hora\n'
                 f'Potência do Sistema: {P_max} kW | Afundamento: {afundamento}% | Eficiência: {eficiencia}%',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Hora do Dia', fontsize=12, fontweight='bold')
    ax.set_ylabel('Potência (kW)', fontsize=12, fontweight='bold')

    # Configurar grid
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Adicionar legenda
    ax.legend(loc='upper left', fontsize=10, framealpha=0.9)

    # Ajustar layout
    plt.tight_layout()
    plt.show()

    # Calcular totais para retorno
    total_armazenado = np.sum(energia_armazenada)
    total_afundamento = np.sum(energia_afundamento)
    total_perdas = np.sum(energia_perdas)

    return energia_total, total_armazenado, total_afundamento, total_perdas


def calcular_e_verificar(P_max, afundamento, eficiencia):
    """
    Calcula e verifica os resultados.
    """
    print("=" * 70)
    print("ANÁLISE DE DISTRIBUIÇÃO DE ENERGIA")
    print("=" * 70)
    print(f"Potência do Sistema: {P_max} kW")
    print(f"Afundamento: {afundamento}%")
    print(f"Eficiência: {eficiencia}%")
    print("=" * 70)

    # Calcular distribuição
    (horas, P_intervalo, energia_armazenada,
     energia_afundamento, energia_perdas, energia_total) = calcular_distribuicao_por_intervalo(
        P_max, afundamento, eficiencia
    )

    # Calcular totais
    total_armazenado = np.sum(energia_armazenada)
    total_afundamento = np.sum(energia_afundamento)
    total_perdas = np.sum(energia_perdas)

    # Calcular valores teóricos para referência
    P_pico = P_max / 1.20

    print("\nINFORMAÇÕES DA CURVA:")
    print(f"✓ Potência de Pico da Curva: {P_pico:.2f} kW")
    print(f"✓ Dispersão da Curva (sigma): 2")
    print(f"✓ Restrição: Potência considerada apenas acima de 36 kW")

    # Encontrar o período de geração
    indices_geracao = np.where(P_intervalo > 0)[0]
    if len(indices_geracao) > 0:
        hora_inicio = indices_geracao[0] * 0.5
        hora_fim = (indices_geracao[-1] + 1) * 0.5
        print(f"✓ Período de Geração: {hora_inicio:.1f}h às {hora_fim:.1f}h")

    print("\nRESULTADOS OBTIDOS:")
    print(f"✓ Energia Gerada: {energia_total:.2f} kWh")
    print(f"✓ Energia Armazenada: {total_armazenado:.2f} kWh")
    print(f"✓ Reserva (Afundamento): {total_afundamento:.2f} kWh")
    print(f"✓ Perdas: {total_perdas:.2f} kWh")
    print(f"✓ Validação: {total_armazenado + total_afundamento + total_perdas:.2f} kWh = {energia_total:.2f} kWh")

    # Verificar porcentagens
    if energia_total > 0:
        print("\nDISTRIBUIÇÃO PERCENTUAL:")
        print(f"✓ Armazenado: {(total_armazenado / energia_total * 100):.1f}%")
        print(f"✓ Reserva: {(total_afundamento / energia_total * 100):.1f}%")
        print(f"✓ Perdas: {(total_perdas / energia_total * 100):.1f}%")

    print("\n" + "=" * 70)

    return energia_total, total_armazenado, total_afundamento, total_perdas


# Exemplo principal
if __name__ == "__main__":
    # Solicitar dados do usuário
    print("=" * 70)
    print("SISTEMA DE ARMAZENAMENTO DE ENERGIA")
    print("=" * 70)

    potencia_sistema = float(input("Digite a potência do sistema (kW): "))
    afundamento = float(input("Digite o percentual de afundamento (%): "))
    eficiencia = float(input("Digite a eficiência do sistema (%): "))

    print("\n" + "=" * 70)

    # Calcular e mostrar resultados
    energia_total, total_armazenado, total_afundamento, total_perdas = calcular_e_verificar(
        potencia_sistema, afundamento, eficiencia
    )

    # Gerar gráfico
    print("\nGerando gráfico de barras seccionadas...")
    plot_grafico_barras_seccionadas(potencia_sistema, afundamento, eficiencia)