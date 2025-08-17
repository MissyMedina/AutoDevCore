#!/usr/bin/env python3
"""
Test page for input field visibility and functionality
"""

import streamlit as st

st.set_page_config(page_title="Input Test - AutoDevCore", page_icon="🧪", layout="wide")

# Custom CSS for input visibility
st.markdown(
    """
<style>
    /* Ensure all input fields are visible and properly styled */
    .stTextInput > div > div > input {
        background-color: white !important;
        color: #1e293b !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        font-size: 16px !important;
        min-height: 40px !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: white !important;
        color: #1e293b !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        font-size: 16px !important;
        min-height: 100px !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    .stSelectbox > div > div > div {
        background-color: white !important;
        color: #1e293b !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🧪 Input Field Test")
st.write("This page tests that all input fields are visible and functional.")

# Test different input types
st.header("Text Input Test")
text_input = st.text_input("Enter some text:", placeholder="Type here...")
if text_input:
    st.success(f"You entered: {text_input}")

st.header("Text Area Test")
text_area = st.text_area(
    "Enter a longer text:", placeholder="Type a longer message here..."
)
if text_area:
    st.success(f"You entered: {text_area}")

st.header("Select Box Test")
options = ["Option 1", "Option 2", "Option 3", "Option 4"]
selected = st.selectbox("Choose an option:", options)
st.success(f"You selected: {selected}")

st.header("Number Input Test")
number = st.number_input("Enter a number:", min_value=0, max_value=100, value=50)
st.success(f"You entered: {number}")

st.header("File Upload Test")
uploaded_file = st.file_uploader("Choose a file:", type=["txt", "py", "md"])
if uploaded_file:
    st.success(f"File uploaded: {uploaded_file.name}")

st.header("Button Test")
if st.button("Click me!"):
    st.balloons()
    st.success("Button clicked successfully!")

st.header("Checkbox Test")
checkbox = st.checkbox("Check this box")
if checkbox:
    st.success("Checkbox is checked!")

st.header("Radio Button Test")
radio = st.radio("Choose one:", ["Choice A", "Choice B", "Choice C"])
st.success(f"You chose: {radio}")

st.header("Slider Test")
slider = st.slider("Select a value:", 0, 100, 50)
st.success(f"Slider value: {slider}")

# Status
st.header("✅ Test Status")
st.success("All input fields should be visible and functional!")
st.info(
    "If you can see and interact with all the fields above, the GUI is working correctly."
)
