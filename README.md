# 📦 Amazon Review Analysis with Streamlit


This project is a web app built using Streamlit that performs sentiment analysis on Amazon product reviews. It allows users to:

Search for Amazon products

Analyze review sentiments using a pre-trained ML model (SVM)

View insights like sentiment distribution

See search history and leave feedback

## 🚀 Features

User authentication (signup/login)

Scrape Amazon product details (title, image, price, reviews)

Sentiment prediction using a trained SVM model

Interactive UI built with Streamlit

Session history stored locally

Feedback submission

## 🛠️ Tech Stack
Frontend/UI: Streamlit, Streamlit Option Menu

Backend: Python

ML Model: SVM (trained separately)

Auth: streamlit-authenticator

Web Scraping: Selenium 

Data Handling: Pandas

## ⚙️ Setup Instructions
Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/amazon-review-analysis.git
cd amazon-review-analysis
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the Streamlit app:

bash
Copy
Edit
streamlit run ui.py
## 📁 File Structure
```bash
.
├── streamlit_userInterface.py                  # Main Streamlit app
├── pdt_reviewCollector.py                       # Amazon scraper logic
├── svm_model.sav                               # Pickled SVM model
├── hashed_pw.pkl                               # Pickled hashed passwords
├── images/                                     # UI assets
├── output.csv                                  # User data
├── out.csv                                     # Review predictions
├── outlink.csv                                 # Product links
├── requirements.txt                            # Python dependencies
└── README.md                                   # Project overview
```bash
## 🎯 steps for running the repository
1. run pdt_reviewCollector.py
2. if planning to use customized model change the path to saved model and perform appropriate data inference.
3. run streamlit_userInterface.py using command: streamlit run streamlit_userInterface.py
4. Login and perform analysis.

## 🤖 Model Info
The model (svm_model.sav) is trained on labeled Amazon reviews using TF-IDF + SVM. You can retrain it on your own dataset for customization. save and load it by changing pah to the model.

✨ TODOs / Improvements
 Add model retraining UI

 Export plots for sentiment

 Host app publicly (e.g. Streamlit Cloud)

## 📬 Feedback or Issues?
Feel free to open an issue or leave feedback using the app’s Feedback section!
