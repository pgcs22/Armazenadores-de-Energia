import numpy as np
import matplotlib.pyplot as plt

# Definição das variáveis de entrada
Vv = [5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5]  # [m/s]
P_nominal = 1.5E6  # [W]
R = 37.5  # [m]
Beta = [0, 5, 10, 15, 20, 25, 30]  # [Graus]
Dar = 1.3  # [kg/m^3]

# Cálculo das constantes
A = np.pi * (R ** 2)

# Inicialização das variáveis
rpm = np.linspace(0, 30, 1000)  # velocidade de rotação em rpm
W = rpm * (2 * np.pi / 60)  # conversão de rpm para rad/s

# Criar matrizes para armazenar resultados
Cp = np.zeros((len(Beta), len(Vv), len(W)))  # [Beta, Vv, W]
P = np.zeros((len(Beta), len(Vv), len(W)))  # [Beta, Vv, W]

# Simulação
for i_beta, beta in enumerate(Beta):
    for i_vv, vv in enumerate(Vv):
        for i_w, w in enumerate(W):
            if w == 0 or vv == 0:
                Cp[i_beta, i_vv, i_w] = 0
                P[i_beta, i_vv, i_w] = 0
                continue

            L = w * R / vv

            # Cálculo de Li
            Li = 1 / (1 / (L + 0.08 * beta) - 0.035 / (beta**3 +1))

            # Cálculo do coeficiente de potência Cp
            Cp_calc = 0.22 * (116 / Li - 0.4 * beta - 5) * np.exp(-12.5 / Li)

            # Garantir que Cp não seja negativo
            Cp[i_beta, i_vv, i_w] = max(0, Cp_calc)

            # Cálculo da potência
            P[i_beta, i_vv, i_w] = 0.5 * Dar * A * (vv ** 3) * Cp[i_beta, i_vv, i_w]

# Loop para cada ângulo beta
for i_beta, beta in enumerate(Beta):

    rpm_otimo = []
    P_max_vento = []
    Vv_para_plot = []

    for i_vv, vv in enumerate(Vv):

        P_vento = P[i_beta, i_vv, :]
        P_max = np.max(P_vento)

        if P_max > 0:  #
            idx_max = np.argmax(P_vento)
            rpm_otimo_vento = rpm[idx_max]

            P_max_limitado = min(P_max, P_nominal)

            rpm_otimo.append(rpm_otimo_vento)
            P_max_vento.append(P_max_limitado)
            Vv_para_plot.append(vv)

    rpm_otimo = np.array(rpm_otimo)
    P_max_vento = np.array(P_max_vento)
    Vv_para_plot = np.array(Vv_para_plot)

    # Adicionar ponto zero no início da curva de máxima potência
    rpm_otimo_com_zero = np.insert(rpm_otimo, 0, 0)
    P_max_vento_com_zero = np.insert(P_max_vento, 0, 0)

    ordem = np.argsort(rpm_otimo_com_zero)
    rpm_otimo_ordenado = rpm_otimo_com_zero[ordem]
    P_max_vento_ordenado = P_max_vento_com_zero[ordem]

    plt.figure(figsize=(12, 8))

    # Plotar curvas para cada velocidade de vento
    for i_vv, vv in enumerate(Vv):
        mask = P[i_beta, i_vv, :] > 0
        rpm_valid = rpm[mask]
        P_valid = P[i_beta, i_vv, :][mask]

        if len(rpm_valid) > 0:
            plt.plot(rpm_valid, P_valid,
                     label=f'Vv = {vv} m/s', linewidth=1.0, alpha=0.6)

    # Plotar curva de máxima potência (MPP) conectando os pontos de pico
    plt.plot(rpm_otimo_ordenado, P_max_vento_ordenado, 'r-', linewidth=2.5,
             label='MPP (Máxima Potência)', marker='o', markersize=6,
             markeredgecolor='red', markerfacecolor='white', markeredgewidth=2)

    # Adicionar linha da potência nominal
    plt.axhline(y=P_nominal, color='blue', linestyle=':', linewidth=1.5,
                label=f'Potência Nominal = {P_nominal / 1e6:.1f} MW')

    # Adicionar ponto onde atinge a potência nominal
    rpm_nominal = None
    for i, P_val in enumerate(P_max_vento_ordenado):
        if P_val >= P_nominal:
            rpm_nominal = rpm_otimo_ordenado[i]
            break

    if rpm_nominal is not None:
        plt.plot(rpm_nominal, P_nominal, 'bo', markersize=8,
                 label=f'Início limitação: {rpm_nominal:.1f} rpm')

    plt.xlabel('Velocidade de rotação (rpm)', fontsize=12)
    plt.ylabel('Potência (W)', fontsize=12)
    plt.title(f'Curvas de Potência da Turbina - Ângulo de ataque β = {beta}°', fontsize=14)
    plt.grid(alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    plt.xlim(0, 30)
    plt.ylim(0, 5000000)
    plt.tight_layout()

    # Salvar a figura

    plt.show()