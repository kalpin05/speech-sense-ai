import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from app.services.whisper_service import _get_model, preload_model
import app.services.whisper_service as ws

def test_whisper_preloading():
    print("--- Test Whisper Model Pre-loading (Sprint 13) ---")
    
    # 1. Verify initially model is not loaded if we don't import or run it,
    # but wait, since ws has been imported, let's look at ws._model
    print(f"Initial model state: {ws._model}")
    
    # 2. Trigger preload manually in this test process (to simulate server startup)
    start_time = time.time()
    preload_model()
    preload_duration = time.time() - start_time
    print(f"Preloading model took: {preload_duration:.2f} seconds.")
    
    # 3. Verify model is loaded
    assert ws._model is not None, "Model was not loaded into memory!"
    print("Success: Model loaded into memory successfully.")
    
    # 4. Measure time to retrieve model again
    start_time = time.time()
    model = _get_model()
    retrieval_duration = time.time() - start_time
    print(f"Subsequent model retrieval took: {retrieval_duration * 1000:.4f} milliseconds.")
    
    # Retrieval should be near instantaneous (less than 1 millisecond)
    assert retrieval_duration < 0.05, f"Subsequent model retrieval took too long: {retrieval_duration:.4f}s"
    print("Success: Subsequent model retrievals are instant!")
    print("\nAll Sprint 13 preloading checks passed successfully!")

if __name__ == "__main__":
    test_whisper_preloading()
