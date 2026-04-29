import rasterio
from matplotlib import pyplot as plt

# Abrimos el archivo
with rasterio.open("output_SRTMGL1.tif") as src:
    # Leemos la primera banda (elevación)
    raster_data = src.read(1)
    
    # Creamos la figura
    plt.figure(figsize=(10, 8))
    
    # Mostramos los datos con un mapa de color 'terrain' (ideal para relieve)
    img = plt.imshow(raster_data, cmap='terrain')
    
    # Añadimos una barra de colores para saber qué altura representa cada color
    plt.colorbar(img, label='Elevación (metros)')
    
    plt.title('Relieve del Volcán Calbuco')
    plt.xlabel('Píxeles (Ancho)')
    plt.ylabel('Píxeles (Alto)')
    
    # Guardamos la imagen para poder verla
    plt.savefig('mapa_calbuco.png')
    print("¡Imagen guardada como mapa_calbuco.png!")
    
    # Intentamos mostrarla en pantalla
    plt.show()