import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from indicadores import (
    validar_cuotas,
    calcular_indicador
)

from simulacion import (
    generar_cuotas_aleatorias,
    simulacion_monte_carlo,
    calcular_percentil,
    resumen_simulacion
)

from evaluador import (
    clasificar_ihh,
    clasificar_percentil,
    evaluar_respuesta,
    feedback_ihh,
    feedback_relativo
)


# ==========================================================
# CONFIGURACIÓN DE STREAMLIT
# ==========================================================

st.set_page_config(
    page_title=
        "Simulador de Concentración de Mercado",

    page_icon="📊",

    layout="wide"
)


# ==========================================================
# TÍTULO
# ==========================================================

st.title(
    "📊 Simulador de Concentración de Mercado"
)


st.write(
    """
    Esta aplicación permite simular diferentes
    estructuras de mercado mediante el método de
    Monte Carlo y comparar un mercado particular
    con la distribución obtenida.
    """
)



# ==========================================================
# 1. CONFIGURACIÓN
# ==========================================================

st.header(
    "1. Configuración"
)


col_a, col_b = st.columns(2)


# ----------------------------------------------------------
# INDICADOR
# ----------------------------------------------------------

with col_a:

    indicador = st.selectbox(
        "Indicador de concentración",
        [
            "IHH",
            "CRk",
            "ID",
            "IE"
        ]
    )


# ----------------------------------------------------------
# NÚMERO DE EMPRESAS
# ----------------------------------------------------------

with col_b:

    n_empresas = st.number_input(
        "Número de empresas (N)",
        min_value=2,
        max_value=100,
        value=5,
        step=1
    )


n_empresas = int(
    n_empresas
)


# ==========================================================
# CONFIGURACIÓN CRk
# ==========================================================

k = min(
    4,
    n_empresas
)


if indicador == "CRk":

    k = st.number_input(
        "Valor de k para CRk",
        min_value=1,
        max_value=n_empresas,
        value=min(
            4,
            n_empresas
        ),
        step=1
    )

    k = int(k)


# ==========================================================
# ITERACIONES
# ==========================================================

iteraciones = st.number_input(
    "Número de iteraciones Monte Carlo",
    min_value=100,
    max_value=20000,
    value=1000,
    step=100
)


iteraciones = int(
    iteraciones
)


st.info(
    """
    La aplicación utiliza 1.000 iteraciones por
    defecto.

    Aumentar el número de iteraciones puede producir
    una distribución empírica más estable, pero también
    aumenta el tiempo de procesamiento y el consumo
    de recursos.
    """
)


if iteraciones > 5000:

    st.warning(
        """
        ⚠️ Has seleccionado más de 5.000 iteraciones.

        La simulación puede tardar más en ejecutarse.
        """
    )


# ==========================================================
# SEMILLA ALEATORIA
# ==========================================================

usar_semilla = st.checkbox(
    "Usar semilla para reproducir la simulación"
)


semilla = None


if usar_semilla:

    semilla = int(

        st.number_input(
            "Semilla aleatoria",
            min_value=0,
            value=123,
            step=1
        )

    )


# ==========================================================
# BOTÓN MONTE CARLO
# ==========================================================

if st.button(
    "🎲 Ejecutar simulación Monte Carlo",
    type="primary"
):

    with st.spinner(
        "Ejecutando simulación..."
    ):

        try:

            resultados = (
                simulacion_monte_carlo(

                    n_empresas=n_empresas,

                    indicador=indicador,

                    iteraciones=iteraciones,

                    k=k,

                    semilla=semilla
                )
            )


            # Guardamos resultados
            st.session_state[
                "resultados"
            ] = resultados


            # Guardamos configuración
            st.session_state[
                "sim_config"
            ] = {

                "indicador":
                    indicador,

                "n_empresas":
                    n_empresas,

                "k":
                    k,

                "iteraciones":
                    iteraciones
            }


            # Eliminamos resultados antiguos
            st.session_state.pop(
                "valor_caso",
                None
            )


            st.session_state.pop(
                "cuotas_caso",
                None
            )


            st.success(
                "Simulación completada."
            )


        except ValueError as error:

            st.error(
                str(error)
            )


# ==========================================================
# 2. RESULTADOS MONTE CARLO
# ==========================================================

if (
    "resultados"
    in st.session_state
):

    resultados = (
        st.session_state[
            "resultados"
        ]
    )


    config = (
        st.session_state[
            "sim_config"
        ]
    )


    st.header(
        "2. Resultados de Monte Carlo"
    )


    resumen = resumen_simulacion(
        resultados
    )


    c1, c2, c3, c4, c5 = (
        st.columns(5)
    )


    c1.metric(
        "Promedio",
        f"{resumen['promedio']:.4f}"
    )


    c2.metric(
        "Mediana",
        f"{resumen['mediana']:.4f}"
    )


    c3.metric(
        "Desv. estándar",
        f"{resumen['desviacion']:.4f}"
    )


    c4.metric(
        "Mínimo",
        f"{resumen['minimo']:.4f}"
    )


    c5.metric(
        "Máximo",
        f"{resumen['maximo']:.4f}"
    )


    # ======================================================
    # HISTOGRAMA
    # ======================================================

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    ax.hist(
        resultados,
        bins=30,
        edgecolor="black",
        alpha=0.75
    )


    ax.set_title(
        f"Distribución Monte Carlo - "
        f"{config['indicador']}"
    )


    ax.set_xlabel(
        f"Valor de "
        f"{config['indicador']}"
    )


    ax.set_ylabel(
        "Frecuencia"
    )


    st.pyplot(
        fig
    )


    plt.close(
        fig
    )


# ==========================================================
# 3. CASO PARTICULAR
# ==========================================================

st.header(
    "3. Caso particular"
)


if (
    "resultados"
    not in st.session_state
):

    st.warning(
        """
        Primero debes ejecutar la simulación
        Monte Carlo para comparar un caso particular.
        """
    )


else:

    config = (
        st.session_state[
            "sim_config"
        ]
    )


    # ======================================================
    # COMPROBAR QUE NO HAYA CAMBIADO LA CONFIGURACIÓN
    # ======================================================

    if (

        config["indicador"]
        != indicador

        or

        config["n_empresas"]
        != n_empresas

        or

        config["k"]
        != k

    ):

        st.warning(
            """
            Cambiaste la configuración después de
            ejecutar Monte Carlo.

            Vuelve a ejecutar la simulación antes
            de analizar el caso particular.
            """
        )


    else:

        # ==================================================
        # SELECCIÓN DEL MÉTODO
        # ==================================================

        modo = st.radio(
            "¿Cómo quieres definir las cuotas?",

            [
                "Ingresar manualmente",
                "Generar caso aleatorio"
            ],

            horizontal=True
        )


        cuotas = None


        # ==================================================
        # INGRESO MANUAL
        # ==================================================

        if (
            modo
            == "Ingresar manualmente"
        ):

            st.write(
                """
                Ingresa las cuotas en porcentaje.
                La suma debe ser exactamente 100%.
                """
            )


            porcentajes = []


            columnas = st.columns(2)


            for i in range(
                n_empresas
            ):

                with columnas[
                    i % 2
                ]:

                    valor = (
                        st.number_input(

                            f"Empresa {i + 1} (%)",

                            min_value=0.0,

                            max_value=100.0,

                            value=round(
                                100.0
                                / n_empresas,
                                4
                            ),

                            step=0.1,

                            key=
                                f"cuota_manual_"
                                f"{n_empresas}_"
                                f"{i}"
                        )
                    )


                    porcentajes.append(
                        valor
                    )


            total = float(
                sum(
                    porcentajes
                )
            )


            st.write(
                f"**Total ingresado: "
                f"{total:.4f}%**"
            )


            if not np.isclose(
                total,
                100.0,
                atol=0.01
            ):

                st.warning(
                    """
                    ⚠️ Las cuotas todavía
                    no suman 100%.
                    """
                )


            cuotas = (

                np.array(
                    porcentajes,
                    dtype=float
                )

                / 100.0

            )


        # ==================================================
        # GENERACIÓN ALEATORIA
        # ==================================================

        else:

            if st.button(
                "Generar cuotas aleatorias"
            ):

                st.session_state[
                    "cuotas_generadas"
                ] = (

                    generar_cuotas_aleatorias(
                        n_empresas
                    )

                )


            if (
                "cuotas_generadas"
                in st.session_state
            ):

                cuotas = (

                    st.session_state[
                        "cuotas_generadas"
                    ]

                )


                st.write(
                    "Cuotas generadas:"
                )


                tabla = {

                    f"Empresa {i + 1}":
                        f"{cuota * 100:.2f}%"

                    for i, cuota
                    in enumerate(cuotas)

                }


                st.dataframe(

                    {

                        "Empresa":
                            list(
                                tabla.keys()
                            ),

                        "Cuota":
                            list(
                                tabla.values()
                            )
                    },

                    hide_index=True,

                    use_container_width=True
                )


        # ==================================================
        # ANALIZAR CASO PARTICULAR
        # ==================================================

        if cuotas is not None:

            if st.button(
                "📈 Analizar caso particular"
            ):

                try:

                    cuotas = validar_cuotas(
                        cuotas
                    )


                    valor_caso = (
                        calcular_indicador(

                            cuotas,

                            indicador,

                            k
                        )
                    )


                    st.session_state[
                        "valor_caso"
                    ] = valor_caso


                    st.session_state[
                        "cuotas_caso"
                    ] = cuotas


                    st.success(
                        """
                        Caso particular
                        calculado correctamente.
                        """
                    )


                except ValueError as error:

                    st.error(
                        str(error)
                    )


# ==========================================================
# 4. COMPARACIÓN
# ==========================================================

if (

    "resultados"
    in st.session_state

    and

    "valor_caso"
    in st.session_state

):

    resultados = (

        st.session_state[
            "resultados"
        ]

    )


    valor_caso = (

        st.session_state[
            "valor_caso"
        ]

    )


    percentil = calcular_percentil(

        resultados,

        valor_caso

    )


    st.session_state[
        "percentil"
    ] = percentil


    st.header(
        "4. Comparación con la distribución"
    )


    d1, d2 = st.columns(2)


    d1.metric(

        f"{indicador} del caso",

        f"{valor_caso:.4f}"

    )


    d2.metric(

        "Percentil",

        f"{percentil:.2f}%"

    )


    st.write(

        f"""
        El caso particular está aproximadamente
        en el percentil **{percentil:.2f}**
        de las simulaciones.
        """

    )


    # ======================================================
    # HISTOGRAMA + CASO PARTICULAR
    # ======================================================

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    ax.hist(

        resultados,

        bins=30,

        edgecolor="black",

        alpha=0.75

    )


    ax.axvline(

        valor_caso,

        linestyle="--",

        linewidth=3,

        label="Caso particular"

    )


    ax.set_title(

        f"Distribución Monte Carlo "
        f"y caso particular - "
        f"{indicador}"

    )


    ax.set_xlabel(

        f"Valor de {indicador}"

    )


    ax.set_ylabel(

        "Frecuencia"

    )


    ax.legend()


    st.pyplot(
        fig
    )


    plt.close(
        fig
    )


# ==========================================================
# 5. EVALUADOR
# ==========================================================

if (

    "valor_caso"
    in st.session_state

    and

    "percentil"
    in st.session_state

):

    st.header(
        "5. Evaluador"
    )


    valor_caso = (

        st.session_state[
            "valor_caso"
        ]

    )


    percentil = (

        st.session_state[
            "percentil"
        ]

    )


    # ======================================================
    # EVALUADOR IHH
    # ======================================================

    if indicador == "IHH":

        opciones = [

            "Baja concentración",

            "Concentración moderada",

            "Alta concentración"

        ]


        correcta = clasificar_ihh(
            valor_caso
        )


        respuesta = st.radio(

            """
            ¿Cómo clasificarías
            este mercado según el IHH?
            """,

            opciones,

            index=None

        )


        if st.button(
            "Comprobar respuesta"
        ):

            if respuesta is None:

                st.warning(
                    """
                    Selecciona una alternativa.
                    """
                )


            elif evaluar_respuesta(
                respuesta,
                correcta
            ):

                st.success(
                    "✅ Respuesta correcta."
                )


                st.write(

                    feedback_ihh(

                        valor_caso,

                        percentil

                    )

                )


            else:

                st.error(
                    "❌ Respuesta incorrecta."
                )


                st.write(

                    feedback_ihh(

                        valor_caso,

                        percentil

                    )

                )


        st.caption(

            """
            Los umbrales utilizados aquí
            son configurables.

            Confírmalos con lo visto en la
            asignatura antes de entregar.
            """

        )


    # ======================================================
    # OTROS INDICADORES
    # ======================================================

    else:

        st.warning(

            """
            El enunciado no especifica umbrales
            teóricos para este indicador.

            Por ahora esta versión utiliza una
            clasificación relativa basada en el
            percentil de Monte Carlo.
            """

        )


        opciones = [

            "Baja concentración relativa",

            "Concentración relativa intermedia",

            "Alta concentración relativa"

        ]


        correcta = (
            clasificar_percentil(
                percentil
            )
        )


        respuesta = st.radio(

            """
            ¿Cómo clasificarías la posición
            relativa de este caso?
            """,

            opciones,

            index=None

        )


        if st.button(
            "Comprobar respuesta"
        ):

            if respuesta is None:

                st.warning(
                    """
                    Selecciona una alternativa.
                    """
                )


            elif evaluar_respuesta(
                respuesta,
                correcta
            ):

                st.success(
                    "✅ Respuesta correcta."
                )


                st.write(

                    feedback_relativo(

                        indicador,

                        valor_caso,

                        percentil

                    )

                )


            else:

                st.error(
                    "❌ Respuesta incorrecta."
                )


                st.write(

                    feedback_relativo(

                        indicador,

                        valor_caso,

                        percentil

                    )

                )
