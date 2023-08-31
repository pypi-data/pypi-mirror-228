## Overview
OdysseusAI is an open-source library is designed to facilitate the logging of input and output interactions with the LLMs in production locally. It keeps track of each interaction, saving them in a structured JSON format. The library focuses on modularity, ease of use, and robust data tracking.


## Installation

To install, simply download the library and include it in your project.

```bash
pip install odysseusai
```

## Usage

```python
import odysseusai
odysseusai.log(project_name, input_llm, output_llm, tracking_dir='', user_id='', session_id='')
```

## License

[MIT](https://choosealicense.com/licenses/mit/)