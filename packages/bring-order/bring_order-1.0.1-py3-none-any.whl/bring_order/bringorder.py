"""Main class"""
import os
import sys
import time
from ipywidgets import widgets
from IPython.display import display
from jupyter_ui_poll import ui_events

class_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, class_dir)
from bogui import BOGui
from bodi import Bodi
from boutils import BOUtils
from deductive import Deductive
from inductive import Inductive
from next_analysis import NextAnalysis
from ai import Ai
from boval import BOVal

class BringOrder:
    """Main class"""
    def __init__(self):
        """Class constructor.     
        'next_step' is passed on to other classes and used to track
        which UI module to run next."""

        self.boutils = BOUtils()
        self.bogui = BOGui()
        self.deductive = None
        self.inductive = None
        self.boval = BOVal()
        self.buttons = {}
        self.dataset_variables = [[]]
        self.ai_disabled = [False]
        self.next_step = [None]
        self.next_analysis = NextAnalysis(
            self.bogui,
            self.boutils,
            self.next_step)
        self.ai = Ai(
            self.bogui,
            self.boutils,
            self.dataset_variables,
            self.ai_disabled,
            self.next_step
        )
        self.bodi = None
        self.bring_order()

    @property
    def button_list(self):
        """Buttons for BringOrder class.

        Returns:
            list of tuples in format (tag: str, description: str, command: func, style: str)
        """
        button_list = [('deductive', 'Test hypothesis', self._deductive, 'success'),
                       ('inductive', 'Explore data', self._inductive, 'success')]

        return button_list

    def _deductive(self, _=None):
        """Deductive button function"""
        self.next_step[0] = 'deductive_analysis'

    def _inductive(self, _=None):
        """Inductive button function"""
        self.next_step[0] = 'inductive_analysis'

    def close_buttons(self):
        """Hides buttons"""
        self.buttons['deductive'].close()
        self.buttons['inductive'].close()

    def start_deductive_analysis(self, _=None):
        """Starts deductive analysis

        returns:
            function: sets self.deductive.start_deductive_analysis() to next_step
        """
        self.close_buttons()
        self.deductive.data_limitations = self.bodi.limitations.data_limitations
        self.deductive.not_normal = self.bodi.not_normal
        self.deductive.checklist = self.bodi.checklist
        self.boutils.change_cell_count = self.deductive.change_cell_count
        return self.deductive.start_deductive_analysis()

    def start_inductive_analysis(self, _=None):
        """Starts inductive analysis

        returns:
            function: sets self.inductive.start_inductive_analysis() to next_step
        """
        self.inductive.data_limitations = self.bodi.limitations.data_limitations
        self.inductive.not_normal = self.bodi.not_normal
        self.inductive.checklist = self.bodi.checklist
        self.close_buttons()
        self.boutils.change_cell_count = self.inductive.change_cell_count
        return self.inductive.start_inductive_analysis()

    def bring_order(self):
        """Runs the UI modules
        The different ui functions are run through a helper function
        that returns the name of the next function to be executed.
        First, the data import function."""

        next_step = 'new_data'
        # Import loop:
        while next_step == 'new_data':
            self.bodi = Bodi(
                self.boutils,
                self.bogui,
                self.boval,
                self.dataset_variables,
                self.ai_disabled,
                self.next_step
            )
            self.boutils.change_cell_count = self.bodi.change_cell_count
            next_step = self.get_next(self.ai.display_ai_popup)
            next_step = self.get_next(self.bodi.bodi, subroutines=[self.ai.toggle_ai])
            # Main analysis loop:
            while next_step == 'start_analysis':
                next_step = self.get_next(self.start_analysis)
                # Branching to deductive/inductive:
                if next_step == 'deductive_analysis':
                    next_step = self.get_next(self.start_deductive_analysis,
                                            subroutines=[self.ai.toggle_ai])
                elif next_step == 'inductive_analysis':
                    next_step = self.get_next(self.start_inductive_analysis,
                                            subroutines=[self.ai.toggle_ai])
                # New analysis/export to pdf-view:
                if next_step == 'analysis_done':
                    next_step = self.get_next(self.next_analysis.new_analysis_view)
            # Close:
            if next_step == 'exit':
                self.boutils.delete_cell_from_current(0)

    def get_next(self, function, subroutines=[]):
        """Runs a function, pauses execution until next_step is updated and then returns it.
        Args:
            function: a function to be executed
            subroutines[function]: list of external subroutine functions that
                                   may be called by function.
        Returns:
            next_step: name of the function to be executed after this"""
        function()
        with ui_events() as ui_poll:
            while self.next_step[0] is None:
                ui_poll(10)
                time.sleep(0.01)
        next_step = str(self.next_step[0])
        for sub in subroutines:
            if sub.__name__ == self.next_step[0]:
                self.next_step[0] = None
                next_step = self.get_next(sub, subroutines=[sub])
        self.next_step[0] = None
        return next_step

    def start_analysis(self):
        """Starts analysis phase"""
        self.deductive = Deductive(
            self.bogui,
            self.boutils,
            self.boval,
            self.ai_disabled,
            self.next_step
        )
        self.inductive = Inductive(
            self.bogui,
            self.boutils,
            self.boval,
            self.ai_disabled,
            self.next_step
        )

        self.buttons = self.bogui.init_buttons(self.button_list)
        display(widgets.HBox([self.buttons['deductive'], self.buttons['inductive']]))

    def __repr__(self):
        return ''
