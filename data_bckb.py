import pandas as pd
import local_p as lp
import streamlit as st

r_weight_m = {
	"Criteria": ["Project_size", "Inv_system", "O&M_Costs", "Inv_O&M _sewage", "Management_O&M_KN", "Peri-urban_exp_areas", "Reuse", "Sew_cover", "Cent_level", "Area", "Dist_treatment_point", "Topography", "Agriculture", "Aquaculture", "Energy availability", "Environmental risk", "Population size", "Population density", "Nutrient recycling", "Water availability", "Sludge production", "Smell_noise", "TSS", "VSS", "COD", "BOD5", "TN", "TP", "NH4+", "NO3-", "PO43-", "Coliform", "E.Coli"],
	"CW": [0, 0.5, 0.75, 0.25, 0.75, 1, 0.75, 0.25, 0.25, 0.25, 0.75, 1, 1, 0.75, 1, 0.75, 0.5, 0.25, 1, 0.75, 0.75, 0.25, 0.75, 0.75, 0.5, 0.75, 0.5, 0.25, 0.75, 0.5, 0.25, 0.75, 0.75],
	"UASB": [0, 0.5, 0.75, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.25, 0.75, 0.5, 0.75, 0.5, 0.75, 0.5, 0.75, 0.5, 0.5, 0.5, 0.5, 0.75, 0.75, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5],
	"SBR": [0, 0.25, 0, 0.75, 0.25, 0.25, 0.75, 0.75, 0.5, 1, 0.25, 0.25, 0.5, 0.25, 0, 0.75, 0.75, 0.75, 0.25, 0.25, 0.25, 0.75, 0.75, 0.75, 0.75, 1, 0.75, 0.5, 1, 0.5, 0.25, 0.75, 0.75],
	"VF": [0, 0.75, 0.75, 0.5, 0.75, 0.75, 0.5, 0.25, 0.25, 0.5, 0.5, 0.5, 0.75, 0.5, 0.75, 0.75, 0.25, 0.25, 0.75, 0.5, 1, 1, 0.75, 0.75, 0.5, 0.75, 0.5, 0.25, 0.5, 0.25, 0.25, 0.75, 0.75],
	"AF": [0, 0.75, 0.5, 0.5, 0.75, 0.75, 0.5, 0.25, 0.25, 0.5, 0.5, 0.25, 0.5, 0.25, 0.75, 0.5, 0.25, 0.25, 0.5, 0.25, 0.5, 0.75, 0.75, 0.5, 0.75, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5],
	"RBC": [0, 0.5, 0.5, 0.75, 0.25, 0.25, 0.75, 0.75, 0.5, 0.75, 0.25, 0.25, 0.5, 0.25, 0.5, 0.75, 0.5, 0.5, 0.25, 0.25, 0.25, 0.75, 0.5, 0.5, 0.75, 1, 0.5, 0.25, 0.75, 0.25, 0.25, 0.5, 0.5],
	"SAS": [0, 0.75, 0.75, 1, 1, 0.5, 0.25, 0, 0, 0.25, 0, 0.5, 0.25, 0, 1, 0, 0.25, 0, 0.5, 0.75, 0.5, 0.25, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.75, 0.75],
	"MBR": [0, 0, 0, 1, 0, 0, 1, 1, 0.75, 1, 0, 0.25, 0.75, 0.5, 0, 1, 1, 1, 0.25, 0.25, 0.25, 0.75, 1, 1, 1, 1, 0.75, 0.75, 1, 0.5, 0.5, 1, 1],
	"Variable": ["Proj_type", "Stratum", "Stratum", "Sew_Dist", "Urb_area", "Peri_urb", "Green_areas", "Sew_Dist", "Urb_Lay", "Area", "Dist_ptar", "Slope", "Ag_zone", "Aq_zone", "En_grid", "Green_areas", "Population", "Population_den", "Ag_zone", "Sup_grid", "Dist_road", "Res_zone", "Proj_type", "Proj_type", "Proj_type", "Proj_type", "Proj_type", "Proj_type", "Proj_type", "Proj_type", "Proj_type", "Proj_type", "Proj_type"],
	"Inverse": [False, True, True, False, True, False, False, False, False, True, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
}

i_ranges_df = {
	"Variable": ["Proj_type", "Stratum", "Stratum", "Sew_Dist", "Urb_area", "Peri_urb", "Green_areas", "Sew_Dist", "Urb_Lay", "Area", "Dist_ptar", "Slope", "Ag_zone", "Aq_zone", "En_grid", "Green_areas", "Population", "Population_den", "Ag_zone", "Sup_grid", "Dist_road", "Res_zone", "Proj_type", "Proj_type", "Proj_type", "Proj_type", "Proj_type", "Proj_type", "Proj_type", "Proj_type", "Proj_type", "Proj_type", "Proj_type"],
	"Max": [1, 6, 6, 2000, 1, 1, 5000, 2000, 1, 4000, 10000, 5, 1, 1, 2000, 5000, 5000, 500, 1, 5000, 5000, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	"Min": [0, 1, 1, 0, 0, 0, 0, 0, 0, 20, 0, 1, 0, 0, 0, 0, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

r_weight = pd.DataFrame(r_weight_m).set_index("Criteria")

#Ranges for normalization process

ind_range = pd.DataFrame(i_ranges_df).set_index("Variable")

#Managing the absolute weights of each indicator

ind_data = pd.DataFrame(r_weight_m).set_index("Variable")

ind_data['Value'] = 0
ind_data = ind_data[['Inverse','Value']]

def evaluate_ind(params):
    #stratum = lp.read_stratum(params['point'],params['st_layer'])

    #if stratum == 0:
    #    stratum = "Zona industrial/commercial"

    #d_road = lp.nearest_shape(params['point'],params['roads'])
    #d_parks = lp.nearest_shape(params['point'],params['parks'])
    #zone = lp.read_zone(params['point'],params['zoning'])
    
    p_type(params['project type'])

    values = {
        'Proj_type': 1,
        'Stratum': 1,
        'Sew_Dist': 1000,
        'Urb_area': 0,
        'Peri_urb': 1,
        'Green_areas': 1,
        'Urb_Lay': 0,
        'Area': 2000,
        'Dist_ptar': 5000,
        'Slope': 2,
        'Ag_zone': 0,
        'Aq_zone': 0,
        'En_grid': 1000,
        'Population': 1000,
        'Population_den': 400,
        'Sup_grid': 2000,
        'Dist_road': 1000,
        'Res_zone': 1.
    }

    values = pd.DataFrame([values],index= ['Value']).T
    ind_data.update(values)
    n_data = norm_criteria(ind_data, ind_range)
    final_weighted_matrix = t_weight(n_data, r_weight)
    final_score = final_weighted_matrix.sum().reset_index()
    final_score.columns = ['System','Final Score']
    final_score = final_score.sort_values(by= 'Final Score', ascending= False)

    st.write("Value results:", n_data)
    st.write("Weighted Results:", final_weighted_matrix)
    st.write("Final Scores:", final_score)

    #st.write(f'Estrato: {stratum}')
    #st.write(f'Zone: {zone}')
    #st.write(f'Distancia hasta la via mas cercana: {d_road}')
    #st.write(f'Distancia a la zona verde mas cercana: {d_parks}')
    #st.write(r_weight)

def t_weight(n_data, r_weights):
    # 1. Filter for numbers
    r_numeric = r_weights.select_dtypes(include=['number'])
    
    # 2. Check dimensions
    if len(n_data) != len(r_numeric):
        msg = f"Row mismatch! Weights: {len(r_numeric)}, Normalized: {len(n_data)}"
        st.error(msg)
        st.stop() # Prevents the return error entirely
    
    # 3. Perform multiplication using .values to bypass index alignment
    # Ensure n_data has the column 'N_Data' as expected
    r_matrix = r_numeric.multiply(n_data['N_Data'].values, axis=0)
    
    return r_matrix

def norm_criteria(ind_data, ranges_df):
    """
    Normalizes indicators even with duplicate names, using a separate ranges table.
    
    Parameters:
    - ind_data: DataFrame with 'Value' column and 'Inverse' logic. Index is Indicator names.
    - ranges_df: DataFrame with unique 'min' and 'max' per Indicator. Index is Indicator names.
    - direction_col: The column name that holds 'normal' or 'inverse' strings.
    """
    # 1. Create a copy to avoid modifying the original data
    df = ind_data.copy()
    
    v_min = ranges_df['Min'].values
    v_max = ranges_df['Max'].values
    v_actual = df['Value'].values

    # Perform the element-wise calculation
    normalized_values = (v_actual - v_min) / (v_max - v_min)

    inv_mask = df['Inverse'].values
    normalized_values[inv_mask] = 1 - normalized_values[inv_mask]

    df['N_Data'] = normalized_values

    return df

def p_type(pr_type):
    match str(pr_type):
        case "Vivienda Unifamiliar":
            pt_rw = {"CW": 0.1,"UASB":0.25,"SBR":0.1,"VF":0.2,"AF":0.5,"RBC":0.15,"SAS":0.5,"MBR":0}
        case "Edificio Residencial":
            pt_rw = {"CW": 0,"UASB":0.05,"SBR":0.3,"VF":0.05,"AF":0.1,"RBC":0.2,"SAS":0.1,"MBR":0.3}
        case "Barrio":
            pt_rw = {"CW": 0.2,"UASB":0.15,"SBR":0.1,"VF":0.2,"AF":0.05,"RBC":0.15,"SAS":0.05,"MBR":0.15}
        case "Urbanismo":
            pt_rw = {"CW": 0.3,"UASB":0.2,"SBR":0.05,"VF":0,"AF":0.05,"RBC":0.05,"SAS":0,"MBR":0.15}

    pt_rw = pd.DataFrame([pt_rw],index=["Project_size"])
    r_weight.update(pt_rw)

    return 1