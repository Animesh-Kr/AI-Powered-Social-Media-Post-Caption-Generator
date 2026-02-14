"""
GPU Environment Diagnostic Script

This script verifies that your NVIDIA drivers, CUDA, PyTorch, and conda environment
are correctly configured for GPU acceleration.

Run this in your PowerShell with GPU_RTX environment activated:
    conda activate GPU_RTX
    python gpu_diagnostic.py
"""

import sys
import subprocess

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_python_environment():
    """Check Python version and environment"""
    print_section("Python Environment")
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    
    # Check if in conda environment
    if 'conda' in sys.executable.lower() or 'GPU_RTX' in sys.executable:
        print("✅ Running in conda environment")
    else:
        print("⚠️  WARNING: Not running in conda environment!")
        print("   Run: conda activate GPU_RTX")

def check_nvidia_drivers():
    """Check NVIDIA driver installation"""
    print_section("NVIDIA Drivers")
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ NVIDIA drivers installed")
            print("\nGPU Information:")
            # Print first few lines of nvidia-smi output
            lines = result.stdout.split('\n')[:10]
            for line in lines:
                print(line)
        else:
            print("❌ nvidia-smi command failed")
            print("   Install NVIDIA drivers from: https://www.nvidia.com/drivers")
    except FileNotFoundError:
        print("❌ nvidia-smi not found")
        print("   NVIDIA drivers may not be installed")

def check_pytorch():
    """Check PyTorch installation and CUDA support"""
    print_section("PyTorch & CUDA")
    try:
        import torch
        print(f"✅ PyTorch installed: {torch.__version__}")
        
        # Check CUDA availability
        cuda_available = torch.cuda.is_available()
        print(f"CUDA Available: {cuda_available}")
        
        if cuda_available:
            print(f"✅ CUDA Version: {torch.version.cuda}")
            print(f"✅ GPU Count: {torch.cuda.device_count()}")
            
            # Get GPU details
            for i in range(torch.cuda.device_count()):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_props = torch.cuda.get_device_properties(i)
                vram_gb = gpu_props.total_memory / 1e9
                
                print(f"\nGPU {i}: {gpu_name}")
                print(f"  VRAM: {vram_gb:.2f} GB")
                print(f"  Compute Capability: {gpu_props.major}.{gpu_props.minor}")
        else:
            print("❌ CUDA not available")
            print("   Install CUDA-enabled PyTorch:")
            print("   pip install torch --index-url https://download.pytorch.org/whl/cu118")
            
    except ImportError:
        print("❌ PyTorch not installed")
        print("   Install: pip install torch")

def check_transformers():
    """Check Transformers library"""
    print_section("Transformers Library")
    try:
        import transformers
        print(f"✅ Transformers installed: {transformers.__version__}")
        
        # Try to load a small model
        print("\nTesting GPU model loading...")
        try:
            from transformers import pipeline
            import torch
            
            device = 0 if torch.cuda.is_available() else -1
            device_name = "GPU" if device == 0 else "CPU"
            
            print(f"Loading sentiment analysis model on {device_name}...")
            analyzer = pipeline("sentiment-analysis", device=device)
            
            # Test inference
            result = analyzer("This is a test sentence")
            print(f"✅ Model loaded successfully on {device_name}")
            print(f"   Test inference result: {result}")
            
        except Exception as e:
            print(f"❌ Model loading failed: {e}")
            
    except ImportError:
        print("❌ Transformers not installed")
        print("   Install: pip install transformers")

def check_langchain_rag():
    """Check RAG dependencies"""
    print_section("RAG Dependencies (Optional)")
    
    dependencies = [
        ('langchain', 'LangChain'),
        ('langchain_community', 'LangChain Community'),
        ('faiss', 'FAISS'),
        ('sentence_transformers', 'Sentence Transformers')
    ]
    
    for module_name, display_name in dependencies:
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {display_name}: {version}")
        except ImportError:
            print(f"⚠️  {display_name}: Not installed")
    
    print("\nTo install RAG dependencies:")
    print("pip install langchain langchain-community faiss-cpu sentence-transformers")

def check_streamlit():
    """Check Streamlit installation"""
    print_section("Streamlit")
    try:
        import streamlit
        print(f"✅ Streamlit installed: {streamlit.__version__}")
        print("\nTo run the app with correct environment:")
        print("  conda activate GPU_RTX")
        print("  python -m streamlit run app.py")
    except ImportError:
        print("❌ Streamlit not installed")
        print("   Install: pip install streamlit")

def main():
    """Run all diagnostic checks"""
    print("\n" + "🔍 GPU ENVIRONMENT DIAGNOSTIC TOOL" + "\n")
    print("This script checks your GPU setup for the AI Content Generator")
    
    check_python_environment()
    check_nvidia_drivers()
    check_pytorch()
    check_transformers()
    check_langchain_rag()
    check_streamlit()
    
    print_section("Summary")
    print("If all checks passed (✅), your environment is ready!")
    print("\nTo launch the app:")
    print("  1. conda activate GPU_RTX")
    print("  2. python -m streamlit run app.py")
    print("\nIf any checks failed (❌), follow the installation instructions above.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
