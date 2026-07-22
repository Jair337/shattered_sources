# Shattered Sources - Gebruikershandleiding

# Welkom! 

Dit is een volledige gids het project aan de praat te krijgen.
---

## Inhoudsopgave
1. [Wat is dit project?](#wat-is-dit-project)
2. [Systeemvereisten](#systeemvereisten)
3. [Installatiegids](#installatiegids)
   - [Stap 1: Python installeren](#stap-1-python-installeren)
   - [Stap 2: Project downloaden en instellen](#stap-2-project-downloaden-en-instellen)
   - [Stap 3: Afhankelijkheden installeren](#stap-3-afhankelijkheden-installeren)
4. [De applicatie uitvoeren](#de-applicatie-uitvoeren)
5. [De applicatie gebruiken](#de-applicatie-gebruiken)
6. [Probleemoplossing](#probleemoplossing)
7. [Hulp krijgen](#hulp-krijgen)

---

## Wat is dit project?

**Shattered Sources** is een webgebaseerde applicatie voor datavisualisatie en analyse dat:
- **Gebeurtenisgegevens analyseert** - Verwerk en analyseer gebeurtenissen
- **Op kaarten visualiseert** - Zie gebeurtenissen weergegeven op interactieve kaarten
- **Statistieken genereert** - Bekijk grafieken en statistieken
- **AI/Machine Learning gebruikt** - Analyseer patronen in je gegevens
- **Een makkelijke interface** - Toegang tot alles via je webbrowser

---

## Systeemvereisten

- Een Windows, Mac of Linux computer met tenmiste 8GB RAM
- Internettoegang (om Python en bibliotheken te downloaden)
- Een moderne webbrowser (Chrome, Firefox, Safari of Edge)

---

## Installatiegids

### Stap 1: Python installeren



#### **Voor Windows:**
1. Ga naar https://www.python.org/downloads/
2. Download een nieuwere versie van Python 3 (bijvoorbeeld Python 3.13.x)
3. **Belangrijk:** Als het installatieprogramma opent, **VINK het vakje aan** dat zegt "Add Python to PATH" ✓
4. Klik op "Install Now"
5. Wacht tot het klaar is 
6. Klik op "Close" als het klaar is

**Controleer of Python correct is geïnstalleerd:**
- Druk op `Windows-toets + R`
- Typ `cmd` en druk op Enter
- Typ dit commando en druk op Enter: `python --version`
- Je zou iets moeten zien als "Python 3.x.x"

#### **Voor Mac:**
1. Ga naar https://www.python.org/downloads/
2. Klik op "Download Python 3.13.x" (of nieuwste versie)
3. Open het installerbestand en volg de aanwijzingen
4. Klik door alle dialogen

**Controleer of Python correct is geïnstalleerd:**
- Open Terminal (zoek naar "Terminal" in Spotlight)
- Typ dit commando en druk op Enter: `python3 --version`
- Je zou iets moeten zien als "Python 3.x.x"

#### **Voor Linux (Ubuntu/Debian):**
- Open een terminal en voer uit: `sudo apt-get install python3 python3-pip`
- Controleer: `python3 --version`

---

### Stap 2: Project downloaden en instellen

1. **Haal de projectbestanden op:**
   - Als je een ZIP-bestand hebt, pak het uit naar een map
   - Als je van GitHub kloont, voer uit: `git clone https://github.com/Jair337/shattered_sources.git`

2. **Navigeer naar de projectmap:**
   
   **Windows:**
   - Druk op `Windows-toets + R`
   - Typ `cmd` en druk op Enter
   - Typ: `cd C:\Users\JouwNaam\pad\naar\shattered_sources` (pas het pad aan naar waar je het hebt opgeslagen)
   - Druk op Enter

   **Mac/Linux:**
   - Open Terminal
   - Typ: `cd /pad/naar/shattered_sources`
   - Druk op Enter

3. **Maak een virtuele omgeving** (dit houdt afhankelijkheden geïsoleerd voor dit project):
   
   **Windows:**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

   **Mac/Linux:**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

   ✓ Na dit commando zou je `(venv)` aan het begin van je opdrachtlijn moeten zien

---

### Stap 3: Afhankelijkheden installeren

Nu moeten we alle bibliotheken installeren die dit project nodig heeft. We gebruiken daarvoor een bestand genaamd `requirements.txt`.

1. **Maak het bestand requirements.txt aan** (als het nog niet bestaat):
   
   Maak in de projectmap een nieuw bestand genaamd `requirements.txt` met deze inhoud:
   ```
   Flask==2.3.0
   flask-cors==4.0.0
   pandas==2.0.0
   numpy==1.24.0
   scikit-learn==1.2.0
   matplotlib==3.7.0
   plotly==5.14.0
   requests==2.31.0
   sqlite3
   ```

2. **Installeer alle afhankelijkheden:**
   
   Met je opdrachtlijn open in de projectmap (en `(venv)` zichtbaar), voer uit:
   ```
   pip install -r requirements.txt
   ```

   Dit zal alles downloaden en installeren. 

---
### Stap 4: Ollama en Gemma2 model installeren

Dit project gebruikt het **Gemma2:2b** LLM model. Ollama is een tool waarmee je dit model lokaal kunt uitvoeren.

#### **Stap 1: Ollama downloaden en installeren**

1. Ga naar https://ollama.com/download
2. Download de versie voor jouw besturingssysteem (Windows, Mac of Linux)
3. Open het bestand en volg de aanwijzingen
4. Nadat de installatie compleet is, start je computer opnieuw op

**Controleer of Ollama correct is geïnstalleerd:**
- **Windows:** Open opdrachtprompt en typ: `ollama --version`
- **Mac/Linux:** Open Terminal en typ: `ollama --version`
- Je zou een versienummer moeten zien

#### **Stap 2: Het Gemma2:2b model downloaden**

Dit model kun je online van het Ollama-modellenbibliotheek downloaden. 

1. **Download het model** via de modelenpagina: https://ollama.com/library/gemma2:2b
   
   Of gebruik je opdrachtlijn:
   ```
   ollama pull gemma2:2b
   ```

2. **Controleer of het model is gedownload:**
   ```
   ollama list
   ```
   Je zou `gemma2:2b` in de lijst moeten zien.

#### **Stap 3: Ollama starten**

Voordat je de applicatie start, moet je Ollama starten zodat het model beschikbaar is, 
controleer nogmaals dat je het model hebt gedownload en het zichtbaar is in de lijst van Ollama.




---

## De applicatie uitvoeren

1. **Open je opdrachtlijn** in de projectmap

2. **Activeer de virtuele omgeving:**
   
   **Windows:**
   ```
   venv\Scripts\activate
   ```
   
   **Mac/Linux:**
   ```
   source venv/bin/activate
   ```
   
   (Je zou `(venv)` aan het begin van je lijn moeten zien)

3. **Start de applicatie:**
   ```
   python main.py
   ```

4. **Wacht tot dit bericht verschijnt:**
   ```
   * Running on http://127.0.0.1:5000
   ```

5. **Open je webbrowser** en ga naar:
   ```
   http://localhost:5000
   ```

   Je zou nu de interface moeten zien! 


---
## Probleemoplossing

### Probleem: "Python is niet herkend"
**Oplossing:**
- Je moet Python opnieuw installeren en ervoor zorgen dat je "Add Python to PATH" aanvinkt
- Of start je computer opnieuw op na het installeren van Python

### Probleem: "No module named 'flask'" of iets soortgelijks
**Oplossing:**
- Zorg ervoor dat je de virtuele omgeving hebt geactiveerd (je zou `(venv)` in je opdrachtlijn moeten zien)
- Voer `pip install -r requirements.txt` opnieuw uit

### Probleem: Poort 5000 is al in gebruik
**Oplossing:**
- Sluit alle andere toepassingen die poort 5000 gebruiken
- Of in het `main.py` bestand, verander `app.run(debug=True)` in `app.run(port=5001, debug=True)` en gebruik `localhost:5001` in je browser



### Probleem: Lege pagina of fouten in browser
**Oplossing:**
- Controleer het opdrachtvenster waar je `python main.py` hebt uitgevoerd
- Zoek naar foutberichten in het rood
- Probeer de pagina te vernieuwen (Ctrl+R of Cmd+R)


---

## Hulp krijgen

Als je nog vastloopt:

1. **Neem contact op met de ontwikkelaar** - Geef:
   - Je besturingssysteem (Windows/Mac/Linux)
   - Het exacte foutbericht
   - Wat je probeerde te doen toen de fout optrad

---

## Tips & Trucs

- **Het draaiend houden:** De applicatie blijft draaien in het opdrachtvenster. Om het te stoppen, druk je op `Ctrl+C`
- **Opnieuw starten:** Nadat je de app hebt gestopt, kun je `python main.py` opnieuw uitvoeren

---



**Laatst bijgewerkt:** 2026
**Versie:** 1.1
