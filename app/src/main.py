import os
# import tesserocr
import cv2
import numpy as np
from tesserocr import PyTessBaseAPI, RIL, PSM, OEM
from pdf2image import convert_from_path, convert_from_bytes
from pathlib import Path
from PIL import Image

def draw_box(image, x, y, w, h):
    # Converting PIL image to numpy array
    cv_image = np.array(image)

    image = cv2.rectangle(cv_image, (x, y), (x+w, y+h), (0,0,255))

    # Change back the format
    return Image.fromarray(image)

def save_image(image, name):
    img_path = Path(Path.cwd(), "app", "output", str(name) + ".jpg")

    image.save(img_path)

# PDF to Image
def convert_to_images(document_path):
    if not Path(document_path).exists():
        print(f"Path {document_path} does not exists")
        return

    images = convert_from_path(document_path)

    # if len(images) > 0:
    #     print(tesserocr.image_to_text(images[0]))
    return images

# image contains only one word
def detect_word(image):
    with PyTessBaseAPI(psm=PSM.AUTO_OSD, oem=OEM.LSTM_ONLY) as api:
        api.SetImage(image)
        detections = api.GetComponentImages(RIL.WORD, True)

        for i, (im, box, _, _) in enumerate(detections):
            text = api.GetUTF8Text()
            return text


def component_images(image):
    with PyTessBaseAPI(psm=PSM.AUTO_OSD, oem=OEM.LSTM_ONLY) as api:
        api.SetImage(image)
        boxes = api.GetComponentImages(RIL.TEXTLINE, True) # Lines
        # boxes = api.GetComponentImages(RIL.PARA, True) # Paragraphs
        print(f"Found {len(boxes)} textline image components.")

        for i, (im, box, _, _) in enumerate(boxes):
            api.SetRectangle(box["x"], box["y"], box["w"], box["h"])
            ocrResult = api.GetUTF8Text()
            conf = api.MeanTextConf()
            # print(u"Box[{0}]: x={x}, y={y}, w={w}, h={h}, confidence: {1}, text: {2}, length: {3}".format(i, conf, ocrResult, len(ocrResult), **box))
            print(f"Box[{i}]: confidence: {conf}, text: {ocrResult}")

            image = draw_box(image, box["x"], box["y"], box["w"], box["h"])

            # Break on the first detection
            if len(ocrResult) > 0:
                print("Detecting word by word")
                words = api.GetWords() # Returns
                for i, w in enumerate(words):
                    word_detected = detect_word(w[0])
                    if word_detected is None:
                        print(f"[{i}] -> No word detected")
                    else:
                        print(f"[{i}] -> {word_detected}", end="")
                    # save_image(w[0], i)
                break

        save_image(image, "img")

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