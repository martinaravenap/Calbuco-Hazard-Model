<p align="center">
  <img src="outputs/banner.jpg" width="100%" alt="Banner Proyecto Calbuco">


###  Simulación de Flujo de Lahar
<p align="center">
  <img src="outputs/simulacion.gif" width="80%" alt="Simulación Volcán Calbuco">
</p>

### 💻 Implementación en VS Code
<p align="center">
  <img src="outputs/vscode.gif" width="100%" alt="Demostración de código en VS Code">
</p>


# Modelamiento Geoespacial de Riesgo por Lahares: Volcán Calbuco
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Status](https://img.shields.io/badge/Status-Finalizado-green.svg)
![Area](https://img.shields.io/badge/Análisis-Geomorfológico-orange.svg)

##  Descripción del Proyecto
Este proyecto presenta un sistema automatizado en **Python** para la delimitación de zonas de peligro ante flujos de detritos (lahares) en el Volcán Calbuco, Región de Los Lagos, Chile. 

A diferencia de los mapas de riesgo tradicionales, este modelo no solo analiza la pendiente, sino que integra variables dinámicas de **acumulación de masa** y **resistencia física del terreno**, permitiendo identificar con alta precisión las rutas críticas de evacuación y la infraestructura vulnerable (como la localidad de Ensenada).

##  Características Principales
- **Automatización Completa**: El flujo de trabajo procesa desde el ráster de elevación (DEM) bruto hasta el mapa interactivo final, permite la reutilizacion de este mismo modelo para utilizarlo en diferentes contextos, para hacerlo solo es necesario modifiar el archivo.tif.
- **Física Aplicada**: Implementación de la Ecuación de Manning para modelar la fricción superficial.
- **Visor Interactivo**: Generación de un visor geográfico en formato HTML para la toma de decisiones dinámica.

##  Metodología Fisica

### 1. Procesamiento Hidrológico
Se utilizó un Modelo Digital de Elevación (DEM) de 12.5m de resolución. El proceso incluyó:
- **Depresión de Sumideros (Sink Filling)**: Eliminación de imperfecciones topográficas para asegurar un flujo continuo.
- **Cálculo de Flujo**: Determinación de la dirección de drenaje y acumulación acumulada para identificar los ejes de los lahares.

### 2. Integración de la Rugosidad de Manning ($n$)
Para dar realismo físico, se asignaron coeficientes de fricción basados en la geomorfología:
- **Zonas Altas ($n=0.03$)**: Flujo rápido sobre roca desnuda.
- **Zonas Medias ($n=0.05$)**: Resistencia moderada por matorrales y depósitos antiguos.
- **Zonas Bajas ($n=0.10$)**: Alta resistencia por bosque nativo y llanuras aluviales.

### 3. Índice Combinado de Peligro (ICP)
El riesgo se calculó mediante la integración de la energía cinética (pendiente) y la masa potencial (acumulación), normalizada por el coeficiente de resistencia.

##  Resultados Técnicos
- **Zonificación de Riesgo Extremo**: Se delimitaron **3.03 km²** de afectación crítica inmediata.
- **Validación Territorial**: El modelo identifica con éxito las quebradas naturales que desembocan hacia el Lago Llanquihue, amenazando rutas de conectividad regional.

##  Stack Tecnológico
- **Análisis de Datos**: `Numpy`, `Rasterio`
- **Modelado Hidrológico**: `Pysheds`
- **Visualización Cartográfica**: `Matplotlib`, `Folium` (Mapas base de ESRI World Imagery y OpenStreetMap).

##  Estructura del Repositorio
```text
├── data/               # Modelos Digitales de Elevación (.tif)
├── scripts/            # Código fuente en Python
├── output/             # Mapas generados (PNG/HTML)
└── requirements.txt    # Librerías necesarias para replicar el estudio