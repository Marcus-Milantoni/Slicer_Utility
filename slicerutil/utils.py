# Utility functions
from enum import Enum
import slicer
from DICOMLib import DICOMUtils
import logging
import os
import numpy as np
import ScreenCapture
import matplotlib.pyplot as plt

# Setup the logger
logger = logging.getLogger(__name__)


####################################################################################################
# Utility classes
####################################################################################################

class TempNodeManager:
    def __init__(self, node_class: str, node_name: str) -> None:
        self.scene = slicer.mrmlScene
        self.node_class = node_class
        self.node_name = node_name

    def __enter__(self) -> slicer.vtkMRMLNode:
        self.node = self.scene.AddNewNodeByClass(self.node_class, self.node_name)
        return self.node

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.scene.RemoveNode(self.node)


class PresetColormaps(Enum):
    CT_BONE = 'CT_BONE'
    CT_AIR = 'CT_AIR'
    CT_BRAIN = 'CT_BRAIN'
    CT_ABDOMEN = 'CT_ABDOMEN'
    CT_LUNG = 'CT_LUNG'
    PET = 'PET'
    DTI = 'DTI'


class PetColormaps(Enum):
    PET_HEAT = 'PET-Heat'
    PET_RAINBOW2 = 'PET-Rainbow2'
    LABELS = 'Labels'
    FULL_RAINBOW = 'Full-Rainbow'
    GREY = 'Grey'
    RAINBOW = 'Rainbow'
    INVERTED_GREY = 'Inverted-Grey'
    FMRI = 'fMRI'


class volumeNodeTypes(Enum):
    CT = ['CT ', 'CT_']
    PET = ['PET ', 'PET_', 'suvbw', 'standardized_uptake_value_body_weight']
    MR = ['MR ', 'MR_']
    US = ['US ', 'US_']


####################################################################################################
# Utility functions
####################################################################################################

def check_type(variable, expected_type, variable_name: str):
    """
    Check if a variable is of the expected type.

    Parameters
    ----------
    variable : any
                The variable to check the type of.
    expected_type : type
                The expected type of the variable.
    variable_name : str
                The name of the variable.
    """
    if not isinstance(variable, expected_type):
        raise TypeError(f"The {variable_name} parameter must be a {expected_type.__name__}.")


def log_and_raise(logger, error_message, exception_type=Exception):
    """"
    Log an error message and raise an exception.
    
    Parameters
    ----------
    logger : logging.Logger
                The logger to log the error message.    
    error_message : str
                The error message to log and raise.
    exception_type : Exception, default: Exception
                The type of exception to raise.
    """
    logger.exception(error_message)
    raise exception_type(error_message)


####################################################################################################
# Functions for loading data
####################################################################################################

def load_DICOM(dicomDataDir) -> list:
    """
    This function loads DICOM data into Slicer. This function uses DICOMutils to handle the data types.

    Parameters
    ----------
    dicomDataDir : str
                The directory containing the DICOM data to load.
    
    Returns
    -------
    list
        The list of all loaded node IDs.

    Raises
    ------
    TypeError
        If the dicomDataDir is not a string.
    ValueError
        If the dicomDataDir is not a valid directory.
    """
    if not isinstance(dicomDataDir, str):
        raise TypeError("The dicomDataDir parameter must be a string.")
    if not os.path.isdir(dicomDataDir):
        raise ValueError("The dicomDataDir parameter must be a valid directory.")
    try:
        logger.info(f"Loading DICOM data from directory: {dicomDataDir}")
        loadedNodeIDs = []  # this list will contain the list of all loaded node IDs
        with DICOMUtils.TemporaryDICOMDatabase() as db:
            logger.debug(f"Importing DICOM data from directory: {dicomDataDir}")
            DICOMUtils.importDicom(dicomDataDir, db)
            patientUIDs = db.patients()
            for patientUID in patientUIDs:
                logger.debug(f"Loading patient with UID: {patientUID}")
                loadedNodeIDs.extend(DICOMUtils.loadPatientByUID(patientUID))
        return loadedNodeIDs
    except Exception:
        logger.exception("An error occurred in load_DICOM")
        raise


####################################################################################################
# Functions for creating nodes
####################################################################################################

def get_volume_nodes_by_type(volumeNodeType: volumeNodeTypes) -> dict:
    try:
        matching_nodes = {}
        for volumeNode in slicer.util.getNodesByClass("vtkMRMLVolumeNode"):
            volume_node_name = volumeNode.GetName()
            if any(substring in volume_node_name for substring in volumeNodeType.value):
                matching_nodes[volume_node_name] = volumeNode
        if not matching_nodes:
            raise ValueError("No volume nodes of the specified type were found.")
        return matching_nodes
    except Exception as e:
        log_and_raise(logger, "An error occurred in get_volume_nodes_by_type", type(e))  


####################################################################################################
# functions for saving screen captures
####################################################################################################

def sweep_screen_capture(backgroundImageNode, savePath, saveName, tupleOfSegmentationNodesToShow=None, 
                         view='axial', frameRate=None, startSweepOffset=None, endSweepOffset=None,
                           foregroundImageNode=None, foregroundOpacity=None, numberOfImages= None, ):
    """
    This function captures a sweep of images from a volume node and saves them as a video to a specified location.

    Parameters:
    ------------
    backgroundImageNode: vtkMRMLScalarVolumeNode
        The volume node to capture the images from.
    savePath: str
        The path to save the images to.
    saveName: str
        The name to save the images as.
    tupleOfSegmentationNodesToShow: tuple, optional
        A tuple of vtkMRMLSegmentationNodes to show in the video. Default is None.
    view: str, optional
        The view to capture the images from. Default is 'axial'.
    frameRate: int or float, optional
        The frame rate of the video. Default is None.
    startSweepOffset: int or float, optional
        The offset to start the sweep from. Default is None.
    endSweepOffset: int or float, optional
        The offset to end the sweep at. Default is None.
    foregroundImageNode: vtkMRMLScalarVolumeNode, optional
        The volume node to overlay on the background image. Default is None.
    foregroundOpacity: int or float, optional
        The opacity of the foreground image. Default is None.
    numberOfImages: int, optional
        The number of images to capture. Default is None. 
    
    Returns:
    ---------
    None
    """
    check_type(backgroundImageNode, slicer.vtkMRMLScalarVolumeNode, 'backgroundImageNode')
    check_type(savePath, str, 'savePath')
    check_type(saveName, str, 'saveName')
    if not isinstance(tupleOfSegmentationNodesToShow, tuple) or not tupleOfSegmentationNodesToShow:
        raise TypeError("tupleOfSegmentationNodesToShow must be a tuple or None")
    check_type(view, str, 'view')
    if frameRate is not None and not isinstance(frameRate, (int, float)):
        raise TypeError("frameRate must be an integer or a float or None.")
    if startSweepOffset is not None and not isinstance(startSweepOffset, (int, float)):
        raise TypeError("startSweepOffset must be an integer or a float or None.")
    if endSweepOffset is not None and not isinstance(endSweepOffset, (int, float)):
        raise TypeError("endSweepOffset must be an integer or a float or None.")
    if foregroundImageNode is not None and not isinstance(foregroundImageNode, slicer.vtkMRMLScalarVolumeNode):
        raise TypeError("ForegroundImageNode must be a vtkMRMLScalarVolumeNode or None")
    if numberOfImages is not None and not isinstance(numberOfImages, int):
        raise TypeError("numberOfImages must be an integer")
    if foregroundOpacity is not None and not isinstance(foregroundOpacity, (int, float)):
        raise TypeError("foregroundOpacity must be an integer or a float or None.")
    if foregroundOpacity is not None and not 0 <= foregroundOpacity <= 1:
        raise ValueError("foregroundOpacity must be between 0 and 1")
    if not view.lower() in ['axial', 'sagittal', 'coronal']:
        raise ValueError("view must be either 'axial', 'sagittal' or 'coronal'")
    if not all(isinstance(segmentationNode, slicer.vtkMRMLSegmentationNode) for segmentationNode in tupleOfSegmentationNodesToShow):
        raise ValueError("All elements of tupleOfSegmentationNodesToShow must be vtkMRMLSegmentationNodes")
    if frameRate is not None and not 0 <= frameRate <= 60:
        raise ValueError("frameRate must be between 0 and 60 frames per second")
    # Create the save path if it does not exist
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    # Set the index for the desired view
    logger.debug(f"Setting the view to {view}")
    if view.lower() == 'axial':
        index = 2
        sliceNode = slicer.util.getNode("vtkMRMLSliceNodeRed")
    elif view.lower() == 'sagittal':
        index = 0
        sliceNode = slicer.util.getNode("vtkMRMLSliceNodeYellow")
    elif view.lower() == 'coronal':
        index = 1
        sliceNode = slicer.util.getNode("vtkMRMLSliceNodeGreen")
    # set the start and end sweep offsets if none are provided
    if not startSweepOffset:
        logger.debug("No start sweep offset provided, setting it to the start of the volume")
        if index == 2:
            startSweepOffset = round(backgroundImageNode.GetOrigin()[index], 2)
        else:
            startSweepOffset = round(backgroundImageNode.GetOrigin()[index] - backgroundImageNode.GetSpacing()[index] * (backgroundImageNode.GetImageData().GetDimensions()[index]-1), 2) 
    if not endSweepOffset:
        logger.debug("No end sweep offset provided, setting it to the end of the volume")
        if index == 2:
            endSweepOffset = round(backgroundImageNode.GetOrigin()[index] + backgroundImageNode.GetSpacing()[index] * (backgroundImageNode.GetImageData().GetDimensions()[index]-1), 2)
        else:
            round(backgroundImageNode.GetOrigin()[index], 2)
    if not numberOfImages:
        logger.debug("No number of images provided, setting it to the number of slices in the volume")
        numberOfImages = backgroundImageNode.GetImageData().GetDimensions()[index] - 1 # Set the number of images to the number of slices in the volume
    if not frameRate:
        logger.debug("No frame rate provided, setting it to 6 frames per second")
        frameRate = 4 # Set the frame rate to 6 frames per second
    # Set the foreground opacity to 50% if none is provided and there is a foreground image
    if foregroundImageNode and not foregroundOpacity:
        logger.debug("Foreground image provided but no opacity, setting opacity to 50%")
        foregroundOpacity = 0.5
    # Set the display to what is desired for the video
    logger.debug(f"Setting the display for the {view} view")
    slicer.util.setSliceViewerLayers(background=backgroundImageNode, foreground=foregroundImageNode, foregroundOpacity=foregroundOpacity)
    for currentSegmentationNode in slicer.util.getNodesByClass("vtkMRMLSegmentationNode"): # Hide all segmentations
        currentSegmentationNode.GetDisplayNode().SetVisibility(False)
    if tupleOfSegmentationNodesToShow:
        for currentSegmentationNode in tupleOfSegmentationNodesToShow: # Show the desired segmentations
            currentSegmentationNode.GetDisplayNode().SetVisibility(True)
    # Capture the individual images
    logger.debug(f"Capturing {numberOfImages} images from {startSweepOffset} to {endSweepOffset} in the {view} view")
    ScreenCapture.ScreenCaptureLogic().captureSliceSweep(sliceNode, startSweepOffset, endSweepOffset, numberOfImages, savePath, f"{saveName}_%05d.png")
    # create the video freom the images
    logger.debug(f"Creating video from images at {savePath}/{saveName}.mp4")
    ScreenCapture.ScreenCaptureLogic().createVideo(frameRate, "-codec libx264 -preset slower -pix_fmt yuv420p", savePath, f"{saveName}_%05d.png", f"{saveName}.mp4")
    # Delete the temporairly saved images after the video is created
    for imageIndex in range(numberOfImages):
       logger.debug(f"Deleting {savePath}/{saveName}_{imageIndex:05d}.png")
       os.remove(os.path.join(savePath, f"{saveName}_{imageIndex:05d}.png"))

