import os
# import tesserocr
import cv2
import numpy as np
from tesserocr import PyTessBaseAPI, RIL, PSM
from pdf2image import convert_from_path, convert_from_bytes
from pathlib import Path
from PIL import Image

def draw_box(image, x, y, w, h):
    # Converting PIL image to numpy array
    cv_image = np.array(image)
    image = cv2.rectangle(cv_image, (x, y), (x+w, y+h), (0,0,255))

    # Change back the format
    return Image.fromarray(image)

def save_image(image):
    img_path = Path(Path.cwd(), "app", "output", "img.jpg")

    image.save(img_path)

def convert_to_images(document_path):
    if not Path(document_path).exists():
        print(f"Path {document_path} does not exists")
        return

    images = convert_from_path(document_path)

    # if len(images) > 0:
    #     print(tesserocr.image_to_text(images[0]))
    return images

def component_images(image):
    with PyTessBaseAPI(psm=PSM.AUTO_OSD) as api:
        api.SetImage(image)
        boxes = api.GetComponentImages(RIL.TEXTLINE, True)
        print(f"Found {len(boxes)} textline image components.")

        for i, (im, box, _, _) in enumerate(boxes):
            api.SetRectangle(box["x"], box["y"], box["w"], box["h"])
            ocrResult = api.GetUTF8Text()
            conf = api.MeanTextConf()
            print(u"Box[{0}]: x={x}, y={y}, w={w}, h={h}, confidence: {1}, text: {2}".format(i, conf, ocrResult, **box))

            image = draw_box(image, box["x"], box["y"], box["w"], box["h"])

        save_image(image)

def run():
    # print(tesserocr.tesseract_version())
    # print(tesserocr.get_languages())
    document_path = Path(Path.cwd(), "src", "documents", "doc1.pdf")
    images = convert_to_images(document_path)

    print(f"Converted {len(images)} pages")

    if len(images) > 0:
        component_images(images[0])
    
    
if __name__ == "__main__":
    run()