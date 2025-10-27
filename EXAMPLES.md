# Esempi di Testi per Testare SBERT Similarity Analyzer

## Esempio 1: Risposte ChatGPT (Italiano vs Inglese)
### Risultato atteso: ~89-90% similarità

**Testo Italiano:**
```
L'acne cosmetica è una forma di acne causata dall'uso di prodotti cosmetici che ostruiscono i pori della pelle. Questi prodotti, come fondotinta, creme idratanti o oli per il viso, contengono ingredienti comedogenici (ad esempio, isopropyl myristate) che favoriscono la formazione di comedoni (punti neri e bianchi). L'ostruzione dei pori impedisce la normale eliminazione del sebo, creando un ambiente favorevole alla proliferazione di batteri e all'infiammazione. È importante rimuovere completamente il trucco ogni sera e scegliere prodotti etichettati come "non-comedogenici". L'olio minerale, se altamente raffinato, è generalmente considerato sicuro, ma alcune persone potrebbero comunque essere sensibili.
```

**Testo Inglese:**
```
Cosmetic acne is a type of acne caused by the use of cosmetic products that clog the pores of the skin. These products, such as foundations, moisturizers, or face oils, contain comedogenic ingredients (for example, isopropyl myristate) that promote the formation of comedones (blackheads and whiteheads). The blockage of pores prevents the normal elimination of sebum, creating an environment conducive to bacterial proliferation (particularly Cutibacterium acnes) and inflammation. It is important to completely remove makeup every evening and choose products labeled as "non-comedogenic." Mineral oil, when highly refined, is generally considered safe, but some individuals may still be sensitive to it.
```

---

## Esempio 2: Traduzione Fedele vs Parafrasi
### Risultato atteso: ~70-75% similarità

**Testo Originale:**
```
La fotosintesi clorofilliana è il processo attraverso cui le piante verdi convertono l'energia luminosa in energia chimica. Durante questo processo, l'anidride carbonica e l'acqua vengono trasformate in glucosio e ossigeno, utilizzando la luce solare come fonte di energia.
```

**Parafrasi:**
```
Le piante utilizzano la luce del sole per produrre il proprio nutrimento. Questo meccanismo biologico trasforma molecole semplici come CO2 e H2O in zuccheri complessi, rilasciando ossigeno nell'atmosfera come sottoprodotto della reazione.
```

---

## Esempio 3: Testi Completamente Diversi
### Risultato atteso: ~30-40% similarità

**Testo A:**
```
Il machine learning è una branca dell'intelligenza artificiale che permette ai computer di apprendere dai dati senza essere esplicitamente programmati. Gli algoritmi di ML identificano pattern e prendono decisioni basate su esempi precedenti.
```

**Testo B:**
```
La pizza napoletana è un piatto tradizionale italiano caratterizzato da una base sottile e morbida. Gli ingredienti principali sono pomodoro San Marzano, mozzarella di bufala, basilico fresco e olio extravergine di oliva.
```

---

## Esempio 4: Stessa Domanda, Risposte Simili
### Risultato atteso: ~85-88% similarità

**Risposta 1:**
```
I benefici della meditazione includono la riduzione dello stress, il miglioramento della concentrazione e la regolazione delle emozioni. Praticare meditazione quotidianamente può anche abbassare la pressione sanguigna e migliorare la qualità del sonno. Molti studi scientifici confermano questi effetti positivi sul benessere mentale e fisico.
```

**Risposta 2:**
```
Meditare regolarmente porta numerosi vantaggi per la salute. Tra questi, troviamo una significativa riduzione dell'ansia, maggiore capacità di focus e controllo emotivo. Inoltre, la pratica meditativa contribuisce a normalizzare la pressione arteriosa e favorisce un riposo notturno più profondo. La ricerca scientifica supporta ampiamente questi benefici.
```

---

## Come Usare Questi Esempi

1. Copia uno dei testi in "Testo 1"
2. Copia il testo corrispondente in "Testo 2"
3. Clicca "Avvia Analisi"
4. Confronta il risultato con quello atteso

## Note

- I risultati possono variare leggermente (±2-3%) a seconda della versione del modello
- SBERT è deterministico: stessi input = stessi output
- Per verificare la riproducibilità, esegui più volte la stessa analisi
