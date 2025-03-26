import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp

class SecantMethodApp:
    def __init__(self, master):
        self.master = master
        master.title("Metode Secant - Pencarian Akar Persamaan")
        master.geometry("900x800")
        master.configure(bg='#f0f0f0')

        # Style
        style = ttk.Style()
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TEntry', font=('Arial', 10))

        # Frame utama
        main_frame = ttk.Frame(master, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input persamaan
        ttk.Label(main_frame, text="Masukkan Fungsi f(x):").grid(row=0, column=0, sticky='w', pady=5)
        self.function_entry = ttk.Entry(main_frame, width=50)
        self.function_entry.grid(row=0, column=1, columnspan=2, sticky='ew', pady=5)
        self.function_entry.insert(0, "x**3 + x**2 - 3*x - 3")  # Contoh default

        # Input batas awal
        ttk.Label(main_frame, text="x0:").grid(row=1, column=0, sticky='w', pady=5)
        self.x0_entry = ttk.Entry(main_frame, width=20)
        self.x0_entry.grid(row=1, column=1, sticky='ew', pady=5)
        self.x0_entry.insert(0, "1")

        ttk.Label(main_frame, text="x1:").grid(row=2, column=0, sticky='w', pady=5)
        self.x1_entry = ttk.Entry(main_frame, width=20)
        self.x1_entry.grid(row=2, column=1, sticky='ew', pady=5)
        self.x1_entry.insert(0, "2")

        # Input toleransi error
        ttk.Label(main_frame, text="Toleransi Error:").grid(row=3, column=0, sticky='w', pady=5)
        self.tolerance_entry = ttk.Entry(main_frame, width=20)
        self.tolerance_entry.grid(row=3, column=1, sticky='ew', pady=5)
        self.tolerance_entry.insert(0, "1e-6")

        # Maksimum iterasi
        ttk.Label(main_frame, text="Maks Iterasi:").grid(row=4, column=0, sticky='w', pady=5)
        self.max_iter_entry = ttk.Entry(main_frame, width=20)
        self.max_iter_entry.grid(row=4, column=1, sticky='ew', pady=5)
        self.max_iter_entry.insert(0, "100")

        # Tombol hitung
        calculate_button = ttk.Button(main_frame, text="Hitung", command=self.calculate_secant)
        calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Frame untuk hasil dan grafik
        self.result_frame = ttk.Frame(main_frame)
        self.result_frame.grid(row=6, column=0, columnspan=3, sticky='nsew')

        # Konfigurasi grid
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)

    def create_function(self, func_str):
        """
        Membuat fungsi lambda dari string ekspresi matematis
        """
        try:
            # Menggunakan sympy untuk parsing yang lebih aman
            x = sp.Symbol('x')
            expr = sp.sympify(func_str)
            # Konversi ke fungsi numerik
            return sp.lambdify(x, expr, 'numpy')
        except Exception as e:
            messagebox.showerror("Error", f"Kesalahan parsing fungsi: {e}")
            return None

    def calculate_secant(self):
        try:
            # Ambil input
            func_str = self.function_entry.get()
            x0 = float(self.x0_entry.get())
            x1 = float(self.x1_entry.get())
            tolerance = float(self.tolerance_entry.get())
            max_iterations = int(self.max_iter_entry.get())

            # Buat fungsi
            f = self.create_function(func_str)
            if f is None:
                return

            # Bersihkan frame hasil sebelumnya
            for widget in self.result_frame.winfo_children():
                widget.destroy()

            # List untuk menyimpan iterasi
            iterations = []
            x_values = [x0, x1]
            error_values = []

            # Proses metode secant
            iteration = 0
            while iteration < max_iterations:
                # Hitung nilai fungsi
                fx0 = f(x0)
                fx1 = f(x1)

                # Cek kondisi pembagi nol dengan toleransi
                if abs(fx1 - fx0) < tolerance:
                    messagebox.showwarning("Peringatan", "Pembagi mendekati nol!")
                    break

                # Rumus secant
                try:
                    x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
                except Exception as e:
                    messagebox.showerror("Error", f"Kesalahan perhitungan: {e}")
                    break

                # Hitung nilai fungsi untuk x2
                fx2 = f(x2)

                # Hitung error
                error = abs(x2 - x1)
                
                # Simpan data iterasi
                iterations.append({
                    'iteration': iteration,
                    'x0': x0,
                    'x1': x1,
                    'x2': x2,
                    'f(x2)': fx2,
                    'error': error
                })

                x_values.append(x2)
                error_values.append(error)

                # Kriteria konvergensi
                if error < tolerance or abs(fx2) < tolerance:
                    break

                # Persiapan iterasi berikutnya
                x0, x1 = x1, x2
                iteration += 1

            # Tampilkan tabel hasil
            columns = ('Iterasi', 'x0', 'x1', 'x2', 'f(x2)', 'Error')
            tree = ttk.Treeview(self.result_frame, columns=columns, show='headings')
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor='center')
            
            for row in iterations:
                tree.insert('', 'end', values=(
                    row['iteration'], 
                    f"{row['x0']:.6f}", 
                    f"{row['x1']:.6f}", 
                    f"{row['x2']:.6f}", 
                    f"{row['f(x2)']:.6f}", 
                    f"{row['error']:.6e}"
                ))
            
            tree.pack(expand=True, fill='both', side=tk.TOP)

            # Tambahkan label hasil akhir
            if iterations:
                final_result = iterations[-1]
                result_label = ttk.Label(
                    self.result_frame, 
                    text=f"Akar yang ditemukan: x = {final_result['x2']:.6f}\n"
                         f"Nilai fungsi: f(x) = {final_result['f(x2)']:.6e}\n"
                         f"Error: {final_result['error']:.6e}",
                    font=('Arial', 12, 'bold')
                )
                result_label.pack(pady=10)

            # Buat subplot
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
            
            # Plot x2 vs iterasi
            ax1.plot(range(len(x_values)), x_values, marker='o')
            ax1.set_title('Perubahan Nilai x')
            ax1.set_xlabel('Iterasi')
            ax1.set_ylabel('Nilai x')
            ax1.grid(True)

            # Plot error vs iterasi
            ax2.plot(range(len(error_values)), error_values, marker='o', color='red')
            ax2.set_title('Error vs Iterasi')
            ax2.set_xlabel('Iterasi')
            ax2.set_ylabel('Error')
            ax2.grid(True)

            plt.tight_layout()

            # Embed plot di Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.result_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(expand=True, fill='both')
            canvas.draw()

        except ValueError as e:
            messagebox.showerror("Error", f"Masukan tidak valid: {e}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = SecantMethodApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
