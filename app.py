import streamlit as st
from sklearn.linear_model import LinearRegression, Ridge
import numpy as np
import datetime
import snowflake.connector
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch Snowflake credentials from environment variables
try:
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )
except Exception as e:
    st.error("Could not connect to Snowflake. Please check your credentials and connection settings.")
    st.stop()

# Initialize data variables
pmay_data = None
sanitation_data = None

# Sidebar for navigation with icons for each section
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", [
    "🏠 Overview", 
    "📊 Data Overview", 
    "📈 Visualizations", 
    "🔮 Predictive Analysis", 
    "🆚 Comparative Analysis", 
    "🔧 Resource Allocation Simulation",
    "🎯 SDG Goal Tracker",
    "💡 Insights & Recommendations"
    # "🏠🚿 Combined Insights"
])

# Overview Section with icons and emojis
if section == "🏠 Overview":
    st.title("🏠 Housing and Sanitation Dashboard")
    st.write("### 🌍 Welcome to the PMAY Housing and Sanitation Analysis!")
    st.write(
        "📊 This dashboard provides insights into the PMAY Housing and Sanitation projects, "
        "showing completion rates and predicting future trends. Use the navigation on the left to explore."
    )

# Data Overview Section
if section in ["📊 Data Overview", "📈 Visualizations", "🔮 Predictive Analysis", "🆚 Comparative Analysis", "🔧 Resource Allocation Simulation", "🎯 SDG Goal Tracker"]:
    try:
        # Query PMAY Housing Data
        pmay_query = "SELECT sl_no, district, beneficiary_selection, completed, foundation, lintel, roof, progress_total, unstarted FROM pmay_data;"
        pmay_data = pd.DataFrame(
            conn.cursor().execute(pmay_query).fetchall(),
            columns=['Sl.No', 'District', 'Beneficiary Selection', 'Completed', 'Foundation', 'Lintel', 'Roof', 'Progress Total', 'Unstarted']
        )
        
        # Calculate Completion Rate if data is available
        if not pmay_data.empty:
            pmay_data['Completion Rate (%)'] = (pmay_data['Completed'] / pmay_data['Beneficiary Selection']).fillna(0) * 100

        # Display data in "Data Overview" section only
        if section == "📊 Data Overview":
            st.header("PMAY Housing Data 🏠")
            if pmay_data.empty:
                st.warning("PMAY Housing Data is empty.")
            else:
                st.write(pmay_data)

        # Query Sanitation Data
        sanitation_query = "SELECT state, sanctioned, completed, in_progress FROM sanitation_data;"
        sanitation_data = pd.DataFrame(
            conn.cursor().execute(sanitation_query).fetchall(),
            columns=['State', 'Sanctioned', 'Completed', 'In Progress']
        )

        # Calculate Completion Rate if data is available
        if not sanitation_data.empty:
            sanitation_data['Completion Rate (%)'] = (sanitation_data['Completed'] / sanitation_data['Sanctioned']).fillna(0) * 100

        if section == "📊 Data Overview":
            st.header("Sanitation Data 🚿")
            if sanitation_data.empty:
                st.warning("Sanitation Data is empty.")
            else:
                st.write(sanitation_data)

    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        st.stop()

# Close Snowflake connection after data is fetched
conn.close()

# Visualizations Section
if section == "📈 Visualizations" and pmay_data is not None and sanitation_data is not None:
    st.header("Visualizations 📊")
    if not pmay_data.empty:
        st.subheader("Top 5 Districts by Housing Completion Rate")
        top_districts = pmay_data[['District', 'Completion Rate (%)']].sort_values(by='Completion Rate (%)', ascending=False).head(5)
        st.write(top_districts)
        
        fig_top_districts = px.bar(
            top_districts,
            x='District',
            y='Completion Rate (%)',
            title="Top 5 Districts by Housing Completion Rate",
            hover_data={'Completion Rate (%)': ':.2f'}
        )
        fig_top_districts.update_traces(marker_color='blue')
        st.plotly_chart(fig_top_districts)

    if not sanitation_data.empty:
        st.subheader("Top 5 States by Sanitation Completion Rate")
        top_states = sanitation_data[['State', 'Completion Rate (%)']].sort_values(by='Completion Rate (%)', ascending=False).head(5)
        st.write(top_states)
        
        fig_top_states = px.bar(
            top_states,
            x='State',
            y='Completion Rate (%)',
            title="Top 5 States by Sanitation Completion Rate",
            hover_data={'Completion Rate (%)': ':.2f'}
        )
        fig_top_states.update_traces(marker_color='green')
        st.plotly_chart(fig_top_states)

# Predictive Analysis Section
if section == "🔮 Predictive Analysis" and pmay_data is not None:
    st.header("🔮 Predictive Analysis: Future Completion Rates")

    district_selected = st.selectbox("Select a District for Prediction:", pmay_data['District'].unique())
    district_data = pmay_data[pmay_data['District'] == district_selected]

    if not district_data.empty:
        current_year = datetime.datetime.now().year
        years = np.array([current_year, current_year + 1, current_year + 2, current_year + 3, current_year + 4]).reshape(-1, 1)
        completion_rate = district_data['Completion Rate (%)'].values[0]

        X = np.array([current_year]).reshape(-1, 1)
        y = np.array([completion_rate])
        model = LinearRegression().fit(X, y)

        future_completion_rates = model.predict(years)
        prediction_data = pd.DataFrame({
            'Year': years.flatten(),
            'Predicted Completion Rate (%)': future_completion_rates.flatten()
        })

        st.subheader(f"🔮 Predicted Completion Rates for {district_selected}")
        st.write(prediction_data)

        fig_pred = px.line(
            prediction_data, 
            x='Year', 
            y='Predicted Completion Rate (%)', 
            title=f"Predicted Completion Rates for {district_selected} (Next 5 Years)",
            markers=True
        )
        fig_pred.update_traces(line=dict(color="orange", width=3))
        st.plotly_chart(fig_pred)
    else:
        st.write("No data available for the selected district.")

# Comparative Analysis Section
if section == "🆚 Comparative Analysis" and pmay_data is not None:
    st.header("🆚 Comparative Analysis: Housing Completion Rates by Multiple States or Districts")

    # Multi-select for comparing multiple districts
    selected_districts = st.multiselect("Select Districts for Comparison:", pmay_data['District'].unique())
    comparison_data = pmay_data[pmay_data['District'].isin(selected_districts)]

    if not comparison_data.empty:
        st.write("Comparing Housing Completion Rates for Selected Districts:")
        fig_comparison = px.bar(
            comparison_data,
            x='District',
            y='Completion Rate (%)',
            color='District',
            title="Housing Completion Rates by District",
            labels={'Completion Rate (%)': 'Completion Rate (%)'},
            hover_data={'Completion Rate (%)': ':.2f'}
        )
        st.plotly_chart(fig_comparison)
    else:
        st.write("No data available for the selected districts.")

# Resource Allocation Simulation Section
if section == "🔧 Resource Allocation Simulation" and pmay_data is not None:
    st.header("🔧 Resource Allocation Simulation")

    resource_increase = st.slider("Increase in Resources (%)", 0, 100, 10)
    simulation_data = pmay_data.copy()
    simulation_data['Simulated Completion Rate (%)'] = simulation_data['Completion Rate (%)'] * (1 + resource_increase / 100)

    st.write(f"Simulated Completion Rates with {resource_increase}% Increase in Resources")
    st.write(simulation_data[['District', 'Completion Rate (%)', 'Simulated Completion Rate (%)']])

    fig_simulation = px.bar(
        simulation_data,
        x='District',
        y='Simulated Completion Rate (%)',
        title="Simulated Completion Rates with Resource Increase",
        color='District'
    )
    st.plotly_chart(fig_simulation)

# SDG Goal Tracker Section
if section == "🎯 SDG Goal Tracker" and pmay_data is not None:
    st.header("🎯 Progress Toward UN Sustainable Development Goals (SDGs)")

    sdg_target = 100
    pmay_data['Gap to SDG Target (%)'] = sdg_target - pmay_data['Completion Rate (%)']
    
    st.write("Gap to SDG Target")
    st.write(pmay_data[['District', 'Completion Rate (%)', 'Gap to SDG Target (%)']])

    fig_sdg = px.bar(
        pmay_data,
        x='District',
        y='Gap to SDG Target (%)',
        title="Gap to SDG Target by District",
        color='District'
    )
    st.plotly_chart(fig_sdg)

# Insights & Recommendations Section
if section == "💡 Insights & Recommendations":
    st.header("💡 Key Insights")
    st.write("""
    - **Top District in Housing Completion**: Yadgiri with a completion rate of 58.6%.
    - **Top State in Sanitation Completion**: Orissa with a 100% completion rate.
    - **Low-Performing Areas**: Karnataka (0% sanitation completion) and Davanagere (housing completion at 25.7%).
    """)

    st.header("🔍 Recommendations")
    st.write("""
    - **Increase Resources**: Allocate additional resources and funding to low-performing districts and states to help boost completion rates.
    - **Implement Milestone-Based Monitoring**: Introduce milestone checks and timelines in regions with slow progress to ensure steady improvements.
    - **Replicate Successful Strategies**: Study high-performing areas like Orissa and Yadgiri, identifying their best practices and replicating these in underperforming areas.
    - **Enhance Data Collection**: Improve the frequency and accuracy of data collection for real-time monitoring and timely interventions.
    - **Public Awareness Campaigns**: Raise awareness in low-completion areas about the benefits of sanitation and housing projects to encourage higher participation.
    - **Promote Sustainable Practices**: Encourage the use of sustainable, eco-friendly materials in construction and waste management to align with environmental goals.
    - **Conduct Root Cause Analysis**: Investigate specific challenges in regions with significantly low completion rates to address underlying issues effectively.
    - **Integrate with UN SDGs**: Ensure that project goals are aligned with UN SDG targets, particularly for goals related to clean water, sanitation, and sustainable cities.
    """)

# Combined Housing and Sanitation Analysis Section
if section == "🏠🚿 Combined Insights":
    if pmay_data.empty or sanitation_data.empty:
        st.warning("One or both datasets are empty. Cannot generate Combined Insights.")
    else:
        st.header("🏠🚿 Combined Insights: Housing and Sanitation Completion Rates")

        # Prepare data for merging
        pmay_data_renamed = pmay_data.rename(columns={'District': 'Region'})[['Region', 'Completion Rate (%)']]
        sanitation_data_renamed = sanitation_data.rename(columns={'State': 'Region'})[['Region', 'Completion Rate (%)']]

        # Merge datasets
        combined_data = pd.merge(
            pmay_data_renamed, sanitation_data_renamed, 
            on='Region', suffixes=('_Housing', '_Sanitation'), how='inner'
        )

        # Ensure Completion Rate columns are numeric and handle NaNs
        combined_data[['Completion Rate (%)_Housing', 'Completion Rate (%)_Sanitation']] = combined_data[['Completion Rate (%)_Housing', 'Completion Rate (%)_Sanitation']].apply(pd.to_numeric, errors='coerce').fillna(0)

        # Calculate Infrastructure Completion Index
        combined_data['Infrastructure Completion Index (%)'] = combined_data[['Completion Rate (%)_Housing', 'Completion Rate (%)_Sanitation']].mean(axis=1)

        # Display Metrics
        st.write("### 🌟 Key Metrics")
        st.metric(label="Average Housing Completion Rate", value=f"{combined_data['Completion Rate (%)_Housing'].mean():.2f}%")
        st.metric(label="Average Sanitation Completion Rate", value=f"{combined_data['Completion Rate (%)_Sanitation'].mean():.2f}%")
        st.metric(label="Overall Infrastructure Completion Index", value=f"{combined_data['Infrastructure Completion Index (%)'].mean():.2f}%")

        # Identify High and Low Performers
        high_performers = combined_data[combined_data['Infrastructure Completion Index (%)'] > 75]
        low_performers = combined_data[combined_data['Infrastructure Completion Index (%)'] < 50]

        # Display high and low performers
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🏆 High-Performing Regions (Index > 75%)")
            if not high_performers.empty:
                st.write(high_performers[['Region', 'Infrastructure Completion Index (%)']])
            else:
                st.write("No high-performing regions.")
        with col2:
            st.subheader("⚠️ Low-Performing Regions (Index < 50%)")
            if not low_performers.empty:
                st.write(low_performers[['Region', 'Infrastructure Completion Index (%)']])
            else:
                st.write("No low-performing regions.")

        # Correlation Insights
        correlation = combined_data['Completion Rate (%)_Housing'].corr(combined_data['Completion Rate (%)_Sanitation'])
        st.subheader("🔗 Correlation Between Housing and Sanitation Completion Rates")
        st.write(f"The correlation coefficient between Housing and Sanitation completion rates is: **{correlation:.2f}**")

        # Scatter Plot
        st.subheader("📊 Comparison of Housing and Sanitation Completion Rates by Region")
        fig_combined = px.scatter(
            combined_data,
            x='Completion Rate (%)_Housing',
            y='Completion Rate (%)_Sanitation',
            size='Infrastructure Completion Index (%)',
            color='Region',
            hover_name='Region',
            title="Housing vs Sanitation Completion Rates by Region"
        )
        st.plotly_chart(fig_combined)

        # Classification of Regions
        st.subheader("📍 Classification of Regions Based on Completion Rates")
        conditions = [
            (combined_data['Completion Rate (%)_Housing'] > 75) & (combined_data['Completion Rate (%)_Sanitation'] > 75),
            (combined_data['Completion Rate (%)_Housing'] > 75) & (combined_data['Completion Rate (%)_Sanitation'] <= 75),
            (combined_data['Completion Rate (%)_Housing'] <= 75) & (combined_data['Completion Rate (%)_Sanitation'] > 75),
            (combined_data['Completion Rate (%)_Housing'] <= 75) & (combined_data['Completion Rate (%)_Sanitation'] <= 75)
        ]
        labels = ['Balanced Development', 'Housing Priority', 'Sanitation Priority', 'Needs Improvement']
        combined_data['Category'] = np.select(conditions, labels, default='Undefined')

        # Display categorized data
        st.write("### Region Categories Based on Housing and Sanitation Completion Rates")
        st.write(combined_data[['Region', 'Completion Rate (%)_Housing', 'Completion Rate (%)_Sanitation', 'Category']])

        # Bar Chart for Category Distribution
        fig_category = px.bar(
            combined_data,
            x='Region',
            y='Infrastructure Completion Index (%)',
            color='Category',
            title="Regional Categories Based on Housing and Sanitation Completion Rates",
            labels={'Infrastructure Completion Index (%)': 'Completion Index (%)'}
        )
        st.plotly_chart(fig_category)