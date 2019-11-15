import os
import cv2
import glob

#グレースケール関数
def gray_scale(path):
    img = cv2.imread(path, 1) #カラー画像の読み込み
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #グレースケール変換
    return gray

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

        img = bg_subtra(background_img, i) #背景差分関数を実行
        cv2.imwrite(out_path, img) #処理後の画像を保存

    return

#ファイルを探してリサイズする関数を実行
bundle('C:\\sample_img_bgsub', 'C:\\sample_bgsubimg_bgsub', 'C:\\sample_img_bgsub\\background.bmp')