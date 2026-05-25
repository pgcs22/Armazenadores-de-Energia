import numpy as np
import matplotlib.pyplot as plt

I = 0.0285 # [kgm2]
passo = 1 # [s]
N = round(3000/passo)+1

# inicialização das variáveis
rpm = np.linspace(0, 3000, N)
E = np.zeros(N)
w = np.zeros(N)

# Simulação
for n in range(1, N):
    w[n] = rpm[n]*2*np.pi/60
    E[n] = I * w[n]**2 * 0.5 / (60*60)

# desenho dos gráficos
plt.figure(figsize=(10, 6))
plt.plot(rpm, E, 'b-', linewidth=1.5)
plt.xlabel('Velocidade angular (rpm)', fontsize=12)
plt.ylabel('Energia (Wh)', fontsize=12)
plt.title('Energia Armazenada', fontsize=14)
plt.grid(alpha=0.3)
plt.xlim(0, 3000)
plt.show()