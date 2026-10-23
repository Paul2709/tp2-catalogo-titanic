# Catalogo de pasajeros del Titanic — TP2

**Materia:** Programacion Orientada a Datos  
**Autor/a:** completar antes de entregar  
**Estado:** avance inicial, NO es la version final del trabajo practico.

## 1. Problema

Consultar individualmente un conjunto de registros historicos y calcular
resumenes por grupos puede resultar poco practico al trabajar directamente
con archivos tabulares.

## 2. Objetivo y usuarios

Se desarrollara una aplicacion de consola, dirigida a estudiantes y docentes,
para buscar pasajeros, filtrar por clase y grupo etario, obtener estadisticas
de supervivencia y exportar fichas. Por ahora, el programa solamente carga e
inspecciona datos.

## 3. Requisitos

- Python 3.10 o posterior.
- No se requieren paquetes externos en este primer avance.
- El archivo `data/titanic.csv` debe estar presente de forma local.

## 4. Instalar y ejecutar

Abrir la carpeta **tp2-catalogo-titanic** en VS Code y abrir una terminal
ubicada en la raiz del proyecto (donde se encuentra este README).

Comprobar Python:

```bash
python --version
```

Leer el archivo CSV:

```bash
python -m src.main --entrada data/titanic.csv
```

Convertir los mismos registros a JSON:

```bash
python -m src.main --entrada data/titanic.csv --exportar-json data/titanic.json
```

Leer el JSON convertido:

```bash
python -m src.main --entrada data/titanic.json
```

En Windows, si `python` no funciona pero el lanzador de Python si esta
instalado, sustituir `python` por `py`.

## 5. Ejecutar las pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas usan datos inventados y pequenos; no dependen del CSV real.

## 6. Organizacion

- `src/main.py`: entrada de consola y presentacion del resumen inicial.
- `src/fuentes.py`: interfaz `FuenteDatos`, implementaciones `FuenteCSV` y
  `FuenteJSON`, y exportacion de JSON.
- `src/pipeline.py`: comprobacion del esquema e inspeccion inicial.
- `src/modelos.py`: reservada para `Pasajero` en un avance posterior.
- `tests/`: verificaciones automatizadas de lectura e inspeccion.
- `data/`: datos de trabajo, excluidos del repositorio hasta revisar licencias.
- `outputs/`: carpeta para futuras exportaciones.

## 7. Ejemplo de resultado

Con `data/titanic.csv` (891 observaciones) el resumen esperado es:

```text
Observaciones: 891
Edades faltantes: 177
ID duplicados: 0
Sobrevivientes registrados: 342
```

## 8. Fuente, unidad de analisis y condiciones

- Fuente de referencia: https://www.kaggle.com/competitions/titanic/data
- Copia consultada: https://github.com/datasciencedojo/datasets/blob/master/titanic.csv
- Unidad de analisis: pasajero incluido en el archivo.
- Variables principales: `PassengerId`, `Name`, `Ticket`, `Pclass`, `Age`, `Survived`.
- El archivo original tiene 12 columnas y 891 filas.
- Falta confirmar las condiciones de redistribucion del CSV antes de publicarlo.

## 9. Limpieza, resultados y limitaciones

Por ahora, la lectura representa vacios como `None`, valida la presencia de
columnas y calcula estadisticas exploratorias. **Todavia no** se implementaron
las reglas de rechazo, la validacion integral, el catalogo ni los filtros.
Los futuros resultados describiran este dataset de 891 personas y no deben
interpretarse como una estimacion causal de la supervivencia.

## 10. Proximas tareas

1. Implementar clase `Pasajero` y reglas de validacion de campos.
2. Registrar registros aceptados y rechazados con motivo.
3. Implementar indice, busquedas, filtros y resumenes por grupos de edad.
4. Exportar fichas y resultados.
5. Completar pruebas, interpretar salidas y preparar defensa individual.

## 11. Version para entrega

Anotar el commit o etiqueta final una vez terminado el trabajo. El proyecto
necesita al menos cinco commits reales y significativos durante su desarrollo.
