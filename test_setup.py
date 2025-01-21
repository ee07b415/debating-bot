import os
import sys
import platform
from pathlib import Path

def check_kokoro_setup():
    """Verify Kokoro files are present and in Python path"""
    print("\nChecking Kokoro setup...")
    
    # Get the cache directory where files should be
    cache_dir = Path.home() / ".cache" / "kokoro-tts" / "src"
    
    # Print current Python path
    print("\nCurrent Python path:")
    for p in sys.path:
        print(f"  {p}")
    
    # Check if cache directory exists
    print(f"\nChecking cache directory: {cache_dir}")
    if not cache_dir.exists():
        print("Cache directory not found!")
        return False
        
    # List files in cache directory
    print("\nFiles in cache directory:")
    try:
        files = list(cache_dir.glob("*"))
        for f in files:
            print(f"  {f.name}")
    except Exception as e:
        print(f"Error listing cache directory: {e}")
    
    # Check for kokoro.py specifically
    kokoro_file = cache_dir / "kokoro.py"
    print(f"\nLooking for kokoro.py at: {kokoro_file}")
    if not kokoro_file.exists():
        print("kokoro.py not found!")
        return False
        
    # Add to Python path if not already there
    if str(cache_dir) not in sys.path:
        print(f"\nAdding {cache_dir} to Python path")
        sys.path.insert(0, str(cache_dir))
    else:
        print("\nCache directory already in Python path")
    
    # Try importing kokoro
    print("\nTrying to import kokoro...")
    try:
        import kokoro
        print("Successfully imported kokoro!")
        return True
    except ImportError as e:
        print(f"Failed to import kokoro: {e}")
        return False

def verify_espeak_setup():
    """Verify eSpeak setup and environment variables"""
    print("\nChecking eSpeak setup...")
    is_windows = platform.system() == "Windows"
    
    if is_windows:
        espeak_path = Path(r"C:\Program Files\eSpeak NG")
        
        # Check if eSpeak is installed
        if not espeak_path.exists():
            print("Warning: eSpeak NG installation not found!")
            return False
            
        # Set environment variables if not set
        if not os.environ.get("PHONEMIZER_ESPEAK_LIBRARY"):
            os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = str(espeak_path / "libespeak-ng.dll")
        if not os.environ.get("PHONEMIZER_ESPEAK_PATH"):
            os.environ["PHONEMIZER_ESPEAK_PATH"] = str(espeak_path / "espeak-ng.exe")
    
    # Verify environment variables
    library_path = os.environ.get("PHONEMIZER_ESPEAK_LIBRARY")
    binary_path = os.environ.get("PHONEMIZER_ESPEAK_PATH")
    
    print(f"PHONEMIZER_ESPEAK_LIBRARY: {library_path}")
    print(f"PHONEMIZER_ESPEAK_PATH: {binary_path}")
    
    if not library_path or not binary_path:
        print("\nMissing eSpeak environment variables!")
        if is_windows:
            print("Please run the setup.bat script to configure the environment.")
        return False
        
    # Verify files exist
    if not Path(library_path).exists():
        print(f"\nLibrary not found at: {library_path}")
        return False
    if not Path(binary_path).exists():
        print(f"\nBinary not found at: {binary_path}")
        return False
        
    print("eSpeak setup verified successfully!")
    return True

def verify_environment():
    """Verify all required environment variables and dependencies"""
    all_good = True
    
    # Check eSpeak setup
    if not verify_espeak_setup():
        all_good = False
    
    # Check Kokoro setup
    if not check_kokoro_setup():
        all_good = False
    
    # Check API keys
    print("\nChecking API keys...")
    required_vars = ['ANTHROPIC_API_KEY', 'HF_TOKEN']
    for var in required_vars:
        if not os.getenv(var):
            print(f"Warning: {var} not found in environment!")
            all_good = False
    
    if not all_good:
        print("\nSome environment checks failed. Please check the messages above.")
    else:
        print("\nAll environment checks passed!")
    
    return all_good

if __name__ == "__main__":
    verify_environment()