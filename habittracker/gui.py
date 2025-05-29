from datetime import date
import tkinter as tk
from tkinter import ttk
from habittracker.constants import Periodicity, AnalyzerOptions
from tkinter import messagebox
from habittracker.habitmanager import HabitManager
from habittracker.analyzer import HabitAnalyzer
import logging

logger = logging.getLogger(__name__)


class ApplicationGui:
    """
    Represents the graphical user interface.
    Attributes:
        manager:HabitManager object
        analyzer:HabitAnalyzer object
    """

    def __init__(self, gui):
        """
        Initializes ApplicationGui object by setting up the main window.
        set up habit management and analysis components.
        """
        # set the window title to 'Habit Tracker'
        gui.title("Habit Tracker")
        # set size of the window
        gui.geometry("400x300")
        # Create a HabitManager instance to manage habits.
        self.manager = HabitManager()
        # Create a HabitAnalyzer instance to analyze habits.
        self.analyzer = HabitAnalyzer(self.manager)

        # create a notebook (tab manager) to set up tabs.
        self.notebook = ttk.Notebook(gui)
        self.notebook.pack(expand=True, fill="both")

        # Tab 1:Welcome
        welcome_tab = ttk.Frame(self.notebook)
        self.notebook.add(welcome_tab, text="Welcome")
        self.build_welcome_tab(welcome_tab)

        # Tab 2: Habit Manager
        manager_tab = ttk.Frame(self.notebook)
        self.notebook.add(manager_tab, text="Habit Manager")
        self.build_habit_manager_tab(manager_tab)

        # Tab 3: Analyzer
        analyzer_tab = ttk.Frame(self.notebook)
        self.notebook.add(analyzer_tab, text="Analyzer")
        self.build_analyzer_tab(analyzer_tab)

    def build_welcome_tab(self, tab):
        """
        Method to define the welcome tab.
        It creates a top label to show welcome message,
        two lists to show pending daily and weekly and
        labels for each list.
        Args:
            tab:reference to Tk frame
        """
        # Top label
        tk.Label(tab, text="Hi, Welcome!", font=("Helvetica", 20, "bold")).pack(pady=50)
        # create a frame to hold pending habit lists.
        self.pending_list_frame = tk.Frame(tab)
        self.pending_list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        # Pending for today list box(left)
        self.pending_today = tk.Frame(self.pending_list_frame)
        self.pending_today.pack(side="left", fill="both", expand=True, padx=(0, 10))

        label_pending_today = tk.Label(
            self.pending_today, text="Pending Today", font=("Helvetica", "12")
        )
        label_pending_today.pack(anchor="w")
        self.listbox_pending_today = tk.Listbox(self.pending_today)
        pending_habits = self.manager.view_pending_habits_daily(date.today())
        for habit in pending_habits:
            self.listbox_pending_today.insert(tk.END, habit.upper())
            self.listbox_pending_today.pack(fill="both", expand=True)
        # Pending for this week list box(right)
        self.pending_this_week = tk.Frame(self.pending_list_frame)
        self.pending_this_week.pack(side="left", fill="both", expand=True, padx=(0, 10))
        label_pending_this_week = tk.Label(
            self.pending_this_week, text="Pending This Week", font=("Helvetica", "12")
        )
        label_pending_this_week.pack(anchor="w")
        self.listbox_pending_this_week = tk.Listbox(self.pending_this_week)
        pending_habits = self.manager.view_pending_habits_weekly(date.today())
        for habit in pending_habits:
            self.listbox_pending_this_week.insert(tk.END, habit.upper())
            self.listbox_pending_this_week.pack(fill="both", expand=True)

    def build_habit_manager_tab(self, tab):
        """
        Method to define the habit manager tab.Creates two buttons 'create new' and view.
        Setting up frames for create form fields and list of habits container which appers
        on clicking create new and view buttons respectively.
        Args:
            tab:reference to Tk frame
        """

        # create button to show Create New
        self.btn_create_habit = ttk.Button(
            tab, text="Create New", command=self.on_click_btn_create_new_habit
        )
        self.btn_create_habit.pack(pady=30)
        # create view button
        self.btn_view_habit = ttk.Button(
            tab, text="View", command=self.on_click_btn_view_habit
        )
        self.btn_view_habit.pack()
        self.habit_list_container = ttk.Frame(tab)
        self.create_form_fields = ttk.Frame(tab)

    def on_click_btn_create_new_habit(self):
        """
        Method to define the action on clicking create new button.
        It displays input fields for habit name,description and periodicity
        and a create button to create habit.
        """
        self.habit_list_container.pack_forget()
        # create labels and entry fields
        self.create_form_fields.pack(pady=10)

        # Name
        ttk.Label(self.create_form_fields, text="Name").grid(
            row=0, column=0, sticky="w"
        )
        self.name_entry = ttk.Entry(self.create_form_fields, width=30)
        self.name_entry.grid(row=0, column=1)

        # Description
        ttk.Label(self.create_form_fields, text="Description").grid(
            row=1, column=0, sticky="w"
        )
        self.desc_entry = ttk.Entry(self.create_form_fields, width=30)
        self.desc_entry.grid(row=1, column=1)

        # label Periodicity
        ttk.Label(self.create_form_fields, text="Periodicity").grid(
            row=2, column=0, sticky="w"
        )

        # periodicity values drop down
        self.period_drop_down = ttk.Combobox(
            self.create_form_fields,
            values=[p.value for p in Periodicity],
            state="readonly",
            width=30,
        )
        self.period_drop_down.current(0)
        self.period_drop_down.grid(row=2, column=1)

        # create button
        self.btn_create = ttk.Button(
            self.create_form_fields, text="Create", command=self.create_habit
        )
        self.btn_create.grid(row=3, columnspan=2, pady=10)

    def create_habit_error_msg(self):
        messagebox.showerror("Error", "Please fill all the fields.")

    def create_habit(self):
        """Method to create a habit with given input details."""
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        period = self.period_drop_down.get()
        # input validation
        if not name.strip() or not desc.strip() or not period:
            messagebox.showerror("Error", "Please fill all the fields.")
        else:
            try:
                self.manager.create_habit(
                    name=name,
                    description=desc,
                    periodicity=Periodicity(period),
                    creation_date=date.today(),
                )
                messagebox.showinfo("Success", f"Habit {name} created successfully.")
            except ValueError as e:
                messagebox.showerror("Error", e)
        self.create_form_fields.pack_forget()

    def on_click_btn_view_habit(self):
        # create a container frame to hold all habits.
        self.create_form_fields.pack_forget()
        self.habit_list_container.pack(padx=10, pady=10)
        self.show_habits()

    def show_habits(self):
        # clear the container
        for widget in self.habit_list_container.winfo_children():
            widget.destroy()
        # Show the names of habits
        for name, habit in self.manager.habits.items():
            row = tk.Frame(self.habit_list_container)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=habit.name.upper(), width="10", anchor="w").pack(
                side="left"
            )
            # create check off button
            tk.Button(
                row,
                text="Check off",
                width="10",
                command=lambda name=name: self.check_off(name),
            ).pack(side="right")
            # Create Delete button
            tk.Button(
                row,
                text="Delete",
                width="10",
                command=lambda name=name: self.delete_habit(name),
            ).pack(side="right")
            # Create Activate/Deactivate button
            status = "Activate" if not habit.active else "Deactivate"
            tk.Button(
                row,
                text=status,
                width="10",
                command=lambda name=name: self.status_change_habit(name),
            ).pack(side="right")

    def delete_habit(self, name):
        self.manager.delete_habit(name=name)
        self.show_habits()

    def check_off(self, name):
        try:
            self.manager.check_off(name, date.today())
            self.show_habits()
        except ValueError as e:
            messagebox.showerror("Error", e)

    def status_change_habit(self, name):
        if self.manager.habits[name].active:
            self.manager.deactivate_habit(name)
        else:
            self.manager.activate_habit(name)
        self.show_habits()

    def build_analyzer_tab(self, tab):
        """
        Method to define the analyzer tab.
        Args:
            tab:reference to Tk frame
        """
        # create a drop down
        analysis_drop_down_width = max(len(option.value) for option in AnalyzerOptions)
        self.analysis_drop_down = ttk.Combobox(
            tab,
            values=[option.value for option in AnalyzerOptions],
            width=analysis_drop_down_width,
            state="readonly",
        )
        self.analysis_drop_down.current(0)
        self.analysis_drop_down.pack(pady=10)
        self.analysis_drop_down.bind("<<ComboboxSelected>>", self.on_select_analysis)
        # create another drop down to show habit list.
        # This drop down is hidden initially.
        self.habit_list_drop_down = ttk.Combobox(tab, state="readonly")
        self.habit_list_drop_down.pack(pady=10)
        self.habit_list_drop_down.pack_forget()
        # create a label to display result of streak calculation.This is also hidden initially
        self.result_label = ttk.Label(tab, text=f"")
        self.result_label.pack_forget()
        # create a list box to disply list of values in the result.This is hidden initially.
        self.habits_list = tk.Listbox(tab, font=("Courier New", 12), width=50)

    def on_select_analysis(self, evnt):
        """Method defining the action on selecting analysis options from the drop down."""
        # store input from analysis drop down selection
        selection = self.analysis_drop_down.get()
        # convert to enum
        selected_analysis = AnalyzerOptions(selection)
        # create option values for habit drop down list
        # to disply when analysis selcetion is for current streak or longest streak

        habits = [name.upper() for name, habit in self.manager.habits.items()]
        habit_drop_down_options = ["Select a habit"] + habits
        width_drop_down = max(len(option) for option in habit_drop_down_options)
        # set width of drop down to max length of otion

        if selected_analysis == AnalyzerOptions.CURRENT_STREAK:
            self.habits_list.pack_forget()
            self.result_label.pack_forget()
            self.habit_list_drop_down["values"] = habit_drop_down_options
            self.habit_list_drop_down["width"] = width_drop_down
            self.habit_list_drop_down.current(0)
            self.habit_list_drop_down.pack()
            self.habit_list_drop_down.bind("<<ComboboxSelected>>", self.show_streak)
        elif selected_analysis == AnalyzerOptions.CURRENTLY_TRACKED_HABITS:
            self.habit_list_drop_down.pack_forget()
            self.result_label.pack_forget()
            self.show_currently_tracked_habits()
        elif selected_analysis == AnalyzerOptions.DAILY_HABITS:
            self.result_label.pack_forget()
            self.habit_list_drop_down.pack_forget()
            self.show_daily_habits()
        elif selected_analysis == AnalyzerOptions.WEEKLY_HABITS:
            self.result_label.pack_forget()
            self.habit_list_drop_down.pack_forget()
            self.show_weekly_habits()
        elif selected_analysis == AnalyzerOptions.LONGEST_STREAK:
            self.habits_list.pack_forget()
            self.result_label.pack_forget()
            self.habit_list_drop_down["values"] = habit_drop_down_options
            self.habit_list_drop_down.current(0)
            self.habit_list_drop_down.pack()
            self.habit_list_drop_down.bind(
                "<<ComboboxSelected>>", self.show_longest_streak
            )
        elif selected_analysis == AnalyzerOptions.LONGEST_STREAK_ALL:
            self.habit_list_drop_down.pack_forget()
            self.result_label.pack_forget()
            self.show_longest_streak_all()
        else:
            self.habit_list_drop_down.pack_forget()
            self.result_label.pack_forget()
            self.habits_list.pack_forget()

    def show_streak(self, evnt):
        """Method to show current streak of selected habit."""
        habit_name = self.habit_list_drop_down.get()
        try:
            current_streak = self.analyzer.get_streak(
                name=habit_name, calculation_date=date.today()
            )
            self.result_label.configure(
                text=f"Current streak of {habit_name} : {current_streak}",
                foreground="green",
            )
            self.result_label.pack(pady=50)
        except ValueError:
            self.result_label.configure(
                text=f"Select a valid Habit!",
                font=("Times New Roman", 18, "bold"),
                foreground="red",
            )
            self.result_label.pack(pady=50)

    def show_longest_streak(self, evnt):
        """Method to show longest streak of selected habit."""
        habit_name = self.habit_list_drop_down.get()
        try:
            longest_streak = self.analyzer.get_longest_streak(name=habit_name)
            self.result_label.configure(
                text=f"Longest streak of {habit_name} : {longest_streak}",
                foreground="green",
            )
            self.result_label.pack(pady=50)
        except ValueError as e:
            self.result_label.configure(text=f"Select a valid Habit.", foreground="red")
            self.result_label.pack(pady=50)

    def show_currently_tracked_habits(self):
        """Method to show currently tracked habits."""
        currently_tracked_habits = self.analyzer.get_currently_tracked_habits()
        self.habits_list.delete(0, tk.END)
        for habit in currently_tracked_habits:
            self.habits_list.insert(tk.END, habit.upper())
        self.habits_list.pack()

    def show_daily_habits(self):
        """Method to show list of daily habits."""
        habits = self.analyzer.get_habits_with_same_period(period=Periodicity.DAILY)
        self.habits_list.delete(0, tk.END)
        for habit in habits:
            self.habits_list.insert(tk.END, habit.upper())
        self.habits_list.pack()

    def show_weekly_habits(self):
        """Method to show list of weekly habits."""
        habits = self.analyzer.get_habits_with_same_period(period=Periodicity.WEEKLY)
        self.habits_list.delete(0, tk.END)
        for habit in habits:
            self.habits_list.insert(tk.END, habit.upper())
        self.habits_list.pack()

    def show_longest_streak_all(self):
        """Method to disply all habits and their longest streak"""
        longest_streak = self.analyzer.get_longest_streak_all()
        self.habits_list.delete(0, tk.END)
        header = f"{'Habit'.ljust(20)}   {'Longest Streak'.rjust(10)}"
        self.habits_list.insert("end", header)
        self.habits_list.insert("end", "-" * 50)
        for habit, streak in longest_streak.items():
            line = f"{habit.upper().ljust(20)}   {str(streak).rjust(10)}"
            self.habits_list.insert("end", line)
        self.habits_list.pack()
