"""
Modulo per l'estrazione del testo completo dagli articoli
"""
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from typing import Optional, Dict
import logging
import time
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ContentScraper:
    """Gestisce l'estrazione del testo completo dagli URL delle notizie"""

    def __init__(self, config: Dict):
        self.config = config
        self.timeout = config['scraping']['timeout']
        self.max_retries = config['scraping']['max_retries']
        self.user_agent = config['scraping']['user_agent']
        self.headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

    def scrape_article(self, url: str, title: str = "") -> Dict:
        """
        Estrae il testo completo di un articolo usando newspaper3k

        Args:
            url: URL dell'articolo
            title: Titolo dell'articolo (opzionale, per logging)

        Returns:
            Dizionario con 'success', 'text', 'error'
        """
        result = {
            'success': False,
            'text': None,
            'error': None
        }

        # Verifica dominio
        domain = urlparse(url).netloc
        if self._is_excluded_domain(domain):
            result['error'] = f"Dominio escluso: {domain}"
            logger.debug(result['error'])
            return result

        # Prova prima con newspaper3k (più affidabile)
        try:
            logger.debug(f"Scraping with newspaper3k: {url}")
            article = Article(url, language='it')
            article.download()
            article.parse()

            if article.text and len(article.text) > 100:
                result['success'] = True
                result['text'] = article.text
                logger.info(f"Successfully scraped ({len(article.text)} chars): {title[:50]}...")
                return result
            else:
                logger.debug(f"Newspaper3k extracted insufficient text for: {url}")

        except Exception as e:
            logger.debug(f"Newspaper3k failed for {url}: {e}")

        # Fallback: BeautifulSoup
        try:
            logger.debug(f"Scraping with BeautifulSoup: {url}")
            text = self._scrape_with_beautifulsoup(url)

            if text and len(text) > 100:
                result['success'] = True
                result['text'] = text
                logger.info(f"Successfully scraped with BS4 ({len(text)} chars): {title[:50]}...")
                return result
            else:
                result['error'] = "Testo insufficiente estratto"
                logger.warning(f"Insufficient text for: {url}")

        except Exception as e:
            result['error'] = f"BeautifulSoup error: {str(e)}"
            logger.error(f"BeautifulSoup failed for {url}: {e}")

        return result

    def _scrape_with_beautifulsoup(self, url: str) -> Optional[str]:
        """
        Estrae il testo usando BeautifulSoup (fallback)

        Args:
            url: URL dell'articolo

        Returns:
            Testo estratto o None
        """
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    timeout=self.timeout,
                    allow_redirects=True
                )
                response.raise_for_status()
                response.encoding = response.apparent_encoding

                soup = BeautifulSoup(response.text, 'html.parser')

                # Rimuovi script, style, nav, footer, ads
                for element in soup(['script', 'style', 'nav', 'footer', 'aside',
                                    'header', 'iframe', 'noscript']):
                    element.decompose()

                # Rimuovi elementi comuni di advertising/tracking
                for class_name in ['advertisement', 'ads', 'social-share', 'comments',
                                  'related-articles', 'sidebar', 'menu']:
                    for element in soup.find_all(class_=lambda x: x and class_name in x.lower()):
                        element.decompose()

                # Cerca il contenuto principale
                main_content = None

                # Prova con tag article
                main_content = soup.find('article')

                # Prova con div contenuto principale
                if not main_content:
                    for class_name in ['article-body', 'article-content', 'post-content',
                                      'entry-content', 'content-body', 'main-content']:
                        main_content = soup.find(class_=lambda x: x and class_name in x.lower())
                        if main_content:
                            break

                # Fallback: cerca tutti i paragrafi
                if not main_content:
                    main_content = soup.find('body')

                if main_content:
                    # Estrai solo i paragrafi
                    paragraphs = main_content.find_all('p')
                    text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

                    # Pulizia finale
                    text = ' '.join(text.split())  # Normalizza spazi bianchi

                    return text if len(text) > 100 else None

                return None

            except requests.exceptions.RequestException as e:
                logger.debug(f"Attempt {attempt + 1}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise

        return None

    def _is_excluded_domain(self, domain: str) -> bool:
        """Verifica se il dominio è nella lista di esclusione"""
        excluded = self.config.get('excluded_domains', [])
        return any(excl in domain for excl in excluded)

    def scrape_batch(self, articles: list, delay: float = 2.0) -> Dict[str, Dict]:
        """
        Scrape multipli articoli con rate limiting

        Args:
            articles: Lista di dizionari con 'url' e 'title'
            delay: Pausa tra le richieste (secondi)

        Returns:
            Dizionario {url: result} con i risultati
        """
        results = {}
        total = len(articles)

        logger.info(f"Starting batch scraping of {total} articles")

        for i, article in enumerate(articles, 1):
            url = article['url']
            title = article.get('title', '')

            logger.info(f"Scraping {i}/{total}: {title[:50]}...")

            result = self.scrape_article(url, title)
            results[url] = result

            # Pausa tra le richieste
            if i < total:
                time.sleep(delay)

        # Statistiche
        successful = sum(1 for r in results.values() if r['success'])
        logger.info(f"Batch scraping completed: {successful}/{total} successful")

        return results

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Pulizia avanzata del testo estratto

        Args:
            text: Testo da pulire

        Returns:
            Testo pulito
        """
        if not text:
            return ""

        # Rimuovi spazi multipli
        text = ' '.join(text.split())

        # Rimuovi pattern comuni di noise
        noise_patterns = [
            'Cookie', 'Privacy Policy', 'Terms of Service',
            'Subscribe to our newsletter', 'Follow us on',
            'Share this article', 'Related Articles'
        ]

        lines = text.split('\n')
        cleaned_lines = []

        for line in lines:
            # Salta linee troppo corte o con noise
            if len(line.strip()) < 20:
                continue
            if any(pattern.lower() in line.lower() for pattern in noise_patterns):
                continue
            cleaned_lines.append(line.strip())

        return '\n\n'.join(cleaned_lines)
