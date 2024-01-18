#----------------------------------------------------------
# File textureTools.py
#----------------------------------------------------------
import bpy
import os
from . import GLOBALS
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

# - Toggle Image Alpha Function
def ImgAlpha(context, val):
    for img in bpy.data.images:
        if img.source == "FILE":
            img.alpha_mode = val

def Color_Item_Callback(self, context):
    items = [("None", "Select Color", "")]

    if GLOBALS.G_ColorFolders != None:
        for item in GLOBALS.G_ColorFolders:
            normalized_path = os.path.normpath(item)
            path_components = normalized_path.split(os.sep)

            dirName = path_components[len(path_components) - 1]
            if "color" in dirName.lower():
                items.append((item, dirName, ""))

    return items

def Character_Item_Callback(self, context):
    items = []
    chrStrive = [
        ("ANJ", "Anji", ""),
        ("ASK", "Asuka", ""),
        ("AXL", "Axl", ""),
        ("BED", "Bedman", ""),
        ("BGT", "Bridget", ""),
        ("BKN", "Baiken", ""),
        ("CHP", "Chipp", ""),
        ("COS", "Happy Chaos", ""),
        ("ELP", "Elphelt", ""),
        ("FAU", "Faust", ""),
        ("GIO", "Giovanna", ""),
        ("GLD", "Goldlewis", ""),
        ("INO", "I-NO", ""),
        #("JAM", "Jam", ""),
        ("JKO", "Jack'O", ""),
        ("KYK", "Ky", ""),
        ("LEO", "Leo", ""),
        ("MAY", "May", ""),
        ("MLL", "Millia", ""),
        ("NAG", "Nagoriyuki", ""),
        ("POT", "Potemkin", ""),
        ("RAM", "Ramlethal", ""),
        ("SIN", "Sin", ""),
        ("SOL", "Sol", ""),
        ("DSL", "Sol Dragon Install", ""),
        ("TST", "Testament", ""),
        ("ZAT", "Zato", ""),
        #("EDY", "Eddie", ""),
    ]

    chrFighterZ = [
        ("GKS", "Goku (SSJ)", ""),
        ("VGS", "Vegeta (SSJ)", ""),
        ("PCN", "Piccolo", ""),
        ("GHT", "Teen Gohan", ""),
        ("FRN", "Frieza", ""),
        ("TRS", "Future Trunks", ""),
        ("CEN", "Cell", ""),
        ("AEN", "Android 18", ""),
        ("GTL", "Gotenks", ""),
        ("KRN", "Krillin", ""),
        ("BUK", "Kid Buu", ""),
        ("BUN", "Majin Buu", ""),
        ("ASN", "Android 16", ""),
        ("YMN", "Yamcha", ""),
        ("TNN", "Tien", ""),
        ("GHU", "Adult Gohan", ""),
        ("HTN", "Hit", ""),
        ("GKB", "Goku (SSGSS)", ""),
        ("VGB", "Vegeta (SSGSS)", ""),
        ("BSN", "Beerus", ""),
        ("GBR", "Goku Black", ""),
        ("TON", "Android 21", ""),
        ("TOA", "Android 21 (Evil)", ""),
        ("TOZ", "Android 21 (Good)", ""),
        ("GKN", "Goku", ""),
        ("VGN", "Vegeta", ""),
        ("BRS", "Broly (DBZ)", ""),
        ("ZMB", "Fused Zamasu", ""),
        ("BDN", "Bardock", ""),
        ("VTB", "Vegito(SSGSS)", ""),
        ("AVP", "Android 17", ""),
        ("CLF", "Cooler", ""),
        ("JRN", "Jiren", ""),
        ("VDN", "Videl", ""),
        ("VDL", "Videl (Pigtails)", ""),
        ("SGN", "Goku GT", ""),
        ("JNN", "Janemba", ""),
        ("NHY", "Gogeta (SSGSS)", ""),
        ("EST", "Broly (DBS)", ""),
        ("MTN", "Roshi", ""),
        ("OSM", "Super Baby 2", ""),
        ("GFF", "Gogeta (SSJ4)", "")
    ]

    if context.scene.color_props.gameComboBox == "GGST":
        items = chrStrive
    else:
        items = chrFighterZ

    return items

def GetArmMeshAndApplyTexture(context, ArmDrop):
    myLines= (
        "Please make sure select an armature from the dropdown",
        "and try again."
    )
    if ArmDrop == "None":
        GLOBALS.ShowMessageBox(title="No Armature Selected", icon='ERROR', lines=myLines)
        return
    elif len(ArmDrop) == 0:
        GLOBALS.ShowMessageBox(title="Invalid Selection", icon='ERROR', lines=myLines)
        return

    obj = bpy.data.objects[ArmDrop]
    children = [ob for ob in bpy.data.objects if ob.parent == obj]

    props = context.scene.color_props
    print("pressed")
    for i in children:
        ApplyTextures(context.object, i, props.colorSlotsComboBox, props.charactersComboBox, props.texTypeComboBox, props.shaderBool)

def ApplyTextures(context, meshObj, TexDrop, CharDrop, TexTypeDrop, BoolShader):
    print("pressed2")
    myLines= (
        "Please make sure select an color from the dropdown",
        "and try again."
    )
    if TexDrop == "None":
        GLOBALS.ShowMessageBox(title="No Color Selected", icon='ERROR', lines=myLines)
        return
    elif len(TexDrop) == 0:
        GLOBALS.ShowMessageBox(title="Invalid Selection", icon='ERROR', lines=myLines)
        return

    for i in range(0,len(bpy.data.objects)):
            bpy.data.objects[i].select_set(False)

    bpy.context.view_layer.objects.active = meshObj
    meshObj.select_set(True)

    slots = meshObj.material_slots

    for m in slots:
        mat = m.material
        colorFiles = [ f.path for f in os.scandir(TexDrop) ]
        baseFiles = [ f.path for f in os.scandir(GLOBALS.G_BaseFolder) ]

        base = None
        sss = None
        ilm = None
        detail = None
        decal = None

        # - Make sure no suffix added if base
        if TexTypeDrop == "Base":
            TexTypeDrop = ""

        BuildBase = CharDrop + TexTypeDrop + "_base.tga"
        BuildSSS = CharDrop + TexTypeDrop + "_Sss.tga"

        if TexTypeDrop == "P":
            BuildILM = CharDrop + "_ilm.tga"
        elif TexTypeDrop == "WP":
            BuildILM = CharDrop + "W_ilm.tga"
        else:
            BuildILM = CharDrop + TexTypeDrop + "_ilm.tga"

        if CharDrop == "DSL":
            BuildDetail = "SOL_detail.tga"
            BuildDecal = "SOL_decal.tga"
        else:
            BuildDetail = CharDrop + "_detail.tga"
            BuildDecal = CharDrop + "_decal.tga"

        # - Color Folder Files
        for i in colorFiles:
            if BuildBase in str(i):
                base = i

            if BuildSSS in str(i):
                sss = i

            if BuildDecal in str(i):
                if CharDrop != "EDY":
                    decal = i

        # - Base Folder Files
        for i in baseFiles:
            if BuildILM in str(i):
                ilm = i

            if BuildDetail in str(i):
                detail = i

            if BuildDecal in str(i):
                if CharDrop == "EDY":
                    decal = i

        if base == None:
            Error = "Looks like there is no file called " + BuildBase + " in this folder"
            myLines=(Error, "Tip: Select the correct character and texture type")
            GLOBALS.ShowMessageBox(title="Uh-oh", icon='ERROR', lines=myLines)
            return

        if sss == None:
            Error = "Looks like there is no file called " + BuildSSS + " in this folder"
            myLines=(Error, "Tip: Select the correct character and texture type")
            GLOBALS.ShowMessageBox(title="Uh-oh", icon='ERROR', lines=myLines)
            return

        if ilm == None:
            Error = "Looks like there is no file called " + BuildILM + " in this folder"
            myLines=(Error, "Tip: Select the correct character and texture type")
            GLOBALS.ShowMessageBox(title="Uh-oh", icon='ERROR', lines=myLines)
            return

        if detail == None:
            Error = "Looks like there is no file called " + BuildDetail + " in this folder"
            myLines=(Error, "Tip: Select the correct character and texture type")
            GLOBALS.ShowMessageBox(title="Uh-oh", icon='ERROR', lines=myLines)
            return

        nodes = mat.node_tree.nodes
        for node in nodes:
            if node.type != 'OUTPUT_MATERIAL': # skip the material output node as we'll need it later
                nodes.remove(node)

        if BoolShader == False:
            if "decal" not in mat.name.lower():
                if "_di_" in mat.name.lower():
                    print("Replacing Ky")
                    if CharDrop == "KYK":
                        base = base.replace("KYK_base.tga", "DKY_base.tga")
                        sss = sss.replace("KYK_Sss.tga", "DKY_Sss.tga")
                        ilm = ilm.replace("KYK_ilm.tga", "DKY_ilm.tga")
                if "_wep_" in mat.name.lower():
                    if CharDrop == "KYK":
                        base = base.replace("KYK_base.tga", "KYKW_base.tga")
                        sss = sss.replace("KYK_Sss.tga", "KYKW_Sss.tga")
                        ilm = ilm.replace("KYK_ilm.tga", "KYKW_ilm.tga")


                ## Create Basic Shader
                mat.use_nodes = True
                bsdf = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
                shadertorgb = mat.node_tree.nodes.new("ShaderNodeShaderToRGB")
                out = mat.node_tree.nodes["Material Output"]
                texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
                texImage.image = bpy.data.images.load(base)
                mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
                mat.node_tree.links.new(out.inputs['Surface'], bsdf.outputs['BSDF'])
                mat.node_tree.links.new(shadertorgb.inputs['Shader'], texImage.outputs['Alpha'])
        else:
            if "decal" in mat.name.lower():
                Arc = nodes.new("ShaderNodeGroup")
                Arc.node_tree = bpy.data.node_groups['Decal/Damage']
                Dec = mat.node_tree.nodes.new('ShaderNodeTexImage')
                out = mat.node_tree.nodes["Material Output"]

                mat.node_tree.links.new(Dec.outputs['Color'], Arc.inputs['Decal/Damage'])

                mat.node_tree.links.new(Arc.outputs['Out'], out.inputs['Surface'])

                Dec.image = bpy.data.images.load(decal)

                mat.blend_method = 'BLEND'
                mat.shadow_method = 'CLIP'
            else:
                if "_di_" in mat.name.lower():
                    print("Replacing Ky")
                    if CharDrop == "KYK":
                        base = base.replace("KYK_base.tga", "DKY_base.tga")
                        sss = sss.replace("KYK_Sss.tga", "DKY_Sss.tga")
                        ilm = ilm.replace("KYK_ilm.tga", "DKY_ilm.tga")
                if "_wep_" in mat.name.lower():
                    if CharDrop == "KYK":
                        base = base.replace("KYK_base.tga", "KYKW_base.tga")
                        sss = sss.replace("KYK_Sss.tga", "KYKW_Sss.tga")
                        ilm = ilm.replace("KYK_ilm.tga", "KYKW_ilm.tga")

                ## Create ArcSys Shader (Requires Append)
                Arc = nodes.new("ShaderNodeGroup")
                Arc.node_tree = bpy.data.node_groups['Arc System Works - Strive']
                BaseTex = mat.node_tree.nodes.new('ShaderNodeTexImage')
                SssTex = mat.node_tree.nodes.new('ShaderNodeTexImage')
                ILMTex = mat.node_tree.nodes.new('ShaderNodeTexImage')
                DetailTex = mat.node_tree.nodes.new('ShaderNodeTexImage')
                map = UVMap = mat.node_tree.nodes.new("ShaderNodeUVMap")
                out = mat.node_tree.nodes["Material Output"]

                map.uv_map = "UVMap.001"

                mat.node_tree.links.new(Arc.outputs['Color'], out.inputs['Surface'])

                mat.node_tree.links.new(BaseTex.outputs['Color'], Arc.inputs['Base'])
                mat.node_tree.links.new(BaseTex.outputs['Alpha'], Arc.inputs['Base Alpha'])

                mat.node_tree.links.new(SssTex.outputs['Color'], Arc.inputs['SSS'])
                mat.node_tree.links.new(SssTex.outputs['Alpha'], Arc.inputs['SSS Alpha'])

                mat.node_tree.links.new(ILMTex.outputs['Color'], Arc.inputs['ILM Linear'])
                mat.node_tree.links.new(ILMTex.outputs['Alpha'], Arc.inputs['ILM Alpha'])

                mat.node_tree.links.new(DetailTex.outputs['Color'], Arc.inputs['Detail'])
                mat.node_tree.links.new(UVMap.outputs['UV'], DetailTex.inputs['Vector'])

                BaseTex.image = bpy.data.images.load(base)
                SssTex.image = bpy.data.images.load(sss)
                ILMTex.image = bpy.data.images.load(ilm)
                ILMTex.image.colorspace_settings.name = 'Linear'
                DetailTex.image = bpy.data.images.load(detail)



        bpy.context.space_data.shading.type = 'MATERIAL'

def RefreshImages(context):
    # Clean up unused images
    for img in bpy.data.images:
        if not img.users or (img.users == 1 and img.use_fake_user):
            bpy.data.images.remove(img)

    #Reload all File images
    for img in bpy.data.images :
        if img.source == 'FILE' :
            img.reload()

# - Refresh Images Class
class ImgRefresh(bpy.types.Operator):
    """Refresh All Images"""
    bl_idname = "tex.img_refresh"
    bl_label = "Refresh Textures"

    def execute(self, context):
        RefreshImages(context)
        return{"FINISHED"}

# - Clean Unused Class
class CleanUnused(bpy.types.Operator):
    """Purges all unused meshes, materials and images"""
    bl_idname = "tex.clean_unused"
    bl_label = "Purge All Orphaned Data"

    def execute(self, context):
        for block in bpy.data.armatures:
            if block.users == 0:
                bpy.data.armatures.remove(block)

        for block in bpy.data.meshes:
            if block.users == 0:
                bpy.data.meshes.remove(block)

        for block in bpy.data.materials:
            if block.users == 0:
                bpy.data.materials.remove(block)

        for block in bpy.data.textures:
            if block.users == 0:
                bpy.data.textures.remove(block)

        for block in bpy.data.images:
            if block.users == 0:
                bpy.data.images.remove(block)
        return {"FINISHED"}

# - Image Alpha On
class AlphOn(bpy.types.Operator):
    """Turn on all images alpha"""
    bl_idname = "tex.alph_on"
    bl_label = "Alpha On"

    def execute(self, context):
        ImgAlpha(context, "STRAIGHT")
        return {"FINISHED"}

# - Image Alpha Off
class AlphOff(bpy.types.Operator):
    """Turn off all images alpha"""
    bl_idname = "tex.alph_off"
    bl_label = "Alpha Off"

    def execute(self, context):
        ImgAlpha(context, "NONE")
        return {"FINISHED"}

#- Apply Color
class ApplyColor(bpy.types.Operator):
    """Apply selected color slot to selected armature"""
    bl_idname = "tex.apply_color"
    bl_label = "Apply Color"

    def execute(self, context):
        GetArmMeshAndApplyTexture(context, context.scene.arm_items.armatureComboBox)
        return {'FINISHED'}

# - Color Slot Dropdown Properties
class ColorsDrop(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Scene.color_props = bpy.props.PointerProperty(type=ColorsDrop)

    @classmethod
    def unregister(cld):
        del bpy.types.Scene.color_props

    shaderBool : bpy.props.BoolProperty(
        name="Use ArcSys Shader",
        description="Build Shader Using ArcSys Shader by Aerthas Veras"
    )

    colorSlotsComboBox : bpy.props.EnumProperty(
        name="",
        description="LIst of colors from color folder",

        items= Color_Item_Callback
    )

    gameComboBox : bpy.props.EnumProperty(
        name= "",
        description= "Game",
        items= [
            ("GGST", "Strive", ""),
            ("FZ", "FighterZ", ""),
        ]
    )

    charactersComboBox : bpy.props.EnumProperty(
        name= "",
        description= "Character",
        items= Character_Item_Callback
    )

    texTypeComboBox : bpy.props.EnumProperty(
        name= "",
        description= "Texture Types",
        items= [
            ("Base", "Base", ""),
            ("W", "Weapon", ""),
            ("W2", "Anji Weapon Overdrive", ""),
            ("D", "Ramlethal Dog", ""),
            ("P", "Giovanna Powered Up", ""),
            ("WP", "Rei Powered Up", ""),
            ("G", "May Goshogawara", ""),
            ("Y", "May Yamada", ""),
            ("Flare", "Sol Dragon Install Flare", ""),
            ("HairEff", "Millia Hair Effect", ""),
        ]
    )

class SelectColorFolder(bpy.types.Operator, ImportHelper):
    """Select Folder that contains your Base & ColorXX Folders (Base & ColorXX Folders Must contain Appropriate textures)"""
    bl_idname= "open.color_folder"
    bl_label = "Select Colors Folder"
    bl_options = {"REGISTER"}

    directory = bpy.props.StringProperty(
        name="Colors Path",
        description="Directory where colors are"
    )

    def execute(self, context):

        filename, extension = os.path.splitext(self.filepath)

        GLOBALS.G_ColorDir = self.filepath
        GLOBALS.G_ColorFolders = [ f.path for f in os.scandir(GLOBALS.G_ColorDir) if f.is_dir() ]

        if GLOBALS.G_ColorFolders != None:
            for item in GLOBALS.G_ColorFolders:
                normalized_path = os.path.normpath(item)
                path_components = normalized_path.split(os.sep)

                dirName = path_components[len(path_components) - 1]
                if "base" in dirName.lower():
                    print("Setting " + str(item) + " as base")
                    GLOBALS.G_BaseFolder = item

        return {"FINISHED"}

# - Texture Tools Panel
class CA_PT_TexEditPanel(bpy.types.Panel):
    bl_label = "Texture Preview Tools"
    bl_idnsme = "CA_PT_TexLayout"
    bl_category = "C&A ASW Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    # - Draw Function
    def draw(self, context):
        layout = self.layout

        # - Image Refresh Button & Clean Unused Button
        row = layout.row()
        row.scale_y = 1.4
        row.operator("tex.img_refresh")
        row.operator("tex.clean_unused")

        # - Alpha on & off
        row = layout.row()
        row.scale_y = 1.4
        row.operator("tex.alph_on")
        row.operator("tex.alph_off")

        # -- Advanced Texture Previewing -- #
        row = layout.row()
        row.scale_y = 0.7
        row.label(text= "Advanced Texture Preview")

        row = layout.row()
        row.scale_y = 0.7
        row.label(text= "    Current Folder:")

        row = layout.row()
        row.scale_y = 0.7
        row.label(text= "    " + str(GLOBALS.G_ColorDir))

        row = layout.row()
        row.scale_y = 1.3
        row.operator("open.color_folder")
        #row.prop(context.scene.color_props, "gameComboBox")
        row.prop(context.scene.color_props, "shaderBool")

        row = layout.row()
        row.scale_y = 1.4
        row.operator("tex.apply_color")
        row.prop(context.scene.arm_items, "armatureComboBox")
        row.prop(context.scene.color_props, "colorSlotsComboBox")

        row = layout.row()
        row.scale_y = 1.4
        row.prop(context.scene.color_props, "charactersComboBox")
        row.prop(context.scene.color_props, "texTypeComboBox")
