import numpy as np
from PIL import Image

im = Image.open('public/assets/bottle_glass_hero.png').convert('RGB')
arr = np.array(im, dtype=np.float32)

# Save high quality PNG
im.save('public/assets/bottle_glass_original.png')

# Also create an alpha-extracted version where the background dark maroon fades out
r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
brightness = 0.299 * r + 0.587 * g + 0.114 * b

# Background pixels have brightness around 20-40, bottle and glass have specular highlights and dark liquid
# For dark liquid, we want to preserve dark red pixels
# Let's see: pixels that are part of the bottle/glass vs flat background
# A smooth mask can be created
print('Extracted bottle glass hero')
