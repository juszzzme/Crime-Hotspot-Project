"""
Advanced AI Crime Pattern Recognition System
Implements sophisticated pattern recognition using clustering algorithms,
anomaly detection, and crime correlation analysis.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import haversine_distances
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class AdvancedPatternRecognizer:
    """
    Advanced AI system for crime pattern recognition and analysis
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.crime_clusters = None
        self.anomaly_detector = None
        self.pattern_cache = {}
        self.last_analysis = None
        
        # Crime type severity mapping
        self.crime_severity = {
            'murder': 10,
            'rape': 9,
            'robbery': 7,
            'assault': 6,
            'burglary': 5,
            'theft': 4,
            'vandalism': 3,
            'drug': 5,
            'fraud': 4,
            'cybercrime': 3
        }
        
        # Time-based patterns
        self.time_patterns = {
            'morning': (6, 12),
            'afternoon': (12, 18),
            'evening': (18, 22),
            'night': (22, 6)
        }
        
    def analyze_crime_patterns(self, crime_data: List[Dict]) -> Dict:
        """
        Comprehensive crime pattern analysis
        """
        print("[AI] Starting advanced crime pattern analysis...")
        
        if not crime_data:
            return self._empty_analysis()
        
        # Convert to DataFrame for analysis
        df = self._prepare_data(crime_data)
        
        # Perform various pattern analyses
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'total_incidents': len(df),
            'spatial_clusters': self._analyze_spatial_clusters(df),
            'temporal_patterns': self._analyze_temporal_patterns(df),
            'crime_correlations': self._analyze_crime_correlations(df),
            'anomaly_detection': self._detect_anomalies(df),
            'hotspot_evolution': self._analyze_hotspot_evolution(df),
            'risk_assessment': self._assess_risk_levels(df),
            'predictive_insights': self._generate_predictive_insights(df),
            'pattern_summary': self._generate_pattern_summary(df)
        }
        
        self.last_analysis = analysis_results
        print("[AI] Crime pattern analysis completed")
        
        return analysis_results
    
    def _prepare_data(self, crime_data: List[Dict]) -> pd.DataFrame:
        """
        Prepare and clean crime data for analysis
        """
        df = pd.DataFrame(crime_data)
        
        # Ensure required columns exist
        required_columns = ['latitude', 'longitude', 'crime_type', 'date', 'time']
        for col in required_columns:
            if col not in df.columns:
                if col == 'time':
                    df[col] = '12:00'  # Default time
                elif col in ['latitude', 'longitude']:
                    # Generate random coordinates around Chennai if missing
                    base_lat, base_lng = 13.0827, 80.2707
                    df[col] = base_lat if col == 'latitude' else base_lng
                    df[col] += np.random.normal(0, 0.1, len(df))
                else:
                    df[col] = 'unknown'
        
        # Convert date and time to datetime
        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], errors='coerce')
        df['hour'] = df['datetime'].dt.hour
        df['day_of_week'] = df['datetime'].dt.dayofweek
        df['month'] = df['datetime'].dt.month
        
        # Add severity scores
        df['severity'] = df['crime_type'].map(self.crime_severity).fillna(5)
        
        # Add time period classification
        df['time_period'] = df['hour'].apply(self._classify_time_period)
        
        return df
    
    def _classify_time_period(self, hour: int) -> str:
        """Classify hour into time periods"""
        for period, (start, end) in self.time_patterns.items():
            if start <= end:
                if start <= hour < end:
                    return period
            else:  # night period (22-6)
                if hour >= start or hour < end:
                    return period
        return 'unknown'
    
    def _analyze_spatial_clusters(self, df: pd.DataFrame) -> Dict:
        """
        Analyze spatial clustering of crimes using DBSCAN
        """
        if len(df) < 5:
            return {'clusters': 0, 'noise_points': 0, 'cluster_details': []}
        
        # Prepare coordinates for clustering
        coords = df[['latitude', 'longitude']].values
        
        # Convert to radians for haversine distance
        coords_rad = np.radians(coords)
        
        # DBSCAN clustering with haversine distance
        # eps in radians (approximately 500 meters)
        eps_km = 0.5  # 500 meters
        eps_rad = eps_km / 6371.0  # Earth radius in km
        
        dbscan = DBSCAN(eps=eps_rad, min_samples=3, metric='haversine')
        cluster_labels = dbscan.fit_predict(coords_rad)
        
        df['cluster'] = cluster_labels
        
        # Analyze clusters
        unique_clusters = set(cluster_labels)
        noise_points = list(cluster_labels).count(-1)
        n_clusters = len(unique_clusters) - (1 if -1 in unique_clusters else 0)
        
        cluster_details = []
        for cluster_id in unique_clusters:
            if cluster_id == -1:  # Skip noise points
                continue
                
            cluster_data = df[df['cluster'] == cluster_id]
            
            # Calculate cluster statistics
            center_lat = cluster_data['latitude'].mean()
            center_lng = cluster_data['longitude'].mean()
            
            # Most common crime type in cluster
            crime_counts = cluster_data['crime_type'].value_counts()
            dominant_crime = crime_counts.index[0] if len(crime_counts) > 0 else 'unknown'
            
            # Risk level based on crime severity and frequency
            avg_severity = cluster_data['severity'].mean()
            incident_count = len(cluster_data)
            risk_score = (avg_severity * incident_count) / 10
            
            cluster_details.append({
                'cluster_id': int(cluster_id),
                'center': {'lat': center_lat, 'lng': center_lng},
                'incident_count': incident_count,
                'dominant_crime_type': dominant_crime,
                'average_severity': round(avg_severity, 2),
                'risk_score': round(risk_score, 2),
                'time_distribution': cluster_data['time_period'].value_counts().to_dict()
            })
        
        # Sort clusters by risk score
        cluster_details.sort(key=lambda x: x['risk_score'], reverse=True)
        
        return {
            'total_clusters': n_clusters,
            'noise_points': noise_points,
            'cluster_details': cluster_details,
            'clustering_efficiency': round((len(df) - noise_points) / len(df), 2) if len(df) > 0 else 0
        }
    
    def _analyze_temporal_patterns(self, df: pd.DataFrame) -> Dict:
        """
        Analyze temporal patterns in crime data
        """
        temporal_analysis = {
            'hourly_distribution': df['hour'].value_counts().sort_index().to_dict(),
            'daily_distribution': df['day_of_week'].value_counts().sort_index().to_dict(),
            'monthly_distribution': df['month'].value_counts().sort_index().to_dict(),
            'time_period_distribution': df['time_period'].value_counts().to_dict(),
            'peak_hours': [],
            'peak_days': [],
            'seasonal_trends': {}
        }
        
        # Identify peak hours (top 3)
        hourly_counts = df['hour'].value_counts()
        peak_hours = hourly_counts.head(3).index.tolist()
        temporal_analysis['peak_hours'] = [int(hour) for hour in peak_hours]
        
        # Identify peak days (top 3)
        daily_counts = df['day_of_week'].value_counts()
        peak_days = daily_counts.head(3).index.tolist()
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        temporal_analysis['peak_days'] = [day_names[day] for day in peak_days]
        
        # Crime type temporal patterns
        crime_time_patterns = {}
        for crime_type in df['crime_type'].unique():
            crime_subset = df[df['crime_type'] == crime_type]
            crime_time_patterns[crime_type] = {
                'peak_hour': int(crime_subset['hour'].mode().iloc[0]) if len(crime_subset) > 0 else 12,
                'peak_day': day_names[int(crime_subset['day_of_week'].mode().iloc[0])] if len(crime_subset) > 0 else 'Monday',
                'time_period_preference': crime_subset['time_period'].mode().iloc[0] if len(crime_subset) > 0 else 'afternoon'
            }
        
        temporal_analysis['crime_type_patterns'] = crime_time_patterns
        
        return temporal_analysis
    
    def _analyze_crime_correlations(self, df: pd.DataFrame) -> Dict:
        """
        Analyze correlations between different crime types and factors
        """
        correlations = {
            'crime_type_cooccurrence': {},
            'spatial_correlations': {},
            'temporal_correlations': {},
            'severity_correlations': {}
        }
        
        # Crime type co-occurrence analysis
        crime_types = df['crime_type'].unique()
        for crime1 in crime_types:
            for crime2 in crime_types:
                if crime1 != crime2:
                    # Find incidents of crime1 and crime2 within 1km and 24 hours
                    crime1_incidents = df[df['crime_type'] == crime1]
                    crime2_incidents = df[df['crime_type'] == crime2]
                    
                    cooccurrence_count = 0
                    for _, incident1 in crime1_incidents.iterrows():
                        for _, incident2 in crime2_incidents.iterrows():
                            # Calculate distance
                            distance = self._calculate_distance(
                                incident1['latitude'], incident1['longitude'],
                                incident2['latitude'], incident2['longitude']
                            )
                            
                            # Calculate time difference
                            time_diff = abs((incident1['datetime'] - incident2['datetime']).total_seconds() / 3600)
                            
                            if distance <= 1.0 and time_diff <= 24:  # Within 1km and 24 hours
                                cooccurrence_count += 1
                    
                    if cooccurrence_count > 0:
                        correlations['crime_type_cooccurrence'][f"{crime1}-{crime2}"] = cooccurrence_count
        
        # Temporal correlations
        hour_crime_matrix = df.pivot_table(
            values='severity', 
            index='hour', 
            columns='crime_type', 
            aggfunc='count', 
            fill_value=0
        )
        
        if not hour_crime_matrix.empty:
            correlations['temporal_correlations'] = {
                'hour_crime_correlation': hour_crime_matrix.corr().to_dict()
            }
        
        return correlations
    
    def _detect_anomalies(self, df: pd.DataFrame) -> Dict:
        """
        Detect anomalous crime patterns using Isolation Forest
        """
        if len(df) < 10:
            return {'anomalies_detected': 0, 'anomaly_details': []}
        
        # Prepare features for anomaly detection
        features = ['latitude', 'longitude', 'hour', 'day_of_week', 'severity']
        feature_data = df[features].copy()
        
        # Scale features
        scaled_features = self.scaler.fit_transform(feature_data)
        
        # Isolation Forest for anomaly detection
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        anomaly_labels = iso_forest.fit_predict(scaled_features)
        
        # Identify anomalies
        df['is_anomaly'] = anomaly_labels == -1
        anomalies = df[df['is_anomaly']]
        
        anomaly_details = []
        for _, anomaly in anomalies.iterrows():
            anomaly_details.append({
                'id': anomaly.get('id', f"anomaly_{len(anomaly_details)}"),
                'crime_type': anomaly['crime_type'],
                'location': {'lat': anomaly['latitude'], 'lng': anomaly['longitude']},
                'datetime': anomaly['datetime'].isoformat() if pd.notna(anomaly['datetime']) else None,
                'severity': anomaly['severity'],
                'anomaly_score': float(iso_forest.decision_function(scaled_features[anomalies.index])[len(anomaly_details)]),
                'reason': self._determine_anomaly_reason(anomaly, df)
            })
        
        return {
            'anomalies_detected': len(anomalies),
            'anomaly_rate': round(len(anomalies) / len(df), 3),
            'anomaly_details': anomaly_details
        }
    
    def _determine_anomaly_reason(self, anomaly: pd.Series, df: pd.DataFrame) -> str:
        """
        Determine why an incident is considered anomalous
        """
        reasons = []
        
        # Check if location is unusual for this crime type
        same_crime = df[df['crime_type'] == anomaly['crime_type']]
        if len(same_crime) > 1:
            avg_lat = same_crime['latitude'].mean()
            avg_lng = same_crime['longitude'].mean()
            distance = self._calculate_distance(
                anomaly['latitude'], anomaly['longitude'], avg_lat, avg_lng
            )
            if distance > 5:  # More than 5km from average location
                reasons.append("unusual_location")
        
        # Check if time is unusual for this crime type
        crime_hours = same_crime['hour'].values
        if len(crime_hours) > 1:
            hour_std = np.std(crime_hours)
            hour_mean = np.mean(crime_hours)
            if abs(anomaly['hour'] - hour_mean) > 2 * hour_std:
                reasons.append("unusual_time")
        
        # Check if severity is unusual
        if anomaly['severity'] > df['severity'].quantile(0.9):
            reasons.append("high_severity")
        
        return ", ".join(reasons) if reasons else "statistical_outlier"
    
    def _analyze_hotspot_evolution(self, df: pd.DataFrame) -> Dict:
        """
        Analyze how crime hotspots evolve over time
        """
        if len(df) < 20:
            return {'evolution_detected': False, 'hotspot_changes': []}
        
        # Sort by datetime
        df_sorted = df.sort_values('datetime')
        
        # Split data into time periods (e.g., weekly)
        df_sorted['week'] = df_sorted['datetime'].dt.isocalendar().week
        
        hotspot_evolution = []
        weeks = sorted(df_sorted['week'].unique())
        
        for i, week in enumerate(weeks[:-1]):  # Compare consecutive weeks
            current_week = df_sorted[df_sorted['week'] == week]
            next_week = df_sorted[df_sorted['week'] == weeks[i + 1]]
            
            if len(current_week) > 0 and len(next_week) > 0:
                # Simple hotspot detection based on density
                current_hotspot = self._find_simple_hotspot(current_week)
                next_hotspot = self._find_simple_hotspot(next_week)
                
                if current_hotspot and next_hotspot:
                    distance = self._calculate_distance(
                        current_hotspot['lat'], current_hotspot['lng'],
                        next_hotspot['lat'], next_hotspot['lng']
                    )
                    
                    hotspot_evolution.append({
                        'week_from': int(week),
                        'week_to': int(weeks[i + 1]),
                        'hotspot_shift_distance': round(distance, 2),
                        'intensity_change': next_hotspot['intensity'] - current_hotspot['intensity']
                    })
        
        return {
            'evolution_detected': len(hotspot_evolution) > 0,
            'hotspot_changes': hotspot_evolution,
            'average_shift_distance': round(np.mean([h['hotspot_shift_distance'] for h in hotspot_evolution]), 2) if hotspot_evolution else 0
        }
    
    def _find_simple_hotspot(self, df: pd.DataFrame) -> Optional[Dict]:
        """
        Find the primary hotspot in a dataset
        """
        if len(df) < 3:
            return None
        
        # Use KMeans to find the center of highest density
        coords = df[['latitude', 'longitude']].values
        kmeans = KMeans(n_clusters=1, random_state=42, n_init=10)
        center = kmeans.fit(coords).cluster_centers_[0]
        
        return {
            'lat': center[0],
            'lng': center[1],
            'intensity': len(df)
        }
    
    def _assess_risk_levels(self, df: pd.DataFrame) -> Dict:
        """
        Assess risk levels for different areas and times
        """
        risk_assessment = {
            'overall_risk_score': 0,
            'high_risk_areas': [],
            'high_risk_times': [],
            'risk_factors': {}
        }
        
        # Calculate overall risk score
        total_severity = df['severity'].sum()
        total_incidents = len(df)
        risk_assessment['overall_risk_score'] = round(total_severity / max(total_incidents, 1), 2)
        
        # Identify high-risk time periods
        time_risk = df.groupby('time_period')['severity'].agg(['count', 'mean']).reset_index()
        time_risk['risk_score'] = time_risk['count'] * time_risk['mean']
        high_risk_times = time_risk.nlargest(2, 'risk_score')['time_period'].tolist()
        risk_assessment['high_risk_times'] = high_risk_times
        
        # Risk factors analysis
        risk_factors = {
            'crime_diversity': len(df['crime_type'].unique()),
            'temporal_concentration': df['hour'].value_counts().max() / len(df),
            'severity_variance': float(df['severity'].var()),
            'incident_frequency': len(df) / max((df['datetime'].max() - df['datetime'].min()).days, 1)
        }
        risk_assessment['risk_factors'] = risk_factors
        
        return risk_assessment
    
    def _generate_predictive_insights(self, df: pd.DataFrame) -> Dict:
        """
        Generate predictive insights based on patterns
        """
        insights = {
            'predictions': [],
            'recommendations': [],
            'trend_analysis': {}
        }
        
        # Trend analysis
        if len(df) > 10:
            # Weekly trend
            df['week'] = df['datetime'].dt.isocalendar().week
            weekly_counts = df.groupby('week').size()
            if len(weekly_counts) > 1:
                trend_slope = np.polyfit(range(len(weekly_counts)), weekly_counts.values, 1)[0]
                insights['trend_analysis']['weekly_trend'] = 'increasing' if trend_slope > 0 else 'decreasing'
                insights['trend_analysis']['trend_strength'] = abs(trend_slope)
        
        # Generate predictions
        most_common_crime = df['crime_type'].mode().iloc[0] if len(df) > 0 else 'theft'
        peak_hour = df['hour'].mode().iloc[0] if len(df) > 0 else 12
        
        insights['predictions'] = [
            f"High probability of {most_common_crime} incidents during hour {peak_hour}",
            f"Expected {len(df) // 7} incidents per week based on current trends",
            f"Risk level: {'High' if insights.get('trend_analysis', {}).get('weekly_trend') == 'increasing' else 'Moderate'}"
        ]
        
        # Generate recommendations
        insights['recommendations'] = [
            f"Increase patrol presence during {peak_hour}:00-{(peak_hour+1)%24}:00",
            f"Focus prevention efforts on {most_common_crime} incidents",
            "Implement community awareness programs in high-risk areas",
            "Consider installing additional surveillance in identified hotspots"
        ]
        
        return insights
    
    def _generate_pattern_summary(self, df: pd.DataFrame) -> Dict:
        """
        Generate a comprehensive summary of detected patterns
        """
        summary = {
            'key_findings': [],
            'pattern_strength': 'weak',
            'confidence_score': 0.0,
            'data_quality': 'good'
        }
        
        # Key findings
        if len(df) > 0:
            most_common_crime = df['crime_type'].mode().iloc[0]
            peak_hour = df['hour'].mode().iloc[0]
            avg_severity = df['severity'].mean()
            
            summary['key_findings'] = [
                f"Most frequent crime type: {most_common_crime}",
                f"Peak activity hour: {peak_hour}:00",
                f"Average severity level: {avg_severity:.1f}/10",
                f"Total incidents analyzed: {len(df)}"
            ]
            
            # Pattern strength assessment
            crime_concentration = df['crime_type'].value_counts().iloc[0] / len(df)
            time_concentration = df['hour'].value_counts().max() / len(df)
            
            if crime_concentration > 0.5 or time_concentration > 0.3:
                summary['pattern_strength'] = 'strong'
            elif crime_concentration > 0.3 or time_concentration > 0.2:
                summary['pattern_strength'] = 'moderate'
            
            # Confidence score based on data size and consistency
            data_size_factor = min(len(df) / 100, 1.0)  # Max 1.0 for 100+ incidents
            consistency_factor = 1.0 - (df['crime_type'].nunique() / len(df))
            summary['confidence_score'] = round((data_size_factor + consistency_factor) / 2, 2)
        
        return summary
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        Calculate distance between two points using Haversine formula
        """
        from math import radians, cos, sin, asin, sqrt
        
        # Convert to radians
        lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Earth radius in kilometers
        
        return c * r
    
    def _empty_analysis(self) -> Dict:
        """
        Return empty analysis structure when no data is available
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'total_incidents': 0,
            'spatial_clusters': {'total_clusters': 0, 'noise_points': 0, 'cluster_details': []},
            'temporal_patterns': {'hourly_distribution': {}, 'daily_distribution': {}, 'peak_hours': [], 'peak_days': []},
            'crime_correlations': {'crime_type_cooccurrence': {}, 'spatial_correlations': {}, 'temporal_correlations': {}},
            'anomaly_detection': {'anomalies_detected': 0, 'anomaly_details': []},
            'hotspot_evolution': {'evolution_detected': False, 'hotspot_changes': []},
            'risk_assessment': {'overall_risk_score': 0, 'high_risk_areas': [], 'high_risk_times': []},
            'predictive_insights': {'predictions': [], 'recommendations': [], 'trend_analysis': {}},
            'pattern_summary': {'key_findings': ['No data available for analysis'], 'pattern_strength': 'none', 'confidence_score': 0.0}
        }

# Global instance for easy access
pattern_recognizer = AdvancedPatternRecognizer()
