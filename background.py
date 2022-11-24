from pymatting import cutout
import os
import time

outFolder = './results/'

for root, dirs, files in os.walk("./inputs"):
    print("file length:", len(files))
    start_time = time.time()
    for file in files:
        filename = './inputs/' + file
        
        cutout(
            filename,
            "./test.png",
            outFolder + file.split('.')[0] + "cutout.png",
        )
    print("time ran:", time.time() - start_time)