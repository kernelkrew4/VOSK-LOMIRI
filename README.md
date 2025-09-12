Setup Instructions
1. Clone the Repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2. Create Virtual Environment & Activate
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Download and Install Vosk Model

Download a Vosk model 

  Indian English (vosk-model-small-en-in-0.4)

  Hindi (vosk-model-small-hi-0.22)

  Dutch (vosk-model-small-nl-0.22)

  Spanish (vosk-model-small-es-0.42)
  

curl -L -o vosk-model-small-en—in0.4.zip \
https://alphacephei.com/vosk/models/vosk-model-small-en-in-0.4.zip
unzip vosk-model-small-en-in-0.4.zip
rm vosk-model-small-en-in-0.4.zip

curl -L -o vosk-model-small-hi-0.22.zip \
https://alphacephei.com/vosk/models/vosk-model-small-hi-0.22.zip
unzip vosk-model-small-hi-0.22.zip
rm vosk-model-small-hi-0.22.zip

\curl -L -o vosk-model-small-nl-0.22.zip \
https://alphacephei.com/vosk/models/vosk-model-small-nl-0.22.zip
unzip vosk-model-small-nl-0.22.zip
rm vosk-model-small-nl-0.22.zip

curl -L -o vosk-model-small-es-0.42.zip \
https://alphacephei.com/vosk/models/vosk-model-small-es-0.22.zip
unzip vosk-model-small-es-0.42.zip
rm vosk-model-small-es-0.42.zip



5. Run the Voice Keyboard Daemon
   
python daemon.py

How To Use:
1.	Open the QML UI
     
2.	Select a language model from dropdown

3.	Click Load Model → Daemon loads chosen Vosk model

4.	Click Start Recording → Start real-time recognition

5.	Speak into the mic → Transcript appears live in the text area

6.	Click Stop Recording → Recognition stops

7.	Click Save Transcript → Saves recognized text to a file
