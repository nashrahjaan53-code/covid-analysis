"""
COVID-19 Data Loader
Loads and preprocesses COVID-19 data
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

class COVID19Loader:
    def __init__(self, data_path='data/covid_data.csv'):
        self.data_path = data_path
    
    def generate_sample_data(self):
        """Generate realistic COVID-19 sample data"""
        np.random.seed(42)
        
        countries = ['USA', 'India', 'Brazil', 'UK', 'France', 'Germany', 'Italy', 
                    'Spain', 'Canada', 'Australia', 'Japan', 'South Korea']
        
        dates = pd.date_range(start='2020-03-01', end='2024-04-01', freq='D')
        data = []
        
        for country in countries:
            for i, date in enumerate(dates):
                # Realistic COVID trend (peak then decline with seasonality)
                base = 100
                if i < 100:  # Early growth
                    cases = base * (1.1 ** (i / 10))
                elif i < 300:  # First peak
                    cases = base * (1.05 ** (i / 10))
                else:  # Decline
                    cases = base * (0.98 ** ((i - 300) / 20))
                
                # Add seasonality and noise
                seasonality = 50 * np.sin(2 * np.pi * i / 365)
                noise = np.random.normal(0, cases * 0.1)
                
                cases = max(1, cases + seasonality + noise)
                deaths = cases * np.random.uniform(0.001, 0.02)
                vaccinations = max(0, (i - 150) / 365 * 80000) if i > 150 else 0
                vaccinations += np.random.normal(0, vaccinations * 0.1)
                
                data.append({
                    'date': date,
                    'country': country,
                    'confirmed_cases': int(cases),
                    'deaths': int(deaths),
                    'recovered': int(cases * np.random.uniform(0.7, 0.95)),
                    'vaccinations': int(max(0, vaccinations)),
                    'vaccinated_pct': min(90, (i - 150) / 300 * 80) if i > 150 else 0
                })
        
        df = pd.DataFrame(data)
        df.to_csv(self.data_path, index=False)
        print(f"✓ Generated COVID-19 data: {len(df)} records")
        return df
    
    def load_data(self):
        """Load COVID-19 data"""
        if not Path(self.data_path).exists():
            return self.generate_sample_data()
        return pd.read_csv(self.data_path)

class COVID19Analyzer:
    def __init__(self, df):
        self.df = df.copy()
        self.df['date'] = pd.to_datetime(self.df['date'])
    
    def get_global_stats(self):
        """Get global COVID-19 statistics"""
        return {
            'total_cases': int(self.df['confirmed_cases'].sum()),
            'total_deaths': int(self.df['deaths'].sum()),
            'total_recovered': int(self.df['recovered'].sum()),
            'vaccination_rate': f"{self.df['vaccinated_pct'].mean():.1f}%",
            'countries': self.df['country'].nunique(),
            'active_cases': int((self.df['confirmed_cases'] - self.df['deaths'] - self.df['recovered']).sum())
        }
    
    def get_country_stats(self):
        """Get per-country statistics"""
        country_stats = self.df.groupby('country').agg({
            'confirmed_cases': 'sum',
            'deaths': 'sum',
            'recovered': 'sum',
            'vaccinations': 'max',
            'vaccinated_pct': 'max'
        }).reset_index()
        
        country_stats['death_rate'] = (country_stats['deaths'] / country_stats['confirmed_cases'] * 100).round(2)
        country_stats['recovery_rate'] = (country_stats['recovered'] / country_stats['confirmed_cases'] * 100).round(2)
        
        return country_stats.sort_values('confirmed_cases', ascending=False)
    
    def get_trends(self):
        """Get trend data (7-day rolling average)"""
        global_daily = self.df.groupby('date')[['confirmed_cases', 'deaths', 'vaccinations']].sum().reset_index()
        global_daily['cases_7d_avg'] = global_daily['confirmed_cases'].rolling(7).mean()
        global_daily['deaths_7d_avg'] = global_daily['deaths'].rolling(7).mean()
        
        return global_daily
    
    def get_correlation_analysis(self):
        """Analyze correlation between vaccination and mortality"""
        latest = self.df.sort_values('date').drop_duplicates('country', keep='last')
        
        return {
            'corr': latest[['vaccinated_pct', 'death_rate']].corr().iloc[0, 1] if 'death_rate' in latest else 0,
            'data': latest[['country', 'vaccinated_pct', 'confirmed_cases', 'deaths']]
        }
