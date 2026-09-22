Especificação de Requisitos do Sistema - A3

Tema: Gestão Integrada de Acervo e Empréstimos de Bibliotecas
Responsável: Anna Júlia   

1. Requisitos Funcionais (RFs)

RF01: Cadastrar UsuáriosDescrição: O sistema deve permitir o cadastro de novos usuários contendo nome, CPF, e-mail, telefone e perfil de acesso;

RF02: Autenticar UsuáriosDescrição: O sistema deve permitir o login e autenticação dos usuários cadastrados por meio de e-mail e senha;

RF03: Gerenciar Perfis de AcessoDescrição: O sistema deve diferenciar as permissões e regras de negócio para os perfis Aluno, Professor e Bibliotecário;

RF04: Catalogar Obras no AcervoDescrição: O sistema deve permitir ao Bibliotecário cadastrar obras informando título, autor, editora, ISBN, ano de publicação e categoria;

RF05: Gerenciar ExemplaresDescrição: O sistema deve permitir o cadastro e controle individual dos exemplares físicos associados a cada obra do acervo;

RF06: Pesquisar Obras e ExemplaresDescrição: O sistema deve permitir a consulta do acervo por meio de filtros como título, autor, categoria ou ISBN;

RF07: Realizar Empréstimo de ExemplaresDescrição: O sistema deve registrar o empréstimo de um exemplar disponível para um usuário ativo e sem pendências;

RF08: Validar Limite de Empréstimos SimultâneosDescrição: O sistema deve impedir que um usuário realize novos empréstimos caso atinja o limite permitido pelo seu perfil (ex: até 3 livros para Aluno e até 5 para Professor);

F09: Controlar Prazos de DevoluçãoDescrição: O sistema deve definir automaticamente a data limite para devolução de acordo com o perfil do usuário (ex: 7 dias para Aluno e 15 dias para Professor);

RF10: Registrar Devolução de ExemplaresDescrição: O sistema deve dar baixa no empréstimo no momento da devolução do exemplar, alterando o status da obra para disponível;

RF11: Renovar EmpréstimoDescrição: O sistema deve permitir a renovação do prazo de empréstimo de um exemplar, desde que não haja reserva pendente para a mesma obra;

RF12: Calcular Multas por AtrasoDescrição: O sistema deve calcular automaticamente o valor da multa por dia de atraso no momento em que a devolução fora do prazo for realizada;

RF13: Bloquear Usuários InadimplentesDescrição: O sistema deve bloquear automaticamente novos empréstimos para usuários que possuam multas abertas ou pendências de atraso;

RF14: Realizar Reserva de ObrasDescrição: O sistema deve permitir que o usuário faça a reserva de uma obra quando todos os seus exemplares estiverem emprestados;

RF15: Emitir Relatórios do Acervo e CirculaçãoDescrição: O sistema deve gerar relatórios estatísticos informando as obras mais emprestadas, lista de usuários com atrasos e saldo pendente de multas.

2. Requisitos Não Funcionais (RNFs)

RNF01: Segurança e Criptografia (Segurança)
Descrição: O sistema deve criptografar todas as senhas dos usuários no banco de dados utilizando algoritmos de Hash seguros (ex: BCrypt);

RNF02: Tempo de Resposta (Desempenho)
Descrição: O sistema deve retornar os resultados das buscas no acervo em um tempo máximo de 2 segundos para consultas com até 10.000 registros;

RNF03: Integridade das Transações (Confiabilidade)
Descrição: O sistema deve garantir a consistência e atomicidade (ACID) durante o registro simultâneo de empréstimos, evitando que dois usuários reservem ou emprestem o mesmo exemplar ao mesmo tempo;

RNF04: Arquitetura Modular (Manutenibilidade)
Descrição: O código-fonte do sistema deve ser estruturado em camadas independentes (Apresentação, Aplicação, Domínio e Persistência) para facilitar a manutenção e evolução;

RNF05: Responsividade e Interface (Usabilidade)
Descrição: A interface gráfica deve ser simples, intuitiva e acessível em diferentes resoluções de tela Desktop;

RNF06: Registro de Logs de Auditoria (Auditabilidade)
Descrição: O sistema deve manter registro de logs com data, hora e usuário responsável por operações críticas, tais como devoluções, baixas de acervo e aplicação de multas;

NF07: Padronização do Versionamento (Portabilidade/Governança)
Descrição: Todo o código-fonte, scripts de banco de dados e documentação devem ser gerenciados em repositório Git sob controle de versão;

RNF08: Segurança de Acesso e Sessão (Autenticação)
Descrição: As sessões de usuários autenticados devem expirar após 30 minutos de inatividade por questões de segurança.