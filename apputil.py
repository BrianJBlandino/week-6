import pandas as pd
import os
import requests
from dotenv import load_dotenv
load_dotenv("env-1.env")

class Genius:
    """A class to interact with the Genius API."""
    
    def __init__(self):
        """Initialize the Genius object and save the
        access token from the .env file as an attribute."""
        
        # Retrieve the access token from the environment variables
        self.access_token = os.getenv("ACCESS_TOKEN")

        # Handle the case where the ACCESS_TOKEN is not set
        if not self.access_token:
            raise ValueError("ACCESS_TOKEN is missing in the .env file.")
    
    def get_artist(self, search_term):
        """Search for an artist by name and return detailed
        information about the artist.

        Parameters:
        search_term (str): The name of the artist to search for.

        Returns:
        dict: A dictionary containing the artist's information.
        """
        base_url = "http://api.genius.com/search"
        
        # Send a GET request to search for the artist
        response = requests.get(
            base_url,
            params={"q": search_term},
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        
        # Raise an error if the request was unsuccessful
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")
        
        # Parse the JSON response
        search_results = response.json()

        # Extract the artist ID from the first "hit"
        try:
            artist_id = search_results["response"]["hits"][0]["result"]["primary_artist"]["id"]
            artist_api_path = search_results["response"]["hits"][0]["result"]["primary_artist"]["api_path"]
        except (KeyError, IndexError):
            raise Exception("No artist found for the given search term.")

        # Use the artist API path to fetch detailed artist information
        artist_url = f"http://api.genius.com{artist_api_path}"
        artist_response = requests.get(
            artist_url,
            headers={"Authorization": f"Bearer {self.access_token}"}
        )

        # Raise an error if the request was unsuccessful
        if artist_response.status_code != 200:
            raise Exception(f"Failed to fetch artist data: {artist_response.status_code} - {artist_response.text}")
        
        # Return the artist's information as a dictionary
        return artist_response.json()

    def get_artists(self, search_terms):
        """
        Search for multiple artists and return a DataFrame containing relevant information.

        Parameters:
        search_terms (list): A list of artist names to search for.

        Returns:
        pd.DataFrame: A DataFrame with information about each artist.
        """
        # Initialize an empty list to store artist data
        artist_data = []

        # Iterate through the list of search terms
        for term in search_terms:
            try:
                # Get artist information using get_artist method
                artist_info = self.get_artist(term)
                artist = artist_info["response"]["artist"]

                # Extract relevant fields
                artist_data.append({
                    "search_term": term,
                    "artist_name": artist.get("name"),
                    "artist_id": artist.get("id"),
                    "followers_count": artist.get("followers_count", None)
                })
            except Exception as e:
                # Handle errors for individual search terms and log them
                print(f"Error fetching data for '{term}': {e}")
                artist_data.append({
                    "search_term": term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })

        # Convert the list of artist data into a DataFrame
        return pd.DataFrame(artist_data)

