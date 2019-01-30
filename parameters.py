SCREEN_PATH = 'screen.png'

hero_anchor = (10, 120, 9, 5)

tap_cords = {
    'restart': (1000, 635, 1170, 690),
    'continue': (560, 630, 720, 657),
    'start': (880,  555, 1035, 611),
    'skip0': (1190, 12, 1260, 45),
    'skip1': (1190, 12, 1260, 45),
    'exit': (1153, 43, 1264, 93,),
    'start_match': (630, 574, 822, 630),
    'return_room': (661, 638, 812, 684),
    'confirm': (572, 168, 709, 198),
    'match_continue': (542, 635, 739, 690),
    'recover': (710, 619, 757, 671),
    'pick_hero': (1104, 655, 1267, 712),
    'check_finished': (435, 442, 557, 462),
    'confirm_hero': (1103, 658, 1266, 713),
}

tap_only_cords = {
    'add_skill0': (860, 540, 900, 580),
    'add_skill1': (940, 409, 980, 449),
    'add_skill2': (1067, 331, 1107, 371),
    'buy_item': (1205, 95, 1255, 137),
    'expand_hero': (249, 334,268,397)
}


# x, y, width, dura_start, dura_end - dura_start, 从点 x,y 随机方向滑动width，持续时间随机
swipe_cords = {
    'random_walk': (220, 570, 130, 3000, 8000),
    'skill0':(943, 586, 85, 100, 400),
    'skill1':(1030, 500, 85, 100, 400),
    'skill2':(1121, 397, 85, 100, 400),
}

threshold = 10
ACTIONS = tap_cords.keys()

# 屏幕分辨率
device_x, device_y = 1280, 720
base_x, base_y = 1280, 720
