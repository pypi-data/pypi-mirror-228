import openai
import time

class OpenAICompletion:
    """
    A class to interact with OpenAI's ChatCompletion API.
    
    Attributes:
    - model (str): The model to use for completions, default is "gpt-3.5-turbo".
    - open_ai_key (str): The API key for OpenAI.
    - temperature (float): OpenAI temperature setting.
    - max_tokens (int): OpenAI maximum number of tokens setting.
    """

    def __init__(self, model="gpt-3.5-turbo", open_ai_key='', temperature=0, max_tokens=2000):
        """
        Initializes the OpenAICompletion with the provided settings.
        """
        # Setting instance attributes based on provided parameters or defaults
        self.model = model
        self.open_ai_key = open_ai_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Setting the API key for OpenAI based on provided key
        openai.api_key = self.open_ai_key

    def get_completion_from_messages(self, messages):
        """
        Fetches a completion response from OpenAI's ChatCompletion API based on the provided messages.
        """
        try:
            # Attempting to fetch a response from OpenAI
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
        except openai.error.RateLimitError:
            # In case of a rate limit error, wait for 5 seconds and retry
            time.sleep(5)
            return self.get_completion_from_messages(messages)
        
        # Returning the content of the first choice from the model's response
        return response.choices[0].message["content"]
