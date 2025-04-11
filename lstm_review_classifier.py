# train_lstm_model.py

"""
Train an LSTM model on Amazon review sentiment data.

Saves:
- Trained model (`lstm_model.h5`)
- Tokenizer used for text processing (`tokenizer.sav`)
"""

# === Imports ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import emoji
import warnings
import pickle

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Bidirectional, Dense
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import EarlyStopping

# === Configs ===
warnings.filterwarnings("ignore")
plt.style.use("fivethirtyeight")
sns.set_style("darkgrid")

# === Load and preprocess data ===
def load_data(filepath):
    df = pd.read_csv(filepath)
    df = df[["review", "sentiment"]].dropna()
    return df

def clean_text(df, column):
    df[column] = df[column].str.replace(r"@", " at ", regex=True)
    df[column] = df[column].str.replace(r"#\W+", " ", regex=True)
    df[column] = df[column].str.replace(r"[^a-zA-Z(),\"'\n_]", " ", regex=True)
    df[column] = df[column].str.replace(r"http\S+", "", regex=True)
    df[column] = df[column].str.lower()
    return df

def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "can not", text)
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)
    text = re.sub(emoji.get_emoji_regexp(), "", text)
    text = [lemmatizer.lemmatize(word) for word in text.split() if word not in set(stopwords.words("english"))]
    return ' '.join(text)

# === Build LSTM Model ===
def build_lstm_model(vocab_size, input_length):
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size, output_dim=64, input_length=input_length))
    model.add(Bidirectional(LSTM(100)))
    model.add(Dense(128, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model

# === Main training pipeline ===
def main():
    # Load and clean data
    df = load_data("path to the dataset")
    df = clean_text(df, "review")
    df["clean_review"] = df["review"].apply(preprocess_text)

    # Train/test split
    X = df["clean_review"].values
    y = df["sentiment"].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Tokenization
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train)
    X_train_seq = tokenizer.texts_to_sequences(X_train)
    X_test_seq = tokenizer.texts_to_sequences(X_test)

    # Padding
    MAX_LEN = 64
    X_train_pad = pad_sequences(X_train_seq, maxlen=MAX_LEN)
    X_test_pad = pad_sequences(X_test_seq, maxlen=MAX_LEN)

    # Model training
    model = build_lstm_model(len(tokenizer.word_index) + 1, MAX_LEN)
    early_stop = EarlyStopping(monitor="val_loss", patience=5, verbose=True)

    history = model.fit(
        X_train_pad,
        y_train,
        validation_data=(X_test_pad, y_test),
        batch_size=64,
        epochs=15,
        callbacks=[early_stop],
    )

    # Evaluation
    pred_train = model.predict(X_train_pad)
    pred_test = model.predict(X_test_pad)

    print("Train ROC AUC:", roc_auc_score(y_train, pred_train))
    print("Test ROC AUC:", roc_auc_score(y_test, pred_test))
    model.evaluate(X_test_pad, y_test)

    # Save model and tokenizer
    model.save("lstm_model.h5")
    with open("tokenizer.sav", "wb") as f:
        pickle.dump(tokenizer, f)

    print("Model and tokenizer saved successfully.")

# === Run script ===
main()