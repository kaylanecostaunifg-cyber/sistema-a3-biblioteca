import os
import customtkinter as ctk  # type: ignore[reportMissingImports]
from PIL import Image, ImageOps, ImageDraw  # type: ignore[reportMissingImports]
from datetime import datetime, timedelta
from tkinter import messagebox, filedialog
import io
import urllib.request
from infra.banco import inicializar_banco

# Importações das Camadas de Infraestrutura e Domínio
from infra.repositorios.repositorio_usuario import RepositorioUsuarioSQLite
from infra.repositorios.repositorio_livro import RepositorioLivroSQLite
from infra.repositorios.repositorio_emprestimo import RepositorioEmprestimoSQLite
from dominio.modelos.aluno import Aluno
from dominio.modelos.livro import Livro
from dominio.servicos.servico_emprestimo import ServicoEmprestimo

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class AppBiblioteca(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Biblioteca Universitária - A3 (Gestão Integrada)")
        self.geometry("1180x720")
        self.configure(fg_color="#E8E2D9")

        # Persistência e Domínio
        self.repo_usuario = RepositorioUsuarioSQLite()
        self.repo_livro = RepositorioLivroSQLite()
        self.repo_emprestimo = RepositorioEmprestimoSQLite()
        self.servico_emprestimo = ServicoEmprestimo()

        # Paleta de Cores
        self.COR_VINHO_ESCURO = "#4A1A21"
        self.COR_VINHO_HOVER = "#6B232E"
        self.COR_CARD_BG = "#FAF8F5"
        self.COR_TEXTO = "#2C2C2C"

        self.caminho_avatar_padrao = self.criar_avatar_silhueta_exata()
        self.popular_acervo_inicial()

        # Base de credenciais para testes iniciais (RF02)
        self.credenciais_db = {
            "aluno@biblioteca.com": {
                "nome": "Estudante Exemplo",
                "cpf": "11111111111",
                "email": "aluno@biblioteca.com",
                "telefone": "81988881111",
                "curso_colegio": "Ciência da Computação",
                "senha": "123",
                "foto_path": self.caminho_avatar_padrao
            }
        }
        self.usuario_logado_dados = None
        self.exibir_tela_autenticacao(modo="login")

    def criar_avatar_silhueta_exata(self):
        """Gera programaticamente o avatar circular exato idêntico à imagem de referência (silhueta clássica)."""
        tamanho = (100, 100)
        img = Image.new("RGBA", tamanho, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        draw.ellipse((0, 0, 100, 100), fill="#E8E8E8")
        draw.ellipse((34, 22, 66, 54), fill="#B0B0B0")
        draw.chord((-15, 55, 115, 145), start=0, end=180, fill="#B0B0B0")
        
        caminho_temp = "assets_avatar_silhueta_exata.png"
        img.save(caminho_temp)
        return caminho_temp

    def popular_acervo_inicial(self):
        """Catalogação inicial de obras no acervo (RF04, RF05)."""
        livros_iniciais = [
            ("9788535902778", "Dom Casmurro", "Machado de Assis"),
            ("9788576653721", "O Alquimista", "Paulo Coelho"),
            ("9788535914849", "1984", "George Orwell"),
            ("9788576082675", "Código Limpo (Clean Code)", "Robert C. Martin")
        ]
        for isbn, titulo, autor in livros_iniciais:
            try:
                livro = Livro(id_livro=isbn, titulo=titulo, autor=autor, isbn=isbn)
                self.repo_livro.salvar(livro)
            except Exception:
                pass

    # ==========================================
    # 1. TELA DE LOGIN / CADASTRO (RF01, RF02, RF03)
    # ==========================================
    def exibir_tela_autenticacao(self, modo="login"):
        for widget in self.winfo_children():
            widget.destroy()
        
        frame_outer = ctk.CTkFrame(self, fg_color="transparent")
        frame_outer.pack(expand=True, fill="both", pady=20)
        
        self.card_auth = ctk.CTkFrame(
            frame_outer, 
            fg_color=self.COR_CARD_BG, 
            corner_radius=15,
            width=480,
            border_width=2,
            border_color=self.COR_VINHO_ESCURO
        )
        self.card_auth.pack(expand=True)

        if modo == "login":
            self.montar_form_login()
        elif modo == "cadastro":
            self.montar_form_cadastro()

    def montar_form_login(self):
        ctk.CTkLabel(
            self.card_auth, 
            text="Acesse sua Conta", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=self.COR_VINHO_ESCURO
        ).pack(pady=(25, 15))

        ctk.CTkLabel(self.card_auth, text="CPF ou E-mail:", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.COR_TEXTO).pack(anchor="w", padx=70, pady=(0, 2))
        self.txt_login_usr = ctk.CTkEntry(self.card_auth, width=340, height=38)
        self.txt_login_usr.pack(pady=(0, 10))

        ctk.CTkLabel(self.card_auth, text="Senha:", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.COR_TEXTO).pack(anchor="w", padx=70, pady=(0, 2))
        self.txt_login_senha = ctk.CTkEntry(self.card_auth, show="*", width=340, height=38)
        self.txt_login_senha.pack(pady=(0, 10))
        self.txt_login_senha.bind("<Return>", lambda e: self.validar_login())

        btn_entrar = ctk.CTkButton(
            self.card_auth, 
            text="ENTRAR", 
            fg_color=self.COR_VINHO_ESCURO, 
            hover_color=self.COR_VINHO_HOVER,
            width=340, height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.validar_login
        )
        btn_entrar.pack(pady=(10, 10))

        frame_links = ctk.CTkFrame(self.card_auth, fg_color="transparent")
        frame_links.pack(fill="x", padx=70, pady=(5, 25))

        ctk.CTkButton(
            frame_links, text="Criar Conta", fg_color="transparent",
            text_color=self.COR_VINHO_ESCURO, hover_color="#D6C2C5",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda: self.exibir_tela_autenticacao("cadastro")
        ).pack(side="left")

        ctk.CTkButton(
            frame_links, text="Esqueceu a senha?", fg_color="transparent",
            text_color="gray", hover_color="#D6C2C5",
            font=ctk.CTkFont(size=12, underline=True),
            command=self.abrir_modal_esqueceu_senha
        ).pack(side="right")

    def validar_login(self):
        usr = self.txt_login_usr.get().strip()
        senha = self.txt_login_senha.get().strip()
        if not usr or not senha:
            messagebox.showwarning("Aviso", "Preencha o usuário e a senha.")
            return

        usuario_encontrado = None
        for chave, dados in self.credenciais_db.items():
            if usr.lower() == dados["email"].lower() or usr == dados["cpf"]:
                usuario_encontrado = dados
                break

        if not usuario_encontrado or usuario_encontrado["senha"] != senha:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
            return

        self.usuario_logado_dados = usuario_encontrado
        self.iniciar_layout_dashboard()

    def montar_form_cadastro(self):
        scroll = ctk.CTkScrollableFrame(self.card_auth, fg_color="transparent", width=420, height=500)
        scroll.pack(padx=15, pady=15)

        ctk.CTkLabel(
            scroll, text="Cadastro de Usuário", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.COR_VINHO_ESCURO
        ).pack(pady=(5, 10))

        ctk.CTkLabel(scroll, text="Nome Completo (Mínimo nome e sobrenome):", font=ctk.CTkFont(size=11, weight="bold"), text_color=self.COR_TEXTO).pack(anchor="w", padx=10, pady=(4, 2))
        self.cad_nome = ctk.CTkEntry(scroll, width=360)
        self.cad_nome.pack(pady=(0, 6))

        ctk.CTkLabel(scroll, text="CPF:", font=ctk.CTkFont(size=11, weight="bold"), text_color=self.COR_TEXTO).pack(anchor="w", padx=10, pady=(4, 2))
        v_cpf = self.register(lambda text: text.isdigit() and len(text) <= 11 or text == "")
        self.cad_cpf = ctk.CTkEntry(scroll, width=360, validate="key", validatecommand=(v_cpf, '%P'))
        self.cad_cpf.pack(pady=(0, 6))

        ctk.CTkLabel(scroll, text="E-mail:", font=ctk.CTkFont(size=11, weight="bold"), text_color=self.COR_TEXTO).pack(anchor="w", padx=10, pady=(4, 2))
        self.cad_email = ctk.CTkEntry(scroll, width=360)
        self.cad_email.pack(pady=(0, 6))

        ctk.CTkLabel(scroll, text="Telefone (DDD):", font=ctk.CTkFont(size=11, weight="bold"), text_color=self.COR_TEXTO).pack(anchor="w", padx=10, pady=(4, 2))
        v_tel = self.register(lambda text: text.isdigit() and len(text) <= 11 or text == "")
        self.cad_telefone = ctk.CTkEntry(scroll, width=360, validate="key", validatecommand=(v_tel, '%P'))
        self.cad_telefone.pack(pady=(0, 6))

        self.var_aluno = ctk.BooleanVar(value=True)
        chk_aluno = ctk.CTkCheckBox(scroll, text="Estudante", variable=self.var_aluno, command=self.alternar_curso_estado, text_color=self.COR_TEXTO, fg_color=self.COR_VINHO_ESCURO)
        chk_aluno.pack(anchor="w", padx=10, pady=8)

        ctk.CTkLabel(scroll, text="Graduação / Colégio: ", font=ctk.CTkFont(size=11, weight="bold"), text_color=self.COR_TEXTO).pack(anchor="w", padx=10, pady=(4, 2))
        self.cad_curso = ctk.CTkEntry(scroll, width=360)
        self.cad_curso.pack(pady=(0, 6))

        ctk.CTkLabel(scroll, text="Senha:", font=ctk.CTkFont(size=11, weight="bold"), text_color=self.COR_TEXTO).pack(anchor="w", padx=10, pady=(4, 2))
        frame_senha = ctk.CTkFrame(scroll, fg_color="#FFFFFF", corner_radius=6, border_width=1, border_color="#A0A0A0", width=360, height=38)
        frame_senha.pack(pady=(0, 2))
        frame_senha.pack_propagate(False)

        self.cad_senha = ctk.CTkEntry(frame_senha, show="*", border_width=0, fg_color="transparent", width=310)
        self.cad_senha.pack(side="left", padx=(5, 0))
        self.cad_senha.bind("<KeyRelease>", self.avaliar_forca_senha)

        self.senha_visivel = False
        btn_olho = ctk.CTkButton(
            frame_senha, text="👁️", width=35, fg_color="transparent", hover_color="#E0E0E0",
            text_color="#333333", font=ctk.CTkFont(size=14), command=lambda: self.toggle_senha_visibilidade(self.cad_senha, btn_olho)
        )
        btn_olho.pack(side="right", padx=2)

        self.lbl_forca = ctk.CTkLabel(scroll, text="Força da senha: Digite uma senha", font=ctk.CTkFont(size=11), text_color="gray")
        self.lbl_forca.pack(anchor="w", padx=10, pady=(0, 10))

        btn_salvar_cad = ctk.CTkButton(
            scroll, text="FINALIZAR CADASTRO", 
            fg_color=self.COR_VINHO_ESCURO, hover_color=self.COR_VINHO_HOVER,
            width=360, height=40, font=ctk.CTkFont(size=12, weight="bold"),
            command=self.salvar_cadastro
        )
        btn_salvar_cad.pack(pady=(10, 5))

        ctk.CTkButton(
            scroll, text="Voltar ao Login", fg_color="transparent", text_color="gray",
            command=lambda: self.exibir_tela_autenticacao("login")
        ).pack(pady=(0, 10))

    def alternar_curso_estado(self):
        if self.var_aluno.get():
            self.cad_curso.configure(state="normal")
        else:
            self.cad_curso.delete(0, "end")
            self.cad_curso.configure(state="disabled")

    def toggle_senha_visibilidade(self, campo_senha, botao_olho):
        if self.senha_visivel:
            campo_senha.configure(show="*")
            botao_olho.configure(text="👁️")
            self.senha_visivel = False
        else:
            campo_senha.configure(show="")
            botao_olho.configure(text="🔒")
            self.senha_visivel = True

    def avaliar_forca_senha(self, event=None):
        senha = self.cad_senha.get()
        if not senha:
            self.lbl_forca.configure(text="Força da senha: Digite uma senha", text_color="gray")
        elif len(senha) < 4 or senha.isdigit():
            self.lbl_forca.configure(text="Força da senha: 🔴 Fraca", text_color="#B22222")
        elif len(senha) < 6:
            self.lbl_forca.configure(text="Força da senha: 🟡 Média", text_color="#D9822B")
        else:
            self.lbl_forca.configure(text="Força da senha: 🟢 Forte", text_color="#2E8B57")

    def salvar_cadastro(self):
        nome = self.cad_nome.get().strip()
        cpf = self.cad_cpf.get().strip()
        email = self.cad_email.get().strip()
        telefone = self.cad_telefone.get().strip()
        curso = self.cad_curso.get().strip()
        senha = self.cad_senha.get().strip()

        if not (nome and cpf and email and senha):
            messagebox.showwarning("Aviso", "Preencha os campos obrigatórios.")
            return
        if len(nome.split()) < 2:
            messagebox.showerror("Nome Inválido", "Por favor, digite nome e sobrenome.")
            return
        if len(cpf) != 11:
            messagebox.showerror("CPF Inválido", "O CPF deve conter exatamente 11 números.")
            return
        if telefone and len(telefone) != 11:
            messagebox.showerror("Telefone Inválido", "O telefone deve conter exatamente 11 números (DDD + 9 dígitos).")
            return

        novo_usuario = {
            "nome": nome, "cpf": cpf, "email": email, "telefone": telefone,
            "is_aluno": self.var_aluno.get(), "curso_colegio": curso if self.var_aluno.get() else "Não Aluno",
            "senha": senha, "foto_path": self.caminho_avatar_padrao
        }
        self.credenciais_db[email] = novo_usuario
        self.credenciais_db[cpf] = novo_usuario
        self.usuario_logado_dados = novo_usuario
        self.exibir_popup_sucesso_cadastro(nome)

    def exibir_popup_sucesso_cadastro(self, nome):
        popup = ctk.CTkToplevel(self)
        popup.title("Sucesso")
        popup.geometry("360x160")
        popup.grab_set()
        popup.configure(fg_color="#E8E2D9")

        card = ctk.CTkFrame(popup, fg_color=self.COR_CARD_BG, corner_radius=10)
        card.pack(padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(card, text=" Cadastro realizado com sucesso!", font=ctk.CTkFont(size=14, weight="bold"), text_color=self.COR_VINHO_ESCURO).pack(pady=(25, 10))
        ctk.CTkLabel(card, text=f"Bem-vindo(a), {nome}!", text_color=self.COR_TEXTO).pack(pady=(0, 15))
        self.after(1400, lambda: [popup.destroy(), self.iniciar_layout_dashboard()])

    # ==========================================
    # 2. RECUPERAÇÃO DE SENHA (SMS / E-MAIL SIMULADO)
    # ==========================================
    def abrir_modal_esqueceu_senha(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Recuperação de Senha")
        modal.geometry("400x320")
        modal.grab_set()
        modal.configure(fg_color="#E8E2D9")

        card = ctk.CTkFrame(modal, fg_color=self.COR_CARD_BG, corner_radius=10)
        card.pack(padx=15, pady=15, fill="both", expand=True)

        ctk.CTkLabel(card, text="Recuperação de Senha", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.COR_VINHO_ESCURO).pack(pady=(15, 5))
        ctk.CTkLabel(card, text="Informe seu E-mail ou CPF:", font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(0, 5))
        
        txt_id_rec = ctk.CTkEntry(card, placeholder_text="E-mail ou CPF", width=320)
        txt_id_rec.pack(pady=5)

        ctk.CTkLabel(card, text="Como deseja receber o código?", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.COR_TEXTO).pack(pady=(10, 5))
        var_canal = ctk.StringVar(value="email")
        
        frame_radio = ctk.CTkFrame(card, fg_color="transparent")
        frame_radio.pack(pady=5)
        rb_email = ctk.CTkRadioButton(frame_radio, text="E-mail", variable=var_canal, value="email", text_color=self.COR_TEXTO, fg_color=self.COR_VINHO_ESCURO)
        rb_email.pack(side="left", padx=15)
        rb_sms = ctk.CTkRadioButton(frame_radio, text="SMS", variable=var_canal, value="sms", text_color=self.COR_TEXTO, fg_color=self.COR_VINHO_ESCURO)
        rb_sms.pack(side="right", padx=15)

        def avancar_para_codigo():
            identificacao = txt_id_rec.get().strip()
            if not identificacao:
                messagebox.showwarning("Aviso", "Digite seu e-mail ou CPF.")
                return
            canal = "E-mail" if var_canal.get() == "email" else "SMS"
            messagebox.showinfo("Código Enviado", f"Um código de verificação foi enviado via {canal}!")
            modal.destroy()
            self.abrir_modal_digitar_codigo_e_senha(identificacao)

        btn_enviar = ctk.CTkButton(card, text="AVANÇAR", fg_color=self.COR_VINHO_ESCURO, hover_color=self.COR_VINHO_HOVER, width=320, command=avancar_para_codigo)
        btn_enviar.pack(pady=15)

    def abrir_modal_digitar_codigo_e_senha(self, identificacao):
        modal = ctk.CTkToplevel(self)
        modal.title("Alterar Senha")
        modal.geometry("400x340")
        modal.grab_set()
        modal.configure(fg_color="#E8E2D9")

        card = ctk.CTkFrame(modal, fg_color=self.COR_CARD_BG, corner_radius=10)
        card.pack(padx=15, pady=15, fill="both", expand=True)

        ctk.CTkLabel(card, text="Redefinição de Senha", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.COR_VINHO_ESCURO).pack(pady=(15, 5))
        ctk.CTkLabel(card, text="Digite qualquer código recebido e a nova senha:", font=ctk.CTkFont(size=11), text_color="gray").pack(pady=(0, 10))

        txt_codigo = ctk.CTkEntry(card, placeholder_text="Código de Verificação", width=320)
        txt_codigo.pack(pady=5)
        txt_nova_senha = ctk.CTkEntry(card, placeholder_text="Nova Senha", show="*", width=320)
        txt_nova_senha.pack(pady=5)

        def salvar_nova_senha():
            codigo = txt_codigo.get().strip()
            nova_s = txt_nova_senha.get().strip()
            if not codigo or not nova_s:
                messagebox.showwarning("Aviso", "Preencha o código e a nova senha.")
                return

            usuario_encontrado = None
            for chave, dados in self.credenciais_db.items():
                if identificacao.lower() == dados["email"].lower() or identificacao == dados["cpf"]:
                    usuario_encontrado = dados
                    break
            if usuario_encontrado:
                usuario_encontrado["senha"] = nova_s
            else:
                for chave in self.credenciais_db:
                    self.credenciais_db[chave]["senha"] = nova_s

            messagebox.showinfo("Sucesso", "Sua senha foi alterada com sucesso! Faça login com a nova senha.")
            modal.destroy()

        btn_confirmar = ctk.CTkButton(card, text="CONFIRMAR NOVA SENHA", fg_color=self.COR_VINHO_ESCURO, hover_color=self.COR_VINHO_HOVER, width=320, command=salvar_nova_senha)
        btn_confirmar.pack(pady=15)

    # ==========================================
    # 3. PAINEL PRINCIPAL DO ALUNO 
    # ==========================================
    def carregar_avatar(self, path, tamanho=(32, 32)):
        if path and os.path.exists(path):
            try:
                img = Image.open(path).convert("RGBA")
                img = ImageOps.fit(img, tamanho, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
                mascara = Image.new("L", tamanho, 0)
                desenho = ImageDraw.Draw(mascara)
                desenho.ellipse((0, 0) + tamanho, fill=255)
                img_circular = Image.new("RGBA", tamanho, (0, 0, 0, 0))
                img_circular.paste(img, (0, 0), mascara)
                return ctk.CTkImage(light_image=img_circular, dark_image=img_circular, size=tamanho)
            except Exception:
                pass
        return None

    def iniciar_layout_dashboard(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_barra_lateral()
        self.criar_area_conteudo()
        self.exibir_painel_home()

    def criar_barra_lateral(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=self.COR_VINHO_ESCURO)
        sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(sidebar, text="📚 Biblioteca\nUniversitária", font=ctk.CTkFont(size=17, weight="bold"), text_color="#FFFFFF").pack(padx=20, pady=(25, 25))

        opcoes = [
            ("🏠 Painel Principal", self.exibir_painel_home),
            ("📖 Consultar Acervo", self.exibir_painel_acervo),
            ("🔄 Meus Empréstimos", self.exibir_painel_emprestimos)
        ]
        for texto, cmd in opcoes:
            ctk.CTkButton(
                sidebar, text=texto, anchor="w", fg_color="transparent",
                text_color="#D6C2C5", hover_color=self.COR_VINHO_HOVER,
                font=ctk.CTkFont(size=12), command=cmd
            ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            sidebar, text="🚪 Sair", anchor="w", fg_color="transparent",
            text_color="#FF8A8A", hover_color=self.COR_VINHO_HOVER,
            command=lambda: self.exibir_tela_autenticacao("login")
        ).pack(side="bottom", fill="x", padx=10, pady=20)

    def criar_area_conteudo(self):
        main = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew", padx=20, pady=15)

        topbar = ctk.CTkFrame(main, fg_color=self.COR_VINHO_ESCURO, height=50, corner_radius=8)
        topbar.pack(fill="x", pady=(0, 15))

        self.search_entry = ctk.CTkEntry(
            topbar, placeholder_text="Pesquisar por nome, autor ou ISBN...", width=320, corner_radius=20
        )
        self.search_entry.pack(side="left", padx=15, pady=10)
        self.search_entry.bind("<Return>", self.executar_busca_acervo)

        nome = self.usuario_logado_dados["nome"] if self.usuario_logado_dados else "Usuário"
        foto = self.usuario_logado_dados.get("foto_path") if self.usuario_logado_dados else self.caminho_avatar_padrao
        avatar = self.carregar_avatar(foto, (32, 32))

        btn_perfil = ctk.CTkButton(
            topbar, text=f"Bem-vindo(a), {nome}", image=avatar, compound="right",
            fg_color="transparent", text_color="#FFFFFF", hover_color=self.COR_VINHO_HOVER,
            command=self.abrir_modal_perfil
        )
        btn_perfil.pack(side="right", padx=15)

        self.container = ctk.CTkFrame(main, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

    def abrir_modal_perfil(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Perfil Pessoal - Edição de Dados")
        modal.geometry("440x650")
        modal.grab_set()
        modal.configure(fg_color="#E8E2D9")

        card = ctk.CTkScrollableFrame(modal, fg_color=self.COR_CARD_BG, corner_radius=10)
        card.pack(padx=15, pady=15, fill="both", expand=True)

        ctk.CTkLabel(card, text="MEU PERFIL", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.COR_VINHO_ESCURO).pack(pady=10)

        foto_path = self.usuario_logado_dados.get("foto_path", self.caminho_avatar_padrao)
        avatar_grande = self.carregar_avatar(foto_path, (80, 80))
        if avatar_grande:
            ctk.CTkLabel(card, text="", image=avatar_grande).pack(pady=5)

        def alterar_foto():
            caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg *.jfif")])
            if caminho:
                self.usuario_logado_dados["foto_path"] = caminho
                messagebox.showinfo("Sucesso", "Foto alterada com sucesso!")
                modal.destroy()
                self.iniciar_layout_dashboard()

        ctk.CTkButton(card, text="📷 Alterar Foto", fg_color="transparent", text_color=self.COR_VINHO_ESCURO, hover_color="#D6C2C5", command=alterar_foto).pack(pady=5)

        ctk.CTkLabel(card, text="Nome Completo:", text_color="gray").pack(anchor="w", padx=20)
        t_nome = ctk.CTkEntry(card, width=320)
        t_nome.insert(0, self.usuario_logado_dados.get("nome", ""))
        t_nome.pack(pady=(0, 8))

        ctk.CTkLabel(card, text="CPF (11 números):", text_color="gray").pack(anchor="w", padx=20)
        t_cpf = ctk.CTkEntry(card, width=320)
        t_cpf.insert(0, self.usuario_logado_dados.get("cpf", ""))
        t_cpf.pack(pady=(0, 8))

        ctk.CTkLabel(card, text="E-mail:", text_color="gray").pack(anchor="w", padx=20)
        t_email = ctk.CTkEntry(card, width=320)
        t_email.insert(0, self.usuario_logado_dados.get("email", ""))
        t_email.pack(pady=(0, 8))

        ctk.CTkLabel(card, text="Telefone:", text_color="gray").pack(anchor="w", padx=20)
        t_tel = ctk.CTkEntry(card, width=320)
        t_tel.insert(0, self.usuario_logado_dados.get("telefone", ""))
        t_tel.pack(pady=(0, 8))

        ctk.CTkLabel(card, text="Graduação / Colégio:", text_color="gray").pack(anchor="w", padx=20)
        t_curso = ctk.CTkEntry(card, width=320)
        t_curso.insert(0, self.usuario_logado_dados.get("curso_colegio", ""))
        t_curso.pack(pady=(0, 8))

        ctk.CTkLabel(card, text="Nova Senha (opcional):", text_color="gray").pack(anchor="w", padx=20)
        t_senha = ctk.CTkEntry(card, width=320, show="*", placeholder_text="Deixe em branco para manter a atual")
        t_senha.pack(pady=(0, 15))

        def salvar_edicao():
            novo_nome = t_nome.get().strip()
            novo_cpf = t_cpf.get().strip()
            novo_email = t_email.get().strip()
            novo_tel = t_tel.get().strip()
            novo_curso = t_curso.get().strip()
            nova_senha = t_senha.get().strip()

            if not (novo_nome and novo_cpf and novo_email):
                messagebox.showwarning("Aviso", "Nome, CPF e E-mail são obrigatórios.")
                return
            if len(novo_nome.split()) < 2:
                messagebox.showerror("Erro", "O nome precisa ter nome e sobrenome.")
                return
            if len(novo_cpf) != 11 or not novo_cpf.isdigit():
                messagebox.showerror("Erro", "O CPF deve conter exatamente 11 dígitos numéricos.")
                return

            self.usuario_logado_dados["nome"] = novo_nome
            self.usuario_logado_dados["cpf"] = novo_cpf
            self.usuario_logado_dados["email"] = novo_email
            self.usuario_logado_dados["telefone"] = novo_tel
            self.usuario_logado_dados["curso_colegio"] = novo_curso
            if nova_senha:
                self.usuario_logado_dados["senha"] = nova_senha

            messagebox.showinfo("Sucesso", "Seus dados foram atualizados com sucesso!")
            modal.destroy()
            self.iniciar_layout_dashboard()

        ctk.CTkButton(card, text="SALVAR ALTERAÇÕES", fg_color=self.COR_VINHO_ESCURO, hover_color=self.COR_VINHO_HOVER, width=320, command=salvar_edicao).pack(pady=15)

    def limpar_container(self):
        for child in self.container.winfo_children():
            child.destroy()

    # --- HOME ---
    def exibir_painel_home(self):
        self.limpar_container()
        self.container.grid_columnconfigure((0, 1, 2), weight=1)

        total_livros = len(self.repo_livro.listar_todos())
        cpf = self.usuario_logado_dados.get("cpf", "")
        meus_emp = len([e for e in self.repo_emprestimo.listar_todos() if e.usuario.id_usuario == cpf])

        metrics = [("Livros no Acervo", str(total_livros)), ("Meus Empréstimos", str(meus_emp)), ("Pendências", "0")]
        for i, (tit, val) in enumerate(metrics):
            card = ctk.CTkFrame(self.container, fg_color=self.COR_CARD_BG, corner_radius=10)
            card.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            ctk.CTkLabel(card, text=tit, text_color="gray").pack(anchor="w", padx=12, pady=(10, 0))
            ctk.CTkLabel(card, text=val, font=ctk.CTkFont(size=20, weight="bold"), text_color=self.COR_TEXTO).pack(anchor="w", padx=12, pady=(0, 10))

        card_ev = ctk.CTkFrame(self.container, fg_color=self.COR_CARD_BG, corner_radius=10)
        card_ev.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=10)
        ctk.CTkLabel(card_ev, text="Próximos Eventos Acadêmicos", font=ctk.CTkFont(size=14, weight="bold"), text_color=self.COR_TEXTO).pack(anchor="w", padx=15, pady=10)
        ctk.CTkLabel(card_ev, text="• Clube de Leitura - Sexta-feira às 18h\n• Oficina de Python - Sábado às 10h", justify="left", text_color=self.COR_TEXTO).pack(anchor="w", padx=15, pady=(0, 10))

    # --- CONSULTAR ACERVO (RF06, COM GRADE, CAPA DA OPEN LIBRARY E BOTÕES CORRIGIDOS) ---
    def exibir_painel_acervo(self, lista_filtrada=None):
        self.limpar_container()
        
        ctk.CTkLabel(
            self.container, 
            text="📖 Catálogo de Obras Disponíveis (RF06)", 
            font=ctk.CTkFont(size=16, weight="bold"), 
            text_color=self.COR_TEXTO
        ).pack(anchor="w", pady=(0, 10))

        scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        livros = lista_filtrada if lista_filtrada is not None else self.repo_livro.listar_todos()

        if not livros:
            ctk.CTkLabel(scroll, text="Nenhum livro encontrado.", text_color="gray").pack(pady=20)
            return

        if not hasattr(self, "imagens_cache"):
            self.imagens_cache = []

        colunas_maximas = 3  # Organização em grade com 3 colunas

        for index, l in enumerate(livros):
            linha = index // colunas_maximas
            coluna = index % colunas_maximas

            # Card individual com tamanho fixo garantido
            card = ctk.CTkFrame(scroll, fg_color=self.COR_CARD_BG, corner_radius=10, width=220, height=310)
            card.grid(row=linha, column=coluna, padx=12, pady=12, sticky="nsew")
            card.grid_propagate(False)

            # Tenta carregar a capa da Open Library de forma segura via ISBN
            imagem_carregada = False
            try:
                isbn_livro = getattr(l, "isbn", getattr(l, "id_livro", ""))
                if isbn_livro:
                    url_capa = f"https://covers.openlibrary.org/b/isbn/{isbn_livro}-L.jpg"
                    req = urllib.request.Request(url_capa, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=3) as resposta:
                        dados_imagem = resposta.read()
                    
                    load_img = Image.open(io.BytesIO(dados_imagem))
                    
                    if load_img.size[0] > 5 and load_img.size[1] > 5:
                        load_img = load_img.resize((100, 140), Image.Resampling.LANCZOS)
                        foto = ctk.CTkImage(light_image=load_img, dark_image=load_img, size=(100, 140))
                        self.imagens_cache.append(foto)
                        lbl_img = ctk.CTkLabel(card, text="", image=foto)
                        imagem_carregada = True
            except Exception:
                pass

            if not imagem_carregada:
                lbl_img = ctk.CTkLabel(
                    card, 
                    text="📚\nSem Capa", 
                    width=100, 
                    height=140, 
                    fg_color="#E0E0E0", 
                    text_color="#555555",
                    font=ctk.CTkFont(size=11, weight="bold")
                )
            
            lbl_img.pack(pady=(10, 5))

            # Título do Livro
            lbl_titulo = ctk.CTkLabel(
                card, 
                text=l.titulo, 
                font=ctk.CTkFont(size=12, weight="bold"), 
                text_color=self.COR_VINHO_ESCURO, 
                wraplength=200
            )
            lbl_titulo.pack(padx=10, anchor="w")

            # Autor
            lbl_autor = ctk.CTkLabel(
                card, 
                text=f"Autor: {l.autor}", 
                font=ctk.CTkFont(size=10), 
                text_color="gray", 
                wraplength=200
            )
            lbl_autor.pack(padx=10, anchor="w")

            # Função de empréstimo direto pelo card
            def solicitar(livro_obj=l):
                cpf = self.usuario_logado_dados.get("cpf")
                meus_ativos = [e for e in self.repo_emprestimo.listar_todos() if e.usuario.id_usuario == cpf]
                if len(meus_ativos) >= 3:
                    messagebox.showwarning("Limite Atingido", "Você atingiu o limite máximo de 3 empréstimos simultâneos permitidos (RF08).")
                    return
                
                usr = Aluno(id_usuario=cpf, nome=self.usuario_logado_dados["nome"], matricula=cpf, curso=self.usuario_logado_dados["curso_colegio"])
                emp = self.servico_emprestimo.realizar_emprestimo(usr, livro_obj)
                emp.data_devolucao_prevista = datetime.now() + timedelta(days=7)
                
                self.repo_emprestimo.salvar(emp)
                self.repo_livro.salvar(livro_obj)
                
                data_dev = emp.data_devolucao_prevista.strftime('%d/%m/%Y')
                messagebox.showinfo("Sucesso (RF07, RF09)", f"Empréstimo de '{livro_obj.titulo}' realizado com sucesso!\nPrazo de devolução (7 dias): {data_dev}")
                self.exibir_painel_acervo()

            # Botões inferiores organizados (Detalhes e Solicitar)
            frame_botoes = ctk.CTkFrame(card, fg_color="transparent")
            frame_botoes.pack(side="bottom", fill="x", padx=10, pady=8)

            btn_detalhes = ctk.CTkButton(
                frame_botoes, 
                text="Detalhes", 
                fg_color="transparent", 
                border_width=1,
                border_color=self.COR_VINHO_ESCURO,
                text_color=self.COR_VINHO_ESCURO,
                hover_color="#D6C2C5",
                height=26,
                font=ctk.CTkFont(size=11, weight="bold"),
                command=lambda livro_obj=l: self.abrir_modal_detalhes_livro(livro_obj)
            )
            btn_detalhes.pack(side="left", expand=True, fill="x", padx=(0, 4))

            btn_emp = ctk.CTkButton(
                frame_botoes, 
                text="Solicitar", 
                fg_color=self.COR_VINHO_ESCURO, 
                hover_color=self.COR_VINHO_HOVER, 
                height=26,
                font=ctk.CTkFont(size=11, weight="bold"),
                command=solicitar
            )
            btn_emp.pack(side="right", expand=True, fill="x", padx=(4, 0))

    def abrir_modal_detalhes_livro(self, livro_obj):
        """Abre a modal com detalhes da obra e botão de empréstimo (7 dias)."""
        modal = ctk.CTkToplevel(self)
        modal.title(f"Detalhes da Obra: {livro_obj.titulo}")
        modal.geometry("700x520")
        modal.grab_set()
        modal.configure(fg_color="#E8E2D9")

        card_modal = ctk.CTkFrame(modal, fg_color=self.COR_CARD_BG, corner_radius=12)
        card_modal.pack(fill="both", expand=True, padx=15, pady=15)

        # Lado Esquerdo: Imagem da Capa Ampliada via Open Library
        frame_esq = ctk.CTkFrame(card_modal, fg_color="transparent", width=220)
        frame_esq.pack(side="left", fill="y", padx=20, pady=20)

        img_ampliada = None
        try:
            isbn_livro = getattr(livro_obj, "isbn", getattr(livro_obj, "id_livro", ""))
            if isbn_livro:
                url_capa = f"https://covers.openlibrary.org/b/isbn/{isbn_livro}-L.jpg"
                req = urllib.request.Request(url_capa, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=3) as resposta:
                    dados_imagem = resposta.read()
                p_img = Image.open(io.BytesIO(dados_imagem))
                if p_img.size[0] > 5:
                    img_ampliada = ctk.CTkImage(light_image=p_img, dark_image=p_img, size=(160, 230))
        except Exception:
            pass

        if img_ampliada:
            ctk.CTkLabel(frame_esq, text="", image=img_ampliada).pack(pady=(0, 10))
        else:
            lbl_sem_foto = ctk.CTkFrame(frame_esq, fg_color="#D8D0C5", width=160, height=230, corner_radius=6)
            lbl_sem_foto.pack(pady=(0, 10))
            lbl_sem_foto.pack_propagate(False)
            ctk.CTkLabel(lbl_sem_foto, text="📖\n\nCapa não\nencontrada", text_color="#555555", font=ctk.CTkFont(size=12, weight="bold")).pack(expand=True)

        # Lado Direito: Informações Detalhadas
        frame_dir = ctk.CTkScrollableFrame(card_modal, fg_color="transparent", width=420, height=440)
        frame_dir.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

        ctk.CTkLabel(frame_dir, text=livro_obj.titulo, font=ctk.CTkFont(size=18, weight="bold"), text_color=self.COR_VINHO_ESCURO).pack(anchor="w", pady=(0, 2))
        ctk.CTkLabel(frame_dir, text=f"por {livro_obj.autor} (Autor)  •  Formato: Capa comum", font=ctk.CTkFont(size=11), text_color="gray").pack(anchor="w", pady=(0, 10))
        
        ctk.CTkLabel(frame_dir, text="4,7 ⭐⭐⭐⭐⭐ (42.947)", font=ctk.CTkFont(size=11), text_color="#D9822B").pack(anchor="w", pady=(0, 10))

        sinopse_texto = (
            f"Obra literária catalogada no acervo acadêmico sob o título '{livro_obj.titulo}', escrita por {livro_obj.autor}. "
            "Esta edição integra o sistema integrado da biblioteca universitária, oferecendo suporte completo para consulta "
            "e empréstimos rápidos aos discentes e servidores cadastrados."
        )
        lbl_sinopse = ctk.CTkLabel(frame_dir, text=sinopse_texto, font=ctk.CTkFont(size=11), text_color=self.COR_TEXTO, justify="left", wraplength=380)
        lbl_sinopse.pack(anchor="w", pady=(0, 15))

        frame_meta = ctk.CTkFrame(frame_dir, fg_color="#F0ECE1", corner_radius=6)
        frame_meta.pack(fill="x", pady=(0, 15), padx=2)

        info_tecnica = f"ISBN-13: {getattr(livro_obj, 'isbn', 'N/A')}\nEdição: 1ª  |  Editora: Universitária  |  Disponível para Empréstimo"
        ctk.CTkLabel(frame_meta, text=info_tecnica, font=ctk.CTkFont(size=10), text_color="gray", justify="left").pack(padx=10, pady=8)

        def solicitar_emprestimo_modal():
            cpf = self.usuario_logado_dados.get("cpf")
            
            meus_ativos = [e for e in self.repo_emprestimo.listar_todos() if e.usuario.id_usuario == cpf]
            if len(meus_ativos) >= 3:
                messagebox.showwarning("Limite Atingido", "Você atingiu o limite máximo de 3 empréstimos simultâneos permitidos (RF08).")
                return

            usr = Aluno(id_usuario=cpf, nome=self.usuario_logado_dados["nome"], matricula=cpf, curso=self.usuario_logado_dados["curso_colegio"])
            
            emp = self.servico_emprestimo.realizar_emprestimo(usr, livro_obj)
            emp.data_devolucao_prevista = datetime.now() + timedelta(days=7)
            
            self.repo_emprestimo.salvar(emp)
            self.repo_livro.salvar(livro_obj)
            
            data_dev = emp.data_devolucao_prevista.strftime('%d/%m/%Y')
            messagebox.showinfo("Sucesso (RF07, RF09)", f"Empréstimo de '{livro_obj.titulo}' realizado com sucesso!\nPrazo de devolução estipulado (7 dias): {data_dev}")
            modal.destroy()
            self.exibir_painel_acervo()

        btn_solicitar = ctk.CTkButton(
            frame_dir, text="SOLICITAR EMPRÉSTIMO (7 DIAS)", 
            fg_color=self.COR_VINHO_ESCURO, hover_color=self.COR_VINHO_HOVER,
            height=38, font=ctk.CTkFont(size=12, weight="bold"),
            command=solicitar_emprestimo_modal
        )
        btn_solicitar.pack(fill="x", pady=5)

    def executar_busca_acervo(self, event=None):
        termo = self.search_entry.get().strip().lower()
        if not termo:
            self.exibir_painel_acervo()
            return
        todos = self.repo_livro.listar_todos()
        filtrados = [
            l for l in todos 
            if termo in l.titulo.lower() or termo in l.autor.lower() or termo in l.isbn.lower()
        ]
        self.exibir_painel_acervo(lista_filtrada=filtrados)

    # --- MEUS EMPRÉSTIMOS ---
    def exibir_painel_emprestimos(self):
        self.limpar_container()
        ctk.CTkLabel(self.container, text="🔄 Meus Empréstimos Ativos", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.COR_TEXTO).pack(anchor="w", pady=(0, 10))

        txt = ctk.CTkTextbox(self.container, fg_color=self.COR_CARD_BG, text_color=self.COR_TEXTO)
        txt.pack(fill="both", expand=True)

        cpf = self.usuario_logado_dados.get("cpf")
        meus = [e for e in self.repo_emprestimo.listar_todos() if e.usuario.id_usuario == cpf]
        
        if not meus:
            txt.insert("1.0", "Você não possui empréstimos ativos no momento.")
        else:
            for e in meus:
                data_d = e.data_devolucao_prevista.strftime('%d/%m/%Y')
                txt.insert("end", f"• Livro: {e.livro.titulo} | Devolução Prevista (7 dias): {data_d}\n")

if __name__ == "__main__":
    app = AppBiblioteca()
    app.mainloop()