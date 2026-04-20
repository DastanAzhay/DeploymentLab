import streamlit as st
from PIL import Image
st.title("Hello, Streamlit!")
st.write("This is a simple Streamlit app.")
name = st.text_input("Enter your name:")
img = Image.open("flag.png")

if name:
    st.write(f"Hello, {name}!")
with st.container(horizontal_alignment="center"):
    st.image(img, caption="Flag Image", use_column_width=True)
