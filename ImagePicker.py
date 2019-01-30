import glob
import os
import numpy as np
from PIL import Image
from parameters import tap_cords
import logging


class ImagePicker(object):

    def __init__(self, pathname, threshold=10, crop=None):
        self.imgs = glob.glob(pathname)
        self.threshold = threshold
        self.crop = crop

        self.baseline = {}
        for i in self.imgs:
            name = os.path.basename(i)[:-4]
            self.baseline[name] = np.array(Image.open(i))

    def pick(self,img):
        error = {}

        for key, val in self.baseline.items():
            if self.crop:
                crop_img = np.array(img.crop(self.crop[key]))
            else:
                crop_img = np.array(img)
            error[key] = np.sum(val - crop_img) / val.size

        min_key = min(error, key=error.get)

        logging.debug("ImagePicker: error of {}:{}".format(min_key, error[min_key]))
        if error[min_key] < self.threshold:
            return min_key

        return None


ACTION_IMAGE_PICKER = ImagePicker('img/crop*', threshold=10, crop=tap_cords)

HERO_IMG_PICKER = ImagePicker('img/hero/*', threshold=255)