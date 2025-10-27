# 📊 SBERT Similarity Analyzer

Uno strumento professionale e riproducibile per analizzare la similarità semantica tra due testi usando **Sentence-BERT** (SBERT).

## 🎯 Caratteristiche Principali

- ✅ **Analisi cross-lingue**: Confronta testi in lingue diverse (es. Italiano vs Inglese)
- ✅ **SBERT reale**: Usa modelli di machine learning pre-addestrati per analisi semantica
- ✅ **Report dettagliato**: Metriche quantitative, visualizzazioni e interpretazioni
- ✅ **Analisi frase-per-frase**: Matrice di similarità per identificare corrispondenze specifiche
- ✅ **Completamente trasparente**: Codice visibile e verificabile per revisori
- ✅ **Interfaccia user-friendly**: App web interattiva con Streamlit

## 📋 Requisiti

- Python 3.8 o superiore
- 2GB di RAM minimo (per il modello SBERT)
- Connessione internet (solo al primo avvio per scaricare il modello)

## 🚀 Installazione

### 1. Clona il repository

```bash
git clone https://github.com/[tuo-username]/sbert.git
cd sbert
```

### 2. Installa le dipendenze

```bash
pip install -r requirements.txt
```

**Nota**: Al primo avvio, il modello SBERT (~90MB) verrà scaricato automaticamente.

## 💻 Utilizzo

### Avvia l'applicazione

```bash
streamlit run similarity_analyzer.py
```

L'app si aprirà automaticamente nel browser all'indirizzo `http://localhost:8501`

### Passaggi per l'analisi

1. **Inserisci i testi**: Copia e incolla i due testi da confrontare nelle aree di testo
2. **Personalizza etichette** (opzionale): Rinomina "Testo 1" e "Testo 2" per maggiore chiarezza
3. **Avvia analisi**: Clicca sul pulsante "🚀 Avvia Analisi"
4. **Leggi il report**: Ottieni metriche, visualizzazioni e interpretazioni

## 📊 Output del Report

Il report generato include:

### 1. Metriche Quantitative
- **Similarità SBERT**: Percentuale di sovrapposizione semantica (0-100%)
- **Lunghezza testi**: Confronto caratteri e parole
- **Differenza lunghezza**: Percentuale di divergenza in dimensione

### 2. Visualizzazioni
- **Metriche a colpo d'occhio**: Dashboard con valori principali
- **Matrice di similarità**: Heatmap frase-per-frase
- **Migliori corrispondenze**: Tabella delle frasi più simili

### 3. Interpretazione
- Analisi qualitativa automatica basata sul punteggio
- Indicazioni su:
  - Grado di sovrapposizione
  - Allineamento strutturale
  - Equivalenza terminologica

## 🔬 Metodologia

### Algoritmo SBERT

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Modello multilingue
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Conversione testi in embeddings (vettori semantici)
embedding1 = model.encode([text1])[0]
embedding2 = model.encode([text2])[0]

# 3. Calcolo similarità coseno
similarity = cosine_similarity([embedding1], [embedding2])[0][0]
```

### Perché SBERT?

- **Comprensione semantica**: Cattura il significato, non solo le parole
- **Cross-lingue**: Funziona su qualsiasi lingua senza traduzione
- **Veloce e leggero**: Risultati in pochi secondi anche per testi lunghi
- **Scientificamente validato**: Basato su BERT (Google) con ottimizzazioni per similarità

## 📈 Esempi di Utilizzo

### Caso d'uso 1: Confronto risposte AI
Confronta risposte di ChatGPT alla stessa domanda in italiano e inglese.

**Risultato atteso**: ~90% similarità (contenuti praticamente identici)

### Caso d'uso 2: Verifica traduzioni
Verifica quanto una traduzione è fedele all'originale.

**Risultato atteso**: >85% per traduzioni fedeli, <70% per parafrasi libere

### Caso d'uso 3: Analisi plagio
Confronta due documenti per identificare sovrapposizioni.

**Risultato atteso**: >80% indica forte sovrapposizione

## 🔧 Configurazione Avanzata

### Cambiare modello SBERT

Nel file `similarity_analyzer.py`, modifica la riga:

```python
model = SentenceTransformer('all-MiniLM-L6-v2')
```

Modelli alternativi:
- `all-mpnet-base-v2`: Più accurato ma più lento
- `paraphrase-multilingual-MiniLM-L12-v2`: Ottimizzato per multilingue
- `all-distilroberta-v1`: Bilanciato velocità/accuratezza

## 📝 Note per Revisori

### Riproducibilità

1. **Deterministico**: Stessi input → Stessi output
2. **Versionato**: Tutte le dipendenze con versioni fisse
3. **Open source**: Tutto il codice è visibile e modificabile

### Verifica Risultati

Per verificare i risultati:

```bash
# Esegui l'app
streamlit run similarity_analyzer.py

# Inserisci gli stessi testi usati nel report
# I risultati dovrebbero essere identici (±0.1% per arrotondamenti)
```

### Dipendenze Chiave

- `sentence-transformers`: Modello SBERT
- `scikit-learn`: Calcolo cosine similarity
- `streamlit`: Interfaccia web

Tutte le librerie sono open-source e ampiamente usate nella comunità scientifica.

## 🐛 Risoluzione Problemi

### Errore: "No module named 'sentence_transformers'"

```bash
pip install --upgrade sentence-transformers
```

### Errore: "CUDA not available"

Normal! L'app funziona anche senza GPU, usando la CPU.

### L'app è lenta al primo avvio

Il modello SBERT (~90MB) viene scaricato al primo utilizzo. Successivamente sarà istantaneo.

## 📄 Licenza

MIT License - Uso libero con attribuzione

## 👤 Autore

Sviluppato per analisi di similarità semantica cross-lingue riproducibili e trasparenti.

## 🔗 Risorse Utili

- [Sentence-BERT Paper](https://arxiv.org/abs/1908.10084)
- [Hugging Face Models](https://huggingface.co/sentence-transformers)
- [Streamlit Documentation](https://docs.streamlit.io)

---

**Versione**: 1.0.0  
**Ultimo aggiornamento**: Ottobre 2025
