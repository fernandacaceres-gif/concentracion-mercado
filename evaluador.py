# ==========================================================
# CLASIFICACIÓN IHH
# ==========================================================

def clasificar_ihh(valor):
    """
    Clasificación de ejemplo para IHH.

    IMPORTANTE:
    Confirma con tu profesor los umbrales
    utilizados oficialmente en la asignatura.
    """

    if valor < 1500:

        return "Baja concentración"

    if valor < 2500:

        return "Concentración moderada"

    return "Alta concentración"


# ==========================================================
# CLASIFICACIÓN RELATIVA
# ==========================================================

def clasificar_percentil(
    percentil
):
    """
    Clasificación RELATIVA respecto de
    la distribución Monte Carlo.

    NO reemplaza los umbrales teóricos
    específicos de cada indicador.
    """

    if percentil < 33.33:

        return (
            "Baja concentración relativa"
        )

    if percentil < 66.67:

        return (
            "Concentración relativa intermedia"
        )

    return (
        "Alta concentración relativa"
    )


# ==========================================================
# COMPROBAR RESPUESTA
# ==========================================================

def evaluar_respuesta(
    respuesta,
    correcta
):
    """
    Retorna True si la respuesta coincide
    con la clasificación correcta.
    """

    return respuesta == correcta


# ==========================================================
# FEEDBACK IHH
# ==========================================================

def feedback_ihh(
    valor,
    percentil
):
    """
    Genera una explicación automática
    para el IHH.
    """

    categoria = clasificar_ihh(
        valor
    )

    mensaje = (
        f"El IHH del caso es {valor:.2f}. "
        f"Con los umbrales configurados en esta versión, "
        f"corresponde a '{categoria}'. "
        f"Además, el caso está aproximadamente en el "
        f"percentil {percentil:.2f} de la distribución simulada."
    )

    return mensaje


# ==========================================================
# FEEDBACK RELATIVO
# ==========================================================

def feedback_relativo(
    indicador,
    valor,
    percentil
):
    """
    Feedback provisional para indicadores
    cuyos umbrales teóricos todavía no
    han sido definidos.
    """

    categoria = clasificar_percentil(
        percentil
    )

    mensaje = (
        f"El valor de {indicador} es {valor:.4f}. "
        f"Su posición relativa corresponde al percentil "
        f"{percentil:.2f}. "
        f"Por lo tanto se clasifica como "
        f"'{categoria}' dentro de las simulaciones realizadas. "
        f"Esta clasificación es relativa y debe reemplazarse "
        f"por los umbrales teóricos utilizados en la asignatura."
    )

    return mensaje