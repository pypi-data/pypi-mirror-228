# HPrIm
---------------

Esta es una Heramienta para el Procesamiento de Imágnes (HPrIm) provee funciones que son utilizadas en el procesamiento de imágenes, como la ecualización o expansión de un histograma para mejorar el contraste y tecnicás algo más avanzadas como la aplicación de filtros laplaciono, sobel y mediana.

## Uso
Esta librería proporciona filtrado para agudizamiento y el suavizado de imágenes. Para esto se puede usar la clase `Filtro` que implementa todos los métodos para cualquier filtrado.

```python
from HPrIm import Filtro, MascaraLaplaciana

matriz = [
    [4, 4, 3, 2],
    [7, 7, 6, 6],
    [4, 1, 2, 3],
    [2, 5, 1, 2],
]

filtro = Filtro(matriz)
filtro.laplaciano(MascaraLaplaciana.F4)
print(filtro)
```
Por otra parte puedes hacer uso de la clase individual si quieres un poco más de control

```python
from HPrIm import FLaplaciano, MascaraLaplaciana
matriz = [
    [4, 4, 3, 2],
    [7, 7, 6, 6],
    [4, 1, 2, 3],
    [2, 5, 1, 2],
]

filtro = FLaplaciano(matriz)
matriz_filtrada = filtro.ejecutar(MascaraLaplaciana.F4)
print(matriz_filtrada)
```

Si deseas aplicar otros filtros o hacer cosass mucho más a "bajo nivel" puedes optar por la clase `FEspacial` que provee métodos como:

- `get_vecinos`: Sirve para obtener los vecinos de un elemento en la matriz
- `aplicar_filtro`: Aplica una máscara que recibe como parámetro
- `reescalar`: Reescala la matriz según un rango que recibe como parámetro 

```python
from HPrIm import FEspacial
matriz = [
    [4, 4, 3, 2],
    [7, 7, 6, 6],
    [4, 1, 2, 3],
    [2, 5, 1, 2],
]

mascara = [
    [1, 1, 1],
    [1, -8, 1],
    [1, 1, 1]
]

filtro = FEspacial(matriz)
res = filtro.aplicar_filtro(mascara)
print(res)
```