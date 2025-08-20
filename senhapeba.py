# ==========================================================
# Senha Peba
# Autor: José Cleison de Lima
# Direitos autorais © 2025 José Cleison de Lima
# Todos os direitos reservados.
# ==========================================================

import tkinter as tk
from tkinter import messagebox
import secrets
import string
from PIL import Image, ImageTk  # pip install pillow

# Tentar usar pyperclip para copiar; se não tiver, cai fora graciosamente
try:
    import pyperclip
    HAS_PYPERCLIP = True
except Exception:
    HAS_PYPERCLIP = False

# === Variáveis globais ===
historico_senhas = []

# === lógica ===
def calcular_forca(senha: str) -> tuple[str, str, float]:
    if not senha:
        return ("", "white", 0.0)
    
    pontuacao = 0
    n = len(senha)
    if n >= 16: pontuacao += 3
    elif n >= 12: pontuacao += 2
    elif n >= 8: pontuacao += 1

    classes = [
        any(c.islower() for c in senha),
        any(c.isupper() for c in senha),
        any(c.isdigit() for c in senha),
        any(c in string.punctuation for c in senha),
    ]
    pontuacao += sum(classes)

    if pontuacao >= 6:
        return ("Muito forte ✅", "#2ecc71", 1.0)
    elif pontuacao >= 4:
        return ("Forte 👍", "#27ae60", 0.75)
    elif pontuacao >= 3:
        return ("Média 😬", "#f39c12", 0.5)
    else:
        return ("Fraca ❌", "#e74c3c", 0.25)

def adicionar_ao_historico(senha):
    if senha and senha not in historico_senhas:
        historico_senhas.append(senha)
        if len(historico_senhas) > 10:
            historico_senhas.pop(0)

def gerar_senha():
    tamanho = var_tamanho.get()
    usar_minus = var_minus.get()
    usar_maius = var_maius.get()
    usar_num = var_num.get()
    usar_simbolos = var_simbolos.get()

    pool = ""
    if usar_minus: pool += string.ascii_lowercase
    if usar_maius: pool += string.ascii_uppercase
    if usar_num: pool += string.digits
    if usar_simbolos: pool += string.punctuation

    if not pool:
        messagebox.showwarning("Aviso", "Selecione pelo menos um tipo de caractere.")
        return
    if tamanho < 4:
        messagebox.showwarning("Aviso", "Escolha um tamanho mínimo de 4.")
        return

    senha_chars = []
    if usar_minus: senha_chars.append(secrets.choice(string.ascii_lowercase))
    if usar_maius: senha_chars.append(secrets.choice(string.ascii_uppercase))
    if usar_num: senha_chars.append(secrets.choice(string.digits))
    if usar_simbolos: senha_chars.append(secrets.choice(string.punctuation))

    while len(senha_chars) < tamanho:
        senha_chars.append(secrets.choice(pool))

    # Embaralhar
    for i in range(len(senha_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        senha_chars[i], senha_chars[j] = senha_chars[j], senha_chars[i]

    senha = "".join(senha_chars)

    saida.config(state="normal")
    saida.delete(0, tk.END)
    saida.insert(0, senha)
    saida.config(state="readonly")

    txt, cor, forca = calcular_forca(senha)
    lbl_forca.config(text=f"Força: {txt}", fg=cor)
    atualizar_barra_forca(cor, forca)
    
    adicionar_ao_historico(senha)

def copiar():
    senha = saida.get()
    if not senha:
        messagebox.showinfo("Copiar", "Nada para copiar.")
        return
    if HAS_PYPERCLIP:
        pyperclip.copy(senha)
        messagebox.showinfo("Copiado", "Senha copiada para a área de transferência! 🧷")
    else:
        saida.config(state="normal")
        saida.selection_range(0, tk.END)
        saida.config(state="readonly")
        messagebox.showinfo("Atenção", "Instale 'pyperclip' para copiar automaticamente.\nUse Ctrl+C após o campo ficar selecionado.")

def limpar():
    saida.config(state="normal")
    saida.delete(0, tk.END)
    saida.config(state="readonly")
    lbl_forca.config(text="Força: ", fg="white")
    atualizar_barra_forca("white", 0.0)

def toggle_visibilidade():
    if var_ver.get():
        saida.config(show="")
    else:
        saida.config(show="•")

def atualizar_barra_forca(cor, porcentagem):
    canvas_forca.delete("all")
    canvas_forca.create_rectangle(0, 0, 300 * porcentagem, 10, fill=cor, outline="")

def mostrar_historico():
    if not historico_senhas:
        messagebox.showinfo("Histórico", "Nenhuma senha gerada ainda.")
        return
    
    historico_win = tk.Toplevel(janela)
    historico_win.title("Histórico de Senhas")
    historico_win.geometry("400x300")
    historico_win.config(bg="#e0e0e0")
    
    tk.Label(historico_win, text="Últimas senhas geradas:", font=fonte_normal, bg="#e0e0e0").pack(pady=10)
    
    frame_historico = tk.Frame(historico_win, bg="#e0e0e0")
    frame_historico.pack(fill="both", expand=True, padx=20, pady=10)
    
    for i, senha in enumerate(reversed(historico_senhas), 1):
        tk.Label(frame_historico, text=f"{i}. {senha}", font=("Consolas", 10), 
                bg="#e0e0e0", anchor="w").pack(fill="x", pady=2)

def exportar_senhas():
    if not historico_senhas:
        messagebox.showwarning("Exportar", "Nenhuma senha para exportar.")
        return
    
    from tkinter import filedialog
    arquivo = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )
    
    if arquivo:
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write("Histórico de Senhas - Senha Peba\n")
                f.write("=" * 40 + "\n")
                for i, senha in enumerate(reversed(historico_senhas), 1):
                    f.write(f"{i}. {senha}\n")
            messagebox.showinfo("Sucesso", f"Senhas exportadas para:\n{arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}")

def criar_menu_contextual(event):
    menu = tk.Menu(janela, tearoff=0)
    menu.add_command(label="Copiar", command=copiar)
    menu.add_command(label="Limpar", command=limpar)
    menu.add_separator()
    menu.add_command(label="Histórico", command=mostrar_historico)
    menu.add_command(label="Exportar", command=exportar_senhas)
    
    try:
        menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()

def hover_bind(widget, cor_base, cor_hover):
    widget.bind("<Enter>", lambda e: widget.config(bg=cor_hover))
    widget.bind("<Leave>", lambda e: widget.config(bg=cor_base))

# === UI ===
janela = tk.Tk()
janela.title("Senha Peba")
janela.geometry("540x520")
janela.minsize(500, 480)
janela.config(bg="#e0e0e0")

fonte_titulo = ("Segoe UI", 22, "bold italic")
fonte_normal = ("Segoe UI", 12)
cor_texto = "#1b1b1f"
cor_campo = "#f5f5f5"
cor_botao = "#ff6f61"       # laranja divertido
cor_botao_sec = "#6c5ce7"   # roxo moderno
cor_botao_destr = "#e74c3c" # vermelho
cor_botao_hist = "#00b894"  # verde

# Título estilizado
tk.Label(janela, text="🔑 Senha Peba", font=fonte_titulo, bg="#e0e0e0", fg="#d63031").pack(pady=(20,12))

# Frame de opções
frame = tk.Frame(janela, bg="#e0e0e0")
frame.pack(pady=5)

# Tamanho
tk.Label(frame, text="Tamanho:", font=fonte_normal, bg="#e0e0e0", fg=cor_texto).grid(row=0, column=0, sticky="w", padx=6, pady=6)
var_tamanho = tk.IntVar(value=12)
scale = tk.Scale(frame, from_=4, to=32, orient="horizontal", variable=var_tamanho,
                 bg="#e0e0e0", fg=cor_texto, troughcolor="#c0c0c0",
                 highlightthickness=0, length=260, relief="flat")
scale.grid(row=0, column=1, columnspan=3, padx=6, pady=6, sticky="we")

# Checkboxes
var_minus = tk.BooleanVar(value=True)
var_maius = tk.BooleanVar(value=True)
var_num = tk.BooleanVar(value=True)
var_simbolos = tk.BooleanVar(value=False)

chk_kwargs = dict(bg="#e0e0e0", fg=cor_texto, activebackground="#e0e0e0", selectcolor="#c0c0c0", font=fonte_normal)
tk.Checkbutton(frame, text="a-z", variable=var_minus, **chk_kwargs).grid(row=1, column=0, sticky="w", padx=6, pady=4)
tk.Checkbutton(frame, text="A-Z", variable=var_maius, **chk_kwargs).grid(row=1, column=1, sticky="w", padx=6, pady=4)
tk.Checkbutton(frame, text="0-9", variable=var_num, **chk_kwargs).grid(row=1, column=2, sticky="w", padx=6, pady=4)
tk.Checkbutton(frame, text="Símbolos", variable=var_simbolos, **chk_kwargs).grid(row=1, column=3, sticky="w", padx=6, pady=4)

# Saída (senha)
tk.Label(janela, text="Senha:", font=fonte_normal, bg="#e0e0e0", fg=cor_texto).pack(pady=(10, 2))
saida = tk.Entry(
    janela, font=("Consolas", 14), width=34, relief="flat",
    bg=cor_campo, fg=cor_texto, insertbackground=cor_texto,
    readonlybackground=cor_campo, state="readonly", show="•"
)
saida.pack(pady=4)
saida.bind("<Button-3>", criar_menu_contextual)

# Mostrar/ocultar
var_ver = tk.BooleanVar(value=False)
chk_ver = tk.Checkbutton(janela, text="Mostrar senha", variable=var_ver,
                         command=toggle_visibilidade, bg="#e0e0e0", fg=cor_texto,
                         activebackground="#e0e0e0", selectcolor="#c0c0c0", font=("Segoe UI", 10))
chk_ver.pack()

# Indicador de força
lbl_forca = tk.Label(janela, text="Força: ", font=fonte_normal, bg="#e0e0e0", fg="white")
lbl_forca.pack(pady=6)

# Barra de força
canvas_forca = tk.Canvas(janela, width=300, height=10, bg="#e0e0e0", highlightthickness=0)
canvas_forca.pack(pady=2)

# Botões
btns = tk.Frame(janela, bg="#e0e0e0")
btns.pack(pady=8)

btn_gerar = tk.Button(btns, text="Gerar", font=fonte_normal, bg=cor_botao, fg="white", relief="flat", command=gerar_senha, padx=14, pady=6)
btn_gerar.grid(row=0, column=0, padx=6)
hover_bind(btn_gerar, cor_botao, "#e05550")

btn_copiar = tk.Button(btns, text="Copiar", font=fonte_normal, bg=cor_botao_sec, fg="white", relief="flat", command=copiar, padx=14, pady=6)
btn_copiar.grid(row=0, column=1, padx=6)
hover_bind(btn_copiar, cor_botao_sec, "#5a4ed1")

btn_limpar = tk.Button(btns, text="Limpar", font=fonte_normal, bg=cor_botao_destr, fg="white", relief="flat", command=limpar, padx=14, pady=6)
btn_limpar.grid(row=0, column=2, padx=6)
hover_bind(btn_limpar, cor_botao_destr, "#c0392b")

btn_historico = tk.Button(btns, text="Histórico", font=fonte_normal, bg=cor_botao_hist, fg="white", relief="flat", command=mostrar_historico, padx=14, pady=6)
btn_historico.grid(row=0, column=3, padx=6)
hover_bind(btn_historico, cor_botao_hist, "#00a07a")

# rodapé
tk.Label(janela, text="© 2025 José Cleison de Lima.",
         font=("Segoe UI", 9), bg="#e0e0e0", fg="#7f8c8d").pack(side="bottom", pady=6)

janela.mainloop()
