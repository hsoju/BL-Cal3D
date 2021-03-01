import bpy
from ..body_part import BodyPart


class FemaleThighs(bpy.types.Operator):
    """Add imvu mesh primitive female thighs to scene"""
    part = BodyPart("female", "thighs")
    bl_idname = part.bl_idname
    bl_label = part.bl_label
    bl_options = part.bl_options

    def execute(self, context):
        """Specifies the behaviour for the operator method called by Blender.

        Args:
            context (): A bpy context containing data in the current 3d view.

        Returns:

        """
        return self.part.execute(context)
