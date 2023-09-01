"""Class for Inductive analysis"""
from ipywidgets import widgets
from IPython.display import display, clear_output

class Inductive:
    """Class that guides inductive analysis"""

    def __init__(self, bogui, boutils, boval, ai_disabled, next_step):
        """Class constructor.
            Args:
                bogui:
                boutils:
                next_step:
            
            lists:  0 = list of preconceptions, 
                    1 = list of observations
                    2 = list of preconseption checkboxes
            fields: text and integer fiels
                    0 = number of cells
                    1 = observation field (note)
                    2 = summary field
                    3 = error message
                    4 = pre-evaluation slider
                    5 = post-evaluation slider
                    6 = evaluation
        """

        self.bogui = bogui
        self.utils = boutils
        self.ai_disabled = ai_disabled
        self.boval = boval
        self.next_step = next_step
        self._cell_count = 0
        self.not_normal = []
        self.checklist = []
        self.conclusion = None
        self.buttons = self.bogui.init_buttons(self.button_list)
        self.data_limitations = [self.bogui.create_input_field('Data limitations missing')]
        self.lists = [
            [self.bogui.create_input_field('', 'Preconception 1')],
            [],
            []
        ]
        self.fields = [
            self.bogui.create_int_text(),
            self.bogui.create_text_area(),
            self.bogui.create_text_area('', 'Summary'),
            self.bogui.create_error_message(),
            self.bogui.create_int_slider(),
            self.bogui.create_int_slider(),
            None
        ]

    @property
    def button_list(self):
        """Buttons for Inductive class.

        Returns:
            list of tuples in format (tag: str, description: str, command: func, style: str)
        """

        button_list = [
            ('add', 'Add preconception', self._add_preconception, 'primary'),
            ('save', 'Save preconceptions', self._save_preconceptions, 'success'),
            ('open', 'Open cells', self._open_cells, 'primary'),
            ('delete', 'Delete last cell', self._delete_last_cell, 'warning'),
            ('clear', 'Clear cells', self._clear_cells, 'danger'),
            ('run', 'Run cells', self._run_cells, 'primary'),
            ('ready', 'Ready to summarize', self._execute_ready, 'success'),
            ('submit_obs', 'Submit observation', self._new_observation, 'success'),
            ('submit_sum', 'Submit summary', self._submit_summary, 'success'),
            ('lock', 'Lock evaluation', self._lock_evaluation_pressed, 'success'),
            ('save_results', 'Save', self._save_results, 'success'),
            ('assist', 'AI assistant', self.toggle_ai, 'success'),
            ('complete', 'Save and continue', self._complete_evaluation, 'success')
        ]

        return button_list

    def toggle_ai(self, _=None):
        """Button function to open/close AI assistant"""

        if self.buttons['assist'].description == 'AI assistant':
            self.buttons['assist'].description = 'Close AI assistant'
            self.buttons['assist'].button_style = 'warning'
            for button in self.buttons:
                if button != 'assist':
                    self.buttons[button].disabled = True
        else:
            self.buttons['assist'].description = 'AI assistant'
            self.buttons['assist'].button_style = 'success'
            for button in self.buttons:
                if button != 'assist' and (button != 'ready' or self.lists[1]):
                    self.buttons[button].disabled = False
        self.next_step[0] = 'toggle_ai'

    def start_inductive_analysis(self):
        """Starts inductive analysis."""

        self.utils.create_markdown_cells_above(1, '## Data exploration')
        display(self._create_preconception_grid())
        self.lists[0][0].focus()

    def _add_preconception(self, _=None):
        """Button function to add new preconception."""

        self.lists[0].append(
            self.bogui.create_input_field('', f'Preconception {len(self.lists[0]) + 1}')
        )

        clear_output(wait=True)
        display(self._create_preconception_grid())
        self.lists[0][-1].focus()

    def _check_preconceptions(self):
        """Checks that at least one of the preconceptions has a non-empty value."""

        for item in self.lists[0]:
            if self.boval.value_not_empty_or_contains_symbols(item.value):
                return True

        return False

    def _format_preconceptions(self):
        """Formats preconceptions for markdown.

        Returns:
            formatted_preconceptions (str)
        """

        formatted_preconceptions = '### Preconceptions\\n'
        for item in self.lists[0]:
            preconception_text = f'- {item.value}\\n'
            formatted_preconceptions += preconception_text

        formatted_preconceptions += '### Data analysis'
        return formatted_preconceptions

    def _save_preconceptions(self, _=None):
        """Button function to save preconceptions as markdown and show cell operation buttons."""

        clear_output(wait=True)

        if self._check_preconceptions():
            # Remove empty preconceptions from the list
            self.lists[0] = list(filter(
                lambda text_input: text_input.value != '',
                self.lists[0]
            ))

            self.utils.create_markdown_cells_above(
                how_many=1,
                text=self._format_preconceptions()
            )

            display(self._create_cell_operations())

        else:
            display(self._create_preconception_grid(
                error='The preconception cannot be empty or contain special symbols')
            )

    def _create_preconception_grid(self, error=''):
        """Creates the grid with input fields and buttons to add and save preconceptions."""

        preconceptions_label = self.bogui.create_message(
                value='Write about your preconceptions concerning the data set:\
                    what do you expect to find?')

        preconception_grid = widgets.AppLayout(
            header=preconceptions_label,
            center=widgets.VBox(self.lists[0]),
            footer=widgets.VBox([
                self.bogui.create_error_message(error),
                widgets.HBox([
                    self.buttons['add'],
                    self.buttons['save']
                ])
            ]),
            pane_heights=['30px', 1, '70px'],
            grid_gap='12px'
        )

        return preconception_grid

    def _open_cells(self, _=None):
        """Open cells button function that opens the selected number of code cells."""

        if self.fields[0].value > 0:
            self._cell_count += self.fields[0].value
            self.utils.create_code_cells_above(self.fields[0].value)
            self.utils.focus_on_input_above(self.fields[0].value + 2)

    def _delete_last_cell(self, _=None):
        """Delete last cell button function."""

        if self._cell_count > 0:
            self.utils.delete_cell_above()
            self._cell_count -= 1

    def _clear_cells(self, _=None):
        """Clears all code cells above."""

        self.utils.clear_code_cells_above(self._cell_count)

    def _buttons_disabled(self, disabled):
        """Activates/deactivates buttons.
        
        Args:
            disabled (bool): True to disable, False to activate
        """

        self.buttons['open'].disabled = disabled
        self.buttons['clear'].disabled = disabled
        self.buttons['delete'].disabled = disabled
        self.buttons['ready'].disabled = disabled
        self.buttons['assist'].disabled = disabled

    def _run_cells(self, _=None):
        """Executes cells above and displays text area for observations of analysis."""

        if self._cell_count <= 0:
            return

        cell_buttons = self._create_cell_operations()
        self._buttons_disabled(True)
        notes_label = self.bogui.create_label(value='Explain what you observed:')
        self.conclusion = widgets.VBox([
            widgets.HBox([notes_label, self.fields[1]]),
            self.fields[3],
            self.buttons['submit_obs']
        ])

        clear_output(wait=True)
        display(cell_buttons)
        display(self.conclusion)
        self.fields[1].focus()

        if len(self.not_normal) > 0:
            for stat_test in self.checklist:
                self.utils.check_cells_above(self._cell_count, stat_test, self.not_normal)

        self.utils.run_cells_above(self._cell_count)

    def _format_observation(self):
        """Formats observation for markdown.
        
        Returns:
            formatted_obs (str)
        """

        formatted_obs = f'#### Observation {len(self.lists[1])}: '

        notes_list = self.fields[1].value.split('\n')
        first_line_list = notes_list[0].split(' ')
        first_words = self.boval.get_first_words(first_line_list)
        formatted_obs += f'{first_words}\\n'

        notes = '<br />'.join(notes_list)
        formatted_obs += notes

        return formatted_obs

    def _new_observation(self, _=None):
        """Checks new observation, saves it, and resets cell count."""

        if self.boval.value_not_empty_or_contains_symbols(self.fields[1].value):
            self.lists[1].append(self.fields[1].value)
            text = self._format_observation()
            self.utils.create_markdown_cells_above(1, text=text)
            self._buttons_disabled(False)
            self.buttons['assist'].disabled = self.ai_disabled[0]
            self.fields[3].value = ''
            self.fields[1].value = ''
            self._cell_count = 0

            clear_output(wait=True)
            display(self._create_cell_operations())
            self.buttons['ready'].disabled = False

        else:
            self.fields[3].value = 'The observation cannot be empty or contain special symbols'

    def _execute_ready(self, _=None):
        """Button function for Ready to summarize button."""

        self._display_summary()

    def _display_summary(self, error=''):
        """Prints all observations and asks for summary."""

        observations = "<ul>\n"
        observations += "\n".join(["<li>" + observation + "</li>"
                                 for observation in self.lists[1]])
        observations += "\n</ul>"

        observation_list = widgets.HTML(
            '</br>'+'<h4>All your observations from the data:</h4>'+observations)

        summary_label = self.bogui.create_label('What do these observations mean?')
        error_message = self.bogui.create_error_message(value=error)
        grid = widgets.VBox([
            observation_list,
            widgets.HBox([summary_label, self.fields[2]]),
            error_message,
            self.buttons['submit_sum']
        ])

        clear_output(wait=True)
        display(grid)
        self.fields[2].focus()

    def _format_summary(self):
        """Formats summary for markdown.
        
        Returns:
            formatted_summary (str)
        """

        formatted_summary = '### Summary: '

        summary_list = self.fields[2].value.split('\n')
        first_line_list = summary_list[0].split(' ')
        first_words = self.boval.get_first_words(first_line_list)
        formatted_summary += f'{first_words}\\n'

        summary = '<br />'.join(summary_list)
        formatted_summary += summary

        return formatted_summary

    def _submit_summary(self, _=None):
        """Button function to submit summary."""

        if not self.boval.value_not_empty_or_contains_symbols(self.fields[2].value):
            self._display_summary(error='The summary cannot be empty or contain special symbols')
            return

        text = self._format_summary()
        self.utils.create_markdown_cells_above(1, text=text)

        self._evaluation_of_analysis()

    def _evaluation_of_analysis(self, _=None):
        """Displays the slider for pre-evaluation."""

        self.buttons['submit_sum'].disabled = True

        grid = widgets.AppLayout(
            header = self.bogui.create_message(
                        'Evaluate your analysis: how many percent of your\
                            preconceptions does the analysis confirm?'),
            center = widgets.HBox([
                self.fields[4],
                self.buttons['lock']
            ])
        )

        clear_output(wait=True)
        display(grid)

    def _lock_evaluation_pressed(self, _=None):
        """Locks first evaluation value and shows preconception checkboxes."""

        label = self.bogui.create_message('Which of your preconceptions\
                                         does the analysis confirm?')
        self.lists[2] = [
                self.bogui.create_checkbox(prec.value) for prec in self.lists[0]
                ]
        output = widgets.VBox(self.lists[2])

        grid = widgets.AppLayout(
            header = self.bogui.create_message('After checking the preconceptions,\
                                                what percentage of them was confirmed?'),
            center = widgets.VBox([
                self.fields[5],
                self.buttons['save_results']
            ])
        )

        clear_output(wait=True)
        display(label, output)
        display(grid)

    def _save_results(self, _=None):
        """Saves evaluation as markdown."""

        limit = "\\n- ".join(lim.value for lim in self.data_limitations)
        formatted_text = '#### The analysis did not support these preconceptions:\\n'
        for preconception in self.lists[2]:
            if preconception.value is False:
                text = f'- {preconception.description}\\n'
                formatted_text += text
        if formatted_text == '#### The analysis did not support these preconceptions:\\n':
            formatted_text = '#### Note that the analysis appears to confirm\
            all stated preconceptions!\\n'

        text = (f'### Evaluation of the analysis \\n'
                f'#### Limitations that were noticed in the data:\\n- {limit}\\n'
                f'#### Evaluations:\\n'
                f'- According to the pre-evaluation, the analysis confirmed\
                approximately {self.fields[4].value} % of the preconceptions.\\n'
                f'- According to the final evaluation, the analysis confirmed approximately\
                {self.fields[5].value} % of the preconceptions.\\n'
                f'{formatted_text}')

        self.utils.create_markdown_cells_above(how_many=1, text=text)
        self._close_evaluation()

    def _close_evaluation(self):
        '''Creates text field for final evaluation'''
        clear_output(wait=True)
        row = int(self.__check_evaluation_difference())
        if row != 0:
            eval_label = self.bogui.create_message('What caused the difference\
                 between the pre- and final evaluation?')
            self.fields[6] = widgets.Textarea(value='',description='',disabled=False,
                                rows=row,layout={'width': '80%'})
            grid = widgets.AppLayout(
                header=None,
                center = widgets.VBox([eval_label, self.fields[6]]),
                footer = self.buttons['complete']
            )
            display(grid)
            self.fields[6].focus()
        else:
            self.next_step[0] = 'analysis_done'

    def __check_evaluation_difference(self):
        '''Check evaluation difference
            Returns:
                number of rows for text field: int
        '''
        difference = abs(int(self.fields[4].value) - int(self.fields[5].value))
        num_row = 0
        if difference <= 10:
            return num_row
        num_row = difference/5
        return num_row

    def _complete_evaluation(self, _=None):
        clear_output(wait=True)
        value = self.fields[6].value
        value_list = self.fields[6].value.split('\n')
        value = '<br />'.join(value_list)

        evaluation = '#### The difference between the pre- and final evaluation caused by: \\n'
        if value == '':
            evaluation += 'No explanation was given!'
        else:
            evaluation += f'{value}'
        self.utils.create_markdown_cells_above(1, text=evaluation)
        self.next_step[0] = 'analysis_done'

    def _checkbox_preconceptions(self):
        """Displays preconception checkboxes."""

        checkboxes = [self.bogui.create_checkbox(prec) for prec in self.lists[0]]
        output = widgets.VBox(children=checkboxes)
        clear_output(wait=True)
        display(output)

    def _create_cell_operations(self):
        """Displays buttons for operations in inductive analysis."""

        self.buttons['ready'].disabled = True
        self.buttons['assist'].disabled = self.ai_disabled[0]
        cell_number_label = self.bogui.create_label('Add code cells for your analysis:')

        buttons = self.bogui.create_grid(
            2,
            3,
            [
                self.buttons['open'],
                self.buttons['delete'],
                self.buttons['run'],
                self.buttons['clear'],
                self.buttons['assist'],
                self.buttons['ready']
            ]
        )
        buttons.width = '100%'

        grid = widgets.AppLayout(
            left_sidebar=widgets.HBox([
                cell_number_label,
                self.fields[0]
            ]),
            right_sidebar=buttons,
            footer=None,
            pane_widths=['320px', 0, '460px'],
            pane_heights=['0px', '80px', 1],
            grid_gap='12px'
        )

        return grid

    def __repr__(self):
        return ''

    def change_cell_count(self, number):
        """Changes the cell_count value by the given number."""

        self._cell_count += number
        self._cell_count = max(self._cell_count, 0)
