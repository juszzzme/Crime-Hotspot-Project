"""
Crime Trend Analysis Visualization Module

This module provides functions to analyze and visualize crime trends over time,
including time series analysis, seasonal patterns, and trend forecasting.
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from app.models.crime_data import CrimeReport, CrimeType
from sqlalchemy import func, extract, and_
from app.extensions import db

class CrimeTrendAnalyzer:
    """Analyze and visualize crime trends over time."""
    
    def __init__(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
        """Initialize with date range for analysis.
        
        Args:
            start_date: Start date for analysis (inclusive)
            end_date: End date for analysis (inclusive)
        """
        self.start_date = start_date or (datetime.utcnow() - timedelta(days=365))
        self.end_date = end_date or datetime.utcnow()
    
    def get_crime_trends(self, time_unit: str = 'D', crime_type_id: Optional[int] = None) -> pd.DataFrame:
        """Get crime counts aggregated by time unit.
        
        Args:
            time_unit: Time unit for aggregation ('D'=day, 'W'=week, 'M'=month, 'Q'=quarter, 'Y'=year)
            crime_type_id: Optional filter for specific crime type
            
        Returns:
            DataFrame with columns: date, crime_count
        """
        # Base query
        query = db.session.query(
            func.date_trunc(time_unit, CrimeReport.date_occurred).label('date'),
            func.count(CrimeReport.id).label('crime_count')
        ).filter(
            CrimeReport.date_occurred.between(self.start_date, self.end_date)
        )
        
        # Apply filters
        if crime_type_id is not None:
            query = query.filter(CrimeReport.crime_type_id == crime_type_id)
        
        # Group by time unit
        query = query.group_by('date').order_by('date')
        
        # Execute query and convert to DataFrame
        results = query.all()
        df = pd.DataFrame(results, columns=['date', 'crime_count'])
        
        # Fill in missing dates with 0 counts
        if not df.empty:
            date_range = pd.date_range(
                start=df['date'].min(),
                end=df['date'].max(),
                freq=time_unit
            )
            df = df.set_index('date').reindex(date_range, fill_value=0).reset_index()
            df = df.rename(columns={'index': 'date'})
        
        return df
    
    def plot_trend(self, time_unit: str = 'W', crime_type_id: Optional[int] = None) -> go.Figure:
        """Create an interactive trend plot of crime data.
        
        Args:
            time_unit: Time unit for aggregation
            crime_type_id: Optional filter for specific crime type
            
        Returns:
            Plotly Figure object
        """
        df = self.get_crime_trends(time_unit, crime_type_id)
        
        # Get crime type name for title
        crime_type = None
        if crime_type_id:
            crime_type = CrimeType.query.get(crime_type_id)
        
        # Create figure
        fig = go.Figure()
        
        # Add main trend line
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['crime_count'],
            mode='lines+markers',
            name='Crime Count',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6, color='#1f77b4')
        ))
        
        # Add rolling average (7-period)
        if len(df) > 7:
            df['rolling_avg'] = df['crime_count'].rolling(window=7, min_periods=1).mean()
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['rolling_avg'],
                mode='lines',
                name='7-Period Moving Avg',
                line=dict(color='#ff7f0e', width=3, dash='dash')
            ))
        
        # Update layout
        title = 'Crime Trends Over Time'
        if crime_type:
            title = f"{crime_type.category} - {crime_type.name} {title}"
            
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                xanchor='center',
                font=dict(size=18)
            ),
            xaxis_title='Date',
            yaxis_title='Number of Crimes',
            template='plotly_white',
            hovermode='x unified',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        # Add range slider
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        
        return fig
    
    def plot_seasonal_decomposition(self, crime_type_id: Optional[int] = None) -> go.Figure:
        """Create a seasonal decomposition plot of crime data.
        
        Args:
            crime_type_id: Optional filter for specific crime type
            
        Returns:
            Plotly Figure object with subplots for trend, seasonality, and residuals
        """
        from statsmodels.tsa.seasonal import seasonal_decompose
        
        # Get daily data
        df = self.get_crime_trends('D', crime_type_id)
        
        # Ensure we have a complete date range
        date_range = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
        df = df.set_index('date').reindex(date_range, fill_value=0).reset_index()
        
        # Perform seasonal decomposition (assumes weekly seasonality with period=7)
        result = seasonal_decompose(
            df.set_index('index')['crime_count'],
            model='additive',
            period=7  # Weekly seasonality
        )
        
        # Create subplots
        fig = make_subplots(
            rows=4, 
            cols=1,
            subplot_titles=('Observed', 'Trend', 'Seasonal', 'Residual'),
            vertical_spacing=0.08
        )
        
        # Add traces
        fig.add_trace(
            go.Scatter(x=result.observed.index, y=result.observed, name='Observed'),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=result.trend.index, y=result.trend, name='Trend'),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=result.seasonal.index, y=result.seasonal, name='Seasonal'),
            row=3, col=1
        )
        fig.add_trace(
            go.Scatter(x=result.resid.index, y=result.resid, name='Residual'),
            row=4, col=1
        )
        
        # Update layout
        crime_type = None
        if crime_type_id:
            crime_type = CrimeType.query.get(crime_type_id)
            
        title = 'Seasonal Decomposition of Crime Data'
        if crime_type:
            title = f"{crime_type.category} - {crime_type.name} {title}"
        
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                xanchor='center',
                font=dict(size=18)
            ),
            showlegend=False,
            height=800,
            template='plotly_white'
        )
        
        # Update y-axis titles
        fig.update_yaxes(title_text="Crime Count", row=1, col=1)
        fig.update_yaxes(title_text="Trend", row=2, col=1)
        fig.update_yaxes(title_text="Seasonal", row=3, col=1)
        fig.update_yaxes(title_text="Residual", row=4, col=1)
        
        return fig
    
    @staticmethod
    def plot_crime_heatmap(df: pd.DataFrame, 
                          x_col: str, 
                          y_col: str, 
                          z_col: str = 'crime_count',
                          title: str = 'Crime Heatmap') -> go.Figure:
        """Create a heatmap of crime data.
        
        Args:
            df: DataFrame containing the data
            x_col: Column name for x-axis (e.g., 'hour_of_day')
            y_col: Column name for y-axis (e.g., 'day_of_week')
            z_col: Column name for values (default: 'crime_count')
            title: Plot title
            
        Returns:
            Plotly Figure object with heatmap
        """
        # Pivot the data for heatmap
        pivot_df = df.pivot_table(
            index=y_col,
            columns=x_col,
            values=z_col,
            aggfunc='sum',
            fill_value=0
        )
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale='Viridis',
            colorbar=dict(title='Number of Crimes')
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                xanchor='center',
                font=dict(size=18)
            ),
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title(),
            template='plotly_white',
            margin=dict(l=80, r=50, t=80, b=80)
        )
        
        return fig

# Example usage
if __name__ == "__main__":
    # Example 1: Basic trend plot
    analyzer = CrimeTrendAnalyzer()
    fig1 = analyzer.plot_trend('W')
    fig1.show()
    
    # Example 2: Seasonal decomposition
    fig2 = analyzer.plot_seasonal_decomposition()
    fig2.show()
    
    # Example 3: Create a sample heatmap
    # (In practice, you would query this from your database)
    sample_data = {
        'hour_of_day': np.random.randint(0, 24, 1000),
        'day_of_week': np.random.choice(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 1000),
        'crime_count': np.random.poisson(5, 1000)
    }
    df = pd.DataFrame(sample_data)
    fig3 = CrimeTrendAnalyzer.plot_crime_heatmap(
        df, 
        x_col='hour_of_day', 
        y_col='day_of_week',
        title='Crime Distribution by Day and Hour'
    )
    fig3.show()
