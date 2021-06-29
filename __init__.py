#----------------------------------------------------------
# File __init__.py
#----------------------------------------------------------
import bpy
from bpy.types import Operator

from . import renderTools
from . import textureTools
from . import GLOBALS

bl_info = {
    "name": "Chubs and Aerthas ArcSystemWorks Tools",
    "author": "Chubs & Aerthas Veras",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "description": "Tools made to work with ArcSystemWorks models exported from Umodel as GLTF",
    "warning": "",
    "doc_url": "",
    "category": "Rigging",
}

classes = (
    textureTools
)

classes = (
    GLOBALS.ArmatureDrop,
    renderTools.CA_PT_RenderPanel,
    textureTools.CA_PT_TexEditPanel,
    textureTools.ImgRefresh,
    textureTools.CleanUnused,
    textureTools.AlphOn,
    textureTools.AlphOff,
    textureTools.ApplyColor,
    textureTools.ColorsDrop,
    textureTools.SelectColorFolder,
    renderTools.ClearMatOP,
    renderTools.BoneInFront
)

register, unregister = bpy.utils.register_classes_factory(classes)
