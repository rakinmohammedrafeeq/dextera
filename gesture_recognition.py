def fingers_folded(lmList):
    tips = [8, 12, 16, 20]
    joints = [6, 10, 14, 18]
    for tip, joint in zip(tips, joints):
        if lmList[tip][2] < lmList[joint][2]:
            return False
    return True

def fingers_open(lmList):
    tips = [8, 12, 16, 20]
    joints = [6, 10, 14, 18]
    for tip, joint in zip(tips, joints):
        if lmList[tip][2] > lmList[joint][2]:
            return False
    return True


def is_scroll_mode(lmList, threshold = 20):
    index_y = lmList[8][2]
    thumb_y = lmList[4][2]

    return index_y < thumb_y - threshold