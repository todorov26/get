import numpy as np
import matplotlib.pyplot as plt

FILENAME = 'data.csv'

data = np.loadtxt(FILENAME, delimiter=',', encoding='utf-8')
time = data[:, 0].astype(float)
voltage = data[:, 1].astype(float)

U_inf = 4.473  
U_0   = 0.426   

y = np.log((U_inf - voltage) / (U_inf - U_0))

k, b = np.polyfit(time, y, 1)        
tau = -1 / k
r2 = 1 - np.sum((y - (k*time + b))**2) / np.sum((y - y.mean())**2)

print(f'Наклон k = {k:.6f} с^-1')
print(f'Пересечение b = {b:.4f}')
print(f'tau = {tau:.3f} с')
print(f'R^2 = {r2:.5f}')

t_s, y_s = time[::10], y[::10]
plt.figure(figsize=(10, 6))
plt.plot(t_s, y_s, '.', ms=2, color='tab:blue', label='Эксперимент')
t_fit = np.linspace(0, time.max(), 100)
plt.plot(t_fit, k*t_fit + b, 'r-', lw=2,
         label=f'МНК: k = {k:.4f} с$^{{-1}}$, $\\tau$ = {tau:.2f} с')
plt.xlabel('Время t, с')
plt.ylabel(r'$\ln\,\dfrac{U_\infty - U}{U_\infty - U_0}$')
plt.title('Линеаризованная кривая заряда RC-цепи')
plt.legend()
plt.grid(alpha=0.4)
plt.tight_layout()
plt.savefig('plot-linear.png', dpi=300)
plt.show()
