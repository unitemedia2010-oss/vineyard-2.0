import numpy as np
from PIL import Image

im = Image.open('public/assets/bottle_glass_hero.png').convert('RGBA')
w, h = im.size
arr = np.array(im, dtype=np.float32)

# Create an alpha mask with feathered edges
# We only want to feather the outer boundary (top, bottom, left, right)
feather_x = 24
feather_y = 24

alpha = np.ones((h, w), dtype=np.float32) * 255.0

# Feather left and right
for x in range(feather_x):
    factor = float(x) / feather_x
    alpha[:, x] *= factor
    alpha[:, w - 1 - x] *= factor

# Feather top and bottom
for y in range(feather_y):
    factor = float(y) / feather_y
    alpha[y, :] *= factor
    alpha[h - 1 - y, :] *= factor

arr[:, :, 3] = alpha
feathered = Image.fromarray(arr.astype(np.uint8), 'RGBA')
feathered.save('public/assets/bottle_glass_feathered.png', 'PNG')
print('Created feathered bottle & glass image with seamless edges!')
