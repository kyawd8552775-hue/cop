import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.ndimage import gaussian_filter
import json

# ---------------------------------------------------------
# Load spectrogram PNG
# ---------------------------------------------------------
def load_spectrogram_png(path):
    img = Image.open(path).convert("RGB")
    arr = np.array(img).astype(float) / 255.0
    return arr

# ---------------------------------------------------------
# Load events.json
# ---------------------------------------------------------
def load_events_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------------------------------------------
# Generate ripple field using your mapping rules
# ---------------------------------------------------------
def generate_ripple_field(events, width, height):
    H = np.zeros((height, width), dtype=float)

    for ev in events:
        cx = ev["t"] * width
        cy = (1 - ev["f"]) * height

        a = ev["a"]
        b = ev["b"]
        impact = ev["impact"]

        for y in range(height):
            for x in range(width):
                dx = (x - cx) / (a * 40)
                dy = (y - cy) / (b * 40)
                d = np.sqrt(dx*dx + dy*dy)

                # Water ripple formula
                ripple = np.sin(12 * d) * np.exp(-d * 2)

                H[y, x] += impact * ripple

    return gaussian_filter(H, sigma=1.5)

# ---------------------------------------------------------
# Color overlay using your blue/red mapping
# ---------------------------------------------------------
def generate_color_overlay(events, width, height):
    C = np.zeros((height, width, 3), dtype=float)

    for ev in events:
        cx = ev["t"] * width
        cy = (1 - ev["f"]) * height
        color = np.array(ev["color"])

        for y in range(height):
            for x in range(width):
                dx = (x - cx) / 50
                dy = (y - cy) / 50
                d = np.sqrt(dx*dx + dy*dy)

                w = np.exp(-d * 3)
                C[y, x] += color * w

    return np.clip(C, 0, 1)

# ---------------------------------------------------------
# Combine spectrogram + ripple + color
# ---------------------------------------------------------
def overlay_ripple(spec_img, ripple_field, color_field):
    final = (
        spec_img * 0.55 +          # base spectrogram
        color_field * 0.35 +       # color mapping
        ripple_field[..., None] * 0.25  # ripple height
    )
    return np.clip(final, 0, 1)

# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
def process_overlay(spec_png, events_json, out_path="overlay_output.png"):
    spec_img = load_spectrogram_png(spec_png)
    events = load_events_json(events_json)

    height, width, _ = spec_img.shape

    ripple_field = generate_ripple_field(events, width, height)
    color_field = generate_color_overlay(events, width, height)

    final_img = overlay_ripple(spec_img, ripple_field, color_field)

    plt.figure(figsize=(12, 6))
    plt.imshow(final_img)
    plt.axis("off")
    plt.savefig(out_path, dpi=150, bbox_inches="tight", pad_inches=0)
    plt.close()

    print("Overlay visualization saved:", out_path)


if __name__ == "__main__":
    process_overlay("web/mel.png", "web/events.json")
