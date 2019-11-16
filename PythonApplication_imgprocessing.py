import os
import cv2
import glob
import numpy as np

#グレースケール関数
def gray_scale(path):
    img = cv2.imread(path, 1) #カラー画像の読み込み
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #グレースケール変換
    return gray

#ガウシアンフィルタ
def gaussian(img):

    kernel1 = np.array([[1/16, 1/8, 1/16],
                        [1/8, 1/4, 1/8],
                        [1/16, 1/8, 1/16]])

    m, n = kernel1.shape #カーネルサイズ
    
    #畳み込み演算をしない領域の幅
    d = int((m-1)/2)
    h, w = img.shape[0], img.shape[1]

    #出力画像の配列
    dst = img.copy()

    for y in range(d, h - d):
        for x in range(d, w - d):
            #畳み込み演算
            dst[y][x] = np.sum(img[y-d:y+d+1, x-d:x+d+1]*kernel1)

    return dst


#背景差分関数
def bg_subtra(background_img, path):
    img1 = cv2.imread(background_img, 1)
    img2 = cv2.imread(path, 1)

    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

    fgmask = fgbg.apply(img1)
    fgmask = fgbg.apply(img2)

    return fgmask


#指定されたディレクトリ内のファイル情報を取得する関数
def bundle(dir, outdir, background_img):
    path_list = glob.glob(dir + '\*') #指定されたディレクトリ内のすべてのファイルを取得
    name_list = [] #ファイル名の空リストを定義
    ext_list = [] #拡張子の空リストを定義

    #ファイルのフルパスからファイル名と拡張子を抽出
    for i in path_list:
        file = os.path.basename(i) #拡張子ありのファイル名を取得
        name, ext = os.path.splitext(file) #拡張子なしのファイル名と拡張子を取得
        name_list.append(name) #拡張子なしのファイル名をリスト化
        ext_list.append(ext) #拡張子をリスト化

        out_path = os.path.join(*[outdir, name + '_fgmask' + ext]) #保存パスを作成

        img1 = gray_scale(i) #グレースケール処理
        img2 = bg_subtra(background_img, img1) #背景差分関数を実行
        cv2.imwrite(out_path, img2) #処理後の画像を保存

    return

#ファイルを探してリサイズする関数を実行
bundle('C:\\sample_img_bgsub', 'C:\\sample_bgsubimg_bgsub', 'C:\\sample_img_bgsub\\background.bmp')