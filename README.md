# Proyecto de Análisis de Siniestros Viales en la Ciudad de Buenos Aires: Análisis de datos para la reducción de víctimas fatales

## Descripción del Problema

Los siniestros viales son una preocupación importante en ciudades como Buenos Aires, con un alto volumen de tráfico y densidad poblacional. Estos incidentes tienen un impacto significativo en la seguridad de los residentes, la infraestructura vial y los servicios de emergencia.

## Tarea a desarrollar: contexto y datos
Este proyecto tiene como objetivo el análisis de datos sobre homicidios en siniestros viales ocurridos en la Ciudad de Buenos Aires durante el período 2016-2021. El análisis busca generar información relevante para que las autoridades locales puedan tomar medidas efectivas para reducir la cantidad de víctimas fatales. El dataset utilizado se encuentra en formato xlsx y contiene dos hojas: "hechos" y "víctimas". Además, se cuenta con un diccionario de datos para facilitar la comprensión de los datos.

Se dispone de datos brutos en la carpeta 'Data_raw', datos transformados en 'Data_transformed', y recursos gráficos en la carpeta 'Recursos_gráficos'. Además, se incluye un diccionario de datos en el archivo 'Diccionario de datos Siniestros viales.xlsx'.

## Tareas Realizadas

### ETL (Extract, Transform, Load)
Se utilizaron principalmente las librerías pandas y, en algunos casos puntuales, Power Query en Power BI.

- Extracción: Los datos se obtuvieron a partir de dos datasets en formato excel.
- Transformación: Se realizaron diversas operaciones de limpieza, filtrado y transformación para preparar los datos para el análisis posterior. Entre las principales tareas se encuentran:

    - Eliminación de datos nulos: Se eliminaron filas completamente nulas a partir de la fila 696.
    - Eliminación de datos duplicados.
    - Manejo de valores faltantes.
    - Conversión de tipos de datos
    - Creación de nuevas variables o características según sea necesario para el análisis.
- Carga: Los datos transformados se cargaron en Power BI para su posterior análisis y la generación de informes

### Análisis Exploratorio de Datos (EDA)
El Análisis Exploratorio de Datos (EDA) es una etapa fundamental en proyectos de análisis de datos.\ 
Se utilizaron principalmente las bibliotecas como pandas, numpy, seaborn y warnings para el análisis.
- Identificación de tendencias y factores relacionados con víctimas fatales en accidentes de tránsito.


### Power BI Dashboard
Se creó un dashboard interactivo ('Análisis_Vial_CABA.pbix') para visualizar KPIs y medidas relevantes.
permite:
- Visualizar la distribución de las víctimas fatales según diferentes variables como sexo, edad, tipo de usuario de la vía, tipo de vehículo involucrado, horario del accidente, entre otras.
- Identificar patrones y tendencias en los datos.
- Explorar relaciones entre las variables.
- Obtener información valiosa para la toma de decisiones por parte de las autoridades locales.

## Archivos del proyecto

- `Data_raw/`: Archivos de datos en bruto.
- `Data_transformed/`: Datos transformados exportados.
- `Recursos_gráficos/`: Imágenes para el diseño del dashboard en Power BI.
- `Análisis_Vial_CABA.pbix`: Dashboard interactivo.
- `Diccionario de datos Siniestros viales.xlsx`: Guía de datos.
- `ETL.ipynb` y `EDA.ipynb`: Notebooks con procesos de ETL y EDA.
- `Funciones.py`: Funciones empleadas en los porcesos de ETL y EDA.

## Bibliotecas Utilizadas

- pandas
- numpy
- seaborn
- warnings

## Resultados Esperados

El proyecto busca proporcionar información valiosa para las autoridades locales y contribuir a la reducción de víctimas fatales en siniestros viales en Buenos Aires, promoviendo así un entorno vial más seguro.
