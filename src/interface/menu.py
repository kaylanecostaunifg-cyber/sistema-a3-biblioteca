import importlib
from datetime import datetime


def _carregar_classe(module_name, class_name):
    for candidato in (module_name, f"src.{module_name}"):
        try:
            modulo = importlib.import_module(candidato)
            return getattr(modulo, class_name)
        except ModuleNotFoundError:
            continue
    raise ModuleNotFoundError(f"Módulo '{module_name}' não foi encontrado.")


RepositorioUsuarioSQLite = _carregar_classe("infra.repositorios.repositorio_usuario", "RepositorioUsuarioSQLite")
RepositorioLivroSQLite = _carregar_classe("infra.repositorios.repositorio_livro", "RepositorioLivroSQLite")
RepositorioEmprestimoSQLite = _carregar_classe("infra.repositorios.repositorio_emprestimo", "RepositorioEmprestimoSQLite")
Aluno = _carregar_classe("dominio.modelos.aluno", "Aluno")
Professor = _carregar_classe("dominio.modelos.professor", "Professor")
Livro = _carregar_classe("dominio.modelos.livro", "Livro")
Emprestimo = _carregar_classe("dominio.modelos.emprestimo", "Emprestimo")
CalculadorMulta = _carregar_classe("dominio.servicos.calculador_multa", "CalculadorMulta")

class MenuCLI:
    def __init__(self):
        self.repo_usuario = RepositorioUsuarioSQLite()
        self.repo_livro = RepositorioLivroSQLite()
        self.repo_emprestimo = RepositorioEmprestimoSQLite()

    def exibir_menu_principal(self):
        while True:
            print("\n" + "=" * 45)
            print("      SISTEMA DE GESTÃO DE BIBLIOTECA      ")
            print("=" * 45)
            print("1. Cadastrar Usuário (Aluno / Professor)")
            print("2. Cadastrar Livro")
            print("3. Listar Usuários")
            print("4. Listar Livros")
            print("5. Buscar Livro por Título")         # <-- NOVA OPÇÃO
            print("6. Realizar Empréstimo")
            print("7. Registrar Devolução / Calcular Multa")
            print("8. Listar Empréstimos")
            print("9. Relatório de Empréstimos em Atraso") # <-- NOVA OPÇÃO
            print("0. Sair do Sistema")
            print("-" * 45)

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.cadastrar_usuario()
            elif opcao == "2":
                self.cadastrar_livro()
            elif opcao == "3":
                self.listar_usuarios()
            elif opcao == "4":
                self.listar_livros()
            elif opcao == "5":
                self.buscar_livro_por_titulo()         # <-- CHAMADA NOVA
            elif opcao == "6":
                self.realizar_emprestimo()
            elif opcao == "7":
                self.registrar_devolucao()
            elif opcao == "8":
                self.listar_emprestimos()
            elif opcao == "9":
                self.relatorio_atrasos()               # <-- CHAMADA NOVA
            elif opcao == "0":
                print("\nEncerrando o sistema... Até logo!")
                break
            else:
                print("\nOpção inválida. Tente novamente.")

    def cadastrar_usuario(self):
        print("\n--- CADASTRO DE USUÁRIO ---")
        tipo = input("Tipo (1 - Aluno / 2 - Professor): ").strip()
        try:
            id_u = int(input("ID do Usuário (número): "))
            nome = input("Nome Completo: ").strip()
            email = input("E-mail: ").strip()

            if tipo == "1":
                cpf = input("CPF: ").strip()
                curso = input("Curso: ").strip()
                matricula = input("Matrícula: ").strip()
                novo_u = Aluno(id_usuario=id_u, nome=nome, email=email, cpf=cpf, curso=curso, matricula=matricula)
            elif tipo == "2":
                dep = input("Departamento: ").strip()
                novo_u = Professor(id_usuario=id_u, nome=nome, email=email, departamento=dep)
            else:
                print("Tipo de usuário inválido.")
                return

            self.repo_usuario.salvar(novo_u)
            print(f"Usuário {nome} cadastrado com sucesso!")
        except ValueError:
            print("Erro: ID deve ser um valor numérico.")

    def cadastrar_livro(self):
        print("\n--- CADASTRO DE LIVRO ---")
        try:
            id_l = int(input("ID do Livro (número): "))
            titulo = input("Título: ").strip()
            autor = input("Autor: ").strip()
            isbn = input("ISBN: ").strip()
            ano = int(input("Ano de Publicação: "))
            categoria = input("Categoria: ").strip()

            novo_l = Livro(id_livro=id_l, titulo=titulo, autor=autor, isbn=isbn, ano=ano, categoria=categoria)
            self.repo_livro.salvar(novo_l)
            print(f"Livro '{titulo}' cadastrado com sucesso!")
        except ValueError:
            print("Erro: Preencha os campos numéricos (ID e Ano) corretamente.")

    def listar_usuarios(self):
        print("\n--- USUÁRIOS CADASTRADOS ---")
        usuarios = self.repo_usuario.listar_todos()
        if not usuarios:
            print("Nenhum usuário encontrado.")
            return
        for u in usuarios:
            tipo = "Aluno" if isinstance(u, Aluno) else "Professor"
            print(f"[{tipo}] ID: {u.id_usuario} | Nome: {u.nome} | E-mail: {u.email}")

    def listar_livros(self):
        print("\n--- LIVROS CADASTRADOS ---")
        livros = self.repo_livro.listar_todos()
        if not livros:
            print("Nenhum livro encontrado.")
            return
        for l in livros:
            print(f"ID: {l.id_livro} | Título: {l.titulo} | Autor: {l.autor} | Categoria: {l.categoria}")

    def realizar_emprestimo(self):
        print("\n--- NOVO EMPRÉSTIMO ---")
        try:
            id_u = int(input("ID do Usuário: "))
            id_l = int(input("ID do Livro: "))

            usuarios = self.repo_usuario.listar_todos()
            usuario = next((u for u in usuarios if u.id_usuario == id_u), None)

            livros = self.repo_livro.listar_todos()
            livro = next((l for l in livros if l.id_livro == id_l), None)

            if not usuario or not livro:
                print("Usuário ou Livro não encontrado.")
                return

            emp = Emprestimo(usuario=usuario, livro=livro)
            self.repo_emprestimo.salvar(emp)
            
            prazo_str = emp.data_devolucao_prevista.strftime("%d/%m/%Y")
            print(f"Empréstimo registrado com sucesso! Devolução prevista até: {prazo_str}")
        except ValueError:
            print("Entrada inválida. IDs devem ser números.")

    def registrar_devolucao(self):
        print("\n--- REGISTRO DE DEVOLUÇÃO ---")
        try:
            id_emp = int(input("ID do Empréstimo: "))
            emprestimos = self.repo_emprestimo.listar_todos()
            emp = next((e for e in emprestimos if e.id_emprestimo == id_emp), None)

            if not emp:
                print("Empréstimo não encontrado.")
                return

            dt_hoje = datetime.now()
            multa = CalculadorMulta.calcular(emp, dt_hoje)
            
            self.repo_emprestimo.registrar_devolucao(id_emp, dt_hoje, multa)

            print(f"Devolução registrada!")
            if multa > 0:
                print(f"Multa por atraso gerada: R$ {multa:.2f}")
            else:
                print("Devolução realizada dentro do prazo! Nenhuma multa pendente.")
        except ValueError:
            print("Erro ao processar o ID do empréstimo.")

    def listar_emprestimos(self):
        print("\n--- HISTÓRICO DE EMPRÉSTIMOS ---")
        emprestimos = self.repo_emprestimo.listar_todos()
        if not emprestimos:
            print("Nenhum empréstimo registrado.")
            return

        for e in emprestimos:
            status = "Devolvido" if e.data_devolucao_real else "Pendente"
            prev_str = e.data_devolucao_prevista.strftime("%d/%m/%Y")
            print(f"ID: {e.id_emprestimo} | Usuário: {e.usuario.nome} | Livro: {e.livro.titulo} | Previsto: {prev_str} | Status: {status}")

    # =========================================================
    # COLE OS DOIS NOVOS MÉTODOS AQUI NO FINAL DO ARQUIVO:
    # =========================================================

    def buscar_livro_por_titulo(self):
        print("\n--- BUSCAR LIVRO POR TÍTULO ---")
        termo = input("Digite o título ou parte dele: ").strip()
        if not termo:
            print("O termo de busca não pode ser vazio.")
            return

        livros = self.repo_livro.buscar_por_titulo(termo)
        if not livros:
            print(f"Nenhum livro encontrado com o termo '{termo}'.")
            return

        print(f"\n🔍 Resultados encontrados ({len(livros)}):")
        for l in livros:
            print(f"  ID: {l.id_livro} | Título: {l.titulo} | Autor: {l.autor} | Categoria: {l.categoria}")

    def relatorio_atrasos(self):
        print("\n--- RELATÓRIO DE EMPRÉSTIMOS EM ATRASO ---")
        atrasados = self.repo_emprestimo.listar_atrasados()

        if not atrasados:
            print(" Nenhum empréstimo em atraso no momento!")
            return

        print(f" Atenção: {len(atrasados)} empréstimo(s) pendente(s) com atraso:\n")
        agora = datetime.now()

        for e in atrasados:
            dias_atraso = (agora - e.data_devolucao_prevista).days
            multa_estimada = CalculadorMulta.calcular(e, agora)
            prev_str = e.data_devolucao_prevista.strftime("%d/%m/%Y")

            print(f"     Empréstimo ID: {e.id_emprestimo}")
            print(f"     Usuário: {e.usuario.nome} ({e.usuario.email})")
            print(f"     Livro: {e.livro.titulo}")
            print(f"     Data Prevista: {prev_str} ({dias_atraso} dia(s) de atraso)")
            print(f"     Multa Estimada: R$ {multa_estimada:.2f}\n")