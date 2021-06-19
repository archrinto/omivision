# PROGRAM OMNIDIRECTIONAL CAMERA KE PANORAMA

################################
# Author: Archrinto
# Email : hey.archrinto@gmail.com
################################

import numpy as np
import cv2
from math import ceil
import time

def gen_panorama_map(height, width, center, inner_radius=None, outer_radius=None):
    if inner_radius == None:
        inner_radius = 0
    
    if outer_radius == None:
        outer_radius = height / 2.0
    
    center_radius = (outer_radius - inner_radius) / 2 + inner_radius

    # lebar: keliling lingkaran
    # lebar 0-w merepresentasikan sudut
    w = ceil(np.pi * center_radius * 2)

    # tinggi: jari-jari lingkaran
    # tinggi 0-h merepresentasikan jarak
    h = ceil(outer_radius - inner_radius) 

    # membuat mapping
    # 0-360 ke 0-w
    range_sudut = []
    for i in range(w):
        sudut_i = float(i) / float(w-1) * 360.0
        range_sudut.append(sudut_i)
    
    # sudut ke semua range jarak
    range_jarak = []
    for i in range(h):
        # piksel paling bawah merupakan jarak terdekat
        jarak = outer_radius - i
        range_jarak.append(jarak)
    
    # memasukan dalam matrix sudut dan jarak
    map_sudut = np.zeros((h, w))
    for i in range(h):
        map_sudut[i,:] = range_sudut
    
    map_jarak = np.zeros((h, w))
    for i in range(w):
        map_jarak[:,i] = range_jarak
    
    # konversi sudut dan jarak ke dalam koordinat piksel gambar
    map_x = ((np.sin(np.radians(map_sudut)) * map_jarak) + center[0]).astype(int)
    map_y = ((np.cos(np.radians(map_sudut)) * map_jarak) + center[1]).astype(int)

    # mengambil index matrix yang valid
    map_valid = np.logical_and(
        np.logical_and(map_x < height, map_x >= 0),
        np.logical_and(map_y < width, map_y >= 0)
    )
    
    map_size = (h, w)

    return map_size, map_x, map_y, map_valid

def remapping(map, image):
    map_size, map_x, map_y, map_valid = map

    remap = np.zeros((map_size[0], map_size[1], image.shape[2]), np.uint8)
    remap[map_valid] = image[map_x[map_valid], map_y[map_valid]]

    return remap

if __name__ == "__main__":
    img = cv2.imread('omni.jpeg')
    height, width, _ = img.shape
    center = (height / 2, width / 2)
    
    t0 = time.time()
    pano_map = gen_panorama_map(height=height, width=width, center=center, inner_radius=60)
    # menghitung lama proses pembuatan peta
    print("gen map: --- %s seconds ---" % (time.time() - t0))

    t0 = time.time()

    image_remap = remapping(pano_map, img)
    
    # menghitung lama proses remap
    print("remap: --- %s seconds ---" % (time.time() - t0))

    # menyimpan gambar
    cv2.imwrite('mapping-v1.3.jpeg', image_remap)
    
    # # menampilkan gambar
    # cv2.imshow('remapping', res)
    # cv2.waitKey(0)



