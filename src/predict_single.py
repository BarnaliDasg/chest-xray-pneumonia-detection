import os
import sys
import json
import logging
import cv2
import numpy as np

# 🔇 Silence TensorFlow logs BEFORE importing it
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('absl').setLevel(logging.ERROR)

from tensorflow.keras.models import load_model
from gradcam import get_img_array, make_gradcam_heatmap, overlay_heatmap

# Model path
MODEL_PATH = r"C:\xampp\htdocs\pneumonia_detection\model\pneumonia_detection_model.h5"

# ✅ Load model WITHOUT compile (removes warning)
model = load_model(MODEL_PATH, compile=False)


def predict_image(img_path):
    if not os.path.exists(img_path):
        return {"error": "Image not found"}

    img = cv2.imread(img_path)
    if img is None:
        return {"error": "Invalid image file"}

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Model input
    x = cv2.resize(img_rgb, (150, 150))
    x = np.expand_dims(x, axis=0) / 255.0

    # Prediction
    prediction = float(model.predict(x, verbose=0)[0][0])
    label = "PNEUMONIA" if prediction > 0.5 else "NORMAL"

    # 🔥 Grad-CAM
    img_array = get_img_array(img_path, size=(150, 150))

    heatmap = make_gradcam_heatmap(
        img_array,
        model,
        last_conv_layer_name="Conv_1"  # change if needed
    )

    cam_image = overlay_heatmap(img_path, heatmap)

    filename = os.path.basename(img_path)
    cam_path = f"uploads/gradcam_{filename}"

    cv2.imwrite(cam_path, cam_image)

    return {
        "label": label,
        "confidence": float(round(prediction * 100, 2)),
        "gradcam": cam_path
    }


# 🔥 Entry point for PHP
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stdout.write(json.dumps({"error": "No input image"}))
        sys.exit(1)

    img_path = sys.argv[1]

    try:
        result = predict_image(img_path)
        sys.stdout.write(json.dumps(result))
        sys.stdout.flush()
    except Exception as e:
        sys.stdout.write(json.dumps({"error": str(e)}))
        sys.stdout.flush()