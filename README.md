# 🫁 Chest X-Ray Pneumonia Detection

A deep learning-based web application for detecting **pneumonia from chest X-ray images** using computer vision and transfer learning.


## 🚀 Overview

Pneumonia is a potentially life-threatening lung infection that requires timely diagnosis. This project aims to assist in early detection by automatically classifying chest X-ray images into:

- **Normal**
- **Pneumonia**

The system combines a trained deep learning model with a simple web interface to enable real-time predictions.


## 🧠 Model & Methodology

- Transfer Learning using **MobileNetV2**
- Built with **TensorFlow / Keras**
- Image preprocessing using **OpenCV**
- Binary classification (Normal vs Pneumonia)

### Workflow:
1. Image preprocessing and normalization  
2. Model training on labeled dataset  
3. Performance evaluation  
4. Prediction on new images  
5. Integration with web interface  


## 📊 Dataset

This project uses the publicly available dataset:

👉 https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia

### Dataset Details:
- ~5,800+ chest X-ray images  
- Two classes: Normal and Pneumonia  
- Structured into train, test, and validation sets  


## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, PHP  
- **Backend:** Python  
- **ML Framework:** TensorFlow / Keras  
- **Libraries:** OpenCV, NumPy, Matplotlib  
- **Server:** XAMPP  
- **Version Control:** Git & GitHub  


## 📂 Project Structure
```chest-xray-pneumonia-detection/
│
├── 📁 src/
│ ├── train_model.py
│ ├── predict_single.py
│ └── predict_logic.py
│
├── 📁 uploads/ (ignored)
│
├── 🌐 index.php
├── 📄 generate_report.php
├── 📄 fpdf.php
│
├── ⚙️ .gitignore
└── 📘 README.md
```

## ⚙️ Setup Instructions

### 1. Clone the repository
git clone https://github.com/BarnaliDasg/chest-xray-pneumonia-detection.git

cd chest-xray-pneumonia-detection
### 2. Install dependencies
pip install -r requirements.txt
### 3. Train the model (optional)
python src/train_model.py
### 4. Run prediction
python src/predict_single.py
### 5. Run the web application
Move project to xampp/htdocs
Start Apache from XAMPP
Open in browser:
http://localhost/pneumonia_detection/

## ✨ Features
Upload chest X-ray images
Predict pneumonia instantly
Generate downloadable PDF reports
Simple and user-friendly interface

## 📈 Results

- **Test Accuracy: ~94.2%**
- The model achieves strong performance using transfer learning and preprocessing techniques, making it effective for basic pneumonia detection tasks.

## ⚠️ Disclaimer

This project is intended for educational purposes only and should not be used for medical diagnosis.

## 🙌 Acknowledgements
Kaggle dataset contributors
Open-source deep learning community

