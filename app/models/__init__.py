# Import all models here for easier access
from .user import User
from .crime_data import CrimeReport, CrimeType, Location, CrimeMedia
from .relationships import setup_relationships

# Set up all relationships after all models are imported
setup_relationships()

__all__ = ['User', 'CrimeReport', 'CrimeType', 'Location', 'CrimeMedia']
