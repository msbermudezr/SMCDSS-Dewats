import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import st_folium
import folium
import local_p as lp
import data_bckb as db
from shapely.geometry import Point
import time

def notify_on_upload(file_object, key_name):
    """
    Checks if a file is newly uploaded and triggers a toast.
    key_name: a unique string like 'stratum' or 'rivers'
    """
    # Create a unique key in session_state for this specific uploader
    state_key = f"last_file_{key_name}"
    
    if state_key not in st.session_state:
        st.session_state[state_key] = None

    if file_object is not None:
        # Only trigger if the name is different from what we remember
        if st.session_state[state_key] != file_object.name:
            st.toast(f"Layer Loaded: {file_object.name}", icon="✅")
            # Update the 'memory'
            st.session_state[state_key] = file_object.name
            return True
    return False

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="SMCDSS Wastewater Tool", layout="wide")

st.title("♻️🌊 SMCDSS: Sistemas DEWATS")
st.markdown("Algoritmo de soporte para la definición de sistemas descentralizados para la recirculacion de aguas grises")

#SIDEBAR
with st.sidebar:

    st.subheader("📁 Datos Espaciales")

    with st.expander("📍 Estratificacion"):
        gpkg_stratum = st.file_uploader("Select GPKG", type=["gpkg"], key="up_stratum", label_visibility="collapsed")
        notify_on_upload(gpkg_stratum, "stratum")

    with st.expander("🌊 Cuerpos de Agua"):
        gpkg_water = st.file_uploader("Select GPKG", type=["gpkg"], key="up_water", label_visibility="collapsed")
        notify_on_upload(gpkg_water, "water")
    
    with st.expander("🌳​ Zonas Verdes"):
        gpkg_parks = st.file_uploader("Select GPKG", type=["gpkg"], key="up_parks", label_visibility="collapsed")
        notify_on_upload(gpkg_parks, "parks")
    
    with st.expander("🗾​​ Uso de Suelo"):
        gpkg_gzones = st.file_uploader("Select GPKG", type=["gpkg"], key="up_zones", label_visibility="collapsed")
        notify_on_upload(gpkg_gzones, "zoning")

    with st.expander("🛣️​​​ Red Vial"):
        gpkg_roads = st.file_uploader("Select GPKG", type=["gpkg"], key="up_roads", label_visibility="collapsed")
        notify_on_upload(gpkg_roads, "roads")

    with st.expander("🚽 Red de Drenaje"):
        gpkg_sewer = st.file_uploader("Select GPKG", type=["gpkg"], key="up_sewer", label_visibility="collapsed")
        notify_on_upload(gpkg_sewer, "sewer")

    with st.expander("💧 Red de Acueducto"):
        gpkg_supply = st.file_uploader("Select GPKG", type=["gpkg"], key="up_supply", label_visibility="collapsed")
        notify_on_upload(gpkg_supply, "supply")
    
    with st.expander("​💡​ Red de Energia"):
        gpkg_elect = st.file_uploader("Select GPKG", type=["gpkg"], key="up_elect_n", label_visibility="collapsed")
        notify_on_upload(gpkg_elect, "elect_n")

    with st.expander("​🏬​​ PTAR's Ubicación"):
        gpkg_ptar = st.file_uploader("Select GPKG", type=["gpkg"], key="up_ptar", label_visibility="collapsed")
        notify_on_upload(gpkg_ptar, "ptar")    

    st.divider()

    #SIDEBAR: RELATIVE WEIGHTS
    st.header("Pesos Relativos (%)")
    st.info("La suma debe ser 100%")
    
    w_econ = st.slider("Economico", 0, 100, 33)
    w_soc = st.slider("Social", 0, 100, 33)
    w_tech = st.slider("Tecnico", 0, 100, 34)
    
    total_w = w_econ + w_soc + w_tech
    
    if total_w == 100:
        st.success(f"Balance General: {total_w}%")
    else:
        st.error(f"Total: {total_w}%. Favor Ajustar a 100%.")

#SPATIAL DATA (MAP)
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Localización (Bogotá)")
    # Initialize Map at Bogotá Coordinates
    m = folium.Map(location=[4.6097, -74.0817], zoom_start=12)
    
    # Allow user to click and get coordinates
    m.add_child(folium.LatLngPopup())
    map_data = st_folium(m, height=500, width=700)

with col2:

    st.header("Parametros Generales")
    
    # Project Type
    project_options = {
        "Vivienda Unifamiliar": "Single-family Home",
        "Edificio Residencial": "Residential Building",
        "Barrio": "Neighborhood",
        "Urbanismo": "Urban Development"
    }
    project_type = st.selectbox("Project Type / Tipo de Proyecto", options=list(project_options.keys()))

    # Graywater Sources
    graywater_sources = {
        "Lavamanos": "Washbasin / Hand Sink",
        "Ducha": "Shower",
        "Lavadora": "Washing Machine",
        "Lavaplatos": "Kitchen Sink",
        "Sifones de Piso": "Floor Drains",
        "Lavadero": "Laundry Sink"
    }
    # Streamlit Multi-select
    selected_labels = st.multiselect(
        "Seleccione las Fuentes de Agua Gris a Tratar:",
        options=list(graywater_sources.keys()),
        help="Seleccione todas las fuentes de agua que contribuyen al caudal a tratar."
    )

    # Presence of oil
    # Toggle widget acting as the "Flip" button
    grease_present = st.toggle(
        label="Presencia de Grasas o Aceites", 
        value=False,
        help="Active esta opción si el agua a tratar contiene residuos grasos o aceites vegetales/animales."
    )

    # Water Reuse Purpose
    reuse_options = {
        "Descarga de sanitarios": "Toilet flushing",
        "Riego de áreas verdes": "Irrigation",
        "Limpieza de exteriores": "Outdoor cleaning",
        "Uso industrial": "Industrial use"
    }
    reuse_purpose = st.selectbox("Water Reuse / Propósito de Reuso", options=list(reuse_options.keys()))

    st.divider()

    st.subheader("Restricciones Tecnicas")
    # Additional engineering inputs suggested previously
    population = st.number_input(
        "Población Estimada", 
        min_value=1, 
        value=50,
        help= "Indique la población estimada para la cual servira el sistema.")

    available_area = st.number_input(
        "Available Area (m²):", 
        min_value=0.0, 
        step=1.0, 
        help="Espacio total disponible para la construcción del sistema de tratamiento"
    )

    # Display summary of selections for logic verification
    st.write("---")
    st.write("**Resumen:**")
    st.write(f"Tipo: {project_type}")
    st.write(f"Proposito de Reuso: {reuse_purpose}")
    if map_data['last_clicked']:
        st.write(f"Coordenadas: {map_data['last_clicked']['lat']:.4f}, {map_data['last_clicked']['lng']:.4f}")

# --- 5. EXECUTION BUTTON ---
if st.button("Ejecutar Analisis", disabled=(total_w != 100)):
    st.toast('Analisis en Proceso...', icon='⚙️')
    st.write("### Resultados")

    #Getting the coordinates from the user interface
    st.info("Analysis engine is ready to receive data from your backbone...")
    
    if map_data['last_clicked']:

        user_lat = map_data['last_clicked']['lat']
        user_lon = map_data['last_clicked']['lng']
    
        st.write(f"📍 Punto Seleccionado: {user_lat:.4f}, {user_lon:.4f}")
        project_params = {
            'point' : Point(user_lon,user_lat),
            'project type': project_type,
            'reuse options' : reuse_options,
            'grease_p' : grease_present,
            'st_layer' : gpkg_stratum,
            'population' : population,
            'av_area' : available_area,
            'roads' : gpkg_roads,
            'sewage' : gpkg_sewer,
            'parks' : gpkg_parks,
            'supply' : gpkg_supply,
            'ptar' : gpkg_ptar,
            'energy' : gpkg_elect,
            'zoning' : gpkg_gzones,
            'w_bodies': gpkg_water
        }
        db.evaluate_ind(project_params)
    else:
        st.warning("Please click a location on the map to start the analysis.")

    #Call to the logic function
    st.toast('Suitability map generated!', icon='✅')