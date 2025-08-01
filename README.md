# AI-Powered-Social-Media-Post-Caption-Generator
This project is a powerful and intuitive Streamlit-based web application designed to automate the creation of social media content. It leverages a multi-modal Large Language Model (LLM) to generate creative and contextually relevant captions, hashtags, and emojis from user-provided text and images. Additionally, it integrates a sentiment analysis model to provide instant feedback on the emotional tone of the generated content.

Features
AI-Powered Content Generation: Utilizes a multi-modal LLM (Gemini) to create unique captions, hashtags, and emojis.

Multi-modal Input: Generates content based on both text keywords and an optional image upload.

Sentiment Analysis: Analyzes the emotional tone of each generated caption using a transformers model.

Multiple Variations: Allows users to generate multiple distinct post variations at once.

Platform-Specific Prompts: Tailors content generation for different social media platforms (e.g., Instagram, LinkedIn, Twitter).

Easy-to-Use UI: A clean and responsive user interface built with Streamlit.

Copy-to-Clipboard: Convenient copy buttons for individual posts and all generated content.

Technologies Used
Python: The core programming language.

Streamlit: For building the interactive web application.

Gemini API: The multi-modal LLM backend for content generation.

Hugging Face transformers: The library used for sentiment analysis.

torch: The deep learning framework required by the sentiment analysis model.

requests: For making API calls to the LLM.

base64 & json: For data handling and serialization.

Installation and Setup
Prerequisites
Python 3.9 or higher

pip (Python package installer)

Steps
Clone the repository (or download the Python file):

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required dependencies:

pip install streamlit requests transformers torch

Note: torch installation may take a few minutes.

Set up your Gemini API Key:

Obtain a Gemini API key from the Google AI Studio platform.

Create a .streamlit folder in your project directory.

Inside the .streamlit folder, create a secrets.toml file.

Add your API key to the secrets.toml file in the following format:

GEMINI_API_KEY = "your_api_key_here"

The application will securely access this key.

How to Run the App
Navigate to the project directory in your terminal.

Run the Streamlit application:

streamlit run app.py

The application will open in your web browser. You can now start generating social media content!

Usage
Upload an image: (Optional) Upload an image to provide visual context for the AI.

Enter keywords: Provide a short description or relevant keywords for your post.

Select post type: Choose the desired tone or purpose of the post (e.g., "Inspirational", "Promotional").

Select platforms: Choose one or more social media platforms.

Set number of captions: Specify how many variations you want to generate.

Click "Generate Content": The application will display the generated captions, hashtags, emojis, and a sentiment analysis score for each.

Copy and Share: Use the "Copy This Post" buttons to easily copy the content you like.

Project Structure
/your-repo-name/
├── .streamlit/
│   └── secrets.toml         # Securely stores your API key
├── app.py                   # The main Streamlit application script
└── README.md

Contributing
Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, feel free to open an issue or submit a pull request.

License
This project is open-source and available under the MIT License.
