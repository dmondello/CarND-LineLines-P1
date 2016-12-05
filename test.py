#
#  Importo le librerie necessarie
#
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

#
# Leggo un immagine png e la converto in bytescale a 0,255
#
image = (mpimg.imread('test.png') * 255).astype('uint8')

# Recupero x e y e faccio una copia dell'immagine
ysize = image.shape[0]
xsize = image.shape[1]
color_select = np.copy(image)
# print("dimensione immagine",ysize,"x",xsize)

#line_image = np.copy(image)

# Definisco il criterio per la selezione dei colori
red_threshold = 200
green_threshold = 200
blue_threshold = 200

# Creo una soglia per valòutare il colonre dei pixel
rgb_threshold = [red_threshold, green_threshold, blue_threshold]

# Definisco una maschera triangolare (x=0, y=0 è in alto a sinistra
left_bottom = [0, 539]
right_bottom = [900, 539]
apex = [400, 0]

# Perform a linear fit (y=Ax+B) to each of the three sides of the triangle
# np.polyfit returns the coefficients [A, B] of the fit
fit_left = np.polyfit((left_bottom[0], apex[0]), (left_bottom[1], apex[1]), 1)
fit_right = np.polyfit((right_bottom[0], apex[0]), (right_bottom[1], apex[1]), 1)
fit_bottom = np.polyfit((left_bottom[0], right_bottom[0]), (left_bottom[1], right_bottom[1]), 1)

# print(fit_left)
# print(fit_right)
# print(fit_bottom)

# Perform a "bitwise or" to mask pixels below the threshold
color_thresholds = (image[:, :, 0] < rgb_threshold[0]) | \
                   (image[:, :, 1] < rgb_threshold[1]) | \
                   (image[:, :, 2] < rgb_threshold[2])

# Find the region inside the lines
XX, YY = np.meshgrid(np.arange(0, xsize), np.arange(0, ysize))
region_thresholds = (YY > (XX * fit_left[0] + fit_left[1])) & \
                    (YY > (XX * fit_right[0] + fit_right[1])) & \
                    (YY < (XX * fit_bottom[0] + fit_bottom[1]))

# Mask color and region selection
# color_select[color_thresholds | ~region_thresholds] = [0, 0, 0]
# Color pixels red where both color and region selections met
# line_image[~color_thresholds & region_thresholds] = [255, 0, 0]

# Display the image and show region and color selections
plt.imshow(image)
x = [left_bottom[0], right_bottom[0], apex[0], left_bottom[0]]
y = [left_bottom[1], right_bottom[1], apex[1], left_bottom[1]]
plt.plot(x, y, 'b--', lw=4)
plt.savefig('color_select')
#plt.imshow(color_select)
plt.savefig("line_image")
#plt.imshow(line_image)