class Genius:
    """
    A class to interact with the Genius API.
    """
    def __init__(self):
        """
        Initialize the Genius object and save the access token from the .env file as an attribute.
        """
        # Retrieve the access token from the environment variables
        self.access_token = os.getenv("ACCESS_TOKEN")

        # Handle the case where the ACCESS_TOKEN is not set
        if not self.access_token:
            raise ValueError("ACCESS_TOKEN is missing in the .env file.")
