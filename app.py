import os
import streamlit as st
import base64
import google.generativeai as genai
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_drawable_canvas import st_canvas

Expert = " "
profile_imgenh = " "

# Streamlit
st.set_page_config(page_title='Tablero Inteligente')
st.title('Test psicologico')
with st.sidebar:
    st.subheader("Acerca de:")
    st.subheader("Este es el test psicologico HTP donde se analiza el subconsiente por medio de dibujos")
st.subheader("Dibuja una casa, un arbol y una persona")

# Parámetros del canvas
drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 5)
stroke_color = st.color_picker("Color de trazo", "#000000")
bg_color = '#FFFFFF'

# Canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=400,
    drawing_mode=drawing_mode,
    key="canvas",
)

# --- CAMBIO 1: etiqueta actualizada para Google AI Studio ---
ke = st.text_input('Ingresa tu Clave de Google AI Studio')
os.environ['GOOGLE_API_KEY'] = ke
api_key = os.environ['GOOGLE_API_KEY']

# --- CAMBIO 2: configurar el cliente de Gemini ---
if api_key:
    genai.configure(api_key=api_key)

analyze_button = st.button("Analiza la imagen", type="secondary")

if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("Analizando ..."):

        # Convertir el canvas a imagen PIL en RGB
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA').convert('RGB')

        prompt_text = (
            "Analiza la imagen y da un breve texto psicológico en español "
            "basado en la técnica HTP y su interpretación de la imagen."
        )

        # --- CAMBIO 3: llamada a la API de Gemini en lugar de OpenAI ---
        try:
            message_placeholder = st.empty()

            # Gemini acepta la imagen PIL directamente, sin necesidad de base64
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content([prompt_text, input_image])

            full_response = response.text
            message_placeholder.markdown(full_response)

            if Expert == profile_imgenh:
                st.session_state.mi_respuesta = full_response

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

else:
    if not api_key:
        st.warning("Por favor ingresa tu API key de Google AI Studio.")
