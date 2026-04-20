import streamlit as st
from PIL import Image
import numpy as np

st.title("Hello, Streamlit!")
st.write("This is a simple Streamlit app.")
name = st.text_input("Enter your name:")
if name:
    st.write(f"Hello, {name}!")

st.divider()

st.subheader("Image Analyzer")
st.write("Upload any image to analyze it.")

uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file:
    img = Image.open(uploaded_file)

    with st.container():
        st.image(img, caption="Uploaded Image", use_column_width=True)

    st.subheader("Image Info")
    col1, col2, col3 = st.columns(3)
    col1.metric("Width", f"{img.width} px")
    col2.metric("Height", f"{img.height} px")
    col3.metric("Format", img.format or uploaded_file.type.split("/")[1].upper())

    st.subheader("Color Stats (RGB Averages)")
    img_array = np.array(img.convert("RGB"))
    avg_r = int(img_array[:, :, 0].mean())
    avg_g = int(img_array[:, :, 1].mean())
    avg_b = int(img_array[:, :, 2].mean())

    c1, c2, c3 = st.columns(3)
    c1.metric("Red", avg_r)
    c2.metric("Green", avg_g)
    c3.metric("Blue", avg_b)

    st.color_picker("Dominant avg color", f"#{avg_r:02x}{avg_g:02x}{avg_b:02x}", disabled=True)
