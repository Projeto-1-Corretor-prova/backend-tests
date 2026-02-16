import requests
from config.settings import API_BASE_URL, API_TIMEOUT, DEFAULT_HEADERS
from typing import Optional, Dict, Any


class APIClient:
    """Cliente HTTP para testes de API"""

    def __init__(
        self,
        base_url: str = API_BASE_URL,
        timeout: int = API_TIMEOUT,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.headers = {**DEFAULT_HEADERS, **(headers or {})}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _build_url(self, endpoint: str) -> str:
        """Constrói a URL completa"""
        if endpoint.startswith("http"):
            return endpoint
        return f"{self.base_url}{endpoint}"

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """GET request"""
        url = self._build_url(endpoint)
        return self.session.get(url, params=params, timeout=self.timeout, **kwargs)

    def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[str] = None,
        **kwargs
    ) -> requests.Response:
        """POST request"""
        url = self._build_url(endpoint)
        return self.session.post(
            url, json=json, data=data, timeout=self.timeout, **kwargs
        )

    def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """PUT request"""
        url = self._build_url(endpoint)
        return self.session.put(url, json=json, timeout=self.timeout, **kwargs)

    def patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """PATCH request"""
        url = self._build_url(endpoint)
        return self.session.patch(url, json=json, timeout=self.timeout, **kwargs)

    def delete(
        self,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """DELETE request"""
        url = self._build_url(endpoint)
        return self.session.delete(url, timeout=self.timeout, **kwargs)

    def close(self):
        """Fecha a sessão"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
