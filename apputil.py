class Genius:
    """
    A class to interact with the Genius API.
    """
    def __init__(self, access_token):
        """
        Initialize the Genius object and save the access token as an attribute.
        
        Parameters:
        access_token (str): The API access token.
        """
        self.access_token = access_token