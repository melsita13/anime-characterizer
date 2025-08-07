import requests
import streamlit as st

ANILIST_URL = "https://graphql.anilist.co"
JIKAN_URL = "https://api.jikan.moe/v4"


def make_api_request(url, method="get", json_data=None, params=None):
    """
    Makes an API request to the given URL with the specified method and parameters.
    Returns the JSON response if successful, or None if an error occurs.
    :param url: The API endpoint URL.
    :param method: HTTP method (GET or POST).
    :param json_data: JSON data for POST requests.
    :param params: Query parameters for GET requests.
    :return: JSON response if successful, or None if an error occurs.
    """
    try:
        if method == "get":
            response = requests.get(url, params=params)
        elif method == "post":
            response = requests.post(url, json=json_data)
        else:
            raise ValueError("Unsupported HTTP method")

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(
            f"HTTP error: {http_err.response.status_code} - {http_err.response.reason}"
        )
        return {
            f"error": f"HTTP error: {http_err.response.status_code} - {http_err.response.reason}"
        }
    except requests.exceptions.ConnectionError:
        st.error("Connection Error: Could not connect to the API.")
        return {"error": "Failed to connect to the API."}
    except requests.exceptions.Timeout:
        st.error("Timeout Error: The API request timed out.")
        return {"error": "API request timed out."}
    except requests.exceptions.RequestException as err:
        st.error(f"An unexpected error occurred during the API request: {err}")
        return {"error": f"An unknown error occurred."}
