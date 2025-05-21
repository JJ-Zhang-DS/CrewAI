import streamlit as st
from crew import NewsletterGenCrew
import os
from dotenv import load_dotenv

def load_html_template():
    with open('src/newsletter_gen/config/newsletter_template.html', 'r') as file:
        html_template = file.read()
    return html_template

def main():
    st.title("Newsletter Generator")
    st.write("Generate a newsletter about any topic you're interested in!")

    # Load environment variables
    load_dotenv()

    # Input fields
    topic = st.text_input("Enter the topic for your newsletter:", 
                         placeholder="e.g., Artificial Intelligence, Climate Change, etc.")
    personal_message = st.text_area("Enter a personal message for your newsletter (optional):",
                                  placeholder="Add a personal touch to your newsletter...")

    if st.button("Generate Newsletter"):
        if not topic:
            st.error("Please enter a topic for the newsletter.")
            return

        with st.spinner("Generating your newsletter... This may take a few minutes."):
            try:
                # Initialize the crew
                crew = NewsletterGenCrew()
                
                # Prepare inputs
                inputs = {
                    'topic': topic,
                    'personal_message': personal_message,
                    'html_template': load_html_template()
                }
                
                # Run the crew
                result = crew.crew().kickoff(inputs=inputs)
                
                # The HTML will be displayed automatically through the step_callback
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 