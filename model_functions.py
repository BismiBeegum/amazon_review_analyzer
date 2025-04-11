# review_predictor.py

"""
Script to predict sentiment using a trained Keras model and tokenizer.

- Supports single review prediction (interactive)
- Supports batch prediction via `prediction_result()` function

Required files:
- svm_model.sav: Trained model file
- tokenizer.sav: Tokenizer used during training
"""


import pickle
from keras.preprocessing.sequence import pad_sequences

#Load the trained model
with open("svm_model.sav", "rb") as model_file:
    model, _ = pickle.load(model_file)  # _ ignores additional data (if any)

#Load the trained tokenizer
with open("tokenizer.sav", "rb") as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)

def predict_sentiment(text: str, max_len: int = 64) -> str:
    """
    Predict the sentiment of a single review.

    Args:
        text (str): Input review text
        max_len (int): Max sequence length used during training

    Returns:
        str: Sentiment label ("Positive" or "Negative")
    """
    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=max_len)
    prediction = model.predict(padded)

    return "Positive Review 😊 (Label: 1)" if prediction >= 0.5 else "Negative Review 😞 (Label: 0)"

def prediction_result(text_list, max_len: int = 64):
    """
    Predict sentiment for a batch of reviews.

    Args:
        text_list (List[str]): List of review texts
        max_len (int): Max sequence length used during training

    Returns:
        List[int]: List of sentiment labels (1 for positive, 0 for negative)
    """
    sequences = tokenizer.texts_to_sequences(text_list)
    padded = pad_sequences(sequences, maxlen=max_len)
    raw_preds = model.predict(padded)
    return [1 if p >= 0.5 else 0 for p in raw_preds.flatten().tolist()]

if __name__ == "__main__":
    # Example usage
    sample_review = "This book was a fantastic read and very inspiring!"
    result = predict_sentiment(sample_review)
    print("Prediction:", result)

