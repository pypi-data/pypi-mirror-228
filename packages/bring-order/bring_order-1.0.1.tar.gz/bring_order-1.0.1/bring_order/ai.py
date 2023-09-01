"""AI assistant"""
from ipywidgets import widgets
from IPython.display import display, clear_output
import openai

class Ai:
    """AI assistant"""
    def __init__(self, bogui, utils, dataset_variables, ai_disabled, next_step):
        """Initializes AI-assistant class"""

        self.bogui = bogui
        self.utils = utils
        self.dataset_variables = dataset_variables
        self.ai_disabled = ai_disabled
        self.next_step = next_step
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.natural_language_prompt = self.bogui.create_text_area()
        self.api_key_input_field = self.bogui.create_password_field()
        self.api_key = None
        self.ai_response = ''
        self.ai_output_grid = widgets.AppLayout()
        self.ai_error_message_grid = self.bogui.create_message('')
        self.ai_error_msg = ''
        self.model_engine = "gpt-3.5-turbo"
        self.grid = None
        self.visible = False

    @property
    def button_list(self):
        """Buttons for AI assistant class.

        Returns:
            list of tuples in format (tag: str, description: str, command: func, style: str)
        """

        button_list = [
            ('send_ai_btn', 'Send', self.send_ai, 'primary'),
            ('clear_ai_btn', 'Clear', self.clear_ai, 'danger'),
            ('close_ai_btn', 'Close', self.close_ai, 'warning'),
            ('send_api_key_btn','Submit key', self.initiate_ai, 'success'),
            ('disable_ai', 'Skip', self.disable_ai, 'warning'),
            ('show', 'Show response', self.show_response, 'primary'),
            ('hide', 'Hide response', self.hide_response, 'primary')
        ]

        return button_list

    def initiate_ai(self, _=None):
        """Button function for proceeding with AI active"""
        display_message = self.bogui.create_message('Your key is being processed...')
        display(display_message)
        api_key = self.api_key_input_field.value
        if not self.validate_api_key(api_key):
            clear_output(wait=True)
            self.display_ai_popup(self.ai_error_msg)
            self.api_key_input_field.focus()
        else:
            clear_output(wait=True)
            self.ai_disabled[0] = False
            self.next_step[0] = 'bodi'
            self.api_key=api_key

    def disable_ai(self, _=None):
        """Button function for proceeding with AI inactive"""

        self.ai_disabled[0] = True
        self.utils.print_to_console('ai disabled: ' + str(self.ai_disabled[0]))
        clear_output(wait=True)
        self.next_step[0] = 'bodi'

    def send_ai(self, _=None):
        """Button function for sending input to AI API"""

        self.remove_ai_error_message()
        if self.natural_language_prompt.value != '':
            self.display_ai_output(message='The AI assistant is processing your message...')
            self.buttons['show'].disabled = True
            self.openai_api()
        else:
            self.display_ai_output(
                message='Write a message for the AI assistant before sending.')
            self.natural_language_prompt.focus()

    def remove_ai_error_message(self):
        """Removes error messages from display"""

        self.ai_error_msg = ''
        self.ai_error_message_grid.close()
        self.ai_error_message_grid = self.bogui.create_message('')

    def clear_ai(self,_=None):
        """Button function for clearing input text field"""

        self.natural_language_prompt.value = ''

    def close_ai(self, _=None):
        """Button function for closing AI view"""

        self.grid.close()
        self.clear_ai()

    def validate_api_key(self, api_key):
        """Button function for validating API key"""
        if not api_key:
            self.ai_error_msg = 'Please enter your Open AI api key'
            return False

        try:
            openai.api_key = api_key
            response = openai.Model.list()

            if not response.data[0]['object'] == 'model':
                self.ai_error_msg = "Please enter correct Open AI API key.\
                You received no response from the AI assistant."
                return False
            return True


        except openai.error.AuthenticationError:
            self.ai_error_msg = "Incorrect Open AI api key. You can generate API keys in the\
            OpenAI web interface. See https://platform.openai.com/account/api-keys for details."
            return False

    def toggle_ai(self, _=None):
        """Toggles the AI view"""

        self.remove_ai_error_message()

        if self.visible is False:
            self.utils.print_to_console('opening ai')
            self.visible = True
            self.display_ai()
            if self.ai_response != '':
                self.display_ai_output(
                    message='Check the previous response by clicking the button below.')
            else:
                self.display_ai_output()
            self.natural_language_prompt.focus()

        else:
            self.utils.print_to_console('closing ai')
            self.visible = False
            self.close_ai()
            self.ai_output_grid.close()

    def display_ai_popup(self, api_key_error=''):
        """" Function for displaying communication with AI assistant"""

        self.utils.hide_current_input()
        self.utils.hide_selected_input()

        if self.api_key is not None:
            self.next_step[0] = 'bodi'
            return

        api_key_label = self.bogui.create_label('Enter your Open AI key here:')
        api_key_element = widgets.HBox([
            api_key_label,
            widgets.VBox([
                self.api_key_input_field,
                self.bogui.create_error_message(api_key_error, 'red')
            ]),
        ])

        self.grid = widgets.AppLayout(
            header = api_key_element,
            center = widgets.HBox([
                self.buttons['send_api_key_btn'],
                self.buttons['disable_ai']
                ]),
            footer = None,
            pane_widths=[4, 6, 4],
            pane_heights=[4, 6, 3]
        )

        display(self.grid)
        self.api_key_input_field.focus()

    def add_instructions(self, _=None):
        '''Constructs a string containing variables of the user's dataset and
           instructions to the AI assistant'''

        if self.dataset_variables[0] == []:
            return ''

        variables = "The user wants to process a dataset with Python code. Assume that the dataset is stored in a pandas DataFrame called 'df'.\
        The dataset has certain variables. Refer to these given variables where appropriate.\
        Variables of the dataset are: " + ', '.join(str(v) for v in self.dataset_variables[0])
        self.utils.print_to_console(variables)

        return variables

    def display_ai(self, nlp_error= ''):
        '''Displays a text field for entering a question and options for including context'''

        feature_description = self.bogui.create_message(
            'Enter a natural language prompt. The AI assistant will propose code\
            to implement your request.'
            )

        self.grid = widgets.AppLayout(
            header = feature_description,
            center= widgets.VBox([
                self.natural_language_prompt,
                self.bogui.create_error_message(nlp_error, 'red')
            ]),
            footer = widgets.HBox([
                self.buttons['send_ai_btn'],
                self.buttons['clear_ai_btn']
                ]),
            pane_widths=[1, 8, 1],
            pane_heights=[2, 6, 2]
        )
        self.utils.print_to_console('dataset variables: ' + str(self.dataset_variables))
        display(self.grid)

    def display_ai_output(self, message='', ai_output=''):
        """Displays ai output grid. Displays 'Hide' -button if AI output is visible and        
           'Show' -button if there is a previous answer from AI
        
        Args:
            message (str, optional): Message for the user
            ai_output (str, optional): The AI response formatted for HTML
        """

        self.ai_output_grid.close()

        self.ai_output_grid = widgets.AppLayout(
            header = self.bogui.create_message(message),
            center = self.bogui.create_message(ai_output),
            pane_heights = ['40px', 1, '40px']
        )

        if ai_output != '':
            self.ai_output_grid.footer = self.buttons['hide']

        elif self.ai_response != '':
            self.ai_output_grid.footer = self.buttons['show']

        display(self.ai_output_grid)

    def display_ai_error_message(self):
        """Displays error message"""

        self.display_ai_output()
        self.ai_error_message_grid.close()
        self.ai_error_message_grid = self.bogui.create_message(self.ai_error_msg)

        display(self.ai_error_message_grid)

    def openai_api(self):
        """Function to check openai api key"""

        try:
            openai.api_key = self.api_key
            model_engine = self.model_engine
            system_msg = 'If the answer includes code, give the answer in one Python code block\
            indicated with ```python. If not, please ignore all information about the dataset.'
            content = self.natural_language_prompt.value + self.add_instructions()
            response = openai.ChatCompletion.create(
                model = model_engine,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": content},
            ])

            self.ai_response = response.choices[0]['message']['content']
            code = self.utils.get_python_code_from_response(self.ai_response)


            if code == 'No Python code in the response':
                self.display_ai_output(
                    message='Python code was not found in the response.')

            else:
                self.utils.insert_ai_code_into_new_cell(code)
                self.display_ai_output('Code inserted into a code cell above.')

            self.buttons['show'].disabled = False

        except openai.error.Timeout as err:
            self.ai_error_msg = f"OpenAI API request timed out: {err}"
            self.display_ai_error_message()

        except openai.error.APIError as err:
            self.ai_error_msg = f"OpenAI API returned an API Error: {err}"
            self.display_ai_error_message()

        except openai.error.APIConnectionError as err:
            self.ai_error_msg = f"OpenAI API request failed to connect: {err}"
            self.display_ai_error_message()

        except openai.error.InvalidRequestError as err:
            self.ai_error_msg = f"OpenAI API request was invalid: {err}"
            self.display_ai_error_message()

        except openai.error.AuthenticationError as err:
            self.ai_error_msg = f"OpenAI API request was not authorized: {err}"
            self.display_ai_error_message()

        except openai.error.PermissionError as err:
            self.ai_error_msg = f"OpenAI API request was not permitted: {err}"
            self.display_ai_error_message()

        except openai.error.RateLimitError as err:
            self.ai_error_msg = f"OpenAI API request exceeded rate limit: {err}"
            self.display_ai_error_message()

    def format_response(self, text):
        """ Formats AI response for html widget.

        Args:
            test (str): The AI response

        Returns:
            formatted_text (str): The AI response formatted for HTML
        """

        formatted_text = '<br />'.join(text.split('\n'))
        formatted_text = '<pre>' + formatted_text + '</pre>'

        return formatted_text

    def show_response(self, _=None):
        """Button function to show the complete AI response."""

        output = self.format_response(self.ai_response)
        self.display_ai_output(
            message='The response from the AI assistant:',
            ai_output=output)

    def hide_response(self, _=None):
        """Button function to hide AI response."""

        self.display_ai_output(
            message='Check the previous response by clicking the button below.')
