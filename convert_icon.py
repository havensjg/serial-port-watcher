# Tool for converting icon.png to a Windows .ico file

from PIL import Image

# Open icon
img = Image.open("icon.png")

# Make sure image is in RGBA
if img.mode != "RGBA":
    img = img.convert("RGBA")

# Define icon sizes
icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

# Save as .ico file
img.save("icon.ico", format="ICO", sizes=icon_sizes)