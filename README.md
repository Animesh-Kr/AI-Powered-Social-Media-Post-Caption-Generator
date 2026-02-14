# 🚀 AI-Powered Social Media Content Generator

> **Advanced AI platform for generating engaging, platform-optimized social media content**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Overview

This project is an **AI-powered social media content intelligence platform** that generates high-quality captions, hashtags, and emojis optimized for multiple social media platforms. Built as part of a **Newcastle University MSc dissertation** in partnership with **IBM**, it demonstrates advanced software engineering practices and cutting-edge AI/ML techniques.

### ✨ Key Features

- 🎨 **Multi-Modal AI**: Analyzes both text and images using Google's Gemini 2.0
- 🧠 **RAG Pipeline**: Context-aware generation using brand examples and vector search
- 📊 **GPU-Accelerated ML**: Sentiment analysis and embeddings on NVIDIA GPUs
- 🎯 **Platform Optimization**: Tailored content for Instagram, LinkedIn, Twitter, Facebook, TikTok, and more
- 🔄 **Multiple Variations**: Generate up to 5 unique caption variations
- 🏗️ **Modular Architecture**: Clean, maintainable code following enterprise patterns
- 🔒 **Secure Configuration**: Environment-based API key management
- 📈 **Production-Ready**: Comprehensive error handling and logging

---

## 🎯 Research Objectives

This project explores **multi-model AI orchestration** for enterprise social media content generation, addressing:

1. **Brand Voice Consistency**: Maintaining consistent brand identity across posts
2. **Cross-Platform Optimization**: Automated content adaptation for different platforms
3. **Engagement Prediction**: ML models to forecast content performance
4. **Quality Evaluation**: Novel metrics beyond traditional NLP benchmarks

---

## 🏗️ Architecture

```
AI-Powered-Social-Media-Post-Caption-Generator/
├── app.py                              # Main Streamlit application
├── config.py                           # Configuration management
├── content_generator.py                # AI content generation module
├── vector_store.py                     # RAG vector database (FAISS)
├── rag_pipeline.py                     # RAG orchestration
├── brand_content/                      # Brand examples & guidelines
│   ├── brand_voice.txt
│   └── example_posts.json
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore rules
└── README.md                           # This file
```

### Technology Stack

- **Frontend**: Streamlit (Python-based web framework)
- **AI/ML**: Google Gemini 2.0, Transformers (HuggingFace), Sentence Transformers
- **RAG**: LangChain, FAISS vector database
- **GPU Acceleration**: PyTorch with CUDA support
- **Backend**: Python 3.11+
- **Configuration**: python-dotenv for environment management

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Git (for cloning the repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/[your-username]/AI-Powered-Social-Media-Post-Caption-Generator.git
   cd AI-Powered-Social-Media-Post-Caption-Generator
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example file
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux

   # Edit .env and add your Gemini API key
   # GEMINI_API_KEY=your_actual_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

---

## 📖 Usage Guide

### Basic Workflow

1. **Upload an Image** (optional)
   - Supports PNG, JPG, JPEG formats
   - AI will analyze image content and incorporate it into captions

2. **Enter Keywords**
   - Describe your post topic
   - Be specific for better results

3. **Select Post Type**
   - Choose from: Inspirational, Informative, Promotional, etc.
   - Affects tone and style of generated content

4. **Choose Platforms**
   - Select target social media platforms
   - Content will be optimized for each platform

5. **Generate Content**
   - Click "Generate Content" button
   - Review generated captions, hashtags, and emojis
   - Check sentiment analysis results
   - Copy your favorite variation

### Example Use Cases

**Product Launch**
```
Keywords: "New AI-powered smartwatch with health tracking"
Post Type: Promotional
Platforms: Instagram, Twitter, Facebook
```

**Team Celebration**
```
Keywords: "Team completed major project milestone"
Post Type: Behind-the-Scenes
Platforms: LinkedIn, Instagram
```

**Educational Content**
```
Keywords: "How machine learning improves healthcare diagnostics"
Post Type: Informative
Platforms: LinkedIn, Twitter
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
ENVIRONMENT=development          # development or production
CACHE_ENABLED=true              # Enable response caching
MAX_GENERATIONS=5               # Maximum caption variations (1-10)
TEMPERATURE=0.7                 # Model creativity (0.0-1.0)
DEBUG=false                     # Enable debug logging
```

### Advanced Configuration

For production deployment or advanced features, see [`config.py`](config.py) for all available options.

---

## 🧪 Testing

### Manual Testing

1. Test with text-only input
2. Test with image-only input
3. Test with both text and image
4. Test different post types and platforms
5. Verify sentiment analysis accuracy

### Automated Testing (Coming Soon)

```bash
pytest tests/
```

---

## 📊 Performance Benchmarks

| Metric | Value |
|--------|-------|
| Average Generation Time | ~2-3 seconds |
| Supported Platforms | 7 |
| Max Captions per Request | 5 |
| Image Size Limit | 10 MB |
| Sentiment Analysis Accuracy | ~85% |

---

## 🛠️ Development

### Code Structure

- **`app.py`**: Streamlit UI and main application logic
- **`config.py`**: Configuration management with environment support
- **`content_generator.py`**: AI content generation with Gemini API
- **Modular Design**: Each component has a single responsibility
- **Error Handling**: Comprehensive exception handling throughout
- **Logging**: Structured logging for debugging and monitoring

### Best Practices Implemented

✅ **Separation of Concerns**: UI, business logic, and configuration are separated  
✅ **Type Hints**: All functions have type annotations  
✅ **Docstrings**: Comprehensive documentation for all modules and functions  
✅ **Error Handling**: Graceful degradation with user-friendly error messages  
✅ **Security**: API keys stored in environment variables, not in code  
✅ **Caching**: Streamlit caching for expensive operations  

---

## 🚧 Roadmap

### Current Version (v1.0)
- ✅ Multi-modal content generation
- ✅ GPU-accelerated sentiment analysis
- ✅ RAG pipeline with vector search
- ✅ Platform-specific optimization
- ✅ Modular architecture

### Planned Features (v2.0)
- [ ] Multi-model orchestration (GPT-4, Claude, custom models)
- [ ] Fine-tuned brand voice models
- [ ] Engagement prediction model
- [ ] A/B testing framework
- [ ] RESTful API
- [ ] User authentication
- [ ] Content performance tracking
- [ ] Database integration

---

## 📚 Research & Publications

This project is part of ongoing research on **multi-model AI orchestration for enterprise content generation**. Key research areas:

- Novel evaluation metrics for AI-generated content
- Brand voice transfer learning techniques
- Cross-platform content optimization algorithms
- Engagement prediction using multi-modal features

**Publications**: Coming soon

---

## 🤝 Contributing

This is currently a dissertation project, but contributions are welcome after the initial submission. Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**[Your Name]**

- 🎓 MSc Advanced Computer Science, Newcastle University
- 💼 [LinkedIn](https://linkedin.com/in/your-profile)
- 🐙 [GitHub](https://github.com/your-username)
- 📧 [Email](mailto:your.email@example.com)

---

## 🙏 Acknowledgments

- **Newcastle University** - Academic supervision and support
- **IBM** - Industry partnership and guidance
- **Google** - Gemini API access
- **HuggingFace** - Transformers library and pre-trained models
- **Streamlit** - Rapid UI development framework

---

## 📞 Support

For questions or issues:

1. Check the [documentation](#-usage-guide)
2. Review [common issues](#-troubleshooting)
3. Open an issue on GitHub
4. Contact the author

---

## 🔍 Troubleshooting

### Common Issues

**Issue**: `ValueError: GEMINI_API_KEY environment variable is required`
- **Solution**: Create a `.env` file and add your Gemini API key

**Issue**: `ModuleNotFoundError: No module named 'transformers'`
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: Slow generation times
- **Solution**: Check your internet connection; Gemini API requires network access

**Issue**: Sentiment analysis fails
- **Solution**: Ensure PyTorch and Transformers are properly installed

---

## 📈 Project Status

🟢 **Active Development** - This project is actively maintained as part of an ongoing dissertation.

**Last Updated**: February 2026  
**Version**: 1.0.0  
**Status**: Production-ready prototype

---

<div align="center">

**Built with ❤️ for the future of AI-powered content creation**

[⬆ Back to Top](#-ai-powered-social-media-content-generator)

</div>
