
import gradio as gr
import numpy as np
from PIL import Image, ImageEnhance

def diagnose(image):
    if image is None:
        return "Please upload a leaf photo.", None

    image = image.convert("RGB").resize((200, 200))
    arr = np.array(image)

    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    green = (g > r * 1.10) & (g > b * 1.05)
    spots = (r > 100) & (g > 75) & (r >= g) & (g > b * 1.10)

    green_ratio = green.mean()
    spot_ratio = spots.mean()

    if spot_ratio > 0.20:
        finding = "Possible leaf discoloration or leaf spots."
        advice = (
            "Inspect both sides of the leaf. Avoid wetting leaves "
            "when watering. Ask an agricultural expert to confirm "
            "the disease before applying treatment."
        )
    elif green_ratio < 0.25:
        finding = "Uncertain result: the leaf or image may be unclear."
        advice = (
            "Take a clear photo in natural light. Check for pests, "
            "spots, curling, and wilting. Consult an agricultural expert."
        )
    else:
        finding = "No obvious discoloration detected by this basic check."
        advice = (
            "Continue monitoring the plant and check for unusual "
            "spots, insects, or wilting."
        )

    report = (
        "CROP DOCTOR - PRELIMINARY REPORT\n\n"
        + finding + "\n\n"
        + advice + "\n\n"
        + "Green pixels: " + str(round(green_ratio * 100, 1)) + "%\n"
        + "Yellow/brown pixels: " + str(round(spot_ratio * 100, 1))
        + "%\n\n"
        + "This is a basic image-processing demo, not a trained "
        "ML disease detector. Results may be inaccurate."
    )

    processed = ImageEnhance.Contrast(image).enhance(1.2)
    return report, processed

with gr.Blocks(title="Crop Doctor") as demo:
    gr.Markdown("# Crop Doctor")
    gr.Markdown("Upload a leaf image for a preliminary check.")
    photo = gr.Image(type="pil", label="Leaf photo")
    button = gr.Button("Check Leaf")
    report = gr.Textbox(label="Finding and advice", lines=10)
    processed = gr.Image(label="Processed image")
    button.click(diagnose, inputs=photo, outputs=[report, processed])

demo.launch()
