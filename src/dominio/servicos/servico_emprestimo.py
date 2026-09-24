from datetime import datetime, timedelta
from dominio.modelos.emprestimo import Emprestimo

class ServicoEmprestimo:
    def realizar_emprestimo(self, usuario, livro, dias_prazo=14):
        data_hoje = datetime.now()
        data_devolucao = data_hoje + timedelta(dias=dias_prazo)
        id_emp = f"EMP-{int(datetime.now().timestamp())}"
        
        livro.disponivel = False
        return Emprestimo(
            id_emprestimo=id_emp,
            usuario=usuario,
            livro=livro,
            data_emprestimo=data_hoje,
            data_devolucao_prevista=data_devolucao
        )

    def calcular_multa(self, emprestimo, valor_dia=2.0):
        if not emprestimo.data_devolucao_prevista:
            return 0.0
        hoje = datetime.now()
        if hoje > emprestimo.data_devolucao_prevista:
            dias_atraso = (hoje - emprestimo.data_devolucao_prevista).days
            return max(0.0, dias_atraso * valor_dia)
        return 0.0