"""Resonance Ionization Mass Spectrometry (RIMS) Data Evaluation for CRD Files."""

import iniabu

from . import data_io
from . import guis
from . import interfacer
from . import utilities
from ._version import __version__
from .multi_proc import MultiFileProcessor
from .processor import CRDFileProcessor

VERBOSITY = 0

ini = iniabu.IniAbu(database="nist")

__all__ = [
    "VERBOSITY",
    "ini",
    "CRDFileProcessor",
    "data_io",
    "guis",
    "interfacer",
    "MultiFileProcessor",
    "utilities",
    "__version__",
]

__title__ = "rimseval"
__description__ = (
    "Evaluate resonance ionization mass spectrometry measurements, correct, and "
    "filter. Contains a reader for crd files (Chicago Raw Data) but can also convert "
    "FastComTec lst files to crd."
)

__uri__ = "https://rimseval.readthedocs.io"
__author__ = "Reto Trappitsch"

__license__ = "MIT"
__copyright__ = "Copyright (c) 2020-2023, Reto Trappitsch"
