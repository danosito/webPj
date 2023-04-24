from PIL import Image
img = Image.open("static/img/3.jpg")
img = img.crop(((img.size[0] - 400) // 2, 0, (img.size[0] - 400) // 2 + 400, 400) if img.size[0] > img.size[1] else (0, (img.size[1] - 400) // 2, 400, img.size[1] - 400) // 2 + 400)
img.save("test.jpg")