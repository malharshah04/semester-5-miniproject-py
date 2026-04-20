# 🚗 License Plate Detection & Vehicle Info System

## 📖 Overview

This project detects Indian vehicle license plates from a video, extracts text using OCR, and gathers additional vehicle details via web scraping. It also provides analytics and audio feedback.

---

## ✨ Features

* 🎥 Detect license plates from video using OpenCV
* 🔍 Extract text using Tesseract OCR
* 🧹 Clean and validate Indian license plate format
* 🔊 Announce detected plates using text-to-speech
* 🌐 Fetch vehicle details from web
* 📊 Generate analytics (cars by state)
* 📈 Create pie chart visualization
* 📁 Export data to Excel

---

## 🛠️ Technologies Used

* Python
* OpenCV
* Tesseract OCR
* Regex
* gTTS (Google Text-to-Speech)
* BeautifulSoup (Web Scraping)
* Pandas
* Matplotlib

---

## 📂 Project Structure

```
├── license_plate_detector.py
├── india_license_plate.xml
├── car_plate_720p.mp4
├── detected_plates.txt
├── links.txt
├── vehicle_info.xlsx
├── cars_by_state_pie_chart.png
```

---

## ⚙️ Installation

### 1. Install Dependencies

```bash
pip install opencv-python pytesseract gtts playsound requests beautifulsoup4 pandas matplotlib
```

### 2. Install Tesseract OCR

Download and install Tesseract from:
https://github.com/tesseract-ocr/tesseract

Update path in code:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## ▶️ How to Run

```bash
python license_plate_detector.py
```

Press **ESC** to stop the video processing.

---

## 🔄 Workflow

1. Video is loaded and frames are processed
2. License plates are detected using Haar Cascade
3. OCR extracts plate text
4. Regex filters valid Indian plates
5. Unique plates are stored in a file
6. URLs are generated for each plate
7. Vehicle details are scraped
8. Data is saved to Excel
9. Pie chart of state distribution is created
10. Plate numbers are announced via audio

---

## 📊 Output Files

* `detected_plates.txt` → List of detected plates
* `links.txt` → Generated URLs
* `vehicle_info.xlsx` → Vehicle details
* `cars_by_state_pie_chart.png` → Visualization

---

## ⚠️ Notes

* Ensure Haar Cascade XML file is present
* Internet connection required for scraping
* Website structure may change (scraper may need updates)
* Tesseract path must be correctly set

---

## 🚀 Future Improvements

* Real-time camera integration
* Higher accuracy detection models (YOLO)
* Database integration
* GUI dashboard
* API-based vehicle data fetching

---

## 👨‍💻 Author

Developed as part of a smart automation / AI-based project.

---

## 📜 License

This project is for educational purposes.
