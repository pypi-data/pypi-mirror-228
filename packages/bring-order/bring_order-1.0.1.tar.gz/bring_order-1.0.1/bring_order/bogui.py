"""Methods for creating widgets"""
from ipywidgets import widgets
from ipyfilechooser import FileChooser


class BOGui:
    """General methods for creating widgets"""
    def __init__(self):
        """Class constructor"""

    def create_button(self, desc: str, command, style='success', tooltip=''):
        """Creates button"""
        button = widgets.Button(description=desc,
                                button_style=style,
                                tooltip=tooltip)
        button.on_click(command)
        return button

    def init_buttons(self, buttons):
        """Initializes buttons.

        args:
            buttons: list of tuples.

        returns:
            dictionary containing the buttons

        """
        button_list = {}
        for button in buttons:
            new_button = self.create_button(
                desc=button[1],
                command=button[2],
                style=button[3]
            )
            button_list[button[0]] = new_button
        return button_list

    def create_message(self, value, style=''):
        """Creates HTML"""
        if style == '':
            style = {'font_size': '15px'}
        message = widgets.HTML(value=value, style=style)
        return message

    def create_error_message(self, value='', color='red'):
        """Creates HTML, color: red"""
        error = self.create_message(value=value,
                                    style={'font_size': '12px',
                                           'text_color': color})
        return error

    def create_input_field(self, default_value='', placeholder=''):
        """Creates input field"""
        input_field = widgets.Text(value=default_value, placeholder=placeholder)
        return input_field

    def create_text_area(self, default_value='', place_holder=''):
        """Creates text box"""
        text_area = widgets.Textarea(value=default_value,layout={'width': '70%'},
                                     placeholder=place_holder)
        return text_area

    def create_label(self, value):
        """Creates label"""
        label = widgets.Label(value=value,
                              layout=widgets.Layout(justify_content='flex-end'))
        return label

    def create_grid(self, rows, cols, items, width='50%'):
        """Creates grid of widgets"""
        grid = widgets.GridspecLayout(rows,
                                      cols,
                                      height='auto',
                                      width=width,
                                      grid_gap="0px")
        item_index = 0
        k = len(items)
        for i in range(rows):
            for j in range(cols):
                if k == 0:
                    break
                grid[i, j] = items[item_index]
                item_index += 1
                k -= 1

        return grid

    def create_int_text(self, default_value=1, desc=''):
        """Creates integer input"""
        int_text = widgets.BoundedIntText(value=default_value, min=0,
                                        description=desc, layout={'width':'80px'})
        return int_text

    def create_radiobuttons(self, options, desc=''):
        """Creates radiobuttons"""
        radiobuttons = widgets.RadioButtons(
            options=options,
            description=desc,
            disabled=False,
            layout={'width': 'max-content'}
        )

        return radiobuttons

    def create_checkbox(self, desc):
        '''Create checkbox'''
        checkbox = widgets.Checkbox(
            value=False, description=desc,
            disabled=False, indent=False
        )

        return checkbox

    def create_file_chooser(self):
        """Creates a FileChooser object"""
        file_chooser = FileChooser()

        return file_chooser

    def create_int_slider(self):
        '''Creates a Numeric Slider'''
        slider = widgets.IntSlider(
            value=50, min=0, max=100, step=5,
            description='', disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True, readout_format='d'
        )

        return slider

    def create_password_field(self, default_value='', placeholder=''):
        """Creates password field"""
        password_field = widgets.Password(value=default_value,
                                          placeholder=placeholder,
                                          disabled=False)
        return password_field
