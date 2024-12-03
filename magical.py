import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import math
import matplotlib.pyplot as plt
import numpy as np

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scientific Calculator")
        self.root.geometry("500x700")
        self.root.configure(bg='#2c3e50')
        
        # Initialize calculator state
        self.current = ""
        self.result = ""
        self.operation = None
        self.new_number = True
        self.memory = 0
        
        # Main Frame Setup
        self.main_frame = ttk.Frame(root, padding="15")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.configure(style='Dark.TFrame')
        
        # Style configuration
        self.configure_styles()
        
        # UI component creation
        self.create_display()
        self.create_button_frames()
        
        # Window grid configuration
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        # Keyboard bindings for ease of use
        self.bind_keyboard()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')  # Modern theme
        
        # Frame styles
        style.configure('Dark.TFrame', background='#2c3e50')
        
        # Display styles
        style.configure('Display.TEntry', 
            font=('Consolas', 28), 
            foreground='white', 
            background='#34495e', 
            fieldbackground='#34495e'
        )
        
        # Button styles
        style.configure('Calculator.TButton', 
            font=('Arial', 12), 
            background='#3498db', 
            foreground='white'
        )
        style.map('Calculator.TButton', 
            background=[('active', '#2980b9')],
            foreground=[('active', 'white')]
        )
        
        style.configure('Operation.TButton', 
            font=('Arial', 10), 
            background='#2ecc71', 
            foreground='white'
        )
        style.map('Operation.TButton', 
            background=[('active', '#27ae60')],
            foreground=[('active', 'white')]
        )
        
        style.configure('Memory.TButton', 
            font=('Arial', 10), 
            background='#e74c3c', 
            foreground='white'
        )
        style.map('Memory.TButton', 
            background=[('active', '#c0392b')],
            foreground=[('active', 'white')]
        )
        
        style.configure('Equals.TButton', 
            font=('Arial', 14, 'bold'), 
            background='#f39c12', 
            foreground='white'
        )
        style.map('Equals.TButton', 
            background=[('active', '#d35400')],
            foreground=[('active', 'white')]
        )

    def create_display(self):
        display_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        display_frame.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")
        
        self.display = ttk.Entry(
            display_frame,
            justify="right",
            style='Display.TEntry',
            font=('Consolas', 28)
        )
        self.display.pack(fill='x', padx=5, pady=5)
        self.display.insert(0, "0")

    def create_button_frames(self):
        self.create_memory_buttons()
        self.create_scientific_buttons()
        self.create_main_buttons()
        self.create_plotting_button()

    def create_memory_buttons(self):
        memory_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        memory_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", pady=5)
        
        memory_buttons = [
            ('MC', self.memory_clear),
            ('MR', self.memory_recall),
            ('M+', self.memory_add),
            ('M-', self.memory_subtract)
        ]
        
        for i, (text, cmd) in enumerate(memory_buttons):
            btn = ttk.Button(memory_frame, text=text, style='Memory.TButton', command=cmd)
            btn.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")
            memory_frame.grid_columnconfigure(i, weight=1)

    def create_scientific_buttons(self):
        scientific_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        scientific_frame.grid(row=2, column=0, columnspan=5, sticky="nsew", pady=5)
        
        scientific_buttons = [
            ('sin', lambda: self.scientific_operation('sin')),
            ('cos', lambda: self.scientific_operation('cos')),
            ('tan', lambda: self.scientific_operation('tan')),
            ('√', lambda: self.scientific_operation('sqrt')),
            ('x²', lambda: self.scientific_operation('square')),
            ('log', lambda: self.scientific_operation('log')),
            ('ln', lambda: self.scientific_operation('ln')),
            ('exp', lambda: self.scientific_operation('exp')),
            ('1/x', lambda: self.scientific_operation('reciprocal')),
            ('∛', lambda: self.scientific_operation('cube_root'))
        ]
        
        for i, (text, command) in enumerate(scientific_buttons):
            btn = ttk.Button(scientific_frame, text=text, style='Operation.TButton', command=command)
            btn.grid(row=(i//5), column=(i%5), padx=2, pady=2, sticky="nsew")
            scientific_frame.grid_columnconfigure((i%5), weight=1)
            scientific_frame.grid_rowconfigure((i//5), weight=1)

    def create_plotting_button(self):
        plotting_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        plotting_frame.grid(row=4, column=0, columnspan=5, sticky="nsew", pady=5)
        
        plot_btn = ttk.Button(plotting_frame, text="Plot Linear Equation", style='Operation.TButton', command=self.plot_linear_equation)
        plot_btn.pack(fill='x', padx=5, pady=5)

    def create_main_buttons(self):
        buttons_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        buttons_frame.grid(row=3, column=0, columnspan=5, sticky="nsew")
        
        button_layout = [
            ['7', '8', '9', '/', 'CE'],
            ['4', '5', '6', '*', '←'],
            ['1', '2', '3', '-', '±'],
            ['0', '.', 'π', '+', '=']
        ]
        
        for i, row in enumerate(button_layout):
            for j, text in enumerate(row):
                style = 'Equals.TButton' if text == '=' else 'Calculator.TButton'
                btn = ttk.Button(buttons_frame, text=text, style=style, command=lambda t=text: self.button_click(t))
                btn.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
                buttons_frame.grid_columnconfigure(j, weight=1)
            buttons_frame.grid_rowconfigure(i, weight=1)

    def bind_keyboard(self):
        self.root.bind('<Return>', lambda event: self.button_click('='))
        self.root.bind('<BackSpace>', lambda event: self.button_click('←'))
        self.root.bind('<Escape>', lambda event: self.button_click('CE'))
        for key in '0123456789.+-*/':
            self.root.bind(key, lambda event, k=key: self.button_click(k))

    def memory_clear(self):
        self.memory = 0
        messagebox.showinfo("Memory", "Memory cleared")

    def memory_recall(self):
        self.update_display(str(self.memory))

    def memory_add(self):
        try:
            current_value = float(self.display.get())
            self.memory += current_value
            messagebox.showinfo("Memory", f"Added {current_value} to memory")
        except ValueError:
            messagebox.showerror("Error", "Invalid number")

    def memory_subtract(self):
        try:
            current_value = float(self.display.get())
            self.memory -= current_value
            messagebox.showinfo("Memory", f"Subtracted {current_value} from memory")
        except ValueError:
            messagebox.showerror("Error", "Invalid number")

    def scientific_operation(self, operation):
        try:
            current = float(self.display.get())
            result = {
                'sin': math.sin(math.radians(current)),
                'cos': math.cos(math.radians(current)),
                'tan': math.tan(math.radians(current)),
                'sqrt': math.sqrt(current) if current >= 0 else "Error",
                'square': current * current,
                'log': math.log10(current) if current > 0 else "Error",
                'ln': math.log(current) if current > 0 else "Error",
                'exp': math.exp(current),
                'reciprocal': 1/current if current != 0 else "Error",
                'cube_root': math.pow(current, 1/3)
            }[operation]
            
            self.update_display(result)
        except ValueError:
            self.update_display("Error")
        except ZeroDivisionError:
            self.update_display("Error")

    def plot_linear_equation(self):
        try:
            # Open dialog boxes to get slope and y-intercept
            m = simpledialog.askfloat("Input", "Enter the slope (m):")
            if m is None:  # User cancelled
                return
            
            b = simpledialog.askfloat("Input", "Enter the b (y-intercept):")
            if b is None:  # User cancelled
                return

            # Generate x values
            x = np.linspace(-10, 10, 400)
            
            # Calculate y values based on the equation
            y = m * x + b
            
            # Plot the graph
            plt.figure(figsize=(8, 6))
            plt.plot(x, y, label=f'y = {m}x + {b}')
            plt.axhline(0, color='black', linewidth=0.8, linestyle='--') # x-axis
            plt.axvline(0, color='black', linewidth=0.8, linestyle='--') # y-axis
            plt.grid(color='gray', linestyle='--', linewidth=0.5)
            plt.title("Graph of Linear Equation")
            plt.xlabel("x-axis")
            plt.ylabel("y-axis")
            plt.legend()
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while plotting: {str(e)}")

    def button_click(self, text):
        if text == 'CE':
            self.clear_display()
        elif text == '←':
            self.backspace()
        elif text == '±':
            self.toggle_sign()
        elif text == 'π':
            self.display_pi()
        elif text in "0123456789.":
            self.append_to_display(text)
        elif text in "+-*/":
            self.set_operation(text)
        elif text == "=":
            self.calculate_result()

    def set_operation(self, operation):
        try:
            self.result = float(self.display.get())
            self.operation = operation
            self.new_number = True
        except ValueError:
            pass

    def calculate_result(self):
        try:
            current = float(self.display.get())
            result = {
                "+": self.result + current,
                "-": self.result - current,
                "*": self.result * current,
                "/": "Error" if current == 0 else self.result / current
            }.get(self.operation, current)
            
            self.update_display(result)
        except ValueError:
            self.update_display("Error")
        self.operation = None
        self.new_number = True

    def update_display(self, value):
        self.display.delete(0, tk.END)
        self.display.insert(0, str(value))
        self.new_number = True

    def clear_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, "0")
        self.result = ""
        self.operation = None
        self.new_number = True

    def backspace(self):
        current = self.display.get()
        self.display.delete(len(current)-1, tk.END) if len(current) > 1 else self.clear_display()

    def toggle_sign(self):
        try:
            current = float(self.display.get())
            self.update_display(-current)
        except ValueError:
            pass

    def display_pi(self):
        self.update_display(math.pi)

    def append_to_display(self, text):
        if self.new_number:
            self.display.delete(0, tk.END)
            self.new_number = False
        if text != '.' or '.' not in self.display.get():
            self.display.insert(tk.END, text)

def main():
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
