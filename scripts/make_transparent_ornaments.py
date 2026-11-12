import numpy as np
from PIL import Image

def extract_gold_on_dark(input_path, output_path, bg_color=(45, 12, 18), threshold=40):
    im = Image.open(input_path).convert('RGB')
    arr = np.array(im, dtype=np.float32)
    
    # Calculate brightness and color difference from background
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    
    # Background in the reference is dark bordeaux: around R=40-55, G=8-15, B=12-20
    # Gold pixels have high brightness (usually > 65) and strong yellow/orange tint (R > B, G > B)
    # Let's create an alpha channel based on brightness and warmth
    bg_diff = np.sqrt((r - 35)**2 + (g - 10)**2 + (b - 14)**2)
    
    # Alpha is low where it's close to dark background, high where it's bright gold
    alpha = np.clip((brightness - 25) / 70.0, 0, 1) * 255
    alpha = np.where(brightness < 22, 0, alpha).astype(np.uint8)
    
    rgba = np.dstack([im, alpha])
    out_im = Image.fromarray(rgba, 'RGBA')
    out_im.save(output_path, 'PNG')
    print(f"Saved transparent ornament to {output_path}")

extract_gold_on_dark('public/assets/ornament_left.png', 'public/assets/ornament_left_trans.png')
extract_gold_on_dark('public/assets/ornament_right.png', 'public/assets/ornament_right_trans.png')
extract_gold_on_dark('public/assets/phoenix_accent.png', 'public/assets/phoenix_accent_trans.png')
