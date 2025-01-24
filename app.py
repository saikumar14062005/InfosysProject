# import streamlit as st
# import json
# import time
# from sentimentAnalysis import *
# from rag import *
# from pieChart import *
# import cohere


# # Initialize the Cohere client
# co = cohere.Client("IT8QOLxK1JfYlN0vRwoCBmkjnvjqC0cXOOrlz7o1")

# # Load the objections from JSON file
# with open("objections.json", "r") as f:
#     objections_data = json.load(f)

# # Sidebar for navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["Speech Analysis", "Dashboard"])

# # Page 1: Real-Time Speech-to-Text and Sentiment Analysis
# if page == "Speech Analysis":
#     st.title("Real-Time Audio Sentiment Analysis and Product Recommendation")

#     # Check if previous session data exists
#     if "chunks" in st.session_state and "full_text" in st.session_state:
#         chunks = st.session_state["chunks"]
#         full_text = st.session_state["full_text"]
#     else:
#         chunks = []
#         full_text = ""

#     # Real-time speech-to-text
#     st.subheader("Real-Time Speech Input")
#     if st.button("Start Listening"):
#         with st.spinner("Listening... Speak into your microphone!"):
#             start_time = time.time()  # Start recording the duration
#             chunks, full_text = audio_to_text()  # Use your real-time audio-to-text function
#             end_time = time.time()  # End recording the duration

#         # Calculate conversation duration
#         duration = end_time - start_time
#         minutes, seconds = divmod(duration, 60)

#         # Save data to session state
#         st.session_state["chunks"] = chunks
#         st.session_state["full_text"] = full_text
#         st.session_state["duration"] = (minutes, seconds)

#     # Display the full transcribed text
#     if full_text:
#         st.subheader("Transcribed Full Text")
#         st.text_area("Audio Transcript", full_text, height=200)

#     # Sentiment and Chunk Analysis
#     if chunks:
#         st.subheader("Chunk Analysis and Recommendations")
#         sentiment_scores = []
#         product_keywords = set()  # To store detected product-related keywords

#         for i, chunk in enumerate(chunks):
#             chunk_sentiment = analyze_sentiment(chunk)
#             sentiment_scores.append(chunk_sentiment)
#             st.markdown(f"### Chunk {i+1}")
#             st.write(chunk)

#             # Display sentiment with color coding
#             if chunk_sentiment > 0:
#                 st.markdown(f"**Sentiment:** <span style='color: green;'>Positive</span>", unsafe_allow_html=True)
#             elif chunk_sentiment < 0:
#                 st.markdown(f"**Sentiment:** <span style='color: red;'>Negative</span>", unsafe_allow_html=True)
#             else:
#                 st.markdown(f"**Sentiment:** <span style='color: yellow;'>Neutral</span>", unsafe_allow_html=True)

#             # Check for objectionable words
#             objection_solutions = []
#             for obj in objections_data:
#                 if obj["objection"] in chunk.lower():
#                     objection_solutions.append(obj["solution"])

#             if objection_solutions:
#                 st.markdown("**Objectionable Content Detected:**")
#                 for solution in objection_solutions:
#                     st.write(f"- {solution}")

#             # Find related data
#             related_data = search_data(chunk, data, data_embeddings)
#             if related_data:
#                 st.markdown("**Related Products:**")
#                 for item in related_data:
#                     st.write(f"- {item}")
#             else:
#                 st.write("No related products found.")

#         # Save session data
#         st.session_state["sentiment_scores"] = sentiment_scores

# elif page == "Dashboard":
#     st.title("Conversation Dashboard")

#     if "sentiment_scores" in st.session_state:
#         sentiment_scores = st.session_state["sentiment_scores"]
#         duration = st.session_state["duration"]
#         full_text = st.session_state["full_text"]
#         chunks = st.session_state["chunks"]

#         # Summarize the full text using Cohere
#         response = co.summarize(
#             text=full_text,
#             length="medium"  # Options: "short", "medium", "long"
#         )
#         summary = response.summary

#         col1, col2 = st.columns(2)

#         # Sentiment Summary
#         with col1:
#             st.markdown("### Sentiment Summary")
#             overall_sentiment = "Positive" if sum(sentiment_scores) > 0 else "Negative" if sum(sentiment_scores) < 0 else "Neutral"
#             sentiment_color = "green" if overall_sentiment == "Positive" else "red" if overall_sentiment == "Negative" else "yellow"
#             st.markdown(f"Overall Sentiment: <span style='color: {sentiment_color};'><b>{overall_sentiment}</b></span>", unsafe_allow_html=True)

#         # Conversation Duration
#         with col2:
#             st.markdown("### Conversation Duration")
#             minutes, seconds = duration
#             st.write(f"**{int(minutes)} minutes and {int(seconds)} seconds**")

#         # Full Conversation Summary
#         st.subheader("Summary of Conversation Transcript")
#         st.text_area("Conversation Text", summary, height=200)

#         # Table of Sentiments and Chunks
#         st.subheader("Chunks and Sentiment Analysis Table")

#         # Map sentiment scores to their respective labels
#         sentiment_labels = [
#             "Positive" if score > 0 else "Negative" if score < 0 else "Neutral" 
#             for score in sentiment_scores
#         ]

#         # Create a table with chunks and sentiment labels
#         data = [{"Chunk": chunks[i], "Sentiment": sentiment_labels[i]} for i in range(len(chunks))]

#         # Display the table
#         sentiment_table = st.dataframe(data, width=800, height=300)


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


# # Initialize the Cohere client
# co = cohere.Client("IT8QOLxK1JfYlN0vRwoCBmkjnvjqC0cXOOrlz7o1")

# # Load the objections from JSON file
# with open("objections.json", "r") as f:
#     objections_data = json.load(f)

# # Sidebar for navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["Speech Analysis", "Dashboard"])

# # Page 1: Real-Time Speech-to-Text and Sentiment Analysis
# if page == "Speech Analysis":
#     st.title("Real-Time Audio Sentiment Analysis and Product Recommendation")

#     # Check if previous session data exists
#     if "chunks" in st.session_state and "full_text" in st.session_state:
#         chunks = st.session_state["chunks"]
#         full_text = st.session_state["full_text"]
#     else:
#         chunks = []
#         full_text = ""

#     # Real-time speech-to-text
#     st.subheader("Real-Time Speech Input")
#     if st.button("Start Listening"):
#         with st.spinner("Listening... Speak into your microphone!"):
#             start_time = time.time()  # Start recording the duration
#             chunks, full_text = audio_to_text()  # Use your real-time audio-to-text function
#             end_time = time.time()  # End recording the duration

#         # Calculate conversation duration
#         duration = end_time - start_time
#         minutes, seconds = divmod(duration, 60)

#         # Save data to session state
#         st.session_state["chunks"] = chunks
#         st.session_state["full_text"] = full_text
#         st.session_state["duration"] = (minutes, seconds)

#     # Display the full transcribed text
#     if full_text:
#         st.subheader("Transcribed Full Text")
#         st.text_area("Audio Transcript", full_text, height=200)

#     # Sentiment and Chunk Analysis
#     if chunks:
#         st.subheader("Chunk Analysis and Recommendations")
#         sentiment_scores = []
#         product_keywords = set()  # To store detected product-related keywords

#         for i, chunk in enumerate(chunks):
#             chunk_sentiment = analyze_sentiment(chunk)
#             sentiment_scores.append(chunk_sentiment)
#             st.markdown(f"### Chunk {i+1}")
#             st.write(chunk)

#             # Display sentiment with color coding
#             if chunk_sentiment > 0:
#                 st.markdown(f"**Sentiment:** <span style='color: green;'>Positive</span>", unsafe_allow_html=True)
#             elif chunk_sentiment < 0:
#                 st.markdown(f"**Sentiment:** <span style='color: red;'>Negative</span>", unsafe_allow_html=True)
#             else:
#                 st.markdown(f"**Sentiment:** <span style='color: yellow;'>Neutral</span>", unsafe_allow_html=True)

#             # Check for objectionable words
#             objection_solutions = []
#             for obj in objections_data:
#                 if obj["objection"] in chunk.lower():
#                     objection_solutions.append(obj["solution"])

#             if objection_solutions:
#                 st.markdown("**Objectionable Content Detected:**")
#                 for solution in objection_solutions:
#                     st.write(f"- {solution}")

#             # Find related data
#             related_data = search_data(chunk, data, data_embeddings)
#            # Inside the loop for related products
#             if related_data:
#                 st.markdown("**Related Products:**")
#                 # Vertically scrollable container
#                 with st.container():
#                     for idx, item in enumerate(related_data):
#                         st.markdown(f"**Product {idx + 1}**")
#                         st.text_area(
#                             label=f"Details for Product {idx + 1}",
#                             value=item,
#                             height=100,
#                             key=f"product_{idx + 1}",  # Increment the key
#                         )

#             else:
#                 st.write("No related products found.")

#         # Save session data
#         st.session_state["sentiment_scores"] = sentiment_scores

# elif page == "Dashboard":
#     st.title("Conversation Dashboard")

#     if "sentiment_scores" in st.session_state:
#         sentiment_scores = st.session_state["sentiment_scores"]
#         duration = st.session_state["duration"]
#         full_text = st.session_state["full_text"]
#         chunks = st.session_state["chunks"]

#         # Summarize the full text using Cohere
#         response = co.summarize(
#             text=full_text,
#             length="medium"  # Options: "short", "medium", "long"
#         )
#         summary = response.summary

#         col1, col2 = st.columns(2)

#         # Sentiment Summary
#         with col1:
#             st.markdown("### Sentiment Summary")
#             overall_sentiment = "Positive" if sum(sentiment_scores) > 0 else "Negative" if sum(sentiment_scores) < 0 else "Neutral"
#             sentiment_color = "green" if overall_sentiment == "Positive" else "red" if overall_sentiment == "Negative" else "yellow"
#             st.markdown(f"Overall Sentiment: <span style='color: {sentiment_color};'><b>{overall_sentiment}</b></span>", unsafe_allow_html=True)

#         # Conversation Duration
#         with col2:
#             st.markdown("### Conversation Duration")
#             minutes, seconds = duration
#             st.write(f"**{int(minutes)} minutes and {int(seconds)} seconds**")

#         # Full Conversation Summary
#         st.subheader("Summary of Conversation Transcript")
#         st.text_area("Conversation Text", summary, height=200)

#         # Table of Sentiments and Chunks
#         st.subheader("Chunks and Sentiment Analysis Table")

#         # Map sentiment scores to their respective labels
#         sentiment_labels = [
#             "Positive" if score > 0 else "Negative" if score < 0 else "Neutral" 
#             for score in sentiment_scores
#         ]

#         # Create a table with chunks and sentiment labels
#         data = [{"Chunk": chunks[i], "Sentiment": sentiment_labels[i]} for i in range(len(chunks))]

#         # Display the table
#         sentiment_table = st.dataframe(data, width=800, height=300)

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


# Initialize the Cohere client
co = cohere.Client("IT8QOLxK1JfYlN0vRwoCBmkjnvjqC0cXOOrlz7o1")

# Load the objections from JSON file
with open("objections.json", "r") as f:
    objections_data = json.load(f)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Speech Analysis", "Dashboard"])

# Page 1: Real-Time Speech-to-Text and Sentiment Analysis
if page == "Speech Analysis":
    st.title("Real-Time Audio Sentiment Analysis and Product Recommendation")

    # Check if previous session data exists
    if "chunks" in st.session_state and "full_text" in st.session_state:
        chunks = st.session_state["chunks"]
        full_text = st.session_state["full_text"]
    else:
        chunks = []
        full_text = ""

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

        # Save data to session state
        st.session_state["chunks"] = chunks
        st.session_state["full_text"] = full_text
        st.session_state["duration"] = (minutes, seconds)

    # Display the full transcribed text
    if full_text:
        st.subheader("Transcribed Full Text")
        st.text_area("Audio Transcript", full_text, height=200)

    # Sentiment and Chunk Analysis
    if chunks:
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
                with st.container():
                    for idx, item in enumerate(related_data):
                        # Generate a unique key for each text area
                        unique_key = f"product_{idx + 1}_{uuid.uuid4()}"  # Add a unique identifier using uuid4
                        st.markdown(f"**Product {idx + 1}**")
                        st.text_area(
                            label=f"Details for Product {idx + 1}",
                            value=item,
                            height=100,
                            key=unique_key,  # Use the generated unique key
                        )
            else:
                st.write("No related products found.")

        # Save session data
        st.session_state["sentiment_scores"] = sentiment_scores

elif page == "Dashboard":
    st.title("Conversation Dashboard")

    if "sentiment_scores" in st.session_state:
        sentiment_scores = st.session_state["sentiment_scores"]
        duration = st.session_state["duration"]
        full_text = st.session_state["full_text"]
        chunks = st.session_state["chunks"]

        # Summarize the full text using Cohere
        response = co.summarize(
            text=full_text,
            length="medium"  # Options: "short", "medium", "long"
        )
        summary = response.summary

        col1, col2 = st.columns(2)

        # Sentiment Summary
        with col1:
            st.markdown("### Sentiment Summary")
            overall_sentiment = "Positive" if sum(sentiment_scores) > 0 else "Negative" if sum(sentiment_scores) < 0 else "Neutral"
            sentiment_color = "green" if overall_sentiment == "Positive" else "red" if overall_sentiment == "Negative" else "yellow"
            st.markdown(f"Overall Sentiment: <span style='color: {sentiment_color};'><b>{overall_sentiment}</b></span>", unsafe_allow_html=True)

        # Conversation Duration
        with col2:
            st.markdown("### Conversation Duration")
            minutes, seconds = duration
            st.write(f"**{int(minutes)} minutes and {int(seconds)} seconds**")

        # Full Conversation Summary
        st.subheader("Summary of Conversation Transcript")
        st.text_area("Conversation Text", summary, height=200)

        # Table of Sentiments and Chunks
        st.subheader("Chunks and Sentiment Analysis Table")

        # Map sentiment scores to their respective labels
        sentiment_labels = [
            "Positive" if score > 0 else "Negative" if score < 0 else "Neutral" 
            for score in sentiment_scores
        ]

        # Create a table with chunks and sentiment labels
        data = [{"Chunk": chunks[i], "Sentiment": sentiment_labels[i]} for i in range(len(chunks))]

        # Display the table
        sentiment_table = st.dataframe(data, width=800, height=300)

        # Sentiment Distribution
        st.subheader("Sentiment Distribution")
        sentiment_counts = {
            "Positive": len([s for s in sentiment_scores if s > 0]),
            "Negative": len([s for s in sentiment_scores if s < 0]),
            "Neutral": len([s for s in sentiment_scores if s == 0])
        }

       
        
        # Sentiment Analysis Graph
        st.subheader("Sentiment Analysis Progression")
        st.line_chart(sentiment_scores)  # Streamlit's built-in line chart

         # Pie Chart Visualization
        st.markdown("### Sentiment Distribution Pie Chart")
        st.pyplot(create_pie_chart(sentiment_counts))
    else:
        st.warning("No conversation data available. Please analyze speech in the 'Speech Analysis' page first.")










