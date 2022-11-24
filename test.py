import os
from PIL import Image

folderTo = './inputs/'
i = 0

for root, dirs, files in os.walk("./test"):
    for dir in dirs:
        for root, dirs, files in os.walk("./test/" + dir):
            for file in files:
                filename = os.path.splitext(file)[0]
                ext = os.path.splitext(file)[1]
                img = Image.open("./test/" + dir + "/" + file)
                extrema = img.convert("L").getextrema()
                if ext == ".png" and not 'cut' in filename and  extrema != (0, 0) and extrema != (255, 255):
                    i += 1
                    os.rename("./test/" + dir + "/" + file, folderTo + str(i) + ".png")
