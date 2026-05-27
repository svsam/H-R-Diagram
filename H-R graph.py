import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('gaia_hr_data_1million.csv')

plt.scatter(
    df['surface_temperature_K'],
    df['luminosity_L_sun'],
    s=1,
    alpha=0.2,
)

plt.xlabel('Temperature (K)')
plt.gca().invert_xaxis()

plt.ylabel('Luminosity (L_sun)')
plt.yscale('log')

plt.title('H-R Diagram from Gaia Data')
plt.show()
