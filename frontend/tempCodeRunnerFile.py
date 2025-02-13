import customtkinter as ctk
from tkinter import messagebox
import sqlite3

# Importação opcional para futuras referências (não está em uso neste exemplo)
from backend import listar_produtos  

# Configuração do tema do CustomTkinter
ctk.set_appearance_mode("dark")  # Modo escuro
ctk.set_default_color_theme("blue")

# URL base da API (não utilizada neste exemplo)
BASE_URL = "http://127.0.0.1:8000/api"


# ===============================
# FUNÇÕES DE BANCO DE DADOS
# ===============================
def inicializar_banco_usuarios():
    try:
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            );
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao inicializar o banco de dados: {e}")


def cadastrar_usuario():
    usuario = campo_usuario.get().strip()
    senha = campo_senha.get().strip()
    if not usuario or not senha:
        messagebox.showwarning("Aviso", "Preencha os campos de usuário e senha!")
        return
    try:
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,))
        if cursor.fetchone():
            messagebox.showwarning("Aviso", "Usuário já existe!")
        else:
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao cadastrar usuário: {e}")
    finally:
        conn.close()
    campo_usuario.delete(0, ctk.END)
    campo_senha.delete(0, ctk.END)


def validar_login():
    usuario = campo_usuario.get().strip()
    senha = campo_senha.get().strip()
    if not usuario or not senha:
        resultado_log.configure(text="Preencha os campos de usuário e senha!", text_color="red")
        return
    try:
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
        if cursor.fetchone():
            resultado_log.configure(text="Login feito com sucesso", text_color="green")
            janela_login.withdraw()  # Esconde a janela de login
            abrir_menu_principal()
        else:
            resultado_log.configure(text="Usuário ou senha incorretos", text_color="red")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao validar login: {e}")
    finally:
        conn.close()


# ===============================
# FUNÇÕES DE UTILIDADE PARA A INTERFACE
# ===============================
def limpar_janela(janela):
    for widget in janela.winfo_children():
        widget.destroy()


def voltar_menu_principal(janela):
    limpar_janela(janela)
    abrir_menu_principal()


# ===============================
# TELA DE MENU PRINCIPAL
# ===============================
def abrir_menu_principal():
    global janela_menu
    if 'janela_menu' not in globals():
        janela_menu = ctk.CTkToplevel()
        janela_menu.title("OnTech System - Menu Principal")
        janela_menu.geometry("1200x700")
        janela_menu.minsize(1200, 700)
    else:
        limpar_janela(janela_menu)

    # Configura layout responsivo
    janela_menu.grid_rowconfigure(0, weight=1)
    janela_menu.grid_columnconfigure((0, 1, 2), weight=1)

    # Botão PDV (Verde)
    botao_pdv = ctk.CTkButton(
        janela_menu, 
        text="PDV", 
        command=lambda: abrir_tela(janela_menu, "PDV"), 
        width=200, 
        height=200, 
        fg_color="#4CAF50"
    )
    botao_pdv.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Botão Estoque (Azul)
    botao_estoque = ctk.CTkButton(
        janela_menu, 
        text="Estoque", 
        command=lambda: abrir_tela(janela_menu, "Estoque"), 
        width=200, 
        height=200, 
        fg_color="#2196F3"
    )
    botao_estoque.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # Botão Clientes (Amarelo)
    botao_clientes = ctk.CTkButton(
        janela_menu, 
        text="Clientes", 
        command=lambda: abrir_tela(janela_menu, "Clientes"), 
        width=200, 
        height=200, 
        fg_color="#FFC107"
    )
    botao_clientes.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")


def abrir_tela(janela, tela):
    limpar_janela(janela)
    if tela == "PDV":
        abrir_pdv(janela)
    elif tela == "Estoque":
        abrir_estoque(janela)
    elif tela == "Clientes":
        abrir_clientes(janela)


# ===============================
# TELA DE PDV
# ===============================
def abrir_pdv(janela):
    limpar_janela(janela)
    # Título da tela PDV
    label = ctk.CTkLabel(janela, text="PDV", font=("Arial", 20))
    label.grid(row=0, column=0, columnspan=3, pady=20)
    
    # Aqui você pode adicionar os demais elementos da tela de PDV
    # Por exemplo, campos de entrada, botões de operação, etc.

    # Botão Voltar
    botao_voltar = ctk.CTkButton(janela, text="Voltar", command=lambda: voltar_menu_principal(janela))
    botao_voltar.grid(row=4, column=0, columnspan=3, pady=10)


# ===============================
# TELA DE ESTOQUE
# ===============================
def abrir_estoque(janela):
    limpar_janela(janela)

    # Título da tela de Estoque
    label = ctk.CTkLabel(janela, text="Estoque - Gerenciamento de Produtos", font=("Arial", 20))
    label.grid(row=0, column=0, columnspan=3, pady=20)

    produtos_estoque = []  # Lista que armazenará os produtos

    def atualizar_lista():
        lista_produtos.configure(state="normal")  # Habilita edição
        lista_produtos.delete("0.0", ctk.END)  # Limpa o conteúdo
        for produto in produtos_estoque:
            lista_produtos.insert(ctk.END, f"{produto['nome']} - {produto['quantidade']} unidades - R${produto['preco']:.2f}\n")
        lista_produtos.configure(state="disabled")  # Desabilita edição

    def adicionar_produto():
        nome = entry_nome.get().strip()
        quantidade = entry_quantidade.get().strip()
        preco = entry_preco.get().strip()

        if not nome or not quantidade or not preco:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            quantidade = int(quantidade)
            preco = float(preco)
            if quantidade <= 0 or preco <= 0:
                raise ValueError("Quantidade e preço devem ser números positivos.")
        except ValueError as e:
            messagebox.showwarning("Aviso", str(e))
            return

        produtos_estoque.append({"nome": nome, "quantidade": quantidade, "preco": preco})
        atualizar_lista()

        # Limpa os campos de entrada
        entry_nome.delete(0, ctk.END)
        entry_quantidade.delete(0, ctk.END)
        entry_preco.delete(0, ctk.END)

    # Criação do frame para os campos de entrada
    frame_campos = ctk.CTkFrame(janela)
    frame_campos.grid(row=1, column=0, columnspan=3, pady=10)

    label_nome = ctk.CTkLabel(frame_campos, text="Nome:")
    label_nome.grid(row=0, column=0, padx=5, pady=5)
    entry_nome = ctk.CTkEntry(frame_campos, placeholder_text="Nome do Produto")
    entry_nome.grid(row=0, column=1, padx=5, pady=5)

    label_quantidade = ctk.CTkLabel(frame_campos, text="Quantidade:")
    label_quantidade.grid(row=1, column=0, padx=5, pady=5)
    entry_quantidade = ctk.CTkEntry(frame_campos, placeholder_text="Quantidade")
    entry_quantidade.grid(row=1, column=1, padx=5, pady=5)

    label_preco = ctk.CTkLabel(frame_campos, text="Preço:")
    label_preco.grid(row=2, column=0, padx=5, pady=5)
    entry_preco = ctk.CTkEntry(frame_campos, placeholder_text="Preço")
    entry_preco.grid(row=2, column=1, padx=5, pady=5)

    botao_adicionar = ctk.CTkButton(frame_campos, text="Adicionar Produto", command=adicionar_produto)
    botao_adicionar.grid(row=3, column=0, columnspan=2, pady=10)

    # Caixa de texto para exibir os produtos adicionados
    lista_produtos = ctk.CTkTextbox(janela, height=200, width=400, state="disabled")
    lista_produtos.grid(row=2, column=0, columnspan=3, pady=10)

    # Função para calcular o valor total do estoque
    def calcular_total_estoque():
        total = sum(produto["quantidade"] * produto["preco"] for produto in produtos_estoque)
        label_total.configure(text=f"Valor Total do Estoque: R${total:.2f}")

    botao_calcular = ctk.CTkButton(janela, text="Calcular Valor Total", command=calcular_total_estoque)
    botao_calcular.grid(row=3, column=0, pady=10)

    label_total = ctk.CTkLabel(janela, text="Valor Total do Estoque: R$0.00", font=("Arial", 16))
    label_total.grid(row=3, column=1, pady=10)

    botao_voltar = ctk.CTkButton(janela, text="Voltar", command=lambda: voltar_menu_principal(janela))
    botao_voltar.grid(row=4, column=0, columnspan=3, pady=10)


# ===============================
# TELA DE CLIENTES
# ===============================
def abrir_clientes(janela):
    limpar_janela(janela)

    label = ctk.CTkLabel(janela, text="Clientes - Gerenciamento de Clientes", font=("Arial", 20))
    label.grid(row=0, column=0, columnspan=3, pady=20)

    clientes = []  # Lista para armazenar os clientes

    def atualizar_lista():
        lista_clientes.configure(state="normal")
        lista_clientes.delete("0.0", ctk.END)
        for cliente in clientes:
            lista_clientes.insert(ctk.END, f"{cliente['nome']} - {cliente['telefone']} - {cliente['endereco']}\n")
        lista_clientes.configure(state="disabled")

    def adicionar_cliente():
        nome = entry_nome.get().strip()
        telefone = entry_telefone.get().strip()
        endereco = entry_endereco.get().strip()

        if not nome or not telefone or not endereco:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        clientes.append({"nome": nome, "telefone": telefone, "endereco": endereco})
        atualizar_lista()

        entry_nome.delete(0, ctk.END)
        entry_telefone.delete(0, ctk.END)
        entry_endereco.delete(0, ctk.END)

    frame_campos = ctk.CTkFrame(janela)
    frame_campos.grid(row=1, column=0, columnspan=3, pady=10)

    label_nome = ctk.CTkLabel(frame_campos, text="Nome:")
    label_nome.grid(row=0, column=0, padx=5, pady=5)
    entry_nome = ctk.CTkEntry(frame_campos, placeholder_text="Nome do Cliente")
    entry_nome.grid(row=0, column=1, padx=5, pady=5)

    label_telefone = ctk.CTkLabel(frame_campos, text="Telefone:")
    label_telefone.grid(row=1, column=0, padx=5, pady=5)
    entry_telefone = ctk.CTkEntry(frame_campos, placeholder_text="Telefone")
    entry_telefone.grid(row=1, column=1, padx=5, pady=5)

    label_endereco = ctk.CTkLabel(frame_campos, text="Endereço:")
    label_endereco.grid(row=2, column=0, padx=5, pady=5)
    entry_endereco = ctk.CTkEntry(frame_campos, placeholder_text="Endereço")
    entry_endereco.grid(row=2, column=1, padx=5, pady=5)

    botao_adicionar = ctk.CTkButton(frame_campos, text="Adicionar Cliente", command=adicionar_cliente)
    botao_adicionar.grid(row=3, column=0, columnspan=2, pady=10)

    lista_clientes = ctk.CTkTextbox(janela, height=200, width=400, state="disabled")
    lista_clientes.grid(row=2, column=0, columnspan=3, pady=10)

    botao_voltar = ctk.CTkButton(janela, text="Voltar", command=lambda: voltar_menu_principal(janela))
    botao_voltar.grid(row=3, column=0, columnspan=3, pady=10)


# ===============================
# JANELA DE LOGIN
# ===============================
janela_login = ctk.CTk()
janela_login.title("OnTech System - Login")
janela_login.geometry("400x300")

label_usuario = ctk.CTkLabel(janela_login, text="Usuário")
label_usuario.pack(pady=10)
campo_usuario = ctk.CTkEntry(janela_login, placeholder_text="Digite seu Usuário")
campo_usuario.pack(pady=10)

label_senha = ctk.CTkLabel(janela_login, text="Senha")
label_senha.pack(pady=10)
campo_senha = ctk.CTkEntry(janela_login, placeholder_text="Digite sua Senha", show="*")
campo_senha.pack(pady=10)

frame_botoes = ctk.CTkFrame(janela_login)
frame_botoes.pack(pady=10)

but_login = ctk.CTkButton(frame_botoes, text="Login", command=validar_login, width=70, height=20)
but_login.pack(side="left", padx=10)
but_cadastro = ctk.CTkButton(frame_botoes, text="Cadastrar", command=cadastrar_usuario, width=70, height=20)
but_cadastro.pack(side="left")

resultado_log = ctk.CTkLabel(janela_login, text="")
resultado_log.pack(pady=10)


# Inicializa o banco de dados e inicia a interface de login
inicializar_banco_usuarios()
janela_login.mainloop()
