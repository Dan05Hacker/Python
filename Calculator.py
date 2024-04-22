# Author: Dan Lai Kai Yi
# Email: danlaikaiyi@hotmail.com
# Date: 23/04/2024
# Description: This is a simple calculator application implemented using tkinter in Python. It provides basic arithmetic operations (+, -, *, /, %), square root (√), 
#              and square (x^2) functionalities. The calculator allows users to input expressions using both the keyboard and mouse clicks.
import tkinter as tk
import math

# Function to handle button clicks
def button_click(event):
    global evalBool, lastEvaluatedResult
    current_text = entry_var.get()
    lastEvaluatedResult = None
    
    if "Error" in current_text:
        current_text = ""
        entry_var.set("")
    
    # Check if an evaluation has occurred
    if evalBool:
        current_text = result_var.get()
        lastEvaluatedResult = current_text
        evalBool = False  # Reset the flag after using the result
    
    # Check if the button clicked is a number or decimal point
    if event.widget.cget("text").isdigit() or event.widget.cget("text") == ".":
        entry_var.set("0." if current_text == "0" and event.widget.cget("text") == "." else event.widget.cget("text") if current_text == "0" else current_text + event.widget.cget("text"))
    elif event.widget.cget("text") == "+/-": # Check if the button clicked is "+/-"
        entry_var.set("-0" if current_text == "" else "-" + current_text if current_text and (current_text[0] == "-" or current_text.isdigit()) else current_text[1:])
    elif event.widget.cget("text") in ["+", "-", "*", "/", "%"]: # Check if the button clicked is an arithmetic operator
        entry_var.set(current_text + event.widget.cget("text") if current_text and current_text[-1].isdigit() else current_text[:-1] + event.widget.cget("text") if current_text and current_text[-1] in ["+", "-", "*", "/","%"] else current_text)
    elif event.widget.cget("text") in ["1/x", "x^2", "sqrt"]: # Check if the button clicked is a special function: "1/x", "x^2", "sqrt"
        if lastEvaluatedResult: # If an evaluation has occurred, set current text to the last evaluated result
            current_text = lastEvaluatedResult
        entry_var.set({"1/x": f"1 / {current_text}", "sqrt": f"√({current_text})", "x^2": f"sqr({current_text})"}.get(event.widget.cget("text"), current_text))
        evaluate_expression()
        return
    evalBool = False

# Function to clear the entry field
def clear_entry(type):
    # Clear Entry (CE): Clears the current entry
    # Clear (C): Clears the entire calculation
    # Clear Operation (X): Clears the current operation (if any)
    current_text = entry_var.get()
    if type == "CE":
        entry_var.set(current_text[:-1]) if current_text and current_text != "Error" else result_var.set("0")
    elif type == "C":
        entry_var.set("")
        result_var.set("0")
    elif type == "X":
       entry_var.set(current_text[:-1]) if current_text and current_text != "Error" else entry_var.set("0")

# Function to evaluate the expression
def evaluate_expression():
    global evalBool
    try:
        expression = entry_var.get()
        if "sqr" in expression:
            expression = expression.replace("sqr", "math.pow").replace(")", ",2)")
        elif "√" in expression:
            expression = expression.replace("√", "math.sqrt")
        result = eval(expression)
        result_var.set(str(result))
        evalBool = True
    except ZeroDivisionError:
        entry_var.set("Error: Division by zero")
    except Exception as e:
        entry_var.set("Error")

# Create the main Tkinter window
root = tk.Tk()
root.title("Calculator")
root.geometry("600x600")

# Define StringVars & Create labels for the entry field and result display & Define the buttons for the calculator
entry_var = tk.StringVar(value="")
result_var = tk.StringVar(value="0")
expLabel = tk.Label(root, textvariable=entry_var, anchor="e", font=("Arial", 16),height=2).grid(row=0, column=0, columnspan=4, sticky="ew")
label = tk.Label(root, textvariable=result_var, anchor="e", font=("Arial", 40), height=2).grid(row=1, column=0, columnspan=4, sticky="ew")
buttons = [('%', 2, 0), ('CE', 2, 1), ('C', 2, 2), ('x', 2, 3),('1/x', 3, 0), ('x^2', 3, 1), ('sqrt', 3, 2), ('/', 3, 3),('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('*', 4, 3),('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('-', 5, 3),('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('+', 6, 3),('+/-', 7, 0), ('0', 7, 1), ('.', 7, 2), ('=', 7, 3)]

# Configure column and row weights for the layout
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
    root.grid_rowconfigure(i, weight=1)

# Create buttons and configure their actions
for (text, row, col) in buttons:
    button = tk.Button(root, text=text, font=("Arial", 20), height=2)
    button.grid(row=row, column=col, sticky="ew")
    if text == 'CE' or text == 'C' or  text == 'x':
        button.config(command=lambda t=text: clear_entry(t))
    elif text == '=':
        button.config(command=evaluate_expression)
    else:
        button.bind("<Button-1>", button_click)
evalBool = False
root.mainloop()