# Convert an image to a pencil sketch

### Import Libraries -

- `openCV` is the only library which is needed for the project. 
- `matplotlib` library will also be used optionally for some visualizations.

### Steps -

1. Read the image in BGR format and then convert it to a grayscale image. This will turn an image 
into a classic black and white photo. 
2. Then invert the grayscale image also called negative image, this will be our inverted grayscale image. Inversion 
can be used to enhance details.
3. Finally, create the pencil sketch by mixing the grayscale image with the inverted blurry image. 
This can be done by dividing the grayscale image by the inverted blurry image. Since images are just arrays, 
we can easily do this programmatically using the divide function from the cv2 library in Python.

### program files

1. `image_to_pencil_sketch.ipynb` - jupyter notebook with step-by-step instructions and visualizations.
2. `image_to_pencil_sketch.py` - interactive python program file for converting images to sketch.