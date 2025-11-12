#!/usr/bin/env python3
"""
Script per estrarre dati dei ricercatori altamente citati da Clarivate usando Playwright
Estrae: FULL NAME, CATEGORY, PRIMARY AFFILIATION, SECONDARY AFFILIATIONS
dalle pagine 1-714
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import csv
import time
import sys
from typing import List, Dict

def scrape_page(page, page_number: int) -> List[Dict[str, str]]:
    """
    Estrae i dati da una singola pagina usando Playwright

    Args:
        page: Oggetto page di Playwright
        page_number: Numero della pagina da scrapare (1-714)

    Returns:
        Lista di dizionari con i dati dei ricercatori
    """
    url = f"https://clarivate.com/highly-cited-researchers/?action=clv_hcr_members_filter&clv-paged={page_number}&clv-category=&clv-institution=&clv-region=&clv-name=&address1="

    try:
        # Naviga alla pagina e aspetta che il contenuto si carichi
        page.goto(url, wait_until='networkidle', timeout=60000)

        # Aspetta un momento per assicurarsi che il JavaScript abbia caricato i dati
        time.sleep(2)

        researchers = []

        # Prova diverse strategie per trovare i dati

        # Strategia 1: cerca per selettori comuni
        selectors_to_try = [
            '.researcher-item',
            '.member-item',
            '.hcr-member',
            'article.researcher',
            'div[class*="researcher"]',
            'div[class*="member"]',
            'tr.member',
            'li.researcher',
        ]

        researcher_elements = None
        for selector in selectors_to_try:
            try:
                researcher_elements = page.query_selector_all(selector)
                if researcher_elements and len(researcher_elements) > 0:
                    print(f"  Trovati elementi con selettore: {selector}")
                    break
            except:
                continue

        if not researcher_elements or len(researcher_elements) == 0:
            # Se non troviamo elementi specifici, proviamo a estrarre tutto il contenuto
            html_content = page.content()

            # Salviamo un esempio della pagina per debug
            if page_number == 1:
                with open('page_sample.html', 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"  Salvato esempio HTML in page_sample.html per analisi")

            return []

        # Estrai i dati da ogni elemento trovato
        for elem in researcher_elements:
            try:
                researcher_data = {
                    'full_name': '',
                    'category': '',
                    'primary_affiliation': '',
                    'secondary_affiliations': ''
                }

                # Cerca il nome
                name_selectors = ['h2', 'h3', 'h4', '.name', '.title', '[class*="name"]']
                for sel in name_selectors:
                    name_elem = elem.query_selector(sel)
                    if name_elem:
                        researcher_data['full_name'] = name_elem.inner_text().strip()
                        break

                # Cerca la categoria
                category_selectors = ['.category', '[class*="category"]', 'span.cat']
                for sel in category_selectors:
                    cat_elem = elem.query_selector(sel)
                    if cat_elem:
                        researcher_data['category'] = cat_elem.inner_text().strip()
                        break

                # Cerca l'affiliazione primaria
                primary_selectors = ['.primary-affiliation', '[class*="primary"]', '.affiliation', '[class*="institution"]']
                for sel in primary_selectors:
                    prim_elem = elem.query_selector(sel)
                    if prim_elem:
                        researcher_data['primary_affiliation'] = prim_elem.inner_text().strip()
                        break

                # Cerca le affiliazioni secondarie
                secondary_selectors = ['.secondary-affiliation', '[class*="secondary"]', '.secondary']
                for sel in secondary_selectors:
                    sec_elem = elem.query_selector(sel)
                    if sec_elem:
                        researcher_data['secondary_affiliations'] = sec_elem.inner_text().strip()
                        break

                # Aggiungi solo se abbiamo almeno il nome
                if researcher_data['full_name']:
                    researchers.append(researcher_data)

            except Exception as e:
                print(f"  Errore nell'estrazione dati da elemento: {e}")
                continue

        return researchers

    except PlaywrightTimeout:
        print(f"  Timeout durante il caricamento della pagina {page_number}")
        return []
    except Exception as e:
        print(f"  Errore nel scraping della pagina {page_number}: {e}")
        return []

def main():
    """Funzione principale per lo scraping di tutte le pagine"""

    print("Inizio scraping dei ricercatori altamente citati di Clarivate con Playwright")
    print("=" * 70)

    with sync_playwright() as p:
        # Lancia il browser
        print("\nAvvio del browser Chromium...")
        browser = p.chromium.launch(headless=True)

        # Crea un contesto con user agent personalizzato e ignora errori SSL
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            ignore_https_errors=True
        )

        page = context.new_page()

        # Test iniziale con la pagina 1
        print("\nTest iniziale con la pagina 1...")
        test_data = scrape_page(page, 1)

        if test_data:
            print(f"\n✓ Test riuscito! Trovati {len(test_data)} ricercatori nella pagina 1")
            print("\nEsempio del primo ricercatore:")
            print(f"  Nome: {test_data[0]['full_name']}")
            print(f"  Categoria: {test_data[0]['category']}")
            print(f"  Affiliazione primaria: {test_data[0]['primary_affiliation']}")
            print(f"  Affiliazioni secondarie: {test_data[0]['secondary_affiliations']}")
            print("\nProcedo con lo scraping di tutte le 714 pagine...")
        else:
            print("\n⚠ Nessun dato trovato nella pagina 1.")
            print("Controllare il file page_sample.html per analizzare la struttura.")
            print("\nVuoi che continui comunque? (Ctrl+C per interrompere)")
            time.sleep(5)

        all_researchers = []
        total_pages = 714

        # Iniziamo dalla pagina 1
        for page_num in range(1, total_pages + 1):
            print(f"\nScraping pagina {page_num}/{total_pages}...", end=" ")

            researchers = scrape_page(page, page_num)

            if researchers:
                all_researchers.extend(researchers)
                print(f"✓ {len(researchers)} ricercatori estratti (Totale: {len(all_researchers)})")
            else:
                print("✗ Nessun dato estratto")

            # Pausa per evitare di sovraccaricare il server
            if page_num % 50 == 0:
                print(f"  [Pausa di 5 secondi dopo {page_num} pagine...]")
                time.sleep(5)
            else:
                time.sleep(1)

            # Salvataggio intermedio ogni 100 pagine
            if page_num % 100 == 0 and all_researchers:
                print(f"  Salvataggio intermedio dopo {page_num} pagine...")
                save_to_csv(all_researchers, f'researchers_partial_{page_num}.csv')

        # Chiudi il browser
        browser.close()

        # Salvataggio finale
        print(f"\n{'='*70}")
        print(f"Scraping completato!")
        print(f"Totale ricercatori estratti: {len(all_researchers)}")

        if all_researchers:
            save_to_csv(all_researchers, 'highly_cited_researchers_complete.csv')
            print(f"\n✓ Dati salvati in: highly_cited_researchers_complete.csv")
        else:
            print("\n⚠ ATTENZIONE: Nessun dato estratto.")
            print("Controlla page_sample.html per analizzare la struttura della pagina.")

def save_to_csv(data: List[Dict[str, str]], filename: str):
    """Salva i dati in un file CSV"""
    if not data:
        print(f"Nessun dato da salvare in {filename}")
        return

    filepath = f'/home/user/sbert/{filename}'
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['full_name', 'category', 'primary_affiliation', 'secondary_affiliations']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for researcher in data:
            writer.writerow(researcher)

    print(f"  ✓ {len(data)} record salvati in {filepath}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrotto dall'utente. Uscita...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nErrore fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
