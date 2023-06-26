from base64 import b64decode
import scipy as sc
import io
import difflib
import pandas as pd
import os

import bulkhours_premium
from .tools import styles
from .summary import summary
from . import answers

AUDIO_HTML = """
<script>
var my_div = document.createElement("DIV");
var my_p = document.createElement("P");
var my_btn = document.createElement("BUTTON");
var t = document.createTextNode("Press to start recording");

my_btn.appendChild(t);
my_div.appendChild(my_btn);
document.body.appendChild(my_div);

var base64data = 0;
var reader;
var recorder, gumStream;
var recordButton = my_btn;

var handleSuccess = function(stream) {
  gumStream = stream;
  var options = {
    //bitsPerSecond: 8000, //chrome seems to ignore, always 48k
    mimeType : 'audio/webm;codecs=opus'
  };            
  //recorder = new MediaRecorder(stream, options);
  recorder = new MediaRecorder(stream);
  recorder.ondataavailable = function(e) {            
    var url = URL.createObjectURL(e.data);
    var preview = document.createElement('audio');
    preview.controls = true;
    preview.src = url;
    document.body.appendChild(preview);

    reader = new FileReader();
    reader.readAsDataURL(e.data); 
    reader.onloadend = function() {
      base64data = reader.result;
    }
  };
  recorder.start();
  };

recordButton.innerText = "Arrete l'enregistrement";

navigator.mediaDevices.getUserMedia({audio: true}).then(handleSuccess);


function toggleRecording() {
  if (recorder && recorder.state == "recording") {
      recorder.stop();
      gumStream.getAudioTracks()[0].stop();
      recordButton.innerText = "Saving the recording... pls wait!"
  }
}

// https://stackoverflow.com/a/951057
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var data = new Promise(resolve=>{
//recordButton.addEventListener("click", toggleRecording);
recordButton.onclick = ()=>{
toggleRecording()

sleep(1000).then(() => {
  // wait 1000ms for the data to be available...
  // ideally this should use something like await...
  //console.log("Inside data:" + base64data)
  resolve(base64data.toString())

});

}
});
      
</script>
"""


def transcript(filename, sample_rate=16000, language_code="fr-FR"):
    from google.cloud import speech

    with io.open(filename, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

    client = speech.SpeechClient()
    response = client.recognize(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code=language_code,
        ),
        audio=audio,
    )
    for result in response.results:
        result.alternatives[0].transcript
    return result.alternatives[0].transcript


def estimate_grade(text, exo, cinfo=None):
    students = summary(no_admin=False, cmap=None)
    ref_dist = dict(dist=0, name="Nope", grade=1)
    oral_name = text.split()
    sname = " ".join(oral_name[:-1]).lower()

    rep = {"I": 1.0, "II": 2.0, "III": 3.0, "IV": 4.0}

    for i in students.index:
        if type(students["nom"][i]) == str:
            s = students["nom"][i] + " " + students["prenom"][i]
            r_dist = difflib.SequenceMatcher(None, str(s).lower(), sname).ratio()
            if r_dist > ref_dist["dist"]:
                grade = rep[oral_name[-1]] if oral_name[-1] in rep else float(oral_name[-1].replace(",", "."))
                ref_dist = dict(dist=r_dist, name=str(s), login=i, grade=grade, raw=text)
    if ref_dist["login"] != "Nope":
        # students.at[ref_dist["login"], exo] = float(ref_dist["grade"])
        answers.update_note(cinfo.notebook_id + "_" + exo, ref_dist["login"], float(ref_dist["grade"]))

    return ref_dist


def get_audio(exo, output, update_git=False):
    """
    To write this piece of code I took inspiration/code from a lot of places.
    It was late night, so I'm not sure how much I created or just copied o.O
    Here are some of the possible references:
    https://blog.addpipe.com/recording-audio-in-the-browser-using-pure-html5-and-minimal-javascript/
    https://stackoverflow.com/a/18650249
    https://hacks.mozilla.org/2014/06/easy-audio-capture-with-the-mediarecorder-api/
    https://air.ghost.io/recording-to-an-audio-file-using-html5-and-js/
    https://stackoverflow.com/a/49019356
    """
    cinfo = bulkhours_premium.tools.get_config(is_namespace=True)

    import IPython
    import ffmpeg
    from google.colab.output import eval_js

    IPython.display.display(IPython.display.HTML(AUDIO_HTML))
    data = eval_js("data")
    binary = b64decode(data.split(",")[1])

    process = (
        ffmpeg.input("pipe:0")
        .output("pipe:1", format="wav")
        .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True, quiet=True, overwrite_output=True)
    )
    output, err = process.communicate(input=binary)

    riff_chunk_size = len(output) - 8  # Break up the chunk size into four bytes, held in b.
    q = riff_chunk_size
    b = []
    for i in range(4):
        q, r = divmod(q, 256)
        b.append(r)

    # Replace bytes 4:8 in proc.stdout with the actual size of the RIFF chunk.
    riff = output[:4] + bytes(b) + output[8:]

    sr, audio = sc.io.wavfile.read(io.BytesIO(riff))
    sc.io.wavfile.write("recording.wav", sr, audio)
    text = transcript("recording.wav", sample_rate=48000)
    ref_dist = estimate_grade(text, exo, cinfo=cinfo)

    if ref_dist["login"] == "Nope":
        play_message("Pour évaluer un élève, dites, nom, prenom, note")
        return

    play_message(f"{ref_dist['name']} a la note de {ref_dist['grade']} sur 10")

    IPython.display.display(students := summary(no_admin=False))

    return students


def play_message(msg):
    import IPython
    import gtts

    tts = gtts.gTTS(msg, lang="fr")  # Provide the string to convert to speech
    tts.save(sound_file := "last_read_message.wav")  # save the string converted to speech as a .wav file
    IPython.display.display(IPython.display.Audio(sound_file, autoplay=True))
