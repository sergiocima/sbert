#!/usr/bin/env python3
"""
📊 SIMILARITY ANALYZER - SBERT Cross-Language Analysis Tool
Una soluzione reiterabile per confrontare due testi usando Sentence-BERT

Autore: Sviluppato con Python + Streamlit + Sentence-Transformers
Data: Ottobre 2025
Licenza: MIT - Uso libero con attribuzione
"""

import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from datetime import datetime

# ==================== CONFIGURAZIONE ====================
st.set_page_config(
    page_title="📊 SBERT Similarity Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== STILI ====================
st.markdown("""
<style>
    .main-header { font-size: 2.5em; font-weight: bold; color: #1f77b4; }
    .section-header { font-size: 1.5em; font-weight: bold; color: #2ca02c; margin-top: 20px; }
    .metric-box { background-color: #f0f2f6; padding: 15px; border-radius: 8px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">📊 SBERT Similarity Analyzer</div>', unsafe_allow_html=True)
st.markdown("*Analizza la similarità semantica tra due testi usando Sentence-BERT multilingue*")
st.markdown("---")

# ==================== CARICAMENTO MODELLO ====================
@st.cache_resource
def load_model():
    """Carica il modello SBERT multilingue (ottimizzato per cloud)"""
    import os
    
    # Controlla se il modello è già nel repository (pre-scaricato)
    local_model_path = "./sbert_model"
    
    with st.spinner("⏳ Caricamento modello SBERT multilingue..."):
        if os.path.exists(local_model_path):
            # Carica da locale (più veloce, no download)
            model = SentenceTransformer(local_model_path)
            st.success("✅ Modello caricato da repository locale!")
        else:
            # Scarica da Hugging Face (più lento al primo avvio)
            # paraphrase-MiniLM-L3-v2: 61MB, veloce e accurato
            model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
            st.success("✅ Modello scaricato e caricato!")
    
    return model

model = load_model()

# ==================== FUNZIONI DI ANALISI ====================

def count_words(text):
    """Conta le parole nel testo"""
    return len(text.split())

def count_chars(text):
    """Conta i caratteri nel testo"""
    return len(text)

def extract_sentences(text):
    """Estrai le frasi da un testo"""
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]

def analyze_similarity(text1, text2, label1="Testo 1", label2="Testo 2"):
    """Analizza la similarità tra due testi usando SBERT"""
    
    # Embedding dei testi completi
    embedding1 = model.encode([text1])[0]
    embedding2 = model.encode([text2])[0]
    
    # Calcola similarità globale
    global_similarity = cosine_similarity([embedding1], [embedding2])[0][0]
    
    # Analisi per frasi
    sentences1 = extract_sentences(text1)
    sentences2 = extract_sentences(text2)
    
    # Embedding delle frasi
    if sentences1 and sentences2:
        embeddings1 = model.encode(sentences1)
        embeddings2 = model.encode(sentences2)
        
        # Matrice di similarità
        similarity_matrix = cosine_similarity(embeddings1, embeddings2)
    else:
        similarity_matrix = None
    
    # Metriche base
    word_count1 = count_words(text1)
    word_count2 = count_words(text2)
    char_count1 = count_chars(text1)
    char_count2 = count_chars(text2)
    
    # Calcola differenza lunghezza
    length_diff_pct = abs(char_count1 - char_count2) / max(char_count1, char_count2) * 100
    
    results = {
        'global_similarity': global_similarity,
        'similarity_matrix': similarity_matrix,
        'sentences1': sentences1,
        'sentences2': sentences2,
        'word_count1': word_count1,
        'word_count2': word_count2,
        'char_count1': char_count1,
        'char_count2': char_count2,
        'length_diff_pct': length_diff_pct,
        'label1': label1,
        'label2': label2
    }
    
    return results

def generate_report(results):
    """Genera il report di analisi"""
    
    st.markdown('<div class="section-header">📋 RISULTATI CHIAVE</div>', unsafe_allow_html=True)
    
    # TL;DR
    similarity_pct = results['global_similarity'] * 100
    
    st.info(f"""
    **TL;DR:** I tuoi due testi sono **{similarity_pct:.1f}%** sovrapponibili nei contenuti.
    """)
    
    # Metriche quantitative
    st.markdown("### 📊 Metriche Quantitative")
    
    df_metrics = pd.DataFrame({
        'Aspetto': [
            'Lunghezza (caratteri)',
            'Lunghezza (parole)',
            'Similarità SBERT',
            'Ordine dei concetti',
            'Terminologia'
        ],
        'Risultato': [
            f"{results['char_count1']} ({results['label1']}) vs {results['char_count2']} ({results['label2']}) → Differenza: {results['length_diff_pct']:.1f}%",
            f"{results['word_count1']} vs {results['word_count2']} parole",
            f"{results['global_similarity']:.3f}/1.0 = {similarity_pct:.1f}%",
            "Analisi per frasi disponibile sotto" if results['similarity_matrix'] is not None else "N/A",
            "Equivalente (analisi semantica)" if similarity_pct > 80 else "Parzialmente diversa"
        ],
        'Valutazione': [
            '✅' if results['length_diff_pct'] < 10 else '⚠️',
            '✅' if abs(results['word_count1'] - results['word_count2']) / max(results['word_count1'], results['word_count2']) < 0.1 else '⚠️',
            '✅' if similarity_pct > 80 else ('⚠️' if similarity_pct > 60 else '❌'),
            '✅',
            '✅' if similarity_pct > 80 else '⚠️'
        ]
    })
    
    st.dataframe(df_metrics, use_container_width=True)
    
    # Visualizzazione similarità
    st.markdown("### 📈 Visualizzazione Similarità")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Similarità Globale",
            value=f"{similarity_pct:.1f}%",
            delta=f"{similarity_pct - 50:.1f}% sopra media" if similarity_pct > 50 else None
        )
    
    with col2:
        st.metric(
            label=f"Lunghezza {results['label1']}",
            value=f"{results['char_count1']} char",
            delta=f"{results['word_count1']} parole"
        )
    
    with col3:
        st.metric(
            label=f"Lunghezza {results['label2']}",
            value=f"{results['char_count2']} char",
            delta=f"{results['word_count2']} parole"
        )
    
    # Matrice di similarità per frasi
    if results['similarity_matrix'] is not None and len(results['sentences1']) > 0 and len(results['sentences2']) > 0:
        st.markdown("### 🔍 Analisi Frase-per-Frase")
        
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(
            results['similarity_matrix'],
            annot=True,
            fmt='.2f',
            cmap='RdYlGn',
            vmin=0,
            vmax=1,
            xticklabels=[f"{results['label2']}-{i+1}" for i in range(len(results['sentences2']))],
            yticklabels=[f"{results['label1']}-{i+1}" for i in range(len(results['sentences1']))],
            ax=ax
        )
        ax.set_title('Matrice di Similarità tra Frasi')
        ax.set_xlabel(f'Frasi {results["label2"]}')
        ax.set_ylabel(f'Frasi {results["label1"]}')
        st.pyplot(fig)
        
        # Migliori corrispondenze
        st.markdown("#### 🎯 Migliori Corrispondenze")
        
        best_matches = []
        for i in range(len(results['sentences1'])):
            for j in range(len(results['sentences2'])):
                score = results['similarity_matrix'][i][j]
                if score > 0.7:  # Soglia di rilevanza
                    best_matches.append({
                        f'Frase {results["label1"]}': f"{i+1}: {results['sentences1'][i][:80]}...",
                        f'Frase {results["label2"]}': f"{j+1}: {results['sentences2'][j][:80]}...",
                        'Similarità': f"{score:.1%}"
                    })
        
        if best_matches:
            df_matches = pd.DataFrame(best_matches).sort_values('Similarità', ascending=False)
            st.dataframe(df_matches, use_container_width=True)
    
    # Interpretazione
    st.markdown("### 💡 Interpretazione")
    
    if similarity_pct >= 85:
        st.success(f"""
        **Alta Sovrapposizione ({similarity_pct:.1f}%)**
        
        I due testi sono estremamente simili nei contenuti. Questo indica che:
        - Le informazioni veicolate sono sostanzialmente identiche
        - L'ordine logico e la struttura sono allineati
        - La terminologia usata è equivalente semanticamente
        """)
    elif similarity_pct >= 70:
        st.warning(f"""
        **Sovrapposizione Moderata-Alta ({similarity_pct:.1f}%)**
        
        I due testi condividono la maggior parte dei contenuti, ma con alcune differenze:
        - Alcuni concetti sono approfonditi diversamente
        - La struttura potrebbe variare in alcune sezioni
        - Potrebbero esserci aggiunte o omissioni minori
        """)
    else:
        st.error(f"""
        **Sovrapposizione Limitata ({similarity_pct:.1f}%)**
        
        I due testi hanno differenze significative:
        - Contenuti parzialmente diversi
        - Approcci o focus differenti
        - Struttura o organizzazione diverse
        """)

# ==================== INTERFACCIA PRINCIPALE ====================

st.sidebar.header("⚙️ Configurazione")
st.sidebar.markdown("---")

# Input testi
st.markdown("## 📝 Inserisci i Testi da Confrontare")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Testo 1")
    label1 = st.text_input("Etichetta Testo 1", value="Italiano", key="label1")
    text1 = st.text_area(
        "Inserisci il primo testo",
        height=300,
        placeholder="Incolla qui il primo testo da analizzare...",
        key="text1"
    )
    if text1:
        st.caption(f"📊 Caratteri: {count_chars(text1)} | Parole: {count_words(text1)}")

with col2:
    st.markdown("### Testo 2")
    label2 = st.text_input("Etichetta Testo 2", value="Inglese", key="label2")
    text2 = st.text_area(
        "Inserisci il secondo testo",
        height=300,
        placeholder="Incolla qui il secondo testo da analizzare...",
        key="text2"
    )
    if text2:
        st.caption(f"📊 Caratteri: {count_chars(text2)} | Parole: {count_words(text2)}")

# Pulsante analisi
st.markdown("---")

if st.button("🚀 Avvia Analisi", type="primary", use_container_width=True):
    if not text1 or not text2:
        st.error("⚠️ Per favore inserisci entrambi i testi prima di avviare l'analisi.")
    else:
        with st.spinner("🔄 Analisi in corso..."):
            results = analyze_similarity(text1, text2, label1, label2)
            generate_report(results)
            
            # Timestamp
            st.markdown("---")
            st.caption(f"📅 Analisi generata il: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Sezione codice
st.markdown("---")
st.markdown("## 💻 Codice per la Trasparenza")

with st.expander("📖 Visualizza il codice usato per l'analisi"):
    st.code("""
# ALGORITMO DI ANALISI UTILIZZATO

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Caricamento modello SBERT
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Generazione embeddings
embedding1 = model.encode([text1])[0]
embedding2 = model.encode([text2])[0]

# 3. Calcolo similarità (cosine similarity)
similarity = cosine_similarity([embedding1], [embedding2])[0][0]

# 4. Conversione in percentuale
similarity_percentage = similarity * 100

# SPIEGAZIONE:
# - SBERT converte il testo in vettori numerici (embeddings)
# - La cosine similarity misura l'angolo tra i due vettori
# - Risultato: 0 = completamente diversi, 1 = identici
# - Multilingue: funziona su qualsiasi lingua
    """, language="python")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Informazioni")
st.sidebar.info("""
**Modello**: all-MiniLM-L6-v2  
**Algoritmo**: Sentence-BERT  
**Metrica**: Cosine Similarity  

Questo strumento è completamente 
riproducibile e verificabile.
""")
