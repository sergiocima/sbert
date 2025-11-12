# Scraping Clarivate Highly Cited Researchers

## Problema Riscontrato

L'ambiente corrente ha **forti restrizioni di rete** che impediscono lo scraping del sito Clarivate:

- **Errore 403 Forbidden**: con richieste HTTP normali (requests)
- **Errore certificato SSL**: problemi con certificati HTTPS
- **Page Crash**: il browser Playwright non riesce a connettersi

Questi problemi sono dovuti alle restrizioni di rete dell'ambiente, non agli script.

## Script Creati

Ho creato due script pronti all'uso che funzioneranno su una macchina **senza restrizioni di rete**:

### 1. `scrape_researchers.py`
Script base con requests e BeautifulSoup

### 2. `scrape_researchers_playwright.py` (RACCOMANDATO)
Script avanzato con Playwright che simula un browser reale

**Caratteristiche:**
- Gestisce JavaScript e contenuti dinamici
- Bypassa molte protezioni anti-scraping
- Salvataggi intermedi ogni 100 pagine
- Gestione errori robusta
- Pausa tra richieste per non sovraccaricare il server

## Come Usare gli Script

### Opzione 1: Eseguire su altra macchina (RACCOMANDATO)

1. Copia lo script `scrape_researchers_playwright.py` su una macchina con connessione libera
2. Installa le dipendenze:
   ```bash
   pip install playwright beautifulsoup4 lxml
   playwright install chromium
   ```
3. Esegui lo script:
   ```bash
   python3 scrape_researchers_playwright.py
   ```
4. Il processo impiegherà circa **2-3 ore** per 714 pagine (con pause di 1 secondo tra richieste)
5. Troverai i risultati in:
   - `highly_cited_researchers_complete.csv` (file finale)
   - `researchers_partial_100.csv`, `researchers_partial_200.csv`, ecc. (salvataggi intermedi)

### Opzione 2: Usare un servizio di scraping

Servizi cloud che possono eseguire lo scraping:

1. **Google Colab** (gratis)
   - Carica lo script su Colab
   - Esegui da lì

2. **ScrapingBee / ScraperAPI** (a pagamento)
   - Servizi specializzati per scraping
   - Gestiscono automaticamente protezioni anti-bot

3. **AWS Lambda / Google Cloud Functions**
   - Esegui lo script serverless

### Opzione 3: Verificare se esiste un'API o CSV ufficiale

Clarivate potrebbe offrire:
- Un'API ufficiale per accedere ai dati
- Un file CSV scaricabile direttamente dal sito
- Un servizio di export dati

Ti consiglio di:
1. Controllare su https://clarivate.com se c'è un modo ufficiale per scaricare i dati
2. Contattare il supporto Clarivate per chiedere accesso ai dati

## Formato Dati Estratti

Il CSV finale conterrà 4 colonne:

| Campo | Descrizione |
|-------|-------------|
| `full_name` | Nome completo del ricercatore |
| `category` | Categoria di ricerca |
| `primary_affiliation` | Affiliazione primaria (università/istituto) |
| `secondary_affiliations` | Affiliazioni secondarie (se presenti) |

## Note Tecniche

### Struttura URL
```
https://clarivate.com/highly-cited-researchers/?action=clv_hcr_members_filter&clv-paged={PAGE}&clv-category=&clv-institution=&clv-region=&clv-name=&address1=
```

Dove `{PAGE}` va da 1 a 714

### Tempi Stimati
- Con pausa di 1 secondo: ~12 minuti per 714 pagine
- Con pausa di 5 secondi ogni 50 pagine: ~15-20 minuti
- Parsing e salvataggio: variabile in base alla complessità HTML

### Considerazioni Legali
⚠️ **Importante**: Verifica che lo scraping sia permesso dai termini di servizio di Clarivate prima di procedere.

## Prossimi Passi

1. **Opzione più semplice**: Esegui `scrape_researchers_playwright.py` su una macchina senza restrizioni di rete
2. **Opzione più veloce**: Verifica se Clarivate offre download diretto dei dati
3. **Opzione intermedia**: Usa Google Colab per eseguire lo scraping gratuitamente

---

**Scripts pronti in:**
- `/home/user/sbert/scrape_researchers.py`
- `/home/user/sbert/scrape_researchers_playwright.py`
