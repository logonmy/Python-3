from django import forms

from PIL import Image, ImageDraw
from io import BytesIO
from django.core.cache import cache

class ImageForm(forms.Form):
    '''form to validate requested placeholder image.'''
    height = forms.IntegerField(min_value = 0, max_value = 2000)
    width = forms.IntegerField(min_value = 0, max_value = 2000)

    def generate(self, image_format = 'PNG'):
        '''Generate an image of the given type and return as raw bytes.'''
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        key = '{}.{}.{}'.format(width, height, image_format)
        content = cache.get(key)
        if content is None:
            #create a new image here
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            text = '{} X {}'.format(width, height)
            textwidth, textheight = draw.textsize(text)
            if textwidth < width and textheight < height:
                texttop = (height - textheight) // 2
                textleft = (width - textwidth) // 2
                draw.text((textleft, texttop), text, fill = (255, 255, 255))
            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)
            cache.set(key, content, 60 * 60)
        return content



