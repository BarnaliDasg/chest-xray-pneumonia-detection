🫁 Chest X-Ray Pneumonia Detection

A deep learning-based web application that detects pneumonia from chest X-ray images using computer vision and neural networks.

🚀 Overview

Pneumonia is a serious lung infection that requires early and accurate diagnosis. This project leverages Deep Learning + Medical Imaging to automatically classify chest X-ray images as:

✅ Normal
⚠️ Pneumonia

The system integrates:

A trained deep learning model
A prediction pipeline
A web interface for real-time usage
🧠 Model & Approach
Built using Python, TensorFlow/Keras
Transfer Learning with MobileNetV2
Image preprocessing using OpenCV
Binary classification (Normal vs Pneumonia)
🔍 Workflow
Load and preprocess X-ray images
Train CNN model using labeled dataset
Evaluate performance on test data
Deploy prediction pipeline
Integrate with web interface (PHP)
📊 Dataset

This project uses the publicly available dataset:

👉 Chest X-Ray Pneumonia Dataset

📌 Dataset Details:
~5,800+ chest X-ray images
Two classes:
Normal
Pneumonia
Organized into:
train/
test/
val/
Images sourced from pediatric patients (1–5 years old)
🛠️ Tech Stack
Frontend: HTML, CSS, PHP
Backend: Python
ML Framework: TensorFlow / Keras
Libraries: OpenCV, NumPy, Matplotlib
Version Control: Git & GitHub
📂 Project Structure
chest-xray-pneumonia-detection/
│
├── src/
│   ├── train_model.py
│   ├── predict_single.py
│   ├── predict_logic.py
│
├── uploads/              # User uploaded images (ignored in git)
├── index.php             # Web interface
├── generate_report.php   # Report generation
├── fpdf.php              # PDF handling
├── .gitignore
└── README.md
⚙️ Installation & Setup
🔹 1. Clone the repository
git clone https://github.com/BarnaliDasg/chest-xray-pneumonia-detection.git
cd chest-xray-pneumonia-detection
🔹 2. Install dependencies
pip install -r requirements.txt
🔹 3. Run training (optional)
python src/train_model.py
🔹 4. Run prediction
python src/predict_single.py
🔹 5. Run web app
Place project inside xampp/htdocs
Start Apache server
Open:
http://localhost/pneumonia_detection/
📸 Features
Upload chest X-ray image
Predict pneumonia instantly
Generate PDF report
Visualize model performance
📈 Results
Achieved high accuracy using transfer learning
Improved performance with data preprocessing
Handles real-world X-ray variations
⚠️ Disclaimer

This project is for educational and research purposes only.
It is not a substitute for professional medical diagnosis.

🙌 Acknowledgements
Dataset by Kaggle contributors
Research inspiration from deep learning in medical imaging
Based on real-world clinical X-ray data
