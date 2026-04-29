import rasterio
import numpy as np
import matplotlib.pyplot as plt

# 1. Abrimos el mapa en metros
with rasterio.open("calbuco_metros.tif") as src:
    res = src.res[0]  # Tamaño del píxel en metros (aprox 30m)
    data = src.read(1).astype(float)
    
    # 2. Calculamos los gradientes (cambio de altura / distancia)
    # np.gradient nos da la derivada en y (filas) y x (columnas)
    gy, gx = np.gradient(data, res)
    
    # 3. Calculamos la pendiente (slope)
    # Pendiente = arctan( raíz(gx^2 + gy^2) )
    slope = np.arctan(np.sqrt(gx**2 + gy**2))
    
    # Convertimos de radianes a grados para que sea fácil de leer
    slope_deg = np.degrees(slope)

# 4. Visualizamos
plt.figure(figsize=(10, 8))
plt.imshow(slope_deg, cmap='magma')
plt.colorbar(label='Pendiente (grados °)')
plt.title('Pendiente del Volcán Calbuco (Calculado con NumPy)')
plt.savefig('pendiente_numpy.png')
print(f"✅ ¡Pendiente calculada! Máxima inclinación: {np.max(slope_deg):.2f}°")
plt.show()