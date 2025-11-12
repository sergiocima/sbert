#!/usr/bin/env python3
"""
Script per estrarre dati dei ricercatori altamente citati da Clarivate
Estrae: FULL NAME, CATEGORY, PRIMARY AFFILIATION, SECONDARY AFFILIATIONS
dalle pagine 1-714
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import sys
from typing import List, Dict

def scrape_page(page_number: int, session: requests.Session) -> List[Dict[str, str]]:
    """
    Estrae i dati da una singola pagina

    Args:
        page_number: Numero della pagina da scrapare (1-714)
        session: Sessione requests per mantenere le connessioni

    Returns:
        Lista di dizionari con i dati dei ricercatori
    """
    url = f"https://clarivate.com/highly-cited-researchers/?action=clv_hcr_members_filter&clv-paged={page_number}&clv-category=&clv-institution=&clv-region=&clv-name=&address1="

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
    }

    try:
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')
        researchers = []

        # Cerca i contenitori dei ricercatori
        # La struttura HTML può variare, quindi proviamo diverse opzioni

        # Opzione 1: cerca per classe o ID specifico
        researcher_items = soup.find_all(['div', 'article', 'li'], class_=lambda x: x and ('researcher' in x.lower() or 'member' in x.lower() or 'hcr' in x.lower()))

        # Opzione 2: cerca per struttura di tabella
        if not researcher_items:
            researcher_items = soup.find_all('tr', class_=lambda x: x and 'row' in x.lower())

        # Opzione 3: cerca in modo più generico
        if not researcher_items:
            # Cerca tutti i div che potrebbero contenere dati strutturati
            researcher_items = soup.find_all(['div', 'article'], class_=True)

        print(f"Pagina {page_number}: trovati {len(researcher_items)} potenziali elementi")

        for item in researcher_items:
            researcher_data = {
                'full_name': '',
                'category': '',
                'primary_affiliation': '',
                'secondary_affiliations': ''
            }

            # Cerca il nome
            name_elem = item.find(['h2', 'h3', 'h4', 'span', 'div', 'td'],
                                  class_=lambda x: x and ('name' in x.lower() or 'title' in x.lower()))
            if name_elem:
                researcher_data['full_name'] = name_elem.get_text(strip=True)

            # Cerca la categoria
            category_elem = item.find(['span', 'div', 'p', 'td'],
                                     class_=lambda x: x and 'category' in x.lower())
            if category_elem:
                researcher_data['category'] = category_elem.get_text(strip=True)

            # Cerca l'affiliazione primaria
            primary_elem = item.find(['span', 'div', 'p', 'td'],
                                    class_=lambda x: x and ('primary' in x.lower() or 'affiliation' in x.lower() or 'institution' in x.lower()))
            if primary_elem:
                researcher_data['primary_affiliation'] = primary_elem.get_text(strip=True)

            # Cerca le affiliazioni secondarie
            secondary_elem = item.find(['span', 'div', 'p', 'td'],
                                       class_=lambda x: x and 'secondary' in x.lower())
            if secondary_elem:
                researcher_data['secondary_affiliations'] = secondary_elem.get_text(strip=True)

            # Aggiungi solo se abbiamo almeno il nome
            if researcher_data['full_name']:
                researchers.append(researcher_data)

        # Se non abbiamo trovato nulla con il metodo specifico, proviamo un parsing più generale
        if not researchers:
            # Stampa un esempio della struttura HTML per debug
            print(f"\n=== STRUTTURA HTML PAGINA {page_number} (primi 2000 caratteri) ===")
            print(str(soup)[:2000])
            print("="*60)

        return researchers

    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta alla pagina {page_number}: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Errore nel parsing della pagina {page_number}: {e}", file=sys.stderr)
        return []

def main():
    """Funzione principale per lo scraping di tutte le pagine"""

    print("Inizio scraping dei ricercatori altamente citati di Clarivate")
    print("=" * 60)

    # Prima facciamo un test con la pagina 1 per capire la struttura
    print("\nTest iniziale con la pagina 1...")

    session = requests.Session()
    test_data = scrape_page(1, session)

    if test_data:
        print(f"\n✓ Test riuscito! Trovati {len(test_data)} ricercatori nella pagina 1")
        print("\nEsempio del primo ricercatore:")
        print(f"  Nome: {test_data[0]['full_name']}")
        print(f"  Categoria: {test_data[0]['category']}")
        print(f"  Affiliazione primaria: {test_data[0]['primary_affiliation']}")
        print(f"  Affiliazioni secondarie: {test_data[0]['secondary_affiliations']}")
        print("\nProcedo con lo scraping di tutte le 714 pagine...")
    else:
        print("\n⚠ Nessun dato trovato nella pagina 1. Verifico la struttura HTML...")
        # Il messaggio di debug verrà stampato dalla funzione scrape_page
        print("\nVuoi continuare comunque? (potrebbe essere necessario analizzare manualmente la struttura)")
        # Per ora continuiamo

    all_researchers = []
    total_pages = 714

    # Iniziamo dalla pagina 1 se il test è andato bene
    for page in range(1, total_pages + 1):
        print(f"\nScraping pagina {page}/{total_pages}...", end=" ")

        researchers = scrape_page(page, session)

        if researchers:
            all_researchers.extend(researchers)
            print(f"✓ {len(researchers)} ricercatori estratti")
        else:
            print("✗ Nessun dato estratto")

        # Pausa per evitare di sovraccaricare il server
        # Aumentiamo la pausa ogni 50 pagine
        if page % 50 == 0:
            print(f"  [Pausa di 5 secondi dopo {page} pagine...]")
            time.sleep(5)
        else:
            time.sleep(1)  # 1 secondo tra le richieste

        # Salvataggio intermedio ogni 100 pagine
        if page % 100 == 0:
            print(f"\n  Salvataggio intermedio dopo {page} pagine...")
            save_to_csv(all_researchers, f'researchers_partial_{page}.csv')

    # Salvataggio finale
    print(f"\n{'='*60}")
    print(f"Scraping completato!")
    print(f"Totale ricercatori estratti: {len(all_researchers)}")

    if all_researchers:
        save_to_csv(all_researchers, 'highly_cited_researchers_complete.csv')
        print(f"\nDati salvati in: highly_cited_researchers_complete.csv")
    else:
        print("\n⚠ ATTENZIONE: Nessun dato estratto. Potrebbe essere necessario analizzare la struttura HTML.")

def save_to_csv(data: List[Dict[str, str]], filename: str):
    """Salva i dati in un file CSV"""
    if not data:
        print(f"Nessun dato da salvare in {filename}")
        return

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['full_name', 'category', 'primary_affiliation', 'secondary_affiliations']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for researcher in data:
            writer.writerow(researcher)

    print(f"  ✓ {len(data)} record salvati in {filename}")

if __name__ == "__main__":
    main()
