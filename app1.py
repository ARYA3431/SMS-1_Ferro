from pulp import *
import pandas as pd
import streamlit as st
from pulp import LpStatus, LpStatusInfeasible

st.title('Ferroalloy Model with Optimal Cost')# :copyright:')
#st.title(':blue[Ferroalloy Model with Optimal Cost]:copyright:')
#st.subheader('Enter the target chemistry')
#st.markdown("<h2 style='text-align: left; color: white; font-size: 18px;'>Enter the target chemistry</h2>", unsafe_allow_html=True)
# st.subheader(':blue[Enter the target chemistry]')

def model():

    #taking cost details from sheet as Dataframe
    cost_df = pd.read_excel('details.xlsx', sheet_name='cost', index_col=0)

    #taking Ferro alloy details from sheet as Dataframe
    FA_df = pd.read_excel('details.xlsx', sheet_name='FA_details')

    # set the 'Ferroalloy' column as the index
    FA_df.set_index('Ferroalloy', inplace=True)

    # Define the problem
    prob1 = LpProblem("LP Problem", LpMinimize)
    prob2 = LpProblem("LP Problem", LpMaximize)

    # Create the variables with the user-defined upper bounds
    SiMn = LpVariable("SiMn", lowBound=0, upBound=SiMn_limit)
    HCMn = LpVariable("HCMn", lowBound=0, upBound=HCMn_limit)
    MCMn = LpVariable("MCMn", lowBound=0, upBound=MCMn_limit)
    LCMn = LpVariable("LCMn", lowBound=0, upBound=LCMn_limit)
    MtMn = LpVariable("MtMn", lowBound=0, upBound=MtMn_limit)
    FeSi = LpVariable("FeSi", lowBound=0, upBound=FeSi_limit)
    CPC = LpVariable("CPC", lowBound=0, upBound=CPC_limit)


    # Define the objective function
    prob1 += cost_df.loc["SiMn", "COST"] * SiMn + \
        cost_df.loc["HCMn", "COST"] * HCMn + \
        cost_df.loc["MCMn", "COST"] * MCMn + \
        cost_df.loc["LCMn", "COST"] * LCMn + \
        cost_df.loc["FeSi", "COST"] * FeSi + \
        cost_df.loc["MtMn", "COST"] * MtMn + \
        cost_df.loc["CPC", "COST"] * CPC
    
      #'''Define the constraints for each elements in ferroalloy'''

        # weight*recovery/100 of C in each ferro alloy
    prob1 += FA_df.loc['SiMn', 'C']*SiMn1*SiMn + \
        FA_df.loc['HCMn','C']*HCMn1*HCMn + \
        FA_df.loc['MCMn', 'C']*MCMn1*MCMn + \
        FA_df.loc['LCMn', 'C']*LCMn1*LCMn + \
        FA_df.loc['FeSi', 'C']*FeSi1*FeSi  + \
        FA_df.loc['MtMn', 'C']*MtMn1*MtMn + \
        FA_df.loc['CPC', 'C']*CPC1*CPC == (filtered_df['c_aim'].iloc[0] - Carbon) * Tap_Weight * 10

# weight*recovery/100 of Si in each ferro alloy  
    prob1 += FA_df.loc['SiMn', 'Si']*SiMn1*SiMn + \
        FA_df.loc['HCMn','Si']*HCMn1*HCMn + \
        FA_df.loc['MCMn', 'Si']*MCMn1*MCMn + \
        FA_df.loc['LCMn', 'Si']*LCMn1*LCMn + \
        FA_df.loc['FeSi', 'Si']*FeSi1*FeSi + \
        FA_df.loc['MtMn', 'Si']*MtMn1*MtMn + \
        FA_df.loc['CPC', 'Si']*CPC1*CPC  == (filtered_df['si_aim'].iloc[0] - Silicon) * Tap_Weight * 10

# weight*recovery/100 of Mn in each ferro alloy 
    prob1 += FA_df.loc['SiMn', 'Mn']*SiMn1*SiMn + \
        FA_df.loc['HCMn','Mn']*HCMn1*HCMn + \
        FA_df.loc['MCMn', 'Mn']*MCMn1*MCMn + \
        FA_df.loc['LCMn', 'Mn']*LCMn1*LCMn + \
        FA_df.loc['FeSi', 'Mn']*FeSi1*FeSi  + \
        FA_df.loc['MtMn', 'Mn']*MtMn1*MtMn + \
        FA_df.loc['CPC', 'Mn']*CPC1*CPC == (filtered_df['mn_aim'].iloc[0]- Manganese) * Tap_Weight * 10

 #weight*recovery/100 of P in each ferro alloy
    prob1 += FA_df.loc['SiMn', 'P']*SiMn1*SiMn + \
        FA_df.loc['HCMn','P']*HCMn1*HCMn + \
        FA_df.loc['MCMn', 'P']*MCMn1*MCMn + \
        FA_df.loc['LCMn', 'P']*LCMn1*LCMn + \
        FA_df.loc['FeSi', 'P']*FeSi1*FeSi  + \
        FA_df.loc['MtMn', 'P']*MtMn1*MtMn + \
        FA_df.loc['CPC', 'P']*CPC1*CPC <= (filtered_df['p_aim'].iloc[0]- Phosphorus) * Tap_Weight * 10
    
# weight*recovery/100 of S in each ferro alloy0
    prob1 += FA_df.loc['SiMn', 'S']*SiMn1*SiMn + \
        FA_df.loc['HCMn','S']*HCMn1*HCMn + \
        FA_df.loc['MCMn', 'S']*MCMn1*MCMn + \
        FA_df.loc['LCMn', 'S']*LCMn1*LCMn + \
        FA_df.loc['FeSi', 'S']*FeSi1*FeSi  + \
        FA_df.loc['MtMn', 'S']*MtMn1*MtMn + \
        FA_df.loc['CPC', 'S']*CPC1*CPC <= (filtered_df['s_aim'].iloc[0] - Sulphur) * Tap_Weight * 10
    
    prob1.solve()

# Print the results
    # if prob1.status == LpStatusInfeasible:
    #     infeasible_reasons = []
    #     for constraint in prob1.constraints.values():
    #         if not constraint.valid():
    #             infeasible_reasons.append(constraint.name)
    #     st.write("Status: Infeasible")
    #     st.write("Infeasible reasons:") 
    #     for reason in infeasible_reasons:
    #         st.write(reason)
    # else:
    #     st.write("Status:", LpStatus[prob1.status])

    st.write("Status: ", LpStatus[prob1.status] )
    st.write("Minimum cost = ", round(value(prob1.objective),0)) #, 'Thank You ! for saving Money :sparkling_heart:')
    st.write("SiMn = ", value(SiMn.varValue),"kg")
    st.write("HCMn = ", value(HCMn.varValue),"kg")
    st.write("MCMn = ", value(MCMn.varValue),"kg")
    st.write("LCMn = ", value(LCMn.varValue),"kg")
    st.write("FeSi = ", value(FeSi.varValue),"kg")
    st.write("CPC = ", value(CPC.varValue),"kg")
    st.write("MtMn = ", value(MtMn.varValue),"kg")  

############################## this is all for maximum   ###########################

    # Define the objective function
    prob2 += cost_df.loc["SiMn", "COST"] * SiMn + \
        cost_df.loc["HCMn", "COST"] * HCMn + \
        cost_df.loc["MCMn", "COST"] * MCMn + \
        cost_df.loc["LCMn", "COST"] * LCMn + \
        cost_df.loc["FeSi", "COST"] * FeSi + \
        cost_df.loc["MtMn", "COST"] * MtMn + \
        cost_df.loc["CPC", "COST"] * CPC
    
      #'''Define the constraints for each elements in ferroalloy'''

        # weight*recovery/100 of C in each ferro alloy
    prob2 += FA_df.loc['SiMn', 'C']*SiMn1*SiMn + \
        FA_df.loc['HCMn','C']*HCMn1*HCMn + \
        FA_df.loc['MCMn', 'C']*MCMn1*MCMn + \
        FA_df.loc['LCMn', 'C']*LCMn1*LCMn + \
        FA_df.loc['FeSi', 'C']*FeSi1*FeSi  + \
        FA_df.loc['MtMn', 'C']*MtMn1*MtMn + \
        FA_df.loc['CPC', 'C']*CPC1*CPC == (filtered_df['c_aim'].iloc[0] - Carbon) * Tap_Weight * 10

# weight*recovery/100 of Si in each ferro alloy  
    prob2 += FA_df.loc['SiMn', 'Si']*SiMn1*SiMn + \
        FA_df.loc['HCMn','Si']*HCMn1*HCMn + \
        FA_df.loc['MCMn', 'Si']*MCMn1*MCMn + \
        FA_df.loc['LCMn', 'Si']*LCMn1*LCMn + \
        FA_df.loc['FeSi', 'Si']*FeSi1*FeSi + \
        FA_df.loc['MtMn', 'Si']*MtMn1*MtMn + \
        FA_df.loc['CPC', 'Si']*CPC1*CPC  == (filtered_df['si_aim'].iloc[0] - Silicon) * Tap_Weight * 10

# weight*recovery/100 of Mn in each ferro alloy 
    prob2 += FA_df.loc['SiMn', 'Mn']*SiMn1*SiMn + \
        FA_df.loc['HCMn','Mn']*HCMn1*HCMn + \
        FA_df.loc['MCMn', 'Mn']*MCMn1*MCMn + \
        FA_df.loc['LCMn', 'Mn']*LCMn1*LCMn + \
        FA_df.loc['FeSi', 'Mn']*FeSi1*FeSi  + \
        FA_df.loc['MtMn', 'Mn']*MtMn1*MtMn + \
        FA_df.loc['CPC', 'Mn']*CPC1*CPC == (filtered_df['mn_aim'].iloc[0] - Manganese) * Tap_Weight * 10

 #weight*recovery/100 of P in each ferro alloy
    prob2 += FA_df.loc['SiMn', 'P']*SiMn1*SiMn + \
        FA_df.loc['HCMn','P']*HCMn1*HCMn + \
        FA_df.loc['MCMn', 'P']*MCMn1*MCMn + \
        FA_df.loc['LCMn', 'P']*LCMn1*LCMn + \
        FA_df.loc['FeSi', 'P']*FeSi1*FeSi  + \
        FA_df.loc['MtMn', 'P']*MtMn1*MtMn + \
        FA_df.loc['CPC', 'P']*CPC1*CPC <= (filtered_df['p_aim'].iloc[0] - Phosphorus) * Tap_Weight * 10
    
# weight*recovery/100 of S in each ferro alloy0
    prob2 += FA_df.loc['SiMn', 'S']*SiMn1*SiMn + \
        FA_df.loc['HCMn','S']*HCMn1*HCMn + \
        FA_df.loc['MCMn', 'S']*MCMn1*MCMn + \
        FA_df.loc['LCMn', 'S']*LCMn1*LCMn + \
        FA_df.loc['FeSi', 'S']*FeSi1*FeSi  + \
        FA_df.loc['MtMn', 'S']*MtMn1*MtMn + \
        FA_df.loc['CPC', 'S']*CPC1*CPC <= (filtered_df['s_aim'].iloc[0] - Sulphur) * Tap_Weight * 10
    
    status = prob2.solve()

# contraint for reason
    # if prob2.status == LpStatusInfeasible:
    #     infeasible_reasons = []
    #     for constraint in prob2.constraints.values():
    #         if not constraint.valid():
    #             infeasible_reasons.append(constraint.name)
    #     st.write("Status: Infeasible")
    #     st.write("Infeasible reasons:") 
    #     for reason in infeasible_reasons:
    #         st.write(reason)
    # else:
    #     st.write("Status:", LpStatus[prob2.status])
# Print the results
    st.write("Status: ", LpStatus[prob1.status] )
    st.write("Maximum cost = ", round(value(prob1.objective),0)) #, 'Thank You ! for saving Money :sparkling_heart:')
    st.write("SiMn = ", value(SiMn.varValue),"kg")
    st.write("HCMn = ", value(HCMn.varValue),"kg")
    st.write("MCMn = ", value(MCMn.varValue),"kg")
    st.write("LCMn = ", value(LCMn.varValue),"kg")
    st.write("FeSi = ", value(FeSi.varValue),"kg")
    st.write("CPC = ", value(CPC.varValue),"kg")
    st.write("MtMn = ", value(MtMn.varValue),"kg") 
    # if status == pulp.LpStatusInfeasible:
    #     st.write('The problem is infeasible. The following contrain is not satisfied:')
    #     for constraint in prob2.constraints:
    #         if constraint.status == pulp.LpConstraintNotSatisfied:
    #             st.write(constraint.name)

# Create a column for each elements
container = st.container()
with st.container():
   df = pd.read_excel("grade.xlsx")

st.write("Raw Columns:", list(df.columns))

df.columns = df.columns.str.strip().str.lower()

# use lowercase everywhere
df['dolvi grades'] = df['dolvi grades'].astype(str).str.upper()

grade = st.selectbox('Select Grade', df['dolvi grades'].unique())

filtered_df = df[df['dolvi grades'] == grade.upper()]

# all the conditions which causes infeasible result
if filtered_df['si_aim'].iloc[0] == 0:
    # fix simn zero
    filtered_df.loc[filtered_df.index[0], 'si_aim'] = 0.009
else:
    filtered_df.loc[filtered_df.index[0], 'si_aim'] = filtered_df['si_aim'].iloc[0]


min_max_df = pd.DataFrame({
    'Elements': ['Min', 'Max', 'Aim'],
    'C': [filtered_df['c_min'].iloc[0], filtered_df['c_max'].iloc[0], filtered_df['c_aim'].iloc[0]],
    'Mn': [filtered_df['mn_min'].iloc[0], filtered_df['mn_max'].iloc[0], filtered_df['mn_aim'].iloc[0]],
    'S': [filtered_df['s_min'].iloc[0], filtered_df['s_max'].iloc[0], filtered_df['s_aim'].iloc[0]],
    'P': [filtered_df['p_min'].iloc[0], filtered_df['p_max'].iloc[0], filtered_df['p_aim'].iloc[0]],
    'Si': [filtered_df['si_min'].iloc[0], filtered_df['si_max'].iloc[0], filtered_df['si_aim'].iloc[0]],
    'Al': [filtered_df['al_min'].iloc[0], filtered_df['al_max'].iloc[0], filtered_df['al_aim'].iloc[0]],
    'Cr': [filtered_df['cr_min'].iloc[0], filtered_df['cr_max'].iloc[0], filtered_df['cr_aim'].iloc[0]],
    'Cu': [filtered_df['cu_min'].iloc[0], filtered_df['cu_max'].iloc[0], filtered_df['cu_aim'].iloc[0]],
    'V': [filtered_df['v_min'].iloc[0], filtered_df['v_max'].iloc[0], filtered_df['v_aim'].iloc[0]],
    'Ti': [filtered_df['ti_min'].iloc[0], filtered_df['ti_max'].iloc[0], filtered_df['ti_aim'].iloc[0]],
    'Nb': [filtered_df['nb_min'].iloc[0], filtered_df['nb_max'].iloc[0], filtered_df['nb_aim'].iloc[0]],
    'Mo': [filtered_df['mo_min'].iloc[0], filtered_df['mo_max'].iloc[0], filtered_df['mo_aim'].iloc[0]],
    'B': [filtered_df['b_min'].iloc[0], filtered_df['b_max'].iloc[0], filtered_df['b_aim'].iloc[0]],
    'Ca': [filtered_df['ca_min'].iloc[0], filtered_df['ca_max'].iloc[0], filtered_df['ca_aim'].iloc[0]]
})

st.write(min_max_df[['Elements', 'C', 'Mn', 'S', 'P', 'Si', 'Al', 'Cr', 'Cu', 'V', 'Ti', 'Nb', 'Mo', 'B', 'Ca']])

st.markdown("<h2 style='text-align: left; color: white; font-size: 15px;'>Enter the blow end chemistry</h2>", unsafe_allow_html=True)

container = st.container()

col1, col2, col3 = container.columns(3)

Carbon = col1.number_input("C", format="%.3f")
Manganese = col2.number_input("Mn", format="%.3f")
Sulphur = col3.number_input("S", format="%.3f")

col4, col5, col6 = container.columns(3)

Phosphorus = col4.number_input("P", format="%.3f")
Silicon = col5.number_input("Si", format="%.3f")
Tap_Weight = col6.number_input("Tap_Weight", value=350)


if Carbon >= filtered_df['c_aim'].iloc[0]:
    filtered_df.loc[filtered_df.index[0], 'c_aim'] = filtered_df['c_max'].iloc[0]
    filtered_df.loc[filtered_df.index[0], 'c_max'] = filtered_df['c_aim'].iloc[0]


# sidebar function
with st.sidebar:
    st.subheader("Availibility of bunkers:")

    col1, col2 = st.columns(2)

    col1.write("Materials")
    SiMn1 = col1.number_input("SiMn1", min_value=0.0, max_value=1.0, value=1.0, step=1.0)
    HCMn1 = col1.number_input("HCMn1", min_value=0.0, max_value=1.0, value=1.0, step=1.0)
    MCMn1 = col1.number_input("MCMn1", min_value=0.0, max_value=1.0, value=1.0, step=1.0)
    LCMn1 = col1.number_input("LCMn1", min_value=0.0, max_value=1.0, value=1.0, step=1.0)
    MtMn1 = col1.number_input("MtMn1", min_value=0.0, max_value=1.0, value=1.0, step=1.0)
    FeSi1 = col1.number_input("FeSi1", min_value=0.0, max_value=1.0, value=1.0, step=1.0)
    CPC1 = col1.number_input("CPC1", min_value=0.0, max_value=1.0, value=1.0, step=1.0)

    col2.write("Limit")
    SiMn_limit = col2.number_input("SiMn_Limit", value=9999)
    HCMn_limit = col2.number_input("HCMn_Limit", value=9999)
    MCMn_limit = col2.number_input("MCMn_Limit", value=9999)
    LCMn_limit = col2.number_input("LCMn_Limit", value=9999)
    MtMn_limit = col2.number_input("MtMn_Limit", value=9999)
    FeSi_limit = col2.number_input("FeSi_Limit", value=9999)
    CPC_limit = col2.number_input("CPC_Limit", value=9999)

    if SiMn1 == 0:
        SiMn_limit = 0
    if HCMn1 == 0:
        HCMn_limit = 0
    if MCMn1 == 0:
        MCMn_limit = 0
    if LCMn1 == 0:
        LCMn_limit = 0
    if MtMn1 == 0:
        MtMn_limit = 0
    if CPC1 == 0:
        CPC_limit = 0


if st.button("Predict"):
    model()
