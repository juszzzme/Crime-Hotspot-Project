from datetime import datetime
from sqlalchemy import func, Index, Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from app.extensions import db

import math

class Location(db.Model):
    """Geographic location model for crime reports with geospatial capabilities."""
    __tablename__ = 'locations'
    __table_args__ = (
        Index('idx_location_geom', 'geom', postgresql_using='gist'),
        Index('idx_location_coords', 'latitude', 'longitude'),
        {'extend_existing': True}
    )
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Location details with validation
    address = db.Column(db.String(255), index=True)
    city = db.Column(db.String(100), nullable=False, index=True)
    state = db.Column(db.String(100), nullable=False, index=True)
    country = db.Column(db.String(100), default='India', index=True)
    postal_code = db.Column(db.String(20), index=True)
    
    # Geospatial data with validation
    latitude = db.Column(Float, nullable=False)
    longitude = db.Column(Float, nullable=False)
    geom = db.Column(Text, nullable=False)  # Store as WKT (Well-Known Text)
    
    # Additional metadata
    place_id = db.Column(db.String(100), unique=True, index=True)
    location_metadata = db.Column(JSON)
    
    # Crime statistics (denormalized for performance)
    crime_count = db.Column(db.Integer, default=0, index=True)
    last_crime_reported = db.Column(db.DateTime)
    
    # Relationships are set up in relationships.py to avoid circular imports
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(Location, self).__init__(**kwargs)
        self._validate_coordinates()
    
    def _validate_coordinates(self):
        """Validate latitude and longitude values."""
        if self.latitude < -90 or self.latitude > 90:
            raise ValueError("Latitude must be between -90 and 90 degrees")
        if self.longitude < -180 or self.longitude > 180:
            raise ValueError("Longitude must be between -180 and 180 degrees")
    
    def update_crime_stats(self):
        """Update denormalized crime statistics for this location."""
        from sqlalchemy import func
        
        self.crime_count = self.crime_reports.count()
        last_crime = self.crime_reports.order_by(
            CrimeReport.date_occurred.desc()
        ).first()
        if last_crime:
            self.last_crime_reported = last_crime.date_occurred
    
    @classmethod
    def get_nearby_locations(cls, latitude, longitude, radius_km=1.0, limit=10):
        """Find locations within a given radius (in km) of a point."""
        # Approximate km to degrees conversion (roughly 111km per degree)
        lat_range = radius_km / 111.0
        lng_range = radius_km / (111.0 * abs(math.cos(math.radians(latitude))))
        
        return cls.query.filter(
            cls.latitude.between(latitude - lat_range, latitude + lat_range),
            cls.longitude.between(longitude - lng_range, longitude + lng_range)
        ).limit(limit).all()
    
    def get_crime_density(self, radius_km=1.0):
        """Calculate crime density in crimes per square km in the given radius."""
        from sqlalchemy import func, and_
        
        # Calculate area in square km (approximate)
        area = math.pi * (radius_km ** 2)
        
        # Count crimes in the area
        crime_count = CrimeReport.query.join(Location).filter(
            func.ST_DWithin(
                func.ST_GeomFromText(self.geom),
                CrimeReport.geom,
                radius_km * 1000  # Convert km to meters for PostGIS
            )
        ).count()
        
        return crime_count / area if area > 0 else 0
    
    def to_geojson(self):
        """Convert location to GeoJSON format."""
        # For SQLite compatibility, we'll use the lat/long directly
        # If we had PostGIS, we could parse the WKT from self.geom
        return {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [self.longitude, self.latitude]  # Longitude, Latitude order for GeoJSON
            },
            'properties': {
                'id': self.id,
                'address': self.address,
                'city': self.city,
                'state': self.state,
                'country': self.country,
                'postal_code': self.postal_code,
                'place_id': self.place_id,
                'crime_count': self.crime_reports.count() if hasattr(self, 'crime_reports') else 0
            }
        }
    
    def __repr__(self):
        return f'<Location {self.city}, {self.state}, {self.country}>'

class CrimeType(db.Model):
    """Categories and types of crimes with enhanced functionality."""
    __tablename__ = 'crime_types'
    __table_args__ = (
        db.UniqueConstraint('category', 'name', name='uix_category_name'),
        db.CheckConstraint('severity >= 1 AND severity <= 5', name='check_severity_range'),
        {'extend_existing': True}
    )
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    code = db.Column(db.String(50), unique=True, index=True)
    severity = db.Column(db.Integer, default=1, index=True)  # 1-5 scale
    description = db.Column(db.Text)
    keywords = db.Column(JSON, default=list)
    is_violent = db.Column(db.Boolean, default=False, index=True)
    is_property_crime = db.Column(db.Boolean, default=False, index=True)
    
    # Statistics
    report_count = db.Column(db.Integer, default=0, index=True)
    last_reported = db.Column(db.DateTime, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(CrimeType, self).__init__(**kwargs)
        self._validate_severity()
    
    def _validate_severity(self):
        if not 1 <= self.severity <= 5:
            raise ValueError("Severity must be between 1 and 5")
    
    def update_stats(self):
        """Update denormalized statistics for this crime type."""
        from sqlalchemy import desc
        
        self.report_count = self.crime_reports.count()
        last_report = self.crime_reports.order_by(
            desc(CrimeReport.date_reported)
        ).first()
        if last_report:
            self.last_reported = last_report.date_reported
    
    @classmethod
    def get_crimes_by_category(cls, category=None, min_severity=1, max_severity=5):
        """Get crimes filtered by category and severity range."""
        query = cls.query
        
        if category:
            query = query.filter_by(category=category)
        
        return query.filter(
            cls.severity.between(min_severity, max_severity)
        ).order_by(
            cls.severity.desc(),
            cls.report_count.desc()
        ).all()
    
    def __repr__(self):
        return f'<CrimeType {self.category} - {self.name}>'

class CrimeReport(db.Model):
    """Report of a crime incident with enhanced functionality."""
    __tablename__ = 'crime_reports'
    __table_args__ = (
        Index('idx_crime_date_occurred', 'date_occurred'),
        Index('idx_crime_status', 'status'),
        Index('idx_crime_verified', 'is_verified'),
        Index('idx_crime_geom', 'geom', postgresql_using='gist'),
        Index('idx_crime_type', 'crime_type_id'),
        Index('idx_crime_location', 'location_id'),
        {'extend_existing': True}
    )
    
    # Status constants
    STATUS_REPORTED = 'reported'
    STATUS_UNDER_INVESTIGATION = 'under_investigation'
    STATUS_RESOLVED = 'resolved'
    STATUS_REJECTED = 'rejected'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    
    # Incident details
    date_occurred = db.Column(db.DateTime, nullable=False, index=True)
    date_reported = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    status = db.Column(
        db.String(30),
        default=STATUS_REPORTED,
        nullable=False,
        index=True
    )
    
    # Location and type references
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    crime_type_id = db.Column(db.Integer, db.ForeignKey('crime_types.id'), nullable=False)
    
    # User who reported
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Verification
    is_verified = db.Column(db.Boolean, default=False, index=True)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    verified_at = db.Column(db.DateTime)
    
    # Geospatial data
    geom = db.Column(Text, nullable=False)  # WKT format
    
    # Additional metadata
    report_metadata = db.Column(JSON, default=dict)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(CrimeReport, self).__init__(**kwargs)
        self._validate_dates()
    
    def _validate_dates(self):
        """Ensure dates are valid and in the correct order."""
        if self.date_occurred and self.date_reported:
            if self.date_occurred > datetime.utcnow():
                raise ValueError("Date occurred cannot be in the future")
            if self.date_reported < self.date_occurred:
                raise ValueError("Date reported cannot be before date occurred")
    
    def verify(self, user_id):
        """Mark this report as verified by a user."""
        self.is_verified = True
        self.verified_by = user_id
        self.verified_at = datetime.utcnow()
        self.status = self.STATUS_UNDER_INVESTIGATION
    
    def update_status(self, status, user_id=None):
        """Update the status of this report."""
        valid_statuses = [
            self.STATUS_REPORTED,
            self.STATUS_UNDER_INVESTIGATION,
            self.STATUS_RESOLVED,
            self.STATUS_REJECTED
        ]
        
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        self.status = status
        if user_id:
            self.verified_by = user_id
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert report to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date_occurred': self.date_occurred.isoformat() if self.date_occurred else None,
            'date_reported': self.date_reported.isoformat() if self.date_reported else None,
            'status': self.status,
            'is_verified': self.is_verified,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'location_id': self.location_id,
            'crime_type_id': self.crime_type_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'verification_notes': self.metadata.get('verification_notes') if self.metadata else None
        }
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='CASCADE'), nullable=False)
    crime_type_id = db.Column(db.Integer, db.ForeignKey('crime_types.id', ondelete='RESTRICT'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    
    # Geospatial data (duplicated from Location for performance)
    latitude = db.Column(Float, nullable=False)
    longitude = db.Column(Float, nullable=False)
    # Storing as text for SQLite compatibility
    geom = db.Column(Text, nullable=False)  # Store as WKT (Well-Known Text)
    
    # Additional metadata
    report_metadata = db.Column(JSON)  # Store additional report details, evidence, etc.
    tags = db.Column(JSON, default=list)  # Store as JSON for SQLite compatibility
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships are set up in relationships.py to avoid circular imports
    
    def to_dict(self, include_related=True):
        """Convert report to dictionary for JSON serialization.
        
        Args:
            include_related (bool): Whether to include related objects (location, crime_type, etc.)
        """
        result = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date_occurred': self.date_occurred.isoformat(),
            'date_reported': self.date_reported.isoformat(),
            'date_resolved': self.date_resolved.isoformat() if self.date_resolved else None,
            'status': self.status,
            'is_verified': self.is_verified,
            'verification_notes': self.verification_notes,
            'coordinates': {
                'latitude': self.latitude,
                'longitude': self.longitude
            },
            'tags': self.tags,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_related:
            result.update({
                'location': self.location.to_geojson() if self.location else None,
                'crime_type': {
                    'id': self.crime_type.id,
                    'category': self.crime_type.category,
                    'name': self.crime_type.name,
                    'severity': self.crime_type.severity,
                    'is_violent': self.crime_type.is_violent,
                    'code': self.crime_type.code
                } if self.crime_type else None,
                'reporter': {
                    'id': self.reporter.id,
                    'name': self.reporter.get_full_name(),
                    'email': self.reporter.email if self.reporter else None
                } if self.reporter else None,
                'verifier': {
                    'id': self.verifier.id,
                    'name': self.verifier.get_full_name()
                } if self.verifier else None,
                'media': [m.to_dict() for m in self.media.all()] if hasattr(self, 'media') else []
            })
            
        return result
        
    def to_geojson(self, include_properties=True):
        """Convert report to GeoJSON format."""
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [self.longitude, self.latitude]
            },
            'properties': {}
        }
        
        if include_properties:
            feature['properties'] = self.to_dict(include_related=False)
            
        return feature
    
    def __repr__(self):
        return f'<CrimeReport {self.id}: {self.title} ({self.date_occurred.date()})>'


class CrimeMedia(db.Model):
    """Media files (images, videos) associated with crime reports."""
    __tablename__ = 'crime_media'
    
    id = db.Column(db.Integer, primary_key=True)
    crime_report_id = db.Column(db.Integer, db.ForeignKey('crime_reports.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    
    # File information
    file_path = db.Column(db.String(512), nullable=False)
    file_type = db.Column(db.String(50))  # image/jpeg, video/mp4, etc.
    file_size = db.Column(db.Integer)  # Size in bytes
    thumbnail_path = db.Column(db.String(512))  # For images/videos
    
    # Metadata
    caption = db.Column(db.String(255))
    is_primary = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships are set up in relationships.py to avoid circular imports
    
    def to_dict(self):
        """Convert media to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'url': self.file_path,  # Should be replaced with actual URL in the view
            'thumbnail_url': self.thumbnail_path,  # Should be replaced with actual URL
            'file_type': self.file_type,
            'file_size': self.file_size,
            'caption': self.caption,
            'is_primary': self.is_primary,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat(),
            'uploaded_by': {
                'id': self.user.id,
                'name': self.user.get_full_name()
            } if self.user else None
        }
    
    def __repr__(self):
        return f'<CrimeMedia {self.id}: {self.file_path}>'
