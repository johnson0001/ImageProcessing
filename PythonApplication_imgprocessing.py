import numpy as np
import cv2
if __name__ == '__main__':

    #画像の読み込み
    img1 = cv2.imread(r"C:\Users\myiq_\downloads\background_ori.jpg", 1)
    img2 = cv2.imread(r"C:\users\myiq_\downloads\background_add.jpg", 1)

    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

    fgmask = fgbg.apply(img1)
    fgmask = fgbg.apply(img2)


    #表示
    cv2.imshow('frame', fgmask)

    #検出画像
    bg_diff_path = r'C:\Users\myiq_\downloads\diff.jpg'
    cv2.imwrite(bg_diff_path, fgmask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()