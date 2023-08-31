from llms import OpenAICompletion
from utils import StringUtils, JSONUtils

class FailureEvaluator:
    """
    Evaluator for assessing the accuracy of chatbot interactions. Determines whether the chatbot's answer was correct based on the given content and user's question.

    Attributes:
        model (str): OpenAI's GPT model name.
        open_ai_key (str): API key for OpenAI.
    """
    
    # Pre-defined prompts for OpenAI's GPT model
    SYSTEM_MESSAGE = """ 
        You are an expert at evaluating whether a chatbot provided the correct answer to a user's question based solely on given content.
    """
    USER_MESSAGE_TEMPLATE = """
        Let's think step by step.
        1. Consider the following: 
        User's question: {}.
        Content: {}.
        Chatbot's answer: {}.
        2. Determine if the chatbot's answer successfully addresses the user's question based solely on the given content.
        3. Provide a brief explanation, termed 'explanation', for the evaluation, leading up to a verdict (Yes/No) labeled as 'verdict'.
        4. Return a JSON object in the following format: ["verdict": 'verdict', "explanation": 'explanation'].
    """

    def __init__(self, model, open_ai_key):
        """
        Initializes the FailureEvaluator with the specified model and OpenAI key.

        Args:
            model (str): OpenAI's GPT model name.
            open_ai_key (str): API key for OpenAI.
        """
        
        self.model = model
        self.open_ai_key = open_ai_key
        
        # Create an OpenAI completion instance for interactions with OpenAI's API
        self.completion = OpenAICompletion(model=self.model, open_ai_key=self.open_ai_key)

    def evaluate(self, question, content, answer):
        """
        Evaluate whether the chatbot's answer aligns with the content in reference to the question.
        Args:
            question (str): User's query to the chatbot.
            content (str): Content base used by the chatbot to generate the answer.
            answer (str): Chatbot's generated response to the user's question.

        Returns:
            str: OpenAI's evaluation response.
        """
        
        # Format user and system messages using the provided question, content, and answer
        user_message = self.USER_MESSAGE_TEMPLATE.format(question, content, answer)
        system_message = self.SYSTEM_MESSAGE
        message = [{'role': 'system', 'content': system_message}, {'role': 'user', 'content': user_message}]
        
        # Get response from OpenAI's ChatCompletion API
        openai_response = self.completion.get_completion_from_messages(message)
        
        # Print and return the response
        print(openai_response)
        return openai_response
    
    @staticmethod
    def _extract_json_from_response(response):
        response_json_format = JSONUtils.extract_json(response)
        response_json = JSONUtils.load_json_from_text(response_json_format)
        return(response_json)

    def parse_response(self, response):
        response_json = self._extract_json_from_response(response)
        is_failure_case = StringUtils.switch_yes_no(response_json['verdict'])
        explanation_failure_case = response_json['explanation']
        return is_failure_case, explanation_failure_case
    

   
    


class FailureClassifier:
    """
    Classifier for evaluating the failure case.

    Uses OpenAI's GPT model to determine the type of failure based on given explanations.

    Attributes:
        model (str): OpenAI's GPT model name.
        open_ai_key (str): API key for OpenAI.
        categories (list): Categories of failure types.
    """
    
    DEFAULT_CATEGORIES = ['Content irrelevant to question', 'Content irrelevant to answer', 'Answer irrelevant to question']
    SYSTEM_MESSAGE = """ 
        You are an expert at classifying detected failure cases based on an explanation.
    """
    USER_MESSAGE_TEMPLATE = """
        Let's think step by step.
        1. Consider the following: 
        Explanation: {}.
        Categories: {}.
        2. Classify the explanation into one of the provided categories.
        3. Provide a brief explanation, termed 'explanation', for the evaluation, leading up to a category labeled as 'category'.
        4. Return a JSON object in the following format: ["category": 'category', "explanation": 'explanation']. 
    """

    def __init__(self, model, open_ai_key, categories=None):
        """
        Initializes the FailureClassifier with the specified model, OpenAI key, and categories.

        Args:
            model (str): OpenAI's GPT model name.
            open_ai_key (str): API key for OpenAI.
            categories (list, optional): Custom list of failure categories. Defaults to None, which will then use DEFAULT_CATEGORIES.
        """
        
        self.model = model
        self.open_ai_key = open_ai_key
        self.completion = OpenAICompletion(model=self.model, open_ai_key=self.open_ai_key)
        
        # Use provided categories or fall back to default ones
        self.categories = categories if categories is not None else self.DEFAULT_CATEGORIES

    def classify_failure(self, explanation):
        """
        Classify the given explanation into one of the failure categories.

        Args:
            explanation (str): Explanation of the chatbot's response.

        Returns:
            str: OpenAI's classification response.
        """
        
        user_message = self.USER_MESSAGE_TEMPLATE.format(explanation, self.categories)
        system_message = self.SYSTEM_MESSAGE
        message = [{'role': 'system', 'content': system_message}, {'role': 'user', 'content': user_message}]
        
        # Get response from OpenAI's ChatCompletion API
        openai_response = self.completion.get_completion_from_messages(message)
        
        # Print and return the response
        print(openai_response)
        return openai_response

    @staticmethod
    def _extract_json_from_response(response):
        response_json_format = JSONUtils.extract_json(response)
        response_json = JSONUtils.load_json_from_text(response_json_format)
        return(response_json)

    def parse_response(self, response):
        response_json = self._extract_json_from_response(response)
        category_classification = response_json['category']
        explanation_classification = response_json['explanation']
        return category_classification, explanation_classification

