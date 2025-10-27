#!/bin/bash

# Script per caricare i file sul repository GitHub
# Esegui questo script dal tuo computer dopo aver scaricato i file

echo "🚀 Caricamento file su GitHub: sergiocima/bert"
echo "================================================"
echo ""

# Naviga nella directory del progetto
cd "$(dirname "$0")"

# Verifica che Git sia installato
if ! command -v git &> /dev/null; then
    echo "❌ Errore: Git non è installato. Installalo prima di procedere."
    exit 1
fi

# Configura Git (modifica con i tuoi dati se necessario)
echo "📝 Configurazione Git..."
git config user.name "sergiocima"
git config user.email "sergio.cima@example.com"  # Modifica con la tua email

# Inizializza repository se non esiste
if [ ! -d ".git" ]; then
    echo "🔧 Inizializzazione repository Git..."
    git init
    git branch -M main
fi

# Aggiungi remote se non esiste
if ! git remote | grep -q origin; then
    echo "🔗 Aggiunta remote..."
    git remote add origin https://github.com/sergiocima/bert.git
fi

# Aggiungi tutti i file
echo "📦 Aggiunta file..."
git add .

# Verifica se ci sono modifiche da committare
if git diff --staged --quiet; then
    echo "ℹ️  Nessuna modifica da committare"
else
    # Commit
    echo "💾 Commit..."
    git commit -m "SBERT Similarity Analyzer - App completa

- App Streamlit con analisi SBERT multilingue
- Report dettagliato con metriche e visualizzazioni  
- Documentazione completa con esempi
- Codice trasparente per revisori"
fi

# Pull con merge (gestisce eventuali file esistenti)
echo "⬇️  Sincronizzazione con repository remoto..."
git pull origin main --allow-unrelated-histories --no-edit 2>/dev/null || echo "⚠️  Prima volta - nessun file remoto da sincronizzare"

# Push
echo "⬆️  Caricamento su GitHub..."
if git push -u origin main; then
    echo ""
    echo "✅ Caricamento completato con successo!"
    echo "🌐 Repository: https://github.com/sergiocima/bert"
    echo ""
    echo "📋 File caricati:"
    echo "  - similarity_analyzer.py (App principale)"
    echo "  - requirements.txt (Dipendenze)"
    echo "  - README.md (Documentazione)"
    echo "  - EXAMPLES.md (Esempi di test)"
    echo "  - .gitignore (Configurazione Git)"
    echo "  - LICENSE (Licenza MIT)"
else
    echo ""
    echo "❌ Errore durante il push"
    echo ""
    echo "💡 Possibili soluzioni:"
    echo "  1. Verifica di avere i permessi sul repository"
    echo "  2. Configura l'autenticazione GitHub:"
    echo "     - Token: https://github.com/settings/tokens"
    echo "     - SSH: https://docs.github.com/en/authentication"
    echo "  3. Verifica la connessione internet"
    echo ""
    echo "🔧 Push manuale:"
    echo "  git push -u origin main"
fi
