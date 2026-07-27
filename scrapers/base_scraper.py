import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional

class BaseScraper:
    def __init__(self, store_name: str, config: Dict):
        self.store_name = store_name
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"❌ Error al obtener {url}: {e}")
            return None
    
    def extract_price(self, soup: BeautifulSoup) -> Optional[float]:
        raise NotImplementedError("Cada scraper debe implementar extract_price")
    
    def extract_name(self, soup: BeautifulSoup) -> Optional[str]:
        raise NotImplementedError("Cada scraper debe implementar extract_name")
