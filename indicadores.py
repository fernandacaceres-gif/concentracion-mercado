import numpy as np


def validar_cuotas(cuotas, tolerancia=1e-6):
    """
    Valida un vector de cuotas expresadas entre 0 y 1.
    """

    cuotas = np.asarray(cuotas, dtype=float)

    # Verificar que sea un vector
    if cuotas.ndim != 1:
        raise ValueError(
            "Las cuotas deben ser un vector de una dimensión."
        )

    # Deben existir al menos 2 empresas
    if len(cuotas) < 2:
        raise ValueError(
            "El mercado debe tener al menos 2 empresas."
        )

    # Ninguna cuota puede ser negativa ni mayor a 1
    if np.any(cuotas < 0) or np.any(cuotas > 1):
        raise ValueError(
            "Cada cuota debe estar entre 0 y 1."
        )

    # Suma total
    total = cuotas.sum()

    # Las cuotas deben sumar 1
    if not np.isclose(
        total,
        1.0,
        atol=tolerancia
    ):
        raise ValueError(
            f"Las cuotas deben sumar 1 (100%). "
            f"Actualmente suman {total:.6f}."
        )

    return cuotas


# ==========================================================
# CRk
# ==========================================================

def calcular_crk(cuotas, k):
    """
    CRk:
    suma las k cuotas de mercado más grandes.

    Retorna un valor entre 0 y 1.
    """

    cuotas = validar_cuotas(cuotas)

    if not isinstance(
        k,
        (int, np.integer)
    ):
        raise ValueError(
            "k debe ser un número entero."
        )

    if k < 1 or k > len(cuotas):
        raise ValueError(
            "k debe estar entre 1 y el número de empresas."
        )

    # Ordenar de mayor a menor
    cuotas_ordenadas = np.sort(cuotas)[::-1]

    # Sumar las k más grandes
    return float(
        cuotas_ordenadas[:k].sum()
    )


# ==========================================================
# IHH
# ==========================================================

def calcular_ihh(cuotas):
    """
    Índice Herfindahl-Hirschman.

    Se calcula en escala 0 - 10.000.

    Ejemplo:
    40%, 30%, 20%, 10%

    40² + 30² + 20² + 10² = 3000
    """

    cuotas = validar_cuotas(cuotas)

    return float(
        np.sum(
            (cuotas * 100) ** 2
        )
    )


# ==========================================================
# ÍNDICE DE DOMINANCIA
# ==========================================================

def calcular_id(cuotas):
    """
    Índice de Dominancia.

    En esta versión se utiliza:

        ID = sum(s_i^4) / (sum(s_i^2))^2

    IMPORTANTE:
    El enunciado del taller no entrega la fórmula exacta
    del Índice de Dominancia.

    Deben confirmar que esta sea la fórmula utilizada
    por el profesor en la asignatura.
    """

    cuotas = validar_cuotas(cuotas)

    numerador = np.sum(
        cuotas ** 4
    )

    denominador = (
        np.sum(cuotas ** 2)
    ) ** 2

    if denominador == 0:
        raise ValueError(
            "No es posible calcular el ID."
        )

    return float(
        numerador / denominador
    )


# ==========================================================
# ENTROPÍA
# ==========================================================

def calcular_entropia(cuotas):
    """
    Índice de Entropía.

    IE = - sum(s_i * ln(s_i))
    """

    cuotas = validar_cuotas(cuotas)

    # Evitamos calcular log(0)
    positivas = cuotas[
        cuotas > 0
    ]

    return float(
        -np.sum(
            positivas *
            np.log(positivas)
        )
    )


# ==========================================================
# FUNCIÓN GENERAL
# ==========================================================

def calcular_indicador(
    cuotas,
    indicador,
    k=4
):
    """
    Permite calcular cualquier indicador
    utilizando una sola función.
    """

    if indicador == "CRk":

        return calcular_crk(
            cuotas,
            k
        )

    if indicador == "IHH":

        return calcular_ihh(
            cuotas
        )

    if indicador == "ID":

        return calcular_id(
            cuotas
        )

    if indicador == "IE":

        return calcular_entropia(
            cuotas
        )

    raise ValueError(
        f"Indicador no reconocido: {indicador}"
    )