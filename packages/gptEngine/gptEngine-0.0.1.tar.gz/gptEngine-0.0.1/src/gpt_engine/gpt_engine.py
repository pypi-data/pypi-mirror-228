import openai
from . import config
from docx import Document

class GPTEngineModel:

    def __init__(self, main_task, input_prompt):
        self.openai = openai
        self.params = config.config()
        self.main_task = main_task
        self.input_prompt = input_prompt
        self.api_key = self.params['openai_api_key']

    def _setup_openai(self):
        self.openai.api_key = self.params['openai_api_key']

    def _get_context(self):
        """
        Get the context for the current task.

        Args:
            self: The current object.

        Returns:
            The context string.

        Raises:
            NotImplementedError: If the main task or input prompt is not created.
        """

        if self.main_task is None:
            raise NotImplementedError("Main task is not created")
        if self.input_prompt is None:
            raise NotImplementedError("Input Prompt is not created")
        context = f"{self.main_task} {self.input_prompt}"
        return context

    def _get_file(self, file_path: str):
        """
        Read the .doc file and return the text content.

        Args:
            file_path: The path to the .doc file.

        Returns:
            The text content of the file.
        """

        document = Document(file_path)
        content = ""
        for paragraph in document.paragraphs:
            content += paragraph.text
        return content

    def _batch_process(self, file_path: str):
        """
        Batch process the instructions and input prompt.

        Args:
            file_path: The path to the .doc file.

        Returns:
            A list of messages to be processed by OpenAI.
        """

        content = self._get_file(file_path)
        messages = []
        for i in range(0, len(content), 500):
            batch_content = content[i:i + 500]
            instruction = f"{self._get_context()}: \n" + batch_content
            messages.append({"role": "system", "content": "You are a intelligent assistant." })
            messages.append({"role": "user", "content": instruction})
        return messages

    def generate_response(self, file_path: str):
        """
        Generate a response from OpenAI.

        Args:
            file_path: The path to the .doc file.

        Returns:
            The response from OpenAI.
        """

        messages = self._batch_process(file_path)
        self._setup_openai()
        response = ""
        for message in messages:
            chat = self.openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[message])
            response += chat.choices[0].message.content
        return response