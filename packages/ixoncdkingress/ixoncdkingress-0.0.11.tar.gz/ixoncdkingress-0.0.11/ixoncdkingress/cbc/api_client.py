"""
Contains code dealing with API clients
"""
from typing import Any, Dict, List, MutableMapping, Optional, Union

import json

import requests

Query = MutableMapping[str, Union[None, str, List[str]]]

ClientRequest = Union[Dict[str, Any], List[Dict[str, Any]], bytes]

ServerResponse = Dict[str, Any]

class ApiClient:
    """
    class for a API client
    """

    _base_url: str
    """
    The base URL (entry point) of the API server
    """

    _default_headers: Dict[str, str]
    """
    The headers to send along with every request
    """

    _session: requests.Session
    """
    Requests session to run requests with
    """

    _discovery: Optional[Dict[str, str]]
    """
    Discovery dictionary
    """

    def __init__(
        self,
        base_url: str,
        api_application: Optional[str] = None,
        api_company: Optional[str] = None,
        authorization: Optional[str] = None,
    ) -> None:
        self._base_url = base_url

        self._default_headers = {
            'Api-Version': '2',
        }

        if api_application:
            self._default_headers['Api-Application'] = api_application
        if api_company:
            self._default_headers['Api-Company'] = api_company
        if authorization:
            self._default_headers['Authorization'] = authorization

        self._session = requests.session()

        self._discovery = None

    def _check_discovery(self, verify: bool = True) -> None:
        """
        Checks whether discovery has been run, and, if not, runs it.

        Set verify on True when the certificate shouldn't be checked, which is the case when
        the ApiClient has to talk to the envdev ixapi-server.

        We don't expire the discovery as a new ApiClient instance is
        created for every Backend Component call.
        """
        if self._discovery is not None:
            return

        discovery_headers =  {'Api-Version': self._default_headers['Api-Version']}
        response = self._session.get(self._base_url, headers=discovery_headers, verify=verify)
        assert response.ok, 'Api discovery failed'
        data = response.json()
        assert 'Discovery' == data['type']
        self._discovery = {
            discovery['rel']: discovery['href']
            for discovery in data['data']
        }

    def set_custom_api_application(self, api_application: str) -> None:
        """
        Modifies the Api-Application header used for API server requests.
        """
        self._default_headers['Api-Application'] = api_application

    def get(
            self,
            url_name: str,
            url_args: Optional[Dict[str, str]] = None,
            query: Optional[Query] = None,
            headers: Optional[Dict[str, str]] = None,
            **kwargs: Any
        ) -> ServerResponse:
        """
        Performs a GET request on the API server, on the URL with the given
        name

        The URL names are found in the discovery
        """
        return self._request(
            'GET', url_name, url_args=url_args, query=query, headers=headers, **kwargs
        )

    def patch(
            self,
            url_name: str,
            data: ClientRequest,
            url_args: Optional[Dict[str, str]] = None,
            query: Optional[Query] = None,
            headers: Optional[Dict[str, str]] = None,
            **kwargs: Any
        ) -> ServerResponse:
        """
        Performs a PATCH request on the API server, on the URL with the given
        name

        The URL names are found in the discovery
        """
        return self._request(
            'PATCH', url_name, url_args=url_args, query=query, data=data, headers=headers, **kwargs
        )

    def post(
            self,
            url_name: str,
            data: ClientRequest,
            url_args: Optional[Dict[str, str]] = None,
            query: Optional[Query] = None,
            headers: Optional[Dict[str, str]] = None,
            **kwargs: Any
        ) -> ServerResponse:
        """
        Performs a POST request on the API server, on the URL with the given
        name

        The URL names are found in the discovery
        """
        return self._request(
            'POST', url_name, url_args=url_args, query=query, data=data, headers=headers, **kwargs
        )

    def options(
            self,
            url_name: str,
            url_args: Optional[Dict[str, str]] = None,
            headers: Optional[Dict[str, str]] = None,
            **kwargs: Any
        ) -> ServerResponse:
        """
        Performs an OPTIONS request on the API server, on the URL with the given
        name

        The URL names are found in the discovery

        When using a browser, these are done automatically. When not using a browser,
        these are not required
        """
        return self._request(
            'OPTIONS', url_name, url_args=url_args, headers=headers, **kwargs
        )

    def put(
            self,
            url_name: str,
            url_args: Optional[Dict[str, str]] = None,
            data: Optional[ClientRequest] = None,
            headers: Optional[Dict[str, str]] = None,
            **kwargs: Any
        ) -> Dict[str, Any]:
        """
        Performs a PUT request on the API server, on the URL with the given
        name

        The URL names are found in the discovery
        """
        return self._request(
            'PUT', url_name, url_args=url_args, data=data, headers=headers, **kwargs
        )

    def delete(
            self,
            url_name: str,
            url_args: Optional[Dict[str, str]] = None,
            data: Optional[ClientRequest] = None,
            query: Optional[Query] = None,
            headers: Optional[Dict[str, str]] = None,
            **kwargs: Any
        ) -> ServerResponse:
        """
        Performs a DELETE request on the API server, on the URL with the given
        name

        The URL names are found in the discovery
        """
        return self._request(
            'DELETE', url_name, url_args=url_args, query=query, data=data, headers=headers,
            **kwargs
        )

    def _request(
            self,
            method: str,
            url_name: str,
            url_args: Optional[Dict[str, str]] = None,
            headers: Optional[Dict[str, str]] = None,
            query: Optional[Query] = None,
            data: Optional[ClientRequest] = None,
            **kwargs: Any,
        ) -> ServerResponse:
        """
        Sends a request to the API server
        """
        if url_args is None:
            url_args = {}

        url = self._get_url(url_name, url_args, kwargs.get('verify', True))

        if headers is None:
            headers = {}

        data_json: Optional[bytes]
        if data is None or isinstance(data, bytes):
            data_json = data
        else:
            data_json = json.dumps(data).encode('UTF-8')

        response = self._session.request(
            method, url,
            params=query,
            headers={
                **self._default_headers,
                **headers,
            },
            data=data_json,
            **kwargs,
        )
        try:
            return response.json() # type: ignore
        except json.decoder.JSONDecodeError:
            return {
                'type': 'Error',
                'data': [
                    {
                        'message': response.text,
                    }
                ],
                'status': 'error'
            }

    def _get_url(self, url_name: str, url_args: Dict[str, str], verify: bool = True) -> str:
        """
        Returns an URL by name from the discovery and apply the URL arguments
        """
        self._check_discovery(verify=verify)
        assert self._discovery is not None # type hint

        return self._discovery[url_name].format(**url_args)

    def __repr__(self) -> str:
        return (
            '<ApiClient'
            f' base_url={self._base_url},'
            f' default_headers={self._default_headers},'
            '>'
        )
