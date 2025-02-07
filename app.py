#----------------------------
#File Headers:
#----------------------------
#Shebang:
#!/usr/bin/env python


#Encoding:
# -*- coding: utf-8 -*-


#Docstring:
"""
Filename: app.py
Authors: PERVasive, Tsukiko
Date: 05/09/2018
Version: 1.0.0
Description:
    Omo Tracker keeps track of the fluids you drink, models your pee desperation over time,
    and tracks intentional pees and accidents to learn your personal bladder capacity.

License: The MIT License (MIT)
Contact: https://github.com/perv-asive, tsukiko1701@gmail.com
Dependencies: time, tkinter, tkinter.ttk, tkinter.messagebox, customtkinter, appdirs, csv, os, math, omo.py, stopwatch.py, timer.py
"""


#Dunders:
__author__ = "PERVasive, Tsukiko"
__copyright__ = "Copyright (c) 2018 perv-asive, Copyright (c) 2025 Tsukiko-030"
__credits__ = ["PERVasive", "Tsukiko"]
__license__ = "The MIT License (MIT)"
__version__ = "1.0.0"
__maintainer__ = "Tsukiko"
__email__ = "tsukiko1701@gmail.com"
__status__ = "Production"
#----------------------------




#----------------------------
#Import Statements:
#----------------------------
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import customtkinter as ctk
import appdirs
import csv
import os
import math
import omo
import stopwatch
import timer
#----------------------------




#---------------------------------------------------------------
#Set up save file storage paths:
#---------------------------------------------------------------
save_dir = appdirs.user_data_dir('Omo Trainer', 'PERVasive')
accident_log = os.path.join(save_dir, 'accidents.csv')
#---------------------------------------------------------------




#--------------------------------------
#Exterior Functions:
#--------------------------------------
def current_time_in_minutes_float():
    return time.time()/60.0
#--------------------------------------




#----------------------------------------------------------------------------------------------------------------------
#Main Class:
#----------------------------------------------------------------------------------------------------------------------
class App(object):
    def __init__(self):
        #Setup application window:
        self.root = ctk.CTk()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.title("Omo Tracker")
        

        #Try to load application icon:
        self.root.iconbitmap('icon.ico')


        #Initialize Drinker Class:
        self.drinker = omo.Drinker()


        #Initialize Hold Stopwatch:
        self.hold_stopwatch = stopwatch.Stopwatch()


        #Try to load hold history CSV
        self.load_data()


        # Initialize GUI property variables:
        self.desperation = tk.DoubleVar()
        self.drink_amount = tk.IntVar()
        self.drink_amount.set(500)
        self.bladder_text = tk.StringVar()
        self.drink_text = tk.StringVar()
        self.eta_text = tk.StringVar()
        self.hold_time_display_control_variable = tk.StringVar() # Variable for controling GUI's the displayed hold time.


        #GUI Styling:
        self.button_font = ctk.CTkFont("Arial", 12)


        #Display GUI Widgets:
        self.create_widgets()


        #Display GUI Menus:
        self.create_menus()


        #Initialize hold stopwatch:
        self.hold_time_display_control_variable.set("00:00:00") # Initialize the hold stopwatch display.
        self.hold_stopwatch.start_stopwatch() # Start the hold stopwatch.
        

        #Periodically check for GUI changes and update backend:
        self.poll()




    def create_widgets(self):
        # Set up customtkinter main frame:
        self.mainframe = ctk.CTkFrame(self.root)
        self.mainframe.grid(column = 0, row = 0, padx=3, pady=3, sticky = (tk.N, tk.W, tk.E, tk.S))
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)


        #Set up customtkinter widgets:
        self.bladder_bar = ctk.CTkProgressBar(self.mainframe, orientation = "vertical", variable=self.desperation, fg_color = "#ffb8bf", border_color = "#fb928e", progress_color = "#fff177")
        self.bladder_bar.grid(column=0, row=0, rowspan=2, sticky=(tk.N, tk.S))

        self.bladder_display = ctk.CTkLabel(self.mainframe, textvariable = self.bladder_text)
        self.bladder_display.grid(column = 0, row = 2, sticky = (tk.S, tk.W))

        self.eta_display = ctk.CTkLabel(self.mainframe, textvariable = self.eta_text)
        self.eta_display.grid(column = 1, row = 2, columnspan = 2, sticky = (tk.S, tk.W))

        self.drink_slider = ctk.CTkSlider(self.mainframe, orientation = "horizontal", width = 200,
                                      variable = self.drink_amount, command = self._quantize_drink, from_ = 100, to = 750, progress_color = "white", button_color = "#fff177", button_hover_color = "#dbc300")
        self.drink_slider.grid(column = 1, row = 0, columnspan = 2, sticky = (tk.W, tk.E))

        self.drink_display = ctk.CTkLabel(self.mainframe, textvariable=self.drink_text)
        self.drink_display.grid(column = 3, row = 0, sticky = (tk.E))
        self._quantize_drink()

        self.drink_button = ctk.CTkButton(self.mainframe, text = "Drink ☕", command = self.drink, font = self.button_font, border_width = 3, fg_color = "#ffb8bf", hover_color = "#fb928e", border_color = "#fb928e", text_color = "#fff177")
        self.drink_button.grid(column = 4, row = 0, sticky = (tk.E))

        self.pee_button = ctk.CTkButton(self.mainframe, text = "Pee 🚽", command = self.pee, font = self.button_font, border_width = 0, fg_color = "#00ff00", hover_color = "#1fc600", border_color = "#fff177", text_color = "white")
        self.pee_button.grid(column = 1, row = 1, sticky = (tk.W))

        self.accident_button = ctk.CTkButton(self.mainframe, text = "Accident 💦", command = self.accident, font = self.button_font, border_width = 0, fg_color = "#ff0000", hover_color = "#c80000", border_color = "#fff177", text_color = "white")
        self.accident_button.grid(column = 2, row = 1, sticky = (tk.E))

        self.hold_time_display = ctk.CTkLabel(self.mainframe, textvariable = self.hold_time_display_control_variable)
        self.hold_time_display.grid(column = 4, row = 2, sticky = (tk.S, tk.E))

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx = 5, pady = 5)




    def create_menus(self):
        self.menubar = tk.Menu(self.root, tearoff = 0)
        self.menu_main = tk.Menu(self.menubar, tearoff = 0)
        self.root.config(menu=self.menubar)
        self.menubar.add_cascade(menu = self.menu_main, label = 'Menu')
        self.menu_main.add_command(label = 'Reset Capacity Log', command = self.reset_capacity)




    def _quantize_drink(self, *args):
        value = self.drink_slider.get()
        quantized_val = int(round(value/50)*50)
        self.drink_amount.set(quantized_val)
        self.drink_text.set(str(quantized_val) + " mL")




    def _on_click(self, button):
        """Briefly disables a CustomTkinter button to avoid accidental double-clicking."""
        button.configure(state="disabled")  # Disable the button
        self.root.after(1000, lambda: button.configure(state="normal"))  # Re-enable the button after 1 second




    def drink(self):
        self.drinker.add_drink(current_time_in_minutes_float(), self.drink_amount.get())
        self._on_click(self.drink_button)




    def accident(self):
        # Store Urination and the fact that permission was allowed not in CSV:
        self.drinker.add_release(current_time_in_minutes_float(), False)


        # Reset Hold Timer:
        self.hold_stopwatch.reset_stopwatch()
        self.hold_stopwatch.start_stopwatch()


        #Briefly disable the I can't hold it button to avoid accidental double clicking:
        self._on_click(self.accident_button)




    def pee(self):
        # Store Urination and the fact that permission was allowed in CSV:
        self.drinker.add_release(current_time_in_minutes_float(), True)


        #Reset hold timer:
        self.hold_stopwatch.reset_stopwatch()
        self.hold_stopwatch.start_stopwatch()


        # Briefly disable the button to prevent accidental double clicking:
        self._on_click(self.pee_button)




    def poll(self):
        t = current_time_in_minutes_float()

        self.hold_time_display_control_variable.set(self.hold_stopwatch.output_elapsed_time())

        self.desperation.set(self.drinker.desperation(t))

        self.bladder_text.set(str(round(self.drinker.bladder(t))) + " mL/" + str(round(self.drinker.capacity)) + " mL")
        
        if self.drinker.eta:
            eta = math.ceil(self.drinker.eta - t)
            if eta > 1:
                self.eta_text.set("Potty emergency in: " + str(eta) + " minutes")
            elif eta == 1:
                self.eta_text.set("Potty emergency in: " + str(eta) + " minute")
            else:
                self.eta_text.set("Potty emergency now!")
        else:
            self.eta_text.set("")
        
        self.root.after(500, self.poll)




    def load_data(self):
        if os.path.exists(accident_log):
            with open(accident_log, 'r', newline='') as f:
                reader = csv.reader(f)
                self.drinker.old_accidents = [float(row[0]) for row in reader]




    def save_data(self):
        os.makedirs(os.path.dirname(accident_log), exist_ok=True)
        with open(accident_log, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([accident.amount] for accident in self.drinker.accidents)




    def reset_capacity(self):
        response = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the capacity log?")

        if response:  # User clicked "Yes".
            if os.path.exists(accident_log):
                os.remove(accident_log)
            self.drinker.old_accidents = []
            tk.messagebox.showinfo("Reset Successful", "Capacity has been reset.")
        else:  # User clicked "No"
            tk.messagebox.showinfo("Reset Canceled", "Capacity reset was canceled.")

#----------------------------------------------------------------------------------------------------------------------




#----------------------------
#Main Loop
#----------------------------
if __name__ == "__main__":
    app = App()
    app.root.mainloop()
    app.save_data()
#----------------------------
