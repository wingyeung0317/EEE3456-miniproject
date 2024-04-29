import time
import digitalio
import board
from PIL import Image, ImageDraw
from PIL import ImageFont
import adafruit_rgb_display.st7735 as st7735

# Define Color for this display
BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
BLUE    = (255,   0,   0)
GREEN   = (  0, 255,   0)
RED     = (  0,   0, 255)
CYAN    = (255, 255,   0)
MAGENTA = (255,   0, 255)
YELLOW  = (  0, 255, 255)

# Define constants to allow easy resizing of shapes
BORDER = 10
FONTSIZE = 12

class ST7735:
    def __init__(self, cs_pin = digitalio.DigitalInOut(board.CE0), dc_pin = digitalio.DigitalInOut(board.D25), reset_pin = digitalio.DigitalInOut(board.D24)):
        self.__cs_pin = cs_pin
        self.__dc_pin = dc_pin
        self.__reset_pin = reset_pin
        
        self.__BAUDRATE = 24000000 #24MHz
        # Setup SPI bus using hardware SPI
        self.__spi = board.SPI()

        # Create the display
        self.disp = st7735.ST7735R(
            self.__spi,
            rotation=90,
            cs=self.__cs_pin,
            dc=self.__dc_pin,
            rst=self.__reset_pin,
            baudrate=self.__BAUDRATE
        )
        
        # Create blank image for drawing, (160 x 128)
        if self.disp.rotation % 180 == 90:
            self.height = self.disp.width
            self.width = self.disp.height
        else:
            self.width = self.disp.width
            self.height = self.disp.height
            
        self.__image = Image.new("RGB", (self.width, self.height))

        # Get drawing object to draw on image
        self.draw = ImageDraw.Draw(self.__image)

        # Load a TTF font
        self.__font = ImageFont.truetype("/user/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", FONTSIZE)

    def custom_img(self, img):
        image = Image.open(img)
        self.__image = image.rotate(0).resize((self.width, self.height))
        self.draw = ImageDraw.Draw(self.__image)

    def custom_rectangle(self, color1=GREEN, color2 = MAGENTA):
        width = self.width
        height = self.height
        # Draw a green filled box as the background
        self.draw.rectangle((0, 0, width, height), outline=color1, fill=GREEN)
        #Draw a smaller inner purple rectangle
        self.draw.rectangle((BORDER, BORDER, width-BORDER, height-BORDER-1), outline=color2, fill=color2)

    def custom_text(self, font:ImageFont.FreeTypeFont=None, text="Hello World!", color=WHITE):
        font = self.__font if font==None else font
        # Draw some text
        (font_width, font_height) = font.getsize(text)
        self.draw.text(
            (self.width // 2 - font_width // 2, self.height // 2 - font_height // 2),
            text,
            font=font,
            fill=color,
        )
    
    def image(self):
        self.disp.image(self.__image)