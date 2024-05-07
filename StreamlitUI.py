import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import seaborn as sns
import sounddevice as sd
import threading
import InfoTekst


# Initialisér Streamlit siden:
st.set_page_config(
    page_title="Lydvisualisering",
    page_icon="🔊",
    layout="wide"
)

st.title('Lydvisualisering')                        # Sidens titel (fanen i browseren)
col1, col2, col3 = st.columns([0.15, 0.7, 0.15])    # Kolonner til de forskellige elementer på siden
with col2:
    plot_placeholder = st.empty()                   # Placeholder til plottet


# PYAUDIO:

# Initialisér PyAudio:
p = pyaudio.PyAudio()

# Initialisér input_mode i Streamlits session state (så den kun bliver sat første gang):
if 'input_mode' not in st.session_state:
    st.session_state.input_mode = True

# Sæt parametrer for PyAudio
if st.session_state.input_mode:
    DEVICE_INDEX = 1                                                            # Device index vælger hvilken enhed der skal bruges.
else:
    DEVICE_INDEX = 16                                                           #1 er mikrofonen, 16 er højttaleren (forskelligt fra pc til pc)

CHUNK = 1024                                                                    # Antal 'samples' der bliver gemt i bufferen
FORMAT = pyaudio.paInt16                                                        # Lyddataens format
CHANNELS = int(p.get_device_info_by_index(DEVICE_INDEX)['maxInputChannels'])    # Antal kanaler, som lydenheden har. Bliver valgt udfra standard antallet af PyAudio
RATE = int(p.get_device_info_by_index(DEVICE_INDEX)['defaultSampleRate'])       # Antal samples per sekund. Samme koncept som channels

# Åben en lydstrøm fra lydenheden i PyAudio med de givne parametre
def open_stream():
    global stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=DEVICE_INDEX)


# MATPLOTLIB:

# Frekvens/Lydstyrke Plottet:
# Funktion til at opdatere Frekvens/Lydstyrke plottet:
def Frekvens_Lydstyrke_plot():
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    y = np.fft.fft(data)
    y = np.abs(y[0:CHUNK]) * 2 / (256 * CHUNK)

    xf = np.linspace(20, RATE/2, CHUNK)

    plt.figure(figsize=(10, 5))
    plt.plot(xf, y, color='mediumorchid')
    plt.title('Frekvens/Lydsyrke Graf')
    plt.ylim(0, 20)
    plt.xlim(20, 2000)
    plt.style.use('dark_background')
    plt.xticks([])
    plt.yticks([])
    plt.xlabel('Frekvens (Hz)')
    plt.ylabel('Lydstyrke')
    sns.despine()

    # Sæt plottet ind i placeholderen i Streamlit
    plot_placeholder.pyplot(plt.gcf())

# Funktion, som læser data fra mikrofonen og opdaterer plottet
def Frekvens_Lydstyrke_konstant():
    while True:
        plt.close()
        Frekvens_Lydstyrke_plot()


# Lydbølge Funktionen:
# Først find højeste amplitude og tilsvarende frekvens:
def find_highest_amp():
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)

    Amps = np.fft.fft(data)
    Amps = np.abs(Amps[0:CHUNK]) * 2 / (256 * CHUNK)
    Freqs= np.fft.fftfreq(CHUNK, 1.0/RATE)

    max_index = np.argmax(Amps)

    maxAmp = Amps[max_index]
    maxFreq = Freqs[max_index]

    return maxFreq, maxAmp

# Funktion til at plotte lydbølgen med den højeste amplitude:
def Lydbølge_plot():
    f, A = find_highest_amp()
    x = np.linspace(0, 0.015, RATE)
    y = A * np.sin(2 * np.pi * f * x)

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, color='mediumorchid')
    plt.title('Lydbølge med højest amplitude')
    plt.ylim([-100, 100])
    plt.xlim([0, 0.015])
    plt.style.use('dark_background')
    plt.xticks([])
    plt.yticks([])

    # Sæt plottet ind i placeholderen i Streamlit
    plot_placeholder.pyplot(plt.gcf())

# Få plottet til at opdatere konstant:
def Lydbølge_konstant():
    while True:
        plt.close()
        Lydbølge_plot()

# Åben lydstrømmen
open_stream()

# Tråde til funktionerne:


# STREAMLIT:

# Tal som vælger mellem funktionerne (starter på 0, som svarer til Frekvens/Lydstyrke grafen):
if 'funk_tal' not in st.session_state:
    st.session_state.funk_tal = 0

# Funktioner til at skifte mellem de forskellige visualiseringsfunktioner ved at ændre tallet:
def skift_funktion_højre():
    plt.close()
    st.session_state.funk_tal += 1
    st.session_state.funk_tal %= 3
def skift_funktion_venstre():
    plt.close()
    st.session_state.funk_tal -= 1
    st.session_state.funk_tal %= 3

# Knapper til at vælge mellem visualiseringsfunktioner og knapper til at ændre sprog og se info om produktet (ikke funktionelle):
with col3:
    st.button('​>', on_click=skift_funktion_højre)
    st.button('ℹ️')
with col1:
    st.button('<', on_click=skift_funktion_venstre)
    st.button('🇩🇰')


# Mikrofon og højttaler:
# Funktioner til at skifte mellem mikrofon og højttaler:
def set_input_mode():
    st.session_state.input_mode = True
def set_output_mode():
    st.session_state.input_mode = False

# Knappernes labels (så de ændrer farver alt efter, hvilken mode der er valgt):
if st.session_state.input_mode:
    input_label = ':red[:🎙️:]'
    output_label = ':white[🔊]'
else:
    input_label = ':white[🎙️]'
    output_label = ':red[:🔊:]'
# Knapper til at skifte mellem de to:
with col2:
    st.button(input_label, on_click=set_input_mode)
    st.button(output_label, on_click=set_output_mode)

# Lydafspiller:
# Funktion til at afspille lyd med variabel frekvens og lydstyrke:
def play_sound(f, L):
    t = np.linspace(0, 1, RATE, endpoint=False)
    wave = L/100*np.sin(2*np.pi*f*t)
    sd.play(wave, samplerate=RATE, blocking=False, loop=True)

# Sliders og knap til lydafspilleren:.
if not st.session_state.input_mode:                                                                         # Kun vis, hvis den er sat til højttaleren.
    with col2:
        Frekvens = st.slider(f'Frekvens (Hz)', min_value=20, max_value=2000, value=400, key='Frekvens')     # Vælg frekvens mellem 20 og 2000 Hz med slider. Startværdiern er 400 Hz
        Lydstyrke = st.slider(f'Lydstyrke', min_value=0, max_value=100, value=0, key='Lydstyrke')           # Vælg lydstyrken fra 0 til 100% med slider. Startværdien er 0%

    # Start en tråd til at afspille lyden:
    sound_thread = threading.Thread(target=play_sound, args=(Frekvens, Lydstyrke,))
    sound_thread.start()

# Kør den valgte funktion og indsæt infotekst:
with col2:
        infotekst_placeholder = st.empty()               # Placeholder til infotekst

if st.session_state.funk_tal == 0:
    if st.session_state.input_mode:
        infotekst_placeholder.text(InfoTekst.FLMikTekst)
    else:
        infotekst_placeholder.text(InfoTekst.FLHøjtTekst)
    Frekvens_Lydstyrke_konstant()
elif st.session_state.funk_tal == 1:
    if st.session_state.input_mode:
        infotekst_placeholder.text(InfoTekst.LydbMikTekst)
    else:
        infotekst_placeholder.text(InfoTekst.LydbHøjtTekst)
    Lydbølge_konstant()
elif st.session_state.funk_tal == 2:
    if st.session_state.input_mode:
        infotekst_placeholder.text(InfoTekst.TrykbMikTekst)
    else:
        infotekst_placeholder.text(InfoTekst.TrykbHøjtTekst)
    # Viser en GIF af, hvordan det skulle have set ud:
    plot_placeholder.markdown("![Alt Text](https://cdn.discordapp.com/attachments/881263067072200774/1237042352263139420/Untitledvideo-MadewithClipchamp101-ezgif.com-resize_1.gif?ex=663a34f7&is=6638e377&hm=2eb67822e80482d5ad1cfb47b1f8188caf6d75024a91ebdd74f3f1335746b37e&)")

# Luk alt for at bevare hukommelse:
plt.close()
stream.stop_stream()
stream.close()
p.terminate()
st.stop()
# For at køre gennem terminal:
# streamlit run StreamlitUI.py