"""
Quick Environment Test
Run this to verify your setup before launching the full app
"""

print("🔍 Testing GPU Environment...\n")

# Test 1: Python Environment
print("[1/5] Python Environment")
import sys
print(f"  ✅ Python: {sys.version.split()[0]}")
print(f"  📁 Location: {sys.executable}")

# Test 2: PyTorch
print("\n[2/5] PyTorch & CUDA")
try:
    import torch
    print(f"  ✅ PyTorch: {torch.__version__}")
    if torch.cuda.is_available():
        print(f"  ✅ CUDA: Available")
        print(f"  🎯 GPU: {torch.cuda.get_device_name(0)}")
    else:
        print(f"  ⚠️  CUDA: Not available (CPU mode)")
except ImportError:
    print(f"  ❌ PyTorch not installed")

# Test 3: Transformers
print("\n[3/5] Transformers")
try:
    import transformers
    print(f"  ✅ Transformers: {transformers.__version__}")
except ImportError:
    print(f"  ❌ Transformers not installed")

# Test 4: Streamlit
print("\n[4/5] Streamlit")
try:
    import streamlit
    print(f"  ✅ Streamlit: {streamlit.__version__}")
except ImportError:
    print(f"  ❌ Streamlit not installed")

# Test 5: RAG Dependencies (Optional)
print("\n[5/5] RAG Dependencies (Optional)")
try:
    import langchain
    import faiss
    import sentence_transformers
    print(f"  ✅ RAG: All dependencies installed")
except ImportError as e:
    print(f"  ⚠️  RAG: Some dependencies missing")
    print(f"     Install with: pip install -r requirements.txt")

# Summary
print("\n" + "="*50)
print("Summary:")
print("  If all core tests passed (✅), you're ready!")
print("  Launch app: python -m streamlit run app.py")
print("="*50)
