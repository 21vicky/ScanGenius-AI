
import cv2
import numpy as np
import torch

from PIL import Image
from transformers import (
    TrOCRProcessor,
    VisionEncoderDecoderModel
)


# ==========================================
# CONFIGURATION
# ==========================================

MODEL_NAME = "microsoft/trocr-base-handwritten"


# ==========================================
# LOAD AI MODEL
# ==========================================

def load_ocr_model():

    print("Loading ScanGenius AI model...", flush=True)

    torch.set_num_threads(2)

    processor = TrOCRProcessor.from_pretrained(
        MODEL_NAME
    )

    model = VisionEncoderDecoderModel.from_pretrained(
        MODEL_NAME
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"

    model.to(device)
    model.eval()

    print(
        f"Model loaded successfully on {device}",
        flush=True
    )

    return processor, model, device


# ==========================================
# BLUE INK DETECTION
# ==========================================

def create_ink_image(image):

    image_np = np.array(
        image.convert("RGB")
    )

    hsv = cv2.cvtColor(
        image_np,
        cv2.COLOR_RGB2HSV
    )

    # Detect blue handwriting
    lower_blue = np.array([90, 45, 20])
    upper_blue = np.array([140, 255, 255])

    blue_mask = cv2.inRange(
        hsv,
        lower_blue,
        upper_blue
    )

    # Remove tiny isolated noise
    kernel = np.ones((2, 2), np.uint8)

    blue_mask = cv2.morphologyEx(
        blue_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    # White background, black handwriting
    ink_image = np.full(
        blue_mask.shape,
        255,
        dtype=np.uint8
    )

    ink_image[blue_mask > 0] = 0

    return ink_image


# ==========================================
# DETECT HANDWRITTEN TEXT LINES
# ==========================================

def detect_text_lines(image):

    print("Detecting blue handwriting...", flush=True)

    ink_image = create_ink_image(image)

    height, width = ink_image.shape

    # Convert handwriting to foreground
    binary = cv2.threshold(
        ink_image,
        127,
        255,
        cv2.THRESH_BINARY_INV
    )[1]

    # Connect characters horizontally
    kernel_width = max(30, width // 24)

    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (kernel_width, 5)
    )

    connected = cv2.dilate(
        binary,
        kernel,
        iterations=1
    )

    # Find text contours
    contours, _ = cv2.findContours(
        connected,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    boxes = []

    for contour in contours:

        x, y, w, h = cv2.boundingRect(contour)

        # Ignore tiny noise
        if w > 30 and h > 10:

            padding_x = 15
            padding_y = 15

            x1 = max(0, x - padding_x)
            y1 = max(0, y - padding_y)

            x2 = min(width, x + w + padding_x)
            y2 = min(height, y + h + padding_y)

            boxes.append(
                (x1, y1, x2, y2)
            )

    # Sort lines from top to bottom
    boxes.sort(
        key=lambda box: box[1]
    )

    print(
        f"Detected handwriting regions: {len(boxes)}",
        flush=True
    )

    print(
        f"Bounding boxes: {boxes}",
        flush=True
    )

    return boxes


# ==========================================
# RECOGNIZE INDIVIDUAL TEXT LINE
# ==========================================

def recognize_line(image, processor, model, device):

    image = image.convert("RGB")

    # Ensure readable image dimensions
    image = image.resize(
        (
            max(1, image.width),
            max(1, image.height)
        )
    )

    pixel_values = processor(
        images=image,
        return_tensors="pt"
    ).pixel_values.to(device)

    with torch.inference_mode():

        generated_ids = model.generate(
            pixel_values,
            max_new_tokens=128,
            num_beams=4,
            early_stopping=True
        )

    extracted_text = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

    return extracted_text.strip()


# ==========================================
# MAIN OCR FUNCTION
# ==========================================

def extract_text(image, processor, model, device):

    print("\n" + "=" * 50, flush=True)

    print(
        "SCANGENIUS AI - OCR STARTED",
        flush=True
    )

    print("=" * 50, flush=True)

    image = image.convert("RGB")

    # Detect handwritten lines
    boxes = detect_text_lines(image)

    # Create clean black-and-white handwriting image
    ink_image = Image.fromarray(
        create_ink_image(image)
    ).convert("RGB")

    # Fallback when no handwriting is detected
    if not boxes:

        print(
            "No handwriting detected. Using full image.",
            flush=True
        )

        return recognize_line(
            ink_image,
            processor,
            model,
            device
        )

    extracted_lines = []

    # Recognize each handwritten line
    for index, (x1, y1, x2, y2) in enumerate(boxes):

        print(
            f"\nProcessing line {index + 1}/{len(boxes)}",
            flush=True
        )

        cropped_line = ink_image.crop(
            (x1, y1, x2, y2)
        )

        text = recognize_line(
            cropped_line,
            processor,
            model,
            device
        )

        print(
            f"Recognized line {index + 1}: {text}",
            flush=True
        )

        if text:

            extracted_lines.append(text)

    # Combine all recognized lines
    final_text = "\n".join(
        extracted_lines
    )

    print("\n" + "=" * 50, flush=True)

    print(
        "FINAL OCR RESULT:",
        flush=True
    )

    print(final_text, flush=True)

    print("=" * 50, flush=True)

    return final_text
