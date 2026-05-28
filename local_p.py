import geopandas as gpd
from shapely.geometry import Point
import streamlit as st
import os
import pandas as pd

def read_stratum(my_point: Point, uploaded_file):
    
    if uploaded_file is None:
        return "No file uploaded"
    
    try:
        # 1. Converting the uploaded file to a GeoDataFrame
        gdf_stratum = gpd.read_file(uploaded_file)
        
        # 2. Prepare your point 
        point_gdf = gpd.GeoDataFrame(
            index=[0], 
            crs='EPSG:4326', 
            geometry=[my_point]
        ).to_crs('EPSG:3116')

        # 3. Ensuring the uploaded data is also in EPSG:3116 for the join
        if gdf_stratum.crs != 'EPSG:3116':
            gdf_stratum = gdf_stratum.to_crs('EPSG:3116')

        # 4. Joining the data to extract the required attributes
        result = gpd.sjoin(point_gdf, gdf_stratum, how="left", predicate="within")
        
        if not result.empty:
            # Checking if the point actually matched a polygon
            # 'index_right' is created by sjoin; if it's NaN, the point is outside all polygons
            if pd.isna(result['index_right'].values[0]):
                return 0 # Area fuera de rango / Industrial / Comercial

            if 'ESTRATO' in result.columns:
                val = result['ESTRATO'].values[0]
                if pd.notna(val):
                    return int(val)
                else:
                    return "Industrial / Comercial"
    
    except Exception as e:
        print(f'Error handling the file {uploaded_file}')
        return 0
    
    return 0

def read_zone(my_point: Point, uploaded_file) -> str:

    if uploaded_file is None:
        return "No file uploaded"

    try:
        # 1. Converting the uploaded file to a GeoDataFrame
        gdf_zone = gpd.read_file(uploaded_file)
        
        # 2. Preparing the point 
        point_gdf = gpd.GeoDataFrame(
            index=[0], 
            crs='EPSG:4326', 
            geometry=[my_point]
        ).to_crs('EPSG:3116')

        # 3. Ensuring the uploaded data is also in EPSG:3116 for the join
        if gdf_zone.crs != 'EPSG:3116':
            gdf_zone = gdf_zone.to_crs('EPSG:3116')

        # 4. Joining the data to extract the required attributes
        result = gpd.sjoin(point_gdf, gdf_zone, how="left", predicate="within")
        
        if not result.empty and 'CLASE_SUELO' in result.columns:
            val = result['CLASE_SUELO'].values[0]
            if pd.notna(val):
                match int(val):
                    case 1:
                        return "Suelo Urbano"
                    case 2:
                        return "Suelo de Expansión"
                    case 3:
                        return "Suelo Rural"
                    case _:
                        return "Suelo Desconocido"
    
    except Exception as e:
            print(f'Error handling the file {uploaded_file}')
            return 0

    return 0

def nearest_shape(target_point: Point, uploaded_file) -> float:

    if uploaded_file is None:
        return "No file uploaded"

    try:

        gdf_layer = gpd.read_file(uploaded_file)

        if gdf_layer.crs != 'EPSG:3116':
            gdf_layer = gdf_layer.to_crs('EPSG:3116')
        
        point_gdf = gpd.GeoDataFrame(index=[0], crs='EPSG:4326', geometry=[target_point]).to_crs('EPSG:3116')
        

        result = gpd.sjoin_nearest(point_gdf, gdf_layer, distance_col="dist_m")
        
        if not result.empty:
            return float(result['dist_m'].values[0])
    except Exception as e:
        print(f"Error in nearest_shape: {e}")
    return -1.0

def evaluate_values(params):


    zone = read_zone(params['point'],params['zoning'])
    if zone == "Suelo Urbano":
        Urb_area = 1
        Peri_urb = 0
    else:
        Urb_area = 0
        Peri_urb = 1

    stratum = read_stratum(params['point'],params['st_layer'])
    res_zone = 1
    if stratum == 0 and Peri_urb == 0:
        stratum = 6
        res_zone = 0
    elif Peri_urb == 1:
        stratum = 2
        res_zone = 1

    d_road = int(nearest_shape(params['point'],params['roads']))
    d_parks = int(nearest_shape(params['point'],params['parks']))
    d_ptar = int(nearest_shape(params['point'],params['ptar']))
    d_supply = int(d_road*0.5)
    d_energy = int(d_road*1.2)
    d_sewage = int(d_road*0.7)

    #Evaluate typical population densities in accordance with the type of project
    match str(params['project type']):
        case "Unidad Habitacional en Propiedad Horizontal":
            population_density = 40 # Low density, unifamiliar houses/flats
        case "Predio Residencial con Autonomía de Lote":
            population_density = 650 # High vertical density, buildings
        case "Núcleo Residencial Comunitario":
            population_density = 250 # Medium-high consolidated urban density
        case "Macroproyecto de Desarrollo Urbano":
            population_density = 450 # High planned density

    values = {
        'Proj_type': 1,
        'Stratum': stratum,
        'Sew_Dist': d_sewage,
        'Urb_area': Urb_area,
        'Peri_urb': Peri_urb,
        'Green_areas': d_parks,
        'Area': params['av_area'],
        'Dist_ptar': d_ptar,
        'Slope': 2,
        'En_grid': d_energy,
        'Population': params['population'],
        'Population_den': population_density,
        'Sup_grid': d_supply,
        'Dist_road': d_road,
        'Res_zone': res_zone
    }
    return values