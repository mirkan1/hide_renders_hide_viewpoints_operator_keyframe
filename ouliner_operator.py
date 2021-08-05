bl_info = {
    "name" : "hide_renders_hide_viewpoints_operator",
    "author" : "raq/mirkan1",
    "description" : "hide renders and hide viewpoints",
    "blender" : (2, 93, 0),
    "location" : "View3D",
    "category" : "Generic"
}

import bpy
from time import sleep
            
class Collection_Iterator(bpy.types.Operator):
    bl_idname = "outliner.hide_renders_hide_viewpoints_operator"
    bl_label = "hide_renders_hide_viewpoints_operator"
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'OUTLINER'

    def get_selected_collection_name(self, context):
        for item in context.selected_ids:
            if item.bl_rna.identifier == "Collection":
                return item.name
                
    def execute(self, context):
        name = self.get_selected_collection_name(context)
        length = len(bpy.data.collections[name].all_objects)
        current_frame = bpy.data.scenes['Scene'].frame_current
        
        hide_viewport = bpy.data.collections[name].hide_viewport
        hide_render = bpy.data.collections[name].hide_render
        # print(f"{hide_viewport=},{hide_render=}")
        # task = "hide_viewport"
        # task = "hide_render"
        count = 0
        while count < length:
            bpy.data.collections[name].all_objects[count].hide_viewport = hide_viewport
            bpy.data.collections[name].all_objects[count].keyframe_insert(data_path="hide_viewport", frame=current_frame)
            
            bpy.data.collections[name].all_objects[count].hide_render = hide_render
            bpy.data.collections[name].all_objects[count].keyframe_insert(data_path="hide_render", frame=current_frame)
            
            count+=1
        return {'FINISHED'}
    
class Collection_Keyframe_Cleaner(bpy.types.Operator):
    bl_idname = "outliner.clear_renders_clear_viewpoints_created"
    bl_label = "clear_renders_clear_viewpoints_created"
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'OUTLINER'

    def get_selected_collection_name(self, context):
        for item in context.selected_ids:
            if item.bl_rna.identifier == "Collection":
                return item.name
                
    def execute(self, context):
        name = self.get_selected_collection_name(context)
        length = len(bpy.data.collections[name].all_objects)
        count = 0
        while count < length:
            try:
                remove_types = ["hide_viewport", "hide_render"]
                fcurves = [
                    fc for fc in bpy.data.collections[name].all_objects[count].animation_data.action.fcurves
                    for type in remove_types
                    if fc.data_path.startswith(type)
                ]
                # remove fcurves
                while(fcurves):
                    fc = fcurves.pop()
                    bpy.data.collections[name].all_objects[count].animation_data.action.fcurves.remove(fc)
            except:
                pass
            count+=1
        return {'FINISHED'}

#GUI
class KeyFrameAutomatorPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Viewpoint, Render'
    bl_options = {'DEFAULT_CLOSED'}
    bl_idname = "outliner.key_frame_automator"
    bl_label = "Viewpoint, Render Tooltip"
    bl_space_type = "VIEW_3D"

    def draw(self, context):
        layout = self.layout  
        row = layout.row()      
        row.label(text="Click on The Asset Group")
        row = layout.row()
        row.label(text="Disable/Enable in Viewpoint or Disable Renders or both on Outliner section")
        row = layout.row()
        row.operator("outliner.hide_renders_hide_viewpoints_operator", text='''Click "Shift + Q" While Asset Group is Selected''')
        row = layout.row()
        row.label(text='''Clear "hide_viewport" and "hide_render" keyframes For The Selected Asset Group''')
        row = layout.row()
        row.operator("outliner.clear_renders_clear_viewpoints_created", text='''Click "Shift + T" While Asset Group is Selected''')
    
addon_keymaps = [] 
classes = (Collection_Iterator, KeyFrameAutomatorPanel, Collection_Keyframe_Cleaner)

def register():
    from bpy.utils import register_class
    # register_class(MessageBoxOperator)
    for cls in classes:
        register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
        kmi = km.keymap_items.new(Collection_Iterator.bl_idname, 'Q', 'PRESS', shift=True)
        addon_keymaps.append((km, kmi))
        km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
        kmi = km.keymap_items.new(Collection_Keyframe_Cleaner.bl_idname, 'T', 'PRESS', shift=True)
        addon_keymaps.append((km, kmi))

if __name__ == "__main__":
    print("iinstalled")
    register()