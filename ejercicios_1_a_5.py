"""
Ejercicios de Geometría Computacional
1) Orientación del robot   2) Intersección de segmentos
3) Pares de tuberías       4) Triangulación de un terreno
Convención: orient(P,Q,R) > 0 antihorario, < 0 horario, = 0 colineal
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------------------------------------------------------------
# Funciones base
# ---------------------------------------------------------------
def orient(P, Q, R):
    """Determinante de orientación del trío P, Q, R."""
    return (Q[0]-P[0])*(R[1]-P[1]) - (Q[1]-P[1])*(R[0]-P[0])


def signo(x):
    return (x > 0) - (x < 0)


def en_segmento(P, Q, R):
    """R es colineal con PQ: ¿está dentro del rectángulo de PQ?"""
    return (min(P[0], Q[0]) <= R[0] <= max(P[0], Q[0]) and
            min(P[1], Q[1]) <= R[1] <= max(P[1], Q[1]))


# ---------------------------------------------------------------
# EJERCICIO 1
# ---------------------------------------------------------------
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


# ---------------------------------------------------------------
# EJERCICIO 2
# ---------------------------------------------------------------
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


# ---------------------------------------------------------------
# EJERCICIO 3
# ---------------------------------------------------------------
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


# ---------------------------------------------------------------
# EJERCICIO 4
# ---------------------------------------------------------------
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


# ---------------------------------------------------------------
# EJERCICIO 5
# ---------------------------------------------------------------
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


if __name__ == "__main__":
    ejercicio1()
    ejercicio2()
    ejercicio3()
    ejercicio4()
    ejercicio5()
