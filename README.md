# Real-Time AI Sales Call Assistant for Enhanced Conversation Strategies
The **Real-Time Audio Sentiment Analysis and Product Recommendation** Application leverages cutting-edge technology to transform how businesses interact with their customers through voice.
This innovative application takes audio input from users, processes it by dividing it into smaller chunks, and analyzes the sentiment conveyed in each segment.
Based on the analysis, the system recommends relevant products in real-time to address user needs effectively.

🚀 Features  

🎤 **Audio Sentiment Analysis**: Breaks down voice input into segments, analyzing each for emotional tone and identifying associated products.  
🛒 **Personalized Product Recommendations**: Recommends products based on user sentiment (e.g., budget-friendly options for price dissatisfaction).  
🤖 **Interactive Object Handling**: Engages users conversationally (e.g., responding to "Too expensive" with alternative suggestions).  
📊 **Dashboard for Insights**: Provides a visual summary of audio input, including a table of segments with sentiment and recommendations, plus overall sentiment trends and key insights.  

## 🚀 Installation  

Follow these steps to set up and run the **InfosysProject** on your local machine.  

### Prerequisites  
Make sure you have the following installed:  
- 🐍 Python 3.10
- 📦 Required dependencies (see `requirements.txt`)  


### Steps to Install  

1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/your-username/InfosysProject.git
cd InfosysProject

```
2️⃣  **Add Environment Family**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

```

3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

4️⃣ **Set Up Environment Variables**

Create a .env file in the root directory.
Add required API keys, database credentials, or any configuration details.

5️⃣ **Run the Application**
```bash
python3 app.py 
```
## 🚀 Usage  

- **Real-Time Speech Audio 🎤**  
  The app processes live speech input and splits it into smaller chunks.  

- **Sentiment Analysis 😃😐😢**  
  Each chunk is analyzed for emotion (positive, neutral, negative).  

- **Product Recommendation 🛒**  
  The system suggests relevant products based on sentiment.  

- **Interactive Dashboard 📊**  
  Users can view sentiment trends and product suggestions visually.

## 📂 Project Structure  
  
audio-sentiment-analysis/

├── app.py

├── flipkartproducts.csv

├── objections.json

├── pieChart.py

├── rag.py

├── removeDuplicates.py

├── requirements.txt

├── sentimentAnalysis.py

└── README.md

### 📌 **File Descriptions**  

- **app.py**: The main application file.  
- **flipkartproducts.csv**: Contains product data for recommendations.  
- **objections.json**: Stores predefined objections and responses for interactive handling.  
- **pieChart.py**: Handles visualization of sentiment analysis results.  
- **rag.py**: Implements retrieval-augmented generation (RAG) techniques.  
- **removeDuplicates.py**: Cleans and filters duplicate records from datasets.  
- **requirements.txt**: Lists all the project dependencies.  
- **sentimentAnalysis.py**: Performs sentiment analysis on processed audio data.

  🤝 **Contributing**
  
We welcome contributions! Follow these steps to contribute:

1.Fork the repository 📌

2.Create a new branch

      git checkout -b feature-branch

3.Make your changes ✨

4.Commit your changes

      git commit -m "Added new feature"

5.Push to the branch 

      git push origin feature-branch

6.Submit a Pull Request 🚀

💡 **Acknowledgments**

Special thanks to Infosys Springboard and the Open Source Community for their support!
