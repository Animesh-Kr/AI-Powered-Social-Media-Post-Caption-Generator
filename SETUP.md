# Setup Instructions

## Quick Setup (5 minutes)

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

1. Copy the example environment file:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   ```

2. Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. Get your API key from: https://makersuite.google.com/app/apikey

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## Detailed Setup

### Prerequisites

- **Python 3.11+**: Download from https://www.python.org/downloads/
- **pip**: Comes with Python
- **Git**: For cloning the repository (optional)

### Installation Steps

1. **Create Virtual Environment** (Recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```bash
   python -c "import streamlit; import transformers; import torch; print('All dependencies installed successfully!')"
   ```

### Configuration Options

Edit `.env` to customize:

```bash
# Required
GEMINI_API_KEY=your_key_here

# Optional
ENVIRONMENT=development     # or production
CACHE_ENABLED=true         # Enable caching
MAX_GENERATIONS=5          # Max captions (1-10)
TEMPERATURE=0.7            # Creativity (0.0-1.0)
DEBUG=false                # Debug logging
```

---

## Troubleshooting

### Issue: Import errors

**Solution**: Ensure you've activated the virtual environment and installed all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: API key not found

**Solution**: Make sure `.env` file exists in the project root and contains:
```
GEMINI_API_KEY=your_actual_key
```

### Issue: Slow first run

**Solution**: First run downloads transformer models (~500MB). This is normal and only happens once.

---

## Running for the First Time

1. Activate virtual environment
2. Run `streamlit run app.py`
3. Wait for models to download (first time only)
4. Application opens in browser
5. Upload an image or enter keywords
6. Click "Generate Content"

---

## For Development

### Install Development Dependencies

```bash
pip install pytest black flake8 mypy
```

### Run Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black .
```

### Type Checking

```bash
mypy .
```

---

## Deployment

### Local Deployment

Already covered above - just run `streamlit run app.py`

### Cloud Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your repository
4. Add `GEMINI_API_KEY` to secrets
5. Deploy!

### Docker Deployment (Coming Soon)

```bash
docker build -t social-media-ai .
docker run -p 8501:8501 social-media-ai
```

---

## Support

If you encounter issues:
1. Check this guide
2. Review README.md
3. Check GitHub issues
4. Contact the author
