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
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, BoolProperty, StringProperty


class WarpImageProps(PropertyGroup):
    src_uv: StringProperty()
    dst_uv: StringProperty()

    src_image: PointerProperty(type=bpy.types.Image)
    dst_image_name: StringProperty()
    save_image_path: StringProperty(subtype="FILE_PATH")


def register():
    bpy.utils.register_class(WarpImageProps)
    bpy.types.Scene.warp_img_props = bpy.props.PointerProperty(type=WarpImageProps)


def unregister():
    del bpy.types.Scene.warp_img_props
    bpy.utils.unregister_class(WarpImageProps)


if __name__ == '__main__':
    register()
