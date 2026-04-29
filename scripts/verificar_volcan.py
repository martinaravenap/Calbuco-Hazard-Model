import rasterio

# Abrimos el archivo del Calbuco
with rasterio.open("output_SRTMGL1.tif") as dataset:
    print(f"Número de bandas: {dataset.count}")
    print(f"Ancho: {dataset.width} píxeles")
    print(f"Alto: {dataset.height} píxeles")
    print(f"Sistema de coordenadas (CRS): {dataset.crs}")