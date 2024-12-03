import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from io import StringIO
import os
# Set page configuration
st.set_page_config(
    page_title="India Housing & Sanitation Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: black;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric {
        background-color: black;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .plot-container {
        background-color: black;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for data upload and filters
st.sidebar.title("Dashboard Controls")

# Data upload section
st.sidebar.header("Data Upload")
pmay_file = st.sidebar.file_uploader("Upload PMAY Data (CSV)", type=['csv'])
sanitation_file = st.sidebar.file_uploader("Upload Sanitation Data (CSV)", type=['csv'])

@st.cache_data
def load_data(pmay_file, sanitation_file):
    if pmay_file is not None:
        pmay_data = pd.read_csv(pmay_file)
    else:
        # Sample PMAY data
        pmay_data = pd.DataFrame({
            'State': ['Maharashtra', 'Uttar Pradesh', 'Tamil Nadu', 'Gujarat', 'Karnataka'],
            'Houses_Sanctioned': [1200000, 1500000, 800000, 900000, 700000],
            'Houses_Completed': [900000, 1000000, 600000, 750000, 500000],
            'Fund_Utilized_Cr': [15000, 18000, 10000, 12000, 8000],
            'Year': [2023, 2023, 2023, 2023, 2023],
            'Target_Completion_Date': ['2024-12', '2024-12', '2024-12', '2024-12', '2024-12']
        })
    
    if sanitation_file is not None:
        sanitation_data = pd.read_csv(sanitation_file)
    else:
        # Sample sanitation data
        sanitation_data = pd.DataFrame({
            'State': ['Maharashtra', 'Uttar Pradesh', 'Tamil Nadu', 'Gujarat', 'Karnataka'],
            'Toilets_Built': [2000000, 2500000, 1500000, 1800000, 1200000],
            'ODF_Villages': [15000, 20000, 12000, 14000, 10000],
            'Coverage_Percentage': [85, 78, 90, 88, 82],
            'Year': [2023, 2023, 2023, 2023, 2023],
            'Water_Connection_Percentage': [75, 68, 82, 80, 72]
        })
    
    return pmay_data, sanitation_data

# Load data
pmay_data, sanitation_data = load_data(pmay_file, sanitation_file)

# Sidebar filters
st.sidebar.header("Filters")
selected_states = st.sidebar.multiselect(
    "Select States",
    options=pmay_data['State'].unique(),
    default=pmay_data['State'].unique()
)

# Filter data based on selection
filtered_pmay = pmay_data[pmay_data['State'].isin(selected_states)]
filtered_sanitation = sanitation_data[sanitation_data['State'].isin(selected_states)]

# Main dashboard
st.title("🏠 India Housing & Sanitation Analysis Dashboard")
st.markdown("### Monitoring Progress in Housing and Sanitation Initiatives")

# Tabs for different sections
tab1, tab2, tab3, tab4 , tab5= st.tabs(["📊 Overview", "🏘️ PMAY Analysis", "🚽 Sanitation Progress", "📈 Trends & Insights", "📊Comparative Analysis"])

with tab1:
    # Overview metrics with enhanced styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Houses Sanctioned",
            f"{filtered_pmay['Houses_Sanctioned'].sum():,}",
            f"{filtered_pmay['Houses_Sanctioned'].sum() / pmay_data['Houses_Sanctioned'].sum() * 100:.1f}% of national total"
        )
    
    with col2:
        completion_rate = (filtered_pmay['Houses_Completed'].sum() / 
                         filtered_pmay['Houses_Sanctioned'].sum() * 100)
        st.metric(
            "Completion Rate",
            f"{completion_rate:.1f}%",
            f"{completion_rate - 75:.1f}% vs target"
        )
    
    with col3:
        st.metric(
            "Total Toilets Built",
            f"{filtered_sanitation['Toilets_Built'].sum():,}",
            f"Coverage: {filtered_sanitation['Coverage_Percentage'].mean():.1f}%"
        )
    
    with col4:
        water_coverage = filtered_sanitation['Water_Connection_Percentage'].mean()
        st.metric(
            "Water Connection Coverage",
            f"{water_coverage:.1f}%",
            f"{water_coverage - filtered_sanitation['Water_Connection_Percentage'].mean():.1f}% vs national avg"
        )

   # Enhanced Interactive Map of Houses Completed
    st.markdown("### State-wise Housing Completion Analysis")
    
    # Prepare map data
    map_data = pd.DataFrame({
        'State': filtered_pmay['State'],
        'Houses Completed': filtered_pmay['Houses_Completed'],
        'Total Sanctioned': filtered_pmay['Houses_Sanctioned'],
        'Completion Rate': (filtered_pmay['Houses_Completed'] / filtered_pmay['Houses_Sanctioned'] * 100).round(2)
    })
    
    # Map visualization options
    map_metric = st.selectbox(
        "Select Visualization Metric",
        [
            "Houses Completed", 
            "Completion Rate", 
            "Total Sanctioned"
        ]
    )
    
    # Color scale selection
    color_scale = st.selectbox(
        "Choose Color Palette",
        [
            "Viridis", 
            "Plasma", 
            "Inferno", 
            "Magma", 
            "Cividis"
        ]
    )
    
    # Create enhanced choropleth map
    fig = px.choropleth(
        map_data,
        locations='State',
        locationmode='country names',
        color=map_metric,
        hover_name='State',
        hover_data={
            'State': True,
            'Houses Completed': ':.0f',
            'Total Sanctioned': ':.0f',
            'Completion Rate': ':.2f%',
            map_metric: ':.2f'
        },
        color_continuous_scale=color_scale,
        scope='asia',
        title=f'Housing Progress: {map_metric} Across Indian States',
        labels={
            'Houses Completed': 'Houses Completed',
            'Total Sanctioned': 'Total Sanctioned Houses',
            'Completion Rate': 'Completion Rate (%)'
        }
    )
    
    # Customize map layout
    fig.update_layout(
        title_font_size=20,
        title_x=0.5,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        )
    )
    
    # Add detailed annotations
    annotation_text = f"""
    **Analysis Insights:**
    - Metric Shown: {map_metric}
    - Color Palette: {color_scale}
    - Darker/Brighter colors indicate higher values
    - Hover over states for detailed information
    """
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(annotation_text)
    
  

with tab2:
    st.markdown("### PMAY Implementation Analysis")
    
    # Enhanced state selector with metrics
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_state = st.selectbox(
            "Select State for Detailed Analysis",
            filtered_pmay['State'].unique()
        )
        
        state_data = filtered_pmay[filtered_pmay['State'] == selected_state].iloc[0]
        
        # Fund utilization gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = state_data['Fund_Utilized_Cr'],
            delta = {'reference': state_data['Fund_Utilized_Cr'] * 0.8},
            title = {'text': "Fund Utilization (Cr ₹)"},
            gauge = {
                'axis': {'range': [None, state_data['Fund_Utilized_Cr'] * 1.5]},
                'steps': [
                    {'range': [0, state_data['Fund_Utilized_Cr'] * 0.6], 'color': "lightgray"},
                    {'range': [state_data['Fund_Utilized_Cr'] * 0.6, state_data['Fund_Utilized_Cr'] * 0.8], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': state_data['Fund_Utilized_Cr'] * 0.8
                }
            }
        ))
        st.plotly_chart(fig)
    
    with col2:
        # Timeline analysis
        progress_data = pd.DataFrame({
            'Month': pd.date_range(start='2023-01', end=state_data['Target_Completion_Date'], freq='M'),
            'Target': np.linspace(state_data['Houses_Completed'], 
                                state_data['Houses_Sanctioned'], 
                                len(pd.date_range(start='2023-01', 
                                                end=state_data['Target_Completion_Date'], 
                                                freq='M')))
        })
        
        fig = px.line(
            progress_data,
            x='Month',
            y='Target',
            title=f'Project Timeline - {selected_state}',
            labels={'Target': 'Houses to Complete'}
        )
        fig.add_hline(y=state_data['Houses_Completed'], 
                     line_dash="dash", 
                     annotation_text="Current Progress")
        st.plotly_chart(fig)

with tab3:
    st.markdown("### Sanitation Progress Monitoring")
    
    # Enhanced visualization options
    viz_type = st.radio(
        "Select Visualization Type",
        ["Coverage Analysis", "ODF Status", "Water Connection Analysis"]
    )
    
    if viz_type == "Coverage Analysis":
        # Sanitation coverage comparison with water connection
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Sanitation Coverage',
            x=filtered_sanitation['State'],
            y=filtered_sanitation['Coverage_Percentage'],
        ))
        fig.add_trace(go.Bar(
            name='Water Connection',
            x=filtered_sanitation['State'],
            y=filtered_sanitation['Water_Connection_Percentage'],
        ))
        fig.update_layout(
            barmode='group',
            title='Sanitation Coverage vs Water Connection by State',
            yaxis_title='Percentage (%)'
        )
        st.plotly_chart(fig)
        
    elif viz_type == "ODF Status":
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                filtered_sanitation,
                values='ODF_Villages',
                names='State',
                title='Distribution of ODF Villages'
            )
            st.plotly_chart(fig)
        
        with col2:
            fig = px.scatter(
                filtered_sanitation,
                x='Coverage_Percentage',
                y='ODF_Villages',
                size='Toilets_Built',
                color='State',
                title='Correlation: Coverage vs ODF Villages'
            )
            st.plotly_chart(fig)
            
    else:  # Water Connection Analysis
        fig = px.scatter_matrix(
            filtered_sanitation,
            dimensions=['Coverage_Percentage', 'Water_Connection_Percentage', 'ODF_Villages'],
            color='State',
            title='Multi-dimensional Analysis of Sanitation Parameters'
        )
        st.plotly_chart(fig)

with tab4:
    st.markdown("### Trends & Insights")
    
    # Key Performance Indicators
    st.markdown("#### Key Performance Indicators")
    
    # Calculate KPIs
    overall_completion = (filtered_pmay['Houses_Completed'].sum() / 
                        filtered_pmay['Houses_Sanctioned'].sum() * 100)
    avg_fund_utilization = filtered_pmay['Fund_Utilized_Cr'].mean()
    sanitation_coverage = filtered_sanitation['Coverage_Percentage'].mean()
    
    # Display KPIs in cards
    kpi_cols = st.columns(3)
    
    with kpi_cols[0]:
        st.markdown("""
            <div class="metric-card">
                <h4>Overall Completion Rate</h4>
                <h2>{:.1f}%</h2>
                <p>Target: 100%</p>
            </div>
        """.format(overall_completion), unsafe_allow_html=True)
    
    with kpi_cols[1]:
        st.markdown("""
            <div class="metric-card">
                <h4>Average Fund Utilization</h4>
                <h2>₹{:,.0f} Cr</h2>
                <p>Per State</p>
            </div>
        """.format(avg_fund_utilization), unsafe_allow_html=True)
    
    with kpi_cols[2]:
        st.markdown("""
            <div class="metric-card">
                <h4>Average Sanitation Coverage</h4>
                <h2>{:.1f}%</h2>
                <p>Target: 100%</p>
            </div>
        """.format(sanitation_coverage), unsafe_allow_html=True)
    
    # Correlation Analysis
    st.markdown("#### Correlation Analysis")
    
    # Merge datasets for correlation
    merged_data = pd.merge(filtered_pmay, filtered_sanitation, on='State')
    correlation_vars = ['Houses_Completed', 'Fund_Utilized_Cr', 'Coverage_Percentage', 'Water_Connection_Percentage']
    
    fig = px.imshow(
        merged_data[correlation_vars].corr(),
        title='Correlation Matrix of Key Metrics',
        labels=dict(color="Correlation Coefficient"),
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig)

# Footer with data timestamp and download buttons
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d')}*")

with col2:
    if st.button("Download PMAY Analysis Report"):
        # Generate report logic here
        st.download_button(
            label="Download Report",
            data=filtered_pmay.to_csv().encode('utf-8'),
            file_name=f"pmay_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with col3:
    if st.button("Download Sanitation Analysis Report"):
        st.download_button(
            label="Download Report",
            data=filtered_sanitation.to_csv().encode('utf-8'),
            file_name=f"sanitation_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
with tab5:
    if st.button("Go to Next Page"):
        os.system("streamlit run dashboard2.py")
    
    if st.button("Comparative Data Analysis"):
        os.system("streamlit run app.py")