# Build dell'Eseguibile

## Come Funziona

PyInstaller analizza il codice Python, include tutte le dipendenze e crea un singolo eseguibile standalone.

## Processo di Build

### 1. Installa PyInstaller
```bash
pip install pyinstaller
```

### 2. Crea l'eseguibile

**macOS/Linux:**
```bash
./build.sh
```

**Windows:**
```bash
build.bat
```

**Manualmente:**
```bash
pyinstaller --clean NubblePrintClient.spec
```

### 3. Risultato

- **macOS/Linux**: `dist/NubblePrintClient` (file binario)
- **Windows**: `dist/NubblePrintClient.exe`

## File di Configurazione: NubblePrintClient.spec

Il file `.spec` controlla come PyInstaller crea l'eseguibile:

- `name`: Nome dell'eseguibile
- `console=True`: Mostra finestra console (utile per vedere i log)
- `onefile`: Tutto in un singolo file
- `hiddenimports`: Moduli da includere anche se non rilevati automaticamente

## Personalizzazione

### Aggiungere un'icona

1. Crea/trova un'icona:
   - Windows: file `.ico`
   - macOS: file `.icns`
   
2. Modifica `NubblePrintClient.spec`:
```python
exe = EXE(
    ...
    icon='path/to/icon.ico',  # o .icns su macOS
)
```

### Modalità no-console (Windows)

Per nascondere la finestra console su Windows:

```python
exe = EXE(
    ...
    console=False,  # Nasconde la console
)
```

## Distribuzione

### File da distribuire:
1. Eseguibile (`NubblePrintClient` o `NubblePrintClient.exe`)
2. File `.env` di configurazione

### Istruzioni per l'utente finale:
1. Scarica l'eseguibile
2. Crea un file `.env` nella stessa cartella con:
   ```
   DB_HOST=server.com
   DB_PORT=3306
   DB_NAME=database
   DB_USER=user
   DB_PASSWORD=password
   ```
3. Esegui il programma

## Troubleshooting

### L'eseguibile non parte su macOS
```bash
# Rimuovi il quarantine attribute
xattr -d com.apple.quarantine NubblePrintClient
```

### Windows SmartScreen blocca l'eseguibile
- Normale per eseguibili non firmati
- Clicca "Maggiori informazioni" → "Esegui comunque"
- Per evitarlo: firma il codice con un certificato

### Errore "ModuleNotFoundError"
Aggiungi il modulo mancante in `hiddenimports` nel file `.spec`

### L'eseguibile è troppo grande
È normale: include Python + tutte le librerie (~40-80 MB)

## Build Cross-Platform

**IMPORTANTE:** PyInstaller crea eseguibili solo per il sistema operativo su cui viene eseguito:

- Per Windows EXE: build su Windows
- Per macOS binary: build su macOS  
- Per Linux binary: build su Linux

Non è possibile fare cross-compile.

### Soluzioni per multi-platform:

1. **VM/Docker**: Crea VM per ogni OS
2. **GitHub Actions**: Automatizza build su tutti gli OS
3. **Distribuisci il codice Python**: Gli utenti eseguono `python main.py`
