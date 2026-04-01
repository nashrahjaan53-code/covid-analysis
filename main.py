"""
Main Pipeline
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import COVID19Loader, COVID19Analyzer

def main():
    print("🦠 COVID-19 Analysis Pipeline Starting...")
    
    # Load data
    loader = COVID19Loader()
    df = loader.load_data()
    
    # Analyze
    analyzer = COVID19Analyzer(df)
    
    # Global stats
    stats = analyzer.get_global_stats()
    print(f"\n📊 Global Statistics:")
    print(f"✓ Total Cases: {stats['total_cases']:,}")
    print(f"✓ Total Deaths: {stats['total_deaths']:,}")
    print(f"✓ Total Recovered: {stats['total_recovered']:,}")
    print(f"✓ Vaccination Rate: {stats['vaccination_rate']}")
    print(f"✓ Countries: {stats['countries']}")
    
    # Country stats
    country_stats = analyzer.get_country_stats()
    print(f"\n🌍 Top 5 Countries by Cases:")
    print(country_stats.head()[['country', 'confirmed_cases', 'deaths']].to_string(index=False))
    
    # Trends
    trends = analyzer.get_trends()
    latest_trend = trends.iloc[-1]
    print(f"\n📈 Latest Trend (7-day avg):")
    print(f"✓ Cases: {int(latest_trend['cases_7d_avg']):,.0f}")
    print(f"✓ Deaths: {int(latest_trend['deaths_7d_avg']):,.0f}")
    
    print("\n✅ Pipeline Complete! Start dashboard with: streamlit run dashboard/app.py")

if __name__ == '__main__':
    main()
