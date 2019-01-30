from PIL import Image
import numpy as np
import os
import logging
import subprocess
from io import BytesIO
from adb.client import Client as AdbClient
import glob
from ImagePicker import ACTION_IMAGE_PICKER, HERO_IMG_PICKER
from parameters import *

client = AdbClient(host="127.0.0.1", port=5037)

device = client.devices()[0]

baseline = {}

def init():
    find_screen_size()


def convert_cord(x,y):
    real_x = int(x / base_x * device_x)
    real_y = int(y / base_y * device_y)
    return real_x, real_y


def tap_screen(x, y):
    """calculate real x, y according to device resolution."""
    real_x, real_y = convert_cord(x, y)
    device.shell('input tap {} {}'.format(real_x, real_y))


def tap_center(top_left, bottom_right):
    tap_screen((top_left[0] + bottom_right[0])/2, (top_left[1] + bottom_right[1])/2)


def tap_by_name(name):
    try:
        cord = tap_cords[name]
    except KeyError as e:
        cord = tap_only_cords[name]

    top_left = cord[:2]
    bottom_right = cord[2:]
    tap_center(top_left, bottom_right)


def swipe(x, y, x1, y1, duration):
    device.shell('input swipe {} {} {} {} {}'.format(x, y, x1, y1, duration))


def find_screen_size():
    global device_x
    global device_y
    img = pull_screenshot(False)
    device_x, device_y = img.size
    logging.info('device size x, y = ({}, {})'.format(device_x, device_y))


def save_crop():
    for key, val in tap_cords.items():
        img = Image.open('img/' + key + '.png')
        img.crop(val).save('img/crop_'+key+'.png')


def pull_screenshot(resize=False, method=0, save_file=False):
    if save_file and os.path.exists(SCREEN_PATH):
        os.remove(SCREEN_PATH)

    if method == 0:
        result = device.screencap()
        img = Image.open(BytesIO(result))

        if save_file:
            with open(SCREEN_PATH, "wb") as fp:
                fp.write(result)
    else:
        os.system('adb shell screencap -p /sdcard/screen.png')
        os.system('adb pull /sdcard/screen.png {}'.format(SCREEN_PATH))
        img = Image.open(SCREEN_PATH)

    if resize and img.size != (base_x, base_y):
        return img.resize((base_x, base_y))
    else:
        return img


def check_action():
    if not baseline:
        for n in ACTIONS:
            baseline[n] = np.array(Image.open('img/crop_' + n + '.png'))

    frame = pull_screenshot()

    crop_frame = {}
    for key, val in tap_cords.items():
        crop_frame[key] = np.sum(baseline[key] - np.array(frame.crop(val))) / baseline[key].size

    min_key = min(crop_frame, key=crop_frame.get)
    if crop_frame[min_key] < threshold:
        logging.debug("ACTION: {}".format(min_key))
        return min_key

    logging.debug("ACTION: no action")

    return None


def check_single_action(name):
    if not baseline:
        for n in ACTIONS:
            baseline[n] = np.array(Image.open('img/crop_' + n + '.png'))

    frame = pull_screenshot()

    res = np.sum(baseline[name] - np.array(frame.crop(tap_cords[name]))) / baseline[name].size

    if res < threshold:
        return True

    return False


def generate_hero_img():
    frame = pull_screenshot(save_file=True)
    y = 180
    h = 138
    x = 10
    w = 120
    row_num = 9
    col_num = 4

    base = 0

    for j in range(col_num):
        for i in range(row_num):
            x_start = x + i * w
            y_start = y + j * h
            y_end = y_start + 100
            x_end = x_start + 100
            frame.crop((x_start, y_start, x_end, y_end)).save("heros1/{}.png".format(j * row_num + i + base))


def generate_hero_name_img():
    frame = pull_screenshot(save_file=True)
    y = 180
    h = 138
    x = 10
    w = 120
    row_num = 9
    col_num = 4

    hero = {}

    if os.path.exists('hero'):
        for i in glob.glob('hero'):
            name = os.path.basename(i)[:-4]
            hero[name] = np.array(Image.open(i))

    for j in range(col_num):
        for i in range(row_num):
            x_start = x + i * w
            y_start = y + j * h
            y_end = y_start + 100
            x_end = x_start + 100
            hero_img = frame.crop((x_start, y_start, x_end, y_end)) #.save("heros1/{}.png".format(j * row_num + i + base))

            name_img = frame.crop((x_start, y_end , x_end, y_end + 25))

            name = HERO_IMG_PICKER.pick(hero_img)
            if name:
                name_img.save('img/name/{}.png'.format(name))


if __name__ == '__main__':
    generate_hero_name_img()
