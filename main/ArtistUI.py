import bpy
from bpy.app.handlers import persistent
from rna_prop_ui import PropertyPanel


import os




class addNewColourStyle(bpy.types.Operator):
    bl_idname = 'add.colorstyle'
    bl_label = 'Save New Colour Style'
    bl_description = 'Append new colour style to colour list'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print(">:3c")
        self.report({'INFO'}, '>:3c')
        return {'FINISHED'}

class nextColorStyle(bpy.types.Operator):
    bl_idname = 'next.colorstyle'
    bl_label = 'Next CS'
    bl_description = 'Next colour style'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        Outfit_Generator
        return {'FINISHED'}

# ---------------------- Panels ----------------------------

class WCUSTOM_PT_ArtistUI(bpy.types.Panel):
    bl_label ="Colour Panel"
    bl_idname = "WCUSTOM_PT_ArtistUI"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ARTIST'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        box = row.box()
        box.label(text="wrow")

        row = layout.row()
        row.operator(nextColorStyle.bl_idname, text=nextColorStyle.bl_label)
        row.prop(mytool, "colourStyleIndex", text='')
        # row.label(text="{:03d}".format(int(bpy.context.scene.my_tool.colourStyleIndex)))
        row.operator(nextColorStyle.bl_idname, text=nextColorStyle.bl_label)

        row = layout.row()
        row.operator(addNewColourStyle.bl_idname, text=addNewColourStyle.bl_label)