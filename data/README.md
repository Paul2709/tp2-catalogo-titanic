# Datos del Titanic

## 1. Descripción del dataset

Este directorio contiene los archivos de datos utilizados por la aplicación Catálogo de pasajeros del Titanic, desarrollada para el Trabajo Práctico 2 de Programación Orientada a Datos.

El conjunto de datos contiene 891 observaciones y 12 variables. Cada fila representa un pasajero del Titanic.

## 2. Procedencia de los datos

* **Nombre:** Titanic Passenger Dataset.
* **Fuente de referencia:** https://www.kaggle.com/competitions/titanic/data
* **Copia CSV consultada:** https://github.com/datasciencedojo/datasets/blob/master/titanic.csv
* **Fecha de consulta:** 23 de octubre de 2026.
* **Unidad de análisis:** pasajero incluido en el conjunto de datos.

El archivo se utiliza con fines educativos. Su disponibilidad pública no implica automáticamente autorización para redistribuirlo.

## 3. Variables utilizadas

La aplicación utiliza principalmente las siguientes variables:

|Variable|Descripción|
|-|-|
|PassengerId|Identificador del pasajero|
|Name|Nombre del pasajero|
|Ticket|Código o número de billete|
|Pclass|Clase de viaje (1, 2 o 3)|
|Age|Edad del pasajero|
|Survived|Supervivencia (0 = no; 1 = sí)|

## 4. Calidad y valores faltantes

El conjunto de datos original presenta:

* 891 pasajeros.
* 177 valores faltantes en Age.
* 687 valores faltantes en Cabin.
* 2 valores faltantes en Embarked.
* Ningún identificador PassengerId duplicado.

Los pasajeros con edad faltante se conservan y se clasifican en el grupo Edad desconocida.

## 5. Archivos utilizados

* **titanic.csv:** archivo original descargado.
* **titanic.json:** representación JSON generada a partir del CSV.

Ambos archivos se mantienen localmente y están excluidos del repositorio Git mediante `.gitignore`.

## 6. Cómo obtener los datos

Descargar `titanic.csv` desde el repositorio de DataScienceDojo e incorporarlo a esta carpeta con el nombre `titanic.csv`.

Alternativamente, descargar `train.csv` desde Kaggle y renombrarlo a `titanic.csv`.

## 7. Generar el archivo JSON

Desde la carpeta principal del proyecto, ejecutar:

```powershell
python -m src.main --entrada data/titanic.csv --exportar-json data/titanic.json
```

Este procedimiento genera una representación JSON equivalente de los registros originales.

Durante la normalización, los campos vacíos se representan como `None` en Python y `null` en JSON. Las validaciones posteriores convierten los campos necesarios a los tipos correspondientes.

## 8. Limitaciones

El dataset de 891 pasajeros no representa a todas las personas que viajaban en el Titanic.

Los datos faltantes pueden afectar determinados análisis. Los resultados generados son descriptivos y no deben interpretarse como predicciones ni como evidencia de causalidad.

