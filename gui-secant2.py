import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from tkinter import scrolledtext

def f(x):
    return 2 * x**3 - x - math.exp(-x)

def secant_with_iterations(x0, x1, tol, max_iter):
    iterations = []
    step = 1
    while step <= max_iter:
        if f(x0) == f(x1):
            raise ValueError("Divide by zero error in Secant method!")
        x2 = x0 - (x1 - x0) * f(x0) / (f(x1) - f(x0))
        error = abs(x2 - x1)
        iterations.append((step, x0, x1, x2, error))
        if error < tol:
            return x2, step, iterations
        x0, x1 = x1, x2
        step += 1
    raise ValueError("Method did not converge within the maximum number of iterations!")

def hitung():
    try:
        # Validasi input
        if not all([x0_entry.get(), x1_entry.get(), tol_entry.get(), max_iter_entry.get()]):
            raise ValueError("Semua field harus diisi!")
            
        x0 = float(x0_entry.get())
        x1 = float(x1_entry.get())
        tol = float(tol_entry.get())
        max_iter = int(max_iter_entry.get())
        
        if tol <= 0:
            raise ValueError("Toleransi harus lebih besar dari 0!")
        if max_iter <= 0:
            raise ValueError("Iterasi maksimum harus lebih besar dari 0!")
        
        root, iterations_count, iterations = secant_with_iterations(x0, x1, tol, max_iter)
        result_label.config(text=f"Hasil : x = {root:.10f} (ditemukan dalam {iterations_count} iterasi)", fg="#C85C8E")
        
        # Update tabel iterasi
        update_iteration_table(iterations)
        
        # Update visualisasi grafik
        plot_graph(iterations)
        
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

def update_iteration_table(iterations):
    # Clear previous content
    iteration_text.config(state=tk.NORMAL)
    iteration_text.delete(1.0, tk.END)
    
    # Add header
    header = f"{'Iterasi':<10}{'X0':<20}{'Xi':<20}{'Xi+1':<20}{'Error':<20}\n"
    iteration_text.insert(tk.END, header)
    iteration_text.insert(tk.END, "-"*90 + "\n")
    
    # Add iteration data
    for i, (step, x0, x1, x2, error) in enumerate(iterations):
        row = f"{step:<10}{x0:<20.10f}{x1:<20.10f}{x2:<20.10f}{error:<20.10f}\n"
        iteration_text.insert(tk.END, row)
        
        # Apply alternating background colors
        iteration_text.tag_add(f"row_{i}", f"{i+3}.0", f"{i+3}.end")
        iteration_text.tag_config(f"row_{i}", background="#FFD6E3" if i % 2 == 0 else "#FFEBF1")
    
    iteration_text.config(state=tk.DISABLED)

def reset():
    x0_entry.delete(0, tk.END)
    x1_entry.delete(0, tk.END)
    tol_entry.delete(0, tk.END)
    max_iter_entry.delete(0, tk.END)
    result_label.config(text="")
    iteration_text.config(state=tk.NORMAL)
    iteration_text.delete(1.0, tk.END)
    iteration_text.config(state=tk.DISABLED)
    for widget in graph_frame.winfo_children():
        widget.destroy()

def export_to_csv():
    content = iteration_text.get(1.0, tk.END)
    if not content.strip():
        messagebox.showwarning("Peringatan", "Tidak ada data untuk diekspor!")
        return
    
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
        title="Simpan Hasil Sebagai"
    )
    
    if not file_path:
        return
    
    try:
        with open(file_path, 'w', newline='') as file:
            # Write header
            file.write("Iterasi,X0,Xi,Xi+1,Error\n")
            # Write data
            for line in content.split('\n')[2:-1]:  # Skip header and empty lines
                if line.strip():
                    parts = line.split()
                    file.write(f"{parts[0]},{parts[1]},{parts[2]},{parts[3]},{parts[4]}\n")
        messagebox.showinfo("Sukses", "Data berhasil diekspor ke CSV!")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengekspor data: {str(e)}")

def plot_graph(iterations):
    steps = [i[0] for i in iterations]
    x2_values = [i[3] for i in iterations]
    errors = [i[4] for i in iterations]
    
    fig = plt.figure(figsize=(12, 5), facecolor="#FDE2E4")
    fig.suptitle(f"Visualisasi Metode Secant", color="#C85C8E")
    
    # Plot 1: Nilai Xi+1
    ax1 = fig.add_subplot(121)
    ax1.plot(steps, x2_values, marker="o", color="#C85C8E", label="Xi+1", linewidth=2)
    ax1.set_xlabel("Iterasi", color="#C85C8E")
    ax1.set_ylabel("Nilai Xi+1", color="#C85C8E")
    ax1.set_title("Perkembangan Nilai Xi+1", color="#C85C8E")
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()
    
    # Plot 2: Error
    ax2 = fig.add_subplot(122)
    ax2.plot(steps, errors, marker="o", color="#FFB3C6", label="Error", linewidth=2)
    ax2.set_xlabel("Iterasi", color="#C85C8E")
    ax2.set_ylabel("Error", color="#C85C8E")
    ax2.set_title("Perkembangan Error", color="#C85C8E")
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend()
    
    plt.tight_layout()
    
    # Clear previous graph
    for widget in graph_frame.winfo_children():
        widget.destroy()
    
    # Embed graph in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root = tk.Tk()
root.title("Metode Secant")
root.geometry("1000x700")  # Slightly larger window
root.resizable(True, True)  
root.configure(bg="#FDE2E4")

main_frame = tk.Frame(root, bg="#FDE2E4")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Input Section
input_frame = tk.Frame(main_frame, bg="#FDE2E4")
input_frame.pack(fill=tk.X, pady=5)

tk.Label(input_frame, text="Tebakan Awal X0:", fg="#C85C8E", bg="#FDE2E4").grid(row=0, column=0, padx=5, pady=5, sticky="e")
x0_entry = tk.Entry(input_frame, bg="#FFB3C6")
x0_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(input_frame, text="Tebakan Awal Xi:", fg="#C85C8E", bg="#FDE2E4").grid(row=0, column=2, padx=5, pady=5, sticky="e")
x1_entry = tk.Entry(input_frame, bg="#FFB3C6")
x1_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

tk.Label(input_frame, text="Toleransi:", fg="#C85C8E", bg="#FDE2E4").grid(row=1, column=0, padx=5, pady=5, sticky="e")
tol_entry = tk.Entry(input_frame, bg="#FFB3C6")
tol_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(input_frame, text="Iterasi Maksimum:", fg="#C85C8E", bg="#FDE2E4").grid(row=1, column=2, padx=5, pady=5, sticky="e")
max_iter_entry = tk.Entry(input_frame, bg="#FFB3C6")
max_iter_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")

# Button Section
button_frame = tk.Frame(main_frame, bg="#FDE2E4")
button_frame.pack(fill=tk.X, pady=5)

calculate_button = tk.Button(button_frame, text="Hitung", command=hitung, fg="#FFFFFF", bg="#C85C8E", width=10)
calculate_button.pack(side=tk.LEFT, padx=5)

reset_button = tk.Button(button_frame, text="Reset", command=reset, fg="#FFFFFF", bg="#FF7BA9", width=10)
reset_button.pack(side=tk.LEFT, padx=5)

export_button = tk.Button(button_frame, text="Ekspor CSV", command=export_to_csv, fg="#FFFFFF", bg="#FF7BA9", width=10)
export_button.pack(side=tk.LEFT, padx=5)

# Result Label
result_label = tk.Label(main_frame, text="", font=("Arial", 10, "bold"), fg="#C85C8E", bg="#FDE2E4")
result_label.pack(fill=tk.X, pady=5)

# Iteration Table Section
table_frame = tk.LabelFrame(main_frame, text="Tabel Iterasi", fg="#C85C8E", bg="#FDE2E4")
table_frame.pack(fill=tk.BOTH, expand=True, pady=5)

iteration_text = scrolledtext.ScrolledText(table_frame, width=100, height=10, wrap=tk.NONE, bg="white")
iteration_text.pack(fill=tk.BOTH, expand=True)

# Configure tags for alternating row colors
iteration_text.tag_config("header", foreground="#C85C8E", font=('Arial', 10, 'bold'))
iteration_text.config(state=tk.DISABLED)

# Graph Section
graph_frame = tk.LabelFrame(main_frame, text="Visualisasi Grafik", fg="#C85C8E", bg="#FDE2E4")
graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)

root.mainloop()
