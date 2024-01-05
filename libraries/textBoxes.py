# found here https://gist.githubusercontent.com/digitaltembo/eb7c8a7fdef987e6689ee8de050720c4/raw/d80c4e75f028ab377bec263bbf64548b3a23b34d/text_box.py


""" 
Draws the text <text> on the ImageDraw <image_draw> in the box (specified as a 4-ple of [x,y,width,height])
with the font <font> and the alignments as given. Passes other arguments to the ImageDraw.text function 
(for example, fill is a good one to use here). 

Can be used to center text horizontally and vertically, as well as right-align and bottom-allign (although it defaults to
left- and top-alignment). Nothing is done to prevent overflow, but the y and height values from the box will be used for vertical
alignment.

Example usage:

    img = Image.new("RGB", (300,300), (255,255,255))
    img_draw = ImageDraw.Draw(img)
    text_box(
        "this is a text\n that respects linebreaks and will also break on spaces",
        img_draw,
        font("/Library/Fonts/Times New Roman Bold Italic.ttf", 16),
        (20, 20, 260,260),
        ALIGNMENT_RIGHT,
        ALIGNMENT_CENTER,
        fill=(255,0,255)
    )
    img.show()

    https://discord.com/channels/@me/1002014548619952149/1192782251637886996
"""

from PIL import Image, ImageDraw, ImageFont

# The various alignments.
# horizontal_alignment can take ALIGNMENT_LEFT, ALIGNMENT_CENTER, and ALIGNMENT_RIGHT
# verical_alignment can take ALIGNMENT_TOP, ALIGNMENT_CENTER, and ALIGNMENT_BOTTOM
ALIGNMENT_LEFT = 0
ALIGNMENT_CENTER = 1
ALIGNMENT_RIGHT = 2
ALIGNMENT_TOP = 3
ALIGNMENT_BOTTOM = 4


def text_box(text, image_draw, font, box, horizontal_alignment=ALIGNMENT_LEFT, vertical_alignment=ALIGNMENT_TOP, **kwargs):
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
    lineheight = font.getsize(true_lines[0])[1] * 1.2  # Gives a margin of 0.2x the font height
    if vertical_alignment == ALIGNMENT_CENTER:
        y = int(y + height / 2)
        y_offset = -(len(true_lines) * lineheight) / 2
    elif vertical_alignment == ALIGNMENT_BOTTOM:
        y = int(y + height)
        y_offset = -(len(true_lines) * lineheight)

    for line in true_lines:
        linewidth = font.getsize(line)[0]
        if horizontal_alignment == ALIGNMENT_CENTER:
            x_offset = (width - linewidth) / 2
        elif horizontal_alignment == ALIGNMENT_RIGHT:
            x_offset = width - linewidth
        image_draw.text((int(x + x_offset), int(y + y_offset)), line, font=font, **kwargs)
        y_offset += lineheight


# Helper function for fonts
def font(font_path, size=12):
    return ImageFont.truetype(font_path, size=size, encoding="unic")
