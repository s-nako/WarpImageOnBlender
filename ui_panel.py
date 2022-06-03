# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.types import Panel


class TEXTURE_WARP_PT_main_panel(Panel):
    bl_label = "Texture Warp"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Texture Warp'

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Texture Warp")

        box = layout.box()
        row = box.column(align=True)

        props = bpy.context.scene.tex_warp_props
        mesh = bpy.context.object.data

        row.prop_search(props, "src_uv", mesh, "uv_layers", text="Src UV")
        row.prop_search(props, "dst_uv", mesh, "uv_layers", text="Dst UV")
        row.prop_search(props, "src_image", bpy.data, "images", text="Src Image")
        row.prop(props, "dst_image_name", text="Dst Image Name")

        row.operator("texture_warp.warp_main", text="Warp")
        row.prop(props, "save_image_path", text="Save Path")
        row.operator("texture_warp.save_img", text="Save")


def register():
    bpy.utils.register_class(TEXTURE_WARP_PT_main_panel)


def unregister():
    bpy.utils.unregister_class(TEXTURE_WARP_PT_main_panel)


if __name__ == '__main__':
    register()
