import streamlit as st
from PIL import Image
st.title("Hello, Streamlit!")
st.write("This is a simple Streamlit app.")
name = st.text_input("Enter your name:")
img = Image.open("C:/Users/dasta/Desktop/backend/flag.png")
st.image(img, caption="Sample Image")
if name:
    st.write(f"Hello, {name}!") 
