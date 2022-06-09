from captcha.image import ImageCaptcha
import random

import captcha
 
 if __name__ == '__main__':
    # Create an image instance of the given size
    sizes = []
    for i in range(1, 10):
        sizes.append(random.randint(110, 170))

    imageCaptcha = ImageCaptcha(fonts = ["./font.ttf"], font_sizes = sizes, width = 500, height = 300)
    #ImageCaptcha.create_noise_dots(image, color = (0, 0, 0), width = 1, number = 100)
    
    possibleLetters = "ABCEFGHJKLMNOPRSTUVWXYZ"

    captchaStr = " "
    for i in range(0, 5):
        captchaStr += random.choice(possibleLetters)
        captchaStr += " " * random.randint(1, 4)

    
    # generate the image of the given text
    data = imageCaptcha.generate(captchaStr)
    #image.create_noise_dots(image, color = (0, 0, 0), width = 1, number = 100)
    print(captchaStr)
    
    # write the image on the given file and save it
    imageCaptcha.write(captchaStr, 'CAPTCHA.png')