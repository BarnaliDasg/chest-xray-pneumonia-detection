import tensorflow as tf
import numpy as np
import cv2


# -----------------------------
# LOAD IMAGE
# -----------------------------
def get_img_array(img_path, size):

    img = tf.keras.preprocessing.image.load_img(
        img_path,
        target_size=size
    )

    array = tf.keras.preprocessing.image.img_to_array(img)

    array = np.expand_dims(array, axis=0)

    array = array / 255.0

    return array


# -----------------------------
# CLEAN THRESHOLD
# -----------------------------
def apply_threshold(heatmap, threshold=0.40):

    heatmap = np.where(
        heatmap > threshold,
        heatmap,
        0
    )

    return heatmap


# -----------------------------
# GENERATE GRADCAM
# -----------------------------
def make_gradcam_heatmap(
    img_array,
    model,
    last_conv_layer_name
):

    grad_model = tf.keras.models.Model(
        inputs=model.input,
        outputs=[
            model.get_layer(last_conv_layer_name).output,
            model.output
        ]
    )

    with tf.GradientTape() as tape:

        conv_outputs, predictions = grad_model(img_array)

        loss = predictions[:, 0]

    grads = tape.gradient(
        loss,
        conv_outputs
    )

    pooled_grads = tf.reduce_mean(
        grads,
        axis=(0, 1, 2)
    )

    conv_outputs = conv_outputs[0]

    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]

    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0)

    heatmap = heatmap / (
        tf.math.reduce_max(heatmap) + 1e-8
    )

    heatmap = heatmap.numpy()

    # Apply threshold
    heatmap = apply_threshold(heatmap)

    return heatmap


# -----------------------------
# OVERLAY HEATMAP
# -----------------------------
def overlay_heatmap(
    img_path,
    heatmap,
    alpha=0.4
):


    # Read original image
    img = cv2.imread(img_path)

    # Resize heatmap
    heatmap = cv2.resize(
        heatmap,
        (img.shape[1], img.shape[0])
    )

    # Normalize
    heatmap = np.maximum(heatmap, 0)

    heatmap = heatmap / (
        np.max(heatmap) + 1e-8
    )

    # Light threshold
    heatmap = np.where(
        heatmap > 0.20,
        heatmap,
        0
    )

    # Gentle blur
    heatmap = cv2.GaussianBlur(
        heatmap,
        (21, 21),
        0
    )

    # Convert to uint8
    heatmap_uint8 = np.uint8(
        255 * heatmap
    )

    # Apply colormap
    colored_heatmap = cv2.applyColorMap(
        heatmap_uint8,
        cv2.COLORMAP_JET
    )

    # Blend
    superimposed_img = cv2.addWeighted(
        img,
        0.75,
        colored_heatmap,
        alpha,
        0
    )

    return superimposed_img
