from PIL import Image
import pytesseract
import os
import cv2

class OpticalCharacterRecognizer:
    def __init__(self, image_path):
        self._image_path = image_path
        self._preprocessing_type = "thresh"

    # load the example image and convert it to grayscale
    def load_image(self):
        image = cv2.imread(self._image_path)
        self.gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # check to see if we should apply thresholding to preprocess the
    # image
    def check_thresholding(self):
        if self._preprocessing_type == "thresh":
            gray = cv2.threshold(self.gray, 0, 255,
                                 cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # make a check to see if median blurring should be done to remove
        # noise
        elif self._preprocessing_type == "blur":
            gray = cv2.medianBlur(self.gray, 3)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    def write_img_to_disk(self):
        self.filename = "{}.png".format(os.getpid())
        cv2.imwrite(self.filename, self.gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    def get_result(self):
        text = pytesseract.image_to_string(Image.open(self.filename))
        os.remove(self.filename)
        return text

