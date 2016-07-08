from PIL import Image, ImageDraw
import operator
from collections import defaultdict
import re
import functools

input_path = 'brick-house.png'
output_path = 'output.png'

width_cubes = 10
height_cubes = 20
#Size will basically be the number of rubiks cubes on the height and width (multiplied by 3, for number of tiles)
size = (width_cubes*3,height_cubes*3)


palette = [
    (255, 0,  0),  #red
    (0, 255,  0),  #green
    (0, 0,  255),  #blue
    (255, 128,  0),  #orange
    (255, 255,  0),  #yellow
    (255, 255,  255),  #white
]


while len(palette) < 256:
    palette.append((0, 0, 0))

#PIL needs a flat array, not an array of tuples ß
# Next round: From python 3, Removed reduce(). Use functools.reduce() if you really need it; however, 99 percent of the time an explicit for loop is more readable.
flat_palette = functools.reduce(lambda a, b: a+b, palette)
assert len(flat_palette) == 768

#Declare an image to hold the palette
palette_img = Image.new('P', (1, 1), 0)
palette_img.putpalette(flat_palette)

multiplier = 8#The higher the number the noisier the picture appears
img = Image.open(input_path)

img = img.resize((size[0] * multiplier, size[1] * multiplier), Image.BICUBIC)
img = img.quantize(palette=palette_img) #reduce the palette

img = img.convert('RGB')

out = Image.new('RGB', size)
for x in range(size[0]):
    for y in range(size[1]):
        #sample at get average color in the corresponding square
        histogram = defaultdict(int)
        for x2 in range(x * multiplier, (x + 1) * multiplier):
            for y2 in range(y * multiplier, (y + 1) * multiplier):
                histogram[img.getpixel((x2,y2))] += 1
        color = max(histogram.keys(), key=operator.itemgetter(1))
        out.putpixel((x, y), color)


#pixels are now 10 by 10 (times the orinal *3)
out= out.resize((width_cubes*30,height_cubes*30))
#Maybe put this somewhere easier to do the 10x
size= size*10

out.save(output_path)

img = Image.open(output_path)
draw = ImageDraw.Draw(img)

print (range(size[0]))

for x in range(size[0]):
    if (x%3 ==0):
        #part of the 10x growth for the x's
        draw.line((x*10,0,x*10,size[1]*10), fill=000000, width=3)
    else:
        draw.line((x*10,0,x*10,size[1]*10), fill=000000, width=1)

for y in range(size[1]):
    if (y%3 ==0):
        #part of the 10x growth for the x's
        draw.line((0,y*10,size[0]*10,y*10), fill=000000, width=3)
    else:
        draw.line((0,y*10,size[0]*10,y*10), fill=000000, width=1)

img.show()
img.save('output2.png')
