import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from abc import ABC, abstractmethod
import tempfile
import os

# Import classes from app.py
from app import (
    DataAnalyzer, DataFilter, CongestionAnalyzer, RouteAnalyzer,
    DisruptionAnalyzer, RegionalAnalyzer, TimeFilter, RegionFilter,
    RouteFilter, DataProcessor, SearchEngine, BusPassengerAnalysisApp
)

class TestDataProcessor:
    """Test suite for DataProcessor class"""
    
    @pytest.fixture
    def sample_csv_file(self):
        """Create a temporary CSV file for testing"""
        data = {
            'timestamp': pd.date_range('2023-01-01', periods=100, freq='h'),
            'passenger_id': ['P_' + str(i).zfill(6) for i in range(1, 101)],
            'entry_station_id': np.random.randint(1, 51, 100),
            'exit_station_id': np.random.randint(1, 51, 100),
            'region': ['Region_' + str(i % 3) for i in range(100)],
            'day_of_week': [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][i % 7] for i in range(100)],
            'route_id': ['Route_' + str(i % 5).zfill(3) for i in range(100)],
            'transfer_station_id': [str(i % 10) if i % 3 == 0 else '' for i in range(100)],
            'service_status': ['On Time'] * 100,
            'anomaly_flag': [False] * 100,
            'trip_duration_minutes': np.random.randint(5, 60, 100),
            'boarding_time': pd.date_range('2023-01-01', periods=100, freq='h'),
            'alighting_time': pd.date_range('2023-01-01', periods=100, freq='h') + pd.Timedelta(minutes=30),
            'fare_amount': np.round(np.random.uniform(2.0, 6.0, 100), 2)
        }
        df = pd.DataFrame(data)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            yield f.name
        
        os.unlink(f.name)
    
    def test_data_processor_initialization(self, sample_csv_file):
        """Test DataProcessor initialization"""
        processor = DataProcessor(sample_csv_file)
        assert processor._file_path == sample_csv_file
        assert processor._data is None
        assert processor._processed_data is None
    
    def test_load_data_success(self, sample_csv_file):
        """Test successful data loading"""
        processor = DataProcessor(sample_csv_file)
        data = processor.load_data()
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0
        assert 'timestamp' in data.columns
        assert 'route_id' in data.columns
    
    @patch('app.st.error')
    def test_load_data_file_not_found(self, mock_error):
        """Test data loading with non-existent file"""
        processor = DataProcessor("non_existent_file.csv")
        
        # The actual implementation returns an empty DataFrame on error, not raise
        result = processor.load_data()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        mock_error.assert_called_once()
    
    def test_data_property(self, sample_csv_file):
        """Test data property getter"""
        processor = DataProcessor(sample_csv_file)
        processor.load_data()
        
        data = processor.data
        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0


class TestCongestionAnalyzer:
    """Test suite for CongestionAnalyzer class"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample DataFrame for testing"""
        return pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=100, freq='h'),
            'passenger_id': ['P_' + str(i).zfill(6) for i in range(1, 101)],
            'entry_station_id': np.random.randint(1, 51, 100),
            'exit_station_id': np.random.randint(1, 51, 100),
            'region': ['Region_' + str(i % 3) for i in range(100)],
            'day_of_week': [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][i % 7] for i in range(100)],
            'route_id': ['Route_' + str(i % 5).zfill(3) for i in range(100)],
            'transfer_station_id': [str(i % 10) if i % 3 == 0 else '' for i in range(100)],
            'service_status': ['On Time'] * 100,
            'anomaly_flag': [False] * 100,
            'trip_duration_minutes': np.random.randint(5, 60, 100),
            'boarding_time': pd.date_range('2023-01-01', periods=100, freq='h'),
            'alighting_time': pd.date_range('2023-01-01', periods=100, freq='h') + pd.Timedelta(minutes=30),
            'fare_amount': np.round(np.random.uniform(2.0, 6.0, 100), 2),
            'hour': [i % 24 for i in range(100)],
            'month': [1] * 100,
            'day': [i % 28 + 1 for i in range(100)],
            'year': [2023] * 100
        })
    
    def test_congestion_analyzer_inheritance(self):
        """Test that CongestionAnalyzer inherits from DataAnalyzer"""
        analyzer = CongestionAnalyzer()
        assert isinstance(analyzer, DataAnalyzer)
    
    def test_analyze_method_returns_dict(self, sample_data):
        """Test analyze method returns dictionary"""
        analyzer = CongestionAnalyzer()
        result = analyzer.analyze(sample_data)
        
        assert isinstance(result, dict)
        assert 'hourly' in result
        assert 'daily' in result
        assert 'monthly' in result
        assert 'stations' in result
    
    def test_visualize_method_returns_figures(self, sample_data):
        """Test visualize method returns figure dictionary"""
        analyzer = CongestionAnalyzer()
        analysis_result = analyzer.analyze(sample_data)
        figures = analyzer.visualize(analysis_result)
        
        assert isinstance(figures, dict)
        assert len(figures) > 0
    
    @patch('matplotlib.pyplot.figure')
    def test_visualize_with_mock_matplotlib(self, mock_figure, sample_data):
        """Test visualization with mocked matplotlib"""
        mock_fig = Mock()
        mock_figure.return_value = mock_fig
        
        analyzer = CongestionAnalyzer()
        analysis_result = analyzer.analyze(sample_data)
        figures = analyzer.visualize(analysis_result)
        
        assert isinstance(figures, dict)


class TestRouteAnalyzer:
    """Test suite for RouteAnalyzer class"""
    
    @pytest.fixture
    def route_data(self):
        """Create route-specific test data"""
        return pd.DataFrame({
            'route_id': ['Route_001', 'Route_002', 'Route_003'] * 30,
            'passenger_id': ['P_' + str(i).zfill(6) for i in range(1, 91)],
            'transfer_station_id': ['Point_1', 'Point_2', 'Point_3'] * 30,
            'timestamp': pd.date_range('2023-01-01', periods=90, freq='h'),
            'region': ['North', 'South', 'Central'] * 30
        })
    
    def test_route_analyzer_inheritance(self):
        """Test RouteAnalyzer inherits from DataAnalyzer"""
        analyzer = RouteAnalyzer()
        assert isinstance(analyzer, DataAnalyzer)
    
    def test_analyze_popular_routes(self, route_data):
        """Test analysis of popular routes"""
        analyzer = RouteAnalyzer()
        result = analyzer.analyze(route_data)
        
        assert 'routes' in result
        assert 'transfers' in result
        assert 'route_region' in result
        assert isinstance(result['routes'], pd.DataFrame)


class TestTimeFilter:
    """Test suite for TimeFilter class"""
    
    @pytest.fixture
    def time_data(self):
        """Create time-based test data"""
        return pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=200, freq='h'),
            'passenger_id': ['P_' + str(i).zfill(6) for i in range(1, 201)],
            'hour': [i % 24 for i in range(200)]
        })
    
    def test_time_filter_inheritance(self):
        """Test TimeFilter inherits from DataFilter"""
        filter_obj = TimeFilter()
        assert isinstance(filter_obj, DataFilter)
    
    def test_filter_by_date_range(self, time_data):
        """Test filtering by date range"""
        filter_obj = TimeFilter()
        filtered_data = filter_obj.filter(
            time_data,
            start_date='2023-01-02',
            end_date='2023-01-05',
            hour_range=None
        )
        
        assert isinstance(filtered_data, pd.DataFrame)
        assert len(filtered_data) < len(time_data)
    
    def test_filter_by_hour_range(self, time_data):
        """Test filtering by hour range"""
        filter_obj = TimeFilter()
        filtered_data = filter_obj.filter(
            time_data,
            start_date=None,
            end_date=None,
            hour_range=(8, 18)
        )
        
        assert isinstance(filtered_data, pd.DataFrame)
        assert all(8 <= hour <= 18 for hour in filtered_data['hour'])
    
    def test_filter_empty_result(self, time_data):
        """Test filtering that returns empty result"""
        filter_obj = TimeFilter()
        filtered_data = filter_obj.filter(
            time_data,
            start_date='2025-01-01',
            end_date='2025-01-02',
            hour_range=None
        )
        
        assert isinstance(filtered_data, pd.DataFrame)
        assert len(filtered_data) == 0


class TestRegionFilter:
    """Test suite for RegionFilter class"""
    
    @pytest.fixture
    def region_data(self):
        """Create region-based test data"""
        return pd.DataFrame({
            'region': ['North', 'South', 'East', 'West'] * 25,
            'passenger_id': ['P_' + str(i).zfill(6) for i in range(1, 101)],
            'route_id': ['Route_' + str(i).zfill(3) for i in range(100)]
        })
    
    def test_region_filter_inheritance(self):
        """Test RegionFilter inherits from DataFilter"""
        filter_obj = RegionFilter()
        assert isinstance(filter_obj, DataFilter)
    
    def test_filter_by_regions(self, region_data):
        """Test filtering by specific regions"""
        filter_obj = RegionFilter()
        filtered_data = filter_obj.filter(region_data, regions=['North', 'South'])
        
        assert isinstance(filtered_data, pd.DataFrame)
        assert all(region in ['North', 'South'] for region in filtered_data['region'])
        assert len(filtered_data) <= len(region_data)
    
    def test_filter_single_region(self, region_data):
        """Test filtering by single region"""
        filter_obj = RegionFilter()
        filtered_data = filter_obj.filter(region_data, regions=['North'])
        
        assert all(region == 'North' for region in filtered_data['region'])


class TestSearchEngine:
    """Test suite for SearchEngine class"""
    
    @pytest.fixture
    def search_data(self):
        """Create search test data"""
        return pd.DataFrame({
            'route_id': ['Route_Express', 'Route_Local', 'Route_Night'] * 20,
            'region': ['Downtown', 'Suburb', 'Airport'] * 20,
            'timestamp': pd.date_range('2023-01-01', periods=60, freq='h'),
            'passenger_id': ['P_' + str(i).zfill(6) for i in range(1, 61)],
            'service_status': ['On Time', 'Delayed', 'Early'] * 20
        })
    
    def test_search_engine_initialization(self):
        """Test SearchEngine initialization"""
        engine = SearchEngine()
        assert hasattr(engine, '_strategies')
        assert isinstance(engine._strategies, dict)
    
    @patch.object(TimeFilter, 'filter')
    def test_search_with_time_strategy(self, mock_filter, search_data):
        """Test search using time filter strategy"""
        mock_filter.return_value = search_data[:10]
        
        engine = SearchEngine()
        result = engine.search(
            search_data,
            search_type='time',
            start_date='2023-01-01',
            end_date='2023-01-02'
        )
        
        assert isinstance(result, pd.DataFrame)
        mock_filter.assert_called_once()
    
    def test_quick_search(self, search_data):
        """Test quick search functionality"""
        engine = SearchEngine()
        result = engine.quick_search(search_data, 'Express')
        
        assert isinstance(result, pd.DataFrame)
        # Should find rows containing 'Express' in any string column
    
    def test_search_invalid_type(self, search_data):
        """Test search with invalid search type"""
        engine = SearchEngine()
        
        # Invalid search type should just return original data
        result = engine.search(search_data, search_type='invalid_type')
        assert result.equals(search_data)


class TestBusPassengerAnalysisApp:
    """Test suite for BusPassengerAnalysisApp (Singleton) class"""
    
    def test_singleton_pattern(self):
        """Test that BusPassengerAnalysisApp implements Singleton pattern"""
        app1 = BusPassengerAnalysisApp()
        app2 = BusPassengerAnalysisApp()
        
        assert app1 is app2
        assert id(app1) == id(app2)
    
    def test_app_initialization(self):
        """Test application initialization"""
        app = BusPassengerAnalysisApp()
        
        assert hasattr(app, 'data_processor')
        assert hasattr(app, 'search_engine')
        assert hasattr(app, 'analyzers')
        assert isinstance(app.analyzers, dict)
    
    def test_analyzers_setup(self):
        """Test that all analyzers are properly initialized"""
        app = BusPassengerAnalysisApp()
        
        expected_analyzers = [
            'congestion', 'route', 'disruption', 'regional'
        ]
        
        for analyzer_name in expected_analyzers:
            assert analyzer_name in app.analyzers
            assert isinstance(app.analyzers[analyzer_name], DataAnalyzer)
    
    @patch('app.st.set_page_config')
    def test_setup_page_config(self, mock_set_config):
        """Test Streamlit page configuration setup"""
        app = BusPassengerAnalysisApp()
        app.setup_page_config()
        
        mock_set_config.assert_called_once()
    
    @patch.object(DataProcessor, 'load_data')
    def test_load_data(self, mock_load_data):
        """Test data loading functionality"""
        mock_df = pd.DataFrame({'test': [1, 2, 3]})
        mock_load_data.return_value = mock_df
        
        app = BusPassengerAnalysisApp()
        result = app.load_data('test_file.csv')
        
        assert isinstance(result, pd.DataFrame)
        mock_load_data.assert_called_once()
    
    def test_apply_filters_with_empty_filters(self):
        """Test applying empty filters"""
        app = BusPassengerAnalysisApp()
        test_data = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
        
        # Provide the expected filter structure
        empty_filters = {
            'search_term': '',
            'start_date': None,
            'end_date': None,
            'hour_range': None,
            'regions': None,
            'routes': None,
            'date_range': []
        }
        
        result = app.apply_filters(test_data, empty_filters)
        
        assert result.equals(test_data)
    
    @patch('app.st.metric')
    def test_display_overview_metrics(self, mock_metric):
        """Test overview metrics display"""
        app = BusPassengerAnalysisApp()
        test_data = pd.DataFrame({
            'passenger_id': ['P_000001', 'P_000002', 'P_000003'],
            'route_id': ['Route_001', 'Route_002', 'Route_001'],
            'timestamp': pd.date_range('2023-01-01', periods=3),
            'region': ['North', 'South', 'Central'],
            'anomaly_flag': [False, True, False]
        })
        
        app.display_overview_metrics(test_data)
        
        # Should call streamlit metric function
        assert mock_metric.called


class TestIntegration:
    """Integration tests for the entire application"""
    
    @pytest.fixture
    def integration_data(self):
        """Create comprehensive test data for integration testing"""
        np.random.seed(42)  # For reproducible tests
        
        return pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=1000, freq='h'),
            'passenger_id': ['P_' + str(i).zfill(6) for i in range(1, 1001)],
            'entry_station_id': np.random.randint(1, 51, 1000),
            'exit_station_id': np.random.randint(1, 51, 1000),
            'region': ['Region_' + str(i % 5) for i in range(1000)],
            'day_of_week': [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][i % 7] for i in range(1000)],
            'route_id': ['Route_' + str(i % 10).zfill(3) for i in range(1000)],
            'transfer_station_id': ['Point_' + str(i % 8) for i in range(1000)],
            'hour': [i % 24 for i in range(1000)],
            'month': [(i // 720) + 1 for i in range(1000)],
            'day': [(i % 30) + 1 for i in range(1000)],
            'anomaly_flag': [i % 20 == 0 for i in range(1000)],  # 5% anomaly rate
            'service_status': [['On Time', 'Delayed', 'Early'][i % 3] for i in range(1000)],
            'trip_duration_minutes': np.random.randint(5, 60, 1000),
            'fare_amount': np.round(np.random.uniform(2.0, 6.0, 1000), 2)
        })
    
    def test_end_to_end_analysis_pipeline(self, integration_data):
        """Test complete analysis pipeline"""
        # Initialize app
        app = BusPassengerAnalysisApp()
        
        # Test filtering
        time_filter = TimeFilter()
        filtered_data = time_filter.filter(
            integration_data,
            start_date='2023-01-01',
            end_date='2023-01-10',
            hour_range=(6, 22)
        )
        
        # Test analysis
        congestion_analyzer = CongestionAnalyzer()
        analysis_result = congestion_analyzer.analyze(filtered_data)
        
        # Test visualization
        figures = congestion_analyzer.visualize(analysis_result)
        
        # Assertions
        assert isinstance(filtered_data, pd.DataFrame)
        assert len(filtered_data) > 0
        assert isinstance(analysis_result, dict)
        assert isinstance(figures, dict)
    
    def test_multiple_filters_combination(self, integration_data):
        """Test combining multiple filters"""
        # Apply time filter
        time_filter = TimeFilter()
        time_filtered = time_filter.filter(
            integration_data,
            start_date='2023-01-01',
            end_date='2023-01-15',
            hour_range=None
        )
        
        # Apply region filter
        region_filter = RegionFilter()
        final_filtered = region_filter.filter(
            time_filtered,
            regions=['Region_0', 'Region_1']
        )
        
        assert len(final_filtered) <= len(time_filtered)
        assert len(final_filtered) <= len(integration_data)
    
    def test_all_analyzers_with_same_data(self, integration_data):
        """Test all analyzers work with the same dataset"""
        analyzers = [
            CongestionAnalyzer(),
            RouteAnalyzer(),
            DisruptionAnalyzer(),
            RegionalAnalyzer()
        ]
        
        for analyzer in analyzers:
            result = analyzer.analyze(integration_data)
            assert isinstance(result, dict)
            
            figures = analyzer.visualize(result)
            assert isinstance(figures, dict)


# Pytest configuration and fixtures
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment before running tests"""
    # Mock streamlit functions to avoid import errors during testing
    import sys
    from unittest.mock import Mock, MagicMock
    
    # Create a more comprehensive mock for streamlit
    streamlit_mock = MagicMock()
    streamlit_mock.set_page_config = Mock()
    streamlit_mock.metric = Mock()
    streamlit_mock.selectbox = Mock()
    streamlit_mock.slider = Mock()
    streamlit_mock.error = Mock()
    
    # Mock streamlit.emojis submodule
    emojis_mock = Mock()
    emojis_mock.ALL_EMOJIS = ['🚌', '📊', '🚍']
    streamlit_mock.emojis = emojis_mock
    
    # Mock string_util functions
    string_util_mock = Mock()
    string_util_mock.is_emoji = Mock(return_value=True)
    streamlit_mock.string_util = string_util_mock
    
    sys.modules['streamlit'] = streamlit_mock
    sys.modules['streamlit.emojis'] = emojis_mock
    sys.modules['streamlit.string_util'] = string_util_mock
    
    yield
    
    # Cleanup if needed
    modules_to_remove = ['streamlit', 'streamlit.emojis', 'streamlit.string_util']
    for module in modules_to_remove:
        if module in sys.modules:
            del sys.modules[module]


# Custom pytest markers
pytestmark = [
    pytest.mark.unit,
    pytest.mark.analytics
]


if __name__ == "__main__":
    # Run tests with coverage
    pytest.main([
        __file__,
        "-v",
        "--cov=app",
        "--cov-report=html",
        "--cov-report=term-missing"
    ])
