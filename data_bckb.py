import pandas as pd
import local_p as lp
import streamlit as st

def evaluate_ind(params):

    r_weight_m = {
        "Criteria": ["Project_size", "Inv_system", "O&M_Costs", "Management_O&M_KN", "Peri-urban_exp_areas", "Reuse", "Sew_cover", "Area", "Dist_treatment_point", "Topography", "Resource Recovery", "Energy availability", "Environmental risk", "Population size", "Social participation", "Population density", "Water stress resilience", "Sludge production", "Smell_noise", "Org_Removal_Eff", "Nut_Removal_Eff", "Pathogen_Inactivation"],
        "CW": [0, 0.5, 0.75, 0.75, 1, 0, 0.25, 0.25, 0.75, 1, 0.75, 1, 0.5, 0.5, 0.75, 0.25, 0.75, 0.75, 0.5, 0.5, 0.25, 0.5],
        "UASB": [0, 0.5, 0.75, 0.75, 0.5, 0, 0.5, 0.5, 0.5, 0.25, 1, 1, 0.5, 0.75, 0.5, 0.5, 0.25, 0.75, 0.5, 0.5, 0.25, 0.5],
        "SBR": [0, 0.25, 0.25, 0.25, 0.25, 0, 0.75, 1, 0.25, 0.25, 0, 0.25, 0.75, 0.75, 0.25, 1, 1, 0.25, 0.75, 1, 1, 0.75],
        "VF": [0, 0.75, 0.75, 0.5, 0.5, 0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 0.25, 0.25, 0.75, 0.25, 0.75, 1, 0.5, 0.75, 0.5, 0.5],
        "AF": [0, 0.75, 0.5, 0.75, 0.75, 0, 0.25, 0.5, 0.5, 0.25, 0.5, 0.75, 0.5, 0.25, 0.5, 0.25, 0.25, 0.75, 0.75, 0.5, 0.25, 0.75],
        "RBC": [0, 0.5, 0.5, 0.75, 0.5, 0, 0.75, 0.75, 0.25, 0.25, 0.25, 0.75, 0.75, 0.5, 0.25, 0.5, 0.25, 0.25, 0.75, 0.5, 0.5, 0.5],
        "SAS": [0, 0.75, 0.75, 1, 0.75, 0, 0.25, 0.25, 0.25, 0.5, 0, 1, 0, 0.25, 0.75, 0.25, 0.75, 0.5, 0.25, 0.5, 0.25, 0.75],
        "MBR": [0, 0.25, 0.25, 0.25, 0.25, 0, 1, 1, 0.5, 0.25, 0, 0.25, 1, 1, 0.25, 1, 1, 0.75, 1, 1, 1, 1],
        "Type": ["Economic", "Economic", "Economic", "Economic", "Economic", "Technical", "Technical", "Technical", "Technical", "Technical", "Technical", "Technical", "Social", "Technical", "Social", "Technical", "Technical", "Technical", "Social", "Technical", "Technical", "Technical"],
        "Variable": ["Proj_type", "Stratum", "Stratum", "Urb_area", "Peri_urb", "Green_areas", "Sew_Dist", "Area", "Dist_ptar", "Slope", "Proj_type", "En_grid", "Green_areas", "Population", "Proj_type", "Population_den", "Sup_grid", "Dist_road", "Res_zone", "Proj_type", "Proj_type", "Proj_type"],
        "Inverse": [False, True, True, False, False, True, False, True, False, True, False, False, False, True, False, False, False, False, False, False, False, False],
    }

    i_ranges_df = {
        "Variable": ["Proj_type", "Stratum", "Stratum", "Urb_area", "Peri_urb", "Green_areas", "Sew_Dist", "Area", "Dist_ptar", "Slope", "Proj_type", "En_grid", "Green_areas", "Population", "Proj_type", "Population_den", "Sup_grid", "Dist_road", "Res_zone", "Proj_type", "Proj_type", "Proj_type"],
        "Max": [1, 6, 6, 1, 1, 5000, 2000, 4000, 30000, 5, 1, 2000, 5000, 5000, 1, 650, 5000, 5000, 1, 1, 1, 1],
        "Min": [0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    }

    r_weight = pd.DataFrame(r_weight_m).set_index("Criteria")

    #Ranges for normalization process

    ind_range = pd.DataFrame(i_ranges_df).set_index("Variable")

    #Managing the absolute weights of each indicator

    ind_data = pd.DataFrame(r_weight_m).set_index("Variable")

    ind_data['Value'] = 0
    ind_data = ind_data[['Inverse','Value']]
    
    p_type(params['project type'], params['population'],r_weight)
    r_type(params['reuse purpose'], r_weight)
    pg_ind(params['contaminants'],params['p_gtrap'],r_weight)

    values = lp.evaluate_values(params)

    Zone = 'Suelo Rural'

    tech_uf(params['av_area'],params['population'],values['Stratum'],params['project type'],Zone,r_weight)

    values = pd.DataFrame([values],index= ['Value']).T
    ind_data.update(values)
    n_data = norm_criteria(ind_data, ind_range)
    calc_pweight(r_weight,params['w_econ'],params['w_tech'],params['w_soc'])
    final_weighted_matrix = t_weight(n_data, r_weight)
    final_score = final_weighted_matrix.sum().reset_index()
    final_score.columns = ['System','Final Score']
    final_score = final_score.sort_values(by= 'Final Score', ascending= False)

    st.write("Value results:", n_data)
    st.write("Weighted Results:", final_weighted_matrix)
    st.write("Final Scores:", final_score)

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

def r_type(r_purpose,r_weight):
    match str(r_purpose):
        case "Urbano Interior (Cisternas, lavado)":
            pt_rw = {"CW": 0,"UASB":0,"SBR":1,"VF":0.75,"AF":0,"RBC":0.5,"SAS":0,"MBR":1}
        case 'Urbano no Potable (Lavado de calles/autos)':
            pt_rw = {"CW": 0.5,"UASB":0.25,"SBR":1,"VF":0.75,"AF":0.25,"RBC":0.75,"SAS":0.25,"MBR":1}
        case "Agricultura no Restringida / Acuicultura":
            pt_rw = {"CW": 0,"UASB":0.25,"SBR":1,"VF":1,"AF":0.25,"RBC":0.75,"SAS":0.25,"MBR":1}
        case "Agricultura Restringida / Acuicultura":
            pt_rw = {"CW": 1,"UASB":0.25,"SBR":1,"VF":1,"AF":0.25,"RBC":0.75,"SAS":0.5,"MBR":1}
        case "Enfriamiento Industrial":
            pt_rw = {"CW": 0,"UASB":0.25,"SBR":0.75,"VF":0,"AF":0.25,"RBC":0.25,"SAS":0,"MBR":1}

    pt_rw = pd.DataFrame([pt_rw],index=["Reuse"])
    r_weight.update(pt_rw)

    return 1

def p_type(pr_type,population,r_weight):
    match str(pr_type):
        case "Unidad Habitacional en Propiedad Horizontal":
            pt_rw = {"CW": 0.25,"UASB":0.75,"SBR":1,"VF":0.75,"AF":1,"RBC":0.5,"SAS":1,"MBR":0}
        case "Predio Residencial con Autonomía de Lote":
            if population < 25:
                pt_rw = {"CW": 0.25,"UASB":0.75,"SBR":0.25,"VF":0.50,"AF":0.75,"RBC":0.5,"SAS":1,"MBR":0}
            else:
                pt_rw = {"CW": 0.75,"UASB":0.25,"SBR":0.75,"VF":0.25,"AF":0.25,"RBC":0.75,"SAS":0.25,"MBR":0.5}
        case "Núcleo Residencial Comunitario":
            pt_rw = {"CW": 0.75,"UASB":0.5,"SBR":0.25,"VF":0.75,"AF":0.25,"RBC":0.75,"SAS":0.25,"MBR":0.75}
        case "Macroproyecto de Desarrollo Urbano":
            pt_rw = {"CW": 0.75,"UASB":0.75,"SBR":0.25,"VF":0,"AF":0.25,"RBC":0.25,"SAS":0,"MBR":0.75}

    pt_rw = pd.DataFrame([pt_rw],index=["Project_size"])
    r_weight.update(pt_rw)

    return 1

def calc_pweight(r_weight, w_econ, w_tech, w_soc):

    pweights = {
        'Economic': w_econ,
        'Technical': w_tech,
        'Social': w_soc
    }
    
    for type in r_weight['Type'].unique():

        columns = r_weight.select_dtypes(include=['number']).columns
        mask = r_weight['Type'] == type
        multiplier = pweights[type]/r_weight['Type'].eq(type).sum()
        r_weight.loc[mask,columns] *= multiplier

    return 1

def pg_ind(contaminants,p_gtrap,r_weight):
    
    for contaminant in contaminants:

        a_ind = []
        current_config = {}

        match contaminant:
            case 'Grasas y Aceites':
                if p_gtrap == False:
                    # Without trap: severe effect over the costs and risks of VF y MBR
                    a_ind = ['O&M_Costs', 'Environmental risk']
                    current_config = {
                        0.60: ['VF', 'MBR'],
                        0.70: ['CW']
                    }
                else:
                    # With trap: the entire system becomes expensive in terms of investment and mantainance
                    a_ind = ['Inv_system', 'O&M_Costs']
                    current_config = {
                        # Solution nature-based: Significant economic effect
                        0.80: ['CW', 'VF'], 
                        # Anaerobic and mechanical systems: Moderate effect
                        0.90: ['UASB', 'AF', 'RBC'], 
                        # High tech: Cheaper trap in comparison with the reactor
                        0.95: ['SBR', 'SAS', 'MBR'] 
                    }

            case 'Solidos Suspendidos Gruesos y Material no Biodegradable':
                a_ind = ['O&M_Costs', 'Environmental risk']
                current_config = {
                    0.60: ['MBR'], # Maximum alert for membrane braiding
                    0.80: ['SBR', 'UASB', 'AF', 'RBC'], # Moderate alert for pump
                    0.95: ['CW', 'VF'] # Almost immune
                }

            case 'Cloro y Desinfectantes':
                a_ind = ['Org_Removal_Eff', 'Pathogen_Inactivation']
                current_config = {
                    0.60: ['VF', 'CW'],   # Macroorganisms are most vulnerable
                    0.80: ['UASB', 'AF'], # Anaerobic sensitivity
                    0.90: ['MBR', 'SBR', 'RBC', 'SAS'] # Volume resilience
                }

            case 'Detergentes y Tensioactivos':
                a_ind = ['Nut_Removal_Eff', 'Environmental risk']
                current_config = {
                    0.80: ['MBR', 'SBR', 'SAS'], # Problems with foam and phosphorus peaks
                    0.75: ['CW'],                # Phosphorus saturation in the filter medium
                    0.90: ['VF', 'UASB', 'AF']   # Minimum impact from foam
                }
            
        for multiplier, techs in current_config.items():
                existing_techs = [t for t in techs if t in r_weight.columns]
                r_weight.loc[a_ind,existing_techs] *= multiplier
    
    return 1

def tech_uf(av_area,e_population,stratum,p_type,zone,r_weight):

    a_ind = ['Inv_system','O&M_Costs','Environmental risk','Sludge production', 'Population size', 'Population density']
    #CW area required per person
    f_cap = 2
    if av_area < f_cap*e_population:
        r_weight.loc[a_ind,'CW'] *= 0.1
    
    if p_type == "Unidad Habitacional en Propiedad Horizontal":
        r_weight.loc[:,'SAS'] = 0
    
    if stratum < 4 and not isinstance(stratum,str):
        r_weight.loc[a_ind,'MBR'] *= 0.1
        r_weight.loc[a_ind,'SBR'] *= 0.1
    
    if zone == "Suelo Rural":
        r_weight.loc[:,'MBR'] *= 0.95
        r_weight.loc[a_ind,'RBC'] *= 0.1
        
    return 1