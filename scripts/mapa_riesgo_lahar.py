import numpy as np
import matplotlib.pyplot as plt
from pysheds.grid import Grid
import folium
from matplotlib.colors import ListedColormap

# ==========================================
# 1. CARGA Y PROCESAMIENTO HIDROLÓGICO
# ==========================================
# Asegúrate de que 'calbuco_metros.tif' esté en la misma carpeta
grid = Grid.from_raster('calbuco_metros.tif')
dem = grid.read_raster('calbuco_metros.tif')

# Limpieza del terreno para asegurar flujo continuo
dem_f = grid.resolve_flats(grid.fill_depressions(grid.fill_pits(dem)))

# Cálculo de dirección de flujo y acumulación
fdir = grid.flowdir(dem_f)
acc = grid.accumulation(fdir)

# Cálculo de pendiente en grados (asumiendo resolución de 12.5m)
dy, dx = np.gradient(dem_f, 12.5)
slope = np.arctan(np.sqrt(dx**2 + dy**2)) * (180 / np.pi)

# ==========================================
# 2. REFINAMIENTO FÍSICO Y RIESGO
# ==========================================
# Filtrado de cauces: solo mostramos donde el flujo es significativo
acc_mask = acc > 500 
acc_log = np.log1p(acc)
acc_n = (acc_log - acc_log[acc_mask].min()) / (acc_log.max() - acc_log[acc_mask].min())
acc_n = np.where(acc_mask, acc_n, 0)

# Normalización de pendiente con corrección de contraste (gamma)
slope_n = (slope / slope.max()) ** 0.5

# Lógica de Rugosidad de Manning (Fricción)
# Pendientes altas = liso (0.03), Pendientes bajas/bosque = mucha fricción (0.10)
n_manning = np.where(slope > 25, 0.03, 
             np.where(slope >= 10, 0.05, 0.10))

# FÓRMULA FINAL: Riesgo = (Masa * Energía) / Fricción
riesgo = (acc_n * slope_n) / n_manning

# ==========================================
# 3. ZONIFICACIÓN Y ESTADÍSTICAS
# ==========================================
condiciones = [
    (riesgo >= 0.4),                          # Extremo
    (riesgo >= 0.2) & (riesgo < 0.4),         # Alto
    (riesgo >= 0.05) & (riesgo < 0.2),        # Medio
    (riesgo < 0.05) & (riesgo > 0)            # Bajo
]
valores = [4, 3, 2, 1] 
zonificacion = np.select(condiciones, valores, default=0)

# Cálculo de área afectada en riesgo extremo
num_pixeles_riesgo = np.sum(riesgo > 0.4)
area_total_km2 = (num_pixeles_riesgo * (12.5 * 12.5)) / 1e6

print("-" * 50)
print(f"RESUMEN TÉCNICO - VOLCÁN CALBUCO")
print(f"⚠️ Áreas de Riesgo Extremo: {area_total_km2:.2f} km²")
print("-" * 50)

# ==========================================
# 4. VISUALIZACIÓN 1: INFORME GRÁFICO (PNG)
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

# Panel 1: Sombreado 3D e Índice de Peligro
ls = plt.matplotlib.colors.LightSource(azdeg=315, altdeg=45)
hillshade = ls.hillshade(dem_f, vert_exag=1)
ax1.imshow(hillshade, cmap='gray')
im1 = ax1.imshow(riesgo, cmap='inferno', vmin=0.01, vmax=0.6, alpha=0.7)
ax1.set_title('Índice Combinado de Peligro (Físico)')
plt.colorbar(im1, ax=ax1, label='Fuerza del Lahar')

# Panel 2: Mapa de Zonificación de Emergencia
cmap_riesgo = ListedColormap(['black', 'green', 'yellow', 'orange', 'red'])
im2 = ax2.imshow(zonificacion, cmap=cmap_riesgo)
ax2.set_title('Zonificación para Protección Civil')
cbar2 = plt.colorbar(im2, ax=ax2, ticks=[0, 1, 2, 3, 4])
cbar2.ax.set_yticklabels(['Sin Riesgo', 'Bajo', 'Medio', 'Alto', 'Extremo'])

plt.tight_layout()
plt.savefig('informe_riesgo_calbuco.png', dpi=300)

# ==========================================
# ==========================================
# 5. VISUALIZACIÓN 2: MAPA INTERACTIVO PRO (HTML)
# ==========================================
import folium
from folium import plugins

# Convertimos a matriz NumPy para evitar el error anterior
riesgo_np = np.asarray(riesgo)

# Coordenadas del Calbuco
lat_centro, lon_centro = -41.33, -72.61
mapa_final = folium.Map(location=[lat_centro, lon_centro], zoom_start=12)

# --- AÑADIMOS VARIOS MAPAS BASE ---
folium.TileLayer('OpenStreetMap', name='Mapa de Calles').add_to(mapa_final)
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Vista Satelital'
).add_to(mapa_final)

# --- CAPA DE RIESGO CON COLORES FUERTES ---
# Solo pintamos donde el riesgo es real (>0.05) para no tapar todo el mapa
capa_riesgo = folium.raster_layers.ImageOverlay(
    image=riesgo_np,
    bounds=[[-41.45, -72.8], [-41.2, -72.4]], 
    colormap=lambda x: (1, 0, 0, 0.8) if x > 0.4 else (1, 0.5, 0, 0.7) if x > 0.1 else (0,0,0,0),
    name="Zonas de Peligro (Lahar)",
    opacity=0.7,
    interactive=True
)
capa_riesgo.add_to(mapa_final)

# --- HERRAMIENTAS DE INTERACTIVIDAD ---
# 1. Control de Capas: Permite al usuario elegir qué ver
folium.LayerControl(collapsed=False).add_to(mapa_final)

# 2. Pantalla Completa
plugins.Fullscreen().add_to(mapa_final)

# 3. MiniMapa de referencia
plugins.MiniMap(toggle_display=True).add_to(mapa_final)

# Guardamos el archivo
mapa_final.save("PROYECTO_FINAL_CALBUCO.html")

print("🚀 ¡Ahora sí! Abre 'PROYECTO_FINAL_CALBUCO.html' y usa el panel de arriba a la derecha.")
mapa_final.save("PROYECTO_FINAL_CALBUCO.html")

print("✅ ¡Éxito! Archivo 'PROYECTO_FINAL_CALBUCO.html' generado correctamente.")
print("1. 'informe_riesgo_calbuco.png' (Mapa técnico para impresión)")
print("2. 'PROYECTO_FINAL_CALBUCO.html' (Mapa interactivo para navegador)")

plt.show()