import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

# Definimos el destino: UTM Zona 18S (EPSG:32718)
dst_crs = 'EPSG:32718'

with rasterio.open('output_SRTMGL1.tif') as src:
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds)
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height
    })

    with rasterio.open('calbuco_metros.tif', 'w', **kwargs) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest)

print("✅ ¡Mapa convertido a metros exitosamente!")