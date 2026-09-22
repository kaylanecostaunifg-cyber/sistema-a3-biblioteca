import sys
import os
from pathlib import Path

# Fixa o caminho da raiz e da pasta src no sys.path de forma absoluta
RAIZ_PROJETO = Path(__file__).resolve().parent
PASTA_SRC = RAIZ_PROJETO / "src"

if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))
if str(PASTA_SRC) not in sys.path:
    sys.path.insert(0, str(PASTA_SRC))

# Importação defensiva para funcionar com ou sem o prefixo 'src.'
try:
    from src.dominio.modelos.aluno import Aluno
    from src.dominio.modelos.professor import Professor
    from src.dominio.modelos.livro import Livro
    from src.dominio.modelos.emprestimo import Emprestimo
    from src.dominio.servicos.calculador_multa import CalculadorMulta
except ModuleNotFoundError:
    from dominio.modelos.aluno import Aluno
    from dominio.modelos.professor import Professor
    from dominio.modelos.livro import Livro
    from dominio.modelos.emprestimo import Emprestimo
    from dominio.servicos.calculador_multa import CalculadorMulta

from datetime import datetime, timedelta


def executar_testes():
    print("=" * 60)
    print("      TESTE DE CRIAÇÃO DE EMPRÉSTIMO E CÁLCULO DE MULTA")
    print("=" * 60)

    # 1. Instanciando Usuários e Livro
    aluno = Aluno(
        id_usuario=1,
        nome="Kaylane Costa",
        email="kaylane@email.com",
        cpf="123.456.789-00",
        matricula="20251001",
        curso="Ciência da Computação"
    )

    professor = Professor(
        id_usuario=2,
        nome="Christian Azonyetin",
        email="christian@email.com",
        cpf="987.654.321-11",
        siape="998877",
        departamento="Tecnologia da Informação"
    )

    # Ajustado 'ano_publicacao' para 'ano' para bater com o __init__ do modelo Livro
    try:
        livro = Livro(
            id_livro=101,
            titulo="Engenharia de Software",
            autor="Ian Sommerville",
            isbn="978-85-7605-115-2",
            ano=2019,
            categoria="Tecnologia"
        )
    except TypeError:
        # Fallback caso a classe Livro não receba 'ano' nem 'ano_publicacao'
        livro = Livro(
            id_livro=101,
            titulo="Engenharia de Software",
            autor="Ian Sommerville",
            isbn="978-85-7605-115-2"
        )

    calculador = CalculadorMulta(valor_diaria=2.0)

    # ------------------------------------------------------------------
    # CENÁRIO 1: Empréstimo para Aluno (Prazo: 7 dias / Devolução Sem Atraso)
    # ------------------------------------------------------------------
    print("\n--- CENÁRIO 1: Empréstimo de Aluno (No Prazo) ---")
    emp_aluno = Emprestimo(id_emprestimo=10, usuario=aluno, livro=livro)

    print(f"Usuário: {emp_aluno.usuario.nome} ({emp_aluno.usuario.__class__.__name__})")
    print(f"Livro: {emp_aluno.livro.titulo}")
    print(f"Data do Empréstimo: {emp_aluno.data_emprestimo.strftime('%d/%m/%Y')}")
    print(f"Data Prevista de Devolução: {emp_aluno.data_devolucao_prevista.strftime('%d/%m/%Y')}")

    # Simulando devolução 5 dias após o empréstimo (dentro do prazo de 7 dias)
    data_devolucao_aluno = emp_aluno.data_emprestimo + timedelta(days=5)
    emp_aluno.realizar_devolucao(data_devolucao=data_devolucao_aluno)

    multa_aluno = calculador.calcular_multa(emp_aluno)
    print(f"Data Efetiva de Devolução: {emp_aluno.data_devolucao_real.strftime('%d/%m/%Y')}")
    print(f"Status do Empréstimo: {emp_aluno.status}")
    print(f"Valor da Multa: R$ {multa_aluno:.2f}")

    # ------------------------------------------------------------------
    # CENÁRIO 2: Empréstimo para Professor (Prazo: 15 dias / Devolução Com Atraso)
    # ------------------------------------------------------------------
    print("\n--- CENÁRIO 2: Empréstimo de Professor (Com Atraso) ---")
    emp_prof = Emprestimo(id_emprestimo=20, usuario=professor, livro=livro)

    print(f"Usuário: {emp_prof.usuario.nome} ({emp_prof.usuario.__class__.__name__})")
    print(f"Livro: {emp_prof.livro.titulo}")
    print(f"Data do Empréstimo: {emp_prof.data_emprestimo.strftime('%d/%m/%Y')}")
    print(f"Data Prevista de Devolução: {emp_prof.data_devolucao_prevista.strftime('%d/%m/%Y')}")

    # Simulando devolução 20 dias após o empréstimo (5 dias de atraso)
    data_devolucao_prof = emp_prof.data_emprestimo + timedelta(days=20)
    emp_prof.realizar_devolucao(data_devolucao=data_devolucao_prof)

    multa_prof = calculador.calcular_multa(emp_prof)
    print(f"Data Efetiva de Devolução: {emp_prof.data_devolucao_real.strftime('%d/%m/%Y')}")
    print(f"Status do Empréstimo: {emp_prof.status}")
    print(f"Atraso Calculado: 5 dias")
    print(f"Valor da Multa (R$ 2.00/dia): R$ {multa_prof:.2f}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    executar_testes()