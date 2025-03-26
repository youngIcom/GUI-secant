import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

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
    for item in iteration_tree.get_children():
        iteration_tree.delete(item)
    
    # Add data to treeview
    for step, x0, x1, x2, error in iterations:
        iteration_tree.insert("", tk.END, values=(step, f"{x0:.10f}", f"{x1:.10f}", f"{x2:.10f}", f"{error:.10f}"))

def reset():
    x0_entry.delete(0, tk.END)
    x1_entry.delete(0, tk.END)
    tol_entry.delete(0, tk.END)
    max_iter_entry.delete(0, tk.END)
    result_label.config(text="")
    for item in iteration_tree.get_children():
        iteration_tree.delete(item)
    for widget in graph_frame.winfo_children():
        widget.destroy()

def export_to_csv():
    if not iteration_tree.get_children():
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
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Iterasi", "X0", "Xi", "Xi+1", "Error"])
            # Write data
            for child in iteration_tree.get_children():
                writer.writerow(iteration_tree.item(child)['values'])
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
root.geometry("1000x700")
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

# Create Treeview with scrollbars
tree_scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
tree_scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")

iteration_tree = ttk.Treeview(
    table_frame,
    columns=("Iterasi", "X0", "Xi", "Xi+1", "Error"),
    show="headings",
    yscrollcommand=tree_scroll_y.set,
    xscrollcommand=tree_scroll_x.set
)

# Configure scrollbars
tree_scroll_y.config(command=iteration_tree.yview)
tree_scroll_x.config(command=iteration_tree.xview)

# Define headings
iteration_tree.heading("Iterasi", text="Iterasi")
iteration_tree.heading("X0", text="X0")
iteration_tree.heading("Xi", text="Xi")
iteration_tree.heading("Xi+1", text="Xi+1")
iteration_tree.heading("Error", text="Error")

# Set column widths
iteration_tree.column("Iterasi", width=80, anchor="center")
iteration_tree.column("X0", width=200, anchor="center")
iteration_tree.column("Xi", width=200, anchor="center")
iteration_tree.column("Xi+1", width=200, anchor="center")
iteration_tree.column("Error", width=200, anchor="center")

# Pack everything
iteration_tree.pack(side="left", fill="both", expand=True)
tree_scroll_y.pack(side="right", fill="y")
tree_scroll_x.pack(side="bottom", fill="x")

# Configure style for alternating row colors
style = ttk.Style()
style.configure("Treeview", 
               background="#FFFFFF",
               foreground="#000000",
               rowheight=25,
               fieldbackground="#FFFFFF")
style.map("Treeview",
          background=[('selected', '#FF7BA9')])

# Graph Section
graph_frame = tk.LabelFrame(main_frame, text="Visualisasi Grafik", fg="#C85C8E", bg="#FDE2E4")
graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)

root.mainloop()
