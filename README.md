# Nubble Print Client

Client **multipiattaforma** (Windows, macOS, Linux) per la stampa automatica di documenti tramite API Laravel.

## 🚀 Caratteristiche

- **Multipiattaforma**: funziona su Windows, macOS e Linux
- **Polling ottimizzato** con backoff esponenziale
- **API REST**: nessun accesso diretto al database
- **Tracciamento intelligente** dei documenti
- **Logging completo** su file e console
- **Gestione errori** con retry automatico
- **Configurazione flessibile** tramite file .env
- **Conversione XML → PDF** automatica

## 📋 Prerequisiti

- Python 3.8 o superiore
- Stampante configurata sul sistema
- Accesso all'API Laravel

## ⚙️ Installazione

### 1. Clona o scarica il progetto

### 2. Installa le dipendenze Python

```bash
# Crea un virtual environment (opzionale ma consigliato)
python3 -m venv venv

# Attiva il virtual environment
# Su macOS/Linux:
source venv/bin/activate
# Su Windows:
venv\Scripts\activate

# Installa le dipendenze
pip install -r requirements.txt
```

### 3. Configura l'ambiente

```bash
# Copia il file di esempio
cp .env.example .env

# Modifica .env con i tuoi dati
nano .env  # o usa il tuo editor preferito
```

Configurazione `.env`:
```bash
API_URL=https://app.nubble.it/api/printData
API_TIMEOUT=10

POLL_INTERVAL=5
MAX_POLL_INTERVAL=30
BACKOFF_MULTIPLIER=1.5

DEFAULT_PRINTER=  # Lascia vuoto per stampante di default

LOG_LEVEL=INFO
LOG_FILE=logs/nubble_print.log
```

### 4. Esegui il client

```bash
python main.py
```

## 🔧 Come funziona

### Polling Intelligente

1. **Avvio**: chiamata API ogni 5 secondi
2. **Nessun dato**: intervallo aumenta progressivamente (5s → 7.5s → 11s → 16s → 24s → 30s)
3. **Dati ricevuti**: stampa e intervallo torna a 5 secondi

### API Laravel

Il client effettua chiamate POST a:
```
https://app.nubble.it/api/printData
```

Risposta attesa:
```json
{
  "success": true,
  "data": "<xml>...</xml>"
}
```

Se `data` è presente, viene stampato. Se vuoto, nessuna azione.

### Ottimizzazioni

- Backoff esponenziale quando non ci sono dati
- Session HTTP riutilizzabile
- Timeout configurabile
- Retry automatico su errori di rete

## 📁 Struttura Progetto

```
nubble-print-client/
├── src/
│   ├── models/
│   │   └── print_job.py           # Modello dati
│   ├── services/
│   │   ├── api_service.py         # Gestione API Laravel
│   │   ├── print_service.py       # Gestione stampa multipiattaforma
│   │   └── polling_service.py     # Logica polling
│   └── config.py                   # Configurazione
├── main.py                         # Entry point
├── requirements.txt                # Dipendenze Python
├── .env.example                    # Template configurazione
└── README.md
```

## 🖨️ Personalizzazione Stampa

Modifica [src/services/print_service.py](src/services/print_service.py) nel metodo `_xml_to_pdf()` per personalizzare il rendering del PDF in base alla struttura del tuo XML:

```python
def _xml_to_pdf(self, xml_content: str, output_path: str) -> bool:
    root = etree.fromstring(xml_content.encode('utf-8'))
    c = canvas.Canvas(output_path, pagesize=A4)
    
    # PERSONALIZZA QUI in base al tuo XML
    # Esempio: estrai campi specifici
    title = root.find('.//title').text
    content = root.find('.//content').text
    date = root.find('.//date').text
    
    # Renderizza sul PDF
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, title)
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Data: {date}")
    c.drawString(50, 720, content)
    
    c.save()
    return True
```

## 📊 Logs

I log vengono salvati in `logs/nubble_print.log`:

```
2026-02-01 10:30:15 - __main__ - INFO - Nubble Print Client - Avviato
2026-02-01 10:30:15 - src.services.api_service - INFO - Connessione all'API riuscita
2026-02-01 10:30:20 - src.services.api_service - INFO - Ricevuti dati XML dall'API (1250 caratteri)
2026-02-01 10:30:21 - src.services.print_service - INFO - Stampa completata con successo
```

## 🔒 Sicurezza

- L'URL dell'API è nel file `.env`
- **Aggiungi `.env` al `.gitignore`** (già fatto)
- **Non committare mai il file `.env`** nel repository
- Usa HTTPS per le chiamate API
- Usa permessi appropriati: `chmod 600 .env` su Unix

## 🐛 Troubleshooting

### Errore di connessione API
```bash
# Testa l'API manualmente
curl -X POST https://app.nubble.it/api/printData
```
- Verifica che l'API sia raggiungibile
- Controlla firewall e CORS
- Verifica certificato SSL

### Timeout API
- Aumenta `API_TIMEOUT` nel file `.env`
- Verifica la latenza di rete
- Controlla i log del server Laravel

### Stampante non trovata (macOS/Linux)
```bash
# Lista stampanti disponibili
lpstat -p

# Su macOS, aggiungi stampante da Preferenze di Sistema
# Su Linux, usa CUPS: http://localhost:631
```

### Stampante non trovata (Windows)
```bash
# Lista stampanti
wmic printer get name

# Verifica che la stampante sia online
```

### Errore import lxml
```bash
# Su macOS potrebbe servire:
brew install libxml2 libxslt
pip install --upgrade lxml

# Su Ubuntu/Debian:
sudo apt-get install libxml2-dev libxslt-dev
pip install --upgrade lxml
```

## � Esecuzione in Background
### Creazione Eseguibile Standalone

Per distribuire l'applicazione senza richiedere Python, crea un eseguibile:

**Su macOS/Linux:**
```bash
# Installa PyInstaller (già in requirements.txt)
pip install pyinstaller

# Crea l'eseguibile
./build.sh

# L'eseguibile sarà in: dist/NubblePrintClient
```

**Su Windows:**
```bash
# Installa PyInstaller
pip install pyinstaller

# Crea l'eseguibile
build.bat

# L'eseguibile sarà in: dist\NubblePrintClient.exe
```

**Distribuzione:**
1. Copia l'eseguibile (`dist/NubblePrintClient` o `dist/NubblePrintClient.exe`)
2. Crea un file `.env` nella stessa cartella dell'eseguibile
3. Esegui l'applicazione

**Note:**
- L'eseguibile include tutte le dipendenze Python
- Non serve installare Python sulla macchina target
- Su macOS potrebbe servire: `xattr -d com.apple.quarantine NubblePrintClient`
- Su Windows potrebbe apparire un warning di SmartScreen (normale per exe non firmati)
### Su macOS/Linux (systemd)

Crea `/etc/systemd/system/nubble-print.service`:

```ini
[Unit]
Description=Nubble Print Client
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/nubble-print-client
ExecStart=/path/to/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Poi:
```bash
sudo systemctl enable nubble-print
sudo systemctl start nubble-print
sudo systemctl status nubble-print
```

### Su macOS (launchd)

Crea `~/Library/LaunchAgents/com.nubble.printclient.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.nubble.printclient</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/venv/bin/python</string>
        <string>/path/to/main.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/nubble-print-client</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Poi:
```bash
launchctl load ~/Library/LaunchAgents/com.nubble.printclient.plist
launchctl start com.nubble.printclient
```

### Su Windows

Usa **NSSM** (Non-Sucking Service Manager):

```bash
# Scarica NSSM da https://nssm.cc/
nssm install NubblePrintClient "C:\path\to\python.exe" "C:\path\to\main.py"
nssm set NubblePrintClient AppDirectory "C:\path\to\nubble-print-client"
nssm start NubblePrintClient
```

## 📄 Licenza

Uso interno - Nubble Print System
