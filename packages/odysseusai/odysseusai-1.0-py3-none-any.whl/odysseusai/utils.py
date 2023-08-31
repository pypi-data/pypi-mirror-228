import json

class StringUtils:
    @staticmethod
    def switch_yes_no(text: str) -> str:
        """
        Switches 'Yes' to 'No' and vice versa. If the input is neither, it returns the original text.
        """
        if text == "Yes":
            return "No"
        elif text == "No":
            return "Yes"
        return text

class JSONUtils:
    @staticmethod
    def extract_json(data_string: str) -> str:
        """
        Extracts a JSON string from a larger string. 
        Assumes the JSON content starts with '{' and continues to the end of the input string.
        """
        start_index = data_string.index("{")
        json_string = data_string[start_index:]
        return json_string
    
    @staticmethod
    def load_json_from_text(text):
        """
        Extracts and loads a JSON string from a given text.
        """
        return json.loads(text)


