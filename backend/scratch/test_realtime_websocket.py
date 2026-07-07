import sys
import os
import wave
import json
import asyncio
import websockets

wav_path = os.path.dirname(os.path.abspath(__file__)) + "/test_whisper.wav"
base_ws_url = "ws://127.0.0.1:8000/ws/stream"

async def test_realtime_websocket():
    print("--- Test Real-Time WebSocket Streaming Endpoint ---")
    
    assert os.path.exists(wav_path), f"Sample audio file {wav_path} not found!"
    
    print(f"Connecting to live WebSocket server at: {base_ws_url}")
    
    async with websockets.connect(base_ws_url) as ws:
        print("1. Connected to WebSocket ws/stream.")
        
        # Send initial configuration
        config = {
            "expected_text": "The quick brown fox jumps over the lazy dog.",
            "language": "English"
        }
        await ws.send(json.dumps(config))
        print("2. Sent configuration JSON.")
        
        # Read the WAV file and stream raw PCM data in chunks
        with wave.open(wav_path, "rb") as wav_file:
            n_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            framerate = wav_file.getframerate()
            n_frames = wav_file.getnframes()
            
            print(f"   Audio details: {n_channels} channels, {sample_width} bytes/sample, {framerate}Hz, {n_frames} total frames")
            
            chunk_size = 4096  # 256ms of audio at 16kHz
            print("3. Streaming PCM chunks...")
            
            sent_bytes = 0
            while True:
                data = wav_file.readframes(chunk_size)
                if not data:
                    break
                await ws.send(data)
                sent_bytes += len(data)
                # Sleep briefly to simulate real-time stream intervals
                await asyncio.sleep(0.01)
                
            print(f"   Sent {sent_bytes} bytes of raw PCM.")
            
        print("4. Signal stop command to backend...")
        # Send stop message to close segment buffer
        await ws.send(json.dumps({"type": "stop"}))
        
        print("5. Waiting for real-time transcription feedback from server...")
        
        # Collect responses
        feedbacks = []
        try:
            # We wait for messages until connection closes or timeout
            while True:
                try:
                    msg_str = await asyncio.wait_for(ws.recv(), timeout=90.0)
                    msg = json.loads(msg_str)
                    print("\nReceived message from WebSocket:")
                    # Truncate large word lists to keep print statements readable
                    words_summary = msg.get("words", [])
                    print(f" - Type: {msg.get('type')}")
                    print(f" - Transcription: '{msg.get('transcription')}'")
                    print(f" - Accuracy: {msg.get('accuracy')}%")
                    print(f" - Word Alignment Count: {len(words_summary)}")
                    
                    if msg.get("type") == "feedback":
                        feedbacks.append(msg)
                except asyncio.TimeoutError:
                    print("   Timed out waiting for message.")
                    break
        except websockets.exceptions.ConnectionClosed:
            print("   Connection closed by server.")
            
        assert len(feedbacks) > 0, "No feedback messages received from the WebSocket!"
        print(f"\nSuccessfully received {len(feedbacks)} real-time feedback updates.")
        print("Real-time WebSocket streaming checks completed successfully!")

if __name__ == "__main__":
    try:
        asyncio.run(test_realtime_websocket())
    except ConnectionRefusedError:
        print("\n[ERROR] Connection refused. Please ensure uvicorn server is running on port 8000!")
        sys.exit(1)
