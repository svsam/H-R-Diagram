import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('gaia_hr_data_1million.csv')

L = df['luminosity_L_sun']
T = df['surface_temperature_K']

fig, ax = plt.subplots(figsize=(10, 7))

fig.patch.set_facecolor('black')
ax.set_facecolor('black')

ax.scatter(
    T,
    L,
    color='white',
    s=0.8,
    alpha=0.6,
    edgecolors='none',
    rasterized=True,
)

ax.set_xlabel('Surface Temperature (K)', color='white')
ax.invert_xaxis()
ax.set_ylabel('Luminosity ($L_\\odot$)', color='white')
ax.set_yscale('log')
ax.set_title('Hertzsprung-Russell Diagram', color='white')

ax.tick_params(colors='white')

plt.show()