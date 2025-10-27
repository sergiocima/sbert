# 📤 Istruzioni per Caricare i File su GitHub

## 🎯 Opzione 1: Script Automatico (Consigliato)

### Passo 1: Scarica i file
Tutti i file sono pronti in questa directory.

### Passo 2: Esegui lo script
```bash
cd sbert-app
./push-to-github.sh
```

Lo script farà automaticamente:
- ✅ Inizializzazione repository Git
- ✅ Configurazione remote GitHub
- ✅ Commit di tutti i file
- ✅ Sincronizzazione con repository remoto
- ✅ Push su https://github.com/sergiocima/bert

---

## 🔧 Opzione 2: Comandi Manuali

Se preferisci eseguire i comandi uno per uno:

```bash
# 1. Vai nella directory
cd sbert-app

# 2. Inizializza Git (se non già fatto)
git init
git branch -M main

# 3. Configura Git (modifica con i tuoi dati)
git config user.name "sergiocima"
git config user.email "tua-email@example.com"

# 4. Aggiungi remote
git remote add origin https://github.com/sergiocima/bert.git

# 5. Aggiungi tutti i file
git add .

# 6. Commit
git commit -m "SBERT Similarity Analyzer - App completa"

# 7. Pull (se il repository ha già dei file)
git pull origin main --allow-unrelated-histories --no-edit

# 8. Push
git push -u origin main
```

---

## 🔐 Autenticazione GitHub

Se ricevi errori di autenticazione, hai due opzioni:

### Opzione A: Personal Access Token (più semplice)

1. Vai su: https://github.com/settings/tokens
2. Clicca "Generate new token (classic)"
3. Seleziona: `repo` (full control)
4. Genera il token e copialo
5. Quando fai `git push`, usa:
   - Username: `sergiocima`
   - Password: `[il tuo token]`

### Opzione B: SSH Key

1. Genera chiave SSH: `ssh-keygen -t ed25519 -C "tua-email@example.com"`
2. Aggiungi chiave a GitHub: https://github.com/settings/keys
3. Cambia remote: `git remote set-url origin git@github.com:sergiocima/bert.git`

---

## 📂 File Inclusi nel Caricamento

```
sbert-app/
├── similarity_analyzer.py    # App Streamlit principale
├── requirements.txt           # Dipendenze Python
├── README.md                  # Documentazione completa
├── EXAMPLES.md                # Esempi di test
├── LICENSE                    # Licenza MIT
├── .gitignore                 # File da escludere
└── push-to-github.sh          # Questo script
```

---

## ✅ Verifica Caricamento

Dopo il push, verifica su:
https://github.com/sergiocima/bert

Dovresti vedere tutti i file elencati sopra.

---

## ❓ Risoluzione Problemi

### Errore: "Permission denied"
- Verifica le credenziali GitHub
- Assicurati di avere i permessi di scrittura sul repository

### Errore: "Repository not found"
- Verifica che il repository `bert` esista su GitHub
- Controlla di essere loggato con l'account `sergiocima`

### Errore: "fatal: refusing to merge unrelated histories"
- Usa: `git pull origin main --allow-unrelated-histories`

### Il push richiede username/password ogni volta
- Configura SSH invece di HTTPS (vedi Opzione B sopra)
- Oppure usa credential helper: `git config --global credential.helper store`

---

## 🚀 Test Post-Caricamento

Dopo aver caricato i file:

1. Clona il repository su un'altra macchina:
   ```bash
   git clone https://github.com/sergiocima/bert.git
   cd bert
   ```

2. Installa dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

3. Avvia l'app:
   ```bash
   streamlit run similarity_analyzer.py
   ```

4. Test con esempi:
   - Apri `EXAMPLES.md`
   - Copia i testi di esempio nell'app
   - Verifica che i risultati corrispondano a quelli attesi

---

## 📧 Supporto

Se hai problemi:
1. Controlla la documentazione in `README.md`
2. Verifica che Git sia installato: `git --version`
3. Controlla i permessi GitHub
4. Verifica la connessione: `ping github.com`

---

**Ultimo aggiornamento**: Ottobre 2025
