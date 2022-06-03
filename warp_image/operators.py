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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.types import Operator
from . import warp_image_main


class NK_WARP_IMAGE_PT_warp(Operator):
    bl_idname = 'texture_warp.warp_main'
    bl_label = "Warp"
    bl_options = {'REGISTER'}

    def execute(self, context):
        obj = bpy.context.active_object
        if not obj:
            return {'FINISHED'}
        src_uv = bpy.context.scene.tex_warp_props.src_uv
        dst_uv = bpy.context.scene.tex_warp_props.dst_uv
        src_img = bpy.context.scene.tex_warp_props.src_image
        dst_image_name = bpy.context.scene.tex_warp_props.dst_image_name
        if src_uv and dst_uv and src_img:
            warp_image_main.warp_main(obj, src_uv, dst_uv, src_img, dst_image_name)
        return {'FINISHED'}


class NK_WARP_IMAGE_PT_save(Operator):
    bl_idname = 'texture_warp.save_img'
    bl_label = "Save"
    bl_options = {'REGISTER'}

    def execute(self, context):
        dst_image_name = bpy.context.scene.tex_warp_props.dst_image_name
        save_image_path = bpy.context.scene.tex_warp_props.save_image_path

        warp_image_main.save_img(dst_image_name, save_image_path)
        return {'FINISHED'}


classes = [
    NK_WARP_IMAGE_PT_warp,
    NK_WARP_IMAGE_PT_save
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()
