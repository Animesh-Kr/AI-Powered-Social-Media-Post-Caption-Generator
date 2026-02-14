"""
AI-Powered Social Media Content Generator (Simplified Version)

A dissertation-level application demonstrating advanced software engineering
practices including modular architecture, configuration management, error
handling, and comprehensive documentation.

Author: Animesh Kumar

Note: This version has sentiment analysis disabled to avoid dependency issues.
      Install transformers and torch to enable sentiment analysis.
"""
import os
import streamlit as st
import logging
from typing import Optional
from dotenv import load_dotenv
# Import custom modules
from config import Config
from content_generator import (
    GeminiContentGenerator,
    ContentRequest,
    ContentGenerationError
)

# Import RAG pipeline (optional - graceful degradation if not available)
try:
    from rag_pipeline import create_rag_pipeline
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    logger.warning("⚠️ RAG pipeline not available (install dependencies)")

# Configure logging
load_dotenv(override=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# --- Page Configuration ---
st.set_page_config(
    page_title="AI Social Media Content Generator",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# --- Initialize Configuration ---
@st.cache_resource
def load_config() -> Optional[Config]:
    """
    Load and validate application configuration.
    
    Returns:
        Config object or None if configuration fails
    """
    try:
        config = Config.from_env()
        config.validate()
        logger.info(f"Configuration loaded successfully (env: {config.environment})")
        return config
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        st.error(f"⚠️ Configuration Error: {e}")
        st.info(
            "💡 **Setup Instructions:**\n"
            "1. Copy `.env.example` to `.env`\n"
            "2. Add your Gemini API key to `.env`\n"
            "3. Restart the application"
        )
        return None


# --- Initialize Content Generator ---
@st.cache_resource
def get_content_generator(_config: Config) -> Optional[GeminiContentGenerator]:
    """
    Initialize and cache content generator.
    
    Args:
        _config: Configuration object (underscore prevents hashing)
        
    Returns:
        GeminiContentGenerator or None if initialization fails
    """
    try:
        generator = GeminiContentGenerator(
            api_key=_config.gemini_api_key,
            temperature=_config.temperature
        )
        logger.info("Content generator initialized successfully")
        return generator
    except Exception as e:
        logger.error(f"Failed to initialize content generator: {e}")
        st.error(f"Failed to initialize AI model: {e}")
        return None


# --- Helper Function for Copy to Clipboard ---
def copy_to_clipboard_button(text_to_copy: str, button_text: str = "Copy", key: str = None):
    """
    Create an HTML button that copies text to clipboard.
    
    Args:
        text_to_copy: Text to copy
        button_text: Button label
        key: Unique key for the button
    """
    unique_id = f"copy_button_{key}" if key else f"copy_button_{hash(text_to_copy)}"
    # Escape backticks in the text (can't use backslash in f-string)
    escaped_text = text_to_copy.replace('`', '\\`')
    html_code = f"""
    <button id="{unique_id}" onclick="
        var text = `{escaped_text}`;
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
        background-color: #007bff;
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


# --- Main Application ---
def main():
    """Main application entry point."""
    
    # Load configuration
    config = load_config()
    if not config:
        st.stop()
    
    # Initialize content generator
    content_generator = get_content_generator(config)
    
    if not content_generator:
        st.stop()
    
    # --- UI Header ---
    st.title("🚀 AI-Powered Social Media Content Generator")
    st.markdown("""
    Generate engaging social media content using advanced AI. Upload an image,
    provide keywords, and let AI create platform-optimized captions, hashtags,
    and emojis.
    
    **Features:**
    - 🎨 Multi-modal AI (text + image analysis)
    - 🎯 Platform-specific optimization
    - ✨ Multiple caption variations
    """)
    
    # --- Sidebar for Advanced Options ---
    with st.sidebar:
        st.header("⚙️ System Status")
        st.markdown(f"**Environment:** `{config.environment}`")
        st.markdown(f"**Cache:** `{'Enabled' if config.cache_enabled else 'Disabled'}`")
        
        # GPU Status Display with Hardware Name
        from content_generator import SENTIMENT_ENABLED, GPU_HARDWARE
        
        if SENTIMENT_ENABLED and GPU_HARDWARE != "None" and GPU_HARDWARE != "CPU":
            st.success(f"🚀 **GPU Acceleration:** Active ({GPU_HARDWARE})")
            
            # Show additional GPU info if available
            try:
                import torch
                if torch.cuda.is_available():
                    vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
                    st.info(f"💾 **VRAM:** {vram_gb:.1f} GB")
            except:
                pass
        elif GPU_HARDWARE == "CPU":
            st.warning("⚠️ **GPU:** Not available (using CPU)")
            st.caption("Models running on CPU - slower inference")
        else:
            st.error("⚠️ **Sentiment Analysis:** Disabled")
            st.caption("Check environment: `conda activate GPU_RTX`")
            st.caption("Install: `pip install torch transformers`")
        
        # Sentiment Analysis Status
        if SENTIMENT_ENABLED:
            st.success("✅ **Sentiment Analysis:** Enabled")
        else:
            st.warning("⚠️ **Sentiment Analysis:** Disabled")
        
        # RAG Settings
        st.markdown("---")
        st.header("🧠 RAG Settings")
        
        if RAG_AVAILABLE:
            use_rag = st.checkbox(
                "Enable Context-Aware Generation",
                value=True,
                help="Retrieve similar brand examples for consistent content"
            )
            
            if use_rag:
                num_context_examples = st.slider(
                    "Context Examples",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="Number of similar examples to retrieve"
                )
                
                platform_filter = st.checkbox(
                    "Filter by Platform",
                    value=True,
                    help="Only retrieve examples from target platform"
                )
                
                st.success("✅ **RAG:** Enabled")
                st.info(f"🔍 Will retrieve {num_context_examples} similar examples")
            else:
                num_context_examples = 3
                platform_filter = True
                st.info("ℹ️ **RAG:** Disabled (standard generation)")
        else:
            use_rag = False
            num_context_examples = 3
            platform_filter = True
            st.warning("⚠️ **RAG:** Not available")
            st.caption("Install: `pip install -r requirements_rag.txt`")
        
        if config.debug:
            st.warning("🐛 Debug mode enabled")

    
    # --- Image Upload ---
    st.subheader("📸 Upload Image (Optional)")
    uploaded_file = st.file_uploader(
        "Choose an image to analyze",
        type=["png", "jpg", "jpeg"],
        help="The AI will analyze the image content and incorporate it into the captions"
    )
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        st.success("✅ Image uploaded successfully. AI will analyze this image.")
    
    # --- Input Section ---
    st.subheader("✍️ Content Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        keywords = st.text_area(
            "Keywords or Description",
            placeholder="e.g., AI in agriculture, new product launch, team celebration",
            height=100,
            help="Describe what your post is about"
        )
    
    with col2:
        post_type = st.selectbox(
            "Post Type/Tone",
            options=[
                "Inspirational",
                "Informative",
                "Promotional",
                "Announcement",
                "General",
                "Question/Engagement",
                "Behind-the-Scenes",
                "Tutorial/How-To",
                "Success Story"
            ],
            index=1,
            help="Select the tone and style for your post"
        )
    
    # --- Platform Selection ---
    st.subheader("🌐 Target Platforms")
    platforms_options = [
        "Instagram",
        "LinkedIn",
        "Twitter",
        "Facebook",
        "TikTok",
        "Pinterest",
        "YouTube Community"
    ]
    selected_platforms = st.multiselect(
        "Select platforms",
        options=platforms_options,
        default=["Instagram"],
        help="Content will be optimized for the selected platforms"
    )
    
    # --- Generation Options ---
    num_generations = st.slider(
        "Number of caption variations",
        min_value=1,
        max_value=min(5, config.max_generations),
        value=1,
        help="Generate multiple variations to choose from"
    )
    
    # --- Generate Button ---
    if st.button("🎨 Generate Content", type="primary", use_container_width=True):
        # Validation
        if not keywords and uploaded_file is None:
            st.warning("⚠️ Please enter keywords or upload an image to generate content.")
            return
        
        if not selected_platforms:
            st.warning("⚠️ Please select at least one social media platform.")
            return
        
        # Prepare request
        image_data = None
        image_mime_type = None
        
        if uploaded_file is not None:
            image_data = uploaded_file.getvalue()
            image_mime_type = uploaded_file.type
        
        request = ContentRequest(
            keywords=keywords or "",
            post_type=post_type,
            platforms=selected_platforms,
            num_generations=num_generations,
            image_data=image_data,
            image_mime_type=image_mime_type
        )
        
        # Generate content with or without RAG
        spinner_text = f"🤖 Generating {num_generations} caption(s) using AI..."
        if use_rag and RAG_AVAILABLE:
            spinner_text = f"🧠 Generating {num_generations} caption(s) with RAG context..."
        
        with st.spinner(spinner_text):
            try:
                # Use RAG pipeline if enabled
                if use_rag and RAG_AVAILABLE:
                    rag_pipeline = create_rag_pipeline(content_generator)
                    generated_posts = rag_pipeline.generate_with_context(
                        request,
                        num_examples=num_context_examples,
                        use_platform_filter=platform_filter
                    )
                else:
                    # Standard generation
                    generated_posts = content_generator.generate(request)
                
                # Display results
                st.success(f"✅ Successfully generated {len(generated_posts)} caption(s)!")
                st.subheader("✨ Your Generated Content")
                
                for i, post in enumerate(generated_posts):
                    st.markdown("---")
                    st.markdown(f"### 📝 Post #{i+1}")
                    
                    # Display caption with emojis
                    st.write(f"**Caption:** {post.caption} {post.emojis}")
                    
                    # Display hashtags
                    st.write(f"**Hashtags:** {' '.join(post.hashtags)}")
                    
                    # Display GPU-accelerated sentiment analysis
                    if post.sentiment:
                        # Color-code sentiment based on label
                        if "POSITIVE" in post.sentiment:
                            st.success(f"🎯 **Sentiment:** {post.sentiment}")
                        elif "NEGATIVE" in post.sentiment:
                            st.error(f"🎯 **Sentiment:** {post.sentiment}")
                        else:
                            st.info(f"🎯 **Sentiment:** {post.sentiment}")
                    
                    # Copy button
                    post_content = (
                        f"Caption: {post.caption} {post.emojis}\n"
                        f"Hashtags: {' '.join(post.hashtags)}"
                    )
                    copy_to_clipboard_button(
                        post_content,
                        button_text="📋 Copy This Post",
                        key=f"copy_post_{i}"
                    )
                
            except ContentGenerationError as e:
                st.error(f"❌ Content generation failed: {e}")
                logger.error(f"Generation error: {e}")
            
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")
                logger.exception("Unexpected error during generation")
    
    # --- Footer ---
    st.markdown("---")
    st.markdown("""
    ### 💡 Tips for Better Results
    - Be specific with your keywords
    - Upload high-quality images
    - Select appropriate post type for your content
    - Try generating multiple variations
    - Enable RAG for brand-consistent content
    
    **Technology:** Powered by Google Gemini AI • GPU-Accelerated ML • RAG Pipeline • Built with Streamlit
    
    ---
    *Part of B.Tech Computer Science & Engineering Project*  
    *DR. A.P.J. Abdul Kalam Technical University • IBM Skill Build Program Partnership with Edunet Foundation*
    
    **Features:** Multi-modal AI • Sentiment Analysis • Context-Aware Generation (RAG)
    """)


if __name__ == "__main__":
    main()
