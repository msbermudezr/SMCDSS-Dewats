import geopandas as gpd
from shapely.geometry import Point
import os
import pandas as pd

def read_stratum(my_point: Point, uploaded_file) -> int:
    # 1. OPEN THE "BRIEFCASE": Convert the uploaded file to a GeoDataFrame
    gdf_stratum = gpd.read_file(uploaded_file)
    
    # 2. Prepare your point (Same as your logic)
    point_gdf = gpd.GeoDataFrame(
        index=[0], 
        crs='EPSG:4326', 
        geometry=[my_point]
    ).to_crs('EPSG:3116')

    # 3. Ensure the uploaded data is also in EPSG:3116 for the join
    if gdf_stratum.crs != 'EPSG:3116':
        gdf_stratum = gdf_stratum.to_crs('EPSG:3116')

    # 4. NOW the join will work because 'gdf_stratum' is a GeoDataFrame
    result = gpd.sjoin(point_gdf, gdf_stratum, how="left", predicate="within")
    
    if not result.empty and 'ESTRATO' in result.columns:
        val = result['ESTRATO'].values[0]
        if pd.notna(val):
            return int(val)
            
    return 0

def nearest_road(target_point: Point, uploaded_file) -> float:

    gdf_road = gpd.read_file(uploaded_file)

    point_gdf = gpd.GeoDataFrame(index=[0], crs='EPSG:4326', geometry=[target_point]).to_crs('EPSG:3116')
    result = gpd.sjoin_nearest(point_gdf, gdf_road, distance_col="dist_m")
    
    if not result.empty:
        return float(result['dist_m'].values[0])
    return -1.0

def nearest_park(target_point: Point, uploaded_file) -> float:
    try:

        gdf_park = gpd.read_file(uploaded_file)
        point_gdf = gpd.GeoDataFrame(index=[0], crs='EPSG:4326', geometry=[target_point]).to_crs('EPSG:3116')
        

        result = gpd.sjoin_nearest(point_gdf, gdf_park, distance_col="dist_m")
        
        if not result.empty:
            return float(result['dist_m'].values[0])
    except Exception as e:
        print(f"Error in nearest_park: {e}")
    return -1.0