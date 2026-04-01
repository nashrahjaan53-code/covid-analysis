# 🦠 COVID-19 Pandemic Analysis

Advanced data analysis of COVID-19 spread, mortality, and vaccination impact globally.

## 📊 Features

- **Time Series Analysis:** Trend detection, moving averages, growth rates
- **Geographical Heatmaps:** Country-level case, death, vaccination data
- **Forecasting:** ARIMA/Prophet predictions for cases/deaths
- **Correlation Analysis:** Vaccination vs mortality patterns
- **Statistical Tests:** Chi-square tests for trend significance

## 🛠️ Tech Stack

- **Data:** Johns Hopkins dataset, COVID tracking API
- **Analysis:** Pandas, NumPy, SciPy  
- **ML:** Scikit-learn, Prophet
- **Visualization:** Plotly, Folium (interactive maps), Seaborn
- **Dashboard:** Streamlit

## 📁 Project Structure

```
covid_analysis/
├── data/
│   └── covid_data.csv
├── src/
│   ├── data_loader.py
│   ├── analysis.py
│   └── utils.py
├── dashboard/
│   └── app.py
├── main.py
└── requirements.txt
```

## 🚀 Quick Start

```bash
cd covid_analysis
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
streamlit run dashboard/app.py
```

## 📈 Key Analysis

- **Global Trends:** Cases, deaths by region
- **Vaccination Impact:** Correlation with mortality decline
- **Growth Rates:** Exponential vs linear trends
- **Forecasting:** 30-day case/death predictions
- **Hotspots:** Current surge regions

## 💼 Portfolio Value

Perfect for: Data Scientist, Epidemiologist, Public Health Analyst roles
