from PIL import Image
import math

def add_filter(image, filter):
	chroma_key = (255, 255, 255, 255)
	s_image = Image.open(image)
	filter_image = Image.open(f'templates/{filter}.png')
	for y in range(0, s_image.height):
		for x in range(0, s_image.width):
			f_rgb = filter_image.getpixel((x, y))
			if f_rgb != chroma_key:
				s_image.putpixel((x, y), filter_image.getpixel((x, y)))
	s_image.save(image)

def bigger(image):
	s_image = Image.open(image)
	width, height = s_image.size
	canvas = Image.new('RGB', (width*2,height*2), 'white')
	target_x = 0
	for source_x in range(0, s_image.width):
		target_y = 0
		for source_y in range(0, s_image.height):
			color = s_image.getpixel((source_x, source_y))
			canvas.putpixel((target_x, target_y), color)
			canvas.putpixel((target_x, target_y+1), color)
			canvas.putpixel((target_x+1, target_y), color)
			canvas.putpixel((target_x+1, target_y+1), color)
			target_y += 2
		target_x += 2
	canvas.save(image)
	
def smaller(image):
	s_image = Image.open(image)
	width, height = s_image.size
	canvas = Image.new('RGB', (math.ceil(width/2),math.ceil(height/2)), 'white')
	target_x = 0
	for source_x in range(0, s_image.width, 2):
		target_y = 0
		for source_y in range(0, s_image.height, 2):
			color = s_image.getpixel((source_x, source_y))
			canvas.putpixel((target_x, target_y), color)
			target_y += 1
		target_x += 1
	canvas.save(image)

def negative(image):
	s_image = Image.open(image)
	new_list = []
	for p in s_image.getdata():
		temp = (255-p[0], 255-p[1], 255-p[2])
		new_list.append(temp)
	s_image.putdata(new_list)
	s_image.save(image)

def grayscale(picture):
	new_list = []
	for p in picture.getdata():
		new_red = int(p[0] * 0.299)
		new_green = int(p[1] * 0.587)
		new_blue = int(p[2] * 0.114)
		luminance = new_red + new_green + new_blue
		temp = (luminance, luminance, luminance)
		new_list.append(temp)
	return new_list

def grayscale_create(image):
	s_image = Image.open(image)
	new_list = []
	for p in s_image.getdata():
		new_red = int(p[0] * 0.299)
		new_green = int(p[1] * 0.587)
		new_blue = int(p[2] * 0.114)
		luminance = new_red + new_green + new_blue
		temp = (luminance, luminance, luminance)
		new_list.append(temp)
	s_image.putdata(new_list)
	s_image.save(image)

def sepia_tint(image):
	s_image = Image.open(image)
	width, height = s_image.size
	mode = s_image.mode
	temp_list = []
	pic_data = grayscale(s_image)

	for p in pic_data:
	# tint shadows
		if p[0] < 63:
			red_val = int(p[0] * 1.1)
			green_val = p[1]
			blue_val = int(p[2] * 0.9)

		# tint midtones
		if p[0] > 62 and p[0] < 192:
			red_val = int(p[0] * 1.15)
			green_val = p[1]
			blue_val = int(p[2] * 0.85)

		# tint highlights
		if p[0] > 191:
			red_val = int(p[0] * 1.08)
			if red_val > 255:
				red_val = 255
			green_val = p[1]
			blue_val = int(p[2] * 0.5)
		temp_list.append((red_val, green_val, blue_val))
	s_image.putdata(temp_list)
	s_image.save(image)