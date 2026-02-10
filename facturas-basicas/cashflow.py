import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# ==================== VARIABLES GLOBALES ====================
ventana = None
carrito = []
texto_carrito = None
etiqueta_total = None

# ==================== BASE DE DATOS ====================

def iniciar_bd():
    conn = sqlite3.connect("cashflow.db")
    c = conn.cursor()
    
    c.execute("""CREATE TABLE IF NOT EXISTS Producto (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        precio REAL
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS Venta (
        id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        total REAL
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS DetalleVenta (
        id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
        id_venta INTEGER,
        id_producto INTEGER,
        cantidad INTEGER,
        subtotal REAL
    )""")
    
    conn.commit()
    conn.close()

# ==================== FUNCIONES AUXILIARES ====================

def limpiar():
    for widget in ventana.winfo_children():
        widget.destroy()

def header(titulo, boton_atras=True):
    h = tk.Frame(ventana, bg="#1E88E5", height=60)
    h.pack(fill=tk.X)
    h.pack_propagate(False)
    
    if boton_atras:
        tk.Button(h, text="←", font=("Arial", 20), bg="#1E88E5", fg="white",
                  border=0, command=menu).pack(side=tk.LEFT, padx=10)
    
    tk.Label(h, text=titulo, font=("Arial", 16, "bold"), bg="#1E88E5",
             fg="white").pack(side=tk.LEFT, padx=10)

# ==================== MENÚ PRINCIPAL ====================

def menu():
    global carrito
    carrito = []
    limpiar()
    header("CASHFLOW", False)
    
    f = tk.Frame(ventana, bg="#F5F5F5")
    f.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(f, text="💰", font=("Arial", 50), bg="#F5F5F5").pack(pady=20)
    tk.Label(f, text="Sistema de Ventas", font=("Arial", 10), bg="#F5F5F5").pack()
    
    tk.Button(f, text="🛍️ Nueva Venta", font=("Arial", 14, "bold"), bg="#43A047",
              fg="white", border=0, height=3, command=nueva_venta).pack(fill=tk.X, padx=20, pady=5)
    
    tk.Button(f, text="📦 Productos", font=("Arial", 14, "bold"), bg="#FF6F00",
              fg="white", border=0, height=3, command=productos).pack(fill=tk.X, padx=20, pady=5)
    
    tk.Button(f, text="📊 Ventas", font=("Arial", 14, "bold"), bg="#5E35B1",
              fg="white", border=0, height=3, command=ver_ventas).pack(fill=tk.X, padx=20, pady=5)
    
    tk.Button(f, text="❌ Salir", font=("Arial", 14, "bold"), bg="#D32F2F",
              fg="white", border=0, height=3, command=ventana.quit).pack(fill=tk.X, padx=20, pady=5)

# ==================== PRODUCTOS ====================

def productos():
    limpiar()
    header("Productos")
    
    f = tk.Frame(ventana, bg="#F5F5F5")
    f.pack(fill=tk.BOTH, expand=True)
    
    tk.Button(f, text="+ Agregar", font=("Arial", 12, "bold"), bg="#43A047",
              fg="white", border=0, command=agregar_producto).pack(fill=tk.X, padx=20, pady=10)
    
    conn = sqlite3.connect("cashflow.db")
    c = conn.cursor()
    c.execute("SELECT * FROM Producto")
    prods = c.fetchall()
    conn.close()
    
    if len(prods) == 0:
        tk.Label(f, text="Sin productos", font=("Arial", 12), bg="#F5F5F5").pack(pady=50)
    else:
        for p in prods:
            card = tk.Frame(f, bg="white", relief="solid", borderwidth=1)
            card.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(card, text=p[1], font=("Arial", 13, "bold"), bg="white",
                     anchor="w").pack(fill=tk.X, padx=15, pady=5)
            tk.Label(card, text=f"${p[2]:.2f}", font=("Arial", 12), bg="white",
                     fg="#43A047", anchor="w").pack(fill=tk.X, padx=15)
            
            bf = tk.Frame(card, bg="white")
            bf.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Button(bf, text="✏️ Editar", font=("Arial", 9), bg="#FFA726",
                      fg="white", border=0,
                      command=lambda id=p[0], n=p[1], pr=p[2]: editar_producto(id, n, pr)).pack(side=tk.LEFT, padx=5)
            
            tk.Button(bf, text="🗑️ Borrar", font=("Arial", 9), bg="#E53935",
                      fg="white", border=0,
                      command=lambda id=p[0]: borrar_producto(id)).pack(side=tk.LEFT, padx=5)

def agregar_producto():
    d = tk.Toplevel(ventana)
    d.title("Agregar")
    d.geometry("300x200")
    d.resizable(False, False)
    d.grab_set()
    
    x = (d.winfo_screenwidth() - 300) // 2
    y = (d.winfo_screenheight() - 200) // 2
    d.geometry(f"+{x}+{y}")
    
    tk.Label(d, text="Nombre:", font=("Arial", 11)).pack(pady=5)
    e_nom = tk.Entry(d, font=("Arial", 11), width=25)
    e_nom.pack(pady=5)
    
    tk.Label(d, text="Precio:", font=("Arial", 11)).pack(pady=5)
    e_pre = tk.Entry(d, font=("Arial", 11), width=25)
    e_pre.pack(pady=5)
    
    def guardar():
        nom = e_nom.get().strip()
        pre = e_pre.get().strip()
        
        if nom == "" or pre == "":
            messagebox.showerror("Error", "Llena todos los campos")
            return
        
        try:
            precio = float(pre)
            if precio <= 0:
                messagebox.showerror("Error", "Precio mayor a 0")
                return
        except:
            messagebox.showerror("Error", "Precio inválido")
            return
        
        conn = sqlite3.connect("cashflow.db")
        c = conn.cursor()
        c.execute("INSERT INTO Producto (nombre, precio) VALUES (?, ?)", (nom, precio))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("OK", "Producto agregado")
        d.destroy()
        productos()
    
    tk.Button(d, text="Guardar", font=("Arial", 11, "bold"), bg="#43A047",
              fg="white", border=0, command=guardar).pack(pady=10)

def editar_producto(id_prod, nombre, precio):
    d = tk.Toplevel(ventana)
    d.title("Editar")
    d.geometry("300x200")
    d.resizable(False, False)
    d.grab_set()
    
    x = (d.winfo_screenwidth() - 300) // 2
    y = (d.winfo_screenheight() - 200) // 2
    d.geometry(f"+{x}+{y}")
    
    tk.Label(d, text="Nombre:", font=("Arial", 11)).pack(pady=5)
    e_nom = tk.Entry(d, font=("Arial", 11), width=25)
    e_nom.insert(0, nombre)
    e_nom.pack(pady=5)
    
    tk.Label(d, text="Precio:", font=("Arial", 11)).pack(pady=5)
    e_pre = tk.Entry(d, font=("Arial", 11), width=25)
    e_pre.insert(0, str(precio))
    e_pre.pack(pady=5)
    
    def guardar():
        nom = e_nom.get().strip()
        pre = e_pre.get().strip()
        
        if nom == "" or pre == "":
            messagebox.showerror("Error", "Llena todos los campos")
            return
        
        try:
            precio = float(pre)
            if precio <= 0:
                messagebox.showerror("Error", "Precio mayor a 0")
                return
        except:
            messagebox.showerror("Error", "Precio inválido")
            return
        
        conn = sqlite3.connect("cashflow.db")
        c = conn.cursor()
        c.execute("UPDATE Producto SET nombre=?, precio=? WHERE id_producto=?", (nom, precio, id_prod))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("OK", "Producto actualizado")
        d.destroy()
        productos()
    
    tk.Button(d, text="Guardar", font=("Arial", 11, "bold"), bg="#43A047",
              fg="white", border=0, command=guardar).pack(pady=10)

def borrar_producto(id_prod):
    resp = messagebox.askyesno("Confirmar", "¿Borrar producto?")
    if resp:
        conn = sqlite3.connect("cashflow.db")
        c = conn.cursor()
        c.execute("DELETE FROM Producto WHERE id_producto=?", (id_prod,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("OK", "Producto borrado")
        productos()

# ==================== NUEVA VENTA ====================

def nueva_venta():
    global carrito, texto_carrito, etiqueta_total
    carrito = []
    
    limpiar()
    header("Nueva Venta")
    
    f = tk.Frame(ventana, bg="#F5F5F5")
    f.pack(fill=tk.BOTH, expand=True)
    
    # Carrito
    fc = tk.Frame(f, bg="white", height=150)
    fc.pack(fill=tk.X, padx=20, pady=10)
    fc.pack_propagate(False)
    
    tk.Label(fc, text="🛒 Carrito", font=("Arial", 12, "bold"), bg="white").pack(pady=5)
    
    texto_carrito = tk.Text(fc, height=5, font=("Arial", 9), bg="#F5F5F5", state="disabled")
    texto_carrito.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Total
    etiqueta_total = tk.Label(f, text="TOTAL: $0.00", font=("Arial", 16, "bold"),
                              bg="#F5F5F5", fg="#43A047")
    etiqueta_total.pack(pady=5)
    
    # Botones
    tk.Button(f, text="+ Agregar", font=("Arial", 11, "bold"), bg="#1E88E5",
              fg="white", border=0, command=agregar_carrito).pack(fill=tk.X, padx=20, pady=3)
    
    tk.Button(f, text="💳 Finalizar", font=("Arial", 11, "bold"), bg="#43A047",
              fg="white", border=0, command=finalizar).pack(fill=tk.X, padx=20, pady=3)
    
    tk.Button(f, text="🗑️ Limpiar", font=("Arial", 11, "bold"), bg="#E53935",
              fg="white", border=0, command=limpiar_carrito).pack(fill=tk.X, padx=20, pady=3)
    
    actualizar_carrito()

def agregar_carrito():
    conn = sqlite3.connect("cashflow.db")
    c = conn.cursor()
    c.execute("SELECT * FROM Producto")
    prods = c.fetchall()
    conn.close()
    
    if len(prods) == 0:
        messagebox.showwarning("Aviso", "Sin productos")
        return
    
    d = tk.Toplevel(ventana)
    d.title("Seleccionar")
    d.geometry("300x250")
    d.resizable(False, False)
    d.grab_set()
    
    x = (d.winfo_screenwidth() - 300) // 2
    y = (d.winfo_screenheight() - 250) // 2
    d.geometry(f"+{x}+{y}")
    
    tk.Label(d, text="Producto:", font=("Arial", 11)).pack(pady=5)
    
    var = tk.StringVar()
    combo = ttk.Combobox(d, textvariable=var, font=("Arial", 10),
                         state="readonly", width=25)
    
    lista = []
    for p in prods:
        lista.append(f"{p[1]} - ${p[2]:.2f}")
    combo['values'] = lista
    combo.pack(pady=5)
    
    tk.Label(d, text="Cantidad:", font=("Arial", 11)).pack(pady=5)
    e_cant = tk.Entry(d, font=("Arial", 11), width=25)
    e_cant.insert(0, "1")
    e_cant.pack(pady=5)
    
    def agregar():
        global carrito
        
        if var.get() == "":
            messagebox.showerror("Error", "Selecciona producto")
            return
        
        try:
            cant = int(e_cant.get())
            if cant <= 0:
                messagebox.showerror("Error", "Cantidad mayor a 0")
                return
        except:
            messagebox.showerror("Error", "Cantidad inválida")
            return
        
        idx = combo.current()
        p = prods[idx]
        
        item = {
            'id_producto': p[0],
            'nombre': p[1],
            'precio': p[2],
            'cantidad': cant,
            'subtotal': p[2] * cant
        }
        
        carrito.append(item)
        actualizar_carrito()
        d.destroy()
    
    tk.Button(d, text="Agregar", font=("Arial", 11, "bold"), bg="#43A047",
              fg="white", border=0, command=agregar).pack(pady=10)

def actualizar_carrito():
    global texto_carrito, etiqueta_total, carrito
    
    texto_carrito.config(state="normal")
    texto_carrito.delete(1.0, tk.END)
    
    if len(carrito) == 0:
        texto_carrito.insert(tk.END, "Vacío")
        total = 0
    else:
        total = 0
        for item in carrito:
            texto_carrito.insert(tk.END, f"{item['nombre']} x{item['cantidad']} - ${item['subtotal']:.2f}\n")
            total += item['subtotal']
    
    texto_carrito.config(state="disabled")
    etiqueta_total.config(text=f"TOTAL: ${total:.2f}")

def limpiar_carrito():
    global carrito
    if len(carrito) > 0:
        resp = messagebox.askyesno("Confirmar", "¿Limpiar carrito?")
        if resp:
            carrito = []
            actualizar_carrito()

def finalizar():
    global carrito
    
    if len(carrito) == 0:
        messagebox.showwarning("Aviso", "Carrito vacío")
        return
    
    # Guardar venta
    total = 0
    for item in carrito:
        total += item['subtotal']
    
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect("cashflow.db")
    c = conn.cursor()
    c.execute("INSERT INTO Venta (fecha, total) VALUES (?, ?)", (fecha, total))
    id_venta = c.lastrowid
    
    for item in carrito:
        c.execute("INSERT INTO DetalleVenta (id_venta, id_producto, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                  (id_venta, item['id_producto'], item['cantidad'], item['subtotal']))
    
    conn.commit()
    conn.close()
    
    messagebox.showinfo("OK", f"Venta #{id_venta} registrada")
    comprobante(id_venta)

def comprobante(id_venta):
    d = tk.Toplevel(ventana)
    d.title(f"Comprobante #{id_venta}")
    d.geometry("350x500")
    d.resizable(False, False)
    
    x = (d.winfo_screenwidth() - 350) // 2
    y = (d.winfo_screenheight() - 500) // 2
    d.geometry(f"+{x}+{y}")
    
    f = tk.Frame(d, bg="white")
    f.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    tk.Label(f, text="CASHFLOW", font=("Arial", 18, "bold"), bg="white",
             fg="#1E88E5").pack()
    tk.Label(f, text="Sistema de Ventas", font=("Arial", 9), bg="white").pack()
    tk.Label(f, text="─" * 40, bg="white").pack(pady=5)
    
    conn = sqlite3.connect("cashflow.db")
    c = conn.cursor()
    c.execute("SELECT * FROM Venta WHERE id_venta=?", (id_venta,))
    venta = c.fetchone()
    
    tk.Label(f, text=f"Venta #{id_venta}", font=("Arial", 12, "bold"), bg="white").pack()
    tk.Label(f, text=f"Fecha: {venta[1]}", font=("Arial", 9), bg="white").pack()
    tk.Label(f, text="─" * 40, bg="white").pack(pady=5)
    
    c.execute("""SELECT p.nombre, d.cantidad, p.precio, d.subtotal
                 FROM DetalleVenta d
                 JOIN Producto p ON d.id_producto = p.id_producto
                 WHERE d.id_venta = ?""", (id_venta,))
    detalles = c.fetchall()
    conn.close()
    
    total = 0
    for det in detalles:
        tk.Label(f, text=det[0], font=("Arial", 10, "bold"), bg="white",
                 anchor="w").pack(fill=tk.X)
        tk.Label(f, text=f"{det[1]} x ${det[2]:.2f} = ${det[3]:.2f}",
                 font=("Arial", 9), bg="white", anchor="w").pack(fill=tk.X)
        total += det[3]
    
    tk.Label(f, text="─" * 40, bg="white").pack(pady=5)
    tk.Label(f, text=f"TOTAL: ${total:.2f}", font=("Arial", 16, "bold"),
             bg="white", fg="#43A047").pack(pady=10)
    
    tk.Button(f, text="Cerrar", font=("Arial", 11, "bold"), bg="#1E88E5",
              fg="white", border=0, command=lambda: [d.destroy(), menu()]).pack(pady=10)

# ==================== VER VENTAS ====================

def ver_ventas():
    limpiar()
    header("Ventas")
    
    f = tk.Frame(ventana, bg="#F5F5F5")
    f.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    conn = sqlite3.connect("cashflow.db")
    c = conn.cursor()
    c.execute("SELECT * FROM Venta ORDER BY fecha DESC")
    ventas = c.fetchall()
    conn.close()
    
    if len(ventas) == 0:
        tk.Label(f, text="Sin ventas", font=("Arial", 12), bg="#F5F5F5").pack(pady=50)
    else:
        for v in ventas:
            card = tk.Frame(f, bg="white", relief="solid", borderwidth=1)
            card.pack(fill=tk.X, pady=5)
            
            tk.Label(card, text=f"Venta #{v[0]}", font=("Arial", 13, "bold"),
                     bg="white", anchor="w").pack(fill=tk.X, padx=15, pady=5)
            tk.Label(card, text=f"📅 {v[1]}", font=("Arial", 10), bg="white",
                     anchor="w").pack(fill=tk.X, padx=15)
            tk.Label(card, text=f"💰 ${v[2]:.2f}", font=("Arial", 12, "bold"),
                     bg="white", fg="#43A047", anchor="w").pack(fill=tk.X, padx=15)
            
            tk.Button(card, text="📄 Ver Comprobante", font=("Arial", 10, "bold"),
                      bg="#1E88E5", fg="white", border=0,
                      command=lambda id=v[0]: comprobante(id)).pack(fill=tk.X, padx=10, pady=5)

# ==================== INICIO ====================

def iniciar():
    global ventana
    
    iniciar_bd()
    
    ventana = tk.Tk()
    ventana.title("CASHFLOW")
    
    ancho = 375
    alto = 667
    x = (ventana.winfo_screenwidth() - ancho) // 2
    y = (ventana.winfo_screenheight() - alto) // 2
    
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana.resizable(False, False)
    
    menu()
    ventana.mainloop()

iniciar()