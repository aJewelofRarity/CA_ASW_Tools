#----------------------------------------------------------
# File GLOBALS.py
#----------------------------------------------------------
import bpy

G_ColorDir = None
G_BaseFolder = None
G_ColorFolders = None

# - Popup
def ShowMessageBox(title = "Message Box", icon = 'INFO', lines=""):
    myLines=lines
    def draw(self, context):
        for n in myLines:
            self.layout.label(text=n)
            self.layout.ui_units_x = 20
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

def Armature_Item_Callback(self, context):
    items = [("None", "Select Armature", "")]

    for item in bpy.context.scene.objects:
        if item.type == "ARMATURE":
            items.append((item.name, item.name, ""))

    return items

# - Armature Dropdown Properties
class ArmatureDrop(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Scene.arm_items = bpy.props.PointerProperty(type=ArmatureDrop)

    @classmethod
    def unregister(cls):
        del bpy.types.Scene.arm_items

    armatureComboBox : bpy.props.EnumProperty(
        name="",
        description="Armatures in Scene",

        items= Armature_Item_Callback
    )
