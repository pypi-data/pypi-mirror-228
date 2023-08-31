import json
from dotenv import load_dotenv
import openai
import os
from logging_llm import LLMLogger  # Ensure this module is correctly located


# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
# Create an instance of the LLMLogger
llm_logger = LLMLogger(project_name='test_4', model='gpt-3.5-turbo', open_ai_key=openai.api_key, is_auto_failure=True, is_categorization=True)

# Open the 'data.json' file and load the content
with open("data/data.json", "r") as file:
    data = json.load(file)

# Iterate through each data element
for elem in data:
    # Extract the relevant details from each data element
    retrieved_content = elem['retrieved_content']
    question = elem['question']
    answer = elem['answer']
    label = elem['label']

    # Print the extracted details for visualization
    print(retrieved_content)
    print(question)
    print(answer)

   
    # Log the data using the created logger
    llm_logger.log(input_llm=question, retrieved_content=retrieved_content, output_llm=answer, label=label, user_id='', session_id='')
