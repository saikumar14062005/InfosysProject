# import streamlit as st
# import json
# from app import *
# from rag import *

# # Load the objections from JSON file
# with open("objections.json", "r") as f:
#     objections_data = json.load(f)

# # Streamlit app title
# st.title("Audio Sentiment Analysis and Product Recommendation")

# # Option to choose input method
# input_method = st.radio(
#     "Choose input method:",
#     ("Upload Audio File", "Real-Time Speech")
# )

# if input_method == "Upload Audio File":
#     # File uploader for audio file
#     uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "aac"])

#     if uploaded_file is not None:
#         # Convert audio to text
#         with st.spinner("Processing the audio file..."):
#             chunks, full_text = audio_to_text(uploaded_file)

#         # Display the full transcribed text
#         st.subheader("Transcribed Full Text")
#         st.text_area("Audio Transcript", full_text, height=200)

#         # Iterate through chunks for sentiment analysis
#         st.subheader("Chunk Analysis and Recommendations")
#         for i, chunk in enumerate(chunks):
#             chunk_sentiment = analyze_sentiment(chunk)
#             st.markdown(f"### Chunk {i+1}")
#             st.write(chunk)
#             st.write(f"**Sentiment**: {chunk_sentiment}")

#             # Check for objectionable words
#             objection_solutions = []
#             for obj in objections_data:
#                 if obj["objection"] in chunk.lower():
#                     objection_solutions.append(obj["solution"])
            
#             if objection_solutions:
#                 st.markdown("**Objectionable Content Detected**:")
#                 for solution in objection_solutions:
#                     st.write(f"- {solution}")

#             # Find related data
#             related_data = search_data(chunk, data, data_embeddings)
#             if related_data:
#                 st.markdown("**Related Products**:")
#                 for item in related_data:
#                     st.write(f"- {item}")
#             else:
#                 st.write("No related products found.")

# elif input_method == "Real-Time Speech":
#     # Real-time speech-to-text
#     st.subheader("Real-Time Speech Input")
#     if st.button("Start Listening"):
#         with st.spinner("Listening... Speak into your microphone!"):
#             chunks, full_text = audio_to_text()  # Use your real-time audio-to-text function

#         # Display the full transcribed text
#         st.subheader("Transcribed Full Text")
#         st.text_area("Audio Transcript", full_text, height=200)

#         # Iterate through chunks for sentiment analysis
#         st.subheader("Chunk Analysis and Recommendations")
#         for i, chunk in enumerate(chunks):
#             chunk_sentiment = analyze_sentiment(chunk)
#             st.markdown(f"### Chunk {i+1}")
#             st.write(chunk)
#             st.write(f"**Sentiment**: {chunk_sentiment}")

#             # Check for objectionable words
#             objection_solutions = []
#             for obj in objections_data:
#                 if obj["objection"] in chunk.lower():
#                     objection_solutions.append(obj["solution"])
            
#             if objection_solutions:
#                 st.markdown("**Objectionable Content Detected**:")
#                 for solution in objection_solutions:
#                     st.write(f"- {solution}")

#             # Find related data
#             related_data = search_data(chunk, data, data_embeddings)
#             if related_data:
#                 st.markdown("**Related Products**:")
#                 for item in related_data:
#                     st.write(f"- {item}")
#             else:
#                 st.write("No related products found.")



import streamlit as st
import json
import time
from app import *
from rag import *

# Load the objections from JSON file
with open("objections.json", "r") as f:
    objections_data = json.load(f)

# Streamlit app title
st.title("Real-Time Audio Sentiment Analysis and Product Recommendation")

# Real-time speech-to-text
st.subheader("Real-Time Speech Input")
if st.button("Start Listening"):
    with st.spinner("Listening... Speak into your microphone!"):
        start_time = time.time()  # Start recording the duration
        chunks, full_text = audio_to_text()  # Use your real-time audio-to-text function
        end_time = time.time()  # End recording the duration

    # Calculate conversation duration
    duration = end_time - start_time
    minutes, seconds = divmod(duration, 60)

    # Display the full transcribed text
    st.subheader("Transcribed Full Text")
    st.text_area("Audio Transcript", full_text, height=200)

    # Sentiment and Chunk Analysis
    st.subheader("Chunk Analysis and Recommendations")
    sentiment_scores = []
    product_keywords = set()  # To store detected product-related keywords

    for i, chunk in enumerate(chunks):
        chunk_sentiment = analyze_sentiment(chunk)
        sentiment_scores.append(chunk_sentiment)
        st.markdown(f"### Chunk {i+1}")
        st.write(chunk)

        # Display sentiment with color coding
        if chunk_sentiment > 0:
            st.markdown(f"**Sentiment:** <span style='color: green;'>Positive</span>", unsafe_allow_html=True)
        elif chunk_sentiment < 0:
            st.markdown(f"**Sentiment:** <span style='color: red;'>Negative</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"**Sentiment:** <span style='color: yellow;'>Neutral</span>", unsafe_allow_html=True)

        # Check for objectionable words
        objection_solutions = []
        for obj in objections_data:
            if obj["objection"] in chunk.lower():
                objection_solutions.append(obj["solution"])
        
        if objection_solutions:
            st.markdown("**Objectionable Content Detected:**")
            for solution in objection_solutions:
                st.write(f"- {solution}")

        # Find related data
        related_data = search_data(chunk, data, data_embeddings)
        if related_data:
            st.markdown("**Related Products:**")
            for item in related_data:
                st.write(f"- {item}")
                # product_keywords.add(item)  # Highlight detected product keywords
        else:
            st.write("No related products found.")

    # Dashboard Summary
    st.subheader("Conversation Dashboard")
    col1, col2= st.columns(2)

    # Sentiment Summary
    with col1:
        st.markdown("### Sentiment Summary")
        overall_sentiment = "Positive" if sum(sentiment_scores) > 0 else "Negative" if sum(sentiment_scores) < 0 else "Neutral"
        sentiment_color = "green" if overall_sentiment == "Positive" else "red" if overall_sentiment == "Negative" else "yellow"
        st.markdown(f"Overall Sentiment: <span style='color: {sentiment_color};'><b>{overall_sentiment}</b></span>", unsafe_allow_html=True)

    # Conversation Duration
    with col2:
        st.markdown("### Conversation Duration")
        st.write(f"**{int(minutes)} minutes and {int(seconds)} seconds**")

  

    # Full Conversation
    st.subheader("Full Conversation Transcript")
    st.text_area("Conversation Text", full_text, height=200)

