import tkinter as tk
from tkinter import messagebox, Canvas, Scrollbar
from datetime import datetime
from PIL import Image, ImageTk
import requests
from io import BytesIO
import random

class SistemaVerificacion:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Biometria")
        self.ventana.geometry("1500x900")
        self.ventana.configure(bg="#1a0033")
        
        self.biometria_ok = False
        self.fotos = {}
        
        self.usuarios = {
            '1025520829': {
                'nombre': 'Karen Torres', 'edad': 21, 'nacimiento': '11/12/2004',
                'lugar_nac': 'Bogota, Cundinamarca', 'ciudad': 'Bogota D.C.',
                'direccion': 'Ciudad Bolivar', 'estatura': '165 cm', 'ojos': 'Cafe',
                'sangre': 'O+', 'civil': 'Soltera', 'genero': 'Femenino',
                'madre': 'Maria Emilia Torres', 'padre': 'Augusto Useche Useche',
                'ocupacion': 'Ingeniera', 'tel': '+57 321 505 2238',
                'rasgos': 'lunar mejilla', 'firma': 'K.torres',
                'foto': 'https://previews.123rf.com/images/portocala/portocala2203/portocala220300013/183368079-3d-illustration-of-smiling-pretty-woman-cartoon-close-up-portrait-of-standing-caucasian-woman-on-a.jpg', 'fraude': 0.02
            },
            '9876543210': {
                'nombre': 'Maria Gonzalez Ruiz', 'edad': 28, 'nacimiento': '22/07/1996',
                'lugar_nac': 'Medellin, Antioquia', 'ciudad': 'Medellin',
                'direccion': 'Carrera 43A #14-80', 'estatura': '162 cm', 'ojos': 'Verde',
                'sangre': 'A+', 'civil': 'Casada', 'genero': 'Femenino',
                'madre': 'Carmen Ruiz Diaz', 'padre': 'Luis Gonzalez Perez',
                'ocupacion': 'Medico', 'tel': '+57 315 876 5432',
                'rasgos': 'Pecas, cabello ondulado', 'firma': 'Maria G. Ruiz',
                'foto': 'https://randomuser.me/api/portraits/women/44.jpg', 'fraude': 0.01
            },
            '5555555555': {
                'nombre': 'Carlos Rodriguez Lopez', 'edad': 42, 'nacimiento': '08/11/1982',
                'lugar_nac': 'Cali, Valle', 'ciudad': 'Cali',
                'direccion': 'Av. 6N #25-70', 'estatura': '180 cm', 'ojos': 'Negro',
                'sangre': 'B+', 'civil': 'Divorciado', 'genero': 'Masculino',
                'madre': 'Ana Lopez Torres', 'padre': 'Miguel Rodriguez Sanchez',
                'ocupacion': 'Arquitecto', 'tel': '+57 320 555 5555',
                'rasgos': 'Barba, gafas', 'firma': 'Carlos R. Lopez',
                'foto': 'https://randomuser.me/api/portraits/men/67.jpg', 'fraude': 0.03
            }
        }
        
        self.crear_interfaz()
        self.cargar_fotos()
    
    def cargar_fotos(self):
        for cc, u in self.usuarios.items():
            try:
                r = requests.get(u['foto'], timeout=5)
                img = Image.open(BytesIO(r.content)).resize((140, 140), Image.Resampling.LANCZOS)
                self.fotos[cc] = ImageTk.PhotoImage(img)
            except:
                pass
    
    def crear_interfaz(self):
        # Header
        tk.Label(self.ventana, text="SISTEMA DE BIOMETRIA RNEC", 
                font=("Arial", 40, "bold"), bg="#1a0033", fg="#00ffff").pack(pady=20)
        tk.Label(self.ventana, text="Registraduria Nacional del Estado Civil", 
                font=("Arial", 12), bg="#1a0033", fg="#9333ea").pack()
        
        tk.Frame(self.ventana, bg="#22c55e", height=8).pack(fill="x", pady=15)
        
        # Paneles
        container = tk.Frame(self.ventana, bg="#1a0033")
        container.pack(fill="both", expand=True, padx=30)
        
        # IZQUIERDA CON SCROLL
        izq = tk.Frame(container, bg="#2d1b4e", bd=3, relief="ridge")
        izq.pack(side="left", fill="both", expand=True, padx=8)
        
        tk.Label(izq, text="DATOS DEL CIUDADANO", font=("Arial", 18, "bold"), 
                bg="#2d1b4e", fg="#fbbf24").pack(pady=15)
        
        canvas_izq = Canvas(izq, bg="#2d1b4e", highlightthickness=0)
        scroll_izq = Scrollbar(izq, orient="vertical", command=canvas_izq.yview)
        frame_form = tk.Frame(canvas_izq, bg="#2d1b4e")
        
        canvas_izq.configure(yscrollcommand=scroll_izq.set)
        scroll_izq.pack(side="right", fill="y")
        canvas_izq.pack(side="left", fill="both", expand=True)
        
        canvas_izq.create_window((0,0), window=frame_form, anchor="nw", width=680)
        frame_form.bind("<Configure>", lambda e: canvas_izq.configure(scrollregion=canvas_izq.bbox("all")))
        
        # Formulario
        form = tk.Frame(frame_form, bg="#2d1b4e")
        form.pack(padx=20, pady=10, fill="x")
        
        tk.Label(form, text="Nombre:", font=("Arial", 11, "bold"), 
                bg="#2d1b4e", fg="white").pack(anchor="w", pady=(10,3))
        self.entry_nombre = tk.Entry(form, font=("Arial", 14), bg="#1a0033", 
                                     fg="white", insertbackground="#00ffff", bd=2)
        self.entry_nombre.pack(fill="x", ipady=10)
        
        tk.Label(form, text="Cedula:", font=("Arial", 11, "bold"), 
                bg="#2d1b4e", fg="white").pack(anchor="w", pady=(20,3))
        self.entry_cedula = tk.Entry(form, font=("Arial", 14), bg="#1a0033", 
                                     fg="white", insertbackground="#00ffff", bd=2)
        self.entry_cedula.pack(fill="x", ipady=10)
        
        tk.Label(frame_form, text="Escaner Biometrico", font=("Arial", 13, "bold"), 
                bg="#2d1b4e", fg="#00ffff").pack(pady=(25,8))
        
        self.cam = tk.Frame(frame_form, bg="#000", width=450, height=210, bd=4, relief="solid")
        self.cam.pack(pady=5)
        self.cam.pack_propagate(False)
        
        self.lbl_cam = tk.Label(self.cam, text="Camara inactiva\nPresione para escanear", 
                               font=("Arial", 12), bg="#000", fg="#666")
        self.lbl_cam.pack(expand=True)
        
        tk.Button(frame_form, text="CAPTURAR BIOMETRIA", font=("Arial", 12, "bold"), 
                 bg="#9333ea", fg="white", command=self.capturar, bd=0, 
                 pady=14).pack(pady=12, padx=20, fill="x")
        
        # Boton validar cedula
        tk.Button(frame_form, text="VALIDAR CEDULA", font=("Arial", 12, "bold"), 
                 bg="#f59e0b", fg="white", command=self.validar_cedula_btn, 
                 bd=0, pady=12).pack(pady=8, padx=20, fill="x")
        
        self.frm_prog = tk.Frame(frame_form, bg="#1e3a8a", bd=2)
        self.lbl_prog = tk.Label(self.frm_prog, text="", font=("Arial", 10), 
                                bg="#1e3a8a", fg="#93c5fd")
        
        btns = tk.Frame(frame_form, bg="#2d1b4e")
        btns.pack(pady=10, padx=20, fill="x")
        
        tk.Button(btns, text="VERIFICAR", font=("Arial", 13, "bold"), 
                 bg="#22c55e", fg="white", command=self.verificar, 
                 bd=0, pady=16).pack(side="left", expand=True, fill="x", padx=(0,5))
        
        tk.Button(btns, text="LIMPIAR", font=("Arial", 13, "bold"), 
                 bg="#64748b", fg="white", command=self.limpiar, 
                 bd=0, pady=16).pack(side="right", expand=True, fill="x", padx=(5,0))
        
        # Boton intentar nueva validacion
        tk.Button(frame_form, text="INTENTAR NUEVA VALIDACION", font=("Arial", 11, "bold"), 
                 bg="#3b82f6", fg="white", command=self.nueva_validacion, 
                 bd=0, pady=12).pack(pady=8, padx=20, fill="x")
        
        # DERECHA con scroll
        der = tk.Frame(container, bg="#2d1b4e", bd=3, relief="ridge")
        der.pack(side="right", fill="both", expand=True, padx=8)
        
        tk.Label(der, text="RESULTADO", font=("Arial", 18, "bold"), 
                bg="#2d1b4e", fg="#fbbf24").pack(pady=15)
        
        canvas = Canvas(der, bg="#2d1b4e", highlightthickness=0)
        scroll = Scrollbar(der, orient="vertical", command=canvas.yview)
        self.resultado = tk.Frame(canvas, bg="#2d1b4e")
        
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        canvas.create_window((0,0), window=self.resultado, anchor="nw", width=550)
        self.resultado.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        self.inicial()
        
        # Footer
        footer = tk.Frame(self.ventana, bg="#2d1b4e", bd=2, relief="ridge")
        footer.pack(fill="x", padx=30, pady=(12,20))
        
        tk.Label(footer, text="Usuarios de Prueba", font=("Arial", 14, "bold"), 
                bg="#2d1b4e", fg="#00ffff").pack(pady=10)
        
        grid = tk.Frame(footer, bg="#2d1b4e")
        grid.pack(pady=8)
        
        for i, (cc, u) in enumerate(self.usuarios.items()):
            c = tk.Frame(grid, bg="#1a0033", bd=2, relief="solid")
            c.grid(row=0, column=i, padx=10, pady=5)
            
            if cc in self.fotos:
                tk.Label(c, image=self.fotos[cc], bg="#1a0033").pack(pady=5)
            
            tk.Label(c, text=u['nombre'], font=("Arial", 9, "bold"), 
                    bg="#1a0033", fg="white", wraplength=120).pack(pady=3)
            tk.Label(c, text=cc, font=("Arial", 8), 
                    bg="#1a0033", fg="#9333ea").pack(pady=3)
    
    def inicial(self):
        for w in self.resultado.winfo_children():
            w.destroy()
        tk.Label(self.resultado, text="En espera", font=("Arial", 18), 
                bg="#2d1b4e", fg="#888").pack(pady=150)
    
    def validar_cedula_btn(self):
        cc = self.entry_cedula.get().strip()
        
        if not cc:
            messagebox.showwarning("Alerta", "Ingrese un numero de cedula")
            return
        
        if not (cc.isdigit() and 6 <= len(cc) <= 10):
            messagebox.showerror("Error", "Cedula invalida. Debe tener entre 6 y 10 digitos")
            return
        
        for w in self.resultado.winfo_children():
            w.destroy()
        
        if cc in self.usuarios:
            p = self.usuarios[cc]
            
            info = tk.Frame(self.resultado, bg="#065f46", bd=3, relief="solid")
            info.pack(fill="both", expand=True, padx=10, pady=10)
            
            tk.Label(info, text="CEDULA ENCONTRADA", font=("Arial", 18, "bold"), 
                    bg="#065f46", fg="#22c55e").pack(pady=15)
            
            datos_frame = tk.Frame(info, bg="#1a0033", bd=2)
            datos_frame.pack(fill="x", padx=12, pady=12)
            
            if cc in self.fotos:
                tk.Label(datos_frame, image=self.fotos[cc], bg="#1a0033").pack(pady=10)
            
            tk.Label(datos_frame, text="DATOS DEL REGISTRO CIVIL", font=("Arial", 13, "bold"), 
                    bg="#1a0033", fg="#fbbf24").pack(pady=10)
            
            datos = [
                ("Nombre", p['nombre']),
                ("Cedula", cc),
                ("Nacimiento", p['nacimiento']),
                ("Edad", f"{p['edad']} anos"),
                ("Lugar Nacimiento", p['lugar_nac']),
                ("Genero", p['genero']),
                ("Estado Civil", p['civil']),
                ("Madre", p['madre']),
                ("Padre", p['padre']),
                ("Ciudad", p['ciudad']),
                ("Direccion", p['direccion']),
                ("Estatura", p['estatura']),
                ("Color Ojos", p['ojos']),
                ("Tipo Sangre", p['sangre']),
                ("Ocupacion", p['ocupacion']),
                ("Telefono", p['tel']),
                ("Rasgos", p['rasgos'])
            ]
            
            for lbl, val in datos:
                row = tk.Frame(datos_frame, bg="#2d1b4e")
                row.pack(fill="x", padx=10, pady=2)
                tk.Label(row, text=f"{lbl}:", font=("Arial", 9, "bold"), 
                        bg="#2d1b4e", fg="#888", width=16, anchor="w").pack(side="left", padx=5, pady=4)
                tk.Label(row, text=val, font=("Arial", 9), 
                        bg="#2d1b4e", fg="white", anchor="w").pack(side="left", padx=5, pady=4)
            
            tk.Label(info, text="Complete nombre y capture biometria para verificar identidad", 
                    font=("Arial", 10), bg="#065f46", fg="white").pack(pady=10)
        else:
            err = tk.Frame(self.resultado, bg="#991b1b", bd=3, relief="solid")
            err.pack(fill="both", expand=True, padx=10, pady=10)
            tk.Label(err, text="CEDULA NO ENCONTRADA", font=("Arial", 18, "bold"), 
                    bg="#991b1b", fg="#fca5a5").pack(pady=80)
            tk.Label(err, text=f"La cedula {cc} no esta registrada en la base de datos", 
                    font=("Arial", 11), bg="#991b1b", fg="white").pack(pady=15)
    
    def nueva_validacion(self):
        self.limpiar()
        messagebox.showinfo("Nueva Validacion", "Sistema listo para nueva verificacion")
    
    def capturar(self):
        if self.biometria_ok:
            return
        
        self.lbl_cam.config(text="Escaneando...\nAnalizando patrones faciales", 
                           fg="#f59e0b", font=("Arial", 12, "bold"))
        self.ventana.after(1500, self.validar_biometria)
    
    def validar_biometria(self):
        # Simular validacion biometrica (80% exito, 20% falla)
        exito = random.random() > 0.2
        
        if exito:
            self.biometria_ok = True
            self.lbl_cam.config(text="Captura exitosa\nBiometria registrada", fg="#22c55e")
        else:
            self.biometria_ok = False
            self.lbl_cam.config(text="BIOMETRIA FALLIDA\nIntente nuevamente", 
                               fg="#ef4444", font=("Arial", 12, "bold"))
            messagebox.showerror("Error Biometrico", 
                               "No se pudo capturar la biometria facial correctamente\n\nPosibles causas:\n- Mala iluminacion\n- Movimiento durante el escaneo\n- Obstruccion del rostro\n\nIntente nuevamente")
    
    def verificar(self):
        nom = self.entry_nombre.get().strip()
        cc = self.entry_cedula.get().strip()
        
        if not nom or not cc:
            messagebox.showwarning("Alerta", "Complete todos los campos")
            return
        
        if not self.biometria_ok:
            messagebox.showwarning("Alerta", "Debe capturar la biometria facial exitosamente primero")
            return
        
        if not (cc.isdigit() and 6 <= len(cc) <= 10):
            messagebox.showerror("Error", "Cedula invalida (6-10 digitos)")
            return
        
        if len(nom) < 3:
            messagebox.showerror("Error", "Nombre invalido")
            return
        
        self.frm_prog.pack(pady=10, padx=20, fill="x")
        self.lbl_prog.pack(pady=8)
        
        etapas = ["Conectando...", "Validando...", "Consultando...", 
                 "Verificando biometria...", "Analizando...", "Finalizando..."]
        self.procesar(etapas, 0, nom, cc)
    
    def procesar(self, etapas, i, nom, cc):
        if i < len(etapas):
            self.lbl_prog.config(text=etapas[i])
            self.ventana.after(400, lambda: self.procesar(etapas, i+1, nom, cc))
        else:
            self.frm_prog.pack_forget()
            self.mostrar(nom, cc)
    
    def mostrar(self, nom, cc):
        for w in self.resultado.winfo_children():
            w.destroy()
        
        p = self.usuarios.get(cc)
        
        if p and p['nombre'].lower() == nom.lower():
            riesgo = p['fraude'] + random.random() * 0.05
            fraude = riesgo > 0.15
            
            if fraude:
                alerta = tk.Frame(self.resultado, bg="#991b1b", bd=3, relief="solid")
                alerta.pack(fill="x", padx=10, pady=10)
                tk.Label(alerta, text="ALERTA DE FRAUDE", font=("Arial", 16, "bold"), 
                        bg="#991b1b", fg="#fca5a5").pack(pady=10)
                tk.Label(alerta, text=f"Riesgo: {riesgo*100:.1f}%", font=("Arial", 10), 
                        bg="#991b1b", fg="white").pack(pady=5)
            
            color = "#991b1b" if fraude else "#065f46"
            titulo = "CON ALERTA" if fraude else "EXITOSA"
            
            exito = tk.Frame(self.resultado, bg=color, bd=3, relief="solid")
            exito.pack(fill="x", padx=10, pady=10)
            tk.Label(exito, text=f"VERIFICACION {titulo}", font=("Arial", 18, "bold"), 
                    bg=color, fg="#fbbf24").pack(pady=12)
            tk.Label(exito, text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
                    font=("Arial", 9), bg=color, fg="white").pack(pady=5)
            
            info = tk.Frame(self.resultado, bg="#1a0033", bd=2, relief="solid")
            info.pack(fill="both", expand=True, padx=10, pady=10)
            
            if cc in self.fotos:
                tk.Label(info, image=self.fotos[cc], bg="#1a0033").pack(pady=12)
            
            tk.Label(info, text=p['nombre'], font=("Arial", 18, "bold"), 
                    bg="#1a0033", fg="white").pack(pady=5)
            tk.Label(info, text=p['ocupacion'], font=("Arial", 11), 
                    bg="#1a0033", fg="#9333ea").pack(pady=3)
            tk.Label(info, text=f"CC: {cc}", font=("Arial", 10, "bold"), 
                    bg="#1a0033", fg="#00ffff").pack(pady=5)
            
            firma = tk.Frame(info, bg="#2d1b4e", bd=1)
            firma.pack(fill="x", padx=12, pady=8)
            tk.Label(firma, text="Firma:", font=("Arial", 9, "bold"), 
                    bg="#2d1b4e", fg="#888").pack(pady=3)
            tk.Label(firma, text=p['firma'], font=("Brush Script MT", 14, "italic"), 
                    bg="#2d1b4e", fg="white").pack(pady=3)
            
            tk.Label(info, text="REGISTRO CIVIL", font=("Arial", 12, "bold"), 
                    bg="#1a0033", fg="#fbbf24").pack(pady=(10,5))
            
            datos = [
                ("Nacimiento", p['nacimiento']), ("Edad", f"{p['edad']} anos"),
                ("Lugar Nac.", p['lugar_nac']), ("Genero", p['genero']),
                ("Estado Civil", p['civil']), ("Madre", p['madre']),
                ("Padre", p['padre']), ("Ciudad", p['ciudad']),
                ("Direccion", p['direccion']), ("Estatura", p['estatura']),
                ("Ojos", p['ojos']), ("Sangre", p['sangre']),
                ("Rasgos", p['rasgos']), ("Telefono", p['tel'])
            ]
            
            for lbl, val in datos:
                row = tk.Frame(info, bg="#2d1b4e")
                row.pack(fill="x", padx=12, pady=1)
                tk.Label(row, text=f"{lbl}:", font=("Arial", 9, "bold"), 
                        bg="#2d1b4e", fg="#888", width=14, anchor="w").pack(side="left", padx=5, pady=4)
                tk.Label(row, text=val, font=("Arial", 9), 
                        bg="#2d1b4e", fg="white", anchor="w").pack(side="left", padx=5, pady=4)
        else:
            err = tk.Frame(self.resultado, bg="#991b1b", bd=3, relief="solid")
            err.pack(fill="both", expand=True, padx=10, pady=10)
            tk.Label(err, text="VERIFICACION FALLIDA", font=("Arial", 20, "bold"), 
                    bg="#991b1b", fg="#fca5a5").pack(pady=100)
            msg = "Datos no coinciden" if p else "Documento no encontrado"
            tk.Label(err, text=msg, font=("Arial", 12), 
                    bg="#991b1b", fg="white").pack(pady=15)
    
    def limpiar(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_cedula.delete(0, tk.END)
        self.biometria_ok = False
        self.lbl_cam.config(text="Camara inactiva\nPresione para escanear", 
                           fg="#666", font=("Arial", 12))
        self.frm_prog.pack_forget()
        self.inicial()

if __name__ == "__main__":
    ventana = tk.Tk()
    app = SistemaVerificacion(ventana)
    ventana.mainloop()