__version__ = "1.0.0"
__license__ = "MIT"

from .linea_de_eventos import LineaDeEventos
from .eventos import TipoEvento, Evento

# Define public API
__all__ = [
    # Core classes
    "TipoEvento",
    "Evento",
    "LineaDeEventos",
    # Metadata
    "__version__",
]
