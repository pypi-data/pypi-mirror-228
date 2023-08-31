import requests, os

class About_API:
    """
    A class to interact with a prediction API.

    Attributes:
        url (str): The URL of the prediction API.

    Methods:
        predict_item(self, item_names):
            Send a POST request to the prediction API and get predictions for given item names.
    """

    def __init__(self, url = None):
        """
        Initialize the About_API class.

        Args:
            url (str): The URL of the prediction API.
              By default, the url will be obtained from the environment variable 'api_url_item_classification'.
              
        """
        self.url = url or os.getenv("api_url_item_classification")

    def predict_item(self, item_names):
        """
        Predict items using the prediction API.

        Args:
            item_names (list): A list of item names to be predicted.

        Returns:
            dict: A dictionary containing predictions for the given item names.
        """
        if type(item_names) != list:
            raise ValueError("Item Names must be of list type")
            
        data = {"item_names": item_names}
        response = requests.post(self.url, json=data)
        predictions = response.json()
        return predictions

