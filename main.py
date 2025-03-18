import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
import time


length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]


if "post_history" not in st.session_state:
    st.session_state.post_history = []


def main():
    st.set_page_config(page_title="LinkedIn Post Generator", page_icon="📢", layout="centered")
    
    # Center align content
    st.markdown(
        """
        <style>
            .centered {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
            }
        </style>
        <div class="centered">
            <h1>📢 AI-Powered LinkedIn Post Generator</h1>
            <p>🚀 Generate engaging and impactful LinkedIn posts effortlessly!<br>
            Customize your post based on topic, length, and language, then let AI do the rest.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Use a centered container for input fields
    with st.container():
        col1, col2 = st.columns([1, 1], gap="large")
        
        fs = FewShotPosts()
        tags = fs.get_tags()

        with col1:
            selected_tag = st.selectbox("🔖 Topic", options=tags)
            selected_length = st.selectbox("📝 Length", options=length_options)

        with col2:
            selected_language = st.selectbox("🌍 Language", options=language_options)
    
    # Centered Generate Button
    st.markdown("<div class='centered'>", unsafe_allow_html=True)
    if st.button("🚀 Generate Post"):
        with st.spinner("Generating your post..."):
            time.sleep(1.5)  # Simulating processing time
            post = generate_post(selected_length, selected_language, selected_tag)
            st.session_state.post_history.append(post)  # Save in session
            st.subheader("Generated Post:")
            
            # Display in a better UI format
            st.markdown(
                f"""
                ✅ **Your AI-Generated LinkedIn Post:**
                ```
                {post}
                ```
                """
            )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display Post History
    if st.session_state.post_history:
        with st.expander("📜 View Previous Posts", expanded=False):
            for idx, old_post in enumerate(reversed(st.session_state.post_history[-5:]), 1):
                st.markdown(f"**{idx}.** {old_post}")
                st.divider()
    
    # Centered Download Button
    st.markdown("<div class='centered'>", unsafe_allow_html=True)
    if st.session_state.post_history:
        history_text = "\n\n".join(st.session_state.post_history)
        st.download_button(
            label="💾 Download Posts",
            data=history_text,
            file_name="generated_posts.txt",
            mime="text/plain"
        )
    st.markdown("</div>", unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
