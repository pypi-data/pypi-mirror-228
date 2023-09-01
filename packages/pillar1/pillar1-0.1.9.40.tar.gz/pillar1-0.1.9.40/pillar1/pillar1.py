import json
import boto3
import datetime
from pyspark.sql import SparkSession
import pillar1.constants as cn
import requests
import ipywidgets as widgets
from IPython.display import display
import vertexai
from vertexai.preview.language_models import CodeGenerationModel
import openai

import re


def extract_sql(text):
    # pattern for SQL statement
    pattern = r"(SELECT.*?;)"

    # search for the pattern
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

    # if a match is found, return it
    if match:
        return match.group(1).strip()
    else:
        return "No valid response returned by LLM"


class MODELS:
    STARCODERPLUS = 'starcoderplus'
    STARCHAT_BETA = 'starchat-beta'
    FALCON_40B_INSTRUCT = 'f40b-instruct'
    FALCON_40B = 'f40b'
    CODEY = 'gcp-codey'
    GPT35 = 'gpt3-5'
    GPT4 = 'gpt4'


MODELS_META = {
    'gpt3-5': {

    },
    'gpt4': {

    },
    'gcp-codey': {

    },
    'f40b-instruct': {
        'stop_token': '<|endoftext|>'
    },
    'f40b': {
        'free': {
            'prepend': 'Given this `claims` table description:',
            'stop_token': '<|endoftext|>'
        },
        'hosted': {
            'prepend': 'Given this `claims` table description:',
            'stop_token': '<|endoftext|>'
        }
    },
    'starcoderplus': {
        'free': {
            'prepend': 'Given this `claims` table description:',
            'append': '',
            'stop_token': '<|end|>',
            'API_URL': 'https://api-inference.huggingface.co/models/bigcode/starcoderplus',
            'placeholder_beg': {'pattern': '```sql', 'index': 1},
            'placeholder_end': {'pattern': '```', 'index': 0}
        },
        'hosted': {
            'prepend': 'Given this `claims` table description:',
            'append': '',
            'stop_token': '<|end|>',
            'placeholder_beg': {'pattern': '```sql', 'index': 1},
            'placeholder_end': {'pattern': '```', 'index': 0}
        },
        'hosted-hf': {
            'prepend': 'Given this `claims` table description:',
            'append': '',
            'stop_token': '<|end|>',
            'API_URL': 'https://sqs1psicnqzs3rr7.us-east-1.aws.endpoints.huggingface.cloud',
            'placeholder_beg': {'pattern': '```sql', 'index': 1},
            'placeholder_end': {'pattern': '```', 'index': 0}
        }
    },
    'starchat-beta': {
        'free': {
            'prepend': '<|user|>Given this `claims` table description:',
            'append': '<|end|>',
            'stop_token': '<|end|>',
            'API_URL': 'https://api-inference.huggingface.co/models/HuggingFaceH4/starchat-beta',
            'replaces': {'': '', }
        }
    }
}


class Model:
    def __init__(self, user_name: str = '', password: str = '', end_point_url='', end_point: str = '', max_new_tokens: int = 100, verbose: bool = False, api_type: str = 'free',
                 huggingface_token='', background: str = '', prepend: str = '', append: str = '', temperature: float = .1, do_sample: bool = True, top_k: int = 50,
                 top_p: float = .7, repetition_penalty: float = 1.03, openai_key: str = ''):
        self.append = append
        self.prepend = prepend
        self.repetition_penalty = repetition_penalty
        self.top_p = top_p
        self.top_k = top_k
        self.do_sample = do_sample
        self.temperature = temperature
        self.end_point = end_point
        self.prompt = None
        self.result = None
        self.huggingface_token = huggingface_token
        self.cleaned_code = ''
        self.response = None
        self.max_new_tokens = max_new_tokens
        self.verbose = verbose
        self.api_type = api_type
        self.full_prompt = ''
        self.end_point_url = end_point_url

        if not background:
            self.background = cn.BACKGROUND_SAMPLE
        else:
            self.background = background

        if self.api_type == 'hosted':
            self.client = boto3.client(
                'sagemaker-runtime',
                aws_access_key_id=user_name,
                aws_secret_access_key=password,
                region_name='us-west-2'
            )

        if self.end_point == MODELS.CODEY:
            vertexai.init(project="main-project-359406", location="us-central1")
            self.curr_model = CodeGenerationModel.from_pretrained("code-bison@001")
        elif self.end_point in (MODELS.GPT35, MODELS.GPT4):
            openai.api_key = openai_key
        else:
            self.curr_model = MODELS_META[end_point][api_type]

    def code(self):
        self.cleaned_code = self.response.replace(self.prompt, '').strip()
        placeholder_beg = self.curr_model.get('placeholder_beg')
        if placeholder_beg:
            try:
                self.cleaned_code = self.cleaned_code.split(placeholder_beg['pattern'])[placeholder_beg['index']]
            except Exception:
                pass

        placeholder_end = self.curr_model.get('placeholder_end')
        if placeholder_end:
            try:
                self.cleaned_code = self.cleaned_code.split(placeholder_end['pattern'])[placeholder_end['index']]
            except Exception:
                pass

        ELS_TO_REMOVE = ['<pre>', '<code>', '</code>', '</pre>']
        for curr_el_to_remove in ELS_TO_REMOVE:
            self.cleaned_code = self.cleaned_code.replace(curr_el_to_remove, '')

        self.cleaned_code = self.cleaned_code.strip()

    def query_list_ui(self, list_of_questions):
        dropdown = widgets.Dropdown(
            options=list_of_questions,
            value=list_of_questions[0],
            description='Question:',
            layout=widgets.Layout(width='80%'),
        )

        # Create the button widget
        button = widgets.Button(
            description='Submit Question',
            button_style='success',
            tooltip='Click to submit',
        )

        # Create the button widget
        button_execute = widgets.Button(
            description='Execute Query',
            button_style='success',
            tooltip='Click to submit',
        )

        # Create a Textarea widget
        textarea = widgets.Textarea(
            value='',
            placeholder='',
            description='Answer: ',
            layout=widgets.Layout(width='80%'),
        )

        html_widget = widgets.HTML(value='')

        # Function to handle button click event
        def on_button_clicked(b):
            textarea.value = 'Request submitted, please wait...'
            self.query(f'For the question: {dropdown.value.lower()}{self.append}')
            self.code()
            textarea.value = self.cleaned_code
            display(widgets.HBox([textarea, button_execute]))

        def show_html_res(b):
            html_widget.value = ''
            try:
                self.cleaned_code = textarea.value
                res = self.execute().toPandas().to_html()
                html_widget.value = res
            except Exception as e:
                html_widget.value = f"<h3>Error: {e}</h3>"

        button.on_click(on_button_clicked)
        button_execute.on_click(show_html_res)

        # Display the widgets
        display(widgets.HBox([dropdown, button]))
        display(widgets.HBox([textarea, button_execute]))
        display(widgets.HBox([html_widget]))

    def execute(self):
        spark = SparkSession.builder.getOrCreate()
        self.result = spark.sql(self.cleaned_code)
        return self.result

    def query(self, prompt: str = 'Find the ten first rows in the table', print_sql: bool = False, execute_code=False):
        def submit_request():
            start_time = datetime.datetime.now()

            if self.end_point == MODELS.GPT35:
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                        messages=[{"role": "user", "content": self.full_prompt}])
                self.response = response['choices'][0]['message']['content'].replace('```sql', '').replace('```', '').replace('SQL', '').strip()
                self.response = extract_sql(self.response)
                end_time = datetime.datetime.now()
                duration = end_time - start_time
                if self.verbose:
                    print(f"Took {duration.total_seconds():.2f} seconds to complete the operation.")

            elif self.end_point == MODELS.GPT4:
                response = openai.ChatCompletion.create(model="gpt-4",
                                                        messages=[{"role": "user", "content": self.full_prompt}])
                self.response = response['choices'][0]['message']['content'].replace('```sql', '').replace('```', '').replace('SQL', '').strip()
                self.response = extract_sql(self.response)
                end_time = datetime.datetime.now()
                duration = end_time - start_time
                if self.verbose:
                    print(f"Took {duration.total_seconds():.2f} seconds to complete the operation.")

            elif self.end_point == MODELS.CODEY:
                if self.verbose:
                    print(f"Input: {self.full_prompt}.\n\nTemperature: {self.temperature}.\nMax output tokens: {self.max_new_tokens}").strip()
                response = self.curr_model.predict(prefix=self.full_prompt,
                                                   temperature=self.temperature,
                                                   max_output_tokens=self.max_new_tokens)
                self.response = response.text.replace('```sql', '').replace('```', '').replace('SQL', '')
                self.response = extract_sql(self.response)

                end_time = datetime.datetime.now()
                duration = end_time - start_time

                if self.verbose:
                    print(f"Took {duration.total_seconds():.2f} seconds to complete the operation.")
            elif self.end_point == MODELS.STARCODERPLUS:
                payload = {
                    'inputs': self.full_prompt,
                    "parameters": {
                        "do_sample": self.do_sample,
                        "top_p": self.top_p,
                        "temperature": self.temperature,
                        "top_k": self.top_k,
                        "max_new_tokens": self.max_new_tokens,
                        "repetition_penalty": self.repetition_penalty,
                        "stop": [self.curr_model['stop_token']]
                    }
                }

                if self.verbose:
                    print(f"Submit payload: {payload}")

                if self.api_type == 'free':
                    headers = {
                        "Authorization": f"Bearer {self.huggingface_token}",
                        "Content-Type": "application/json",
                    }
                    response = requests.post(self.curr_model['API_URL'], headers=headers, json=payload)
                    self.response = response.json()[0]['generated_text'].split('```sql')[1].split('```')[0]
                    self.response = extract_sql(self.response)
                elif self.api_type == 'hosted':
                    response = self.client.invoke_endpoint(
                        EndpointName=self.end_point,
                        ContentType='application/json',
                        Body=json.dumps(payload)
                    )
                    self.response = json.loads(response['Body'].read())[0]['generated_text'].split('```sql')[1].split('```')[0]
                    self.response = extract_sql(self.response)
                elif self.api_type == 'hosted-hf':
                    headers = {
                        "Authorization": f"Bearer {self.huggingface_token}",
                        "Content-Type": "application/json",
                    }
                    # response = requests.post(self.curr_model['API_URL'], headers=headers, json=payload)
                    response = requests.post(self.end_point_url, headers=headers, json=payload)
                    self.response = response.json()[0]['generated_text'].split('```sql')[1].split('```')[0]
                    self.response = extract_sql(self.response)

            """
            curl https://sqs1psicnqzs3rr7.us-east-1.aws.endpoints.huggingface.cloud \
            -X POST \
            -d '{"inputs":"Gradient descent is"}' \
            -H "Authorization: Bearer <hf_token>" \
            -H "Content-Type: application/json"
            """
            if self.verbose:
                end_time = datetime.datetime.now()
                duration = end_time - start_time

                if self.verbose:
                    print(f"Took {duration.total_seconds():.2f} seconds to complete the operation.")

        if prompt:
            self.full_prompt = f'{self.background}{self.prepend}{prompt}{self.append}'
            submit_request()

            if print_sql:
                print(self.response)

            if execute_code:
                result = self.execute()
                return result

            return self.result
