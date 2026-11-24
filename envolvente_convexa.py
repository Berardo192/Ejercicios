"""
Envolvente convexa: Ejercicios 6 a 10
(en el archivo del enunciado aparecen numerados del 1 al 5)

6) Identificar el cierre convexo     7) Orientación de un punto
8) Implementación de Jarvis March    9) Análisis algorítmico T(n, h)
10) Comparación T_A(n,h) = n*h  vs  T_B(n) = n*log2(n)

Convención: orient(P,Q,R) > 0 antihorario, < 0 horario, = 0 colineal.
Uso:  python envolvente_convexa.py            (imprime todos los resultados)
      python envolvente_convexa.py --grafica  (además guarda ej6_envolvente.png,
                                               requiere matplotlib)
"""
import math
import random
import sys


# ======================================================================
# FUNCIONES BASE
# ======================================================================
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


# ======================================================================
# JARVIS MARCH (con contador de evaluaciones de orientación)
# ======================================================================
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


# ======================================================================
# EJERCICIO 6: identificar el cierre convexo
# ======================================================================
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


# ======================================================================
# EJERCICIO 7: orientación de un punto
# ======================================================================
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


# ======================================================================
# EJERCICIO 8: Jarvis March con conteo de evaluaciones (10, 50 y 100 puntos)
# ======================================================================
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


# ======================================================================
# EJERCICIO 9: análisis algorítmico T(n, h)
# ======================================================================
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


# ======================================================================
# EJERCICIO 10: comparación de algoritmos
# ======================================================================
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


# ======================================================================
if __name__ == "__main__":
    ejercicio6(grafica="--grafica" in sys.argv)
    ejercicio7()
    ejercicio8()
    ejercicio9()
    ejercicio10()
