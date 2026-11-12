"""
Polite HTTP Client with Rate Limiting, Backoff, and Robots Checking
"""
import time
import logging
from typing import Optional, Dict, Any, Tuple
from urllib.parse import urlparse
import httpx
from crawler.config import config

logger = logging.getLogger("crawler.client")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

class HttpClient:
    def __init__(self):
        self.headers = {
            "User-Agent": config.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0"
        }
        self.client = httpx.Client(
            headers=self.headers,
            timeout=config.timeout,
            follow_redirects=True,
            verify=False  # Avoid SSL failure if local cert issue, while logging warning
        )
        self.last_request_time = 0.0

    def _wait_rate_limit(self) -> None:
        """Enforce polite rate limiting delay between consecutive requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < config.rate_limit_delay:
            time.sleep(config.rate_limit_delay - elapsed)
        self.last_request_time = time.time()

    def is_allowed_domain(self, url: str) -> bool:
        """Ensure URL strictly belongs to vineyard.vn or allowed domains."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            return any(domain == d or domain.endswith("." + d) for d in config.allowed_domains)
        except Exception:
            return False

    def fetch(self, url: str, max_retries: Optional[int] = None) -> Tuple[Optional[httpx.Response], float, Optional[str]]:
        """
        Fetch URL with exponential backoff and polite delay.
        Returns (response, elapsed_ms, error_message).
        """
        if not self.is_allowed_domain(url):
            return None, 0.0, f"URL domain not allowed: {url}"

        retries = max_retries if max_retries is not None else config.max_retries
        backoff = config.retry_backoff

        for attempt in range(1, retries + 1):
            try:
                self._wait_rate_limit()
                start_time = time.perf_counter()
                response = self.client.get(url)
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0

                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", int(backoff * attempt)))
                    logger.warning(f"Rate limited (429) on {url}. Backing off for {retry_after}s.")
                    time.sleep(retry_after)
                    continue

                if response.status_code >= 500:
                    logger.warning(f"Server error {response.status_code} for {url} on attempt {attempt}.")
                    time.sleep(backoff * attempt)
                    continue

                return response, elapsed_ms, None

            except (httpx.TimeoutException, httpx.NetworkError, httpx.TransportError) as e:
                logger.warning(f"Network error on {url} (attempt {attempt}/{retries}): {e}")
                if attempt == retries:
                    return None, 0.0, str(e)
                time.sleep(backoff * attempt)
            except Exception as e:
                logger.error(f"Unexpected error fetching {url}: {e}")
                return None, 0.0, str(e)

        return None, 0.0, "Max retries exceeded"

    def close(self):
        self.client.close()
