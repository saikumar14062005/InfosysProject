
# import streamlit as st
# import json
# import time
# from sentimentAnalysis import *
# from rag import *
# from pieChart import *
# import cohere
# import uuid
# import speech_recognition as sr
# from removeDuplicates import *

# # Initialize the Cohere client
# co = cohere.Client("IT8QOLxK1JfYlN0vRwoCBmkjnvjqC0cXOOrlz7o1")

# # Load the objections from JSON file
# with open("objections.json", "r") as f:
#     objections_data = json.load(f)

# # Sidebar for navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["Speech Analysis", "Dashboard"])

# # Initialize session state for chunks and full_text
# if "chunks" not in st.session_state:
#     st.session_state["chunks"] = []
# if "full_text" not in st.session_state:
#     st.session_state["full_text"] = ""
# if "start_time" not in st.session_state:
#     st.session_state["start_time"] = None
# if "end_time" not in st.session_state:
#     st.session_state["end_time"] = None

# # Load FAISS vector store
# vector_store_path = "faiss_index"
# try:
#     vector_store = load_faiss_index(vector_store_path)
# except Exception as e:
#     st.error(f"Error loading FAISS index: {e}")
#     vector_store = None

# # Real-time speech-to-text and sentiment analysis
# def audio_to_text_and_analyze():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.write("Listening... Speak now!")
#         recognizer.adjust_for_ambient_noise(source)

#         text = ""
#         chunks = []

#         while True:
#             try:
#                 audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
#                 spoken_text = recognizer.recognize_google(audio)
#                 chunks.append(spoken_text)
#                 st.markdown(f"### You said: {spoken_text}")

#                 # Stop listening if a stop command is spoken
#                 if "stop the process" in spoken_text.lower():
#                     st.write("Stopping listening...")
#                     st.session_state["end_time"] = time.time()
#                     break

#                 # Sentiment analysis for the spoken text
#                 sentiment_score = analyze_sentiment(spoken_text)

#                 if sentiment_score > 0:
#                     st.markdown(f"**Sentiment:** <span style='color: green;'>Positive</span>", unsafe_allow_html=True)
#                 elif sentiment_score < 0:
#                     st.markdown(f"**Sentiment:** <span style='color: red;'>Negative</span>", unsafe_allow_html=True)
#                 else:
#                     st.markdown(f"**Sentiment:** <span style='color: yellow;'>Neutral</span>", unsafe_allow_html=True)

#                 # Check for objectionable content
#                 objection_solutions = []
#                 for obj in objections_data:
#                     if obj["objection"] in spoken_text.lower():
#                         objection_solutions.append(obj["solution"])

#                 if objection_solutions:
#                     st.markdown("**Objectionable Content Detected:**")
#                     for solution in objection_solutions:
#                         st.write(f"- {solution}")

#                 # Product recommendations using FAISS vector store
#                 if vector_store:
#                     related_data = search_faiss_index_with_threshold(
#                         query=spoken_text,
#                         vector_store=vector_store,
#                         similarity_threshold=0.6,
#                     )
#                     if related_data:
#                         st.markdown("**Related Products:**")
#                         for idx, doc in enumerate(related_data):
#                             unique_key = f"product_{idx + 1}_{uuid.uuid4()}"
#                             st.text_area(
#                                 label=f"Details for Product {idx + 1}",
#                                 value=doc.page_content,
#                                 height=100,
#                                 key=unique_key,
#                             )
#                 else:
#                     st.warning("FAISS vector store not loaded. Unable to provide product recommendations.")

#                 # Update session state with new data
#                 st.session_state["chunks"].extend(chunks)
#                 st.session_state["full_text"] = " ".join(st.session_state["chunks"])

#             except sr.UnknownValueError:
#                 st.write("Sorry, I could not understand the audio.")
#             except sr.RequestError as e:
#                 st.write(f"Could not request results; {e}")
#                 break
#             except sr.WaitTimeoutError:
#                 st.write("Listening timeout. Please speak again.")
#                 continue

#             # Real-time return of chunks and text
#             yield chunks, text.strip()


# if page == "Speech Analysis":
#     st.title("Real-Time Audio Sentiment Analysis and Product Recommendation")
#     # Real-time speech-to-text and sentiment analysis
#     st.subheader("Real-Time Speech Input")
#     if st.button("Start Listening"):
#         st.session_state["start_time"] = time.time()  # Start the conversation timer
#         with st.spinner("Listening..."):
#             for chunks, full_text in audio_to_text_and_analyze():
#                 pass  # Data is automatically updated in session state

# if page == "Dashboard":
#     st.title("Conversation Dashboard")

#     if st.session_state["start_time"] and st.session_state["end_time"]:
#         duration_seconds = int(st.session_state["end_time"] - st.session_state["start_time"])
#         hours, remainder = divmod(duration_seconds, 3600)
#         minutes, seconds = divmod(remainder, 60)
#         st.write(f"Total Conversation Duration: {hours}h {minutes}m {seconds}s")
#     else:
#         st.write("Conversation duration: Not available")

#     if st.session_state["chunks"]:
#         chunks = st.session_state["chunks"]
#         chunks = remove_duplicate_phrases(chunks)
#         sentiment_scores = [analyze_sentiment(chunk) for chunk in chunks]
#         sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
#         objectionable_words = []
#         product_recommendations = []

#         for chunk in chunks:
#             sentiment_score = analyze_sentiment(chunk)
#             if sentiment_score > 0:
#                 sentiment_counts["Positive"] += 1
#             elif sentiment_score < 0:
#                 sentiment_counts["Negative"] += 1
#             else:
#                 sentiment_counts["Neutral"] += 1
            
#             objections_found = [obj['objection'] for obj in objections_data if obj['objection'] in chunk.lower()]
#             objectionable_words.append(", ".join(objections_found) if objections_found else "None")
            
#             if vector_store:
#                 related_data = search_faiss_index_with_threshold(query=chunk, vector_store=vector_store,  similarity_threshold=0.6)
#                 product_recommendations.append(", ".join([doc.page_content for doc in related_data]) if related_data else "None")
#             else:
#                 product_recommendations.append("Vector store not available")

#         overall_sentiment = max(sentiment_counts, key=sentiment_counts.get)
#         sentiment_color = "green" if overall_sentiment == "Positive" else "red" if overall_sentiment == "Negative" else "yellow"
#         st.markdown(f"Overall Sentiment: <span style='color: {sentiment_color};'><b>{overall_sentiment}</b></span>", unsafe_allow_html=True)
#          # Summarize the conversation using Cohere
#         min_length = 250
#         full_text = " ".join(chunks)
#         padded_text = full_text + (" " * (min_length - len(full_text))) if len(full_text) < min_length else full_text
#         response = co.summarize(text=padded_text, length="short")
#         summary = response.summary.strip()

#         st.subheader("Summary of Conversation Transcript")
#         st.text_area("Conversation Text", summary, height=200)
#         st.subheader("Chunks and Sentiment Analysis Table")
#         data = [{
#             "Chunk": chunk,
#             "Sentiment": "Positive" if analyze_sentiment(chunk) > 0 else "Negative" if analyze_sentiment(chunk) < 0 else "Neutral",
#             "Objectionable Words": objectionable_words[idx],
#             "Product Recommendations": product_recommendations[idx]
#         } for idx, chunk in enumerate(chunks)]
#         st.dataframe(data, width=800, height=300)

#         st.subheader("Sentiment Distribution Pie Chart")
#         st.pyplot(create_pie_chart(sentiment_counts))

#         st.subheader("Sentiment Analysis Progression")
#         st.line_chart(sentiment_scores)


#     else:
#         st.warning("No conversation data available. Please analyze speech in the 'Speech Analysis' page first.")












import streamlit as st
import json
import time
from sentimentAnalysis import *
from rag import *
from pieChart import *
import cohere
import uuid
import speech_recognition as sr
from removeDuplicates import *
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
# load_dotenv()

# # Retrieve the API key from the environment
# cohere_api_key = os.getenv("COHERE_API_KEY")

# # Initialize the Cohere client
# co = cohere.Client(cohere_api_key)


# Initialize the Cohere client
co = cohere.Client("IT8QOLxK1JfYlN0vRwoCBmkjnvjqC0cXOOrlz7o1")

# Load the objections from JSON file
with open("objections.json", "r") as f:
    objections_data = json.load(f)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Speech Analysis", "Dashboard"])

# Initialize session state for chunks and timing
if "chunks" not in st.session_state:
    st.session_state["chunks"] = []
if "full_text" not in st.session_state:
    st.session_state["full_text"] = ""
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None
if "end_time" not in st.session_state:
    st.session_state["end_time"] = None

# Load FAISS vector store
vector_store_path = "faiss_index"
try:
    vector_store = load_faiss_index(vector_store_path)
except Exception as e:
    st.error(f"Error loading FAISS index: {e}")
    vector_store = None

# Real-time speech-to-text and sentiment analysis
def audio_to_text_and_analyze():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)

        chunks = []

        while True:
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                spoken_text = recognizer.recognize_google(audio)
                chunks.append(spoken_text)
                st.markdown(f"### You said: {spoken_text}")

                # Stop listening if a stop command is spoken
                if "stop the process" in spoken_text.lower():
                    st.write("Stopping listening...")
                    st.session_state["end_time"] = time.time()  # Set end time
                    break

                # Sentiment analysis for the spoken text
                sentiment_score = analyze_sentiment(spoken_text)

                if sentiment_score > 0:
                    st.markdown(f"**Sentiment:** <span style='color: green;'>Positive</span>", unsafe_allow_html=True)
                elif sentiment_score < 0:
                    st.markdown(f"**Sentiment:** <span style='color: red;'>Negative</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**Sentiment:** <span style='color: yellow;'>Neutral</span>", unsafe_allow_html=True)

                # Check for objectionable content
                objection_solutions = []
                for obj in objections_data:
                    if obj["objection"] in spoken_text.lower():
                        objection_solutions.append(obj["solution"])

                if objection_solutions:
                    st.markdown("**Objectionable Content Detected:**")
                    for solution in objection_solutions:
                        st.write(f"- {solution}")

                # Product recommendations using FAISS vector store
                if vector_store:
                    related_data = search_faiss_index_with_threshold(
                        query=spoken_text,
                        vector_store=vector_store,
                        similarity_threshold=0.6,
                    )
                    if related_data:
                        st.markdown("**Related Products:**")
                        for idx, doc in enumerate(related_data):
                            unique_key = f"product_{idx + 1}_{uuid.uuid4()}"
                            st.text_area(
                                label=f"Details for Product {idx + 1}",
                                value=doc.page_content,
                                height=100,
                                key=unique_key,
                            )
                else:
                    st.warning("FAISS vector store not loaded. Unable to provide product recommendations.")

                # Update session state with new data
                st.session_state["chunks"].extend(chunks)
                st.session_state["full_text"] = " ".join(st.session_state["chunks"])

            except sr.UnknownValueError:
                st.write("Sorry, I could not understand the audio.")
            except sr.RequestError as e:
                st.write(f"Could not request results; {e}")
                break
            except sr.WaitTimeoutError:
                st.write("Listening timeout. Please speak again.")
                continue

            # Real-time return of chunks and text
            yield chunks, st.session_state["full_text"]


if page == "Speech Analysis":
    st.title("Real-Time Audio Sentiment Analysis and Product Recommendation")
    st.subheader("Real-Time Speech Input")
    if st.button("Start Listening"):
        st.session_state["start_time"] = time.time()  # Start the conversation timer
        with st.spinner("Listening..."):
            for chunks, full_text in audio_to_text_and_analyze():
                pass  # Data is automatically updated in session state

if page == "Dashboard":
    st.title("Conversation Dashboard")

    if st.session_state["start_time"] and st.session_state["end_time"]:
        duration_seconds = int(st.session_state["end_time"] - st.session_state["start_time"])
        hours, remainder = divmod(duration_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        st.write(f"Total Conversation Duration: {hours}h {minutes}m {seconds}s")
    else:
        st.write("Conversation duration: Not available")

    if st.session_state["chunks"]:
        chunks = remove_duplicate_phrases(st.session_state["chunks"])
        sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
        objectionable_words = []
        product_recommendations = []

        for chunk in chunks:
            sentiment_score = analyze_sentiment(chunk)
            if sentiment_score > 0:
                sentiment_counts["Positive"] += 1
            elif sentiment_score < 0:
                sentiment_counts["Negative"] += 1
            else:
                sentiment_counts["Neutral"] += 1
            
            objections_found = [obj['objection'] for obj in objections_data if obj['objection'] in chunk.lower()]
            objectionable_words.append(", ".join(objections_found) if objections_found else "None")
            
            if vector_store:
                related_data = search_faiss_index_with_threshold(query=chunk, vector_store=vector_store, similarity_threshold=0.6)
                product_recommendations.append(", ".join([doc.page_content for doc in related_data]) if related_data else "None")
            else:
                product_recommendations.append("Vector store not available")

        overall_sentiment = max(sentiment_counts, key=sentiment_counts.get)
        sentiment_color = "green" if overall_sentiment == "Positive" else "red" if overall_sentiment == "Negative" else "yellow"
        st.markdown(f"Overall Sentiment: <span style='color: {sentiment_color};'><b>{overall_sentiment}</b></span>", unsafe_allow_html=True)

        # Summarize the conversation using Cohere
        min_length = 250
        full_text = " ".join(chunks)
        padded_text = full_text + (" " * (min_length - len(full_text))) if len(full_text) < min_length else full_text
        response = co.summarize(text=padded_text, length="short")
        summary = response.summary.strip()

        st.subheader("Summary of Conversation Transcript")
        st.text_area("Conversation Text", summary, height=200)

        st.subheader("Chunks and Sentiment Analysis Table")
        data = [{
            "Chunk": chunk,
            "Sentiment": "Positive" if analyze_sentiment(chunk) > 0 else "Negative" if analyze_sentiment(chunk) < 0 else "Neutral",
            "Objectionable Words": objectionable_words[idx],
            "Product Recommendations": product_recommendations[idx]
        } for idx, chunk in enumerate(chunks)]
        st.dataframe(data, width=800, height=300)

        st.subheader("Sentiment Distribution Pie Chart")
        st.pyplot(create_pie_chart(sentiment_counts))

        st.subheader("Sentiment Analysis Progression")
        st.line_chart([analyze_sentiment(chunk) for chunk in chunks])

    else:
        st.warning("No conversation data available. Please analyze speech in the 'Speech Analysis' page first.")
