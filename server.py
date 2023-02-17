from fastapi import FastAPI
from fastapi.responses import FileResponse
from api import initModel, do_run
from pymatting import cutout
import PIL
from crop import crop
from post_process import postprocessImg
from cleaner import cleanImage
import os.path
import base64

app = FastAPI()

@app.get("/")
async def root(s: str):
    if s.find("spritesheet") == -1:
        s = s + " spritesheet"

    cutFileName = None
    isBlack = True

    while isBlack == True:
        res = do_run(s)
        print(res)
        filename = res[0] + "/" + res[1] + "(" + str(res[2]) + ")_0.png"
        b64Output = ""

        img = PIL.Image.open(filename)
        extrema = img.convert("L").getextrema()
        if extrema == (0, 0):
            isBlack = True
        else:
            isBlack = False

            img = postprocessImg(img)
            img = img.convert('RGBA')

            width, height = img.size
            pixels = img.getcolors(width * height)
            most_frequent_pixel = pixels[0]

            for count, colour in pixels:
                if count > most_frequent_pixel[0]:
                    most_frequent_pixel = (count, colour)

            for x in range(width):
                for y in range(height):
                    pixel = img.getpixel((x, y))
                    if abs(pixel[0] - most_frequent_pixel[1][0]) < 10 and abs(pixel[1] - most_frequent_pixel[1][1]) < 10 and abs(pixel[2] - most_frequent_pixel[1][2]) < 10:
                        img.putpixel((x, y), (255, 255, 255, 0))
            
            img = crop(img)   
            img = cleanImage(img)

            #check if the image is mostly empty
            extrema = img.convert("L").getextrema()
            if extrema == (0, 0):
                isBlack = True
            else:
                b64Output = "data:image/png;base64," + base64.b64encode(img.tobytes()).decode("utf-8")
                isBlack = False

            
            #cutout(preCutFileName, "./mask.png", cutFileName)

    if os.path.exists(filename):
        os.path.remove(filename)

    return { "data": b64Output }


if __name__ == "__main__":
    initModel()
    print("model initialized")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777, log_level="debug")