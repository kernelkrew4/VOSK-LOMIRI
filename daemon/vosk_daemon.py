#!/usr/bin/env python3

import asyncio
import websockets
import json
import sounddevice as sd
import queue
from vosk import Model, KaldiRecognizer
import os
from datetime import datetime

# -------------------------------
# Globals
# -------------------------------
SAMPLE_RATE = 16000
model = None
recognizer = None
recording = False
q = queue.Queue()
transcript = []  # store recognized lines


# -------------------------------
# Audio callback
# -------------------------------
def callback(indata, frames, time, status):
    if recording:
        q.put(bytes(indata))


# -------------------------------
# Audio Streaming
# -------------------------------
async def stream_audio(ws):
    global recording, transcript

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        while recording:
            await asyncio.sleep(0.1)
            if not q.empty():
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    res = json.loads(recognizer.Result())
                    text = res.get("text", "")
                    if text:
                        transcript.append(text)
                    await ws.send(json.dumps({"final": text}))
                else:
                    res = json.loads(recognizer.PartialResult())
                    await ws.send(json.dumps({"partial": res.get("partial", "")}))


# -------------------------------
# WebSocket Client Handler
# -------------------------------
async def handle_client(ws):
    global model, recognizer, recording, transcript
    print("[daemon] Client connected")

    try:
        async for message in ws:
            data = json.loads(message)
            cmd = data.get("cmd")

            # Load model
            if cmd == "load":
                model_name = data.get("model", "vosk-model-small-en-in-0.4")
                if not os.path.exists(model_name):
                    await ws.send(json.dumps({"error": f"Model {model_name} not found"}))
                    continue
                print(f"[daemon] Loading model: {model_name}")
                model = Model(model_name)
                recognizer = KaldiRecognizer(model, SAMPLE_RATE)
                await ws.send(json.dumps({"status": f"Loaded {model_name}"}))

            # Start recording
            elif cmd == "start":
                if not recognizer:
                    await ws.send(json.dumps({"error": "No model loaded"}))
                    continue
                print("[daemon] Starting recording...")
                transcript = []  # reset transcript each time
                recording = True
                asyncio.create_task(stream_audio(ws))
                await ws.send(json.dumps({"status": "Recording started"}))

            # Stop recording
            elif cmd == "stop":
                print("[daemon] Stopping recording...")
                recording = False
                await ws.send(json.dumps({"status": "Stopped"}))

            # Save transcript
            elif cmd == "save":
                if not transcript:
                    await ws.send(json.dumps({"error": "No transcript to save"}))
                else:
                    filename = f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    filepath = os.path.join(os.getcwd(), filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write("\n".join(transcript))
                    await ws.send(json.dumps({"status": f"Transcript saved as {filename}"}))

            else:
                await ws.send(json.dumps({"error": "Unknown command"}))

    except Exception as e:
        print(f"[daemon] Connection error: {e}")


# -------------------------------
# Main entrypoint
# -------------------------------
async def main():
    print("[daemon] Listening on ws://127.0.0.1:8765")
    async with websockets.serve(handle_client, "127.0.0.1", 8765):
        await asyncio.Future()  # keep alive forever


if __name__ == "__main__":
    asyncio.run(main())
