import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from habittracker.habitmanager import HabitManager
from habittracker.analyzer import HabitAnalyzer

class ApplicationGui:
    def __init__(self,gui):
        gui.title("Habit Tracker")
        self.manager=HabitManager()
        self.analyzer=HabitAnalyzer()

        #create a notebook (tab manager)
        self.notebook = ttk.Notebook(gui)
        self.notebook.pack(expand=True, fill='both')

        # Tab 1: Habit Manager
        self.manager_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.manager_tab, text="Habit Manager")
        self.build_habit_manager_tab(self.manager_tab)

        # Tab 2: Analyzer
        self.analyzer_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analyzer_tab, text="Analyzer")
        self.build_analyzer_tab(self.analyzer_tab)

    def on_click(self):
        print("Button was clicked!")

    def build_habit_manager_tab(self,gui):
        #create button to show Create New
        self.btn_create_habit=ttk.Button(gui,text="Create New",command=self.on_click_btn_create_habit)
        self.btn_create_habit.pack(pady=10)
        #create view button
        self.btn_view_habit=ttk.Button(gui,text="View",command=self.on_click_btn_view_habit)
        self.btn_view_habit.pack(pady=10)
        self.habit_list_container=ttk.Frame(gui)
        self.create_form_fields=ttk.Frame(gui)

    def on_click_btn_create_habit(self):
        self.habit_list_container.pack_forget()
        #create labels and entry fields
        
        self.create_form_fields.pack(pady=10)

        #Name
        ttk.Label(self.create_form_fields,text='Name').grid(row=0,column=0,sticky="w")
        self.name_entry=ttk.Entry(self.create_form_fields)
        self.name_entry.grid(row=0,column=1)

        #Description
        ttk.Label(self.create_form_fields,text='Description').grid(row=1,column=0,sticky="w")
        self.desc_entry=ttk.Entry(self.create_form_fields)
        self.desc_entry.grid(row=1,column=1)

        #label Periodicity
        ttk.Label(self.create_form_fields,text='Periodicity').grid(row=2,column=0,sticky="w")
        # pariodicity values drop down
        options=["daily","weekly"]
        self.period_drop_down=ttk.Combobox(self.create_form_fields,values=options,state="readonly")
        self.period_drop_down.current(0)
        self.period_drop_down.grid(row=2,column=1)

        #create button
        self.btn_create=ttk.Button(self.create_form_fields,text="Create",command=self.create_habit)
        self.btn_create.grid(row=3,columnspan=2,pady=10)
    
    def create_habit_success_msg(self):
        messagebox.showinfo("Greetings!","Habit created successfully.")
    
    def create_habit_error_msg(self):
        messagebox.showerror("Error","Please fill all the fields.")

    def create_habit(self):
        name=self.name_entry.get()
        desc=self.desc_entry.get()
        period=self.period_drop_down.get()
        #input validation
        if not name or not desc or not period:
            self.create_habit_error_msg()
        else:
            self.manager.create_habit(name=name,description=desc,periodicity=period)
            self.create_habit_success_msg()
        self.create_form_fields.pack_forget()

    def on_click_btn_view_habit(self):
        #create a container frame to hold all habits.
        self.create_form_fields.pack_forget()
        self.habit_list_container.pack(padx=10,pady=10)
        self.show_habits()

    def show_habits(self):
        #clear the container
        for widget in self.habit_list_container.winfo_children():
            widget.destroy()
        # Show the names of habits
        for name,habit in self.manager.habits.items():
            row=tk.Frame(self.habit_list_container)
            row.pack(fill="x",pady=2)
            tk.Label(row,text=habit.name.upper(),width='20',anchor="w").pack(side="left")
            # create check off button
            tk.Button(row,text='Check off',command=lambda name=name:self.check_off(name)).pack(side="right")
            #Create Delete button
            tk.Button(row,text='Delete',command=lambda name=name:self.delete_habit(name)).pack(side="right")
            #Create Activate/Deactivate button
            status="Activate" if not habit.active else "Deactivate"
            tk.Button(row,text=status,command=lambda name=name:self.status_change_habit(name)).pack(side="right")

    def delete_habit(self,name):
        print("Delete")
        self.manager.delete_habit(name=name)
        self.show_habits()

    def check_off(self,name):
        self.manager.check_off(name)
        self.show_habits()

    def status_change_habit(self,name):
        if self.manager.habits[name].active:
            self.manager.deactivate_habit(name)
        else:
            self.manager.activate_habit(name)
        self.show_habits()

   
        
    def build_analyzer_tab(self,gui):
        #create a drop down
        options=["Current streak","Longest streak","Longest streak of all habits","Weekly Habits","Daily Habits","Currently tracked habits"]
        self.analysis_drop_down=ttk.Combobox(gui,values=options,state="readonly")
        self.analysis_drop_down.current(0)
        self.analysis_drop_down.pack(pady=10)
        #create a submit button
        btn_submit=ttk.Button(gui,text="Submit",command=self.on_click_btn_submit)
        btn_submit.pack

        # analysis_drop_down.bind("<<ComboboxSelected>>",on_select_analysis)
    def on_click_btn_submit(self):
        selected=self.analysis_drop_down.get()
        # if selected==options[0]:


    

        

        

    

if __name__=='__main__':
    gui=tk.Tk()
    app=ApplicationGui(gui)
    gui.mainloop()
