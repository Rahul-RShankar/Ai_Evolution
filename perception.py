import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any

class PerceptionAgent:
    """
    Handles 'Seeing' and 'Hearing' by interacting with the web.
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def scrape_url(self, url: str) -> Dict[str, Any]:
        """
        Scrapes a URL and returns text content.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text(separator=' ', strip=True)
            title = soup.title.string if soup.title else "No Title"

            return {
                "url": url,
                "title": title,
                "content": text[:5000],  # Limit content size for LLM
                "success": True
            }
        except Exception as e:
            return {"url": url, "error": str(e), "success": False}

    def search_web(self, query: str) -> List[str]:
        """
        Mocks a web search returning a list of potential URLs.
        In a real scenario, this would use a Search API or DuckDuckGo.
        """
        # Placeholder: returning some common tech news/doc sites for testing
        print(f"Searching web for: {query}")
        return [
            f"https://www.google.com/search?q={query.replace(' ', '+')}",
            "https://en.wikipedia.org/wiki/" + query.replace(' ', '_'),
            "https://news.ycombinator.com"
        ]

if __name__ == "__main__":
    agent = PerceptionAgent()
    # Note: requests and bs4 need to be installed
    # result = agent.scrape_url("https://example.com")
    # print(result)
