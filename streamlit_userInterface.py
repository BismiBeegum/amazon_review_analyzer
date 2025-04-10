# Cleaned and modularized version of ui.py
import streamlit as st
import pandas as pd
import csv
import os
from pathlib import Path
import pickle
# External packages
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Custom module
import amazonui

# Set Streamlit configuration
st.set_page_config(layout="wide")

# Global user info lists
names = []
usernames = []
passwords = []

# ---------- UI Functions ----------

def feedback():
    st.subheader('Contact us') 
    st.text_area("Tell us how we can help:")
    st.write("We will respond to you via mail or phone")
    cols = st.columns((1, 1))
    cols[0].text_input("Email:")
    cols[1].text_input("Phone:")
    st.markdown('<img width=300 src="https://radioambedkarnagar904.com/wp-content/uploads/2021/09/121212.gif" style="margin-left: 5px; filter: hue-rotate(230deg) brightness(1.1);">', unsafe_allow_html=True)

# Display previous predictions

def previous():
    try:
        links_df = pd.read_csv('/home/six_eyes/amazon/outlink.csv')
        previous_links = links_df.iloc[:, 0].tolist()

        reviews_df = pd.read_csv('/home/six_eyes/amazon/out.csv')
        grouped_reviews = reviews_df.groupby("product")

        product_names = reviews_df["product"].unique()
        product_images = reviews_df["image"].unique()
        product_prices = reviews_df["prize"].unique()

        pred_counts = reviews_df.groupby(['product'])['predictions'].value_counts().reset_index(name='counts')
        product_groups = pred_counts.groupby('product')

        prices = [grouped_reviews.get_group(name)['prize'].iloc[0] for name in product_names]

        for i, name in enumerate(product_names):
            stats = product_groups.get_group(name)
            results = dict(zip(stats['predictions'], stats['counts']))
            pos = round((results.get('Positive', 0) / max(1, sum(results.values()))) * 100)
            neg = round((results.get('Negative', 0) / max(1, sum(results.values()))) * 100)

            result(product_images[i], prices[i], name, previous_links[i], pos, neg)
    except FileNotFoundError:
        st.subheader('No Search History')

# Display a single product result
def result(image, price, product_name, link, positive, negative):
    cols = st.columns((3, 1, 5))
    cols[0].image(image, width=350)
    cols[2].markdown(f"<h2 style='color:black;font-size:20px;'>{product_name}</h2>", unsafe_allow_html=True)
    cols[2].markdown(f"<h2 style='color:red;font-size:25px;'>${price}</h2>", unsafe_allow_html=True)
    cols[2].write(f'{positive}% positive reviews')
    cols[2].write(f'{negative}% negative reviews')
    cols[2].markdown(f"<a href='{link}'>click here to view product in Amazon</a>", unsafe_allow_html=True)

def streamlit_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Login", "Sign up"],
            icons=["house", "book", "person"],
            menu_icon="cast",
            default_index=0,
        )
    return selected

def streamlit_menu1():
    return option_menu(
        menu_title=None,
        options=["Predict", "Feedback", "Previous Search"],
        icons=["search", "chat", "clock-history"],
        menu_icon="cast",
        default_index=0,
        orientation='horizontal'
    )
# Save user credentials and hash password
def keycrt(name, username, password):
    with open('password.csv', 'a') as f:
        csv.writer(f).writerow([password])
    with open('output.csv', 'a') as f:
        csv.writer(f).writerow([name, username])

    data = pd.read_csv("password.csv")
    hashed_passwords = stauth.Hasher(data['code'].tolist()).generate()

    with open(Path(__file__).parent / "hashed_pw.pkl", "wb") as file:
        pickle.dump(hashed_passwords, file)

# ---------- Main App Flow ----------

selected = streamlit_menu()

if selected == "Home":
    st.title('Amazon Review Analysis')
    st.write('Analyse data and prediction')

    st.markdown("""
        <p style='color:black;font-size:16px;font-family:Georgia , serif;'>Amazon review analysis is an invaluable advantage that AI and machine learning have given to businesses...</p>
    """, unsafe_allow_html=True)
    st.image("images/06.jpg")
    st.markdown("<p style='color:black;font-size:16px;font-family:Georgia , serif;'>Because of its popularity...</p>", unsafe_allow_html=True)
    st.markdown("""
        <ul>
        <li>📌 79% of consumers trust online reviews as much as personal recommendations</li>
        <li>📌 85% of consumers say that they read online reviews for local businesses</li>
        <li>📌 73% say positive reviews make them trust a business more</li>
        </ul>
    """, unsafe_allow_html=True)
    cols = st.columns(3)
    cols[0].image('images/03.webp')
    cols[2].image("images/011.png")
    st.markdown("""
        <h2 style='color:black;'>Amazon review analysis can give insightful customer information that can be harnessed for product betterment.</h2>
    """, unsafe_allow_html=True)

elif selected == 'Login':
    data = pd.read_csv("output.csv")
    names = data['names'].tolist()
    usernames = data['usernames'].tolist()

    with open(Path(__file__).parent / "hashed_pw.pkl", "rb") as file:
        hashed_passwords = pickle.load(file)

    authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "sales_dashboard", "abcdef", cookie_expiry_days=30)
    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status is False:
        st.sidebar.error("Username/password is incorrect")
    elif authentication_status is None:
        st.sidebar.warning("Please enter your username and password")
        try:
            os.remove('out.csv')
        except FileNotFoundError:
            st.subheader('WELCOME')
    elif authentication_status:
        authenticator.logout("Logout", "sidebar")
        st.sidebar.title(f"Welcome {name}")

        selected1 = streamlit_menu1()

        if selected1 == "Predict":
            st.title('Welcome product review analysis')
            product = st.text_input('Product name')
            product_nos = st.text_input('Number of products')

            if st.button('click') == 1:
                try:
                    df, lstlink = amazonui.scrapper(product, int(product_nos))
                    df['reviews'] = df['reviews'].str.replace('Read more', '')

                    pd.DataFrame(lstlink).to_csv('outlink.csv', index=False)

                    lstname = df["product"].unique()
                    lstimg = df["image"].unique()
                    lstprize = df["prize"].unique()

                    load_model, cv = pk.load(open('amazonui/svm_model.sav', 'rb'))
                    result1 = load_model.predict(cv.transform(df['reviews']))
                    df['predictions'] = result1
                    df.replace({'predictions': {0: 'Negative', 1: 'Positive'}}, inplace=True)
                    df.to_csv('out.csv', index=False)

                    pred_counts = df.groupby(['product'])['predictions'].value_counts().reset_index(name='counts')
                    grouped = pred_counts.groupby('product')
                    df_grouped = df.groupby("product")

                    for i, name in enumerate(lstname):
                        stats = grouped.get_group(name)
                        results = dict(zip(stats['predictions'], stats['counts']))
                        pos = round((results.get('Positive', 0) / max(1, sum(results.values()))) * 100)
                        neg = round((results.get('Negative', 0) / max(1, sum(results.values()))) * 100)
                        result(lstimg[i], lstprize[i], name, lstlink[i], pos, neg)
                except NoSuchElementException:
                    st.warning('Please Enter the Proper Captcha code 🔒')
                except TimeoutException:
                    st.warning('Please check your Internet connection 🛜')

        elif selected1 == "Feedback":
            feedback()
        elif selected1 == "Previous Search":
            previous()

elif selected == "Sign up":
    with st.form(key="signup"):
        cols = st.columns((2, 1))
        input_1 = cols[0].text_input("Name")
        input_2 = cols[0].text_input("Username")
        input_3 = cols[0].text_input("Password")
        if st.form_submit_button('Submit') == 1:
            keycrt(input_1, input_2, input_3)
            st.success(f'Hi {input_2}, you successfully created a new account 🎉')
