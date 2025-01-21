# src/utils/model_downloader.py
import os
from pathlib import Path
from huggingface_hub import hf_hub_download, HfApi
import sys
import shutil

class ModelDownloader:
    """Handles downloading and caching of models from Hugging Face Hub"""
    
    KOKORO_REPO = "hexgrad/Kokoro-82M"
    MODEL_CACHE_DIR = Path.home() / ".cache" / "kokoro-tts"
    
    # Separate directories for models and code
    MODEL_DIR = MODEL_CACHE_DIR / "models"
    CODE_DIR = MODEL_CACHE_DIR / "src"
    VOICE_DIR = MODEL_CACHE_DIR / "voices"
    
    # Required files
    MODEL_FILES = [
        "kokoro-v0_19.pth",
        "kokoro-v0_19.onnx",  # ONNX version of the model
    ]
    
    CODE_FILES = [
        "kokoro.py",
        "models.py",
        "config.json",
        "istftnet.py",
        "plbert.py",
        "__init__.py",
    ]

    @classmethod
    def get_hf_token(cls):
        """Get Hugging Face token from environment or prompt user"""
        token = os.getenv('HF_TOKEN')
        if not token:
            print("\nHugging Face token is required to download the model.")
            print("You can get your token from: https://huggingface.co/settings/tokens")
            token = input("Please enter your Hugging Face token: ").strip()
            
            # Optionally save to environment for future use
            save = input("Would you like to save this token to your environment? (y/n): ").lower()
            if save == 'y':
                with open(os.path.expanduser("~/.bashrc"), "a") as f:
                    f.write(f'\nexport HF_TOKEN="{token}"')
                print("Token saved to ~/.bashrc. Please restart your terminal or run 'source ~/.bashrc'")
        
        return token

    @classmethod
    def verify_token(cls, token):
        """Verify that the token has access to the repository"""
        try:
            api = HfApi(token=token)
            api.repo_info(repo_id=cls.KOKORO_REPO)
            return True
        except Exception as e:
            print(f"Error verifying token: {e}")
            return False

    @classmethod
    def setup_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.MODEL_DIR.mkdir(parents=True, exist_ok=True)
        cls.CODE_DIR.mkdir(parents=True, exist_ok=True)
        cls.VOICE_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def download_files(cls, token):
        """Download all required files from Hugging Face Hub"""
        cls.setup_directories()
        
        print("Downloading model files...")
        for filename in cls.MODEL_FILES:
            try:
                if (cls.MODEL_DIR / filename).exists():
                    print(f"File {filename} already exists, skipping...")
                    continue
                    
                print(f"Downloading {filename}...")
                hf_hub_download(
                    repo_id=cls.KOKORO_REPO,
                    filename=filename,
                    local_dir=cls.MODEL_DIR,
                    token=token
                )
                print(f"Successfully downloaded {filename}")
            except Exception as e:
                print(f"Error downloading {filename}: {e}")
                if "not found" in str(e).lower():
                    print(f"Note: {filename} might be optional, continuing...")
                    continue
                raise

        print("\nDownloading source code files...")
        for filename in cls.CODE_FILES:
            try:
                if (cls.CODE_DIR / filename).exists():
                    print(f"File {filename} already exists, skipping...")
                    continue
                    
                print(f"Downloading {filename}...")
                hf_hub_download(
                    repo_id=cls.KOKORO_REPO,
                    filename=filename,
                    local_dir=cls.CODE_DIR,
                    token=token
                )
                print(f"Successfully downloaded {filename}")
            except Exception as e:
                print(f"Error downloading {filename}: {e}")
                if filename == "__init__.py":
                    print("Creating empty __init__.py file...")
                    (cls.CODE_DIR / filename).touch()
                    continue
                elif "not found" in str(e).lower():
                    print(f"Note: {filename} might be optional, continuing...")
                    continue
                raise

        # Create an empty __init__.py if it doesn't exist
        init_file = cls.CODE_DIR / "__init__.py"
        if not init_file.exists():
            init_file.touch()

        # Add CODE_DIR to Python path
        code_dir_str = str(cls.CODE_DIR)
        if code_dir_str not in sys.path:
            sys.path.insert(0, code_dir_str)

    @classmethod
    def get_model_path(cls, ensure_downloaded=True):
        """Get path to the Kokoro model, downloading if necessary"""
        model_path = cls.MODEL_DIR / "kokoro-v0_19.pth"
        
        if ensure_downloaded and not model_path.exists():
            token = cls.get_hf_token()
            if not cls.verify_token(token):
                raise ValueError("Invalid or unauthorized Hugging Face token")
            cls.download_files(token)
            
        return model_path

    @classmethod
    def get_voice_path(cls, voice_name="af", ensure_downloaded=True):
        """Get path to a specific voice pack, downloading if necessary"""
        voice_path = cls.VOICE_DIR / f"{voice_name}.pt"
        
        if ensure_downloaded and not voice_path.exists():
            token = cls.get_hf_token()
            if not cls.verify_token(token):
                raise ValueError("Invalid or unauthorized Hugging Face token")
            
            print(f"\nDownloading voice pack: {voice_name}")
            try:
                hf_hub_download(
                    repo_id=cls.KOKORO_REPO,
                    filename=f"voices/{voice_name}.pt",
                    local_dir=cls.MODEL_CACHE_DIR,
                    token=token
                )
                print(f"Voice pack {voice_name} downloaded successfully!")
            except Exception as e:
                print(f"Error downloading voice pack: {e}")
                raise
            
        return voice_path

    @classmethod
    def ensure_code_path(cls):
        """Ensure the code directory is in Python path"""
        code_dir_str = str(cls.CODE_DIR)
        if code_dir_str not in sys.path:
            sys.path.insert(0, code_dir_str)