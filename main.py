import streamlit as st
from post_generator import generate_post
import re  # Import regex for extracting templates

st.title("🚀 AI-Powered LinkedIn Post Generator")

# Predefined tags
TAGS = ["AI", "Data Science", "Machine Learning", "Deep Learning", "Cloud Computing", "Cybersecurity"]

# Select Post Generation Method
generation_method = st.radio(
    "Select post generation method:", 
    ["Use Pre-built Templates", "Upload Your Own Template File"]
)

uploaded_file = None
if generation_method == "Upload Your Own Template File":
    uploaded_file = st.file_uploader("Upload a .txt file with templates", type=["txt"])

# User selects post details
selected_length = st.selectbox("Select Post Length:", ["Short", "Medium", "Long"])
selected_language = st.selectbox("Select Language:", ["English", "Hinglish"])
selected_tag = st.selectbox("Select Topic/Tag:", TAGS)  # Use predefined tags

# Extract templates from text file
def extract_templates(text):
    """Extract templates enclosed in square brackets [ ]"""
    templates = re.findall(r"\[(.*?)\]", text, re.DOTALL)  # Extract text inside [ ]
    return [t.strip() for t in templates if t.strip()]  # Remove empty templates

if st.button("🚀 Generate Post"):
    with st.spinner("Generating your post..."):
        templates = []

        # Read the uploaded text file and extract templates inside [ ]
        if uploaded_file:
            file_content = uploaded_file.read().decode("utf-8")
            templates = extract_templates(file_content)  # Extract bracketed content

        # Generate LinkedIn Post
        post = generate_post(selected_length, selected_language, selected_tag, templates)
        st.session_state.post_history = st.session_state.get("post_history", []) + [post]
        
        # Display the generated post
        st.subheader("Generated Post:")
        st.markdown(f"✅ **Your AI-Generated LinkedIn Post:**\n```\n{post}\n```")
