import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import io
import seaborn as sns
from scipy import stats

# Set page configuration
st.set_page_config(
    page_title="India Housing & Sanitation Dashboard",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: black;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .st-emotion-cache-1y4p8pa {
        max-width: 100%;
    }
    .trend-up { color: green; }
    .trend-down { color: red; }
    </style>
    """, unsafe_allow_html=True)

# Extended sample data with more metrics
@st.cache_data
def load_data():
    # Enhanced PMAY data
    pmay_data = pd.DataFrame({
        'State': ['Maharashtra', 'Uttar Pradesh', 'Gujarat', 'Tamil Nadu', 'Karnataka'],
        'Houses_Sanctioned': [800000, 1200000, 600000, 500000, 400000],
        'Houses_Completed': [600000, 800000, 450000, 400000, 300000],
        'Fund_Utilized_Cr': [15000, 20000, 12000, 10000, 8000],
        'Year': [2023, 2023, 2023, 2023, 2023],
        'BLC_Houses': [400000, 600000, 300000, 250000, 200000],
        'CLSS_Beneficiaries': [200000, 300000, 150000, 125000, 100000],
        'AHP_Houses': [100000, 150000, 75000, 62500, 50000],
        'ISSR_Houses': [100000, 150000, 75000, 62500, 50000],
        'Average_Construction_Time_Days': [180, 200, 160, 170, 190],
        'Cost_Per_Unit_Lakhs': [3.5, 3.2, 3.8, 3.6, 3.4]
    })
    
    # Enhanced sanitation data
    sanitation_data = pd.DataFrame({
        'State': ['Maharashtra', 'Uttar Pradesh', 'Gujarat', 'Tamil Nadu', 'Karnataka'],
        'Toilet_Coverage': [92, 95, 88, 96, 90],
        'ODF_Villages': [85, 88, 82, 94, 87],
        'Water_Connection': [78, 72, 80, 85, 76],
        'Waste_Management_Score': [75, 70, 78, 82, 73],
        'Community_Toilets': [5000, 8000, 4000, 3500, 3000],
        'Public_Toilets': [2500, 4000, 2000, 1750, 1500],
        'Sewage_Treatment_Capacity_MLD': [2000, 3000, 1500, 1300, 1200],
        'Water_Quality_Index': [85, 82, 88, 90, 86],
        'Behavioral_Change_Index': [78, 75, 80, 82, 77]
    })
    
    return pmay_data, sanitation_data

# Load data
pmay_data, sanitation_data = load_data()

# Sidebar configuration
st.sidebar.header("Dashboard Controls")

# Enhanced filtering options
selected_state = st.sidebar.multiselect(
    "Select States",
    options=pmay_data['State'].unique(),
    default=pmay_data['State'].unique()[:3]
)

analysis_year = st.sidebar.selectbox(
    "Select Analysis Year",
    options=[2023, 2022, 2021],
    index=0
)

scheme_filter = st.sidebar.multiselect(
    "Select Housing Schemes",
    options=['BLC', 'CLSS', 'AHP', 'ISSR'],
    default=['BLC', 'CLSS', 'AHP', 'ISSR']
)

# Data Export Section in Sidebar
st.sidebar.markdown("---")
st.sidebar.header("Export Data")

# Export functionality
def export_data(df, name):
    return df.to_csv(index=False).encode('utf-8')

if st.sidebar.button("Export PMAY Data"):
    csv_pmay = export_data(pmay_data[pmay_data['State'].isin(selected_state)], "pmay")
    st.sidebar.download_button(
        label="Download PMAY CSV",
        data=csv_pmay,
        file_name=f'pmay_data_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv'
    )

if st.sidebar.button("Export Sanitation Data"):
    csv_sanitation = export_data(sanitation_data[sanitation_data['State'].isin(selected_state)], "sanitation")
    st.sidebar.download_button(
        label="Download Sanitation CSV",
        data=csv_sanitation,
        file_name=f'sanitation_data_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv'
    )

# Main dashboard
st.title("🏘️ India Housing & Sanitation Analysis Dashboard")
st.markdown("---")

# Enhanced Key Metrics Display
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sanctioned = pmay_data[pmay_data['State'].isin(selected_state)]['Houses_Sanctioned'].sum()
    st.metric(
        "Total Houses Sanctioned",
        f"{total_sanctioned:,}",
        delta=f"{5}% vs prev year"
    )

with col2:
    total_completed = pmay_data[pmay_data['State'].isin(selected_state)]['Houses_Completed'].sum()
    st.metric(
        "Total Houses Completed",
        f"{total_completed:,}",
        delta=f"{8}% vs prev year"
    )

with col3:
    completion_rate = (total_completed / total_sanctioned * 100)
    st.metric(
        "Completion Rate",
        f"{completion_rate:.1f}%",
        delta=f"{3}% vs prev year"
    )

with col4:
    avg_cost = pmay_data[pmay_data['State'].isin(selected_state)]['Cost_Per_Unit_Lakhs'].mean()
    st.metric(
        "Avg Cost Per Unit",
        f"₹{avg_cost:.2f}L",
        delta=f"-{2}% vs prev year"
    )

# New Section: Scheme-wise Analysis
st.header("Scheme-wise Implementation Analysis")
scheme_cols = ['BLC_Houses', 'CLSS_Beneficiaries', 'AHP_Houses', 'ISSR_Houses']
scheme_data = pmay_data[pmay_data['State'].isin(selected_state)][['State'] + scheme_cols]

# Stacked bar chart for scheme distribution
fig_schemes = go.Figure()
for scheme in scheme_cols:
    fig_schemes.add_trace(go.Bar(
        name=scheme.replace('_', ' '),
        x=scheme_data['State'],
        y=scheme_data[scheme],
    ))

fig_schemes.update_layout(
    barmode='stack',
    title='Scheme-wise Housing Distribution by State',
    height=500
)
st.plotly_chart(fig_schemes, use_container_width=True)

# Statistical Analysis Section
st.header("Statistical Analysis")
tab1, tab2, tab3 = st.tabs(["Correlation Analysis", "Performance Metrics", "Trend Analysis"])

with tab1:
    # Correlation matrix for key metrics
    correlation_data = sanitation_data[['Toilet_Coverage', 'ODF_Villages', 'Water_Connection', 'Water_Quality_Index']]
    correlation_matrix = correlation_data.corr()
    
    fig_correlation = px.imshow(
        correlation_matrix,
        labels=dict(color="Correlation"),
        color_continuous_scale="RdBu",
        title="Correlation Matrix of Sanitation Metrics"
    )
    st.plotly_chart(fig_correlation, use_container_width=True)

with tab2:
    # Performance metrics calculation
    performance_metrics = pd.DataFrame({
        'State': selected_state,
        'Implementation_Efficiency': [
            (pmay_data[pmay_data['State'] == state]['Houses_Completed'].iloc[0] /
             pmay_data[pmay_data['State'] == state]['Houses_Sanctioned'].iloc[0] * 100)
            for state in selected_state
        ],
        'Fund_Utilization_Rate': [
            (pmay_data[pmay_data['State'] == state]['Fund_Utilized_Cr'].iloc[0] /
             pmay_data[pmay_data['State'] == state]['Houses_Sanctioned'].iloc[0] * 100)
            for state in selected_state
        ]
    })
    
    st.dataframe(performance_metrics.style.highlight_max(axis=0), use_container_width=True)

with tab3:
    # Trend analysis visualization
    fig_trends = go.Figure()
    
    for state in selected_state:
        fig_trends.add_trace(go.Scatter(
            x=['2021', '2022', '2023'],
            y=np.random.normal(80, 10, 3),  # Replace with actual trend data
            name=state,
            mode='lines+markers'
        ))
    
    fig_trends.update_layout(
        title='Year-wise Implementation Progress',
        xaxis_title='Year',
        yaxis_title='Implementation Progress (%)'
    )
    st.plotly_chart(fig_trends, use_container_width=True)

# Enhanced Sanitation Analysis
st.header("Enhanced Sanitation Analysis")
col1, col2 = st.columns(2)

with col1:
    # Radar chart for sanitation metrics
    categories = ['Toilet_Coverage', 'ODF_Villages', 'Water_Connection', 'Waste_Management_Score']
    
    fig_radar = go.Figure()
    
    for state in selected_state:
        values = sanitation_data[sanitation_data['State'] == state][categories].iloc[0].tolist()
        values.append(values[0])  # Complete the radar by connecting back to first point
        
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            name=state
        ))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title='Sanitation Metrics Comparison'
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col2:
    # Water quality analysis
    fig_water = px.scatter(
        sanitation_data[sanitation_data['State'].isin(selected_state)],
        x='Water_Quality_Index',
        y='Water_Connection',
        size='Sewage_Treatment_Capacity_MLD',
        color='State',
        title='Water Quality vs Connection Coverage'
    )
    st.plotly_chart(fig_water, use_container_width=True)

# Cost Analysis Section
st.header("Cost and Efficiency Analysis")
cost_data = pmay_data[pmay_data['State'].isin(selected_state)]

fig_cost = px.scatter(
    cost_data,
    x='Average_Construction_Time_Days',
    y='Cost_Per_Unit_Lakhs',
    size='Houses_Completed',
    color='State',
    title='Cost vs Construction Time Analysis',
    labels={
        'Average_Construction_Time_Days': 'Average Construction Time (Days)',
        'Cost_Per_Unit_Lakhs': 'Cost Per Unit (Lakhs)',
        'Houses_Completed': 'Houses Completed'
    }
)
st.plotly_chart(fig_cost, use_container_width=True)

# Footer with additional information
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Data Source: Sample data (Replace with actual data sources)</p>
        <p>Last Updated: {}</p>
        <p>For more information, visit the official PMAY and Swachh Bharat Mission websites</p>
    </div>
""".format(datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)