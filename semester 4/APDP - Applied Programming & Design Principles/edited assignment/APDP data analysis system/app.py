"""
Bus Passenger Data Analysis Application
Author: Assignment Solution
Date: July 31, 2025

This application demonstrates Object-Oriented Programming principles including:
- Classes and Inheritance
- Encapsulation and Abstraction
- Design Patterns (Singleton, Strategy, Factory)
- SOLID Principles
- Clean Code Techniques

The application analyzes bus passenger data to provide insights on:
1. Peak Congestion Analysis
2. Popular Route and Transfer Point Analysis
3. Service Disruption Detection
4. Regional Performance Analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union
import warnings
warnings.filterwarnings('ignore')

# =====================================================================
# ABSTRACT BASE CLASSES AND INTERFACES (SOLID - Interface Segregation)
# =====================================================================

class DataAnalyzer(ABC):
    """Abstract base class for all data analyzers - demonstrates abstraction"""
    
    @abstractmethod
    def analyze(self, data: pd.DataFrame) -> Dict:
        """Abstract method that must be implemented by all analyzers"""
        pass
    
    @abstractmethod
    def visualize(self, analysis_result: Dict) -> go.Figure:
        """Abstract method for creating visualizations"""
        pass

class DataFilter(ABC):
    """Abstract base class for data filtering strategies"""
    
    @abstractmethod
    def filter(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """Abstract method for filtering data"""
        pass

# =====================================================================
# CONCRETE FILTER STRATEGIES (STRATEGY PATTERN)
# =====================================================================

class TimeFilter(DataFilter):
    """Concrete filter for time-based filtering"""
    
    def filter(self, data: pd.DataFrame, start_date: str = None, end_date: str = None, 
               hour_range: tuple = None) -> pd.DataFrame:
        filtered_data = data.copy()
        
        if start_date:
            filtered_data = filtered_data[filtered_data['timestamp'] >= start_date]
        if end_date:
            filtered_data = filtered_data[filtered_data['timestamp'] <= end_date]
        if hour_range:
            filtered_data = filtered_data[
                (filtered_data['hour'] >= hour_range[0]) & 
                (filtered_data['hour'] <= hour_range[1])
            ]
        
        return filtered_data

class RegionFilter(DataFilter):
    """Concrete filter for region-based filtering"""
    
    def filter(self, data: pd.DataFrame, regions: List[str] = None) -> pd.DataFrame:
        if regions:
            return data[data['region'].isin(regions)]
        return data

class RouteFilter(DataFilter):
    """Concrete filter for route-based filtering"""
    
    def filter(self, data: pd.DataFrame, routes: List[str] = None) -> pd.DataFrame:
        if routes:
            return data[data['route_id'].isin(routes)]
        return data

# =====================================================================
# DATA PROCESSING CLASS (SINGLE RESPONSIBILITY PRINCIPLE)
# =====================================================================

class DataProcessor:
    """Handles all data loading and preprocessing operations"""
    
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._data = None
        self._processed_data = None
    
    def load_data(self) -> pd.DataFrame:
        """Load data from CSV file with error handling"""
        try:
            self._data = pd.read_csv(self._file_path)
            self._preprocess_data()
            return self._processed_data
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return pd.DataFrame()
    
    def _preprocess_data(self):
        """Private method to preprocess the loaded data"""
        if self._data is not None:
            # Convert timestamp columns
            self._data['timestamp'] = pd.to_datetime(self._data['timestamp'])
            self._data['boarding_time'] = pd.to_datetime(self._data['boarding_time'])
            self._data['alighting_time'] = pd.to_datetime(self._data['alighting_time'])
            
            # Extract time components for analysis
            self._data['hour'] = self._data['timestamp'].dt.hour
            self._data['day'] = self._data['timestamp'].dt.day
            self._data['month'] = self._data['timestamp'].dt.month
            self._data['year'] = self._data['timestamp'].dt.year
            self._data['date'] = self._data['timestamp'].dt.date
            
            # Handle missing values in transfer_station_id
            self._data['transfer_station_id'] = self._data['transfer_station_id'].fillna('No Transfer')
            
            self._processed_data = self._data
    
    @property
    def data(self) -> pd.DataFrame:
        """Getter for processed data - demonstrates encapsulation"""
        return self._processed_data if self._processed_data is not None else pd.DataFrame()

# =====================================================================
# CONCRETE ANALYZER CLASSES (INHERITANCE & POLYMORPHISM)
# =====================================================================

class CongestionAnalyzer(DataAnalyzer):
    """Analyzes peak congestion patterns - implements DataAnalyzer interface"""
    
    def analyze(self, data: pd.DataFrame) -> Dict:
        """Analyze congestion patterns by different time periods"""
        analysis = {}
        
        # Hourly congestion
        hourly_congestion = data.groupby('hour').size().reset_index(name='passenger_count')
        analysis['hourly'] = hourly_congestion
        
        # Daily congestion
        daily_congestion = data.groupby('day_of_week').size().reset_index(name='passenger_count')
        analysis['daily'] = daily_congestion
        
        # Monthly congestion
        monthly_congestion = data.groupby('month').size().reset_index(name='passenger_count')
        analysis['monthly'] = monthly_congestion
        
        # Station congestion (entry and exit)
        entry_congestion = data.groupby('entry_station_id').size().reset_index(name='entries')
        exit_congestion = data.groupby('exit_station_id').size().reset_index(name='exits')
        analysis['stations'] = {'entries': entry_congestion, 'exits': exit_congestion}
        
        return analysis
    
    def visualize(self, analysis_result: Dict) -> Dict[str, go.Figure]:
        """Create visualizations for congestion analysis"""
        figures = {}
        
        # Hourly congestion chart
        fig_hourly = px.bar(
            analysis_result['hourly'], 
            x='hour', 
            y='passenger_count',
            title='🕐 Peak Hours Analysis - Passenger Count by Hour',
            color='passenger_count',
            color_continuous_scale='Viridis'
        )
        fig_hourly.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Number of Passengers",
            template="plotly_white"
        )
        figures['hourly'] = fig_hourly
        
        # Daily congestion chart
        fig_daily = px.pie(
            analysis_result['daily'], 
            values='passenger_count', 
            names='day_of_week',
            title='📅 Weekly Pattern - Passenger Distribution by Day'
        )
        figures['daily'] = fig_daily
        
        # Monthly congestion chart
        fig_monthly = px.line(
            analysis_result['monthly'], 
            x='month', 
            y='passenger_count',
            title='📊 Monthly Trends - Passenger Count by Month',
            markers=True
        )
        fig_monthly.update_layout(template="plotly_white")
        figures['monthly'] = fig_monthly
        
        return figures

class RouteAnalyzer(DataAnalyzer):
    """Analyzes popular routes and transfer points"""
    
    def analyze(self, data: pd.DataFrame) -> Dict:
        """Analyze route popularity and transfer patterns"""
        analysis = {}
        
        # Popular routes
        route_popularity = data.groupby('route_id').size().reset_index(name='passenger_count')
        route_popularity = route_popularity.sort_values('passenger_count', ascending=False)
        analysis['routes'] = route_popularity
        
        # Transfer point analysis
        transfer_data = data[data['transfer_station_id'] != 'No Transfer']
        transfer_popularity = transfer_data.groupby('transfer_station_id').size().reset_index(name='transfer_count')
        transfer_popularity = transfer_popularity.sort_values('transfer_count', ascending=False)
        analysis['transfers'] = transfer_popularity
        
        # Route-Region analysis
        route_region = data.groupby(['route_id', 'region']).size().reset_index(name='count')
        analysis['route_region'] = route_region
        
        return analysis
    
    def visualize(self, analysis_result: Dict) -> Dict[str, go.Figure]:
        """Create visualizations for route analysis"""
        figures = {}
        
        # Top routes bar chart
        top_routes = analysis_result['routes'].head(15)
        fig_routes = px.bar(
            top_routes, 
            x='route_id', 
            y='passenger_count',
            title='🚌 Most Popular Routes - Top 15',
            color='passenger_count',
            color_continuous_scale='Blues'
        )
        fig_routes.update_layout(
            xaxis_title="Route ID",
            yaxis_title="Number of Passengers",
            template="plotly_white"
        )
        figures['routes'] = fig_routes
        
        # Transfer points analysis
        if not analysis_result['transfers'].empty:
            top_transfers = analysis_result['transfers'].head(10)
            fig_transfers = px.bar(
                top_transfers, 
                x='transfer_station_id', 
                y='transfer_count',
                title='🔄 Busiest Transfer Points - Top 10',
                color='transfer_count',
                color_continuous_scale='Reds'
            )
            fig_transfers.update_layout(template="plotly_white")
            figures['transfers'] = fig_transfers
        
        return figures

class DisruptionAnalyzer(DataAnalyzer):
    """Analyzes service disruptions and anomalies"""
    
    def analyze(self, data: pd.DataFrame) -> Dict:
        """Analyze service disruptions and anomalies"""
        analysis = {}
        
        # Anomaly analysis
        anomaly_data = data[data['anomaly_flag'] == True]
        anomaly_by_hour = anomaly_data.groupby('hour').size().reset_index(name='anomaly_count')
        anomaly_by_route = anomaly_data.groupby('route_id').size().reset_index(name='anomaly_count')
        
        analysis['anomalies'] = {
            'by_hour': anomaly_by_hour,
            'by_route': anomaly_by_route,
            'total_anomalies': len(anomaly_data),
            'anomaly_percentage': (len(anomaly_data) / len(data)) * 100
        }
        
        # Service status analysis
        service_status = data.groupby('service_status').size().reset_index(name='count')
        analysis['service_status'] = service_status
        
        # Trip duration analysis (potential disruption indicator)
        avg_duration_by_route = data.groupby('route_id')['trip_duration_minutes'].agg(['mean', 'std']).reset_index()
        analysis['trip_duration'] = avg_duration_by_route
        
        return analysis
    
    def visualize(self, analysis_result: Dict) -> Dict[str, go.Figure]:
        """Create visualizations for disruption analysis"""
        figures = {}
        
        # Anomaly by hour
        fig_anomaly_hour = px.bar(
            analysis_result['anomalies']['by_hour'], 
            x='hour', 
            y='anomaly_count',
            title='⚠️ Service Anomalies by Hour',
            color='anomaly_count',
            color_continuous_scale='Reds'
        )
        fig_anomaly_hour.update_layout(template="plotly_white")
        figures['anomaly_hour'] = fig_anomaly_hour
        
        # Service status pie chart
        fig_status = px.pie(
            analysis_result['service_status'], 
            values='count', 
            names='service_status',
            title='🚦 Service Status Distribution'
        )
        figures['service_status'] = fig_status
        
        return figures

class RegionalAnalyzer(DataAnalyzer):
    """Analyzes regional performance and trends"""
    
    def analyze(self, data: pd.DataFrame) -> Dict:
        """Analyze regional performance metrics"""
        analysis = {}
        
        # Regional passenger distribution
        regional_passengers = data.groupby('region').size().reset_index(name='passenger_count')
        analysis['passenger_distribution'] = regional_passengers
        
        # Regional revenue analysis
        regional_revenue = data.groupby('region')['fare_amount'].sum().reset_index()
        analysis['revenue'] = regional_revenue
        
        # Regional route analysis
        regional_routes = data.groupby('region')['route_id'].nunique().reset_index()
        regional_routes.columns = ['region', 'unique_routes']
        analysis['routes_per_region'] = regional_routes
        
        # Regional trip duration
        regional_duration = data.groupby('region')['trip_duration_minutes'].mean().reset_index()
        analysis['avg_trip_duration'] = regional_duration
        
        return analysis
    
    def visualize(self, analysis_result: Dict) -> Dict[str, go.Figure]:
        """Create visualizations for regional analysis"""
        figures = {}
        
        # Regional passenger distribution
        fig_passengers = px.bar(
            analysis_result['passenger_distribution'], 
            x='region', 
            y='passenger_count',
            title='🌍 Regional Passenger Distribution',
            color='passenger_count',
            color_continuous_scale='Viridis'
        )
        fig_passengers.update_layout(template="plotly_white")
        figures['passengers'] = fig_passengers
        
        # Regional revenue
        fig_revenue = px.bar(
            analysis_result['revenue'], 
            x='region', 
            y='fare_amount',
            title='💰 Regional Revenue Analysis',
            color='fare_amount',
            color_continuous_scale='Greens'
        )
        fig_revenue.update_layout(template="plotly_white")
        figures['revenue'] = fig_revenue
        
        return figures

# =====================================================================
# SEARCH AND FILTER ENGINE (STRATEGY PATTERN IMPLEMENTATION)
# =====================================================================

class SearchEngine:
    """Implements various search algorithms for data filtering"""
    
    def __init__(self):
        self._strategies = {
            'time': TimeFilter(),
            'region': RegionFilter(),
            'route': RouteFilter()
        }
    
    def search(self, data: pd.DataFrame, search_type: str, **kwargs) -> pd.DataFrame:
        """Apply search strategy based on type"""
        if search_type in self._strategies:
            return self._strategies[search_type].filter(data, **kwargs)
        return data
    
    def quick_search(self, data: pd.DataFrame, search_term: str) -> pd.DataFrame:
        """Quick text search across multiple columns"""
        if not search_term:
            return data
        
        # Convert search term to string and make case-insensitive
        search_term = str(search_term).lower()
        
        # Search across relevant string columns
        mask = (
            data['passenger_id'].astype(str).str.lower().str.contains(search_term, na=False) |
            data['route_id'].astype(str).str.lower().str.contains(search_term, na=False) |
            data['region'].astype(str).str.lower().str.contains(search_term, na=False) |
            data['service_status'].astype(str).str.lower().str.contains(search_term, na=False)
        )
        
        return data[mask]

# =====================================================================
# MAIN APPLICATION CLASS (SINGLETON PATTERN)
# =====================================================================

class BusPassengerAnalysisApp:
    """Main application class implementing Singleton pattern"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BusPassengerAnalysisApp, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.data_processor = None
            self.search_engine = SearchEngine()
            self.analyzers = {
                'congestion': CongestionAnalyzer(),
                'route': RouteAnalyzer(),
                'disruption': DisruptionAnalyzer(),
                'regional': RegionalAnalyzer()
            }
            self.initialized = True
    
    def setup_page_config(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="🚌 Bus Passenger Analytics Dashboard",
            page_icon="🚌",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def load_data(self, file_path: str):
        """Load and process data"""
        self.data_processor = DataProcessor(file_path)
        return self.data_processor.load_data()
    
    def create_sidebar_filters(self, data: pd.DataFrame) -> Dict:
        """Create sidebar filters and return filter parameters"""
        st.sidebar.header("🔍 Data Filters & Search")
        
        filters = {}
        
        # Quick search
        search_term = st.sidebar.text_input("🔎 Quick Search", placeholder="Search passenger ID, route, region...")
        filters['search_term'] = search_term
        
        # Region filter
        regions = st.sidebar.multiselect(
            "🌍 Select Regions",
            options=data['region'].unique(),
            default=data['region'].unique()
        )
        filters['regions'] = regions
        
        # Route filter
        routes = st.sidebar.multiselect(
            "🚌 Select Routes",
            options=sorted(data['route_id'].unique()),
            default=sorted(data['route_id'].unique())[:10]  # Default to first 10 routes
        )
        filters['routes'] = routes
        
        # Time filters
        st.sidebar.subheader("⏰ Time Filters")
        date_range = st.sidebar.date_input(
            "Date Range",
            value=[data['date'].min(), data['date'].max()],
            min_value=data['date'].min(),
            max_value=data['date'].max()
        )
        filters['date_range'] = date_range
        
        hour_range = st.sidebar.slider(
            "Hour Range",
            min_value=0,
            max_value=23,
            value=(0, 23),
            format="%d:00"
        )
        filters['hour_range'] = hour_range
        
        return filters
    
    def apply_filters(self, data: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        """Apply all filters to the data"""
        filtered_data = data.copy()
        
        # Apply quick search
        if filters['search_term']:
            filtered_data = self.search_engine.quick_search(filtered_data, filters['search_term'])
        
        # Apply region filter
        if filters['regions']:
            filtered_data = self.search_engine.search(filtered_data, 'region', regions=filters['regions'])
        
        # Apply route filter
        if filters['routes']:
            filtered_data = self.search_engine.search(filtered_data, 'route', routes=filters['routes'])
        
        # Apply time filters
        if len(filters['date_range']) == 2:
            start_date = filters['date_range'][0].strftime('%Y-%m-%d')
            end_date = filters['date_range'][1].strftime('%Y-%m-%d')
            filtered_data = self.search_engine.search(
                filtered_data, 'time', 
                start_date=start_date, 
                end_date=end_date,
                hour_range=filters['hour_range']
            )
        
        return filtered_data
    
    def display_overview_metrics(self, data: pd.DataFrame):
        """Display key metrics in the overview section"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 Total Passengers",
                value=f"{len(data):,}",
                delta=f"{len(data)} records"
            )
        
        with col2:
            st.metric(
                label="🚌 Total Routes",
                value=data['route_id'].nunique(),
                delta=f"{data['route_id'].nunique()} unique routes"
            )
        
        with col3:
            st.metric(
                label="🌍 Regions Covered",
                value=data['region'].nunique(),
                delta=f"{data['region'].nunique()} regions"
            )
        
        with col4:
            anomaly_rate = (data['anomaly_flag'].sum() / len(data)) * 100
            st.metric(
                label="⚠️ Anomaly Rate",
                value=f"{anomaly_rate:.2f}%",
                delta=f"{data['anomaly_flag'].sum()} anomalies"
            )
    
    def run(self):
        """Main application entry point"""
        self.setup_page_config()
        
        # Header
        st.title("🚌 Bus Passenger Analytics Dashboard")
        st.markdown("---")
        
        # Load data
        try:
            data = self.load_data("bus_passenger_dataset.csv")
            if data.empty:
                st.error("No data available. Please check the dataset file.")
                return
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return
        
        # Create sidebar filters
        filters = self.create_sidebar_filters(data)
        
        # Apply filters
        filtered_data = self.apply_filters(data, filters)
        
        # Display data info
        st.sidebar.markdown("---")
        st.sidebar.info(f"📊 Showing {len(filtered_data):,} of {len(data):,} records")
        
        # Main content tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", 
            "⏰ Peak Congestion", 
            "🚌 Route Analysis", 
            "⚠️ Disruption Detection", 
            "🌍 Regional Performance"
        ])
        
        with tab1:
            st.header("📊 Dashboard Overview")
            self.display_overview_metrics(filtered_data)
            
            st.subheader("📈 Quick Insights")
            col1, col2 = st.columns(2)
            
            with col1:
                # Busiest hour
                busiest_hour = filtered_data.groupby('hour').size().idxmax()
                st.info(f"🕐 **Busiest Hour:** {busiest_hour}:00")
                
                # Most popular route
                popular_route = filtered_data['route_id'].value_counts().index[0]
                st.info(f"🚌 **Most Popular Route:** {popular_route}")
            
            with col2:
                # Busiest region
                busiest_region = filtered_data['region'].value_counts().index[0]
                st.info(f"🌍 **Busiest Region:** {busiest_region}")
                
                # Service reliability
                on_time_rate = (filtered_data['service_status'] == 'On Time').mean() * 100
                st.info(f"🚦 **On-Time Rate:** {on_time_rate:.1f}%")
            
            # Sample data table
            st.subheader("📋 Sample Data")
            st.dataframe(
                filtered_data.head(10)[['timestamp', 'passenger_id', 'route_id', 'region', 'service_status', 'fare_amount']],
                use_container_width=True
            )
        
        with tab2:
            st.header("⏰ Peak Congestion Analysis")
            st.markdown("*Analyze passenger traffic patterns to optimize schedules and resource allocation.*")
            
            analyzer = self.analyzers['congestion']
            analysis_result = analyzer.analyze(filtered_data)
            figures = analyzer.visualize(analysis_result)
            
            # Display visualizations
            st.plotly_chart(figures['hourly'], use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(figures['daily'], use_container_width=True)
            with col2:
                st.plotly_chart(figures['monthly'], use_container_width=True)
            
            # Top congested stations
            st.subheader("🚏 Station Congestion Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Top Entry Stations**")
                top_entries = analysis_result['stations']['entries'].sort_values('entries', ascending=False).head(10)
                st.dataframe(top_entries, use_container_width=True)
            
            with col2:
                st.write("**Top Exit Stations**")
                top_exits = analysis_result['stations']['exits'].sort_values('exits', ascending=False).head(10)
                st.dataframe(top_exits, use_container_width=True)
        
        with tab3:
            st.header("🚌 Route & Transfer Point Analysis")
            st.markdown("*Identify popular routes and optimize transfer points for better passenger experience.*")
            
            analyzer = self.analyzers['route']
            analysis_result = analyzer.analyze(filtered_data)
            figures = analyzer.visualize(analysis_result)
            
            # Display visualizations
            st.plotly_chart(figures['routes'], use_container_width=True)
            
            if 'transfers' in figures:
                st.plotly_chart(figures['transfers'], use_container_width=True)
            
            # Route statistics
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Route Statistics")
                route_stats = analysis_result['routes'].head(10)
                st.dataframe(route_stats, use_container_width=True)
            
            with col2:
                st.subheader("🔄 Transfer Point Statistics")
                if not analysis_result['transfers'].empty:
                    transfer_stats = analysis_result['transfers'].head(10)
                    st.dataframe(transfer_stats, use_container_width=True)
                else:
                    st.info("No transfer data available in current filter selection.")
        
        with tab4:
            st.header("⚠️ Service Disruption Detection")
            st.markdown("*Monitor service anomalies and detect potential operational issues.*")
            
            analyzer = self.analyzers['disruption']
            analysis_result = analyzer.analyze(filtered_data)
            figures = analyzer.visualize(analysis_result)
            
            # Key metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Total Anomalies",
                    analysis_result['anomalies']['total_anomalies'],
                    f"{analysis_result['anomalies']['anomaly_percentage']:.2f}%"
                )
            
            with col2:
                avg_duration = filtered_data['trip_duration_minutes'].mean()
                st.metric(
                    "Avg Trip Duration",
                    f"{avg_duration:.1f} min",
                    "minutes"
                )
            
            with col3:
                on_time_count = (filtered_data['service_status'] == 'On Time').sum()
                st.metric(
                    "On-Time Services",
                    on_time_count,
                    f"{(on_time_count/len(filtered_data)*100):.1f}%"
                )
            
            # Display visualizations
            st.plotly_chart(figures['anomaly_hour'], use_container_width=True)
            st.plotly_chart(figures['service_status'], use_container_width=True)
            
            # Anomaly details
            st.subheader("🔍 Anomaly Details")
            anomaly_data = filtered_data[filtered_data['anomaly_flag'] == True]
            if not anomaly_data.empty:
                st.dataframe(
                    anomaly_data[['timestamp', 'passenger_id', 'route_id', 'region', 'trip_duration_minutes']].head(20),
                    use_container_width=True
                )
            else:
                st.info("No anomalies found in current filter selection.")
        
        with tab5:
            st.header("🌍 Regional Performance Analysis")
            st.markdown("*Compare performance across different regions for targeted improvements.*")
            
            analyzer = self.analyzers['regional']
            # Polymorphic behavior: Different analyzers implement analyze() differently
            analysis_result = analyzer.analyze(filtered_data)
            figures = analyzer.visualize(analysis_result)
            
            # Display visualizations
            st.plotly_chart(figures['passengers'], use_container_width=True)
            st.plotly_chart(figures['revenue'], use_container_width=True)
            
            # Regional comparison table
            st.subheader("📊 Regional Comparison")
            
            # Merge all regional data
            regional_summary = analysis_result['passenger_distribution'].copy()
            regional_summary = regional_summary.merge(analysis_result['revenue'], on='region', how='left')
            regional_summary = regional_summary.merge(analysis_result['routes_per_region'], on='region', how='left')
            regional_summary = regional_summary.merge(analysis_result['avg_trip_duration'], on='region', how='left')
            
            # Calculate revenue per passenger
            regional_summary['revenue_per_passenger'] = regional_summary['fare_amount'] / regional_summary['passenger_count']
            
            # Format columns
            regional_summary.columns = ['Region', 'Total Passengers', 'Total Revenue', 'Unique Routes', 'Avg Trip Duration', 'Revenue per Passenger']
            regional_summary['Total Revenue'] = regional_summary['Total Revenue'].round(2)
            regional_summary['Avg Trip Duration'] = regional_summary['Avg Trip Duration'].round(1)
            regional_summary['Revenue per Passenger'] = regional_summary['Revenue per Passenger'].round(2)
            
            st.dataframe(regional_summary, use_container_width=True)

# =====================================================================
# APPLICATION ENTRY POINT
# =====================================================================

def main():
    """Main function to run the application"""
    app = BusPassengerAnalysisApp()
    app.run()

if __name__ == "__main__":
    main()
