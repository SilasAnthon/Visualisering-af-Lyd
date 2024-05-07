# Visualisering-af-lyd
Eksamensprojekt til Teknikfag: Digitalt Design og Udvikling

Skriv 'pip install -r requirements.txt' i terminalen for at installere de nødvendige biblioteker. I 'Frekvens_Lydstyrke.py' (linje 14) og 'Lydbølge.py' (linje 13) kan der skiftes mellem mikrofon og højttaler ved at skifte 'input_mode' mellem True (mikrofon) og False (højttaler).

For at bruge lydvisualiseringsfunktionerne, skal de korrekte Device Indexes først sættes i koden. Disse kan indstilles på linje 18 og 20 i 'Frekvens_Lydstyrke.py', linje 17 & 19 i'Lydbølge.py' og linje 35 & 37 i 'StreamlitUI.py'.
Disse tal er unikke for hver enhed, så først skal man finde ud af, hvad de skal sættes til. Dette kan gøres ved at køre 'AudioIndex.py' filen, som printer en liste af alle lydenheder og deres indexes.
Device Indexet for input mode burde altid være 1, da dette er computerens standard-enhed for mikrofonen.
For output bliver det lidt sværre. Til at starte med skal man åbne kontrolpanelet->Hardware og lyd->lyd->optagelse, så højreklick et frit sted og tryk "Vis deaktiverede enheder". Her er en, der hedder Stereomix, som skal aktiveres ved at højreklicke på den og trykke "Aktivér".
Den rigtige output-enhed fra 'AudioIndex.py' burde hedde Stereomix ('Standard-enheden for højttaler'). Denne burde have mere end 0 input channels, da det er her, PyAudio læser lyden fra.

Det er vigtigt, at 'StreamlitUI.py' og 'InfoTekst.py' er i samme mappe for, at infoteksten bliver vist rigtigt i Streamlit.
For at køre koden til brugergrænsefladen i Streamlit, skal der skrives 'streamlit run StreamlitUI.py' i en dedikeret terminal.
