import subprocess
import os
import random
from random import randint
# -------------------------------------------------------------
# CONFIGURABLE SETTINGS
# ---------------------------------------------------------
# path to ffmpeg bin
FFMPEG_PATH = "D:\Glitch\Tools\\ffmpeg-20160326-git-8ff0f6a-win64-static\\ffmpeg-20160326-git-8ff0f6a-win64-static\\bin\\ffmpeg.exe"
# ----------------------------------------------------------------
# encoding script
# --------------------------------------------------------------


def process():
    cwd = os.getcwd()
    print(cwd)
    createFolders()

    filelist = filter(lambda f: f.split('.')[-1] == 'jpg', os.listdir(cwd))
    filelist = sorted(filelist)

    for f in filelist:
        encode(f)
    print("Moving Pngs")
    movePngs()
    print("CleanUp")
    cleanUp()


def createFolders():
    print("Checking Folders")
    if not os.path.exists("jpeg2000"):
        os.makedirs("jpeg2000")
    if not os.path.exists("png"):
        os.makedirs("png")


def movePngs():
    cwd = os.getcwd()
    if not cwd == orig:
        os.chdir("..")
        movePngs()
    else:
        moveTo = cwd + "\\png\\"
        os.chdir("jpeg2000")
        cwd = os.getcwd()
        filelist = filter(lambda f: f.split('.')[-1] == 'png', os.listdir(cwd))
        filelist = sorted(filelist)
        for f in filelist:
            print("moving " + f + " To :" + moveTo)
            os.rename(cwd + "\\" + f, (moveTo + f))


def cleanUp():
    cwd = os.getcwd()
    if not cwd == orig:
        os.chdir("..")
        cleanUp()
    else:
        os.chdir("jpeg2000")
        cwd = os.getcwd()
        filelist = os.listdir(cwd)
        filelist = sorted(filelist)
        for f in filelist:
            os.remove(cwd + "\\" + f)


def encode(file):
    name = ''.join(file.split('.')[:-1])

    try:
        # create a folder called attachments and symlink it to FONT_DIR
        # extract attachments
        # subprocess.call(['mkdir', 'jpeg2000'])

        subprocess.call([FFMPEG_PATH, '-i', file, '-c:v', 'libopenjpeg', "jpeg2000\\" + name + ".jp2"])

        os.chdir('jpeg2000')
        print("Done encoding " + name + " to jpeg2000")
        hexEdit(name + ".jp2")
    except:
        print("error encoding " + name + " to jpeg2000")


def hexEdit(file):
    name = ''.join(file.split('.')[:-1])
    with open(file, "rb") as imageFile:
        f = imageFile.read()
        b = bytearray(f)
        print(b[156])
        random.seed()
        start = randint(0, 14)
        random.seed()
        end = randint(0, (14 - start))
        for x in range(156 + start, (156 + end)):
            random.seed()
            b[x] = randint(0, 255)
        start = randint(0, 14)
        random.seed()
        end = randint(0, (14 - start))
        for x in range(200 + start, (200 + end)):
            random.seed()
            b[x] = randint(0, 255)
        start = randint(0, 14)
        random.seed()
        end = randint(0, (14 - start))
        for x in range(232 + start, (232 + end)):
            random.seed()
            b[x] = randint(0, 255)
        with open(name + 'Hexed.jp2', 'wb') as f:
            f.write(b)
    decode(name + 'Hexed.jp2')


def decode(file):
    name = ''.join(file.split('.')[:-1])
    try:
            # create a folder called attachments and symlink it to FONT_DIR
            # extract attachments
            # subprocess.call(['mkdir', 'jpeg2000'])

        subprocess.call([FFMPEG_PATH, '-i', file, '-c:v', 'png', name + ".png"])
        print("Done encoding " + name + " to PNG")
        os.chdir('..')
    except:
        print("error encoding " + name + " to PNG")


if __name__ == "__main__":
    orig = os.getcwd()
    process()
