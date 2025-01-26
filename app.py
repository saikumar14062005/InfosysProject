

# import streamlit as st
# import json
# import time
# from sentimentAnalysis import *
# from rag import *
# from pieChart import *
# import cohere
# import uuid
# import speech_recognition as sr

# # Initialize the Cohere client
# co = cohere.Client("IT8QOLxK1JfYlN0vRwoCBmkjnvjqC0cXOOrlz7o1")

# # Load the objections from JSON file
# with open("objections.json", "r") as f:
#     objections_data = json.load(f)

# # Sidebar for navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["Speech Analysis", "Dashboard"])

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

#                 # Product recommendations based on related data
#                 related_data = search_data(spoken_text, data, data_embeddings)
#                 if related_data:
#                     st.markdown("**Related Products:**")
#                     for idx, item in enumerate(related_data):
#                         unique_key = f"product_{idx + 1}_{uuid.uuid4()}"
#                         st.text_area(
#                             label=f"Details for Product {idx + 1}",
#                             value=item,
#                             height=100,
#                             key=unique_key,
#                         )

#                 # Stop listening if a stop command is spoken
#                 if "stop the process" in spoken_text.lower():
#                     st.write("Stopping listening...")
#                     break

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

#     # Check if previous session data exists
#     if "chunks" not in st.session_state:
#         st.session_state["chunks"] = []

#     # Real-time speech-to-text and sentiment analysis
#     st.subheader("Real-Time Speech Input")
#     if st.button("Start Listening"):
#         with st.spinner("Listening..."):
#             for chunks, full_text in audio_to_text_and_analyze():
#                 st.session_state["chunks"] = chunks
#                 st.session_state["full_text"] = full_text

# elif page == "Dashboard":
#     st.title("Conversation Dashboard")

#     if "chunks" in st.session_state:
#         chunks = st.session_state["chunks"]
#         full_text = " ".join(chunks)

#         # Ensure the text meets the 250-character requirement
#         min_length = 250
#         if len(full_text) < min_length:
#             # Add padding to meet the length requirement
#             padded_text = full_text + (" " * (min_length - len(full_text)))
#         else:
#             padded_text = full_text

#         # Summarize the padded text using Cohere
#         response = co.summarize(
#             text=padded_text,
#             length="medium"
#         )
#         summary = response.summary.strip()  # Clean unnecessary padding or whitespace

#         # Remove unnecessary padding from the summary
#         if len(full_text) < min_length:
#             summary = summary.replace((" " * (min_length - len(full_text))), "").strip()

#         col1, col2 = st.columns(2)

#         # Sentiment Summary
#         with col1:
#             st.markdown("### Sentiment Summary")
#             sentiment_scores = [analyze_sentiment(chunk) for chunk in chunks]
#             overall_sentiment = "Positive" if sum(sentiment_scores) > 0 else "Negative" if sum(sentiment_scores) < 0 else "Neutral"
#             sentiment_color = "green" if overall_sentiment == "Positive" else "red" if overall_sentiment == "Negative" else "yellow"
#             st.markdown(f"Overall Sentiment: <span style='color: {sentiment_color};'><b>{overall_sentiment}</b></span>", unsafe_allow_html=True)

#         # Full Conversation Summary
#         st.subheader("Summary of Conversation Transcript")
#         st.text_area("Conversation Text", summary, height=200)

#         # Chunks and Sentiments
#         st.subheader("Chunks and Sentiment Analysis Table")
#         data = [{"Chunk": chunk, "Sentiment": "Positive" if analyze_sentiment(chunk) > 0 else "Negative" if analyze_sentiment(chunk) < 0 else "Neutral"} for chunk in chunks]
#         st.dataframe(data, width=800, height=300)

#         # Sentiment Distribution
#         st.subheader("Sentiment Distribution")
#         sentiment_counts = {
#             "Positive": len([s for s in sentiment_scores if s > 0]),
#             "Negative": len([s for s in sentiment_scores if s < 0]),
#             "Neutral": len([s for s in sentiment_scores if s == 0])
#         }

#         # Pie Chart Visualization
#         st.markdown("### Sentiment Distribution Pie Chart")
#         st.pyplot(create_pie_chart(sentiment_counts))

#         # Sentiment Analysis Graph
#         st.subheader("Sentiment Analysis Progression")
#         st.line_chart(sentiment_scores)  # Streamlit's built-in line chart

#     else:
#         st.warning("No conversation data available. Please analyze speech in the 'Speech Analysis' page first.")









# import streamlit as st
# import json
# import time
# from sentimentAnalysis import *
# from rag import *
# from pieChart import *
# import cohere
# import uuid
# import speech_recognition as sr

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

#                 # Product recommendations based on related data
#                 related_data = search_data(spoken_text, data, data_embeddings)
#                 # related_data = search_faiss_index_with_threshold(spoken_text, vector_store, top_k=5, similarity_threshold=0.6)
#                 if related_data:
#                     st.markdown("**Related Products:**")
#                     for idx, item in enumerate(related_data):
#                         unique_key = f"product_{idx + 1}_{uuid.uuid4()}"
#                         st.text_area(
#                             label=f"Details for Product {idx + 1}",
#                             value=item,
#                             height=100,
#                             key=unique_key,
#                         )

#                 # Update session state with new data
#                 st.session_state["chunks"].extend(chunks)
#                 st.session_state["full_text"] = " ".join(st.session_state["chunks"])

#                 # Stop listening if a stop command is spoken
#                 if "stop the process" in spoken_text.lower():
#                     st.write("Stopping listening...")
#                     break

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

#     # Display previous session data if available
#     if st.session_state["chunks"]:
#         st.subheader("Previous Session Data")
#         st.text_area("Transcript", value=" ".join(st.session_state["chunks"]), height=200)

#     # Real-time speech-to-text and sentiment analysis
#     st.subheader("Real-Time Speech Input")
#     if st.button("Start Listening"):
#         with st.spinner("Listening..."):
#             for chunks, full_text in audio_to_text_and_analyze():
#                 pass  # Data is automatically updated in session state


# elif page == "Dashboard":
#     st.title("Conversation Dashboard")

#     if st.session_state["chunks"]:
#         chunks = st.session_state["chunks"]
#         full_text = st.session_state["full_text"]

#         # Ensure the text meets the 250-character requirement
#         min_length = 250
#         if len(full_text) < min_length:
#             # Add padding to meet the length requirement
#             padded_text = full_text + (" " * (min_length - len(full_text)))
#         else:
#             padded_text = full_text

#         # Summarize the padded text using Cohere
#         response = co.summarize(
#             text=padded_text,
#             length="medium"
#         )
#         summary = response.summary.strip()  # Clean unnecessary padding or whitespace

#         # Remove unnecessary padding from the summary
#         if len(full_text) < min_length:
#             summary = summary.replace((" " * (min_length - len(full_text))), "").strip()

#         col1, col2 = st.columns(2)

#         # Sentiment Summary
#         with col1:
#             st.markdown("### Sentiment Summary")
#             sentiment_scores = [analyze_sentiment(chunk) for chunk in chunks]
#             overall_sentiment = "Positive" if sum(sentiment_scores) > 0 else "Negative" if sum(sentiment_scores) < 0 else "Neutral"
#             sentiment_color = "green" if overall_sentiment == "Positive" else "red" if overall_sentiment == "Negative" else "yellow"
#             st.markdown(f"Overall Sentiment: <span style='color: {sentiment_color};'><b>{overall_sentiment}</b></span>", unsafe_allow_html=True)

#         # Full Conversation Summary
#         st.subheader("Summary of Conversation Transcript")
#         st.text_area("Conversation Text", summary, height=200)

#         # Chunks and Sentiments
#         st.subheader("Chunks and Sentiment Analysis Table")
#         data = [{"Chunk": chunk, "Sentiment": "Positive" if analyze_sentiment(chunk) > 0 else "Negative" if analyze_sentiment(chunk) < 0 else "Neutral"} for chunk in chunks]
#         st.dataframe(data, width=800, height=300)

#         # Sentiment Distribution
#         st.subheader("Sentiment Distribution")
#         sentiment_counts = {
#             "Positive": len([s for s in sentiment_scores if s > 0]),
#             "Negative": len([s for s in sentiment_scores if s < 0]),
#             "Neutral": len([s for s in sentiment_scores if s == 0])
#         }

#         # Pie Chart Visualization
#         st.markdown("### Sentiment Distribution Pie Chart")
#         st.pyplot(create_pie_chart(sentiment_counts))

#         # Sentiment Analysis Graph
#         st.subheader("Sentiment Analysis Progression")
#         st.line_chart(sentiment_scores)  # Streamlit's built-in line chart

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

# Initialize the Cohere client
co = cohere.Client("IT8QOLxK1JfYlN0vRwoCBmkjnvjqC0cXOOrlz7o1")

# Load the objections from JSON file
with open("objections.json", "r") as f:
    objections_data = json.load(f)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Speech Analysis", "Dashboard"])

# Initialize session state for chunks and full_text
if "chunks" not in st.session_state:
    st.session_state["chunks"] = []
if "full_text" not in st.session_state:
    st.session_state["full_text"] = ""

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

        text = ""
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
                        top_k=5,
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

                # # Stop listening if a stop command is spoken
                # if "stop the process" in spoken_text.lower():
                #     st.write("Stopping listening...")
                #     break

            except sr.UnknownValueError:
                st.write("Sorry, I could not understand the audio.")
            except sr.RequestError as e:
                st.write(f"Could not request results; {e}")
                break
            except sr.WaitTimeoutError:
                st.write("Listening timeout. Please speak again.")
                continue

            # Real-time return of chunks and text
            yield chunks, text.strip()


if page == "Speech Analysis":
    st.title("Real-Time Audio Sentiment Analysis and Product Recommendation")

    # Display previous session data if available
    if st.session_state["chunks"]:
        st.subheader("Previous Session Data")
        st.text_area("Transcript", value=" ".join(st.session_state["chunks"]), height=200)

    # Real-time speech-to-text and sentiment analysis
    st.subheader("Real-Time Speech Input")
    if st.button("Start Listening"):
        with st.spinner("Listening..."):
            for chunks, full_text in audio_to_text_and_analyze():
                pass  # Data is automatically updated in session state


elif page == "Dashboard":
    st.title("Conversation Dashboard")

    if st.session_state["chunks"]:
        chunks = st.session_state["chunks"]
        full_text = st.session_state["full_text"]

        # Ensure the text meets the 250-character requirement
        min_length = 250
        if len(full_text) < min_length:
            # Add padding to meet the length requirement
            padded_text = full_text + (" " * (min_length - len(full_text)))
        else:
            padded_text = full_text

        # Summarize the padded text using Cohere
        response = co.summarize(
            text=padded_text,
            length="medium"
        )
        summary = response.summary.strip()  # Clean unnecessary padding or whitespace

        # Remove unnecessary padding from the summary
        if len(full_text) < min_length:
            summary = summary.replace((" " * (min_length - len(full_text))), "").strip()

        col1, col2 = st.columns(2)

        # Sentiment Summary
        with col1:
            st.markdown("### Sentiment Summary")
            sentiment_scores = [analyze_sentiment(chunk) for chunk in chunks]
            overall_sentiment = "Positive" if sum(sentiment_scores) > 0 else "Negative" if sum(sentiment_scores) < 0 else "Neutral"
            sentiment_color = "green" if overall_sentiment == "Positive" else "red" if overall_sentiment == "Negative" else "yellow"
            st.markdown(f"Overall Sentiment: <span style='color: {sentiment_color};'><b>{overall_sentiment}</b></span>", unsafe_allow_html=True)

        # Full Conversation Summary
        st.subheader("Summary of Conversation Transcript")
        st.text_area("Conversation Text", summary, height=200)

        # Chunks and Sentiments
        st.subheader("Chunks and Sentiment Analysis Table")
        data = [{"Chunk": chunk, "Sentiment": "Positive" if analyze_sentiment(chunk) > 0 else "Negative" if analyze_sentiment(chunk) < 0 else "Neutral"} for chunk in chunks]
        st.dataframe(data, width=800, height=300)

        # Sentiment Distribution
        st.subheader("Sentiment Distribution")
        sentiment_counts = {
            "Positive": len([s for s in sentiment_scores if s > 0]),
            "Negative": len([s for s in sentiment_scores if s < 0]),
            "Neutral": len([s for s in sentiment_scores if s == 0])
        }

        # Pie Chart Visualization
        st.markdown("### Sentiment Distribution Pie Chart")
        st.pyplot(create_pie_chart(sentiment_counts))

        # Sentiment Analysis Graph
        st.subheader("Sentiment Analysis Progression")
        st.line_chart(sentiment_scores)  # Streamlit's built-in line chart

    else:
        st.warning("No conversation data available. Please analyze speech in the 'Speech Analysis' page first.")
