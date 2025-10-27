#!/usr/bin/env python3
"""
Script per pre-scaricare il modello SBERT e includerlo nel repository
Esegui questo script LOCALMENTE prima di fare il push su GitHub
"""

from sentence_transformers import SentenceTransformer
import os

print("📥 Download modello SBERT...")

# Crea directory per il modello
model_dir = "./sbert_model"
os.makedirs(model_dir, exist_ok=True)

# Scarica il modello
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

# Salva il modello localmente
model.save(model_dir)

print(f"✅ Modello salvato in: {model_dir}")
print(f"📦 Dimensione: ~60MB")
print("\n⚠️  IMPORTANTE:")
print("1. Aggiungi questa directory al repository")
print("2. Se >100MB, usa Git LFS: https://git-lfs.github.com/")
print("3. Modifica similarity_analyzer.py per caricare da questa directory")
