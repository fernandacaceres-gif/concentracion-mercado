SIMULADOR DE CONCENTRACIÓN DE MERCADO
======================================


DESCRIPCIÓN
-----------

Aplicación web desarrollada en Python y Streamlit
para simular estructuras de mercado mediante el
método de Monte Carlo.

La aplicación permite analizar cuatro indicadores:

- Ratio de Concentración CRk
- Índice Herfindahl-Hirschman (IHH)
- Índice de Dominancia (ID)
- Índice de Entropía (IE)


ESTRUCTURA DEL PROYECTO
-----------------------

app.py
Interfaz principal desarrollada en Streamlit.

indicadores.py
Contiene las funciones matemáticas para calcular
los indicadores de concentración.

simulacion.py
Contiene la generación de cuotas aleatorias,
la simulación Monte Carlo y el cálculo de percentiles.

evaluador.py
Contiene las funciones utilizadas para clasificar
los resultados y evaluar las respuestas del usuario.

requirements.txt
Contiene las dependencias necesarias para ejecutar
la aplicación.


REQUISITOS
----------

Python 3.10 o superior.


INSTALACIÓN
-----------

Abrir una terminal dentro de la carpeta del proyecto.

Ejecutar:

pip install -r requirements.txt


EJECUCIÓN
---------

Ejecutar:

streamlit run app.py


Streamlit abrirá automáticamente la aplicación
en el navegador.


FUNCIONAMIENTO GENERAL
-----------------------

1. El usuario selecciona el indicador.

2. Define el número de empresas.

3. Define la cantidad de iteraciones.

4. La aplicación genera mercados aleatorios.

5. Para cada mercado calcula el indicador elegido.

6. Los resultados forman una distribución Monte Carlo.

7. El usuario introduce un mercado particular.

8. Se calcula el indicador del caso particular.

9. Se compara el caso con la distribución simulada.

10. Se calcula su percentil.

11. La aplicación pregunta al usuario cómo clasificaría
el nivel de concentración.

12. Se entrega retroalimentación automática.


NOTA
----

La fórmula exacta del Índice de Dominancia y los
umbrales teóricos de clasificación deben verificarse
con los contenidos oficiales de la asignatura.