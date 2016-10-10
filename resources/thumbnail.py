import imghdr
from PIL import Image
FILE= 'hello_world.png'
size=()
if imghdr.what(FILE) is not None:
    Image.open(FILE) as im:
        im.thumbnail( [ d  ] ).save('thumbnail_'+FILE)


