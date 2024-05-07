# Importér nødvendige biblioteker:
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyaudio

# PYAUDIO:

#Initialisér PyAudio:
p = pyaudio.PyAudio()

# Vælg input/output mode:
input_mode = True

# Sæt parametrer for PyAudio
if input_mode:
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
plt.style.use('dark_background')                    # Sæt tema i Matplotlib
fig, ax = plt.subplots()                            # Opret et vindue og en akse til plottet
line, = ax.plot([], [], lw=2, color='mediumorchid') # Initialiser en linje til animationen

xlimit = 0.015                                  # x-aksens grænser
ylimit = 100                                    # y-aksens grænser

# Sæt titlen, initialiser plottet med de givne grænser og fjern ticks
ax.set_title('Lydbølge med højest amplitude')
ax.set_xlim(0, xlimit)
ax.set_ylim(-ylimit, ylimit)
plt.xticks([])
plt.yticks([])

# Funktion til at finde den højeste amplitude og den tilsvarende frekvenser
def find_highest_amp():
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)            # Læser lyddata fra lydstrømmen

    # Anvend Fourier transformation for at få arrays af amplituder og frekvenser
    Amps = np.fft.fft(data)                                            
    Amps = np.abs(Amps[0:CHUNK]) * 2 / (256 * CHUNK)
    Freqs= np.fft.fftfreq(CHUNK, 1.0/RATE)
    
    max_index = np.argmax(Amps)                                          # Find indekset af den højeste amplitude

    maxAmp = Amps[max_index]                                             # Find den højeste amplitude
    maxFreq = Freqs[max_index]                                           # Find den tilsvarende frekvens 

    return maxFreq, maxAmp                                               # Returner max-amplituden og den tilsvarende frekvens

# Funktion til at opdatere plottet med sinusbølger af den højeste frekvens
def animate_sin_wave(frame):
    f, A = find_highest_amp()                             # Find den højeste amplitude og frekvens
    x = np.linspace(0, xlimit, RATE)                      # Generer RATE x-værdier fra 0 til xlimit
    y = A * np.sin(2 * np.pi * f * (x-frame/2000))        # Generer sinusbølge med frekvens f og amplitude A. (x-frame/2000) for at få bølgen til at bevæge sig

    line.set_data(x, y)                                   # Sæt linjens data til x og y
    return line,

open_stream()                                            # Åben lydstrømmen

# Opsæt animationen og vis plottet
ani = FuncAnimation(fig, animate_sin_wave, blit=True, interval=20, frames=200)
plt.show()

# Stopper lydstrømmen og afslutter PyAudio og MatkploLib
stream.stop_stream()
stream.close()
p.terminate()
plt.close()