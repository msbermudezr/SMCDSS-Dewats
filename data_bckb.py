import pandas as pd

r_weight_m = {
	"Variables": ["Inv_system", "O&M_Costs", "Inv_O&M _sewage", "Management_O&M_KN", "Peri-urban_exp_areas", "Reuse", "Sew_cover", "Cent_level", "Area", "Dist_treatment_point", "Topography", "Agriculture", "Aquaculture", "Energy availability", "Environmental risk", "Population size", "Population density", "Nutrient recycling", "Water availability", "Sludge production", "Smell_noise", "TSS", "VSS", "COD", "BOD5", "TN", "TP", "NH4+", "NO3-", "PO43-", "Coliform", "E.Coli"],
	"CW": [0.5, 0.25, 0.75, 0.25, 1, 0.75, 0.25, 0.25, 0.75, 0.75, 1, 1, 0.75, 0, 0.25, 0.5, 0.25, 1, 0.75, 0.25, 0.75, 0.75, 0.75, 0.5, 0.75, 0.5, 0.25, 0.75, 0.5, 0.25, 0.75, 0.75],
	"UASB": [0.5, 0.25, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.25, 0.75, 0.5, 0.25, 0.5, 0.75, 0.5, 0.75, 0.5, 0.5, 0.5, 0.5, 0.75, 0.75, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5],
	"SBR": [0.75, 1, 0.25, 0.75, 0.25, 0.75, 0.75, 0.5, 0, 0.25, 0.25, 0.5, 0.25, 1, 0.25, 0.75, 0.75, 0.25, 0.25, 0.75, 0.25, 0.75, 0.75, 0.75, 1, 0.75, 0.5, 1, 0.5, 0.25, 0.75, 0.75],
	"VF": [0.25, 0.25, 0.5, 0.25, 0.75, 0.5, 0.25, 0.25, 0.5, 0.5, 0.5, 0.75, 0.5, 0.25, 0.25, 0.25, 0.25, 0.75, 0.5, 0, 0, 0.75, 0.75, 0.5, 0.75, 0.5, 0.25, 0.5, 0.25, 0.25, 0.75, 0.75],
	"AF": [0.25, 0.5, 0.5, 0.25, 0.75, 0.5, 0.25, 0.25, 0.5, 0.5, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.5, 0.25, 0.75, 0.5, 0.75, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5],
	"RBC": [0.5, 0.5, 0.25, 0.75, 0.25, 0.75, 0.75, 0.5, 0.25, 0.25, 0.25, 0.5, 0.25, 0.5, 0.25, 0.5, 0.5, 0.25, 0.25, 0.75, 0.25, 0.5, 0.5, 0.75, 1, 0.5, 0.25, 0.75, 0.25, 0.25, 0.5, 0.5],
	"SAS": [0.25, 0.25, 0, 0, 0.5, 0.25, 0, 0, 0.75, 0, 0.5, 0.25, 0, 0, 1, 0.25, 0, 0.5, 0.75, 0.5, 0.75, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.75, 0.75],
	"MBR": [1, 1, 0, 1, 0, 1, 1, 0.75, 0, 0, 0.25, 0.75, 0.5, 1, 0, 1, 1, 0.25, 0.25, 0.75, 0.25, 1, 1, 1, 1, 0.75, 0.75, 1, 0.5, 0.5, 1, 1],
	"Indicator": ["Stratum", "Stratum", "Sew_Dist", "Distrital distance", "Peri-urb distance", "Green areas", "Sew_Dist", "Urb-Lay", "Area", "Distance to PTAR's", "Slope", "Urban Zoning (Agriculture)", "Urban Zoning (Aquaculture)", "Energy gird", "Green areas", "Population", "Population density", "Urban Zoning (Agriculture-dist)", "Distance to supply grid", "Distance to road network", "Urban Zoning (Residential-dist)", "TSS", "VSS", "COD", "BOD5", "TN", "TP", "NH4+", "NO3-", "PO43-", "Coliform", "E.Coli"],
	"Inverse": [True, True, False, True, False, False, False, False, True, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
}

i_ranges_df = {
	"Indicator": ["Stratum", "Stratum", "Sew_Dist", "Distrital distance", "Peri-urb distance", "Green areas", "Sew_Dist", "Urb-Lay", "Area", "Distance to PTAR's", "Slope", "Urban Zoning (Agriculture)", "Urban Zoning (Aquaculture)", "Energy gird", "Green areas", "Population", "Population density", "Urban Zoning (Agriculture-dist)", "Distance to supply grid", "Distance to road network", "Urban Zoning (Residential-dist)", "TSS", "VSS", "COD", "BOD5", "TN", "TP", "NH4+", "NO3-", "PO43-", "Coliform", "E.Coli"],
	"Max": [6, 6, 2000, 5000, 1000, 5000, 2000, 1000, 4000, 10000, 5, 1, 1, 2000, 5000, 5000, 0, 10000, 5000, 5000, 1000, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	"Min": [1, 1, 0, 0, 0, 0, 0, 0, 20, 0, 1, 0, 0, 0, 0, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

def normalize_sdss_indicators(ind_data, ranges_df, direction_col='Inverse'):
    """
    Normalizes indicators even with duplicate names, using a separate ranges table.
    
    Parameters:
    - ind_data: DataFrame with 'Value' column and 'Inverse' logic. Index is Indicator names.
    - ranges_df: DataFrame with unique 'min' and 'max' per Indicator. Index is Indicator names.
    - direction_col: The column name that holds 'normal' or 'inverse' strings.
    """
    # 1. Create a copy to avoid modifying the original data
    df = ind_data.copy()
    
    # 2. Map the Unique Ranges to the (potentially duplicated) ind_data index
    # This 'broadcasts' the same min/max to every row with the same name
    v_min = df.index.map(ranges_df['min'])
    v_max = df.index.map(ranges_df['max'])
    
    # 3. Apply Linear Normalization
    # We use .sub and .div for alignment safety
    denom = v_max - v_min
    
    # Handle the math
    df['Norm_Score'] = (df['Value'] - v_min) / denom
    
    # 4. Clean up: Handle cases where max == min (division by zero)
    df['Norm_Score'] = df['Norm_Score'].fillna(0).clip(0, 1)
    
    # 5. Apply Inverse Logic (1 - x)
    # Checks if the direction column contains 'inverse' (case-insensitive)
    is_inverse = df[direction_col].astype(str).str.lower() == 'inverse'
    df.loc[is_inverse, 'Norm_Score'] = 1 - df.loc[is_inverse, 'Norm_Score']
    
    return df

r_weight = pd.DataFrame(r_weight_m).set_index("Variables")

#Ranges for normalization process

ind_range = pd.DataFrame(i_ranges_df).set_index("Indicator")

#Managing the absolute weights of each indicator

ind_data = pd.DataFrame(r_weight_m).set_index("Indicator")
ind_data['Value'] = 0
ind_data = ind_data[['Inverse','Value']]

#weighted_scores = 0.5*r_weight.select_dtypes(include=['number'])