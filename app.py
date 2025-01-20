import speech_recognition as sr
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from textblob import TextBlob  
import time


def setup_google_sheets():
    # Setting up Google Sheets API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("quick-geography-426804-e2-b7deff9240bc.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open("SentimentsStorage").sheet1  # Replace with your Google Sheets name
    return sheet


def audio_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening... Speak now! Say 'stop the process' to stop.")

        recognizer.adjust_for_ambient_noise(source)
        text = ""
        chunks = []
        start_time = time.time()

        while True:
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)  # Timeout after 10 seconds if no sound is detected
                print("Recognizing...")
                spoken_text = recognizer.recognize_google(audio)
                print(f"You said: {spoken_text}")

                text += " " + spoken_text
                chunks.append(spoken_text)

                if time.time() - start_time > 3:
                    print("Starting a new chunk due to silence.")
                    start_time = time.time()

                if "stop the process" in spoken_text.lower():
                    print("Stopping listening.")
                    break

            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                break
            except sr.WaitTimeoutError:
                print("Listening timeout. Please speak again.")
                continue

        return chunks, text.strip()  


def analyze_sentiment(text):
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity  
    if sentiment > 0:
        return  1
    elif sentiment < 0:
        return -1
    else:
        return 0


# Main Program Execution
if __name__ == "__main__":
    print("Initializing system...")
    sheet = setup_google_sheets()
    print("Google Sheets setup complete.")

    print("Press Enter to start listening.")
    input()

    chunks, full_text = audio_to_text()

    if full_text:
        print("\nTranscribed Full Text:")
        print(full_text)

        overall_sentiment = analyze_sentiment(full_text)
        print(f"\nOverall Sentiment: {overall_sentiment}")

        row_data = [full_text, overall_sentiment]  # Create a list for the full text and sentiment

        for i, chunk in enumerate(chunks):
            chunk_sentiment = analyze_sentiment(chunk)
            print(f"\nChunk {i+1}:")
            print(chunk)
            print(f"Sentiment: {chunk_sentiment}")
            row_data.extend([chunk, chunk_sentiment])  # Append chunk and sentiment to the row

        sheet.append_row(row_data)  # Append the whole row data (horizontally)
        print("\nText and Sentiment successfully added to Google Sheet!")
    else:
        print("\nNo valid text to analyze.")
