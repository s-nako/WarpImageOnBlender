import numpy as np
import bpy
import sys
import os


image_file_formats = {
    "BMP": [".bmp"],
    "IRIS": [".sgi", ".rgb", ".bw"],
    "PNG": [".png"],
    "JPEG": [".jpg", ".jpeg"],
    "JPEG2000": [".jp2", ".j2c"],
    "TARGA": [".tga"],
    "TARGA_RAW": [".tga"],
    "CINEON": [".cin"],
    "DPX": [".dpx"],
    "OPEN_EXR": [".exr"],
    # "OPEN_EXR_MULTILAYER":[],
    "HDR": [".hdr"],
    "TIFF": [".tif", ".tiff"],
    # "AVI_JPEG": [],
    # "AVI_RAW": [],
    # "FFMPEG": []
}


class PILImageProcessor():
    def __init__(self):
        pass

    @staticmethod
    def get_img_size(self, image):
        return image.size

    @staticmethod
    def get_pixel(self, image, i, j):
        r, g, b = image.getpixel((i, j))
        return r, g, b, 255

    @staticmethod
    def set_pixel(self, image, i, j, rgba):
        image.putpixel((i, j), rgba)


class BpyImageProcessor():
    def __init__(self):
        pass

    @staticmethod
    def get_img_size(image):
        return image.size

    @staticmethod
    def get_pixel(image, i, j):
        width = image.size[0]
        offset = (i + int(width * j)) * 4
        return tuple(image.pixels[offset:offset+4])

    @staticmethod
    def set_pixel(image, i, j, rgba):
        width = image.size[0]
        offset = (i + int(width * j)) * 4
        for i in range(4):
            image.pixels[offset+i] = rgba[i]


class NumpyImageProcessor():
    def __init__(self):
        pass

    @staticmethod
    def get_img_size(image):
        return image.shape[:2]

    @staticmethod
    def get_pixel(image, i, j):
        return image[j][i]

    @staticmethod
    def set_pixel(image, i, j, rgba):
        image[j][i] = rgba


def get_uvs(obj, layer):
    bpy.ops.object.mode_set(mode='OBJECT')
    uv_dict = {}
    faces = obj.data.polygons
    mesh_uv_loops = obj.data.uv_layers[layer].data
    for face in faces:
        uvs = []
        for idx in face.loop_indices:
            uvs.append((idx, mesh_uv_loops[idx].uv[0], mesh_uv_loops[idx].uv[1]))
        uv_dict[face.index] = uvs
    return uv_dict


def get_pairs(n):
    pairs = [(j, j + 1) for j in range(n - 1)]
    pairs.append((n - 1, 0))
    return pairs


def get_uv_on_edge(src_uv1, src_uv2, dst_uv1, dst_uv2):
    is_inverted_uv = False
    diff_u = dst_uv2[0] - dst_uv1[0]
    diff_v = dst_uv2[1] - dst_uv1[1]

    if diff_u == 0 and diff_v == 0:
        return [(dst_uv1, src_uv1)]

    if abs(diff_u) < abs(diff_v):
        is_inverted_uv = True
        # reverse u v
        dst_uv1 = dst_uv1[::-1]
        dst_uv2 = dst_uv2[::-1]
        src_uv1 = src_uv1[::-1]
        src_uv2 = src_uv2[::-1]
        diff_u, diff_v = diff_v, diff_u
    if diff_u < 0:
        # reverse point1, point2
        diff_u *= -1
        diff_v *= -1
        dst_uv1, dst_uv2 = dst_uv2, dst_uv1
        src_uv1, src_uv2 = src_uv2, src_uv1

    diff = diff_v / diff_u

    src_diff_u = (src_uv2[0] - src_uv1[0]) / diff_u
    src_diff_v = (src_uv2[1] - src_uv1[1]) / diff_u

    line = []
    if is_inverted_uv:
        for i in range(diff_u):
            line.append(((int(dst_uv1[1] + diff * i), dst_uv1[0] + i),
                         (int(src_uv1[1] + src_diff_v * i), int(src_uv1[0] + src_diff_u * i))))
        line.append(((dst_uv2[1], dst_uv2[0]), (src_uv2[1], src_uv2[0])))
    else:
        for i in range(diff_u):
            line.append(((dst_uv1[0] + i, int(dst_uv1[1] + diff * i)),
                         (int(src_uv1[0] + src_diff_u * i), int(src_uv1[1] + src_diff_v * i))))
        line.append(((dst_uv2[0], dst_uv2[1]), (src_uv2[0], src_uv2[1])))

    return line


class Edge:
    def __init__(self, p1, p2, size=None):
        if size:
            self.is_normalized = False
            self.p1 = [int(pos * (size[i]-1)) for i, pos in enumerate(p1)]
            self.p2 = [int(pos * (size[i]-1)) for i, pos in enumerate(p2)]
            if self.p1[0] < self.p2[0] and (self.p2[0] < size[0]-1):
                self.p2[0] += 1
            elif self.p1[0] > self.p2[0] and (self.p1[0] < size[0]-1):
                self.p1[1] += 1
            if self.p1[1] < self.p2[1] and (self.p2[1] < size[1]-1):
                self.p2[1] += 1
            elif self.p1[1] > self.p2[1] and (self.p1[1] < size[1]-1):
                self.p2[1] += 1
        else:
            self.is_normalized = True
            self.p1 = p1
            self.p2 = p2


def uv_remap(dst_uvs, src_uvs, src_texture, dst_texture):
    if len(dst_uvs) != len(src_uvs):
        return
    for i in range(len(dst_uvs)):
        proc = NumpyImageProcessor()
        uv_size = proc.get_img_size(src_texture)
        v_list = [v for _, _, v in dst_uvs[i]]

        max_v = -1
        min_v = 1.1
        for v in v_list:
            if v < 0:
                v = 0
            elif v > 1:
                v = 1
            if max_v < v:
                max_v = v
            if min_v > v:
                min_v = v
        max_v = int(max_v * (uv_size[1] - 1))
        min_v = int(min_v * (uv_size[1] - 1))

        # print("[Warp Image] min_v, max_v", min_v, max_v)
        min_max_list = [[(-1, (0, 0)), (sys.maxsize, (0, 0))] for i in range(max_v + 2)]

        point_pairs = get_pairs(len(src_uvs[i]))

        for p1, p2 in point_pairs:
            src_p1 = src_uvs[i][p1][1:]
            src_p2 = src_uvs[i][p2][1:]
            src_edge = Edge(src_p1, src_p2, size=uv_size)

            dst_p1 = dst_uvs[i][p1][1:]
            dst_p2 = dst_uvs[i][p2][1:]
            dst_edge = Edge(dst_p1, dst_p2, size=uv_size)

            line = get_uv_on_edge(src_edge.p1, src_edge.p2, dst_edge.p1, dst_edge.p2)

            if not line:
                continue
            for dst, src in line:
                dst_u, dst_v = dst
                if not(0 <= dst_v < uv_size[1]):
                    continue
                if dst_u >= min_max_list[dst_v][0][0]:  # max
                    min_max_list[dst_v][0] = (dst_u, src)
                if dst_u <= min_max_list[dst_v][1][0]:  # min
                    min_max_list[dst_v][1] = (dst_u, src)

        for v in range(min_v, max_v+1):
            max_maxuv, min_minuv = min_max_list[v]
            if min_minuv[0] == sys.maxsize and max_maxuv[0] == -1:
                continue
            line = get_uv_on_edge(list(min_minuv[1]),
                                  list(max_maxuv[1]),
                                  [min_minuv[0], v],
                                  [max_maxuv[0], v])

            if not line:
                for u in range(min_minuv[0], max_maxuv[0]):
                    proc.set_pixel(dst_texture, u, v, (0.0, 0.0, 1.0, 1.0))
                continue

            for dst, src in line:
                if not (0 <= src[0] < uv_size[0] and 0 <= src[1] < uv_size[1]):
                    continue
                if not (0 <= dst[0] < uv_size[0] and 0 <= dst[1] < uv_size[1]):
                    continue
                r, g, b, a = proc.get_pixel(src_texture, src[0], src[1])
                proc.set_pixel(dst_texture, dst[0], dst[1], (r, g, b, a))


def set_uv_and_texture(uv_layer, texture):
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.context.object.data.uv_layers[uv_layer].active = True
    for area in bpy.data.screens['UV Editing'].areas:
        if area.type == 'IMAGE_EDITOR':
            area.spaces.active.image = bpy.data.images[texture]


def warp_main(obj_name, src_uv_key, dst_uv_key, src_img, dst_img_name=""):
    if not dst_img_name:
        dst_img_name = "TexWarpDst"
    src_uvs = get_uvs(obj_name, layer=src_uv_key)
    dst_uvs = get_uvs(obj_name, layer=dst_uv_key)

    src_bpy_img = src_img
    width, height = src_bpy_img.size

    src_np_img = np.array(src_bpy_img.pixels[:])
    src_np_img.resize(width, height, 4)
    dst_np_img = np.zeros((width, height, 4))

    # remap
    uv_remap(dst_uvs, src_uvs, src_np_img, dst_np_img)

    dst_np_img = dst_np_img.flatten()
    dst_bpy_img = bpy.data.images.new(dst_img_name, width=width, height=height, alpha=True)
    dst_bpy_img.pixels = dst_np_img
    set_uv_and_texture(dst_uv_key, dst_img_name)


def save_img(image_name, file_path):
    if image_name not in bpy.data.images:
        return
    image = bpy.data.images[image_name]
    image.filepath_raw = file_path
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    for ext_key, ext_list in image_file_formats.items():
        if ext in ext_list:
            image.file_format = ext_key
            break
    image.save()
