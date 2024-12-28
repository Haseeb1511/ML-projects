import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


ps = PorterStemmer()


tf=pickle.load(open("vector.pkl","rb"))
model = pickle.load(open("model.pkl","rb"))

def lowercase(text):
    text=text.lower()
    text=nltk.word_tokenize(text)
    l=[]
    for i in text:
        if i.isalnum():
            l.append(i)
    text=l[:]
    l.clear()
    for i in text:
        if i not in stopwords.words("english") and i not in string.punctuation:
            l.append(i)
    text=l[:]
    l.clear()
    for i in text:
        ps.stem(i)
        l.append(i)
    return " ".join(l)




st.title("Text Spam Classifier")
input=st.text_input("Enter the message....")
if st.button("Predict"):
    transformed_text=lowercase(input)
    vector=tf.transform([transformed_text])
    result=model.predict(vector)[0]

    if result == 1:
         st.header("SPAM")
    else:
        st.header("NOT SPAM")