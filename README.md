# Geometría Computacional: Ejercicios 1 a 10

Proyecto en Python con la solución de 10 ejercicios de geometría computacional y análisis de algoritmos. Este README responde cada pregunta con su análisis, sus fórmulas y los resultados reales de ejecutar el código.

| Ejercicios | Tema | Archivo |
|---|---|---|
| 1 a 5 | Orientación, intersección de segmentos, pares de tuberías, triangulación y comparación de algoritmos | `ejercicios_1_a_5.py` |
| 6 a 10 | Envolvente convexa, Jarvis March y análisis T(n, h) | `envolvente_convexa.py` |

## Contenido del proyecto

```text
geometria_computacional/
├── README.md                # respuestas y análisis de los 10 ejercicios
├── ejercicios_1_a_5.py      # código de los ejercicios 1 a 5
└── envolvente_convexa.py    # código de los ejercicios 6 a 10
```

## Cómo ejecutarlo

```bash
python ejercicios_1_a_5.py               # ejercicios 1 a 5 (requiere matplotlib; guarda PNG de los dibujos)
python envolvente_convexa.py             # ejercicios 6 a 10
python envolvente_convexa.py --grafica   # además guarda ej6_envolvente.png (requiere matplotlib)
```

`envolvente_convexa.py` usa solo la biblioteca estándar; `matplotlib` es opcional y solo hace falta con `--grafica`.

**Convención en todo el proyecto:** `orient(P,Q,R) = (Qx−Px)(Ry−Py) − (Qy−Py)(Rx−Px)`. Si es > 0 el giro es antihorario (izquierda), si es < 0 es horario (derecha) y si es = 0 los puntos son colineales.

---

# Parte 1: Ejercicios 1 a 5

## Funciones base (ejercicios 1 a 5)

```python
def orient(P, Q, R):
    """Determinante de orientación del trío P, Q, R."""
    return (Q[0]-P[0])*(R[1]-P[1]) - (Q[1]-P[1])*(R[0]-P[0])


def signo(x):
    return (x > 0) - (x < 0)


def en_segmento(P, Q, R):
    """R es colineal con PQ: ¿está dentro del rectángulo de PQ?"""
    return (min(P[0], Q[0]) <= R[0] <= max(P[0], Q[0]) and
            min(P[1], Q[1]) <= R[1] <= max(P[1], Q[1]))
```

---

## Ejercicio 1: Orientación del robot

El robot conoce su posición anterior A, su posición actual B y su destino C. El signo del determinante indica hacia qué lado debe girar en B.

**1. Determinantes** (det = ABx·ACy − ABy·ACx, con AB = B − A y AC = C − A):

- Caso 1: A(1,2), B(5,3), C(3,7) → (4)(5) − (1)(2) = **18**
- Caso 2: A(2,1), B(6,5), C(8,2) → (4)(1) − (4)(6) = **−20**
- Caso 3: A(1,1), B(3,3), C(6,6) → (2)(5) − (2)(5) = **0**
- Caso 4: A(0,4), B(5,4), C(3,1) → (5)(−3) − (0)(3) = **−15**

**2. Clasificación:**

- Caso 1: antihorario (gira a la izquierda).
- Caso 2: horario (gira a la derecha).
- Caso 3: colineal (sigue de frente, C está más allá de B).
- Caso 4: horario (gira a la derecha).

**3. T(n):** por trío se hacen 4 restas + 2 multiplicaciones + 1 resta + hasta 2 comparaciones = 9 operaciones, una constante, es decir O(1). Para n tríos:

```text
T(n) = 9n  →  O(n)
```

```python
def clasificar(A, B, C):
    d = orient(A, B, C)
    if d > 0:
        return d, "Giro antihorario"
    elif d < 0:
        return d, "Giro horario"
    return d, "Colineal"


def ejercicio1():
    print("=" * 50, "\nEJERCICIO 1\n" + "=" * 50)
    casos = {
        1: ((1, 2), (5, 3), (3, 7)),
        2: ((2, 1), (6, 5), (8, 2)),
        3: ((1, 1), (3, 3), (6, 6)),
        4: ((0, 4), (5, 4), (3, 1)),
    }
    for n, (A, B, C) in casos.items():
        d, tipo = clasificar(A, B, C)
        print(f"Caso {n}: det = {d:>4} -> {tipo}")
    # T(n): por caso ~ 5 restas + 2 mult + 1 resta + comparaciones = constante
    # T = c -> O(1) por caso; para n casos T(n) = c*n -> O(n)
```

Salida:

```text
================================================== 
EJERCICIO 1
==================================================
Caso 1: det =   18 -> Giro antihorario
Caso 2: det =  -20 -> Giro horario
Caso 3: det =    0 -> Colineal
Caso 4: det =  -15 -> Giro horario
```

---

## Ejercicio 2: Intersección de segmentos

El enunciado no da C ni D en el caso 3; se supusieron C(3,0) y D(3,5).

**1. Dibujo en el plano:**

- Caso 1: AB tiene pendiente 2/3 y CD pendiente −5/6; las rectas se cortan en (44/9, 97/27) ≈ (4,89; 3,59), dentro de ambos segmentos.
- Caso 2: los 4 puntos están sobre y = x, en orden A, B, C, D, con un hueco entre B y C.
- Caso 3: AB es horizontal (y = 2) y CD vertical (x = 3); forman una cruz en (3,2).

**2. Las 4 orientaciones** (o1 = orient(A,B,C), o2 = orient(A,B,D), o3 = orient(C,D,A), o4 = orient(C,D,B)):

- Caso 1: o1 = +26, o2 = −28, o3 = −35, o4 = +19
- Caso 2: o1 = o2 = o3 = o4 = 0
- Caso 3: o1 = −12, o2 = +18, o3 = +15, o4 = −15

**3. ¿Existe intersección?** Hay cruce propio si o1 ≠ o2 y o3 ≠ o4. Si alguna orientación es 0 y el punto cae dentro de la caja del otro segmento, hay contacto o superposición.

- Caso 1: **SÍ** (cruce propio).
- Caso 2: **NO** (AB ocupa x ∈ [1,3] y CD ocupa x ∈ [5,7], sin solaparse).
- Caso 3: **SÍ**, en (3,2).

**4. Función `interseccion`:** calcula las 4 orientaciones, aplica el caso general y luego revisa los casos colineales con `en_segmento`. Está en el código de abajo.

**5. ¿Por qué es O(1)?** Hace 4 orientaciones (7 operaciones cada una, 28 en total) y un número fijo de comparaciones. Siempre procesa 4 puntos, sin ciclos ni recursión, por lo que T ≤ c para cualquier entrada: O(1).

```python
def interseccion(A, B, C, D):
    """True si los segmentos AB y CD se intersectan (cruce, contacto
    o superposición). Costo O(1)."""
    o1 = signo(orient(A, B, C))
    o2 = signo(orient(A, B, D))
    o3 = signo(orient(C, D, A))
    o4 = signo(orient(C, D, B))

    # Caso general: cruce propio
    if o1 != o2 and o3 != o4:
        return True

    # Casos especiales: colineales / contacto / superposición
    if o1 == 0 and en_segmento(A, B, C): return True
    if o2 == 0 and en_segmento(A, B, D): return True
    if o3 == 0 and en_segmento(C, D, A): return True
    if o4 == 0 and en_segmento(C, D, B): return True
    return False


def dibujar_segmentos(A, B, C, D, titulo, archivo):
    plt.figure(figsize=(5, 4))
    plt.plot(*zip(A, B), "b-o", label="AB")
    plt.plot(*zip(C, D), "r-o", label="CD")
    for nombre, p in zip("ABCD", (A, B, C, D)):
        plt.annotate(f"{nombre}{p}", p, textcoords="offset points", xytext=(5, 5))
    plt.grid(True); plt.axis("equal"); plt.legend(); plt.title(titulo)
    plt.savefig(archivo, dpi=130, bbox_inches="tight"); plt.close()


def ejercicio2():
    print("=" * 50, "\nEJERCICIO 2\n" + "=" * 50)
    casos = {
        "Caso 1": ((1, 1), (7, 5), (2, 6), (8, 1)),
        "Caso 2": ((1, 1), (3, 3), (5, 5), (7, 7)),
        # El enunciado no da C y D del caso 3: se suponen C(3,0), D(3,5)
        "Caso 3 (C y D supuestos)": ((0, 2), (6, 2), (3, 0), (3, 5)),
    }
    for k, (nombre, (A, B, C, D)) in enumerate(casos.items(), start=1):
        o = [orient(A, B, C), orient(A, B, D), orient(C, D, A), orient(C, D, B)]
        print(f"{nombre}: o1={o[0]}, o2={o[1]}, o3={o[2]}, o4={o[3]} "
              f"-> intersección: {interseccion(A, B, C, D)}")
        dibujar_segmentos(A, B, C, D, nombre, f"ej2_caso{k}.png")
```

Salida:

```text
================================================== 
EJERCICIO 2
==================================================
Caso 1: o1=26, o2=-28, o3=-35, o4=19 -> intersección: True
Caso 2: o1=0, o2=0, o3=0, o4=0 -> intersección: False
Caso 3 (C y D supuestos): o1=-12, o2=18, o3=15, o4=-15 -> intersección: True
```

---

## Ejercicio 3: Pares de tuberías

**1. ¿Por qué el segundo `for` empieza en `i + 1`?** Evita comparar una tubería consigo misma (i, i), que siempre daría que se intercepta, y evita pares repetidos, porque `interceptan(i,j) = interceptan(j,i)`. Pasa de n² a n(n−1)/2 llamadas.

**2. Tabla de iteraciones:** para cada i, j recorre de i+1 a n−1, o sea n−1−i llamadas.

- N = 5: 4 + 3 + 2 + 1 + 0 = **10** llamadas.
- N = 8: 7 + 6 + 5 + 4 + 3 + 2 + 1 + 0 = **28** llamadas.

**3. Expresión exacta de T(n):**

```text
T(n) = Σ (n − 1 − i),   i = 0 … n−1
```

**4. Sumatoria y complejidad:** con k = n − 1 − i la suma queda Σ k de 0 a n−1, y por Gauss (2S = n(n−1)):

```text
T(n) = n(n−1)/2 = n²/2 − n/2  →  O(n²)
```

Cada llamada a `interceptan` es O(1) (ejercicio 2), así que el algoritmo completo también es O(n²).

**5. Comprobaciones:**

- n = 100: **4.950**
- n = 1.000: **499.500**
- n = 10.000: **49.995.000**

```python
def contar_pares(n):
    """Cuenta las llamadas a interceptan con el doble for (j = i+1)."""
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            c += 1
    return c


def comprobaciones(n):
    """Fórmula cerrada T(n) = n(n-1)/2."""
    return n * (n - 1) // 2


def contar_intersecciones(tuberias):
    """Cuenta los pares de tuberías (segmentos) que se interceptan."""
    n, total = len(tuberias), 0
    for i in range(n):
        for j in range(i + 1, n):
            if interseccion(*tuberias[i], *tuberias[j]):
                total += 1
    return total


def ejercicio3():
    print("=" * 50, "\nEJERCICIO 3\n" + "=" * 50)
    for n in (5, 8):
        print(f"\nTabla de iteraciones N={n}")
        print(" i | llamadas")
        for i in range(n):
            print(f"{i:>2} | {n - 1 - i}")
        print(f"Total = {contar_pares(n)}  (fórmula: {comprobaciones(n)})")
    print()
    for n in (100, 1000, 10000):
        print(f"n={n:>6}: {comprobaciones(n):>12,} comprobaciones")
    # Ejemplo de uso con 3 tuberías
    tub = [((0, 0), (4, 4)), ((0, 4), (4, 0)), ((10, 10), (12, 12))]
    print("\nPares que se interceptan en el ejemplo:", contar_intersecciones(tub))
```

Salida:

```text
================================================== 
EJERCICIO 3
==================================================

Tabla de iteraciones N=5
 i | llamadas
 0 | 4
 1 | 3
 2 | 2
 3 | 1
 4 | 0
Total = 10  (fórmula: 10)

Tabla de iteraciones N=8
 i | llamadas
 0 | 7
 1 | 6
 2 | 5
 3 | 4
 4 | 3
 5 | 2
 6 | 1
 7 | 0
Total = 28  (fórmula: 28)

n=   100:        4,950 comprobaciones
n=  1000:      499,500 comprobaciones
n= 10000:   49,995,000 comprobaciones

Pares que se interceptan en el ejemplo: 1
```

---

## Ejercicio 4: Triangulación del terreno

Vértices A(0,0), B(8,0), C(8,6), D(4,3), E(0,6). El área con signo es +36, así que el recorrido es antihorario.

**1. Vértices convexos y cóncavos** (det > 0 convexo, det < 0 cóncavo, usando anterior, actual, siguiente):

- A: +48 convexo
- B: +48 convexo
- C: +24 convexo
- D: −24 **cóncavo** (el único)
- E: +24 convexo

**2. Triángulos y diagonales internas:**

```text
Triángulos = n − 2 = 3          Diagonales = n − 3 = 2
```

**3. Triangulación válida:** se trazan las diagonales DA y DB desde el vértice cóncavo D. Triángulos: ABD (área 12), BCD (12) y DEA (12); suman 36, igual que el terreno.

**4. Primera oreja:** el vértice **C**, con el triángulo BCD. A y B no son orejas porque D queda sobre el borde de sus triángulos (EB y AC). Al recortarla queda el polígono A, B, D, E.

**5. Condiciones antes de retirar un vértice:**

- Debe ser convexo (orient > 0).
- Ningún otro vértice puede estar dentro del triángulo ni sobre su borde.
- La diagonal (anterior → siguiente) debe ser interior y no cruzar aristas.
- El polígono resultante debe seguir siendo simple.

**6. Función en Python con n:**

```text
f(n) = (n − 2 triángulos,  n − 3 diagonales)
```

Es la función `triangulacion(n)` del código. Ejemplo: n = 100 da 98 triángulos y 97 diagonales.

```python
def punto_en_triangulo(p, a, b, c):
    d1, d2, d3 = orient(a, b, p), orient(b, c, p), orient(c, a, p)
    return d1 >= 0 and d2 >= 0 and d3 >= 0     # incluye el borde


def tipo_vertices(poly):
    """Clasifica cada vértice (polígono antihorario)."""
    n, res = len(poly), []
    for i in range(n):
        d = orient(poly[i-1], poly[i], poly[(i+1) % n])
        res.append((d, "Convexo" if d > 0 else "Cóncavo" if d < 0 else "Colineal"))
    return res


def triangulacion(n):
    """Devuelve (n_triangulos, n_diagonales_internas) de un polígono simple."""
    if n < 3:
        raise ValueError("Un polígono necesita al menos 3 vértices")
    return n - 2, n - 3


def ear_clipping(poly):
    idx = list(range(len(poly)))
    triangulos = []
    while len(idx) > 3:
        for k in range(len(idx)):
            i, j, l = idx[k-1], idx[k], idx[(k+1) % len(idx)]
            a, b, c = poly[i], poly[j], poly[l]
            if orient(a, b, c) <= 0:                 # no convexo
                continue
            if any(punto_en_triangulo(poly[m], a, b, c)
                   for m in idx if m not in (i, j, l)):
                continue
            triangulos.append((i, j, l))
            idx.pop(k)
            break
        else:
            raise ValueError("No se encontró oreja (polígono no simple)")
    triangulos.append(tuple(idx))
    return triangulos


def area_poligono(poly):
    n = len(poly)
    return sum(poly[i][0]*poly[(i+1) % n][1] - poly[(i+1) % n][0]*poly[i][1]
               for i in range(n)) / 2


def ejercicio4():
    print("=" * 50, "\nEJERCICIO 4\n" + "=" * 50)
    P = {"A": (0, 0), "B": (8, 0), "C": (8, 6), "D": (4, 3), "E": (0, 6)}
    nombres = list(P)
    poly = list(P.values())
    print("Área del polígono:", area_poligono(poly), "(positiva = antihorario)")

    print("\nVértices:")
    for nom, (d, t) in zip(nombres, tipo_vertices(poly)):
        print(f"  {nom}: det = {d:>4} -> {t}")

    t, d = triangulacion(len(poly))
    print(f"\nn={len(poly)}: {t} triángulos y {d} diagonales internas")

    tri = ear_clipping(poly)
    print("Ear clipping (índices):", tri)
    print("Triángulos:", ["".join(nombres[i] for i in tr) for tr in tri])

    for n in (3, 4, 5, 8, 100):
        t, d = triangulacion(n)
        print(f"  n={n}: {t} triángulos, {d} diagonales internas")

    # Dibujo de la triangulación (diagonales DA y DB)
    orden = nombres + [nombres[0]]
    xs, ys = zip(*[P[k] for k in orden])
    plt.figure(figsize=(5, 4))
    plt.plot(xs, ys, "k-o")
    for k, (x, y) in P.items():
        plt.annotate(f"{k}({x},{y})", (x, y), textcoords="offset points", xytext=(5, 5))
    for a, b in [("D", "A"), ("D", "B")]:
        plt.plot(*zip(P[a], P[b]), "r--")
    plt.grid(True); plt.axis("equal"); plt.title("Triangulación del terreno")
    plt.savefig("ej4_triangulacion.png", dpi=130, bbox_inches="tight"); plt.close()
```

Salida:

```text
================================================== 
EJERCICIO 4
==================================================
Área del polígono: 36.0 (positiva = antihorario)

Vértices:
  A: det =   48 -> Convexo
  B: det =   48 -> Convexo
  C: det =   24 -> Convexo
  D: det =  -24 -> Cóncavo
  E: det =   24 -> Convexo

n=5: 3 triángulos y 2 diagonales internas
Ear clipping (índices): [(1, 2, 3), (0, 1, 3), (0, 3, 4)]
Triángulos: ['BCD', 'ABD', 'ADE']
  n=3: 1 triángulos, 0 diagonales internas
  n=4: 2 triángulos, 1 diagonales internas
  n=5: 3 triángulos, 2 diagonales internas
  n=8: 6 triángulos, 5 diagonales internas
  n=100: 98 triángulos, 97 diagonales internas
```

---

## Ejercicio 5: Comparación de algoritmos de triangulación

Algoritmo A: implementación sencilla con verificaciones repetidas. Algoritmo B: implementación más eficiente.

```text
T_A(n) = n³          T_B(n) = n²
```

| n | T_A(n) = n³ | T_B(n) = n² | T_A / T_B | Big O de A | Big O de B |
|---|---|---|---|---|---|
| 10 | 1.000 | 100 | 10 | O(n³) | O(n²) |
| 100 | 1.000.000 | 10.000 | 100 | O(n³) | O(n²) |
| 1.000 | 1.000.000.000 | 1.000.000 | 1.000 | O(n³) | O(n²) |

```text
T_A(n) / T_B(n) = n³ / n² = n
```

La razón es igual a n: crece con el tamaño del terreno. Con n = 1.000, A hace 1.000 veces más operaciones que B (10⁹ frente a 10⁶).

**Conclusión: conviene el algoritmo B.** Su complejidad O(n²) crece más despacio que la de A, O(n³), y la ventaja aumenta con n. Solo en polígonos muy pequeños (por ejemplo n = 5) la diferencia es despreciable.

```python
def T_A(n):
    """Algoritmo A: implementación sencilla con verificaciones repetidas, O(n^3)."""
    return n ** 3


def T_B(n):
    """Algoritmo B: implementación más eficiente, O(n^2)."""
    return n ** 2


def ejercicio5():
    print("=" * 50, "\nEJERCICIO 5\n" + "=" * 50)
    print(f"{'n':>6} | {'T_A = n^3':>15} | {'T_B = n^2':>12} | {'T_A/T_B':>8}")
    for n in (10, 100, 1000):
        print(f"{n:>6} | {T_A(n):>15,} | {T_B(n):>12,} | {T_A(n) // T_B(n):>8}")
    print("Big O:  A -> O(n^3)   B -> O(n^2)   razón T_A/T_B = n")
    print("Conclusión: conviene el algoritmo B.")
```

Salida:

```text
================================================== 
EJERCICIO 5
==================================================
     n |       T_A = n^3 |    T_B = n^2 |  T_A/T_B
    10 |           1,000 |          100 |       10
   100 |       1,000,000 |       10,000 |      100
  1000 |   1,000,000,000 |    1,000,000 |     1000
Big O:  A -> O(n^3)   B -> O(n^2)   razón T_A/T_B = n
Conclusión: conviene el algoritmo B.
```

---

# Parte 2: Ejercicios 6 a 10 (envolvente convexa)

En el enunciado original aparecen numerados del 1 al 5; aquí se numeran del 6 al 10. Su código está en `envolvente_convexa.py`.

## Funciones base y Jarvis March (ejercicios 6 a 10)

Estas funciones las usan todos los ejercicios. `jarvis_march` devuelve la envolvente (índices, en sentido antihorario) y cuántas veces calculó `orient`.

```python
def orient(P, Q, R):
    """Determinante de orientación del trío P, Q, R."""
    return (Q[0]-P[0])*(R[1]-P[1]) - (Q[1]-P[1])*(R[0]-P[0])


def sentido(det):
    """Texto del sentido del giro según el signo del determinante."""
    if det > 0:
        return "giro antihorario (izquierda)"
    if det < 0:
        return "giro horario (derecha)"
    return "colineales"


def distancia2(P, Q):
    """Distancia al cuadrado (basta para comparar, evita la raíz)."""
    return (P[0]-Q[0])**2 + (P[1]-Q[1])**2


def jarvis_march(puntos):
    """
    Devuelve (hull, evaluaciones):
      hull          lista de índices de la envolvente, en sentido antihorario,
                    empezando por el punto más a la izquierda.
      evaluaciones  cantidad de veces que se calculó orient().
    Se asume que no hay puntos repetidos.
    """
    n = len(puntos)
    if n < 3:
        return list(range(n)), 0

    evaluaciones = 0
    inicio = min(range(n), key=lambda i: (puntos[i][0], puntos[i][1]))
    hull = []
    p = inicio
    while True:
        hull.append(p)
        q = (p + 1) % n                       # candidato inicial
        for r in range(n):
            d = orient(puntos[p], puntos[q], puntos[r])
            evaluaciones += 1
            if d < 0:                         # r queda a la derecha de p->q
                q = r
            elif d == 0 and distancia2(puntos[p], puntos[r]) > distancia2(puntos[p], puntos[q]):
                q = r                         # colineales: se queda el más lejano
        p = q
        if p == inicio:
            break
    return hull, evaluaciones


def todos_a_la_izquierda(puntos, hull):
    """Verificación: cada arista de la envolvente deja a todos los puntos a su izquierda (o sobre ella)."""
    for k in range(len(hull)):
        a, b = puntos[hull[k]], puntos[hull[(k + 1) % len(hull)]]
        if any(orient(a, b, p) < 0 for p in puntos):
            return False
    return True
```

**Cómo funciona Jarvis March (envoltura de regalo):**

1. Se parte del punto más a la izquierda, que siempre está en la envolvente.
2. Desde el punto actual `p` se elige un candidato `q` y se compara con todos los demás puntos `r` usando `orient(p, q, r)`.
3. Si `r` queda a la derecha de `p→q` (det < 0), `q` no es el más antihorario y se reemplaza por `r`. Si son colineales (det = 0) se conserva el más lejano.
4. Al terminar de revisar los n puntos, todos quedan a la izquierda de `p→q`, así que `p→q` es una arista de la envolvente. Se repite desde `q` hasta volver al punto inicial.

---

## Ejercicio 6: Identificar el cierre convexo

Puntos: a(1,1), b(6,1), c(7,4), d(4,7), e(1,5), f(3,3), g(5,4).

**Dibujo de los puntos** (letra MAYÚSCULA = en la envolvente, minúscula = interior):

```text
 8 | .  .  .  .  .  .  .  .  . 
 7 | .  .  .  .  D  .  .  .  . 
 6 | .  .  .  .  .  .  .  .  . 
 5 | .  E  .  .  .  .  .  .  . 
 4 | .  .  .  .  .  g  .  C  . 
 3 | .  .  .  f  .  .  .  .  . 
 2 | .  .  .  .  .  .  .  .  . 
 1 | .  A  .  .  .  .  B  .  . 
 0 | .  .  .  .  .  .  .  .  . 
   +---------------------------
     0  1  2  3  4  5  6  7  8 
```

**Puntos de la envolvente:** a, b, c, d, e (h = 5). **Puntos interiores:** f y g.

**Recorrido en sentido antihorario:**

```text
a(1,1) → b(6,1) → c(7,4) → d(4,7) → e(1,5) → a(1,1)
```

**Justificación:** en cada vértice del recorrido el giro es antihorario (determinante positivo), y f y g quedan a la izquierda de todas las aristas, es decir, dentro del polígono.

- orient(a,b,c) = 15 > 0
- orient(b,c,d) = 12 > 0
- orient(c,d,e) = 15 > 0
- orient(d,e,a) = 12 > 0
- orient(e,a,b) = 20 > 0

```python
PUNTOS_6 = {"a": (1, 1), "b": (6, 1), "c": (7, 4), "d": (4, 7),
            "e": (1, 5), "f": (3, 3), "g": (5, 4)}


def dibujar_ascii(puntos, nombres, hull):
    """Plano en texto: letra MAYÚSCULA = en la envolvente, minúscula = interior."""
    xmax = max(p[0] for p in puntos) + 1
    ymax = max(p[1] for p in puntos) + 1
    rejilla = {p: n for p, n in zip(puntos, nombres)}
    en_hull = {puntos[i] for i in hull}
    for y in range(ymax, -1, -1):
        fila = ""
        for x in range(xmax + 1):
            if (x, y) in rejilla:
                letra = rejilla[(x, y)]
                fila += f" {letra.upper() if (x, y) in en_hull else letra} "
            else:
                fila += " . "
        print(f"{y:>2} |{fila}")
    print("   +" + "---" * (xmax + 1))
    print("    " + "".join(f"{x:^3}" for x in range(xmax + 1)))


def dibujar_png(puntos, nombres, hull, archivo):
    """Opcional: imagen con matplotlib (solo si se ejecuta con --grafica)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ciclo = hull + [hull[0]]
    plt.figure(figsize=(5, 5))
    plt.plot([puntos[i][0] for i in ciclo], [puntos[i][1] for i in ciclo], "r-")
    plt.scatter(*zip(*puntos), c="k")
    for p, n in zip(puntos, nombres):
        plt.annotate(f"{n}{p}", p, textcoords="offset points", xytext=(5, 5))
    plt.grid(True); plt.axis("equal"); plt.title("Envolvente convexa")
    plt.savefig(archivo, dpi=130, bbox_inches="tight"); plt.close()


def ejercicio6(grafica=False):
    print("=" * 50, "\nEJERCICIO 6: cierre convexo\n" + "=" * 50)
    nombres = list(PUNTOS_6)
    puntos = list(PUNTOS_6.values())
    hull, evals = jarvis_march(puntos)
    print("Puntos:", ", ".join(f"{n}{p}" for n, p in PUNTOS_6.items()))
    dibujar_ascii(puntos, nombres, hull)
    print("(MAYÚSCULA = en la envolvente, minúscula = interior)")
    print("Recorrido antihorario:", " -> ".join(nombres[i] for i in hull + [hull[0]]))
    print("Puntos interiores:", [nombres[i] for i in range(len(puntos)) if i not in hull])
    print("Verificación (todos a la izquierda de cada arista):", todos_a_la_izquierda(puntos, hull))
    print("Tamaño de la envolvente h =", len(hull), "| evaluaciones =", evals)
    if grafica:
        dibujar_png(puntos, nombres, hull, "ej6_envolvente.png")
        print("Imagen guardada en ej6_envolvente.png")
```

Salida:

```text
================================================== 
EJERCICIO 6: cierre convexo
==================================================
Puntos: a(1, 1), b(6, 1), c(7, 4), d(4, 7), e(1, 5), f(3, 3), g(5, 4)
 8 | .  .  .  .  .  .  .  .  . 
 7 | .  .  .  .  D  .  .  .  . 
 6 | .  .  .  .  .  .  .  .  . 
 5 | .  E  .  .  .  .  .  .  . 
 4 | .  .  .  .  .  g  .  C  . 
 3 | .  .  .  f  .  .  .  .  . 
 2 | .  .  .  .  .  .  .  .  . 
 1 | .  A  .  .  .  .  B  .  . 
 0 | .  .  .  .  .  .  .  .  . 
   +---------------------------
     0  1  2  3  4  5  6  7  8 
(MAYÚSCULA = en la envolvente, minúscula = interior)
Recorrido antihorario: a -> b -> c -> d -> e -> a
Puntos interiores: ['f', 'g']
Verificación (todos a la izquierda de cada arista): True
Tamaño de la envolvente h = 5 | evaluaciones = 35
```

---

## Ejercicio 7: Orientación de un punto

Enunciado: a 12, b 53, c 36. Se interpretan como **A(1,2), B(5,3), C(3,6)**.

**Determinante:**

```text
AB = B − A = (4, 1)
AC = C − A = (2, 4)
det = ABx·ACy − ABy·ACx = (4)(4) − (1)(2) = 14
```

**Sentido del giro:** det = 14 > 0, entonces es un **giro antihorario** (a la izquierda). Además, |det|/2 = 7 es el área del triángulo ABC.

**Uso en Jarvis March:** el determinante responde "¿de qué lado de la recta p→q queda el punto r?".

- det > 0: `r` está a la izquierda de `p→q`, el candidato `q` se mantiene.
- det < 0: `r` está a la derecha, `q` se reemplaza por `r` (es más antihorario).
- det = 0: son colineales, se queda el punto más lejano.

En el ejemplo, con p = A, q = B y r = C el resultado es +14, así que C queda a la izquierda de A→B y B sigue siendo el candidato.

```python
def ejercicio7():
    print("=" * 50, "\nEJERCICIO 7: orientación de un punto\n" + "=" * 50)
    A, B, C = (1, 2), (5, 3), (3, 6)          # a 12, b 53, c 36
    ux, uy = B[0]-A[0], B[1]-A[1]
    vx, vy = C[0]-A[0], C[1]-A[1]
    det = ux*vy - uy*vx
    print(f"A={A} B={B} C={C}")
    print(f"AB=({ux},{uy})  AC=({vx},{vy})")
    print(f"det = ({ux})({vy}) - ({uy})({vx}) = {det}  -> {sentido(det)}")
    print(f"Área del triángulo ABC = |det|/2 = {abs(det)/2}")
    # Uso dentro de Jarvis: p = A (punto actual de la envolvente), q = B (candidato), r = C
    if det < 0:
        print("En Jarvis: C queda a la derecha de A->B, entonces el candidato pasa a ser C.")
    else:
        print("En Jarvis: C queda a la izquierda de A->B, entonces el candidato sigue siendo B.")
```

Salida:

```text
================================================== 
EJERCICIO 7: orientación de un punto
==================================================
A=(1, 2) B=(5, 3) C=(3, 6)
AB=(4,1)  AC=(2,4)
det = (4)(4) - (1)(2) = 14  -> giro antihorario (izquierda)
Área del triángulo ABC = |det|/2 = 7.0
En Jarvis: C queda a la izquierda de A->B, entonces el candidato sigue siendo B.
```

---

## Ejercicio 8: Implementación de Jarvis March con conteo de evaluaciones

El programa `jarvis_march` (arriba) devuelve junto con la envolvente el número de evaluaciones de orientación. Se prueba con 10, 50 y 100 puntos enteros aleatorios (semilla fija 2024, cuadrícula de 200 × 200).

```python
def puntos_aleatorios(n, semilla):
    """n puntos enteros distintos en una cuadrícula de 200 x 200."""
    rnd = random.Random(semilla)
    celdas = rnd.sample(range(200 * 200), n)
    return [(c % 200, c // 200) for c in celdas]


def ejercicio8():
    print("=" * 50, "\nEJERCICIO 8: Jarvis March con conteo\n" + "=" * 50)
    print(f"{'n':>5} | {'h (puntos envolvente)':>21} | {'evaluaciones de orient':>22} | {'h*n':>6}")
    for n in (10, 50, 100):
        pts = puntos_aleatorios(n, semilla=2024)
        hull, evals = jarvis_march(pts)
        assert todos_a_la_izquierda(pts, hull)
        print(f"{n:>5} | {len(hull):>21} | {evals:>22} | {len(hull)*n:>6}")
    print("Se cumple: evaluaciones = h * n")
```

Salida:

```text
================================================== 
EJERCICIO 8: Jarvis March con conteo
==================================================
    n | h (puntos envolvente) | evaluaciones de orient |    h*n
   10 |                     6 |                     60 |     60
   50 |                     9 |                    450 |    450
  100 |                    12 |                   1200 |   1200
Se cumple: evaluaciones = h * n
```

| n (puntos) | h (puntos de la envolvente) | Evaluaciones de orientación |
|---|---|---|
| 10 | 6 | 60 |
| 50 | 9 | 450 |
| 100 | 12 | 1200 |

**Análisis:** por cada punto de la envolvente se recorren los n puntos, así que evaluaciones = h · n exactamente. Con otra semilla cambia h y, con él, el número de evaluaciones. Con los 7 puntos del ejercicio 6 se obtienen h = 5 y 35 evaluaciones.

---

## Ejercicio 9: Análisis algorítmico

**Pregunta:** ¿qué pasaría si la función de orientación estuviera dentro de dos `for`, uno con `i` dependiente de h y otro con `j` dependiente de n?

```python
for i in range(h):        # un paso por cada punto de la envolvente
    for j in range(n):    # se revisan todos los puntos
        orient(...)       # O(1)
```

**T(n, h):**

```text
T(n, h) = Σ (i=1..h) Σ (j=1..n) c = c · n · h
```

**Complejidad:** **O(n · h)**. Es sensible a la salida: depende del tamaño de la envolvente.

**Casos:**

- Si h es pequeño (por ejemplo h = 3): T = 3n, es decir O(n).
- Si **h = n** (todos los puntos están en la envolvente): T(n, n) = n · n = **n²**, es decir **O(n²)**. Es el peor caso.

```python
def contar_con_dos_for(n, h):
    """orient dentro de dos for: i depende de h (envolvente) y j depende de n (puntos)."""
    evaluaciones = 0
    for i in range(h):
        for j in range(n):
            evaluaciones += 1          # aquí va una evaluación de orient(), costo O(1)
    return evaluaciones


def T(n, h):
    """T(n, h) = sum_{i=1}^{h} sum_{j=1}^{n} 1 = n * h"""
    return n * h


def puntos_en_parabola(n):
    """Todos los puntos están en la envolvente (h = n): peor caso."""
    return [(i, i * i) for i in range(n)]


def puntos_en_triangulo(n, semilla):
    """3 esquinas + n-3 puntos estrictamente interiores (h = 3): mejor caso."""
    rnd = random.Random(semilla)
    pts = [(0, 0), (1000, 0), (0, 1000)]
    interiores = set()
    while len(interiores) < n - 3:
        x, y = rnd.randint(1, 900), rnd.randint(1, 900)
        if x + y < 990:
            interiores.add((x, y))
    return pts + sorted(interiores)


def ejercicio9():
    print("=" * 50, "\nEJERCICIO 9: análisis T(n, h)\n" + "=" * 50)
    print("Comprobación de T(n,h) = n*h con los dos for:")
    for n, h in ((10, 3), (50, 10), (100, 100)):
        print(f"  n={n:>3}, h={h:>3}: contado = {contar_con_dos_for(n, h):>6}  fórmula n*h = {T(n, h)}")
    n = 100
    mejor = puntos_en_triangulo(n, semilla=1)
    peor = puntos_en_parabola(n)
    for nombre, pts in (("mejor caso (h pequeño)", mejor), ("peor caso (h = n)", peor)):
        hull, evals = jarvis_march(pts)
        print(f"  Jarvis, {nombre}: n={n}, h={len(hull)}, evaluaciones={evals}")
    print("Cuando h = n:  T(n, n) = n*n = n^2  ->  O(n^2)")
```

Salida:

```text
================================================== 
EJERCICIO 9: análisis T(n, h)
==================================================
Comprobación de T(n,h) = n*h con los dos for:
  n= 10, h=  3: contado =     30  fórmula n*h = 30
  n= 50, h= 10: contado =    500  fórmula n*h = 500
  n=100, h=100: contado =  10000  fórmula n*h = 10000
  Jarvis, mejor caso (h pequeño): n=100, h=3, evaluaciones=300
  Jarvis, peor caso (h = n): n=100, h=100, evaluaciones=10000
Cuando h = n:  T(n, n) = n*n = n^2  ->  O(n^2)
```

---

## Ejercicio 10: Comparación de algoritmos

```text
T_A(n, h) = n · h
T_B(n)    = n · log₂(n)
```

(Se usa logaritmo en base 2, que es el habitual en análisis de algoritmos.)

| n | h | T_A = n·h | T_B = n·log₂ n | T_A / T_B | Mejor |
|---|---|---|---|---|---|
| 100 | 5 | 500 | 664,4 | 0,753 | **A** |
| 100 | 80 | 8.000 | 664,4 | 12,041 | **B** |
| 1000 | 10 | 10.000 | 9.965,8 | 1,003 | B (casi empate) |
| 1000 | 900 | 900.000 | 9.965,8 | 90,309 | **B** |

**Análisis:**

- Las dos alternativas se igualan cuando n · h = n · log₂ n, es decir, cuando **h = log₂ n** (≈ 6,64 para n = 100 y ≈ 9,97 para n = 1000).
- Si h < log₂ n conviene A; si h > log₂ n conviene B.
- A depende de h (es sensible a la salida) y B no: B siempre cuesta n log n, sin importar cuántos puntos queden en la envolvente.
- Con n = 100 y h = 5, A gana porque h es menor que log₂ 100. Con h = 80 o h = 900, A se vuelve mucho peor (hasta 90 veces más operaciones).

**Conclusión:** si se espera una envolvente pequeña (h < log n) se usa A (tipo Jarvis). Si h puede ser grande, o no se conoce, conviene B (tipo Graham Scan o cadena monótona), cuyo costo es predecible.

```python
def T_A(n, h):
    """Alternativa A (tipo Jarvis): n * h."""
    return n * h


def T_B(n):
    """Alternativa B (tipo Graham / cadena monótona): n * log2(n)."""
    return n * math.log2(n)


def ejercicio10():
    print("=" * 50, "\nEJERCICIO 10: comparación T_A vs T_B\n" + "=" * 50)
    print(f"{'n':>5} {'h':>4} | {'T_A = n*h':>10} | {'T_B = n*log2 n':>14} | {'T_A/T_B':>8} | mejor")
    for n, h in ((100, 5), (100, 80), (1000, 10), (1000, 900)):
        a, b = T_A(n, h), T_B(n)
        mejor = "A" if a < b else "B" if b < a else "empate"
        print(f"{n:>5} {h:>4} | {a:>10,} | {b:>14,.1f} | {a/b:>8.3f} | {mejor}")
    for n in (100, 1000):
        print(f"Punto de cruce para n={n}: h = log2(n) = {math.log2(n):.2f}")
```

Salida:

```text
================================================== 
EJERCICIO 10: comparación T_A vs T_B
==================================================
    n    h |  T_A = n*h | T_B = n*log2 n |  T_A/T_B | mejor
  100    5 |        500 |          664.4 |    0.753 | A
  100   80 |      8,000 |          664.4 |   12.041 | B
 1000   10 |     10,000 |        9,965.8 |    1.003 | B
 1000  900 |    900,000 |        9,965.8 |   90.309 | B
Punto de cruce para n=100: h = log2(n) = 6.64
Punto de cruce para n=1000: h = log2(n) = 9.97
```
