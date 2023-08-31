import os
import json
from datetime import datetime
import uuid
from utils import StringUtils, JSONUtils
from evaluation import FailureClassifier, FailureEvaluator


class LLMLogger:
    def __init__(self, project_name, model, open_ai_key, tracking_dir='', is_auto_failure = True, is_categorization = False, categories = None):
        """
        Initializes the LLMLogger instance.

        Args:
            project_name (str): Name of the project.
            model (str): OpenAI's GPT model name.
            open_ai_key (str): OpenAI API key.
            categories (list): Categories of failure types.
            is_auto_failure (bool): Enable auto-detect failures.
            is_categorization (bool): Enable to enable/disable categorization.
            tracking_dir (str): Directory path for logging.
        """
        self.project_name = project_name
        self.model = model
        self.tracking_dir = tracking_dir
        self.open_ai_key = open_ai_key
        self.is_auto_failure = is_auto_failure
        self.is_categorization = is_categorization
        if(is_auto_failure):
            self.failure_evaluator = FailureEvaluator (model=self.model, open_ai_key= self.open_ai_key)
        if(is_categorization):
            self.failure_classifier = FailureClassifier(model=self.model, open_ai_key=self.open_ai_key, categories=categories)
        self._init_env()

    def _init_env(self):
        """Initializes the environment for logging."""
        tracking_dest = f'{self.tracking_dir}logs'
        if not os.path.exists(tracking_dest):
            os.makedirs(tracking_dest)
        project_dir = f'{self.tracking_dir}logs/{self.project_name}'
        if not os.path.exists(project_dir):
            self._create_env(project_dir)

    def _create_env(self, project_dir):
        """
        Creates the environment for the given project directory.

        Args:
            project_dir (str): Directory path for the project.
        """
        os.makedirs(project_dir)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
        env_info_dir = f'{project_dir}/env_info.json'
        with open(env_info_dir, 'w') as f:
            json.dump({
                'model': self.model,
                'timestamp': str(current_time),
                'is_auto_failure':str(self.is_auto_failure),
                'is_categorization':str(self.is_categorization)
            }, f, indent=4)

    def log(self, input_llm, retrieved_content, output_llm, label = None, user_id=None, session_id=None):
        """
        Logs interactions with the LLM (Language Learning Model).

        Args:
            input_llm (str): Input string to the LLM.
            retrieved_content (str): Retrieved content string from the LLM.
            output_llm (str): Output response from the LLM.
            user_id (str): Identifier for the user.
            session_id (str): Identifier for the session.
            label (str): Label string.
        """
        unique_str = str(uuid.uuid4())
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
        
        # Auto-detect failures
        if self.is_auto_failure:
            response_failure = self.failure_evaluator.evaluate(question=input_llm, content=retrieved_content, answer=output_llm)
            is_failure_case, explanation_failure_case = self.failure_evaluator.parse_response(response_failure)

            # Categorize failures, if needed
            if (is_failure_case == 'Yes') and self.is_categorization:
                response_classify = self.failure_classifier.classify_failure(explanation=explanation_failure_case)
                category_classification, explanation_classification = self.failure_classifier.parse_response(response_classify)
            else:
                category_classification = 'correct'
                explanation_classification = ''
        else:
            is_failure_case = ''
            explanation_failure_case = ''
            category_classification = ''
            explanation_classification = ''

        # Write the interaction and results to a JSON file
        project_dir = f'{self.tracking_dir}logs/{self.project_name}/{unique_str}.json'
        with open(project_dir, 'w') as f:
            json.dump({
                'user_id': user_id,
                'session_id': session_id,
                'timestamp': str(current_time),
                'input_llm': input_llm,
                'retrieved_content': retrieved_content,
                'output_llm': output_llm,
                'is_failure_case': is_failure_case,
                'explanation_failure_case': explanation_failure_case,
                'category': category_classification,
                'explanation_category': explanation_classification,
                'label': label
            }, f, indent=4)
