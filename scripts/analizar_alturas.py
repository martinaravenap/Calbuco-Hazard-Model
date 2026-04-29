import rasterio
import numpy as np

with rasterio.open("output_SRTMGL1.tif") as src:
    raster_data = src.read(1)
    
    # Encontramos el valor máximo (cima) y mínimo (base/mar)
    max_alt = np.max(raster_data)
    min_alt = np.min(raster_data)
    promedio_alt = np.mean(raster_data)

    print(f"🏔️ Altura máxima detectada: {max_alt} metros")
    print(f"📉 Altura mínima detectada: {min_alt} metros")
    print(f"📊 Altura promedio del área: {promedio_alt:.2f} metros")