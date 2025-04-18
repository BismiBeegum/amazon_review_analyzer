# 📦 Amazon Review Analysis with Streamlit
This project is a web app built using **Streamlit** that performs sentiment analysis on Amazon product reviews using a custom-trained **LSTM model**. It allows users to: 
- Search for Amazon products
- Analyze review sentiments using a deep learning model
- View insights like sentiment distribution
- See search history and leave feedback
## 🚀 Features 
User authentication (signup/login)
Scrape Amazon product details (title, image, price, reviews) 
Sentiment prediction using a trained LSTM model 
Interactive UI built with Streamlit 
Session history stored locally 
Feedback submission 
## 🛠️ Tech Stack 
**Frontend/UI**: Streamlit, Streamlit Option Menu -
**Backend**: Python 
**ML Model**: LSTM (trained via `model_creation.py`) 
**Auth**: `streamlit-authenticator` 
**Web Scraping**: Selenium 
**Data Handling**: Pandas 
## ⚙️ Setup Instructions 
### Clone the repository: 
```bash 
git clone https://github.com/your-username/amazon-review-analysis.git cd amazon-review-analysis
```
### Install dependencies:
```bash pip install -r requirements.txt ``` 
### Run the Streamlit app: 
```bash 
streamlit run streamlit_userInterface.py
```
## 📥 Dataset Download 
To download the Amazon Review dataset used for training the model, run the provided script: 
```bash 
python dataset_download.py
```
This script uses the `kagglehub` library to download and move the dataset to your desired working directory. If you encounter any issues with the API or need more control, refer to the official [Kaggle API Documentation](https://www.kaggle.com/docs/api). Alternatively, you can manually download the dataset from [Kaggle - Amazon Reviews](https://www.kaggle.com/datasets/purvitsharma/amazonn-reviews).
📌 **Note**: For any API or access-related questions, please visit the [Kaggle API Docs](https://www.kaggle.com/docs/api). Alternatively, you can manually download the dataset directly from the Kaggle dataset page: [Amazon Review Dataset](https://www.kaggle.com/datasets/purvitsharma/amazonn-reviews) ---


 ## 📁 File Structure 
 ```bash 
├── streamlit_userInterface.py # Main Streamlit app
├── pdt_reviewCollector.py # Amazon scraper logic
├── lstm_review_classifier.py # Logic to load model and predict
├── model_creation.py # Script to train and save LSTM model
├── model_functions.py # Prediction logic reused across app
├── tokenizer.sav # Saved tokenizer for preprocessing
├── hashed_pw.pkl # Pickled hashed passwords
├── images/ # UI assets
├── output.csv # User data
├── out.csv # Review predictions
├── outlink.csv # Product links
├── dataset_download.csv # Product links
├── requirements.txt # Python dependencies
└── README.md
# Project overview
```
## 🎯 Steps to Run the Project 
1. Run `pdt_reviewCollector.py` to collect product reviews
2. If planning to use a **custom-trained model**:  run `model_creation.py` to generate and save the LSTM model and tokenizer
3. The prediction logic uses functions from `model_functions.py`
4. Run the main app with:
```bash
streamlit run streamlit_userInterface.py
```
5. Login with your credentials and start analyzing reviews 🎉
## 🤖 Model Info
The model is a Long Short-Term Memory (LSTM) neural network trained on labeled Amazon reviews. It uses a tokenizer saved as `tokenizer.sav` for consistent preprocessing. The model must be created using `model_creation.py`. 
To customize: - Modify `model_creation.py` to train on your dataset - Save the new model and tokenizer - Update the paths in `lstm_review_classifier.py` accordingly
## ✨ TODOs / Improvements 
Add UI for training custom models - Export visualizations for sentiment results - Deploy app publicly (e.g., Streamlit Community Cloud) 
## 📬 Feedback or Issues? Feel free to open an issue or leave feedback using the app’s **Feedback** section! 
