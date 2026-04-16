import numpy as np
import matplotlib.pyplot as plt


T = [0, 25, 50, 75]  # Temperaturas em °C
G = [200, 400, 600, 800, 1000]  # Irradiações
nms = 10 # numero de módulos em série
nmp = 10 # número de módulos em paralelo
ai = 0.318 / 100  # Coeficiente de temperatura da corrente
av = -0.34 / 100  # Coeficiente de temperatura da tensão
Isc_r = 8.21*nmp
Voc_r = 32.9*nms

Ns = 54
n = 1.3

Gr = 1000
Tr = 25 + 273.6

q = 1.60217646e-19
K = 1.3806503e-23
Eg = 1.12

Rs = 0.221
Rp = 415.405

# Loop para cada temperatura
for temp in T:

    T_k = temp + 273.6
    dT = T_k - Tr

    Isc = Isc_r + ai * dT
    Voc = Voc_r + av * dT

    Vt = (Ns * n * K * T_k) / q

    # Criar figuras para cada temperatura
    plt.figure(figsize=(10, 4))

    # Subplot I-V
    plt.subplot(1, 2, 1)

    for irradiance in G:
        Iph = Isc * (irradiance / Gr)

        Iss = Isc / (np.exp(Voc / Vt) - 1)
        Is = Iss * ((T_k / Tr) ** 3) * np.exp(((q * Eg) / (n * K)) * ((1 / Tr) - (1 / T_k)))

        V = np.arange(0, Voc + Voc / 75, Voc / 1000)
        Ipv = np.zeros(len(V))

        for i in range(len(V)):
            I = Iph

            for _ in range(20):
                Vd = V[i] + Rs * I
                Id = Is * (np.exp(Vd / Vt) - 1)
                Ip = Vd / Rp

                f = Iph - I - Id - Ip
                df = -1 - (Is * Rs / Vt) * np.exp(Vd / Vt) - (Rs / Rp)

                I = I - f / df

            Ipv[i] = max(I, 0)

        plt.plot(V, Ipv, label=f'G={irradiance} W/m²')

        # Subplot P-V
        plt.subplot(1, 2, 2)
        P = V * Ipv
        plt.plot(V, P, label=f'G={irradiance} W/m²')
        plt.subplot(1, 2, 1)

    # Configuração I-V
    plt.title(f'I-V (T={temp}°C)')
    plt.xlabel('Tensão (V)')
    plt.ylabel('Corrente (A)')
    plt.grid(True)
    plt.legend()

    # Configuração P-V
    plt.subplot(1, 2, 2)
    plt.title(f'P-V (T={temp}°C)')
    plt.xlabel('Tensão (V)')
    plt.ylabel('Potência (W)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()

plt.show()