import tkinter as tk
from tkinter import messagebox
import random
import sqlite3

# =========================
# BANCO DE DADOS
# =========================

conn = sqlite3.connect("pontoplay.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    telefone TEXT,
    email TEXT,
    senha TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS estatisticas (
    id INTEGER PRIMARY KEY,
    acessos INTEGER,
    partidas INTEGER,
    jackpots INTEGER,
    arrecadado INTEGER
)
""")

cursor.execute("""
INSERT OR IGNORE INTO estatisticas
(id, acessos, partidas, jackpots, arrecadado)
VALUES (1,0,0,0,0)
""")

conn.commit()

# =========================
# CONFIGURAÇÕES
# =========================

SIMBOLOS = ['💰', '💲', '🔝', '🎲', '💣', '🔞', '💸']

credits = 100

ADM_EMAIL = "admin@pontoplay.com"
ADM_SENHA = "123456"

usuario_atual = ""

# CORES
PRETO = "#0d0d0d"
AZUL = "#045d98"
BRANCO = "#ECEBE6"
AZUL = "#025487"
CINZA = "#1a1a1a"
BRANCO = "white"

# =========================
# FUNÇÕES
# =========================


def atualizar_creditos():
    label_creditos.config(text=f"💰 CRÉDITOS: {credits}")


# =========================
# PAINEL ADMIN
# =========================


def abrir_painel_admin():

    painel = tk.Toplevel(janela)
    painel.title("PAINEL ADM")
    painel.geometry("500x500")
    painel.config(bg=PRETO)

    cursor.execute("SELECT * FROM estatisticas WHERE id=1")
    stats = cursor.fetchone()

    acessos = stats[1]
    partidas = stats[2]
    jackpots = stats[3]
    arrecadado = stats[4]

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = cursor.fetchone()[0]

    titulo = tk.Label(
        painel,
        text="👑 PAINEL ADMINISTRADOR",
        font=("Arial Black", 24, "bold"),
        bg=PRETO,
        fg=BRANCO
    )

    titulo.pack(pady=30)

    infos = [
        f"👥 Usuários cadastrados: {total_usuarios}",
        f"📈 Acessos ao sistema: {acessos}",
        f"🎲 Partidas jogadas: {partidas}",
        f"🏆 Jackpots: {jackpots}",
        f"💸 Créditos arrecadados: {arrecadado}"
    ]

    for info in infos:
        tk.Label(
            painel,
            text=info,
            font=("Arial", 16, "bold"),
            bg=PRETO,
            fg=BRANCO
        ).pack(pady=12)


# =========================
# CADASTRO
# =========================


def cadastrar():

    global usuario_atual

    nome = entry_nome.get()
    telefone = entry_telefone.get()
    email = entry_email.get()
    senha = entry_senha.get()

    if not nome or not telefone or not email or not senha:
        messagebox.showwarning("Erro", "Preencha todos os campos!")
        return

    if email == ADM_EMAIL and senha == ADM_SENHA:
        abrir_painel_admin()
        return

    cursor.execute("""
    INSERT INTO usuarios
    (nome, telefone, email, senha)
    VALUES (?, ?, ?, ?)
    """, (nome, telefone, email, senha))

    conn.commit()

    usuario_atual = nome

    cursor.execute("""
    UPDATE estatisticas
    SET acessos = acessos + 1
    WHERE id=1
    """)

    conn.commit()

    usuario_label.config(text=f"👤 {usuario_atual}")

    messagebox.showinfo(
        "Sucesso",
        f"Bem-vindo {nome}!"
    )

    tela_cadastro.pack_forget()
    tela_jogo.pack(fill="both", expand=True)


# =========================
# HOVER BOTÃO
# =========================


def hover_entrar(e):
    btn_girar['bg'] = '#00ff99'



def hover_sair(e):
    btn_girar['bg'] = AZUL


# =========================
# GIRAR SLOT
# =========================


def girar():

    global credits

    if credits < 10:
        messagebox.showwarning(
            "Erro",
            "❌ Sem créditos!"
        )
        return

    credits -= 10

    for i in range(25):

        label1.config(text=random.choice(SIMBOLOS))
        label2.config(text=random.choice(SIMBOLOS))
        label3.config(text=random.choice(SIMBOLOS))

        janela.update()
        janela.after(60)

    resultado = [random.choice(SIMBOLOS) for _ in range(3)]

    label1.config(text=resultado[0])
    label2.config(text=resultado[1])
    label3.config(text=resultado[2])

    cursor.execute("""
    UPDATE estatisticas
    SET partidas = partidas + 1,
        arrecadado = arrecadado + 10
    WHERE id=1
    """)

    # JACKPOT
    if resultado[0] == resultado[1] == resultado[2]:

        credits += 100

        cursor.execute("""
        UPDATE estatisticas
        SET jackpots = jackpots + 1
        WHERE id=1
        """)

        status.config(
            text="🎉 JACKPOT +100",
            fg=AZUL
        )

    # DOIS IGUAIS
    elif (
        resultado[0] == resultado[1]
        or resultado[0] == resultado[2]
        or resultado[1] == resultado[2]
    ):

        credits += 30

        status.config(
            text="🔥 DOIS IGUAIS +30",
            fg=AZUL
        )

    else:

        status.config(
            text="❌ VOCÊ PERDEU",
            fg=AZUL
        )

    conn.commit()

    atualizar_creditos()


# =========================
# JANELA PRINCIPAL
# =========================

janela = tk.Tk()

janela.title("🎰 PONTOPLAY FORTUNE ")
janela.geometry("1200x800")
janela.config(bg=PRETO)


# =========================
# TELA LOGIN
# =========================


tela_cadastro = tk.Frame(janela, bg=PRETO)
tela_cadastro.pack(fill="both", expand=True)


# TÍTULO

titulo = tk.Label(
    tela_cadastro,
    text="🎰 PONTOPLAY FORTUNE 🎰",
    font=("Arial Black", 38, "bold"),
    bg=PRETO,
    fg=BRANCO
)

titulo.pack(pady=40)


# ENTRADAS


def criar_entry(texto):

    entry = tk.Entry(
        tela_cadastro,
        width=35,
        font=("Arial", 18),
        bg=CINZA,
        fg=BRANCO,
        insertbackground=BRANCO,
        relief="flat",
        justify="center"
    )

    entry.pack(pady=12, ipady=10)
    entry.insert(0, texto)

    return entry


entry_nome = criar_entry("Nome")
entry_telefone = criar_entry("Telefone")
entry_email = criar_entry("E-mail")
entry_senha = criar_entry("Senha")


# BOTÃO LOGIN

btn_cadastro = tk.Button(
    tela_cadastro,
    text="🎲 ENTRAR",
    command=cadastrar,
    bg=AZUL,
    fg="black",
    font=("Arial Black", 18, "bold"),
    width=20,
    height=2,
    relief="flat",
    cursor="hand2"
)

btn_cadastro.pack(pady=30)


# =========================
# TELA JOGO
# =========================


tela_jogo = tk.Frame(janela, bg=PRETO)


# MENU SUPERIOR

menu_topo = tk.Frame(
    tela_jogo,
    bg=CINZA,
    height=70
)

menu_topo.pack(fill="x")


usuario_label = tk.Label(
    menu_topo,
    text="👤 Jogador",
    font=("Arial", 16, "bold"),
    bg=CINZA,
    fg=BRANCO
)

usuario_label.pack(side="left", padx=20)


btn_deposito = tk.Button(
    menu_topo,
    text="💸 DEPOSITAR",
    bg=AZUL,
    fg="black",
    font=("Arial Black", 12, "bold"),
    relief="flat",
    cursor="hand2"
)

btn_deposito.pack(side="right", padx=20, pady=10)


# TÍTULO JOGO


titulo_jogo = tk.Label(
    tela_jogo,
    text="🎰 SLOT MACHINE 🎰",
    font=("Arial Black", 32, "bold"),
    bg=PRETO,
    fg=BRANCO
)

titulo_jogo.pack(pady=30)


# FRAME SLOTS

frame_slots = tk.Frame(
    tela_jogo,
    bg=PRETO
)

frame_slots.pack(pady=40)


# SLOT LABELS


def criar_slot(coluna):

    label = tk.Label(
        frame_slots,
        text="❔",
        font=("Arial", 100, "bold"),
        bg=CINZA,
        fg=BRANCO,
        width=2,
        height=1,
        relief="solid",
        bd=4
    )

    label.grid(row=0, column=coluna, padx=15)

    return label


label1 = criar_slot(0)
label2 = criar_slot(1)
label3 = criar_slot(2)


# BOTÃO GIRAR

btn_girar = tk.Button(
    tela_jogo,
    text="🎲 GIRAR",
    command=girar,
    font=("Arial Black", 22, "bold"),
    bg=AZUL,
    fg="black",
    width=20,
    height=2,
    relief="flat",
    cursor="hand2"
)

btn_girar.pack(pady=30)

btn_girar.bind("<Enter>", hover_entrar)
btn_girar.bind("<Leave>", hover_sair)


# STATUS

status = tk.Label(
    tela_jogo,
    text="🔥 Boa sorte!",
    font=("Arial", 20, "bold"),
    bg=PRETO,
    fg=BRANCO
)

status.pack(pady=15)


# CRÉDITOS

label_creditos = tk.Label(
    tela_jogo,
    text=f"💰 CRÉDITOS: {credits}",
    font=("Arial Black", 28, "bold"),
    bg=PRETO,
    fg=BRANCO
)

label_creditos.pack(pady=20)


# =========================
# INICIAR
# =========================

janela.mainloop()