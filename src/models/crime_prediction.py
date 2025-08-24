"""
AI-Powered Crime Prediction Engine

This module implements machine learning models for crime prediction using historical data,
pattern recognition, and temporal analysis to forecast crime incidents and safety scores.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Union
import warnings
import logging
import joblib
import json
from pathlib import Path
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore')

# Machine Learning imports
from sklearn.ensemble import (
    RandomForestRegressor, 
    GradientBoostingRegressor,
    AdaBoostRegressor,
    StackingRegressor
)
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.preprocessing import (
    StandardScaler, 
    MinMaxScaler,
    RobustScaler,
    LabelEncoder,
    PolynomialFeatures
)
from sklearn.model_selection import (
    train_test_split, 
    cross_val_score,
    GridSearchCV,
    RandomizedSearchCV,
    TimeSeriesSplit
)
from sklearn.metrics import (
    mean_absolute_error, 
    mean_squared_error, 
    r2_score,
    make_scorer,
    mean_absolute_percentage_error
)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.cluster import KMeans, DBSCAN

# For model interpretation
import shap

# Time series analysis
from scipy import stats
from scipy.signal import find_peaks

# Data processing
import os
from pathlib import Path

class CrimePredictionEngine:
    """Advanced crime prediction engine using multiple ML algorithms."""
    
    def __init__(self, data_path: str = None, model_dir: str = None):
        """Initialize the prediction engine with enhanced configuration.
        
        Args:
            data_path: Path to the processed crime data directory
            model_dir: Directory to save/load trained models
        """
        self.data_path = data_path or self._get_default_data_path()
        self.model_dir = model_dir or str(Path(__file__).parent.parent.parent / 'models')
        
        # Create model directory if it doesn't exist
        Path(self.model_dir).mkdir(parents=True, exist_ok=True)
        
        # Model storage
        self.models = {}
        self.model_metrics = {}
        self.scalers = {}
        self.encoders = {}
        self.feature_importance = {}
        self.prediction_cache = {}
        self.baseline_models = {}
        
        # Model configuration
        self.cv_folds = 5
        self.random_state = 42
        self.test_size = 0.2
        
        # Load and prepare data
        try:
            self.crime_data = self._load_crime_data()
            self.processed_data = self._preprocess_data()
            logger.info("Data loaded and preprocessed successfully.")
        except Exception as e:
            logger.error(f"Error initializing data: {str(e)}")
            self.crime_data = pd.DataFrame()
            self.processed_data = pd.DataFrame()
        
        # Initialize SHAP explainer
        self.explainer = None
        
    def _get_default_data_path(self) -> str:
        """Get default path to processed crime data."""
        project_root = Path(__file__).parent.parent.parent
        return str(project_root / "data" / "processed" / "by_crime_type" / "against_women")
    
    def _save_model(self, model, model_name: str, crime_type: str) -> None:
        """Save trained model to disk.
        
        Args:
            model: Trained model object
            model_name: Name of the model (e.g., 'random_forest', 'xgboost')
            crime_type: Type of crime the model predicts
        """
        model_path = Path(self.model_dir) / f"{crime_type}_{model_name}.joblib"
        joblib.dump(model, model_path)
        logger.info(f"Saved {model_name} model for {crime_type} to {model_path}")
    
    def _load_model(self, model_name: str, crime_type: str):
        """Load trained model from disk.
        
        Args:
            model_name: Name of the model to load
            crime_type: Type of crime the model predicts
            
        Returns:
            Loaded model or None if not found
        """
        model_path = Path(self.model_dir) / f"{crime_type}_{model_name}.joblib"
        if model_path.exists():
            return joblib.load(model_path)
        return None
    
    def _save_encoder(self, encoder, filename: str) -> None:
        """Save encoder to disk.
        
        Args:
            encoder: Encoder object to save
            filename: Name of the file to save to
        """
        encoder_path = Path(self.model_dir) / filename
        joblib.dump(encoder, encoder_path)
    
    def _load_encoder(self, filename: str):
        """Load encoder from disk.
        
        Args:
            filename: Name of the encoder file to load
            
        Returns:
            Loaded encoder or None if not found
        """
        encoder_path = Path(self.model_dir) / filename
        if encoder_path.exists():
            return joblib.load(encoder_path)
        return None
    
    def _load_crime_data(self) -> pd.DataFrame:
        """Load and combine crime data from multiple years."""
        data_frames = []
        
        try:
            # Load data from multiple years
            for year in [2012, 2013, 2014]:
                file_path = os.path.join(
                    self.data_path, 
                    f"processed_42_District_wise_crimes_committed_against_women_{year}.csv"
                )
                if os.path.exists(file_path):
                    df = pd.read_csv(file_path)
                    df['year'] = year
                    data_frames.append(df)
            
            if data_frames:
                combined_df = pd.concat(data_frames, ignore_index=True)
                return combined_df
            else:
                # Fallback to single file if available
                fallback_path = os.path.join(self.data_path, "processed_42_District_wise_crimes_committed_against_women_2014.csv")
                if os.path.exists(fallback_path):
                    df = pd.read_csv(fallback_path)
                    df['year'] = 2014
                    return df
                else:
                    raise FileNotFoundError("No crime data files found")
                    
        except Exception as e:
            print(f"Error loading crime data: {e}")
            # Return sample data for demonstration
            return self._generate_sample_data()
    
    def _generate_sample_data(self) -> pd.DataFrame:
        """Generate sample crime data for demonstration purposes."""
        np.random.seed(42)
        
        districts = [
            'Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem',
            'Tirunelveli', 'Erode', 'Vellore', 'Thoothukudi', 'Dindigul',
            'Thanjavur', 'Kanchipuram', 'Cuddalore', 'Karur', 'Ramanathapuram'
        ]
        
        data = []
        for year in range(2012, 2025):  # Include future years for prediction
            for district in districts:
                # Generate realistic crime data with trends
                base_rape = np.random.poisson(30 + (year - 2012) * 2)
                base_murder = np.random.poisson(15 + (year - 2012) * 1)
                base_robbery = np.random.poisson(10 + (year - 2012) * 0.5)
                base_arson = np.random.poisson(5 + (year - 2012) * 0.2)
                
                # Add seasonal variation
                seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * (year - 2012) / 4)
                
                data.append({
                    'district': district,
                    'year': year,
                    'rape': int(base_rape * seasonal_factor),
                    'murder': int(base_murder * seasonal_factor),
                    'robbery': int(base_robbery * seasonal_factor),
                    'arson': int(base_arson * seasonal_factor)
                })
        
        return pd.DataFrame(data)
    
    def _preprocess_data(self) -> pd.DataFrame:
        """Preprocess crime data for machine learning with enhanced feature engineering."""
        logger.info("Starting data preprocessing...")
        df = self.crime_data.copy()
        
        # Define crime types
        crime_columns = ['rape', 'murder', 'robbery', 'arson']
        crime_columns = [col for col in crime_columns if col in df.columns]
        
        # Handle missing values with more sophisticated imputation
        for col in crime_columns:
            if df[col].isna().any():
                # Use median for the district if available, otherwise global median
                df[col] = df.groupby('district')[col].transform(
                    lambda x: x.fillna(x.median() if not x.isna().all() else df[col].median())
                )
        
        # Create derived features
        df['total_crimes'] = df[crime_columns].sum(axis=1)
        
        # Temporal features
        df['year_sin'] = np.sin(2 * np.pi * (df['year'] - df['year'].min()) / 10)
        df['year_cos'] = np.cos(2 * np.pi * (df['year'] - df['year'].min()) / 10)
        
        # Rolling statistics (3-year window)
        df = df.sort_values(['district', 'year'])
        for col in crime_columns:
            # Lag features
            for lag in [1, 2, 3]:
                df[f'{col}_lag{lag}'] = df.groupby('district')[col].shift(lag)
            
            # Rolling statistics
            df[f'{col}_rolling_mean3'] = df.groupby('district')[col].transform(
                lambda x: x.rolling(window=3, min_periods=1).mean()
            )
            df[f'{col}_rolling_std3'] = df.groupby('district')[col].transform(
                lambda x: x.rolling(window=3, min_periods=1).std()
            )
            
            # Year-over-year change
            df[f'{col}_yoy'] = df.groupby('district')[col].pct_change()
        
        # District-level statistics
        district_stats = df.groupby('district').agg({
            'total_crimes': ['mean', 'std', 'max', 'min']
        })
        district_stats.columns = [f'district_{col[0]}_{col[1]}' for col in district_stats.columns]
        df = df.merge(district_stats, on='district', how='left')
        
        # Encode categorical variables
        if 'district' in df.columns:
            le = LabelEncoder()
            df['district_encoded'] = le.fit_transform(df['district'])
            self.encoders['district'] = le
            
            # Save the encoder
            self._save_encoder(le, 'district_encoder.joblib')
        
        # Handle remaining missing values
        df = df.fillna(method='ffill').fillna(method='bfill').fillna(0)
        
        # Log preprocessing completion
        logger.info(f"Preprocessing complete. Final shape: {df.shape}")
        
        return df
    
    def _get_model_pipeline(self, model, preprocessor=None):
        """Create a scikit-learn pipeline for the given model."""
        if preprocessor is None:
            numeric_features = ['year', 'district_encoded'] + \
                            [col for col in self.processed_data.columns if 'lag' in col or 'rolling' in col or 'yoy' in col]
            numeric_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
            
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', numeric_transformer, numeric_features)
                ])
        
        return Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('feature_selector', SelectKBest(score_func=f_regression, k=10)),
            ('model', model)
        ])
    
    def _get_hyperparameter_grid(self, model_name):
        """Get hyperparameter grid for different models."""
        if model_name == 'random_forest':
            return {
                'model__n_estimators': [50, 100, 200],
                'model__max_depth': [None, 10, 20, 30],
                'model__min_samples_split': [2, 5, 10],
                'model__min_samples_leaf': [1, 2, 4],
                'model__bootstrap': [True, False]
            }
        elif model_name == 'xgboost':
            return {
                'model__n_estimators': [50, 100, 200],
                'model__learning_rate': [0.01, 0.05, 0.1],
                'model__max_depth': [3, 6, 9],
                'model__subsample': [0.8, 0.9, 1.0],
                'model__colsample_bytree': [0.8, 0.9, 1.0]
            }
        elif model_name == 'lightgbm':
            return {
                'model__n_estimators': [50, 100, 200],
                'model__learning_rate': [0.01, 0.05, 0.1],
                'model__num_leaves': [31, 50, 100],
                'model__max_depth': [-1, 10, 20],
                'model__min_child_samples': [20, 50, 100]
            }
        return {}
    
    def _evaluate_model(self, model, X_test, y_test, cv_scores=None):
        """Evaluate model performance with multiple metrics."""
        y_pred = model.predict(X_test)
        
        metrics = {
            'r2': r2_score(y_test, y_pred),
            'mae': mean_absolute_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mape': mean_absolute_percentage_error(y_test, y_pred) * 100,
            'cv_scores': cv_scores.tolist() if cv_scores is not None else None
        }
        
        if hasattr(model, 'feature_importances_'):
            metrics['feature_importances'] = dict(
                zip(X_test.columns, model.feature_importances_)
            )
        
        return metrics
    
    def train_prediction_models(self, use_cv: bool = True, tune_hyperparams: bool = True) -> Dict[str, dict]:
        """
        Train multiple prediction models with hyperparameter tuning and cross-validation.
        
        Args:
            use_cv: Whether to use cross-validation
            tune_hyperparams: Whether to perform hyperparameter tuning
            
        Returns:
            Dictionary containing performance metrics for each crime type
        """
        logger.info("Starting model training...")
        df = self.processed_data
        
        # Define models to train
        models = {
            'random_forest': RandomForestRegressor(random_state=self.random_state),
            'xgboost': XGBRegressor(random_state=self.random_state, n_jobs=-1),
            'lightgbm': LGBMRegressor(random_state=self.random_state, n_jobs=-1)
        }
        
        # Define crime types to predict
        crime_types = ['rape', 'murder', 'robbery', 'arson', 'total_crimes']
        crime_types = [ct for ct in crime_types if ct in df.columns]
        
        # Initialize metrics storage
        self.model_metrics = {ct: {} for ct in crime_types}
        
        for crime_type in crime_types:
            logger.info(f"Training models for {crime_type}...")
            
            # Prepare features and target
            feature_columns = [col for col in df.columns if col not in crime_types + ['district', 'year']]
            X = df[feature_columns]
            y = df[crime_type]
            
            # Train-test split with time-based validation
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=self.test_size, random_state=self.random_state, shuffle=False
            )
            
            # Train each model
            for model_name, model in models.items():
                logger.info(f"  Training {model_name}...")
                
                try:
                    # Create pipeline
                    pipeline = self._get_model_pipeline(model)
                    
                    # Hyperparameter tuning
                    if tune_hyperparams:
                        param_grid = self._get_hyperparameter_grid(model_name)
                        if param_grid:
                            grid_search = GridSearchCV(
                                pipeline,
                                param_grid,
                                cv=TimeSeriesSplit(n_splits=5),
                                scoring='neg_root_mean_squared_error',
                                n_jobs=-1,
                                verbose=1
                            )
                            grid_search.fit(X_train, y_train)
                            best_model = grid_search.best_estimator_
                            best_params = grid_search.best_params_
                            logger.info(f"    Best params: {best_params}")
                        else:
                            best_model = pipeline.fit(X_train, y_train)
                    else:
                        best_model = pipeline.fit(X_train, y_train)
                    
                    # Cross-validation
                    cv_scores = None
                    if use_cv:
                        cv_scores = cross_val_score(
                            best_model, X_train, y_train, 
                            cv=TimeSeriesSplit(n_splits=5),
                            scoring='neg_root_mean_squared_error',
                            n_jobs=-1
                        )
                    
                    # Evaluate on test set
                    metrics = self._evaluate_model(best_model, X_test, y_test, cv_scores)
                    self.model_metrics[crime_type][model_name] = metrics
                    
                    # Store the best model for this crime type
                    if crime_type not in self.models or \
                       metrics['rmse'] < self.model_metrics[crime_type].get('best_rmse', float('inf')):
                        self.models[crime_type] = best_model
                        self.model_metrics[crime_type]['best_model'] = model_name
                        self.model_metrics[crime_type]['best_rmse'] = metrics['rmse']
                    
                    # Save feature importances
                    if hasattr(best_model.named_steps['model'], 'feature_importances_'):
                        self.feature_importance[crime_type] = dict(
                            zip(X_train.columns, best_model.named_steps['model'].feature_importances_)
                        )
                    
                    # Save the trained model
                    self._save_model(best_model, model_name, crime_type)
                    
                    logger.info(f"  {model_name} - RMSE: {metrics['rmse']:.2f}, R²: {metrics['r2']:.3f}")
                    
                except Exception as e:
                    logger.error(f"Error training {model_name} for {crime_type}: {str(e)}")
                    continue
        
        # Initialize SHAP explainer with the best model
        if any(ct in self.models for ct in crime_types):
            self._init_shap_explainer()
        
        logger.info("Model training completed.")
        return self.model_metrics
        
        return performance_metrics
    
    def _init_shap_explainer(self):
        """Initialize SHAP explainer for model interpretation."""
        try:
            # Use the first available model to initialize explainer
            for crime_type, model in self.models.items():
                if hasattr(model.named_steps['model'], 'predict'):
                    # Get a sample of the training data
                    X_sample = self.processed_data.sample(
                        min(100, len(self.processed_data)), 
                        random_state=self.random_state
                    )
                    
                    # Preprocess the sample
                    X_processed = model.named_steps['preprocessor'].transform(X_sample)
                    
                    # Initialize SHAP explainer
                    if hasattr(model.named_steps['model'], 'predict_proba'):
                        self.explainer = shap.Explainer(
                            model.named_steps['model'].predict_proba, 
                            X_processed
                        )
                    else:
                        self.explainer = shap.Explainer(
                            model.named_steps['model'].predict, 
                            X_processed
                        )
                    logger.info("SHAP explainer initialized successfully.")
                    break
        except Exception as e:
            logger.warning(f"Could not initialize SHAP explainer: {str(e)}")
    
    def get_feature_importance(self, crime_type: str, top_n: int = 10) -> Dict[str, float]:
        """Get feature importance for a specific crime type."""
        if crime_type not in self.feature_importance:
            return {}
        
        # Sort features by importance
        sorted_features = sorted(
            self.feature_importance[crime_type].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return dict(sorted_features[:top_n])
    
    def explain_prediction(self, X, crime_type: str) -> Dict:
        """
        Explain model predictions using SHAP values.
        
        Args:
            X: Input features for prediction
            crime_type: Type of crime to explain
            
        Returns:
            Dictionary containing SHAP values and explanation
        """
        if crime_type not in self.models or self.explainer is None:
            return {}
            
        model = self.models[crime_type]
        
        # Preprocess the input
        X_processed = model.named_steps['preprocessor'].transform(X)
        
        # Get SHAP values
        shap_values = self.explainer(X_processed)
        
        # Get feature names after preprocessing
        feature_names = X.columns.tolist()
        
        # Convert to a more interpretable format
        explanation = {
            'expected_value': float(np.mean(shap_values.base_values)),
            'feature_importances': {}
        }
        
        # Get mean absolute SHAP values for each feature
        if len(shap_values.shape) > 2:  # For multi-class models
            mean_shap_values = np.mean(np.abs(shap_values.values), axis=0)
            for i, name in enumerate(feature_names):
                explanation['feature_importances'][name] = float(mean_shap_values[i])
        else:  # For regression or binary classification
            for i, name in enumerate(feature_names):
                explanation['feature_importances'][name] = float(np.abs(shap_values.values[:, i]).mean())
        
        return explanation
    
    def predict_crime_trends(self, district: str, years_ahead: int = 3, 
                           return_confidence: bool = False) -> Dict[str, Union[List[float], Dict[str, List[float]]]]:
        """
        Predict crime trends for a specific district with confidence intervals.
        
        Args:
            district: Name of the district to predict for
            years_ahead: Number of years to predict into the future
            return_confidence: Whether to return confidence intervals
            
        Returns:
            Dictionary containing predictions and optionally confidence intervals
        """
        logger.info(f"Predicting crime trends for {district} for next {years_ahead} years...")
        
        if not self.models:
            logger.warning("No trained models found. Training models...")
            self.train_prediction_models()
        
        # Get historical data for the district
        district_data = self.processed_data[
            self.processed_data['district'] == district
        ].copy()
        
        if district_data.empty:
            # Use average data if district not found
            district_data = self.processed_data.groupby('year').mean().reset_index()
            district_data['district'] = district
            district_data['district_encoded'] = 0
        
        predictions = {}
        current_year = datetime.now().year
        
        for crime_type in self.models.keys():
            if crime_type not in self.models:
                continue
                
            model = self.models[crime_type]
            scaler = self.scalers[crime_type]
            
            crime_predictions = []
            
            # Get the latest data point
            latest_data = district_data.iloc[-1].copy()
            
            for year_offset in range(1, years_ahead + 1):
                future_year = current_year + year_offset
                
                # Prepare features for prediction
                features = []
                feature_columns = [
                    'year_normalized', 'district_encoded', 'rape_lag1', 'murder_lag1',
                    'robbery_lag1', 'arson_lag1', 'rape_trend', 'murder_trend',
                    'robbery_trend', 'arson_trend'
                ]
                
                # Update year feature
                year_normalized = (future_year - self.processed_data['year'].min()) / \
                                (self.processed_data['year'].max() - self.processed_data['year'].min())
                
                feature_values = [year_normalized, latest_data.get('district_encoded', 0)]
                
                # Add lag and trend features
                for col in ['rape_lag1', 'murder_lag1', 'robbery_lag1', 'arson_lag1',
                           'rape_trend', 'murder_trend', 'robbery_trend', 'arson_trend']:
                    feature_values.append(latest_data.get(col, 0))
                
                # Make prediction
                try:
                    X_pred = scaler.transform([feature_values])
                    prediction = model.predict(X_pred)[0]
                    crime_predictions.append(max(0, prediction))  # Ensure non-negative
                except Exception as e:
                    print(f"Prediction error for {crime_type}: {e}")
                    crime_predictions.append(0)
            
            predictions[crime_type] = crime_predictions
        
        return predictions
    
    def calculate_safety_score(self, district: str, include_breakdown: bool = False) -> Dict:
        """
        Calculate a comprehensive safety score for a district.
        
        Args:
            district: Name of the district
            include_breakdown: Whether to include detailed breakdown of score components
            
        Returns:
            Dictionary containing safety score and related metrics
        """
        logger.info(f"Calculating safety score for {district}...")
        
        # Get recent crime data (last 3 years)
        current_year = datetime.now().year
        recent_years = list(range(current_year - 3, current_year))
        
        # Get historical data for the district
        district_data = self.processed_data[
            (self.processed_data['district'] == district) &
            (self.processed_data['year'].isin(recent_years))
        ].copy()
        
        if district_data.empty:
            # Use overall average if no data for this district
            district_data = self.processed_data[
                self.processed_data['year'].isin(recent_years)
            ]
            logger.warning(f"No data found for district {district}. Using overall averages.")
        
        # Calculate base metrics
        metrics = {}
        
        # 1. Crime rate component (0-5 points)
        district_avg = district_data['total_crimes'].mean()
        overall_avg = self.processed_data['total_crimes'].mean()
        crime_rate_score = 5 * min(1, overall_avg / (district_avg + 1e-6))
        
        # 2. Trend component (0-3 points)
        trend_score = 0
        if len(district_data) > 1:
            trend = district_data['total_crimes'].pct_change().mean()
            if trend < -0.1:  # Significant decrease
                trend_score = 3
            elif trend < 0:    # Slight decrease
                trend_score = 2
            elif trend < 0.1:  # Stable
                trend_score = 1
        
        # 3. Crime type severity (0-2 points)
        severity_score = 0
        for crime_type in ['murder', 'rape', 'robbery', 'arson']:
            if crime_type in district_data.columns:
                crime_rate = district_data[crime_type].mean() / (district_data['total_crimes'].mean() + 1e-6)
                if crime_type in ['murder', 'rape'] and crime_rate > 0.1:  # More severe crimes
                    severity_score -= 0.5
        severity_score = max(0, 2 + severity_score)  # Cap at 2
        
        # Calculate final score (0-10 scale)
        safety_score = min(10, crime_rate_score + trend_score + severity_score)
        
        # Determine risk level
        if safety_score >= 8:
            risk_level = 'Very Safe'
        elif safety_score >= 6:
            risk_level = 'Safe'
        elif safety_score >= 4:
            risk_level = 'Moderate'
        elif safety_score >= 2:
            risk_level = 'Caution'
        else:
            risk_level = 'High Risk'
        
        # Prepare result
        result = {
            'safety_score': round(safety_score, 1),
            'risk_level': risk_level,
            'total_crimes_avg': round(district_avg, 1),
            'comparison_to_avg': 'below' if district_avg < overall_avg else 'above',
            'avg_crime_rate': round(overall_avg, 1)
        }
        
        # Add trend information
        if len(district_data) > 1:
            trend = district_data['total_crimes'].pct_change().mean()
            result['trend'] = {
                'direction': 'decreasing' if trend < 0 else 'increasing',
                'rate': abs(round(trend * 100, 1)),  # as percentage
                'description': 'improving' if trend < 0 else 'worsening'
            }
        
        # Add detailed breakdown if requested
        if include_breakdown:
            result['score_breakdown'] = {
                'crime_rate_score': round(crime_rate_score, 1),
                'trend_score': trend_score,
                'severity_score': round(severity_score, 1)
            }
            
            # Add top crime types
            crime_breakdown = {}
            for crime_type in ['murder', 'rape', 'robbery', 'arson']:
                if crime_type in district_data.columns:
                    crime_breakdown[crime_type] = {
                        'count': round(district_data[crime_type].mean(), 1),
                        'percentage': round(100 * district_data[crime_type].mean() / (district_avg + 1e-6), 1)
                    }
            result['crime_breakdown'] = crime_breakdown
        
        return result
    
    def get_high_risk_predictions(self, top_n: int = 10) -> List[Dict]:
        """Get top high-risk areas based on predictions."""
        districts = self.processed_data['district'].unique()
        risk_predictions = []
        
        for district in districts:
            predictions = self.predict_crime_trends(district, years_ahead=1)
            safety_info = self.calculate_safety_score(district)
            
            # Calculate predicted total crimes for next year
            predicted_total = sum([
                predictions.get('rape', [0])[0],
                predictions.get('murder', [0])[0],
                predictions.get('robbery', [0])[0],
                predictions.get('arson', [0])[0]
            ])
            
            risk_predictions.append({
                'district': district,
                'predicted_crimes': round(predicted_total, 1),
                'safety_score': safety_info['safety_score'],
                'risk_level': safety_info['risk_level'],
                'trend': safety_info['trend']
            })
        
        # Sort by predicted crimes (descending) and return top N
        risk_predictions.sort(key=lambda x: x['predicted_crimes'], reverse=True)
        return risk_predictions[:top_n]
    
    def analyze_temporal_patterns(self) -> Dict[str, any]:
        """Analyze temporal patterns in crime data."""
        df = self.processed_data
        
        # Monthly patterns (if we had month data, we'll simulate)
        # For now, analyze yearly patterns
        yearly_stats = df.groupby('year')['total_crimes'].agg(['mean', 'std', 'sum']).reset_index()
        
        # Calculate growth rate
        yearly_stats['growth_rate'] = yearly_stats['sum'].pct_change() * 100
        
        # Find peak crime periods
        crime_values = yearly_stats['sum'].values
        peaks, _ = find_peaks(crime_values)
        
        return {
            'yearly_trends': yearly_stats.to_dict('records'),
            'peak_years': yearly_stats.iloc[peaks]['year'].tolist() if len(peaks) > 0 else [],
            'average_growth_rate': yearly_stats['growth_rate'].mean(),
            'volatility': yearly_stats['sum'].std() / yearly_stats['sum'].mean()
        }
