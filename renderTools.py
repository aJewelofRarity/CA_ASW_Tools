#----------------------------------------------------------
# File renderTools.py
#----------------------------------------------------------
import bpy
from . import GLOBALS

# Clear Mats ##
def ClearMatsMesh(context):
    obj = context
    for i in range(0,len(bpy.data.objects)):
            bpy.data.objects[i].select_set(False)

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    slots = obj.material_slots
    # Verify mode is set to Object mode
    if str(obj.mode) == "OBJECT" or "POSE":
        bpy.ops.object.mode_set(mode='EDIT')

    bpy.ops.mesh.select_all(action='DESELECT')

    matIndex = -1
    for i in range(0,len(slots)):
        matIndex=matIndex+1
        obj.active_material_index = matIndex
        if str(obj.active_material).lower().find("shadow") > 0 or str(obj.active_material).lower().find("outline") > 0 or str(obj.active_material).lower().find("damage_decal") > 0:
            #print("Junk Material found: "+str(obj.active_material.name +". Deleting mesh."))
            bpy.ops.object.material_slot_select()
            bpy.ops.mesh.delete(type='FACE')
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.material_slot_remove()
            bpy.ops.object.mode_set(mode='EDIT')
            matIndex=matIndex-1

    bpy.ops.object.mode_set(mode='OBJECT')

def ClearMats(context, ArmDrop):
    ## Error Check the current dropdown selection
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

    ## Set Armature Variable
    obj = bpy.data.objects[ArmDrop]
    children = [ob for ob in bpy.data.objects if ob.parent == obj]
    for i in children:
        ClearMatsMesh(i)
## Clear mats END ##

class BoneInFront(bpy.types.Operator):
    """Set Bones to show in front and to display as 'BOUNDS' & 'STICK'"""
    bl_idname = "object.bone_in_front"
    bl_label = "Set Armature Bones InFront"

    def execute(self, context):
        ## Error Check the current dropdown selection
        myLines= (
            "Please make sure select an armature from the dropdown",
            "and try again."
        )
        if context.scene.arm_items.armatureComboBox == "None":
            GLOBALS.ShowMessageBox(title="No Armature Selected", icon='ERROR', lines=myLines)
            return {'FINISHED'}
        elif len(context.scene.arm_items.armatureComboBox) == 0:
            GLOBALS.ShowMessageBox(title="Invalid Selection", icon='ERROR', lines=myLines)
            return {'FINISHED'}

        ## Set Armature Variable
        obj = bpy.data.objects[context.scene.arm_items.armatureComboBox]
        obj.show_in_front = True
        obj.display_type = 'BOUNDS'
        obj.data.display_type = 'STICK'
        return  {'FINISHED'}

class ClearMatOP(bpy.types.Operator):
    """Removes Shadow and Outline Mesh"""
    bl_idname = "object.clear_mat"
    bl_label = "Clear Junk Materials"

    def execute(self, context):
        ClearMats(context, context.scene.arm_items.armatureComboBox)
        return {'FINISHED'}

class CA_PT_RenderPanel(bpy.types.Panel):
    bl_label = "Rendering Tools"
    bl_idname = "CA_RENDER_PT_layout"
    bl_category = "C&A ASW Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.scale_y = 1.4
        row.prop(context.scene.arm_items, "armatureComboBox")
        row.operator("object.bone_in_front")
        row.operator("object.clear_mat")
