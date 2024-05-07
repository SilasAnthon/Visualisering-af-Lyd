# Visualisering-af-lyd
Eksamensprojekt til Teknikfag: Digitalt Design og Udvikling

For at bruge lydvisualiseringsfunktionerne, skal de korrekte Device Indexes først sættes i koden. Disse tal er unikke for hver enhed, så først skal man finde ud af, hvad de skal sættes til. Dette kan gøres ved at køre 'AudioIndex.py' filen, som printer en liste af alle lydenheder og deres indexes.
Device Indexet for input mode burde altid være 1, da dette er computerens standard-enhed for mikrofonen.
For output bliver det lidt sværre. Den rigtige output-enhed burde hedde Stereomix ('Standard-enheden for højttaler'). Denne burde have mere end 0 input channels, da det er disse, PyAudio læser lyden fra.

For at køre koden til brugergrænsefladen i Streamlit, skal der skrives 'streamlit run StreamlitUI.py' i en dedikeret terminal.
