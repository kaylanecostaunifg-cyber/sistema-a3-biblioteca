try:
    from importlib import import_module
    ctk = import_module("customtkinter")
except ModuleNotFoundError:
    import tkinter as _tk
    from tkinter import font as _font

    def _tk_options(options):
        options = dict(options)
        if "fg_color" in options:
            options["bg"] = options.pop("fg_color")
        if "text_color" in options:
            options["fg"] = options.pop("text_color")
        if "hover_color" in options:
            options.pop("hover_color")
        for option in ("corner_radius", "wraplength"):
            if option == "corner_radius":
                options.pop(option, None)
        return options

    class _Frame(_tk.Frame):
        def __init__(self, master=None, **options):
            super().__init__(master, **_tk_options(options))

    class _Label(_tk.Label):
        def __init__(self, master=None, **options):
            super().__init__(master, **_tk_options(options))

    class _Button(_tk.Button):
        def __init__(self, master=None, **options):
            super().__init__(master, **_tk_options(options))

    class _Toplevel(_tk.Toplevel):
        def configure(self, cnf=None, **options):
            super().configure(cnf, **_tk_options(options))

    class _TkCompat:
        CTkFrame = _Frame
        CTkLabel = _Label
        CTkButton = _Button
        CTkToplevel = _Toplevel

        @staticmethod
        def CTkFont(**options):
            return _font.Font(**options)

    ctk = _TkCompat()
from datetime import datetime, timedelta
from tkinter import messagebox
from dominio.modelos.aluno import Aluno

def abrir_detalhes_livro(app_principal, livro_obj):
    detalhes_modal = ctk.CTkToplevel(app_principal)
    detalhes_modal.title(f"Detalhes da Obra - {livro_obj.titulo}")
    detalhes_modal.geometry("780x500")
    detalhes_modal.grab_set()
    detalhes_modal.configure(fg_color="#E8E2D9")

    card_detalhes = ctk.CTkFrame(detalhes_modal, fg_color="#FAF8F5", corner_radius=12)
    card_detalhes.pack(padx=20, pady=20, fill="both", expand=True)

    # Lado esquerdo: Capa do Livro (Estilo Amazon)
    lbl_capa = ctk.CTkLabel(
        card_detalhes, 
        text="📖\n[Capa da Obra]", 
        width=180, height=260, 
        fg_color="#D0C9C0", 
        corner_radius=8,
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color="#4A1A21"
    )
    lbl_capa.pack(side="left", padx=20, pady=20)

    # Lado direito: Informações detalhadas
    info_frame = ctk.CTkFrame(card_detalhes, fg_color="transparent")
    info_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # Título e Autor
    ctk.CTkLabel(info_frame, text=livro_obj.titulo, font=ctk.CTkFont(size=22, weight="bold"), text_color="#4A1A21").pack(anchor="w", pady=(0, 2))
    ctk.CTkLabel(info_frame, text=f"Edição Português  |  por {livro_obj.autor} (Autor)", font=ctk.CTkFont(size=12), text_color="gray").pack(anchor="w", pady=(0, 10))

    # Sinopse descritiva
    sinopse_texto = (
        f"Escrito como um grande clássico da literatura, '{livro_obj.titulo}' é considerado uma das "
        "mais famosas obras de referência acadêmica. Nesta edição especial você tem o texto integral "
        "acompanhado de explicações, suporte a pesquisas e encartes para enriquecer o estudo."
    )
    ctk.CTkLabel(info_frame, text=sinopse_texto, font=ctk.CTkFont(size=11), text_color="#2C2C2C", wraplength=440, justify="left").pack(anchor="w", pady=(0, 15))

    # Dados Técnicos (ISBN, Edição, Editora, Data) - Igualzinho à imagem de referência
    grid_tec = ctk.CTkFrame(info_frame, fg_color="transparent")
    grid_tec.pack(anchor="w", pady=(0, 20))

    detalhes_tecnicos = [
        ("ISBN-13", livro_obj.isbn),
        ("Edição", "1ª"),
        ("Editora", "Editora Universitária"),
        ("Publicação", "3 Maio 2019")
    ]
    for i, (rotulo, valor) in enumerate(detalhes_tecnicos):
        col_frame = ctk.CTkFrame(grid_tec, fg_color="transparent")
        col_frame.grid(row=0, column=i, padx=10)
        ctk.CTkLabel(col_frame, text=rotulo, font=ctk.CTkFont(size=10, weight="bold"), text_color="gray").pack()
        ctk.CTkLabel(col_frame, text=valor, font=ctk.CTkFont(size=11), text_color="#2C2C2C").pack()

    # Botão de Solicitar Empréstimo na parte inferior
    def confirmar_emprestimo():
        cpf = app_principal.usuario_logado_dados.get("cpf")
        meus_ativos = [e for e in app_principal.repo_emprestimo.listar_todos() if e.usuario.id_usuario == cpf]
        
        if len(meus_ativos) >= 3:
            messagebox.showwarning("Limite Atingido", "Você atingiu o limite máximo de 3 empréstimos simultâneos (RF08).")
            return

        usr = Aluno(id_usuario=cpf, nome=app_principal.usuario_logado_dados["nome"], matricula=cpf, curso=app_principal.usuario_logado_dados["curso_colegio"])
        emp = app_principal.servico_emprestimo.realizar_emprestimo(usr, livro_obj)
        emp.data_devolucao_prevista = datetime.now() + timedelta(days=7)
        
        app_principal.repo_emprestimo.salvar(emp)
        messagebox.showinfo("Sucesso", f"Empréstimo de '{livro_obj.titulo}' realizado com sucesso!")
        detalhes_modal.destroy()
        app_principal.exibir_painel_acervo()

    ctk.CTkButton(
        info_frame, text="SOLICITAR EMPRÉSTIMO (RF07)", 
        fg_color="#4A1A21", hover_color="#6B232E",
        width=240, height=38, font=ctk.CTkFont(size=12, weight="bold"),
        command=confirmar_emprestimo
    ).pack(anchor="w")