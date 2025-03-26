import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import time
import threading

def secant_method(f, x0, x1, tol, max_iter=100):
    x_values, errors = [x0, x1], []
    for _ in range(max_iter):
        fx0, fx1 = f(x0), f(x1)
        if abs(fx1 - fx0) < tol:
            break
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        error = abs(x2 - x1)
        x_values.append(x2)
        errors.append(error)
        if error < tol:
            break
        x0, x1 = x1, x2
    return x_values, errors

class SecantApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Metode Secant - GUI")
        self.master.geometry("1000x700")
        
        # Create main container
        main_frame = ttk.Frame(master, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Metode Secant", 
                 font=("Arial", 16, "bold"), 
                 bootstyle="primary").pack(pady=10)
        
        # Equation display
        eq_frame = ttk.Frame(main_frame)
        eq_frame.pack(fill=tk.X, pady=5)
        ttk.Label(eq_frame, text="Fungsi: f(x) = 2x³ - x - e⁻ˣ", 
                 font=("Arial", 12), 
                 bootstyle="info").pack()
        
        # Parameters frame
        param_frame = ttk.LabelFrame(main_frame, text="Parameter", bootstyle="info")
        param_frame.pack(fill=tk.X, pady=10, padx=5)
        
        # Initial guesses
        ttk.Label(param_frame, text="Tebakan Awal:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.x0_entry = ttk.Entry(param_frame, width=10)
        self.x0_entry.insert(0, "0.1")
        self.x0_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(param_frame, text="x1:").grid(row=0, column=2, padx=5, pady=5)
        self.x1_entry = ttk.Entry(param_frame, width=10)
        self.x1_entry.insert(0, "2")
        self.x1_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Tolerance
        ttk.Label(param_frame, text="Toleransi:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.tol_entry = ttk.Entry(param_frame, width=10)
        self.tol_entry.insert(0, "0.0001")
        self.tol_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Max iterations
        ttk.Label(param_frame, text="Iterasi Maksimum:").grid(row=1, column=2, padx=5, pady=5)
        self.max_iter_entry = ttk.Entry(param_frame, width=10)
        self.max_iter_entry.insert(0, "100")
        self.max_iter_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        self.calc_button = ttk.Button(button_frame, text="Hitung Akar", 
                                    command=self.start_calculation, 
                                    bootstyle="success-outline")
        self.calc_button.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, 
                                       length=300, mode='determinate', 
                                       bootstyle="info-striped")
        self.progress.pack(pady=10)
        
        # Result frame
        result_frame = ttk.LabelFrame(main_frame, text="Hasil", bootstyle="info")
        result_frame.pack(fill=tk.X, pady=10, padx=5)
        
        self.result_label = ttk.Label(result_frame, text="", font=("Arial", 11))
        self.result_label.pack(pady=5)
        
        # Table frame
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create a notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Graph tab
        self.graph_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.graph_tab, text="Grafik")
        
        # Table tab
        self.table_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.table_tab, text="Tabel Iterasi")
        
        # Initialize table and graph
        self.init_table()
        self.init_graph()
    
    def init_table(self):
        # Create treeview for table
        self.tree = ttk.Treeview(self.table_tab, columns=('Iterasi', 'x_i', 'x_i+1', 'Error'), show='headings')
        
        # Define headings
        self.tree.heading('Iterasi', text='Iterasi')
        self.tree.heading('x_i', text='xᵢ')
        self.tree.heading('x_i+1', text='xᵢ₊₁')
        self.tree.heading('Error', text='Error')
        
        # Set column widths
        self.tree.column('Iterasi', width=80, anchor=tk.CENTER)
        self.tree.column('x_i', width=150, anchor=tk.CENTER)
        self.tree.column('x_i+1', width=150, anchor=tk.CENTER)
        self.tree.column('Error', width=150, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.table_tab, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
    
    def init_graph(self):
        # Create figure for plotting
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.ax.set_title('Perkembangan Nilai xᵢ₊₁ pada Setiap Iterasi')
        self.ax.set_xlabel('Iterasi')
        self.ax.set_ylabel('Nilai xᵢ₊₁')
        self.ax.grid(True, linestyle='--', alpha=0.6)
        
        # Create canvas for the figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def start_calculation(self):
        # Disable button during calculation
        self.calc_button.config(state=tk.DISABLED)
        self.progress['value'] = 0
        
        # Start calculation in a separate thread
        threading.Thread(target=self.calculate, daemon=True).start()
    
    def calculate(self):
        try:
            # Get parameters from entries
            x0 = float(self.x0_entry.get())
            x1 = float(self.x1_entry.get())
            tol = float(self.tol_entry.get())
            max_iter = int(self.max_iter_entry.get())
            
            # Define the function
            x = sp.Symbol('x')
            f_expr = 2*x**3 - x - sp.exp(-x)
            f = sp.lambdify(x, f_expr, "numpy")
            
            # Simulate progress (for demonstration)
            for i in range(10):
                time.sleep(0.1)
                self.progress['value'] += 10
                self.master.update()
            
            # Run secant method
            x_values, errors = secant_method(f, x0, x1, tol, max_iter)
            
            # Update results in GUI
            self.master.after(0, self.update_results, x_values, errors)
            
        except ValueError as e:
            self.master.after(0, messagebox.showerror, "Error", f"Input tidak valid: {str(e)}")
        finally:
            self.master.after(0, lambda: self.calc_button.config(state=tk.NORMAL))
    
    def update_results(self, x_values, errors):
        # Update result label
        self.result_label.config(text=f"Akar ditemukan: x ≈ {x_values[-1]:.8f}")
        
        # Update table
        self.tree.delete(*self.tree.get_children())
        for i in range(len(x_values)-1):
            self.tree.insert('', 'end', values=(
                i+1, 
                f"{x_values[i]:.8f}", 
                f"{x_values[i+1]:.8f}", 
                f"{errors[i]:.8f}" if i < len(errors) else "-"
            ))
        
        # Update graph (plot xi+1 values)
        self.ax.clear()
        iterations = range(1, len(x_values))
        xi_plus_1 = x_values[1:]
        self.ax.plot(iterations, xi_plus_1, 'bo-', markersize=6, linewidth=1.5, label='xᵢ₊₁')
        
        # Add annotations for the last point
        last_iter = iterations[-1]
        last_val = xi_plus_1[-1]
        self.ax.annotate(f'{last_val:.6f}', 
                         xy=(last_iter, last_val), 
                         xytext=(10, -20),
                         textcoords='offset points',
                         bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                         arrowprops=dict(arrowstyle='->'))
        
        self.ax.set_title('Perkembangan Nilai xᵢ₊₁ pada Setiap Iterasi')
        self.ax.set_xlabel('Iterasi')
        self.ax.set_ylabel('Nilai xᵢ₊₁')
        self.ax.legend()
        self.ax.grid(True, linestyle='--', alpha=0.6)
        
        # Redraw canvas
        self.canvas.draw()

if __name__ == "__main__":
    # Use a blue theme
    root = ttk.Window(themename="minty")
    app = SecantApp(root)
    root.mainloop()
