from PIL import Image, ImageFilter
import requests

class CoverArt:
    def __init__(self, cover):
        self.cover = cover

    def getCover(self):
        self.fetch()
        self.upscaleCover()
    
    def fetch(self):
        url = self.cover
        img_data = requests.get(url).content

        with open('Output/Temp/Media/cover.jpg', 'wb') as handler:
            handler.write(img_data)
    
    def upscaleCover(self):
        img = Image.open('Output/Temp/Media/cover.jpg')
        img = img.resize((900, 1350), Image.LANCZOS)
        img.save('Output/Temp/Media/cover.jpg')
    
    def sharpenCover(self):
        img = Image.open('Output/Temp/Media/cover.jpg')
        img = img.filter(ImageFilter.SHARPEN)
        img.save('Output/Temp/Media/cover.jpg')

    def addWatermark(self):
        img = Image.open('Output/Temp/Media/cover.jpg')
        watermark = Image.open('Resources/watermark.png')
        # Add watermark to image top right
        img.paste(watermark, (img.width - watermark.width, 0), watermark)
        img.save('Output/Temp/Media/cover.jpg')
