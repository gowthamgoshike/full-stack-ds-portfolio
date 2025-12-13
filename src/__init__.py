# Inside src/__init__.py

# This tells Python: "When someone imports 'src', also expose the DataCleaner 
# class that lives in the cleaning_utils file."
from .cleaning_utils import DataCleaner