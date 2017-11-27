from PIL import Image

# Creates a copy of an image with a filter
def add_filter(image, filter, chroma_key):
	filter_image = Image.new('RGB', image.size(), 'white')
	# Use a for loop to search through every pixel of the image
	for y in image.height():
		for x in image.width():
			f_rgb = filter.getpixel((x, y))
			# If the pixel is the color of the chroma key, use image pixel
			if f_rgb == chroma_key:
				filter_image.putpixel((x, y), image.getpixel((x, y))
			# If the pixel isn't the color of the chroma key, use filter pixel
			else:
				filter_image.putpixel((x, y), f_rgb)
	return filter_image
	
# Saves the filtered image to a directory
def save_filter(filter_image, name):
	filter_image.save(f'{name}.jpg')