# GitHub Actions Build

Questo progetto usa GitHub Actions per buildare automaticamente eseguibili per:
- ✅ **Windows** (.exe)
- ✅ **Linux** (binario)
- ✅ **macOS** (binario)

## 🚀 Come funziona

1. **Push su GitHub** → Le Actions partono automaticamente
2. **Build parallele** su Windows, Linux e macOS
3. **Download artifact** o **Release automatica**

## 📦 Download degli eseguibili

### Opzione 1: Artifacts (sempre disponibili)
1. Vai su **Actions** nel repo GitHub
2. Clicca sull'ultimo workflow completato
3. Scorri in basso → **Artifacts**
4. Scarica:
   - `NubblePrintClient.exe` (Windows)
   - `NubblePrintClient-linux` (Linux)
   - `NubblePrintClient-macos` (macOS)

### Opzione 2: Releases (automatiche su push main/master)
1. Vai su **Releases** nel repo
2. Scarica l'ultima release
3. Tutti gli eseguibili sono già allegati!

## 🔧 Configurazione

Il file `.env` è incluso negli artifact. Modifica:
```bash
API_URL=https://app.nubble.it/api/printData
API_TOKEN=wqowok9emjibwc7adknn
PRINTER_URL=http://192.168.1.251:9100
```

## ⚡ Attivazione manuale

Puoi anche avviare la build manualmente:
1. Vai su **Actions**
2. Seleziona **Build Executables**
3. Click su **Run workflow**

Gli artifact vengono conservati per 30 giorni.
