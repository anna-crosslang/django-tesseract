import xml.etree.cElementTree as ET
import base64
from PIL import Image
import io
import os
import pytesseract
import os.path
from os import listdir
from os.path import isfile, join

class MatecatIntegrator:

    def translate_to_matecat_format(self, image_path, output_path, uzn_path=None):
        root = ET.Element("xliff", version="1.2")
        file = ET.SubElement(root, "file", {"original": "", "source-language": "en", "target-language": "en",
                                            "datatype": "plaintext"})
        body = ET.SubElement(file, "body")

        if (uzn_path == None):
            trans_unit = ET.SubElement(body, "trans-unit", id="0")
            trans_unit.set("xml:space", "preserve")

            with open(image_path, "rb") as img_file:
                image_base64 = base64.b64encode(img_file.read())

            ET.SubElement(trans_unit, "source").text = image_base64.decode('ascii')

            ocrred_text = pytesseract.image_to_string(image_path)
            ET.SubElement(trans_unit, "target").text = ocrred_text

        else:
            image_object = Image.open(image_path)
            with open(uzn_path) as uzn_file:
                for i, uzn_line in enumerate(uzn_file):

                    trans_unit = ET.SubElement(body, "trans-unit", id=str(i))
                    trans_unit.set("xml:space", "preserve")

                    uzn_data = uzn_line.split(" ")
                    horizontal_start = int(uzn_data[0])
                    vertical_start = int(uzn_data[1])
                    width = int(uzn_data[2])
                    height = int(uzn_data[3])
                    horizontal_end = horizontal_start + width
                    vertical_end = vertical_start + height

                    cropped_image = image_object.crop((horizontal_start, vertical_start, horizontal_end, vertical_end))
                    b = io.BytesIO()
                    cropped_image.save(b, 'jpeg')
                    bytes = b.getvalue()
                    cropped_image_base64 = base64.b64encode(bytes)

                    ET.SubElement(trans_unit, "source").text = cropped_image_base64.decode('ascii')

                    ocrred_text = pytesseract.image_to_string(cropped_image)

                    ET.SubElement(trans_unit, "target").text = ocrred_text

        tree = ET.ElementTree(root)
        tree.write(output_path)

    def cut_up_image(self, image_path):
        horizontal_start = 10
        width = 200
        vertical_start = 10
        height = 400
        image_object = Image.open(image_path)
        cropped_image = image_object.crop((horizontal_start, vertical_start, width, height))
        b = io.BytesIO()
        cropped_image.save(b, 'jpeg')
        bytes = b.getvalue()
        cropped_image_base64 = base64.b64encode(bytes)
        print(cropped_image_base64)

    def show_img_from_base64(self):
        base64_image_data = b'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N5bHO7HGfpQBcoPSikPSgDzX4q6fr94NNfSrdXssmO6mhthNdQBiPnizyMDPQjtXXG907w5otlE8bIHCxQ26R4klfGSAvdupI68E81g/ER7i8tYdKj1uDSrSdGlvJjv84wrjcEwCOh7/AIVtG2s76bTVNq11HZQi5tL52HliQAoOhznBJ6dCaAN7qp4yD1rnNa1TxDHfm20LRobsRAedLd3BgU56bCAd2Oc+nFYcFx9i8RwX2s+I7a5lQbpLUZ8u1L/KPJKr8w3cHfnGOxqi+gTXeq3SQa3ZQFHdjEkzkRB2yApbg7hyeTggAYGaAPUKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiikPIoA83+KXhvUfEepeFRpyRO1pf8Anyq8qo2wFSSASM8A9K9HWuf8QeHk1vVdGllikKWcry+dFdNE0ZxxwPvAkAH2zXQBfmBxQA6kPSlpD0oA8/8AiJeXMV9pVu7RppbMZJpI4mlukcEbTEq/MCPm+faQOMipbKSxWW48NaUureVJted2zElrGVBLRsw5ycZUE8sab8RtV1fRV0u60q1izLcLbPdrCJp4w5+6iEfNnHTPYV0jas4068drC9mktkCsht8GclR91c8jnBPbBoA4SaPwHbvdLbfbYILUqFitIGMbljhjFhTv3LhW2k/L6dazd3gpjifwsklopPlwOyskGeR5a4yCwyWH8JAB5Nbc114tgnjA0S3tWtwohjtrcTJCCcfI+B9/7rAAbV+bvipYW8Vi+lKeEtIeVQf3ckojji3HJ2S7CXLEZbgYIFAHo9FFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFIelLRQBxnxC8BxeN9HESTNbX8B3204YgBvQgdvfGRWNb/DbUrfToU/tXdeWFuLexlMj45YM7yep5dRx0x3r0yigDzC4+GmrwSahDpOuyQWc7B7VZHLNbFjibGc5ynAznB5qw/wqhuI2sptRuksYPL+yGOdxIp2nzdxyM7mw3JOMdq9HooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAJwM1RudZ0uzmMN1qVnBKBkpLOqsPwJq6elfLPxnsTqPxZvYRPBDttYW3TPtHCjj680AfU2QaWuaF7c/8ACyvsPnv9l/sjzvKz8u/zsbvriuloAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAEb7pr548dCVvjfqYgSykb+zo8i8PyfwdOOv9M19EHpXzD+0DBZQeNbe4tjcC8mgxcblITAAC7T34zmgD6IGjD/AISv+3PNOfsX2Pysdt+/dmtaiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAQ9DXzT+0QsS+KrBkS781oWDtLkxHG3Hl5yPrjvivpZhkV8z/tEG5/4Sqw837T9nEJ8nzFUR9t2zHPXGc+1AH0zRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAIehzXzR+0VJE3irT0Wa6aRYCXjkUiNM4xsOMHPfHtX0u3Svmj9olYV8UWDIl2JWhO9pcmI9MeXnj6474oA+mKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigBD0r5Z+Pxgf4hlI5LhphAhkRyPLXgY2c9+/FFFAH/2Q=='
        decoded = base64.decodebytes(base64_image_data)
        #image = Image.frombytes('RGBA', (200,400), decoded, 'raw')
        image = Image.open(io.BytesIO(decoded))
        image.show()

    def translate_dir_to_matecat_format(self, input_dir, output_dir):
        onlyfiles = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
        for file in onlyfiles:
            extension = os.path.splitext(file)[1]
            if (extension == ".jpg"):
                output_file = output_dir + "/" + os.path.splitext(file)[0] + ".xliff"
                uzn_file = None
                hypothetic_uzn_file = input_dir + "/" + os.path.splitext(file)[0] + ".uzn"
                if os.path.isfile(hypothetic_uzn_file):
                    uzn_file = hypothetic_uzn_file
                self.translate_to_matecat_format(input_dir + "/" + file, output_file, uzn_file)

if __name__ == "__main__":
    integrator = MatecatIntegrator()
    integrator.translate_dir_to_matecat_format("/Users/annabardadym/Desktop/xliff-script-demo", "/Users/annabardadym/Desktop/xliff-script-demo")

