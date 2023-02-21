import io
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from api import initModel, do_run
from pymatting import cutout
import PIL
from crop import crop
from post_process import postprocessImg
from cleaner import cleanImage
import os.path
import os
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
        path = res[0] + "/"
        filename = res[0] + "/" + res[1] + "(" + str(res[2]) + ")_0.png"

        img = PIL.Image.open(filename)
        extrema = img.convert("L").getextrema()
        if extrema == (0, 0) or extrema == (1, 1):
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
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                isBlack = False

            
            #cutout(preCutFileName, "./mask.png", cutFileName)


    if os.path.exists(filename):
        os.remove(filename)
    if os.path.exists(path):
        os.rmdir(path)

    return StreamingResponse(io.BytesIO(img_byte_arr), media_type="image/png")


if __name__ == "__main__":
    initModel()
    print("model initialized")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777, log_level="debug")