import streamlit as st
import json
from post_generator import generate_post

st.title("🚀 AI-Powered LinkedIn Post Generator")

# Select Post Generation Method
generation_method = st.radio(
    "Select post generation method:", 
    ["Use Pre-built Templates", "Upload Your Own Templates"]
)

uploaded_files = None
if generation_method == "Upload Your Own Templates":
    uploaded_files = st.file_uploader(
        "Upload JSON files with templates", 
        type=["json"], 
        accept_multiple_files=True
    )

# User selects post details
selected_length = st.selectbox("Select Post Length:", ["Short", "Medium", "Long"])
selected_language = st.selectbox("Select Language:", ["English", "Hinglish"])
selected_tag = st.text_input("Enter Topic/Tag:", "")

if st.button("🚀 Generate Post"):
    with st.spinner("Generating your post..."):
        templates = []

        # Load multiple uploaded JSON files
        if uploaded_files:
            for file in uploaded_files:
                try:
                    templates.extend(json.load(file))  # Append all templates
                except json.JSONDecodeError:
                    st.error(f"Error reading {file.name}. Ensure it's a valid JSON file.")

        # Generate LinkedIn Post
        post = generate_post(selected_length, selected_language, selected_tag, templates)
        st.session_state.post_history = st.session_state.get("post_history", []) + [post]
        
        # Display the generated post
        st.subheader("Generated Post:")
        st.markdown(f"✅ **Your AI-Generated LinkedIn Post:**\n```\n{post}\n```")
