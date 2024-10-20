# __init__.py

__version__ = "0.1.4"
__author__="Marcus Milantoni"
__license__="MIT"
__description__="A package created for ease of use working with NumPy in 3D Slicer",


from .image_volume import ImageVolume
from .segment import Segment
from .segmentation_node import SegmentationNode
from .utils import (
    TempNodeManager, PresetColormaps, PetColormaps, volumeNodeTypes, 
    check_type, log_and_raise, load_DICOM, 
    get_volume_nodes_by_type, sweep_screen_capture
)


__all__ = [
    "ImageVolume",
    "Segment",
    "SegmentationNode",
    "TempNodeManager",
    "PresetColormaps",
    "PetColormaps",
    "volumeNodeTypes",
    "check_type",
    "log_and_raise",
    "load_DICOM",
    "create_volume_node",
    "get_volume_nodes_by_type",
    "sweep_screen_capture"
]


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def set_logging_level(level):
    """
    Dynamically change the logging level.
    
    Args:
        level (str): The logging level as a string (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
    """
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    
    logging.getLogger().setLevel(numeric_level)  # Change root logger level
    logger.info(f"Logging level set to {level}")

