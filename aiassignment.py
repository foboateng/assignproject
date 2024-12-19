import customtkinter as ctk
from tkinter import messagebox, simpledialog
from owlready2 import *
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the ontology
onto = get_ontology(r"C:\Users\User\OneDrive\Assignment\ChemicalReactionsOntology.owl").load()

class ChemistryITS:
    def __init__(self, master):
        self.master = master
        master.title("Chemistry Intelligent Tuturing System")
        master.geometry("1000x700")

        # Set the appearance mode and color theme
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Create main frame
        self.main_frame = ctk.CTkFrame(master)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create notebook (tabbed interface)
        self.notebook = ctk.CTkTabview(self.main_frame)
        self.notebook.pack(fill="both", expand=True)

        # Create tabs
        self.elements_frame = self.notebook.add("Elements")
        self.compounds_frame = self.notebook.add("Compounds")
        self.reactions_frame = self.notebook.add("Reactions")
        self.search_frame = self.notebook.add("Search")
        self.quiz_frame = self.notebook.add("Quiz")
        self.stats_frame = self.notebook.add("Stats")

        self.create_elements_tab()
        self.create_compounds_tab()
        self.create_reactions_tab()
        self.create_search_tab()
        self.create_quiz_tab()
        self.create_stats_tab()

        # Create footer
        self.footer = ctk.CTkLabel(master, text="© Boateng Frank 230279339 ITS")
        self.footer.pack(pady=10)

    def create_elements_tab(self):
        self.elements_scroll_frame = ctk.CTkScrollableFrame(self.elements_frame, width=300)
        self.elements_scroll_frame.pack(side="left", pady=10, padx=10, fill="both", expand=True)

        self.refresh_elements_list()

        add_element_btn = ctk.CTkButton(self.elements_frame, text="Add New Element", command=self.add_new_element)
        add_element_btn.pack(pady=10)

    def refresh_elements_list(self):
        for widget in self.elements_scroll_frame.winfo_children():
            widget.destroy()
        
        for element in onto.Element.instances():
            btn = ctk.CTkButton(self.elements_scroll_frame, text=element.name, 
                                command=lambda e=element: self.show_element_details(e))
            btn.pack(pady=2, padx=5, fill="x")

    def show_element_details(self, element):
        details = f"Name: {element.name}\n"
        details += f"Chemical Formula: {element.hasChemicalFormula[0]}\n"
        details += f"Atomic Number: {element.hasAtomicNumber[0]}"
        messagebox.showinfo("Element Details", details)

    def add_new_element(self):
        name = simpledialog.askstring("New Element", "Enter element name:")
        if name:
            formula = simpledialog.askstring("New Element", "Enter chemical formula:")
            atomic_number = simpledialog.askinteger("New Element", "Enter atomic number:")
            
            with onto:
                new_element = onto.Element(name)
                new_element.hasChemicalFormula = [formula]
                new_element.hasAtomicNumber = [atomic_number]
            
            onto.save()
            self.refresh_elements_list()

    def create_compounds_tab(self):
        self.compounds_scroll_frame = ctk.CTkScrollableFrame(self.compounds_frame, width=300)
        self.compounds_scroll_frame.pack(side="left", pady=10, padx=10, fill="both", expand=True)

        for compound in onto.Compound.instances():
            btn = ctk.CTkButton(self.compounds_scroll_frame, text=compound.name, 
                                command=lambda c=compound: self.show_compound_details(c))
            btn.pack(pady=2, padx=5, fill="x")

    def show_compound_details(self, compound):
        details = f"Name: {compound.name}\n"
        details += f"Chemical Formula: {compound.hasChemicalFormula[0]}\n"
        details += "Consists of: " + ", ".join([e.name for e in compound.ConsistsOf])
        messagebox.showinfo("Compound Details", details)

    def create_reactions_tab(self):
        self.reactions_scroll_frame = ctk.CTkScrollableFrame(self.reactions_frame, width=300)
        self.reactions_scroll_frame.pack(side="left", pady=10, padx=10, fill="both", expand=True)

        for reaction in onto.ChemicalReaction.instances():
            btn = ctk.CTkButton(self.reactions_scroll_frame, text=reaction.name, 
                                command=lambda r=reaction: self.show_reaction_details(r))
            btn.pack(pady=2, padx=5, fill="x")

    def show_reaction_details(self, reaction):
        details = f"Name: {reaction.name}\n"
        details += "Reactants: " + ", ".join([r.name for r in reaction.hasReactant]) + "\n"
        details += "Products: " + ", ".join([p.name for p in reaction.hasProduct])
        messagebox.showinfo("Reaction Details", details)

    def create_search_tab(self):
        search_label = ctk.CTkLabel(self.search_frame, text="Search for chemical concept:")
        search_label.pack(pady=10)
        
        self.search_entry = ctk.CTkEntry(self.search_frame, width=300)
        self.search_entry.pack(pady=10)
        
        search_button = ctk.CTkButton(self.search_frame, text="Search", command=self.perform_search)
        search_button.pack(pady=10)
        
        self.search_results_frame = ctk.CTkScrollableFrame(self.search_frame, width=400, height=300)
        self.search_results_frame.pack(pady=10, padx=10, fill="both", expand=True)

    def perform_search(self):
        query = self.search_entry.get().lower()
        for widget in self.search_results_frame.winfo_children():
            widget.destroy()
        
        for cls in [onto.Element, onto.Compound, onto.ChemicalReaction]:
            for instance in cls.instances():
                if query in instance.name.lower():
                    btn = ctk.CTkButton(self.search_results_frame, 
                                        text=f"{cls.__name__}: {instance.name}",
                                        command=lambda i=instance: self.show_instance_details(i))
                    btn.pack(pady=2, padx=5, fill="x")

    def show_instance_details(self, instance):
        if isinstance(instance, onto.Element):
            self.show_element_details(instance)
        elif isinstance(instance, onto.Compound):
            self.show_compound_details(instance)
        elif isinstance(instance, onto.ChemicalReaction):
            self.show_reaction_details(instance)

    def create_quiz_tab(self):
        self.quiz_question = ctk.CTkLabel(self.quiz_frame, text="", font=("Arial", 16))
        self.quiz_question.pack(pady=20)
        
        self.quiz_entry = ctk.CTkEntry(self.quiz_frame, width=300)
        self.quiz_entry.pack(pady=10)
        
        check_answer_btn = ctk.CTkButton(self.quiz_frame, text="Check Answer", command=self.check_quiz_answer)
        check_answer_btn.pack(pady=10)
        
        new_question_btn = ctk.CTkButton(self.quiz_frame, text="New Question", command=self.generate_quiz_question)
        new_question_btn.pack(pady=10)
        
        self.generate_quiz_question()

    def generate_quiz_question(self):
        element = random.choice(list(onto.Element.instances()))
        self.current_quiz_element = element
        self.quiz_question.configure(text=f"What is the chemical formula for {element.name}?")
        self.quiz_entry.delete(0, "end")

    def check_quiz_answer(self):
        user_answer = self.quiz_entry.get().strip()
        correct_answer = self.current_quiz_element.hasChemicalFormula[0]
        
        if user_answer.lower() == correct_answer.lower():
            messagebox.showinfo("Quiz Result", "Correct!")
        else:
            messagebox.showinfo("Quiz Result", f"Incorrect. The correct answer is {correct_answer}.")

    def create_stats_tab(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        entity_types = ['Elements', 'Compounds', 'Reactions']
        counts = [
            len(onto.Element.instances()),
            len(onto.Compound.instances()),
            len(onto.ChemicalReaction.instances())
        ]
        ax.bar(entity_types, counts)
        ax.set_ylabel('Count')
        ax.set_title('Distribution of Chemical Entities')

        canvas = FigureCanvasTkAgg(fig, master=self.stats_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

root = ctk.CTk()
my_gui = ChemistryITS(root)
root.mainloop()

