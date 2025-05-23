import streamlit as st
from newsletter_gen.crew import NewsletterGenCrew


class NewsletterGenUI:
    def __init__(self):
        # Set page config at the very beginning
        st.set_page_config(
            page_title="Newsletter Generation",
            page_icon=":envelope:",
            initial_sidebar_state="expanded"
        )
        
        # Add custom CSS to force sidebar layout
        st.markdown("""
            <style>
                [data-testid="stSidebar"][aria-expanded="true"]{
                    position: fixed;
                    top: 0;
                    left: 0;
                    height: 100vh;
                    width: 300px;
                    z-index: 1000;
                }
                .main .block-container {
                    padding-left: 320px;
                }
            </style>
        """, unsafe_allow_html=True)

    def load_html_template(self):
        with open("src/newsletter_gen/config/newsletter_template.html", "r") as file:
            html_template = file.read()
        return html_template

    def generate_newsletter(self, topic, personal_message):
        inputs = {
            "topic": topic,
            "personal_message": personal_message,
            "html_template": self.load_html_template()
        }
        
        return NewsletterGenCrew().crew().kickoff(inputs=inputs)

    def newsletter_generation(self):
        if st.session_state.generating:
            try:
                st.session_state.newsletter = self.generate_newsletter(
                    st.session_state.topic,
                    st.session_state.personal_message
                )
                st.session_state.generating = False
            except Exception as e:
                st.error(f"Error generating newsletter: {str(e)}")
                st.session_state.generating = False
                return

        # Debug information
        st.write("Debug Info:")
        st.write(f"Generating: {st.session_state.generating}")
        st.write(f"Newsletter exists: {bool(st.session_state.newsletter)}")
        
        if st.session_state.newsletter:
            st.write("Newsletter Generated Successfully!")
            st.download_button(
                label="Download HTML file",
                data=st.session_state.newsletter,
                file_name="newsletter.html",
                mime="text/html",
            )

    def sidebar(self):
        with st.sidebar:
            st.title("Newsletter Generation")

            st.write(
                """
                To generate a newsletter, you need to provide a topic and a personal message. \n
                AI will generate a newsletter based on the topic and the personal message. 
                """
            )

            st.text_input("Topic", key="topic", placeholder="US Stock Market")
            st.text_area("Personal Message", key="personal_message", placeholder="Welcome to the newsletters")

            if st.button("Generate Newsletter"):
                st.session_state.generating = True

    def render(self):
        # Initialize session state variables
        if "topic" not in st.session_state:
            st.session_state.topic = ""

        if "personal_message" not in st.session_state:
            st.session_state.personal_message = ""

        if "newsletter" not in st.session_state:
            st.session_state.newsletter = ""

        if "generating" not in st.session_state:
            st.session_state.generating = False

        # Render sidebar and main content
        self.sidebar()
        self.newsletter_generation()

if __name__ == "__main__":
    NewsletterGenUI().render()



