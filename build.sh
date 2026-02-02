#!/bin/bash
# Script per creare l'eseguibile multipiattaforma

echo "🔨 Build Nubble Print Client"
echo "=============================="

# Attiva virtual environment se esiste
if [ -d "venv" ]; then
    echo "✓ Attivazione virtual environment..."
    source venv/bin/activate
fi

# Verifica che PyInstaller sia installato
if ! command -v pyinstaller &> /dev/null; then
    echo "⚠️  PyInstaller non trovato, installazione in corso..."
    pip install pyinstaller==6.3.0
fi

# Pulisci build precedenti
echo "🗑️  Pulizia build precedenti..."
rm -rf build dist

# Crea l'eseguibile
echo "🚀 Creazione eseguibile..."
pyinstaller --clean NubblePrintClient.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build completata con successo!"
    echo ""
    echo "📦 Eseguibile creato in:"
    echo "   dist/NubblePrintClient"
    echo ""
    echo "📝 Per utilizzarlo:"
    echo "   1. Copia dist/NubblePrintClient dove vuoi"
    echo "   2. Crea un file .env nella stessa cartella"
    echo "   3. Esegui ./NubblePrintClient"
    echo ""
else
    echo ""
    echo "❌ Errore durante la build"
    exit 1
fi
