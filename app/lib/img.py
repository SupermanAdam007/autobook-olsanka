import io
import logging

from colormap import rgb2hex

from PIL import Image


class MyImage:

    def __init__(self, png_bytes):
        self.image = MyImage.crop_to_remove_borders(Image.open(io.BytesIO(png_bytes)))

    @staticmethod
    def crop_to_remove_borders(original):
        width, height = original.size  # Get dimensions
        left = width / 4
        top = height / 4
        right = 3 * width / 4
        bottom = 3 * height / 4
        return original.crop((left, top, right, bottom))

    def get_average_colour(self, return_hex=True):
        img1 = self.image.resize((1, 1), Image.ANTIALIAS).convert('RGB')
        r, g, b = img1.getpixel((0, 0))
        # logging.info(f'r: {r}, g: {g}, b: {b}')

        if return_hex:
            return rgb2hex(r, g, b)
        else:
            return r, g, b
