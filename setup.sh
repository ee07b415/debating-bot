# setup.py
from setuptools import setup, find_packages

setup(
    name="detective-game",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Core dependencies
        'torch>=2.0.0',
        'transformers>=4.36.0',
        'peft>=0.7.0',
        
        # Model and training
        'accelerate>=0.25.0',
        'bitsandbytes>=0.41.0',
        'sentencepiece>=0.1.99',
        'protobuf>=3.20.0',
        
        # Utilities
        'tqdm>=4.66.1',
        'numpy>=1.24.0',
        'pandas>=2.0.0',
        'safetensors>=0.4.0',
        
        # Optional but recommended
        'gradio>=4.0.0',
        'wandb>=0.15.0',
        
        # API
        'anthropic>=0.43.1',
        
        # Audio and TTS
        'python-dotenv>=1.0.0',
        'huggingface_hub>=0.19.0',
        'phonemizer>=3.0.0',
        'scipy>=1.11.0',
        'munch>=4.0.0',
        'sounddevice>=0.4.6',
    ],
    python_requires='>=3.8',
)

# scripts/setup.sh
#!/bin/bash

# Check the operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Installing system dependencies for Linux..."
    sudo apt-get update
    sudo apt-get install -y espeak-ng python3-sounddevice portaudio19-dev
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Installing system dependencies for macOS..."
    brew install espeak
    brew install portaudio
    
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "For Windows users:"
    echo "Please install eSpeak NG from: https://github.com/espeak-ng/espeak-ng/releases"
    echo "After installation, make sure to add it to your system PATH"
    echo ""
    echo "You'll also need to install the Microsoft Visual C++ Redistributable:"
    echo "https://aka.ms/vs/17/release/vc_redist.x64.exe"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -e .

echo "Setup complete!"

# README.md
# Detective Mystery Game

An AI-powered detective game with voice interactions.

## Prerequisites

### System Dependencies

Before installing the Python packages, you need to install some system dependencies:

#### Linux
```bash
sudo apt-get update
sudo apt-get install -y espeak-ng python3-sounddevice portaudio19-dev
```

#### macOS
```bash
brew install espeak
brew install portaudio
```

#### Windows
1. Download and install eSpeak NG from [GitHub Releases](https://github.com/espeak-ng/espeak-ng/releases)
2. Add eSpeak to your system PATH
3. Install [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/detective-game.git
cd detective-game
```

2. Run the setup script:
```bash
# Linux/macOS
./scripts/setup.sh

# Windows
# Run setup.bat (or follow manual installation steps)
```

3. Create a .env file in the project root:
```
ANTHROPIC_API_KEY=your_api_key_here
HF_TOKEN=your_huggingface_token_here
```

### Running the Game

```bash
python src/main.py
```

# scripts/setup.bat
@echo off
echo Installing system dependencies for Windows...
echo Please make sure you have installed:
echo 1. eSpeak NG from: https://github.com/espeak-ng/espeak-ng/releases
echo 2. Microsoft Visual C++ Redistributable from: https://aka.ms/vs/17/release/vc_redist.x64.exe

echo.
echo Installing Python dependencies...
pip install -e .

echo.
echo Setup complete!
pause