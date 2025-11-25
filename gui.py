import tkinter as tk
from tkinter import messagebox, ttk
from servicos import SistemaReservas


class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reservas - Hotel")
        self.root.geometry("720x480")

        self.sistema = SistemaReservas()

        self.frame_principal = tk.Frame(self.root)
        self.frame_principal.pack(fill="both", expand=True)

        self.montar_menu()

    # ---------------------------------------------------
    # MENU PRINCIPAL
    # ---------------------------------------------------
    def montar_menu(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        tk.Label(self.frame_principal, text="Sistema de Reservas",
                 font=("Arial", 20)).pack(pady=20)

        botoes = [
            ("Cadastrar Cliente", self.tela_cadastrar_cliente),
            ("Cadastrar Quarto", self.tela_cadastrar_quarto),
            ("Consultar Disponibilidade", self.tela_consultar_disponibilidade),
            ("Realizar Reserva", self.tela_realizar_reserva),
            ("Listar Reservas", self.tela_listar_reservas),
            ("Cancelar Reserva", self.tela_cancelar_reserva)
        ]

        for texto, comando in botoes:
            tk.Button(self.frame_principal, text=texto, width=30, height=2,
                      command=comando).pack(pady=5)

    # ---------------------------------------------------
    # TELA: CADASTRAR CLIENTE
    # ---------------------------------------------------
    def tela_cadastrar_cliente(self):
        self._limpar_frame()

        tk.Label(self.frame_principal, text="Cadastrar Cliente", font=("Arial", 16)).pack(pady=10)

        frame = tk.Frame(self.frame_principal)
        frame.pack()

        tk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="e")
        entry_nome = tk.Entry(frame)
        entry_nome.grid(row=0, column=1)

        tk.Label(frame, text="Documento:").grid(row=1, column=0, sticky="e")
        entry_doc = tk.Entry(frame)
        entry_doc.grid(row=1, column=1)

        tk.Label(frame, text="Email:").grid(row=2, column=0, sticky="e")
        entry_email = tk.Entry(frame)
        entry_email.grid(row=2, column=1)

        tk.Label(frame, text="Telefone:").grid(row=3, column=0, sticky="e")
        entry_tel = tk.Entry(frame)
        entry_tel.grid(row=3, column=1)

        def cadastrar():
            try:
                self.sistema.cadastrar_cliente(
                    entry_nome.get(),
                    entry_doc.get(),
                    entry_email.get(),
                    entry_tel.get()
                )
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(self.frame_principal, text="Cadastrar", command=cadastrar)\
            .pack(pady=20)

        tk.Button(self.frame_principal, text="Voltar", command=self.montar_menu)\
            .pack()

    # ---------------------------------------------------
    # TELA: CADASTRAR QUARTO
    # ---------------------------------------------------
    def tela_cadastrar_quarto(self):
        self._limpar_frame()

        tk.Label(self.frame_principal, text="Cadastrar Quarto", font=("Arial", 16)).pack(pady=10)

        frame = tk.Frame(self.frame_principal)
        frame.pack()

        tk.Label(frame, text="Número do Quarto:").grid(row=0, column=0)
        entry_num = tk.Entry(frame)
        entry_num.grid(row=0, column=1)

        tk.Label(frame, text="Tipo:").grid(row=1, column=0)
        entry_tipo = tk.Entry(frame)
        entry_tipo.grid(row=1, column=1)

        tk.Label(frame, text="Preço da Diária:").grid(row=2, column=0)
        entry_preco = tk.Entry(frame)
        entry_preco.grid(row=2, column=1)

        def cadastrar():
            try:
                self.sistema.cadastrar_quarto(
                    int(entry_num.get()),
                    entry_tipo.get(),
                    float(entry_preco.get())
                )
                messagebox.showinfo("Sucesso", "Quarto cadastrado!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(self.frame_principal, text="Cadastrar", command=cadastrar).pack(pady=20)
        tk.Button(self.frame_principal, text="Voltar", command=self.montar_menu).pack()

    # ---------------------------------------------------
    # TELA: CONSULTAR DISPONIBILIDADE
    # ---------------------------------------------------
    def tela_consultar_disponibilidade(self):
        self._limpar_frame()

        tk.Label(self.frame_principal, text="Consultar Disponibilidade", font=("Arial", 16)).pack(pady=10)

        disponiveis = self.sistema.consultar_disponibilidade()

        text = tk.Text(self.frame_principal, width=80, height=20)
        text.pack()

        if not disponiveis:
            text.insert(tk.END, "Nenhum quarto disponível.")
        else:
            for q in disponiveis:
                text.insert(tk.END, f"Quarto {q.numero} - {q.tipo} - R$ {q.precoDiaria:.2f}\n")

        tk.Button(self.frame_principal, text="Voltar", command=self.montar_menu).pack()

    # ---------------------------------------------------
    # TELA: REALIZAR RESERVA
    # ---------------------------------------------------
    def tela_realizar_reserva(self):
        self._limpar_frame()

        tk.Label(self.frame_principal, text="Realizar Reserva", font=("Arial", 16)).pack(pady=10)

        frame = tk.Frame(self.frame_principal)
        frame.pack()

        tk.Label(frame, text="ID do Cliente:").grid(row=0, column=0)
        entry_cliente = tk.Entry(frame)
        entry_cliente.grid(row=0, column=1)

        tk.Label(frame, text="Número do Quarto:").grid(row=1, column=0)
        entry_quarto = tk.Entry(frame)
        entry_quarto.grid(row=1, column=1)

        tk.Label(frame, text="Check-in (AAAA-MM-DD):").grid(row=2, column=0)
        entry_in = tk.Entry(frame)
        entry_in.grid(row=2, column=1)

        tk.Label(frame, text="Check-out (AAAA-MM-DD):").grid(row=3, column=0)
        entry_out = tk.Entry(frame)
        entry_out.grid(row=3, column=1)

        def reservar():
            try:
                self.sistema.realizar_reserva(
                    int(entry_cliente.get()),
                    int(entry_quarto.get()),
                    entry_in.get(),
                    entry_out.get()
                )
                messagebox.showinfo("Sucesso", "Reserva realizada!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(self.frame_principal, text="Reservar", command=reservar).pack(pady=20)
        tk.Button(self.frame_principal, text="Voltar", command=self.montar_menu).pack()

    # ---------------------------------------------------
    # TELA: LISTAR RESERVAS
    # ---------------------------------------------------
    def tela_listar_reservas(self):
        self._limpar_frame()

        tk.Label(self.frame_principal, text="Listar Reservas", font=("Arial", 16)).pack(pady=10)

        text = tk.Text(self.frame_principal, width=80, height=20)
        text.pack()

        reservas = self.sistema.listar_reservas()

        if not reservas:
            text.insert(tk.END, "Nenhuma reserva encontrada.\n")
        else:
            for r in reservas:
                text.insert(tk.END, f"Reserva {r.idReserva} | Cliente {r.cliente_id} | "
                                    f"Quarto {r.quarto.numero} | {r.dataCheckin} → {r.dataCheckout}\n")

        tk.Button(self.frame_principal, text="Voltar", command=self.montar_menu).pack()

    # ---------------------------------------------------
    # TELA: CANCELAR RESERVA
    # ---------------------------------------------------
    def tela_cancelar_reserva(self):
        self._limpar_frame()

        tk.Label(self.frame_principal, text="Cancelar Reserva", font=("Arial", 16)).pack(pady=10)

        frame = tk.Frame(self.frame_principal)
        frame.pack()

        tk.Label(frame, text="ID da Reserva:").grid(row=0, column=0)
        entry_id = tk.Entry(frame)
        entry_id.grid(row=0, column=1)

        def cancelar():
            try:
                self.sistema.cancelar_reserva(int(entry_id.get()))
                messagebox.showinfo("Sucesso", "Reserva cancelada!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(self.frame_principal, text="Cancelar", command=cancelar).pack(pady=20)
        tk.Button(self.frame_principal, text="Voltar", command=self.montar_menu).pack()

    # ---------------------------------------------------
    # Função para limpar tela antes de criar outra
    # ---------------------------------------------------
    def _limpar_frame(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()


# ---------------------------------------------------
# EXECUÇÃO
# ---------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()