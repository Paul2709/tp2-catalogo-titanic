# Catálogo de pasajeros del Titanic — Trabajo Práctico 2

**Materia:** Programación Orientada a Datos  
**Modalidad:** Individual  
**Autor:** Paul Chavez Neira  
**Versión de entrega (commit o etiqueta):** `v1.0.0`

## 1. Problema, usuarios y solución

Este proyecto busca facilitar la consulta de un conjunto de datos históricos de pasajeros del Titanic. Trabajar directamente sobre los archivos tabulares dificulta localizar pasajeros, formar grupos y calcular resultados de manera repetible.

La aplicación está destinada a estudiantes y docentes para actividades educativas. Se ejecuta desde la consola de Python y permite buscar pasajeros por identificador, filtrar por clase de pasaje y grupo de edad, calcular resúmenes de supervivencia y exportar resultados. No implementa interfaz web ni modelos predictivos.

## 2. Funcionalidades

* Cargar registros de pasajeros desde un archivo CSV o JSON.
* Validar columnas, identificadores, nombres, billetes, clase, edad y supervivencia.
* Separar pasajeros válidos y registros rechazados, conservando el motivo del rechazo.
* Buscar un pasajero por `PassengerId`.
* Filtrar por clase (`1`, `2`, `3`) y grupo etario (`Menor`, `Adulto`, `Adulto mayor`, `Edad desconocida`).
* Calcular total, sobrevivientes, no sobrevivientes y proporción de supervivencia de la selección.
* Exportar fichas en CSV, resumen en JSON y rechazos en CSV.
* Generar una representación JSON equivalente al CSV original.

La aplicación no descarga automáticamente el dataset: el archivo de entrada se debe colocar en `data/`.

## 3. Procedencia de los datos

* **Dataset:** Titanic Passenger Dataset, equivalente al conjunto de entrenamiento `train.csv` de la competencia educativa de Kaggle.
* **Fuente de referencia:** https://www.kaggle.com/competitions/titanic/data
* **Copia CSV consultada:** https://github.com/datasciencedojo/datasets/blob/master/titanic.csv
* **Publicadores de las páginas de referencia:** Kaggle y DataScienceDojo, respectivamente.
* **Fecha de consulta de las fuentes:** 23 de octubre de 2026.
* **Condiciones:** Kaggle identifica los datos como sujetos a las reglas de la competencia. La disponibilidad pública de una copia en GitHub no equivale por sí sola a una autorización de redistribución. Por prudencia, el CSV original no se incorpora a este repositorio.
* **Unidad de análisis:** una fila representa un pasajero incluido en el conjunto consultado.

El archivo de trabajo contiene **891 observaciones y 12 columnas**; supera el mínimo de referencia del TP. Las seis variables principales utilizadas por la aplicación son:

| Variable | Significado | Reglas principales |
|---|---|---|
|`PassengerId`|Identificador del pasajero|Entero positivo y único entre los registros aceptados|
|`Name`|Nombre|Texto no vacío|
|`Ticket`|Código de billete|Patrón textual con letras, dígitos, espacios, puntos, barras y guiones|
|`Pclass`|Clase del pasaje|1, 2 o 3|
|`Age`|Edad en años|Valor numérico entre 0 y 120 o ausente|
|`Survived`|Supervivencia registrada|0 = no; 1 = sí|

Las otras columnas originales son `Sex`, `SibSp`, `Parch`, `Fare`, `Cabin` y `Embarked`; se conservan durante la lectura y la conversión inicial a JSON, pero no son necesarias para las funciones del catálogo.

En el archivo original, `Age` tiene **177 valores faltantes**. También faltan 687 valores de `Cabin` y 2 de `Embarked`. Los 891 identificadores de pasajero son únicos en la copia utilizada.

Para obtener el archivo de entrada, descargá `titanic.csv` desde el enlace de DataScienceDojo y guardalo como `data/titanic.csv` dentro del proyecto. Alternativamente, obtené `train.csv` desde Kaggle y renombralo a `titanic.csv` para utilizar los comandos de este README.

## 4. Requisitos técnicos y organización

* Python 3.10 o posterior (el desarrollo fue ejecutado con Python 3.14.2 en Windows).
* No se requieren bibliotecas externas: se utiliza la biblioteca estándar (`csv`, `json`, `argparse`, `re`, `pathlib`, `abc`, `unittest`, etc.).
* Los comandos siguientes se ejecutan desde la **raíz del proyecto**, donde están `README.md`, `src/` y `tests/`.

```text
tp2-catalogo-titanic/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── README.md
│   ├── titanic.csv       # Archivo local, excluido de Git
│   └── titanic.json      # Generado localmente, excluido de Git
├── src/
│   ├── main.py          # Interfaz de consola y coordinación
│   ├── fuentes.py       # FuenteDatos, FuenteCSV, FuenteJSON
│   ├── modelos.py       # Clase Pasajero y validaciones
│   ├── pipeline.py      # Preparación, búsquedas, filtros y resumen
│   └── exportacion.py   # Escritura de archivos de salida
├── tests/               # Pruebas unittest
└── outputs/             # Resultados generados localmente
```

La ruta de `data/titanic.csv` es relativa a la carpeta desde la cual se ejecuta Python. Los archivos de `outputs/` se generan al solicitar una exportación y están excluidos del control de versiones mediante `.gitignore`.

## 5. Comandos de uso

En PowerShell o en la terminal de VS Code:

Comprobar Python:

```powershell
python --version
```

Leer el CSV y mostrar el resumen general:

```powershell
python -m src.main --entrada data/titanic.csv
```

Crear un JSON con los mismos registros y volver a leerlo:

```powershell
python -m src.main --entrada data/titanic.csv --exportar-json data/titanic.json
python -m src.main --entrada data/titanic.json
```

Buscar el pasajero con ID 1 y comprobar un ID inexistente:

```powershell
python -m src.main --buscar-id 1
python -m src.main --buscar-id 9999
```

Filtrar pasajeros de primera clase, menores de edad o ambos criterios:

```powershell
python -m src.main --clase 1
python -m src.main --grupo-edad "Menor"
python -m src.main --clase 1 --grupo-edad "Menor"
```

Exportar la selección de primera clase, su resumen y los rechazos:

```powershell
python -m src.main --clase 1 --exportar-fichas outputs/pasajeros.csv --exportar-resumen outputs/resumen.json --exportar-rechazos outputs/rechazados.csv
```

Para ver todas las opciones disponibles:

```powershell
python -m src.main --help
```

`--buscar-id` no puede combinarse con `--clase` ni `--grupo-edad`. Las clases admitidas son 1, 2 y 3; los grupos de edad deben escribirse como aparecen en la ayuda.

## 6. Flujo, normalización y decisiones de limpieza

El procesamiento sigue este orden:

1. **Leer:** seleccionar la fuente CSV o JSON mediante una interfaz común (`FuenteDatos.cargar()`).
2. **Normalizar:** representar los campos como texto o `None`, independientemente del formato de entrada.
3. **Inspeccionar y validar:** comprobar columnas obligatorias; construir objetos `Pasajero` validando los valores relevantes.
4. **Limpiar:** separar registros aceptados de rechazados e identificar duplicados por `PassengerId`.
5. **Analizar:** buscar por ID, aplicar filtros y calcular estadísticas.
6. **Comunicar:** mostrar resultados en la terminal y, cuando se solicita, exportar archivos CSV/JSON.

Reglas principales:

* Un `PassengerId` debe ser entero positivo; una repetición posterior se rechaza.
* `Pclass` solo admite 1, 2 o 3 y `Survived` solo 0 o 1.
* `Name` no puede estar vacío.
* `Ticket` utiliza la expresión regular `[A-Za-z0-9][A-Za-z0-9 ./-]*`. Comprueba formato, no autenticidad histórica; se admiten billetes repetidos entre pasajeros diferentes.
* Una edad faltante se conserva como `None` y se clasifica en `Edad desconocida`; no se reemplaza por cero ni por una media.
* Una edad informada debe ser numérica y pertenecer al rango de 0 a 120 años.
* Los rechazos se identifican con el número del registro, el ID informado y el motivo. La validación del esquema exige la presencia de las columnas obligatorias: si falta una columna en cualquier fila, la ejecución informa un error de estructura en lugar de tratarlo como un simple rechazo individual.

Los contadores iniciales de inspección describen **los registros originales**, antes de descartar los inválidos. Los resúmenes de supervivencia se calculan sobre **los pasajeros válidos seleccionados**. En la copia original usada para el TP, los 891 registros pasan las validaciones y no hay rechazos.

## 7. Ejemplo de resultados e interpretación

Con el CSV original, el programa muestra:

```text
Observaciones: 891
Edades faltantes: 177
ID duplicados: 0
Sobrevivientes registrados: 342
Pasajeros validos: 891
Registros rechazados: 0

RESUMEN DE SUPERVIVENCIA
Total: 891
Sobrevivientes: 342
No sobrevivientes: 549
Supervivencia: 38.38%
```

Al filtrar por `--clase 1`:

```text
RESUMEN DE SUPERVIVENCIA
Total: 216
Sobrevivientes: 136
No sobrevivientes: 80
Supervivencia: 62.96%
```

El 62,96 % es la proporción de supervivientes dentro del subconjunto de primera clase **incluido en este dataset**: `136 / 216 × 100`. No es una predicción ni demuestra relaciones causales.

Los archivos exportados son:

* `outputs/pasajeros.csv`: una ficha por pasajero seleccionado; para la consulta de primera clase, 216 filas de datos.
* `outputs/resumen.json`: `total`, `sobrevivientes`, `no_sobrevivientes` y `proporcion_supervivencia` (valor entre 0 y 1 o `null` si el grupo está vacío).
* `outputs/rechazados.csv`: encabezados `registro,identificador,motivo` y los errores detectados; en la copia original solo contiene encabezados porque no hay rechazos.

Si el grupo está vacío, la proporción se considera **no disponible**, no 0 %.

## 8. Pruebas y reproducibilidad

Desde la raíz del proyecto:

```powershell
python -m unittest discover -s tests -v
```

En la versión de desarrollo verificada se ejecutaron 39 pruebas, que cubren lectura de archivos, equivalencia CSV/JSON en muestras, casos normales, estructuras inválidas, validaciones del modelo, duplicados, filtros, grupos vacíos, conservación de cantidades y exportaciones.

La igualdad de entrada y parámetros permite repetir el procesamiento con resultados coherentes. Para comprobar el dataset original, ejecutá los comandos del apartado 5; si cambiás los archivos de entrada o las reglas del programa, pueden variar los resultados.

## 9. Limitaciones y alcance

* El conjunto de 891 pasajeros no representa el manifiesto completo del Titanic.
* Existen edades faltantes; las estadísticas por edad excluyen esos registros de los grupos con edad conocida, pero están disponibles en `Edad desconocida`.
* La validación de billetes confirma una estructura de caracteres, no si el billete fue auténtico.
* Los porcentajes son descriptivos del conjunto seleccionado; no permiten concluir causalidad.
* La primera versión no implementa interfaz gráfica, actualización automática, base de datos remota ni aprendizaje automático.
* El manejo de un CSV con columnas obligatorias ausentes se realiza como error estructural, no como rechazo por fila.

## 10. Git, entrega y defensa

El proyecto se desarrolló mediante commits significativos de Git. El repositorio debe seguir accesible para la cátedra (si es privado, otorgar acceso a los evaluadores).

**Repositorio:** https://github.com/Paul2709/tp2-catalogo-titanic  
**Commit de mejoras, validaciones y documentación:** `ecc648c`  
**Versión definitiva de entrega:** `v1.0.0`

En la defensa se demostrará una consulta por ID, un filtro, el resumen de supervivencia, la exportación y la ejecución de las pruebas. También se explicarán la clase `Pasajero`, las fuentes `FuenteCSV`/`FuenteJSON`, la expresión regular y el tratamiento de faltantes y duplicados.

