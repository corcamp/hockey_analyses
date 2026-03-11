import requests

class APIClient:
    """
    A reusable class to interact with REST APIs.
    """

    def __init__(self, base_url, headers=None, auth=None):
        """
        Initialize the API client.

        :param base_url: Base URL of the API
        :param headers: Optional dictionary of headers
        :param auth: Optional authentication tuple (username, password) or requests Auth object
        """
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self.auth = auth

    def get(self, endpoint, params=None):
        """
        Perform a GET request.

        :param endpoint: API endpoint (appended to base_url)
        :param params: Optional query parameters as a dictionary
        :return: JSON response or raises an exception if request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, headers=self.headers, params=params, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None, json=None):
        """
        Perform a POST request.

        :param endpoint: API endpoint
        :param data: Dictionary of form data
        :param json: Dictionary of JSON payload
        :return: JSON response
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.post(url, headers=self.headers, data=data, json=json, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def extract_data(self, endpoint, params=None, key=None):
        """
        Extract specific data from the API response.

        :param endpoint: API endpoint
        :param params: Optional query parameters
        :param key: Key to extract from the JSON response (nested keys supported with dot notation)
        :return: Extracted data or full JSON if key is None
        """
        data = self.get(endpoint, params=params)
        if key:
            for k in key.split('.'):
                data = data.get(k, {})
        return data


from pathlib import Path
import pandas as pd

# Example usage:
if __name__ == "__main__":
    api = APIClient("https://api-web.nhle.com/v1") # , headers={"Authorization": "Bearer YOUR_TOKEN"}
    
    # Fetch raw JSON
    #raw_data = api.get("standings/now")
    #print(raw_data)
    
    # Player Data
    #playerisActive = api.extract_data("player/8478402/landing") # key="isActive"

    # Team Data
    #playerisActive = api.extract_data("standings/now") # key="isActive" 

    #api.extract_data("player/8478402/game-log/20252026/2", key="")


    resapi = APIClient("https://api.nhle.com/stats/rest") 

    resapi.extract_data("en/players?limit=3&sort=lastName&dir=asc&cayenneExp=currentTeamId=7", key="")

    # Get team by id 
    resapi.extract_data("en/team/id/10", key="")

    # Get game information 
    resapi.extract_data("en/game", key="")

    # Get game information 
    resapi.extract_data("en/game/meta", key="")

    # Shift charts ( Function of Game ID )
    resapi.extract_data("en/shiftcharts?cayenneExp=gameId=2021020001", key="")


    tempo =0 


