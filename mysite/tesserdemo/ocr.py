from PIL import Image
import pytesseract
import os
import cv2
import numpy as np
import yaml

class OpticalCharacterRecognizer:
    def __init__(self, image_path, config_path = None):
        self._image_path = image_path
        self._config_path = config_path

    def perform_ocr(self):
        self.load_image()
        self.load_config()
        self.optimize_image()
        self.write_img_to_disk()
        return self.get_result()

    def load_image(self):
        self._image = cv2.imread(self._image_path)

    def load_config(self):
        if self._config_path:
            self._config = yaml.safe_load(open(self._config_path))

    def optimize_image(self):
        if hasattr(self, "_image") and hasattr(self, "_config") and hasattr(self._config, "__len__"):
            if "resize" in self._config:
                dsize = None
                if "dsize" in self._config["resize"]:
                    dsize = self._config["resize"]["dsize"]
                fx = None
                if "fx" in self._config["resize"]:
                    fx = self._config["resize"]["fx"]
                fy = None
                if "fy" in self._config["resize"]:
                    fy = self._config["resize"]["fy"]
                if "interpolation" in self._config["resize"]:
                    interpolation = getattr(cv2, self._config["resize"]["interpolation"])
                    self._image = cv2.resize(self._image, dsize, fx=fx, fy=fy, interpolation=interpolation)
                else:
                    self._image = cv2.resize(self._image, dsize, fx=fx, fy=fy)
            if "gray" in self._config:
                self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
            if "dilate" in self._config:
                dilation_kernel_shape = None
                if "kernel" in self._config["dilate"]:
                    if "shape" in self._config["dilate"]["kernel"]:
                        dilation_kernel_shape = tuple(self._config["dilate"]["kernel"]["shape"])
                dilation_kernel = np.ones(dilation_kernel_shape, np.uint8)
                dilation_iterations = 1
                if "iterations" in self._config["dilate"]:
                    dilation_iterations = self._config["dilate"]["iterations"]
                self._image = cv2.dilate(self._image, dilation_kernel, iterations=dilation_iterations)
            if "erode" in self._config:
                erosion_kernel_shape = None
                if "kernel" in self._config["erode"]:
                    if "shape" in self._config["erode"]["kernel"]:
                        erosion_kernel_shape = tuple(self._config["erode"]["kernel"]["shape"])
                erosion_kernel = np.ones(erosion_kernel_shape, np.uint8)
                erosion_iterations = 1
                if "iterations" in self._config["erode"]:
                    erosion_iterations = self._config["erode"]["iterations"]
                self._image = cv2.erode(self._image, erosion_kernel, iterations=erosion_iterations)
            if "blur" in self._config:
                blur_kernel_shape = None
                if "kernel" in self._config["blur"]:
                    if "shape" in self._config["blur"]["kernel"]:
                        blur_kernel_shape = tuple(self._config["blur"]["kernel"]["shape"])
                self._image = cv2.blur(self._image, blur_kernel_shape)
            if "gaussian_blur" in self._config:
                gaussian_blur_kernel_shape = None
                if "kernel" in self._config["gaussian_blur"]:
                    if "shape" in self._config["gaussian_blur"]["kernel"]:
                        gaussian_blur_kernel_shape = tuple(self._config["gaussian_blur"]["kernel"]["shape"])
                gaussian_blur_sigma_x = 0
                if "sigma_x" in self._config["gaussian_blur"]:
                    gaussian_blur_sigma_x = self._config["gaussian_blur"]["sigma_x"]
                self._image = cv2.GaussianBlur(self._image, gaussian_blur_kernel_shape, gaussian_blur_sigma_x)
            if "median_blur" in self._config:
                median_blur_kernel_shape = None
                if "kernel" in self._config["median_blur"]:
                    if "shape" in self._config["median_blur"]["kernel"]:
                        median_blur_kernel_shape = self._config["median_blur"]["kernel"]["shape"]
                self._image = cv2.medianBlur(self._image, median_blur_kernel_shape)
            if "bilateral_filter" in self._config:
                d = 0
                if "d" in self._config["bilateral_filter"]:
                    d = self._config["bilateral_filter"]["d"]
                sigma_color = 0
                if "sigma_color" in self._config["bilateral_filter"]:
                    sigma_color = self._config["bilateral_filter"]["sigma_color"]
                sigma_space = 0
                if "sigma_space" in self._config["bilateral_filter"]:
                    sigma_space = self._config["bilateral_filter"]["sigma_space"]
                self._image = cv2.bilateralFilter(self._image, d, sigma_color, sigma_space)
            if "threshold" in self._config:
                lower = 0
                if "lower" in self._config["threshold"]:
                    lower = self._config["threshold"]["lower"]
                upper = 255
                if "upper" in self._config["threshold"]:
                    upper = self._config["threshold"]["upper"]
                threshold_type = "THRESH_BINARY"
                if "type" in self._config["threshold"]:
                    threshold_type = self._config["threshold"]["type"]
                type_enum_value = getattr(cv2, threshold_type)
                if "otsu" in self._config["threshold"] and self._config["threshold"]["otsu"] == True:
                    type_enum_value = type_enum_value + cv2.THRESH_OTSU
                self._image = cv2.threshold(self._image, lower, upper, type_enum_value)[1]
            if "adaptive_threshold" in self._config:
                max_value = 255
                if "max_value" in self._config["adaptive_threshold"]:
                    max_value = self._config["adaptive_threshold"]["max_value"]
                adaptive_method = "ADAPTIVE_THRESH_GAUSSIAN_C"
                if "adaptive_method" in self._config["adaptive_threshold"]:
                    adaptive_method = self._config["adaptive_threshold"]["adaptive_method"]
                adaptive_method_enum_value = getattr(cv2, adaptive_method)
                adaptive_threshold_type = "THRESH_BINARY"
                if "threshold_type" in self._config["adaptive_threshold"]:
                    adaptive_threshold_type = self._config["adaptive_threshold"]["threshold_type"]
                threshold_type_enum_value = getattr(cv2, adaptive_threshold_type)
                block_size = 3
                if "block_size" in self._config["adaptive_threshold"]:
                    block_size = self._config["adaptive_threshold"]["block_size"]
                c = 0
                if "c" in self._config["adaptive_threshold"]:
                    c = self._config["adaptive_threshold"]["c"]
                self._image = cv2.adaptiveThreshold(self._image, max_value, adaptive_method_enum_value, threshold_type_enum_value, block_size, c)

    # write the image to disk as a temporary file so we can
    # apply OCR to it
    def write_img_to_disk(self):
        self.filename = "{}.png".format(os.getpid())
        cv2.imwrite(self.filename, self._image)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    def get_result(self):
        text=""
        if hasattr(self, "_config") and hasattr(self._config, "__len__") and ("language" in self._config):
            tessdata_path = os.path.abspath('./tessdata')
            os.environ['TESSDATA_PREFIX'] = tessdata_path
            tessdata_dir_config = r'--tessdata-dir "' + tessdata_path + '"'
            #text = pytesseract.image_to_string(Image.open(self.filename), lang=self._config["language"], config=tessdata_dir_config)
            text = pytesseract.image_to_string(Image.open(self.filename), lang=self._config["language"], config=tessdata_dir_config)
        else:
            #text = pytesseract.image_to_string(Image.open(self.filename))
            text = pytesseract.image_to_string(Image.open(self.filename))
        os.remove(self.filename)
        return text

