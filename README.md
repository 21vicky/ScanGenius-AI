# 📝 ScanGenius AI

### AI-Powered Handwritten Text Recognition

ScanGenius AI is an AI-powered handwritten text recognition application that converts handwritten notes into editable digital text using Microsoft's TrOCR model.

It combines deep learning and computer vision to detect handwritten text regions, recognize handwriting, and extract digital text through an interactive Streamlit interface.

---

## ✨ Features

- 📤 Upload handwritten images (PNG, JPG, JPEG)
- 🤖 AI-powered handwriting recognition
- 🔍 Image preprocessing using OpenCV
- 📝 Handwritten line detection and extraction
- ✏️ Edit recognized text directly
- 📊 Word and character statistics
- ⬇️ Download extracted text
- 🎨 Interactive Streamlit interface

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | Interactive web interface |
| PyTorch | Deep learning framework |
| Hugging Face Transformers | Pretrained AI model |
| Microsoft TrOCR | Handwritten text recognition |
| OpenCV | Image preprocessing and line detection |
| NumPy | Image and numerical operations |
| Pillow (PIL) | Image handling |

---

## 🧠 How It Works

1. Upload a handwritten image.
2. Preprocess the image and isolate handwriting.
3. Detect individual handwritten text regions using OpenCV.
4. Pass detected regions to Microsoft's TrOCR model.
5. Convert handwriting into digital text.
6. Review, edit, and download the extracted result.

---

## 🔄 Project Workflow

The following diagram illustrates the Git workflow used to manage and publish ScanGenius AI.

![ScanGenius AI Git Workflow](assets/scangenius-workflow.png)

---

## 📂 Project Structure

```text
ScanGenius-AI/
│
├── app.py
│
├── utils/
│   ├── __init__.py
│   └── ocr_engine.py
│
├── assets/
│   ├── scangenius-dashboard.png
│   ├── scangenius-results.png
│   └── scangenius-workflow.png
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/21vicky/ScanGenius-AI.git
cd ScanGenius-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The TrOCR model will be downloaded automatically on its first run if it is not already cached.

---

## 📸 Screenshots

### Application Dashboard

![ScanGenius AI Dashboard](assets/scangenius-dashboard.png)

### OCR Recognition Results

![ScanGenius AI OCR Results](assets/scangenius-results.png)

---

## 🎯 Project Goal

To explore practical applications of artificial intelligence and computer vision by building a handwritten text recognition system using pretrained deep learning models.

---

## 🔮 Future Improvements

- Support for different handwriting colours.
- Improved recognition accuracy.
- Better full-page text segmentation.
- Multi-page document recognition.
- PDF upload and text extraction.

---

## 👨‍💻 Author

**Vignesh U**

Full Stack Developer | Python | AI & Data Analytics

GitHub: [21vicky](https://github.com/21vicky)

---

*Built with ❤️ using Python, Streamlit, PyTorch and Hugging Face Transformers.*