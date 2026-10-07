"""
backend/app/services/ml_service.py
ML model loading and management service.
"""
import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))

from ml.models import models_exist
from ml.consensus import get_engine


class MLService:
    """Singleton service for ML model management."""

    def __init__(self):
        self._engine = None
        self._loaded = False

    def ensure_loaded(self):
        """Load models if not already loaded."""
        if not self._loaded:
            if not models_exist():
                raise RuntimeError(
                    "ML models not found. Please run 'python ml/train_models.py' first."
                )
            self._engine = get_engine()
            self._loaded = True

    @property
    def engine(self):
        self.ensure_loaded()
        return self._engine

    @property
    def is_loaded(self):
        return self._loaded


# Global singleton
_ml_service = MLService()


def get_ml_service() -> MLService:
    return _ml_service
