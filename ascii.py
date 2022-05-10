# ascii commands are based of the code found here https://github.com/LyricLy/ASCIIpy/blob/master/bot.py


import argparse
import subprocess
import string
aeirshkvauialufwblefwakicneiaikvalukvifpvulblckefawlvilvnecki
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont


DEFAULT_CHARS = string.ascii_letters + string.digits + string.punctuation + " "
DEFAULT_FONT = "Inconsolata"


def get_font(font_name):
    filename = subprocess.check_output(["fc-match", font_name]).decode().split(":")[0]
    if filename == "arial.ttf" and font_name.lower() not in ("arial", "sans-serif"):
        return None
    return ImageFont.truetype(filename, 12)


def get_size(text, font, spacing=0):
    return ImageDraw.Draw(Image.new("1", (0, 0))).multiline_textsize(
        text, font=font, spacing=spacing
    )


def make_mapping(charset, font, invert):
    float_mapping = {}
    for char in charset:
        x, y = get_size(char, font)

        im = Image.new("L", (x, y * 3), color=255 if invert else 0)
        draw = ImageDraw.Draw(im)
        draw.text((0, 0), " \n" + char, font=font, fill=0 if invert else 255, spacing=0)
        im = im.crop((0, y + 1, x, y * 2 + 1))
        avg = sum(im.getdata()) ** 0.5
        float_mapping[avg] = char
    mn, mx = min(float_mapping), max(float_mapping)
    mapping = []
    for n in range(256):
        total = min(float_mapping.items(), key=lambda x: abs(n / 255 - (x[0] - mn) / (mx - mn)))
        mapping.append(((total[0] - mn) / (mx - mn), total[1]))
    return mapping, (x, y)


def convert(im, mapping, ratio, dither):
    width, height = im.size
    text = []
    c = 0
    offsets = defaultdict(int)
    for i, px in enumerate(im.convert(mode="L").getdata()):
        if i % width == 0:
            c = 0
            text.append([])
        c += ratio
        chars, c = divmod(c, 1)
        if dither:
            new_px = px + offsets[i]
            value, char = mapping[min(max(int(new_px), 0), 255)]
            error = new_px - value * 255
            if i + 1 % width != 0:
                offsets[i + 1] += error * (7 / 16)
                offsets[i + width + 1] += error * (1 / 16)
            if i % width != 0:
                offsets[i + width - 1] += error * (3 / 16)
            offsets[i + width] += error * (5 / 16)
        else:
            char = mapping[px][1]
        text[-1].extend(char * int(chars))
    return "\n".join("".join(l) for l in text)


def to_image(text, font, invert, spacing):
    size = get_size(text, font, spacing)
    im = Image.new("L", size, color=255 if invert else 0)
    draw = ImageDraw.Draw(im)
    draw.multiline_text((0, 0), text, font=font, fill=0 if invert else 255, spacing=spacing)
    return im


def full_convert(im, *, invert, font, spacing, charset, out_text, dither, in_scale, out_scale):
    width, height = im.size
    scaled_im = im.resize((int(width * in_scale), int(height * in_scale)))
    mapping, (fx, fy) = make_mapping(charset, font, invert)
    text = convert(scaled_im, mapping, (fy + spacing) / fx, dither)
    if out_text:
        return text
    else:
        out_im = to_image(text, font, invert, spacing)
        out_width, out_height = out_im.size
        return out_im.resize(
            (int(out_width * out_scale), int(out_height * out_scale)), Image.BILINEAR
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert an image or sequence of images to text.")
    parser.add_argument("input_file", help="Image to convert to ASCII.")
    parser.add_argument("output_file", help="File to save the result to.")
    parser.add_argument(
        "-i",
        "--invert",
        action="store_true",
        help="Target black on white instead of white on black.",
    )
    parser.add_argument(
        "-f",
        "--font",
        default=DEFAULT_FONT,
        help="The font to target. Defaults to Consolas.",
    )
    parser.add_argument(
        "-s",
        "--spacing",
        default=0,
        type=int,
        help="The line spacing, in pixels, to target. Defaults to 0.",
    )
    parser.add_argument(
        "-c",
        "--charset",
        default=DEFAULT_CHARS,
        help="The set of valid characters to use. Defaults to printable ASCII.",
    )
    parser.add_argument(
        "-is",
        "--in-scale",
        type=float,
        default=1,
        help="Factor to scale the input image by. Defaults to 1.",
    )
    parser.add_argument(
        "-os",
        "--out-scale",
        type=float,
        default=1,
        help="Factor to scale the output image by. Does nothing if the --text flag is passed. Defaults to 1.",
    )
    parser.add_argument("-t", "--text", action="store_true", help="Output a text file.")
    parser.add_argument(
        "-nd",
        "--no-dither",
        action="store_true",
        help="Don't apply dithering to the output.",
    )
    args = parser.parse_args()

    im = Image.open(args.input_file)

    r = full_convert(
        im,
        invert=args.invert,
        font=get_font(args.font),
        spacing=args.spacing,
        charset=args.charset,
        out_text=args.text,
        dither=not args.no_dither,
        in_scale=args.in_scale,
        out_scale=args.out_scale,
    )

    if args.text:
        with open(args.output_file, "w") as f:
            f.write(r)
    else:
        r.save(args.output_file)
