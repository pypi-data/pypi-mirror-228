"""Bring Order Data Import and preparation."""
import sys
import pandas as pd
from ipywidgets import widgets
from IPython.display import display, clear_output
from pptx import Presentation
from limitations import Limitations
from stattests import Stattests

class Bodi:
    """Creates code cells for importing data and markdown cell(s) to describe data limitations"""
    def __init__(self, boutils, bogui, boval, dataset_variables, ai_disabled, next_step):
        """Class constructor
            Args:
                bogui: Bring Order GUI components class
                boutils: Bring order helper utilities class
                next_step: next action to do (str)

            fields: text and integer fiels
                    0 = title
                    1 = data_name
                    2 = data_description
                    3 = add_cells_int
        """

        self.boutils = boutils
        self.bogui = bogui
        self.boval = boval
        self.cell_count = 0
        self.ai_disabled = ai_disabled
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.fields = [self.bogui.create_input_field(),
                       self.bogui.create_input_field(),
                       self.bogui.create_text_area(),
                       self.bogui.create_int_text()]
        self.limitations = Limitations(self.bogui, self.boval)
        self.file_chooser = self.bogui.create_file_chooser()
        self.stattests = Stattests(self.bogui)
        self.dataset_variables = dataset_variables
        self.not_normal = []
        self.checklist = []
        self.next_step = next_step
        self.limitations_visible = False

    @property
    def button_list(self):
        """Buttons for Bodi class.

        Returns:
            list of tuples in format (tag: str, description: str, command: func, style: str)
        """

        button_list = [
            ('save', 'Save description', self._start_data_import, 'success'),
            ('analyze', 'Analyze this data', self._import_data, 'success'),
            ('test', 'Test', self._check_variable_independence, 'primary'),
            ('close', 'Close test', self._close_independence_test, 'warning'),
            ('independence', 'Test independence', self._display_independence_test, 'success'),
            ('import', 'Import manually', self._show_cell_operations, 'primary'),
            ('open', 'Open cells', self._open_cells, 'primary'),
            ('delete', 'Delete last cell', self._delete_last_cell, 'warning'),
            ('run', 'Run cells', self._run_cells, 'primary'),
            ('add', 'Add limitation', self._add_limitation, 'primary'),
            ('remove', 'Remove limitations', self._remove_limitation, 'warning'),
            ('start', 'Start analysis', self._start_analysis_clicked, 'success'),
            ('assist', 'AI assistant', self._toggle_ai, 'success'),
            ('limitations', 'Check limitations', self._display_limitations_view, 'success'),
            ('choose', 'Choose data file', self._display_file_chooser, 'warning')
        ]

        return button_list

    def _toggle_ai(self, _=None):
        """Button function to open/close AI assistant.
        
        Args:
            showAI (boolean, optional): set to False to only toggle the button text/description
        """

        if self.ai_disabled[0]:
            return

        if self.buttons['assist'].description == 'AI assistant':
            clear_output(wait=True)
            message = self.limitations.get_limitations_for_print()
            display(self.data_preparation_grid(message))
            self.buttons['assist'].description = 'Close AI assistant'
            self.buttons['assist'].button_style = 'warning'
            for button in self.buttons:
                if button != 'assist':
                    self.buttons[button].disabled = True
        else:
            self.buttons['assist'].description = 'AI assistant'
            self.buttons['assist'].button_style = 'success'
            for button in self.buttons:
                if button != 'assist':
                    self.buttons[button].disabled = False
        self.next_step[0] = 'toggle_ai'

    def _add_limitation(self, _=None):
        """Button function for adding new limitation."""

        self.limitations.add_limitation()
        self._display_limitations_view()

    def _remove_limitation(self, _=None):
        """Button function for removing limitation."""

        self.limitations.remove_limitations()
        self._display_limitations_view()

    def data_preparation_grid(self, message=None):
        """Creates widget grid.

        Args:
            message (widget, optional): HTML widget to be displayed
        """

        self.limitations.set_error_value('')
        cell_number_label = self.bogui.create_label(
            'Add code cells for data preparation:')

        buttons = self.bogui.create_grid(
            2,
            3,
            [
                self.buttons['open'],
                self.buttons['delete'],
                self.buttons['run'],
                self.buttons['independence'],
                self.buttons['assist'],
                self.buttons['limitations']
            ]
        )
        buttons.width = '100%'

        grid = widgets.AppLayout(
            left_sidebar=widgets.HBox([
                cell_number_label,
                self.fields[3]
            ]),
            right_sidebar=buttons,
            footer=message,
            pane_widths=['320px', 0, '460px'],
            pane_heights=['0px', '80px', 1],
            grid_gap='12px'
        )
        return grid

    def _show_cell_operations(self, _=None):
        """Button function for manual import, shows buttons for cell operations."""

        self.dataset_variables[0] = []
        clear_output(wait=True)
        display(self.buttons['choose'])
        display(self.data_preparation_grid())

    def _open_cells(self, _=None):
        """Button function that opens selected number of cells above widget cell"""

        self.buttons['choose'].disabled = True

        if self.fields[3].value > 0:
            self.cell_count += self.fields[3].value
            self.boutils.create_code_cells_above(self.fields[3].value)
            self.boutils.focus_on_input_above(self.fields[3].value + 2)

    def _delete_last_cell(self, _=None):
        """Button function to delete the last data import code cell"""

        if self.cell_count > 0:
            self.boutils.delete_cell_above()
            self.cell_count -= 1
        if self.cell_count == 0:
            self.buttons['choose'].disabled = False

    def _run_cells(self, _=None):
        """Button function that runs cells for manual data import"""

        clear_output(wait=True)
        display(self.data_preparation_grid(
            message=self.limitations.get_limitations_for_print()))
        display(self.bogui.create_message(
            '<h4>Check limitations if you are ready to start analysis.</h4>'
        ))

        if len(self.not_normal) > 0:
            for stat_test in self.checklist:
                self.boutils.check_cells_above(self.cell_count, stat_test, self.not_normal)

        self.boutils.run_cells_above(self.cell_count)

    def _display_limitations_view(self, _=None):
        """Displays limitation view."""

        limitation_grid = self.limitations.create_limitation_grid()
        limitation_grid.footer=widgets.VBox([
            self.limitations.empty_limitations_error,
            widgets.HBox([
                self.buttons['add'],
                self.buttons['remove']
            ])
        ])
        clear_output(wait=True)
        display(self.data_preparation_grid())
        display(limitation_grid)
        display(self.buttons['start'])

    def format_data_description(self):
        """Formats data description for markdown        
        Returns:
            formatted_text (str)
        """

        title = f'# {self.fields[0].value}'
        dataset = f'{self.fields[1].value}'
        description = '<br />'.join(self.fields[2].value.split('\n'))
        formatted_text = f'{title}\\n ## Data: {dataset}\\n ### Description\\n{description}'
        return formatted_text

    def _start_analysis_clicked(self, _=None):
        """Button function to start analysis after data preparation"""

        if self.limitations.call_check_limitation():
            text = self.limitations.format_limitations()
            self.boutils.create_markdown_cells_above(1, text=text)
            clear_output(wait=True)
            self.next_step[0] = 'start_analysis'
        else:
            self.limitations.set_error_value('Data limitations cannot be empty or\
                 contain special symbols')

    def fc_callback(self):
        """Shows buttons to continue with selected data file or import manually."""

        clear_output(wait=True)

        if self.file_chooser.selected.endswith('.csv'):
            self.file_chooser.title = f'Selected file: {self.file_chooser.selected_filename}'
            display(widgets.VBox([
                self.file_chooser,
                self.buttons['analyze']
            ]))
        else:
            self.file_chooser.title = 'Unknown file type: choose a csv file or import manually.'
            display(widgets.VBox([
                self.file_chooser,
                self.buttons['import']
            ]))

    def _import_data(self, _=None):
        """Imports selected data in code cells and opens next view for data preparation."""

        self.boutils.create_code_cells_above(2)
        self.boutils.execute_cell_from_current(
            distance=-2,
            code='import pandas as pd',
            hide_input=False
        )
        self.boutils.execute_cell_from_current(
            distance=1,
            code=f"df = pd.read_csv('{self.__check_file_path()}')",
            hide_input=False
        )
        # Load config files for the tests to be checked
        self.checklist = self.load_cfg_file(self.file_chooser.selected_path)
        self.check_variables()

    def __check_file_path(self):
        '''Check operation system. If windows corrects file path.
            Returns:
                path: str
        '''

        path = self.file_chooser.selected
        if sys.platform.startswith('win'):
            path = path.replace('\\', '/')
        return path

    def load_cfg_file(self, cfg_path):
        """Checks if given path contains file bringorder.cfg. If found,
        returns a list with the tests specified in the config file. Otherwise
        returns the list containing 'ttest'.

        args:
            cfg_path: directory containing bringorder.cfg_file
        returns:
            tests_to_check: list of test names
        """

        if sys.platform.startswith('win'):
            cfg_file = cfg_path + "\\bringorder.cfg"
        else:
            cfg_file = cfg_path + "/bringorder.cfg"
        tests_to_check = []
        try:
            with open(cfg_file, 'r', encoding="utf-8") as get_cfg:
                for line in get_cfg:
                    line = line.replace("\n", "")
                    tests_to_check.append(line)
            tests_to_check.pop()
        except FileNotFoundError:
            tests_to_check.append('ttest')
        return tests_to_check

    def check_normal_distribution(self, data_frame):
        """Checks which variables are not normally distributed.

        Args:
            data_frame (DataFrame): the data to be tested        
        Returns:
            not_normal_dist (list): List of variables that are not normally distributed
        """
        n_distributed = self.stattests.check_numerical_data(data_frame)
        not_normal_dist = []

        for key, val in n_distributed.items():
            if not val:
                not_normal_dist.append(key)

        return not_normal_dist

    def _check_variable_independence(self, _=None):
        """Button function for independence test. Checks independence and adds limitation
        if variables are not independent.
        """

        result = self.stattests.check_variable_independence()

        if isinstance(result[2], str):
            message = self.bogui.create_error_message(result[2])

        elif result[2] is False:
            limitation = f'{result[0]} and {result[1]} are not independent'
            if not limitation in self.limitations.get_values():
                if self.limitations.data_limitations[-1].value != '':
                    self.limitations.add_limitation()
                self.limitations.data_limitations[-1].value = limitation
            message = self.bogui.create_message(f'Result added to limitations: {limitation}')
        else:
            message = self.bogui.create_message(f'{result[0]} and {result[1]} are independent')

        display(message)

    def _display_independence_test(self, _=None):
        """Displays independence test and disables other buttons."""

        independence_test = self.stattests.select_variables()
        if not hasattr(independence_test, 'value'):
            independence_test.footer = widgets.HBox([
                self.buttons['test'],
                self.buttons['close']
            ])

            for button in ['open', 'delete', 'run', 'assist', 'limitations']:
                self.buttons[button].disabled = True

            clear_output(wait=True)
            display(self.data_preparation_grid())

        self.buttons['independence'].disabled = True
        display(independence_test)

    def _close_independence_test(self, _=None):
        """Closes the independence test and activates buttons."""

        for button in ['open', 'delete', 'run', 'independence', 'limitations']:
            self.buttons[button].disabled = False

        self.buttons['assist'].disabled = self.ai_disabled[0]

        clear_output(wait=True)
        message = self.limitations.get_limitations_for_print()
        display(self.data_preparation_grid(message=message))

    def check_variables(self):
        """Checks if data variables are normally distributed.
        Displays buttons for independence test and cell operations.
        """

        data_frame = pd.read_csv(self.file_chooser.selected)
        self.dataset_variables[0] = data_frame.columns.values.tolist()
        self.stattests.dataset = data_frame

        self.not_normal = self.check_normal_distribution(data_frame)
        for index, variable in enumerate(self.not_normal):
            if index != 0:
                self.limitations.add_limitation()
            limitation = f'{variable} is not normally distributed'
            self.limitations.data_limitations[index].value = limitation

        clear_output(wait=True)
        if len(self.not_normal) > 0:
            message = self.limitations.get_limitations_for_print()
            display(self.data_preparation_grid(message=message))
        else:
            display(self.data_preparation_grid())

    def _display_file_chooser(self, _=None):
        """Displays file chooser for data import."""

        clear_output(wait=True)
        display(widgets.VBox([
            self.file_chooser,
            self.buttons['import']
        ]))

    def _start_data_import(self, _=None):
        """Creates markdown for data description and shows buttons for data import"""

        if not self.boval.value_not_empty_or_contains_symbols(self.fields[0].value):
            self.bodi(error = 'The title cannot be empty or contain special symbols')
        elif not self.boval.value_not_empty_or_contains_symbols(self.fields[1].value):
            self.bodi(error = 'The data set name cannot be empty or contain special symbols')
        elif not self.boval.value_not_empty_or_contains_symbols(self.fields[2].value):
            self.bodi(error = 'The data description cannot be empty or contain special characters')
        else:
            self.boutils.pptx_file = self.fields[0].value + '.pptx'
            self.boutils.prs = Presentation()
            self.boutils.create_markdown_cells_above(1, text=self.format_data_description())
            self.file_chooser.register_callback(self.fc_callback)
            self.file_chooser.title = 'Choose a data file:'
            self._display_file_chooser()

    def bodi(self, error=''):
        """Starts data import phase by asking titles and data description.

        args: Error message: str
        """

        question = self.bogui.create_message('What kind of data are you using?')
        title_label = self.bogui.create_label('Main title of your research:')
        data_name_label = self.bogui.create_label('Name of the data set:')
        description_label = self.bogui.create_label('Description of the data:')
        error_message = self.bogui.create_error_message(error)
        self.buttons['assist'].disabled = self.ai_disabled[0]

        grid = widgets.AppLayout(
            header = question,
            left_sidebar = widgets.VBox([
                title_label,
                data_name_label,
                description_label
            ]),
            center=widgets.VBox([
                    self.fields[0],
                    self.fields[1],
                    self.fields[2]
            ]),
            footer = widgets.HBox([
                self.buttons['save'],
                error_message,
            ]),
            pane_widths=[1, 5, 0],
            grid_gap='10px'
        )

        clear_output(wait=True)
        display(grid)

        if 'name' in error:
            self.fields[1].focus()
        elif 'description' in error:
            self.fields[2].focus()
        else:
            self.fields[0].focus()

    def change_cell_count(self, number):
        """Changes the cell_count value by the given number."""

        self.cell_count += number
        self.cell_count = max(self.cell_count, 0)
