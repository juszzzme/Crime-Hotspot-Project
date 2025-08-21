from app.extensions import db

def setup_relationships():
    """Set up all model relationships to avoid circular imports."""
    from app.models.user import User
    from app.models.crime_data import CrimeReport, Location, CrimeType, CrimeMedia
    
    # User relationships
    User.submitted_reports = db.relationship(
        'CrimeReport',
        foreign_keys='CrimeReport.user_id',
        back_populates='reporter',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    User.verified_reports = db.relationship(
        'CrimeReport',
        foreign_keys='CrimeReport.verified_by',
        back_populates='verifier',
        lazy='dynamic'
    )
    
    # CrimeReport relationships
    CrimeReport.reporter = db.relationship(
        'User',
        foreign_keys='CrimeReport.user_id',
        back_populates='submitted_reports'
    )
    
    CrimeReport.verifier = db.relationship(
        'User',
        foreign_keys='CrimeReport.verified_by',
        back_populates='verified_reports'
    )
    
    CrimeReport.location_rel = db.relationship(
        'Location',
        back_populates='crime_reports'
    )
    
    CrimeReport.crime_type_rel = db.relationship(
        'CrimeType',
        back_populates='crime_reports'
    )
    
    # Location relationships
    Location.crime_reports = db.relationship(
        'CrimeReport',
        back_populates='location_rel',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    # CrimeType relationships
    CrimeType.crime_reports = db.relationship(
        'CrimeReport',
        back_populates='crime_type_rel',
        lazy='dynamic'
    )
    
    # CrimeMedia relationships
    CrimeMedia.crime_report_rel = db.relationship(
        'CrimeReport',
        back_populates='media'
    )
    
    CrimeReport.media = db.relationship(
        'CrimeMedia',
        back_populates='crime_report_rel',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
