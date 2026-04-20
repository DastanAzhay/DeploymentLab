import streamlit as st
from PIL import Image
st.title("Hello, Streamlit!")
st.write("This is a simple Streamlit app.")
name = st.text_input("Enter your name:")
if name:
    st.write(f"Hello, {name}!")

img = Image.open("flag.png")
with st.container(horizontal_alignment="center"):
    st.image(img, caption="Flag Image", use_column_width=True) 

