import numpy as np
import matplotlib.pyplot as plt
from pysheds.grid import Grid

# 1. Cargamos el grid con nuestro mapa en metros
grid = Grid.from_raster('calbuco_metros.tif')
dem = grid.read_raster('calbuco_metros.tif')

# 2. Rellenamos los sumideros (Sinks) para que el flujo no se corte
dem_filled = grid.fill_pits(dem)

# 3. Resolvemos las zonas planas
dem_depressed = grid.fill_depressions(dem_filled)
dem_no_flats = grid.resolve_flats(dem_depressed)

# 4. Calculamos la dirección de flujo (D8)
# Esto asigna un código a cada píxel según hacia dónde drena
fdir = grid.flowdir(dem_no_flats)

# 5. Calculamos la acumulación de flujo
acc = grid.accumulation(fdir)

# Visualizamos la acumulación para ver las "venas" del volcán
plt.figure(figsize=(10,8))
plt.imshow(np.log1p(acc), cmap='Blues') # Usamos log para resaltar los cauces pequeños
plt.title('Red de Drenaje y Rutas de Lahar - Volcán Calbuco')
plt.colorbar(label='Intensidad de Acumulación')
plt.savefig('rutas_lahar.png')
print("✅ ¡Red de drenaje calculada!")
plt.show()
# Definimos un umbral: solo píxeles que reciban flujo de otros 1000 píxeles
# Esto nos limpia el mapa y deja solo las "carreteras" del lodo
rutas_principales = acc > 1000

# Visualizamos solo las rutas críticas
plt.figure(figsize=(10,8))
plt.imshow(rutas_principales, cmap='Reds') 
plt.title('Rutas Críticas de Lahares (Filtradas)')
plt.savefig('peligro_lahar_limpio.png')
plt.show()