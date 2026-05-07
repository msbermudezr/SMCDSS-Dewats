import geopandas as gpd
from shapely.geometry import Point
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
                return "Area fuera de rango / Industrial / Comercial"

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