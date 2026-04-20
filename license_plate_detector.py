import cv2
import pytesseract
import re
import time
import os
from gtts import gTTS
from playsound import playsound
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path to where Tesseract is installed

# Load the Haar Cascade for license plate detection
plate_cascade = cv2.CascadeClassifier('india_license_plate.xml')  # Ensure the path is correct

# Check if the cascade loaded correctly
if plate_cascade.empty():
    print("Error: Could not load the Haar Cascade XML file.")
    exit()

def clean_plate_text(text):
    """
    Clean up the detected text and extract valid Indian license plates.
    """
    text = text.upper().replace(' ', '').replace('-', '')
    plate_pattern = r'[A-Z]{2}\d{1,2}[A-Z]{1,2}\d{1,4}'
    matches = re.findall(plate_pattern, text)
    valid_plates = [match for match in matches if 6 <= len(match) <= 10]
    return valid_plates

def detect_plate(img):
    plate_img = img.copy()
    roi = img.copy()
    plate_rects = plate_cascade.detectMultiScale(plate_img, scaleFactor=1.3, minNeighbors=7)
    detected_texts = []

    for (x, y, w, h) in plate_rects:
        roi_ = roi[y:y+h, x:x+w]
        cv2.rectangle(plate_img, (x, y), (x+w, y+h), (51, 51, 255), 3)
        gray_roi = cv2.cvtColor(roi_, cv2.COLOR_BGR2GRAY)
        plate_text = pytesseract.image_to_string(gray_roi, config='--psm 8')
        cleaned_plates = clean_plate_text(plate_text)
        detected_texts.extend(cleaned_plates)

    return plate_img, detected_texts

def process_video():
    cam = cv2.VideoCapture('car_plate_720p.mp4')

    if not cam.isOpened():
        print("Error: Unable to open video file.")
        exit()

    detected_plates = set()  # Use a set to avoid duplicates

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        # Display the original video
        cv2.imshow('Original Video', frame)

        # Process the frame
        processed_frame, plates = detect_plate(frame)
        detected_plates.update(plates)  # Add detected plates to the set

        # Display the processed video
        cv2.imshow('Processed Video', processed_frame)

        # Check for user input to exit
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
            break
        
        # Optional: Add a short delay to simulate real-time processing
        time.sleep(0.03)

    cam.release()
    cv2.destroyAllWindows()

    # Write the unique detected plates to a file
    with open("detected_plates.txt", "w") as f:
        for plate in detected_plates:
            f.write(f"{plate}\n")

def remove_repeated_words(text):
    """
    Remove lines with repeated words.
    """
    words = text.split()
    return len(words) != len(set(words))

def read_plate_numbers(file_name='detected_plates.txt'):
    """ Read plate numbers from a file and remove any duplicates """
    try:
        with open(file_name, 'r') as file:
            plate_numbers = file.read().splitlines()
        # Remove duplicates
        plate_numbers = list(set(plate_numbers))
        # Remove lines with repeated words
        plate_numbers = [plate for plate in plate_numbers if not remove_repeated_words(plate)]
        return plate_numbers
    except FileNotFoundError:
        print(f"Error: The file {file_name} does not exist.")
        return []

def count_cars_by_state(plate_numbers):
    """
    Count the number of cars for each state based on license plate prefixes.
    """
    state_counts = {}
    for plate in plate_numbers:
        if len(plate) >= 2:
            state_code = plate[:2]  # First two characters represent the state
            if state_code in state_counts:
                state_counts[state_code] += 1
            else:
                state_counts[state_code] = 1
    return state_counts

def create_pie_chart(state_counts):
    """
    Create a pie chart from the state counts and save it as an image.
    """
    labels = state_counts.keys()
    sizes = state_counts.values()

    # Create the pie chart
    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Cars by State')
    
    # Save the pie chart to the current folder
    plt.savefig('cars_by_state_pie_chart.png')
    plt.close()

def fetch_and_parse_data(url):
    """ Fetch and parse the data from the URL """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    data = {}
    
    try:
        # Extract License Plate Number
        plate_number = soup.find('p', class_='MuiTypography-root MuiTypography-body1 css-13blwe4')
        data['Number'] = plate_number.get_text(strip=True) if plate_number else 'Not Found'
        
        # Extract Owner Name
        owner_name = soup.find('p', class_='MuiTypography-root MuiTypography-body1 css-10hc59c')
        data['Owner Name'] = owner_name.get_text(strip=True) if owner_name else 'Not Found'
        
        # Extract Maker
        maker = soup.find('p', class_='MuiTypography-root MuiTypography-body1 css-kyau2h')
        data['Maker'] = maker.get_text(strip=True) if maker else 'Not Found'
        
        # Extract RTO Phone Number
        rto_phone = soup.find('p', class_='MuiTypography-root MuiTypography-body1 css-someclass')  # Update the class as needed
        data['RTO Phone Number'] = rto_phone.get_text(strip=True) if rto_phone else 'Not Found'
        
        # Extract Email
        email = soup.find('p', class_='MuiTypography-root MuiTypography-body1 css-anotherclass')  # Update the class as needed
        data['Email'] = email.get_text(strip=True) if email else 'Not Found'
        
    except AttributeError as e:
        print(f"Error: {e}")
    
    return data

def save_data_to_excel(data_list, file_name='vehicle_info.xlsx'):
    """ Save the scraped data to an Excel file """
    df = pd.DataFrame(data_list)
    df.to_excel(file_name, index=False)

def main():
    process_video()
    plate_numbers = read_plate_numbers()

    all_data = []
    
    # Open the 'links.txt' file to save generated URLs
    with open('links.txt', 'w') as links_file:
        for plate_number in plate_numbers:
            if plate_number:
                url = f"https://www.carinfo.app/rc-details/{plate_number}"
                print(f"Generated URL: {url}")
                # Write URL to 'links.txt'
                links_file.write(f"{url}\n")
                
                scraped_data = fetch_and_parse_data(url)
                if scraped_data:
                    all_data.append(scraped_data)
                    # Announce the plate number
                    speech_text = f"License plate: {plate_number}"
                    tts = gTTS(text=speech_text, lang='en')
                    audio_file = 'plate_announcement.mp3'
                    tts.save(audio_file)
                    playsound(audio_file)
                    os.remove(audio_file)
                else:
                    print(f"No data found for plate {plate_number}")

    # Save the scraped data to Excel
    save_data_to_excel(all_data)

    # Count cars by state
    state_counts = count_cars_by_state(plate_numbers)

    # Create and save pie chart of cars by state
    create_pie_chart(state_counts)

if __name__ == "__main__":
    main()
