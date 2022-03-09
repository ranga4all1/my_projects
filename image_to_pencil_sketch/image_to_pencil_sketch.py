# image to pencil sketch using cv2, python and matplotlib for visualization

# import the necessary packages
import cv2
import matplotlib.pyplot as plt

# load the image and view it
# image = cv2.imread("mahatma_gandhi.jpg")   # this is read in BGR format
# cv2.imshow("Original image", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Alternatively, we can use matplotlib to display the image
# RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # convert to RGB for matplotlib
# plt.imshow(RGB_image)
# plt.axis(False)
# plt.savefig('temp.png')
# plt.show()

'''
Matplotlib vs OpenCV

We can observe that the image displayed using matplotlib is not consistent with the original image.

This is because OpenCV uses BGR color scheme whereas matplotlib uses RGB colors scheme.

We can convert BGR image to RGB by using any of the following methods.
'''

# Convert BGR to RGB: Method 1
# plt.imshow(image[:,:,::-1])
# plt.axis(False)
# plt.savefig('temp1.png')
# plt.show()

# Convert BGR to RGB: Method 2
# RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# plt.imshow(RGB_image)
# plt.axis(False)
# plt.savefig('temp2.png')
# plt.show()


## Transform photo to pencil sketch
# Convert image to grayscale
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow("Gray image", gray_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# inverting the image
# inverted_image = cv2.bitwise_not(gray_image)
# inverted_image = 255 - gray_image
# cv2.imshow("Inverted image", inverted_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# applying gaussian blur
# blurred_image = cv2.GaussianBlur(inverted_image, (111, 111), 0)
# cv2.imshow("blurred image", blurred_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# invert the blurred image
# inverted_blurred_image = cv2.bitwise_not(blurred_image)
# cv2.imshow("inverted blurred image", inverted_blurred_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# sketching the image by dividing the gray image with the inverted blurred image
# sketch_image = cv2.divide(gray_image, inverted_blurred_image, scale=256)
# cv2.imshow("sketch image", sketch_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# save the sketch image
# cv2.imwrite("sketch_image.jpg", sketch_image)   # jpg format
# cv2.imwrite("sketch_image.png", sketch_image)   # png format

# display the sketch image interactively
# cv2.imshow("sketch image", sketch_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# display the sketch image using matplotlib
# RGB_sketch_image = cv2.cvtColor(sketch_image, cv2.COLOR_GRAY2RGB)
# plt.imshow(RGB_sketch_image)
# plt.axis(False)
# plt.savefig('temp3.png')
# plt.show()


# Let's display the original image and sketch image side by side using matplotlib
# plt.figure(figsize=(20,10))
#
# plt.subplot(1, 2, 1)
# plt.title("Original Image", size=15)
# plt.imshow(RGB_image)
# plt.axis("off")
#
# plt.subplot(1, 2, 2)
# plt.title("Sketch Image", size=15)
# RGB_sketch_image = cv2.cvtColor(sketch_image, cv2.COLOR_GRAY2RGB)
# plt.imshow(RGB_sketch_image)
# plt.axis("off")
# plt.savefig('temp4.png')
# plt.show()

#  Combine everything together to create a function that returns the sketch
#  of an image
def sketch_image(photo, k_size):
    # read the photo
    image = cv2.imread(photo)

    # convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # inverting the image
    inverted_image = cv2.bitwise_not(gray_image)

    # applying gaussian blur
    blurred_image = cv2.GaussianBlur(inverted_image, (k_size, k_size), 0)

    # invert the blurred image
    inverted_blurred_image = cv2.bitwise_not(blurred_image)

    # sketching the image by dividing the gray image with the inverted blurred image
    sketch_image = cv2.divide(gray_image, inverted_blurred_image, scale=256)

    # save the sketch image
    cv2.imwrite("sketch_image.jpg", sketch_image)   # jpg format
    # v2.imwrite("sketch_image.png", sketch_image)   # png format

    # display the sketch image interactively
    # cv2.imshow("sketch image", sketch_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # display the sketch image
    RGB_sketch_image = cv2.cvtColor(sketch_image, cv2.COLOR_GRAY2RGB)
    plt.figure(figsize=(20,10))
    plt.title("Sketch Image", size=15)
    plt.imshow(RGB_sketch_image)
    plt.axis(False)
    plt.savefig('temp5.png')
    plt.show()

#  function call
sketch_image(photo="mahatma_gandhi.jpg", k_size=111)