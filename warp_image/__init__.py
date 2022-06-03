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


__author__ = "Nako"
__status__ = "production"
__version__ = "0.8"
__date__ = "4 June 2022"

bl_info = {
    "name": "Warp Image",
    "author": "Nako",
    "description": "Warp texture image from src uv to dst uv",
    "location": "",
    "version": (0, 8),
    "blender": (2, 80, 0),
    "doc_url": "https://github.com/s-nako/WarpImageOnBlender",
    "tracker_url": "https://github.com/s-nako/WarpImageOnBlender/issues",
    "category": "UV",
}

from . import properties
from . import operators
from . import ui_panel


def register():
    print("register WARP IMAGE")
    properties.register()
    operators.register()
    ui_panel.register()


def unregister():
    print("unregister WARP IMAGE")
    ui_panel.unregister()
    operators.unregister()
    properties.unregister()


if __name__ == '__main__':
    register()
