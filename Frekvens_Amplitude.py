# Importér nødvendige biblioteker:
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyaudio
import seaborn as sns

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
plt.style.use('dark_background')                 # Sæt tema i Matplotlib
fig, ax = plt.subplots()                         # Lav vindue og akse til matplotlib

xlimit = 2000                                    # Sæt aksegrænser
ylimit = 20

xf = np.linspace(20, RATE/2, CHUNK)                # Beregn frekvenser for hvert punkt på x-aksen (frekvenser fra 20 Hz til xlimit med CHUNK punkter)

# Lav en linje i matplotlib til animationen
line, = ax.plot(xf, np.random.rand(CHUNK), color='mediumorchid')

# Sæt titel, aksegrænser, aksetitler og fjerner ticks og rammer
ax.set_title('Frekvens/Lydstyrke graf')
ax.set_ylim(0, ylimit)
ax.set_xlim(20, xlimit)
ax.set_xlabel('Frekvens (Hz)')
ax.set_ylabel('Lydstyrke')
plt.xticks([])
plt.yticks([])
sns.despine()


# En funktion til animationen, der opdaterer plottet med ny data
def animate(frame):
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)                # Læser lyddata fra lydstrømmen
    
    y = np.fft.fft(data)                                                    # Anvend en Fourier transformation på dataen for at få frekvensspektret
    y = np.abs(y[0:CHUNK]) * 2 / (256 * CHUNK)
    
    line.set_ydata(y)                                                       # Opdater plottet med den nye data
    return line,

open_stream()                                                               # Åben lydstrømmen

# Opsæt animationen og vis plottet
ani = FuncAnimation(fig, animate, blit=True, interval=20, frames=100)       # Start animationen
plt.show()

# Stop audio streamen og afslut PyAudio og Matplotlib
stream.stop_stream()
stream.close()
p.terminate()
plt.close()