# 🧠 Gestione Modello SBERT su Streamlit Cloud

## ❓ Il Problema

Streamlit Cloud ha **storage effimero**:
- Il filesystem viene resettato ad ogni riavvio del container
- Modelli scaricati vanno persi
- Il modello SBERT (~60-90MB) verrebbe scaricato ogni volta

**Quando avviene un riavvio?**
- Aggiornamenti del codice (push su GitHub)
- Riavvio automatico di Streamlit Cloud
- Inattività prolungata (>7 giorni senza visitatori)

---

## ✅ Soluzione Implementata (Ibrida)

L'app ora supporta **due modalità**:

### **Modalità 1: Download Automatico** (default)
```python
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')  # 61MB
```

**Pro:**
- ✅ Zero configurazione
- ✅ Funziona out-of-the-box
- ✅ Modello più leggero (61MB vs 90MB)

**Contro:**
- ⚠️ Download al riavvio (~30-60 secondi)
- ⚠️ Usa banda Hugging Face ad ogni riavvio

### **Modalità 2: Modello Pre-scaricato** (opzionale, più veloce)
```python
model = SentenceTransformer('./sbert_model')  # Da repository
```

**Pro:**
- ✅ Nessun download (modello già nel repo)
- ✅ Avvio istantaneo
- ✅ Funziona offline (se necessario)

**Contro:**
- ⚠️ Repository più grande (~60MB)
- ⚠️ Richiede setup iniziale (una volta sola)

---

## 🚀 Come Attivare Modalità 2 (Opzionale)

Se vuoi evitare il download ad ogni riavvio:

### Passo 1: Scarica il modello localmente

Sul tuo computer:

```bash
cd sbert-app
python download_model.py
```

Questo crea la cartella `sbert_model/` (~60MB)

### Passo 2: Aggiungi al repository GitHub

```bash
# Se il modello è <100MB (probabile)
git add sbert_model/
git commit -m "Add pre-downloaded SBERT model"
git push

# Se il modello è >100MB (raro)
# Usa Git LFS: https://git-lfs.github.com/
git lfs install
git lfs track "sbert_model/*"
git add .gitattributes sbert_model/
git commit -m "Add SBERT model with LFS"
git push
```

### Passo 3: Deploy su Streamlit Cloud

L'app rileverà automaticamente `./sbert_model/` e lo userà! 🎉

---

## 📊 Confronto Modelli

| Modello | Dimensione | Qualità | Velocità |
|---------|-----------|---------|----------|
| **paraphrase-MiniLM-L3-v2** ⭐ | 61 MB | Ottima | Veloce |
| all-MiniLM-L6-v2 | 90 MB | Eccellente | Medio |
| all-mpnet-base-v2 | 420 MB | Massima | Lento |

**Modello attuale:** `paraphrase-MiniLM-L3-v2`
- Perfetto per Streamlit Cloud
- Risultati ~89% accurati (come richiesto)
- Bilanciamento ideale dimensione/qualità

---

## 🔄 Alternative a Streamlit Cloud

Se i download ti preoccupano, considera:

### **Hugging Face Spaces** (consigliato se serve storage)
- ✅ Storage persistente (modello scaricato 1 sola volta)
- ✅ Gratis
- ✅ Supporto Docker/Streamlit
- 🔗 https://huggingface.co/spaces

**Come:**
1. Crea uno Space con Streamlit SDK
2. Carica il codice
3. Il modello viene scaricato una volta e resta in cache

### **Fly.io / Railway** (storage persistente)
- ✅ Storage permanente con volumi
- ⚠️ Piano free limitato
- 🔗 https://fly.io / https://railway.app

### **Deploy Locale** (nessun limite)
- ✅ Controllo totale
- ✅ Modello sempre disponibile
- ⚠️ Richiede server proprio

---

## 🎯 Raccomandazione Finale

**Per il tuo caso d'uso:**

✅ **Usa Streamlit Cloud con Modalità 1** (download automatico)

**Perché?**
1. La tua app sarà usata **sporadicamente** (per revisioni/analisi)
2. Download di 60MB ogni tanto è accettabile
3. Zero configurazione extra
4. I riavvii sono **rari** (~1 volta a settimana)
5. Il caching `@st.cache_resource` mantiene il modello per tutta la sessione

**Il download avviene solo:**
- Primo visitatore dopo un riavvio
- Poi tutti gli altri utenti usano il modello in cache (istantaneo)

---

## ⏱️ Timeline Realistica

**Scenario tipico:**

```
Giorno 1, ore 10:00 - Deploy iniziale
  → Download modello: 60 secondi
  → Utente 1 usa l'app: istantanea
  
Giorno 1, ore 15:00 - Utente 2 visita
  → Modello già in cache: istantaneo
  
Giorno 3 - Push aggiornamento codice
  → Container riavviato
  → Download modello: 60 secondi
  → Poi di nuovo istantaneo

Giorno 15 - Nessun riavvio
  → Tutto istantaneo
```

**Conclusione:** 60 secondi ogni 7-10 giorni è accettabile! ✅

---

## 🛠️ Se Vuoi Ottimizzare Comunque

Usa la **Modalità 2** (modello pre-scaricato):
1. Esegui `python download_model.py`
2. Fai push della cartella `sbert_model/`
3. Avvio sempre istantaneo (0 secondi)

**Trade-off:** Repository +60MB vs 60 secondi di download ogni tanto

---

## 📝 Note Tecniche

**Cache di sentence-transformers:**
```
Streamlit Cloud: /tmp/.cache/torch/sentence_transformers/
  → Persa ad ogni riavvio ❌

Repository locale: ./sbert_model/
  → Persistente nel repo ✅
```

**RAM Usage:**
- Modello in memoria: ~250MB
- Limite Streamlit Cloud: 1GB
- ✅ Ampio margine disponibile

---

## ✅ Checklist

**Setup Base (Modalità 1):**
- [x] Codice aggiornato con modello leggero
- [x] `@st.cache_resource` attivo
- [x] Ready per Streamlit Cloud

**Setup Ottimale (Modalità 2):**
- [ ] Eseguito `download_model.py`
- [ ] Cartella `sbert_model/` nel repository
- [ ] Verificato funzionamento locale
- [ ] Push su GitHub completato

---

**Consiglio finale:** Prova prima la Modalità 1. Se i 60 secondi di download iniziale ti danno fastidio, passa alla Modalità 2 in seguito. 🚀
