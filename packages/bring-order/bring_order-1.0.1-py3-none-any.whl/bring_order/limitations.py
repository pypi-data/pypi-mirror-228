"""Data limitations manager"""
from ipywidgets import widgets

class Limitations:
    """Manages data limitations through different phases of analysis."""
    def __init__(self, bogui, boval):
        """Class constructor."""
        self.bogui = bogui
        self.boval = boval
        self.data_limitations = [self.bogui.create_input_field('', 'Limitation 1')]
        self.empty_limitations_error = self.bogui.create_error_message()
        self.remove_checkboxes = [self.bogui.create_checkbox('Remove')]

    def add_limitation(self):
        """Adds new limitation input to list."""
        self.data_limitations.append(self.bogui.create_input_field
                                    ('',f'Limitation {len(self.data_limitations)+1}'))
        self.remove_checkboxes.append(self.bogui.create_checkbox('Remove'))
        self.empty_limitations_error.value = ''

    def remove_limitations(self):
        """Removes selected limitations from list."""

        not_removed = []
        for index, check in enumerate(self.remove_checkboxes):
            if not check.value:
                limitation = self.bogui.create_input_field(
                    self.data_limitations[index].value,
                    f'Limitation {len(not_removed)+1}'
                )
                not_removed.append(limitation)

        self.data_limitations = not_removed
        self.remove_checkboxes = self.remove_checkboxes[:len(self.data_limitations)]

        if len(self.data_limitations) == 0:
            self.add_limitation()

    def create_limitation_grid(self):
        """Returns text boxes for adding limitations"""
        limitations_label = self.bogui.create_message(
                value='Identify limitations to the data: what kind of\
                questions cannot be answered with it?')

        self.remove_checkboxes = [self.bogui.create_checkbox('Remove')
                                  for _ in range(len(self.data_limitations))]

        limitation_grid = widgets.AppLayout(
            header=limitations_label,
            center=widgets.HBox([
                widgets.VBox(self.data_limitations),
                widgets.VBox(self.remove_checkboxes)
            ]),
            pane_heights=['30px', 1, '70px'],
            grid_gap='12px'
        )

        return limitation_grid

    def check_limitations(self, item=''):
        """Checks that limitations have been given or commented"""
        if not self.boval.value_not_empty_or_contains_symbols(item):
            return False
        return True

    def call_check_limitation(self):
        """Checks that none of the limitations is empty"""
        for limitation in self.data_limitations:
            if not self.check_limitations(limitation.value):
                return False
        return True

    def format_limitations(self):
        """Formats limitations for markdown to prevent Javascript error        
        Returns:
            formatted_limitations (str)
        """
        formatted_limitations = '### Limitations\\n'
        for item in self.data_limitations:
            limitation = '<br />'.join(item.value.split('\n'))
            limitation_text = f'- {limitation}\\n'
            formatted_limitations += limitation_text

        return formatted_limitations

    def set_error_value(self, text):
        """Sets error value."""
        self.empty_limitations_error.value = text

    def get_values(self):
        """Returns a list of the limitations as strings."""

        return [limitation.value for limitation in self.data_limitations]

    def not_normally_distributed_variables(self):
        """Returns a list of variable names in limitations that are not normally distributed."""

        result = []
        for limitation in self.get_values():
            if 'is not normally distributed' in limitation:
                result.append(limitation[:-28])

        return result

    def not_independent_variables(self):
        """Returns a list of variables that are not independent. Each item is a pair of
        variables as a string joined by 'and'."""

        result = []
        for limitation in self.get_values():
            if 'are not independent' in limitation:
                result.append(limitation[:-20])

        return result

    def other_limitations(self):
        """Returns a list of limitations the user has added by hand."""

        result = []
        for limitation in self.get_values():
            if ('not normally distributed' in limitation) or ('are not independent' in limitation):
                continue
            result.append(limitation)

        return result

    def get_limitations_for_print(self):
        """Returns a compact bullet list of limitations as HTML widget."""

        text = ''
        limitations = self.get_values()
        if any(limitation != '' for limitation in limitations):
            text = '<h4>There are some data limitations you should consider:</h4>\n<ul>\n'

            not_normal = self.not_normally_distributed_variables()
            if len(not_normal) > 0:
                text += '<li><b>Variables that are not normally distributed:</b> '
                text += (', ').join(not_normal)
                text += '</li>\n'

            not_independent = self.not_independent_variables()
            if len(not_independent) > 0:
                text += '<li><b>Variables that are not independent:</b> '
                text += (', ').join(not_independent)
                text += '</li>\n'

            other = self.other_limitations()
            text += '\n'.join([
                '<li>' + limitation + '</li>'
                for limitation in other
                if limitation != ''
            ])

            text += '</ul>'

        return widgets.HTML(text)
