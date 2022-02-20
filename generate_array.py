import ezdxf
from ezdxf.addons import Importer
import numpy as np
from pathlib import Path

N_PIXEL = 415
PIXEL_PIXEL_DISTANCE = 4200.0 # microns
NUMBER_PER_ROW = [5, 9, 12, 15, 16, 18, 19, 20, 21, 21, 21, 21, 21, 21, 21, 20, 21, 20, 19, 18, 17, 13, 12, 8, 6]
NUMBER_OF_ROWS = len(NUMBER_PER_ROW)
FIRST_ELEMENT_X_HEX = [4, 1, -1, -3, -4, -5, -6, -7, -8, -8, -9, -9, -10, -10, -11, -11, -12, -12, -12, -12, -12, -11, -11, -8, -8]
FIRST_ELEMENT_Y_HEX = [-12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# nearest 3 disposition
PIXEL_ORDER = [406, 400, 394, 388, 382, 378, 372, 366, 360, 354, 348, 342, 336, 330, 335, 329, 324, 318, 312, 306,
               300, 294, 288, 282, 276, 409, 412, 341, 275, 222, 228, 234, 240, 246, 252, 258, 264, 270, 223, 325, 413, 381, 347,
               281, 269, 175, 181, 187, 193, 199, 205, 211, 217, 170, 229, 319, 373, 387, 353, 287, 263, 216, 169,
               128, 134, 140, 146, 152, 158, 164, 176, 235, 313, 367, 401, 393, 359, 293, 257, 210, 163,  93,  99,
               105, 111, 117, 123,  94, 129, 182, 241, 307, 361, 395, 399, 365, 299, 251, 204, 157, 122,  64,  70,
                76,  82,  88,  65, 100, 135, 188, 247, 301, 355, 389, 405, 371, 305, 245, 198, 151, 116,  87,  41,
                47,  53,  59,  42,  71, 106, 141, 194, 253, 295, 349, 383, 377, 311, 239, 192, 145, 110,  81,  58,
                11,  35,  30,  13,  48,  77, 112, 147, 200, 259, 289, 343, 411, 415, 317, 233, 186, 139, 104,  75,  52,  29,
                16,  20,   3,  36,  54,  83, 118, 153, 206, 265, 283, 337, 323, 227, 180, 133,  98,  69,  46,  34,
                23,   6,  10,  25,  31,  60,  89, 124, 159, 212, 271, 277, 331, 328, 221, 174, 168,  92,  63,  40,
                 9,  18,  12,   1,  14,  17,   7,  43,  66,  95, 165, 171, 218, 326, 274, 268, 215, 162, 127,
                86,  57,  28,  21,   4,   8,  22,  37,  49,  72, 101, 130, 177, 224, 320, 374, 340, 280, 262, 209,
               156, 121,  80,  51,  33,  15,  24,  19,  26,  55,  78, 107, 136, 183, 230, 314, 368, 346, 286, 256,
               203, 150, 115,  74,  45,   2,  27,  32,   5,  61,  84, 113, 142, 189, 236, 308, 362, 380, 352, 292,
               250, 197, 144, 109,  68,  39,  56,  50,  44,  38,  90, 119, 148, 195, 242, 302, 356, 407, 386, 358,
               298, 244, 191, 138, 103,  62,  91,  85,  79,  73,  67, 125, 154, 201, 248, 296, 350, 402, 392, 364,
               304, 238, 185, 132,  97, 126, 120, 114, 108, 102,  96, 160, 207, 254, 290, 344, 396, 398, 370, 310,
               232, 179, 167, 161, 155, 149, 143, 137, 131, 166, 213, 260, 284, 338, 390, 404, 376, 316, 226, 173,
               214, 208, 202, 196, 190, 184, 178, 172, 266, 278, 332, 384, 379, 322, 220, 267, 261, 255, 249, 243,
               237, 231, 225, 219, 272, 410, 414, 273, 279, 285, 291, 297, 303, 309, 315, 321, 327, 333, 339, 345, 351, 357,
               363, 369, 375, 385, 391, 397, 403, 408, 334]
# data: index, x, y, rotation
data = []
pixel_index = 0
for row,(npr, fst_x, fst_y) in enumerate(zip(NUMBER_PER_ROW, FIRST_ELEMENT_X_HEX, FIRST_ELEMENT_Y_HEX)):
    x = PIXEL_PIXEL_DISTANCE * (fst_x + 0.5*fst_y)
    y = fst_y * PIXEL_PIXEL_DISTANCE * 0.5*np.sqrt(3.0)
    if(row%2 == 0):
        rotation = 180
    else:
        rotation = 0
    for npr_i in range(npr):
        data.append([PIXEL_ORDER[pixel_index], x, y, rotation])
        x += PIXEL_PIXEL_DISTANCE
        pixel_index += 1
data = np.array(data)
# sort array data wrt the pixel index
data_sorted = data[data[:, 0].argsort()]

array_dxf = ezdxf.new('R2018')

for [i, x, y, r] in data_sorted:
    pixel_dxf = ezdxf.readfile(Path('examples/{:d}/pixels/pixel_{:d}.dxf'.format(N_PIXEL, int(i))))
    for entity in pixel_dxf.modelspace():
        #entity.transform(ezdxf.math.Matrix44.scale(sx=-1, sy=1, sz=1))     # yes! it works!
        entity.transform(ezdxf.math.Matrix44.z_rotate(np.radians(r)))
        entity.transform(ezdxf.math.Matrix44.translate(x, y, 0.0))
    importer = Importer(pixel_dxf, array_dxf)
    importer.import_modelspace()
    importer.finalize()

array_dxf.saveas('array.dxf')