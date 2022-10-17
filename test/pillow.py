""" 
Draws the text <text> on the ImageDraw <image_draw> in the box (specified as a 4-ple of [x,y,width,height])
with the font <font> and the allignments as given. Passes other arguments to the ImageDraw.text function 
(for example, fill is a good one to use here). 

Can be used to center text horizontally and vertically, as well as right-align and bottom-allign (although it defaults to
left- and top-allignment). Nothing is done to prevent overflow, but the y and height values from the box will be used for vertical
allignment

Example usage:

    img = Image.new("RGB", (300,300), (255,255,255))
    img_draw = ImageDraw.Draw(img)
    text_box(
        "this is a text\n that respects linebreaks and will also break on spaces",
        img_draw,
        font("/Library/Fonts/Times New Roman Bold Italic.ttf", 16),
        (20, 20, 260,260),
        ALLIGNMENT_RIGHT,
        ALLIGNMENT_CENTER,
        fill=(255,0,255)
    )
    img.show()
"""

from PIL import Image, ImageDraw, ImageFont

# The various allignments.
# horizontal_allignment can take ALLIGNMENT_LEFT, ALLIGNMENT_CENTER, and ALLIGNMENT_RIGHT
# verical_allignment can take ALLIGNMENT_TOP, ALLIGNMENT_CENTER, and ALLIGNMENT_BOTTOM
ALLIGNMENT_LEFT = 0
ALLIGNMENT_CENTER = 1
ALLIGNMENT_RIGHT = 2
ALLIGNMENT_TOP = 3
ALLIGNMENT_BOTTOM = 4


def text_box(
    text, image_draw, font, box, horizontal_allignment=ALLIGNMENT_LEFT, vertical_allignment=ALLIGNMENT_TOP, **kwargs
):
    x = box[0]
    y = box[1]
    width = box[2]
    height = box[3]
    lines = text.split("\n")
    true_lines = []
    for line in lines:
        if font.getsize(line)[0] <= width:
            true_lines.append(line)
        else:
            current_line = ""
            for word in line.split(" "):
                if font.getsize(current_line + word)[0] <= width:
                    current_line += " " + word
                else:
                    true_lines.append(current_line)
                    current_line = word
            true_lines.append(current_line)

    x_offset = y_offset = 0
    lineheight = font.getsize(true_lines[0])[1] * 1.2  # Give a margin of 0.2x the font height
    if vertical_allignment == ALLIGNMENT_CENTER:
        y = int(y + height / 2)
        y_offset = -(len(true_lines) * lineheight) / 2
    elif vertical_allignment == ALLIGNMENT_BOTTOM:
        y = int(y + height)
        y_offset = -(len(true_lines) * lineheight)

    for line in true_lines:
        linewidth = font.getsize(line)[0]
        if horizontal_allignment == ALLIGNMENT_CENTER:
            x_offset = (width - linewidth) / 2
        elif horizontal_allignment == ALLIGNMENT_RIGHT:
            x_offset = width - linewidth
        image_draw.text((int(x + x_offset), int(y + y_offset)), line, font=font, **kwargs)
        y_offset += lineheight


# helper function for fonts
def font(font_path, size=12):
    return ImageFont.truetype(font_path, size=size, encoding="unic")


img = Image.new("RGB", (300, 300), (255, 255, 255))
img_draw = ImageDraw.Draw(img)
text_box(
    "this is a text\n that respects lssssssssss rs rs          rs r rs rs rs rsinebreaks and will also break on spaces",
    img_draw,
    font("storage/fonts/pixel.ttf", 16),
    (20, 20, 260, 260),
    ALLIGNMENT_RIGHT,
    ALLIGNMENT_CENTER,
    fill=(255, 0, 255),
)
img.show()
