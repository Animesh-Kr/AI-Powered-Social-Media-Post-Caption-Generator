import streamlit as st
import requests # For making API calls to the LLM
import json # For handling JSON responses
import base64 # For encoding image to base64
from transformers import pipeline # For sentiment analysis
import torch # This is required for the transformers pipeline backend

# To fix the 'ModuleNotFoundError', you need to install the library.
# Since this is running in a controlled environment, we will assume it's installed.
# If you are running this locally, you would need to run:
# pip install transformers
# pip install torch

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Social Media Post & Caption Generator",
    page_icon="📝",
    layout="centered"
)

# --- Initialize Sentiment Analyzer ---
@st.cache_resource
def get_sentiment_analyzer():
    """
    Initializes and caches a sentiment analysis model from the transformers library.
    """
    return pipeline("sentiment-analysis")

sentiment_analyzer = get_sentiment_analyzer()

# --- Helper Function for Copy to Clipboard (Streamlit workaround) ---
def copy_to_clipboard_button(text_to_copy, button_text="Copy", key=None):
    """
    Creates an HTML button that copies text to the clipboard when clicked.
    """
    unique_id = f"copy_button_{key}" if key else f"copy_button_{hash(text_to_copy)}"
    html_code = f"""
    <button id="{unique_id}" onclick="
        var text = `{text_to_copy.replace('`', '\\`')}`; // Escape backticks
        var dummy = document.createElement('textarea');
        document.body.appendChild(dummy);
        dummy.value = text;
        dummy.select();
        document.execCommand('copy');
        document.body.removeChild(dummy);
        var button = document.getElementById('{unique_id}');
        button.innerText = 'Copied!';
        setTimeout(() => {{ button.innerText = '{button_text}'; }}, 2000);
    " style="
        background-color: #007bff; /* Blue */
        border: none;
        color: white;
        padding: 5px 10px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
        transition: background-color 0.3s ease;
    ">{button_text}</button>
    """
    st.components.v1.html(html_code, height=35)

# --- LLM Integration Function ---
def generate_content_with_llm(keywords_input, post_type, platforms, num_generations, uploaded_file=None):
    """
    Generates social media content using the Gemini LLM, optionally with an image.
    Can generate multiple variations.
    """
    # The API key will be automatically provided by the Canvas environment
    api_key = "AIzaSyBUoUHmjGztfv2tGzTMUzc5pf3UTMxw2xo"
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    # Prepare the text prompt
    prompt_text = f"""
    You are a social media content generator. Based on the provided 'keywords', 'post_type', and 'platforms',
    generate {num_generations} distinct social media posts. Each post should include:
    - a social media caption
    - a list of relevant hashtags (up to 10, without '#' prefix)
    - appropriate emojis.
    """
    if uploaded_file:
        prompt_text += "\nAn image is also provided. Please consider its content when generating the posts."

    prompt_text += f"""
    The output should be a JSON array of objects, where each object has the following structure:
    {{
      "caption": "Your generated caption here.",
      "hashtags": ["hashtag1", "hashtag2", ...],
      "emojis": "✨🚀"
    }}

    Keywords: {keywords_input}
    Post Type: {post_type}
    Platforms: {', '.join(platforms)}

    Ensure each caption is engaging and suitable for the selected platforms.
    """

    chat_history_parts = []
    chat_history_parts.append({"text": prompt_text})

    if uploaded_file:
        # Read the image bytes and encode to base64
        image_bytes = uploaded_file.getvalue() # Use getvalue() for BytesIO object from Streamlit
        base64_image_data = base64.b64encode(image_bytes).decode("utf-8")
        mime_type = uploaded_file.type # Get the MIME type from Streamlit's file object

        chat_history_parts.append({
            "inlineData": {
                "mimeType": mime_type,
                "data": base64_image_data
            }
        })

    payload = {
        "contents": [{"role": "user", "parts": chat_history_parts}], # Consolidated parts into a single user message
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "ARRAY", # Expect an array of objects
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "caption": { "type": "STRING" },
                        "hashtags": {
                            "type": "ARRAY",
                            "items": { "type": "STRING" }
                        },
                        "emojis": { "type": "STRING" }
                    },
                    "propertyOrdering": ["caption", "hashtags", "emojis"]
                }
            }
        }
    }

    try:
        response = requests.post(api_url, headers={'Content-Type': 'application/json'}, json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        result = response.json()

        if result.get("candidates") and len(result["candidates"]) > 0 and \
           result["candidates"][0].get("content") and \
           result["candidates"][0]["content"].get("parts") and \
           len(result["candidates"][0]["content"]["parts"]) > 0:

            # The LLM returns the JSON as a string within the 'text' part
            json_string = result["candidates"][0]["content"]["parts"][0]["text"]
            # Parse the JSON string into a list of dictionaries
            parsed_content_list = json.loads(json_string)

            generated_posts = []
            for item in parsed_content_list:
                # Sanitize hashtags: remove spaces and non-alphanumeric characters, then add '#'
                sanitized_hashtags = [
                    h.replace(" ", "").replace("#", "") for h in item.get("hashtags", [])
                ]
                formatted_hashtags = [f"#{h}" for h in sanitized_hashtags if h] # Ensure not empty

                generated_posts.append({
                    "caption": item.get("caption", "Could not generate caption."),
                    "hashtags": formatted_hashtags,
                    "emojis": item.get("emojis", "✨")
                })
            return generated_posts
        else:
            st.error("LLM response structure unexpected. Please try again.")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Network or API error: {e}. Please check your connection or API key.")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error parsing LLM response: {e}. The model might have returned malformed JSON.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# --- Streamlit UI Layout ---
st.header("Generate Your Social Media Content (AI-Powered)")
st.markdown("""
    Upload an image (for your reference), provide keywords/themes, select a post type,
    and choose your target social media platforms.
    This tool will generate a caption, hashtags, and emojis using an AI model.
""")

# Image Upload (for user's visual context, not processed by app for content)
uploaded_file = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    st.info("Note: The AI generator will now consider the image content in addition to your text input.")

# Input for keywords/themes
keywords = st.text_area(
    "Enter keywords or a short description of your post/image:",
    placeholder="e.g., AI in agriculture, new smartphone launch, healthy recipe, team celebration",
    height=100
)

# Select for post type/tone
post_type = st.selectbox(
    "Select the type or tone of your post:",
    options=[
        "Inspirational", "Informative", "Promotional", "Announcement",
        "General", "Question/Engagement", "Behind-the-Scenes",
        "Tutorial/How-To", "Success Story"
    ],
    index=1 # Default to Informative
)

# New: Number of captions to generate
num_generations = st.number_input(
    "Number of captions to generate:",
    min_value=1,
    max_value=5, # Limit to a reasonable number to avoid long generation times
    value=1,
    step=1,
    help="Choose how many distinct caption variations you want to generate."
)


# Multi-select for platforms
platforms_options = ["Instagram", "LinkedIn", "Twitter", "Facebook", "TikTok", "Pinterest", "YouTube Community"]
selected_platforms = st.multiselect(
    "Select target social media platforms:",
    options=platforms_options,
    default=["Instagram"] # Default to Instagram
)

# Generate button
if st.button("Generate Content", type="primary", use_container_width=True):
    if not keywords and uploaded_file is None: # Allow generation with just an image or just text
        st.warning("Please enter some keywords or upload an image to generate content.")
    elif not selected_platforms:
        st.warning("Please select at least one social media platform.")
    else:
        with st.spinner(f"Generating {num_generations} captions using AI..."):
            # Pass the uploaded_file directly to the LLM function
            generated_posts = generate_content_with_llm(keywords, post_type, selected_platforms, num_generations, uploaded_file)

            if generated_posts:
                st.subheader("✨ Your Generated Content:")
                all_content_for_copy = []

                for i, post in enumerate(generated_posts):
                    st.markdown(f"---") # Separator for multiple posts
                    st.markdown(f"**Post #{i+1}:**")
                    caption = post["caption"]
                    hashtags = post["hashtags"]
                    emojis = post["emojis"]

                    # Perform sentiment analysis on the generated caption
                    sentiment_result = sentiment_analyzer(caption)[0]
                    sentiment_label = sentiment_result['label']
                    sentiment_score = sentiment_result['score']

                    # Display the generated content and sentiment result
                    st.write(f"**Caption:** {caption} {emojis}")
                    st.write(f"**Hashtags:** {' '.join(hashtags)}")
                    st.info(f"**Sentiment:** {sentiment_label} (Score: {sentiment_score:.2f})")

                    # Add copy button for each individual post
                    single_post_content = f"Caption: {caption} {emojis}\nHashtags: {' '.join(hashtags)}\nSentiment: {sentiment_label} (Score: {sentiment_score:.2f})"
                    copy_to_clipboard_button(single_post_content, button_text="Copy This Post", key=f"copy_post_{i}")
                    st.markdown("") # Add a small space after the button

                    all_content_for_copy.append(f"Post #{i+1}:\n{single_post_content}")


                #st.markdown("---") # Final separator
                #full_content_to_copy = "\n\n".join(all_content_for_copy)
                #copy_to_clipboard_button(full_content_to_copy, key="final_copy_all_btn", button_text="Copy All Posts")"""

# --- Footer ---
st.markdown("---")
st.markdown("💡 Tip: Be as specific as possible with your keywords for better results!")
st.markdown("This generator uses an AI model (Gemini) for dynamic content creation, offering more creative and context-aware results.")
st.markdown("Developed with Streamlit.")
