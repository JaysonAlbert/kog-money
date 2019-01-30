import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.feature import match_template
import glob
from util import pull_screenshot, SCREEN_PATH, swipe, tap_center, hero_anchor, tap_by_name
import time
from pypinyin import pinyin
import logging
from PIL import Image


OPENCV = 0
SKIMAGE = 1

lib = OPENCV


def get_hero_img(name):
    return 'img/name/{}.png'.format(name)


def match_template1(template, img, plot=False, method=cv2.TM_SQDIFF_NORMED):
    img = cv2.imread(img, 0).copy()
    template = cv2.imread(template, 0)
    w, h = template.shape[::-1]
    if lib == OPENCV:
        res = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
    else:
        result = match_template(img, template)
        ij = np.unravel_index(np.argmax(result), result.shape)
        top_left = ij[::-1]

    bottom_right = (top_left[0] + w, top_left[1] + h)

    if plot:
        cv2.rectangle(img, top_left, bottom_right, 255, 5)
        plt.subplot(121)
        plt.imshow(img)
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.subplot(122)
        plt.imshow(template)

        plt.show()

    return top_left, bottom_right


method = 'cv2.TM_SQDIFF'
template = 'img/crop_start.png'
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']


def test():
    # for method in methods:
    # for template in glob.glob('img/crop*'):
    #     print(template)
    #     match_template1(template, 'screen.png', plot=True, method=eval(method))
    match_template1('img/hero/bailixuance.png','screen.png',plot=True, method=eval(method))
    for template in glob.glob('img/hero/*'):
        match_template1(template,'hero1.png',plot=True, method=eval(method))


def valid_hero(name, img, top_left, bottom_right, threshold=10):

    hero_img = np.array(Image.open(get_hero_img(name)))
    crop_img = np.array(img.crop((*top_left, *bottom_right)))

    err = np.sum(hero_img - crop_img) / hero_img.size

    if err < threshold:
        return True
    return False


def swipe_hero(reverse=False):
    if reverse:
        swipe(65, 200, 65, 600, 1500)
    else:
        swipe(65, 600, 65, 200, 1500)


def chose_hero(name, reverse=False):
    template = get_hero_img(name)

    logging.debug('ACTION: expand_hero')
    tap_by_name('expand_hero')

    now = time.time()
    while True:
        img = pull_screenshot(save_file=True)
        top_left, bottom_right = match_template1(template, SCREEN_PATH, plot=True)
        valid = valid_hero(name, img, top_left, bottom_right)
        if valid :
            break

        if time.time() - now > 40:
            return False
        swipe_hero(reverse=reverse)

    pull_screenshot(save_file=True)
    top_left, bottom_right = match_template1(template, SCREEN_PATH)
    tap_center(top_left, bottom_right)
    return True


def to_pinyin(name):
    n = [x for a in pinyin(name, 0) for x in a]
    return ''.join(n)

if __name__ == '__main__':
    chose_hero('老夫子')