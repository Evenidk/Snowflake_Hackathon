# PMAY Housing and Sanitation Dashboard

## Project Overview

This project is a comprehensive data analysis and visualization dashboard for the Pradhan Mantri Awas Yojana (PMAY) housing scheme, focusing on housing and sanitation metrics across different regions in India.

- Demo Video Link: https://drive.google.com/file/d/1YKdfFReuSj7EwpT-LJEBgdA4BUu-Ie0b/view?usp=sharing
- Presentation Link: https://drive.google.com/file/d/1-2iPzovNs-GjGWK6envPL_beXz-TATmm/view?usp=sharing

### Key Objectives

- Analyze housing project completion rates
- Assess sanitation infrastructure development
- Provide data-driven insights for resource allocation
- Support sustainable urban development

## Technologies Used

### Backend/Data Processing
- Python
- Pandas
- NumPy
- scikit-learn

### Database
- Snowflake

### Visualization
- Plotly
- Streamlit

### Development Tools
- dotenv
- Virtual environments
- VSCode Snowflake Extension
- PyCharm Snowflake Plugin

## Key Features

1. **Interactive Dashboard**
   - Real-time data display
   - Interactive filtering
   - Comprehensive visualizations

2. **Data Analysis Capabilities**
   - State-wise comparisons
   - Project completion rate analysis
   - Resource allocation insights

3. **Predictive Analytics**
   - Forecasting project completion rates
   - Identifying underperforming regions

## Architecture

### Data Flow
1. Data Ingestion from PMAY and Sanitation Sources
2. Data Processing in Snowflake
3. Transfer to Streamlit via Snowpark API
4. Visualization and Analysis

### Key Components
- Snowflake Database
- Custom ETL Framework
- State-specific Data Validation
- Interactive Streamlit Dashboard

## Main Insights

### Regional Variation in Project Completion
- Significant disparities in housing and sanitation project completion rates
- Top-performing regions like Orissa (100% completion) vs. underperforming regions

### Resource Allocation Impact
- Direct correlation between resource allocation and project success
- Recommendation for milestone-based funding

## Installation

### Prerequisites
- Python 3.8+
- Snowflake Account
- Streamlit
- Plotly
- Required Python packages (see `requirements.txt`)

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/pmay-housing-dashboard.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Set up Snowflake credentials
cp .env.example .env
# Edit .env with your Snowflake credentials
```

## Usage

```bash
# Run the Streamlit dashboard
streamlit run app.py
```

## Error Handling

- Database connection error management
- Data validation checks
- User input validation
- Fallback mechanisms for incomplete data

## Future Improvements

- Advanced predictive analytics
- Mobile responsiveness
- Automated data quality checks
- Machine learning trend analysis

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Swati Sharma - swatishrama2005@gmail.com

## Acknowledgements

- Snowflake Inc.
- Netaji Subhas University of Technology
- Open-source community
