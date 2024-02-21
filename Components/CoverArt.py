from PIL import Image, ImageFilter
import requests
import os

class CoverArt:
    def __init__(self, cover, config):
        self.cover = cover
        self.config = config
        self.path = os.path.join(self.config.media, 'cover.jpg')

    def getCover(self):
        self.fetch()
        self.upscaleCover()

    def fetch(self):
        url = self.cover
        img_data = requests.get(url).content

        with open(self.path, 'wb') as handler:
            handler.write(img_data)

    def upscaleCover(self):
        img = Image.open(self.path)
        img = img.resize((900, 1350), Image.LANCZOS)
        img.save(self.path)

    def sharpenCover(self):
        img = Image.open(self.path)
        img = img.filter(ImageFilter.SHARPEN)
        img.save(self.path)

    def addWatermark(self):
        img = Image.open(self.path)
        watermark = Image.open('Resources/watermark.png')
        # Add watermark to image top right
        img.paste(watermark, (img.width - watermark.width, 0), watermark)
        img.save(self.path)
