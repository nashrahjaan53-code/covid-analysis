"""
COVID-19 Dashboard
"""
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import COVID19Loader, COVID19Analyzer

st.set_page_config(page_title="COVID-19 Analysis", page_icon="🦠", layout="wide")

@st.cache_resource
def load_analysis():
    loader = COVID19Loader()
    df = loader.load_data()
    return COVID19Analyzer(df)

analyzer = load_analysis()

st.title("🦠 COVID-19 Pandemic Analysis Dashboard")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🌍 Global Trends", "🏥 Country Analysis", "💉 Vaccination"])

with tab1:
    st.header("Global Overview")
    stats = analyzer.get_global_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Cases", f"{stats['total_cases']:,}", "Confirmed")
    with col2:
        st.metric("Total Deaths", f"{stats['total_deaths']:,}", "Fatalities")
    with col3:
        st.metric("Total Recovered", f"{stats['total_recovered']:,}", "Recovered")
    with col4:
        st.metric("Vaccination Rate", stats['vaccination_rate'], "Avg Global")
    
    st.markdown("---")
    
    country_stats = analyzer.get_country_stats()
    fig = px.bar(country_stats.head(10), x='country', y='confirmed_cases',
                title='Top 10 Countries by Cases',
                color_discrete_sequence=['#d62728'])
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Global Trends")
    trends = analyzer.get_trends().dropna()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_cases = px.line(trends, x='date', y='cases_7d_avg',
                           title='7-Day Average Cases',
                           markers=True, color_discrete_sequence=['#1f77b4'])
        st.plotly_chart(fig_cases, use_container_width=True)
    
    with col2:
        fig_deaths = px.line(trends, x='date', y='deaths_7d_avg',
                            title='7-Day Average Deaths',
                            markers=True, color_discrete_sequence=['#d62728'])
        st.plotly_chart(fig_deaths, use_container_width=True)

with tab3:
    st.header("Country Analysis")
    country_stats = analyzer.get_country_stats()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_deaths = px.pie(country_stats.head(8), values='deaths', names='country',
                           title='Deaths Distribution (Top 8 Countries)')
        st.plotly_chart(fig_deaths, use_container_width=True)
    
    with col2:
        fig_recovery = px.bar(country_stats.head(10), x='country', y='recovery_rate',
                             title='Recovery Rate by Country',
                             color_discrete_sequence=['#2ca02c'])
        st.plotly_chart(fig_recovery, use_container_width=True)
    
    st.subheader("Detailed Country Stats")
    st.dataframe(country_stats, use_container_width=True)

with tab4:
    st.header("Vaccination Impact Analysis")
    country_stats = analyzer.get_country_stats()
    
    fig = px.scatter(country_stats, x='vaccinated_pct', y='death_rate',
                    size='confirmed_cases', hover_name='country',
                    title='Vaccination Rate vs Death Rate',
                    color='death_rate', color_continuous_scale='RdYlGn_r')
    st.plotly_chart(fig, use_container_width=True)
    
    corr = analyzer.get_correlation_analysis()
    st.info(f"📌 Correlation between vaccination and death rate: {corr['corr']:.3f}")
