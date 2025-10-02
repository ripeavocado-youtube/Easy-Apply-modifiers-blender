bl_info = {
    "name": "Apply All Modifiers Button",
    "author": "YourName",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Properties > Modifiers Tab",
    "description": "Adds a button above 'Add Modifier' to apply all modifiers in order.",
    "warning": "",
    "category": "Object",
    "license": "MIT",
}

import bpy

# ------------------------------
# Operator: Apply All Modifiers
# ------------------------------
class OBJECT_OT_apply_all_modifiers(bpy.types.Operator):
    """Apply all modifiers in order"""
    bl_idname = "object.apply_all_modifiers"
    bl_label = "Apply All Modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or not obj.modifiers:
            self.report({'INFO'}, "No modifiers to apply")
            return {'CANCELLED'}

        # Apply modifiers in correct order
        for modifier in obj.modifiers[:]:
            try:
                bpy.ops.object.modifier_apply(modifier=modifier.name)
            except:
                self.report({'WARNING'}, f"Could not apply {modifier.name}")

        self.report({'INFO'}, "All modifiers applied")
        return {'FINISHED'}


# ------------------------------
# Panel: Add button above Add Modifier
# ------------------------------
class OBJECT_PT_apply_all_above(bpy.types.Panel):
    bl_label = "Modifier Tools"
    bl_idname = "OBJECT_PT_apply_all_above"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.apply_all_modifiers", icon="CHECKMARK")


# ------------------------------
# Registration Helpers
# ------------------------------
classes = (
    OBJECT_OT_apply_all_modifiers,
    OBJECT_PT_apply_all_above,
)

def register():
    for cls in classes:
        if not hasattr(bpy.types, cls.__name__):
            bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()

