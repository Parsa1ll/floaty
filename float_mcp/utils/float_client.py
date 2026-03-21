import asyncio
import logging
import time
from typing import Optional

import httpx

from float_mcp.config import FLOAT_API_KEY, FLOAT_BASE_URL

logger = logging.getLogger("float_mcp.client")


class FloatClient:
    """Async HTTP client for Float API with retry logic, rate-limit handling, and structured logging."""

    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {FLOAT_API_KEY}",
            "Content-Type": "application/json",
        }

    async def _ensure_client(self) -> httpx.AsyncClient:
        """Lazily initialize and return the HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=f"{FLOAT_BASE_URL}/v1",
                headers=self._get_headers(),
                timeout=30.0,
            )
        return self._client

    async def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """
        Execute an HTTP request with retry logic, rate-limit handling, and logging.
        Always returns a dict. On error, returns {"error": "message"}.
        """
        client = await self._ensure_client()
        for attempt in range(3):
            start = time.monotonic()
            try:
                resp = await client.request(method, endpoint, **kwargs)
                latency_ms = int((time.monotonic() - start) * 1000)

                # Log structured info
                logger.info(
                    f"endpoint={endpoint} method={method} status={resp.status_code} latency_ms={latency_ms}"
                )

                # Handle rate limit
                if resp.status_code == 429:
                    wait_seconds = float(resp.headers.get("Retry-After", "1"))
                    logger.warning(
                        f"Rate limited (429). Waiting {wait_seconds}s before retry."
                    )
                    await asyncio.sleep(wait_seconds)
                    continue

                # Retry on server errors
                if resp.status_code >= 500 and attempt < 2:
                    logger.warning(
                        f"Server error {resp.status_code}. Retrying (attempt {attempt + 1}/3)"
                    )
                    await asyncio.sleep(2 ** attempt)
                    continue

                # Raise for other HTTP errors
                resp.raise_for_status()
                return resp.json()

            except httpx.HTTPStatusError as e:
                error_text = e.response.text[:200]  # Limit error message length
                return {"error": f"HTTP {e.response.status_code}: {error_text}"}
            except httpx.TimeoutException:
                if attempt == 2:
                    return {"error": "Request timeout after 3 attempts"}
                logger.warning(f"Timeout. Retrying (attempt {attempt + 1}/3)")
                await asyncio.sleep(2 ** attempt)
            except httpx.ConnectError as e:
                if attempt == 2:
                    return {"error": f"Connection error: {str(e)}"}
                logger.warning(f"Connection error. Retrying (attempt {attempt + 1}/3)")
                await asyncio.sleep(2 ** attempt)
            except Exception as e:
                if attempt == 2:
                    return {"error": str(e)}
                logger.warning(f"Request failed: {str(e)}. Retrying (attempt {attempt + 1}/3)")
                await asyncio.sleep(2 ** attempt)

        return {"error": "Max retries exceeded"}

    async def get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """GET request."""
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint: str, data: Optional[dict] = None) -> dict:
        """POST request."""
        return await self._request("POST", endpoint, json=data)

    async def patch(self, endpoint: str, data: Optional[dict] = None) -> dict:
        """PATCH request."""
        return await self._request("PATCH", endpoint, json=data)

    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()


# Module-level singleton
float_client = FloatClient()
