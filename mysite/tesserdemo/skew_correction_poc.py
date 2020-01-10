import numpy as np
import argparse
import cv2

class ImageSkewHandler:

    def __init__(self, image):
        self.image = cv2.imread(image);

    def determine_skew_angle(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # flip forground and background
        gray = cv2.bitwise_not(gray)
        # threshold the image, setting all foreground pixels to
        # 255 and all background pixels to 0
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # grab the (x, y) coordinates of all pixel values that
        # are greater than zero, then use these coordinates to
        # compute a rotated bounding box that contains all
        # coordinates
        coords = np.column_stack(np.where(thresh > 0))
        self.angle = cv2.minAreaRect(coords)[-1]

        # the `cv2.minAreaRect` function returns values in the
        # range [-90, 0); as the rectangle rotates clockwise the
        # returned angle trends to 0 -- in this special case we
        # need to add 90 degrees to the angle
        if self.angle < -45:
            self.angle = -(90 + self.angle)

        # otherwise, just take the inverse of the angle to make
        # it positive
        else:
            self.angle = -self.angle

    def deskew(self):
        # rotate the image to deskew it
        (h, w) = self.image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, self.angle, 1.0)
        self.deskewed = cv2.warpAffine(self.image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    def demonstrate_result(self):
        # draw the correction angle on the image so we can validate it
        cv2.putText(self.deskewed, "Angle: {:.2f} degrees".format(self.angle),
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the output image
        print("[INFO] angle: {:.3f}".format(self.angle))
        cv2.imshow("Input", self.image)
        cv2.imshow("Rotated", self.deskewed)
        cv2.waitKey(0)

if __name__ == "__main__":
    skew_handler = ImageSkewHandler("/Users/annabardadym/Desktop/skew_poc_test_files/1.png")
    skew_handler.determine_skew_angle()
    skew_handler.deskew()
    skew_handler.demonstrate_result()