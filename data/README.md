# Datos del Titanic

El archivo original `titanic.csv` debe guardarse en esta carpeta.

- Fuente de referencia: https://www.kaggle.com/competitions/titanic/data
- Copia de consulta: https://github.com/datasciencedojo/datasets/blob/master/titanic.csv
- Unidad de analisis: un pasajero por fila.
- El archivo usado para desarrollar la aplicacion contiene 891 observaciones.
- Los nombres de las 12 columnas siguen el CSV de esa fuente.
- La variable `Age` contiene 177 valores faltantes.

Los archivos `titanic.csv` y `titanic.json` estan excluidos de Git por ahora,
para evitar redistribuir el dataset sin verificar antes sus condiciones de uso.

## Generar el JSON equivalente

Desde la carpeta principal del proyecto, ejecutar:

```bash
python -m src.main --entrada data/titanic.csv --exportar-json data/titanic.json
```

La transformacion conserva los nombres de los campos y convierte las celdas
vacias en valores `null` en JSON. Los demas valores se representan como texto,
y las futuras validaciones de dominio convertiran tipos segun corresponda.
