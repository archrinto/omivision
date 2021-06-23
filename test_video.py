import cv2
import time
from omni2panorama import gen_panorama_map, remapping

if __name__ == "__main__":
    video = '#bola_top.webm'
    cap = cv2.VideoCapture(video)

    _, img = cap.read()

    height, width, _ = img.shape

    # jika ingin mengatur ukuran gambar
    scale = 0.5
    height = int(height * scale)
    width = int(width * scale)

    center = (height / 2, width / 2)

    pano_map = gen_panorama_map(height=height, width=width, center=center, inner_radius=60)

    while True:
        t0 = time.time()

        ret, img = cap.read()
        if not ret:
            break

        # jika ingin mengatur ukuran gambar
        img = cv2.resize(img, (width, height))

        image_remap = remapping(pano_map, img)

        print("remap: --- %s seconds ---" % (time.time() - t0))

        cv2.imshow('remap', image_remap)
        cv2.imshow('asli', img)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
