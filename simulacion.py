import numpy as np

from indicadores import calcular_indicador


# ==========================================================
# GENERACIÓN DE CUOTAS
# ==========================================================

def generar_cuotas_aleatorias(
    n_empresas,
    rng=None
):
    """
    Genera cuotas de mercado aleatorias.

    La distribución Dirichlet permite generar
    números no negativos cuya suma es 1.
    """

    if not isinstance(
        n_empresas,
        (int, np.integer)
    ):
        raise ValueError(
            "El número de empresas debe ser entero."
        )

    if (
        n_empresas < 2
        or n_empresas > 100
    ):
        raise ValueError(
            "El número de empresas debe estar entre 2 y 100."
        )

    if rng is None:

        rng = np.random.default_rng()

    cuotas = rng.dirichlet(
        np.ones(n_empresas)
    )

    return cuotas


# ==========================================================
# MONTE CARLO
# ==========================================================

def simulacion_monte_carlo(
    n_empresas,
    indicador,
    iteraciones=1000,
    k=4,
    semilla=None
):
    """
    Ejecuta la simulación Monte Carlo.

    Cada iteración:

    1. Genera cuotas aleatorias.
    2. Calcula el indicador.
    3. Guarda el resultado.
    """

    if (
        iteraciones < 100
        or iteraciones > 20000
    ):
        raise ValueError(
            "Las iteraciones deben estar "
            "entre 100 y 20.000."
        )

    if indicador == "CRk":

        if (
            k < 1
            or k > n_empresas
        ):

            raise ValueError(
                "Para CRk, k debe estar entre 1 y N."
            )

    # Generador aleatorio
    rng = np.random.default_rng(
        semilla
    )

    # Creamos un arreglo vacío
    resultados = np.empty(
        iteraciones,
        dtype=float
    )

    # Monte Carlo
    for i in range(iteraciones):

        # Generar mercado aleatorio
        cuotas = generar_cuotas_aleatorias(
            n_empresas,
            rng=rng
        )

        # Calcular indicador
        valor = calcular_indicador(
            cuotas,
            indicador,
            k
        )

        # Guardar resultado
        resultados[i] = valor

    return resultados


# ==========================================================
# PERCENTIL
# ==========================================================

def calcular_percentil(
    resultados,
    valor_caso
):
    """
    Calcula qué porcentaje de las simulaciones
    tiene un valor menor o igual al caso particular.
    """

    resultados = np.asarray(
        resultados,
        dtype=float
    )

    if resultados.size == 0:

        raise ValueError(
            "No existen resultados de simulación."
        )

    percentil = (
        np.mean(
            resultados <= valor_caso
        )
        * 100
    )

    return float(percentil)


# ==========================================================
# ESTADÍSTICAS
# ==========================================================

def resumen_simulacion(
    resultados
):
    """
    Calcula estadísticas descriptivas de
    los resultados de Monte Carlo.
    """

    resultados = np.asarray(
        resultados,
        dtype=float
    )

    return {

        "promedio":
            float(
                np.mean(resultados)
            ),

        "mediana":
            float(
                np.median(resultados)
            ),

        "desviacion":
            float(
                np.std(resultados)
            ),

        "minimo":
            float(
                np.min(resultados)
            ),

        "maximo":
            float(
                np.max(resultados)
            ),
    }