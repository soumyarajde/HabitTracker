import tkinter as tk
from tkinter import ttk
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
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Habit Manager")
        self.build_HabitManager_tab(self.tab1)

        # Tab 2: Analyzer
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Analyzer")
    #     self.build_Analyzer_tab(self.tab2)

    # def on_click(self):
    #     print("Button was clicked!")

    def build_HabitManager_tab(self,gui):
        #create button to show Create New
        self.button1=ttk.Button(gui,text="Create New",command=self.show_create_fields)
        self.button1.pack(pady=10)
        #create view button
        self.button2=ttk.Button(gui,text="View",command=self.show_list)
        self.button2.pack(pady=10)
        self.container=ttk.Frame(gui)
        self.create_form=ttk.Frame(gui)
        
    def show_create_fields(self):
        self.container.pack_forget()
        #create labels and entry fields
        
        self.create_form.pack(pady=10)

        #Name
        ttk.Label(self.create_form,text='Name').grid(row=0,column=0,sticky="w")
        self.name_entry=ttk.Entry(self.create_form)
        self.name_entry.grid(row=0,column=1)

        #Description
        ttk.Label(self.create_form,text='Description').grid(row=1,column=0,sticky="w")
        self.desc_entry=ttk.Entry(self.create_form)
        self.desc_entry.grid(row=1,column=1)

        #Periodicity
        ttk.Label(self.create_form,text='Periodicity').grid(row=2,column=0,sticky="w")
        self.period_entry=ttk.Entry(self.create_form)
        self.period_entry.grid(row=2,column=1)

        #create button
        create_button=ttk.Button(self.create_form,text="Create",command=self.create_habit)
        create_button.grid(row=3,columnspan=2,pady=10)

    def create_habit(self):
        name=self.name_entry.get()
        desc=self.desc_entry.get()
        period=self.period_entry.get()
        # Input validation to be done
        self.manager.create_habit(name=name,description=desc,periodicity=period)

    def show_list(self):
        #create a container frame to hold all habits.
        self.create_form.pack_forget()
        
        self.container.pack(padx=10,pady=10)
        self.show_habits()

    def show_habits(self):
        #clear the container
        for widget in self.container.winfo_children():
            widget.destroy()
        # Show the names of habits
        for name,habit in self.manager.habits.items():
            row=tk.Frame(self.container)
            row.pack(fill="x",pady=2)
            tk.Label(row,text=habit.name.upper(),width='20',anchor="w").pack(side="left")
            # create check off button
            tk.Button(row,text='Check off',command=lambda name:self.check_off(name)).pack(side="right")
            #Create Delete button
            tk.Button(row,text='Delete',command=lambda name:self.delete_habit(name)).pack(side="right")
            #Create Activate/Deactivate button
            status="Activate" if not habit.active else "Deactivate"
            tk.Button(row,text=status,command=lambda name:self.status_change_habit(name)).pack(side="right")


        def delete_habit(self,name):
            self.manager.delete_habit(name=name)
            self.show_habits()

        def check_off(self,name):
            self.manager.check_off(name)
            self.show_habits()

        def status_change_habit(name):
            if self.manager.habits[name].active:
                self.manager.deactivate_habit(name)
            else:
                self.manager.activate_habit(name)
            self.show_habits()
        

        

        

    

if __name__=='__main__':
    gui=tk.Tk()
    app=ApplicationGui(gui)
    gui.mainloop()
