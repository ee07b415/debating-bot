# src/models/audio_model.py
import asyncio
import torch
import sounddevice as sd
import sys
from pathlib import Path
from src.utils.model_downloader import ModelDownloader

class KokoroManager:
    def __init__(self, voice_name='af'):
        """
        Initialize Kokoro TTS manager
        Args:
            voice_name: Voice to use (af, af_bella, af_sarah, etc.)
        """
        print("Initializing KokoroManager...")
        
        # First, ensure model files are downloaded
        self._initialize_kokoro()
        
        # Now try to import Kokoro modules
        try:
            from kokoro import generate
            from models import build_model
            print("Successfully imported Kokoro modules")
        except ImportError as e:
            print(f"Error importing Kokoro: {e}")
            print("Python path:", sys.path)
            raise
        
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")
        
        # Get model and voice paths
        model_path = ModelDownloader.get_model_path()
        voice_path = ModelDownloader.get_voice_path(voice_name)
        print(f"Model path: {model_path}")
        print(f"Voice path: {voice_path}")
        
        # Load model and voice pack
        self.model = build_model(str(model_path), self.device)
        self.voice_pack = torch.load(str(voice_path), weights_only=True).to(self.device)
        self.voice_name = voice_name
        
        # Initialize audio queue and playback
        self.audio_queue = asyncio.Queue()
        self.is_playing = False
        self.queue_processor_active = True
        self._setup_audio()
        self.audio_complete = asyncio.Event()
        
        # Store generate function
        self.generate_fn = generate
        print("KokoroManager initialization complete!")

    def _initialize_kokoro(self):
        """Ensure Kokoro files are downloaded and in Python path"""
        print("\nInitializing Kokoro environment...")
        
        # Get the cache directory
        cache_dir = Path.home() / ".cache" / "kokoro-tts"
        src_dir = cache_dir / "src"
        
        # Add src directory to Python path
        if str(src_dir) not in sys.path:
            print(f"Adding Kokoro to Python path: {src_dir}")
            sys.path.insert(0, str(src_dir))
            
        print("Current Python path:")
        for p in sys.path:
            print(f"  {p}")
        
        # Verify required files exist
        required_files = ['kokoro.py', 'models.py']
        for file in required_files:
            file_path = src_dir / file
            if not file_path.exists():
                print(f"\nMissing required file: {file_path}")
                print("\nContents of cache directory:")
                print_directory_contents(cache_dir)
                raise FileNotFoundError(f"Required file not found: {file_path}")
                
        print("Kokoro files verified successfully")

    def _setup_audio(self):
        """Initialize audio playback system"""
        self.sample_rate = 24000  # Kokoro outputs 24kHz audio
        sd.default.samplerate = self.sample_rate
        sd.default.channels = 1

    async def generate_speech(self, text, output_file="test.wav"):
        """Generate speech from text using Kokoro"""
        try:
            audio, phonemes = self.generate_fn(
                self.model, 
                text, 
                self.voice_pack, 
                lang=self.voice_name[0]
            )
            
            if isinstance(audio, torch.Tensor):
                audio = audio.cpu().numpy()
            debug_path = Path(output_file)
            if output_file:
                import scipy.io.wavfile
                scipy.io.wavfile.write(output_file, self.sample_rate, audio)
                print(f"Saved debug audio to: {debug_path.absolute()}")
            
            return audio
            
        except Exception as e:
            print(f"Error generating speech: {e}")
            return None

    async def play_audio(self, audio_data):
        """Play audio data with sync"""
        try:
            if audio_data is None:
                print("No audio data to play!")
                return
            
            if len(audio_data.shape) == 1:
                audio_data = audio_data.reshape(-1, 1)
                
            # Reset the completion event
            self.audio_complete.clear()
            self.is_playing = True
            
            # Create a callback for when audio finishes
            def callback(outdata, frames, time, status):
                if status:
                    print(f'Status: {status}')
                try:
                    if len(audio_data[self.position:]) >= frames:
                        outdata[:] = audio_data[self.position:self.position + frames]
                        self.position += frames
                    else:
                        outdata[:len(audio_data[self.position:])] = audio_data[self.position:]
                        outdata[len(audio_data[self.position:]):] = 0
                        raise sd.CallbackStop()
                except Exception as e:
                    print(f"Callback error: {e}")
                    raise sd.CallbackStop()
                    
            self.position = 0
            # Start playback with callback
            stream = sd.OutputStream(
                samplerate=self.sample_rate,
                channels=1,
                callback=callback,
                finished_callback=lambda: self.audio_complete.set()
            )
            
            with stream:
                try:
                    await asyncio.wait_for(self.audio_complete.wait(), timeout=30.0)
                except asyncio.TimeoutError:
                    print("Audio playback timed out")
                    
        except Exception as e:
            print(f"Error playing audio: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_playing = False

    async def queue_audio(self, text):
        """Queue text for audio processing"""
        if self.queue_processor_active:
            await self.audio_queue.put(text)
            return True
        return False

    async def process_audio_queue(self):
        """Process audio queue with better error handling"""
        print("Starting audio queue processor...")
        while self.queue_processor_active:
            try:
                # Use timeout to allow checking queue_processor_active
                try:
                    text = await asyncio.wait_for(self.audio_queue.get(), timeout=0.1)
                except asyncio.TimeoutError:
                    continue
                    
                if text is None:  # Sentinel value for shutdown
                    break
                    
                print(f"Processing text for audio: {text[:50]}...")
                audio_data = await self.generate_speech(text)
                if audio_data is not None:
                    await self.play_audio(audio_data)
                
            except asyncio.CancelledError:
                print("Audio queue processor was cancelled")
                break
            except Exception as e:
                print(f"Error in audio queue processor: {e}")
                import traceback
                traceback.print_exc()
                await asyncio.sleep(1)
        
        print("Audio queue processor stopped")

    async def stop_audio(self):
        """Stop audio processing gracefully"""
        print("Stopping audio manager...")
        self.queue_processor_active = False
        
        # Clear the queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except asyncio.QueueEmpty:
                break
        
        # Add sentinel value to ensure the processor exits
        await self.audio_queue.put(None)
        
        # Stop any playing audio
        if self.is_playing:
            sd.stop()
            self.is_playing = False
            self.audio_complete.set()

def print_directory_contents(path, indent=""):
    """Helper function to print directory contents recursively"""
    try:
        for item in path.iterdir():
            print(f"{indent}{item.name}")
            if item.is_dir():
                print_directory_contents(item, indent + "  ")
    except Exception as e:
        print(f"Error listing directory {path}: {e}")