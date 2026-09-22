Processos de Desenvolvimento, Product Backlog e Controle de Mudanças

Disciplina: Projeto e Engenharia de Software

Responsável: Bhyanca

Projeto: Sistema Integrado de Gestão de Biblioteca (A3)

1. Análise Comparativa de Metodologias de Desenvolvimento

Para a escolha do ciclo de vida e modelo de processo do software, foram avaliadas três abordagens principais:

1.1 Modelo em Cascata (Waterfall)

Descrição: Abordagem sequencial e rígida na qual cada fase (Requisitos, Projeto, Implementação, Testes, Implantação) deve ser totalmente concluída antes do início da seguinte.

Vantagens: Alta previsibilidade de documentação e escopo bem definido desde o início.

Desvantagens: Baixa flexibilidade a mudanças, feedback tardio do usuário e alto risco de atrasos na entrega final.

1.2 Scrum (Metodologia Ágil)

Descrição: Framework iterativo e incremental centrado em entregas de valor em ciclos curtos e fixos (Sprints), com reuniões frequentes de alinhamento e papéis bem definidos.

Vantagens: Alta capacidade de adaptação a mudanças, visibilidade contínua do progresso e validações constantes com o cliente/professor.

Desvantagens: Exige disciplina e comunicação constante entre todos os membros da equipe.

1.3 Kanban (Gestão Visual)

Descrição: Método focado no fluxo contínuo de trabalho e limitação de trabalho em andamento (WIP) utilizando cartões visuais (A Fazer, Em Andamento, Concluído).

Vantagens: Reduz o gargalo de tarefas, proporciona visualização clara do status e simplifica o fluxo de entregas.

Desvantagens: Pode perder o foco no planejamento de prazos longos se não associado a metas bem definidas.

1.4 Justificativa da Escolha para o Projeto

O grupo adotou uma abordagem híbrida Ágil (Scrum + Kanban):

Por que Scrum?
 O projeto acadêmico possui um cronograma fixo de 5 semanas. A divisão do desenvolvimento em Sprints semanais garante entregas incrementais da documentação, modelos UML e código-fonte funcional.

Por que Kanban? 
O acompanhamento visual das tarefas da equipe (Kaylane, Anna Júlia e Bhyanca) permite identificar rapidamente gargalos e garantir o cumprimento dos prazos do cronograma.

2. Product Backlog e Histórias de Usuário (User Stories)

Abaixo estão as User Stories priorizadas para guiar o desenvolvimento do sistema, conectadas aos Requisitos Funcionais (RFs):

US01 - Cadastro de Usuários (RF01, RF03):

Como Bibliotecário, quero cadastrar e gerenciar perfis de alunos e professores, para que eles possam realizar empréstimos de obras na biblioteca.

Critério de Aceite: O sistema deve validar CPF único, e-mail e aplicar o perfil correto.

US02 - Autenticação e Login (RF02, RNF01, RNF08):

Como Usuário (Aluno/Professor/Bibliotecário), quero me autenticar com e-mail e senha, para que eu possa acessar as funcionalidades restritas do meu perfil.

Critério de Aceite: Senha deve ser tratada com hash criptográfico (BCrypt) e a sessão deve expirar após inatividade.

US03 - Catalogação de Obras e Exemplares (RF04, RF05):

Como Bibliotecário, quero cadastrar livros e organizar seus exemplares físicos, para que o acervo esteja atualizado no sistema.

Critério de Aceite: Cada livro deve conter título, autor, ISBN, editora e quantidade de exemplares associados.

US04 - Pesquisa de Acervo (RF06, RNF02):

Como Usuário, quero pesquisar obras por título, autor ou categoria, para que eu possa verificar a disponibilidade de exemplares.

Critério de Aceite: Retorno das pesquisas em até 2 segundos.

US05 - Empréstimo e Validação de Limites (RF07, RF08, RF09):

Como Bibliotecário, quero registrar o empréstimo de um exemplar para um usuário, para que o status da obra mude para emprestado e a data de devolução seja gravada.

Critério de Aceite: Impedir empréstimo se o Aluno já tiver 3 livros ou o Professor 5 livros, ou se o usuário possuir pendências.

US06 - Devolução e Cálculo de Multas (RF10, RF12, RF13):

Como Bibliotecário, quero registrar a devolução de um exemplar, para que a obra volte a ficar disponível e multas por atraso sejam calculadas automaticamente.

Critério de Aceite: Se a devolução estiver atrasada, o sistema gera o valor da multa e bloqueia o usuário para novos empréstimos até a regularização.

US07 - Renovação e Reserva (RF11, RF14):

Como Aluno/Professor, quero renovar um empréstimo ou reservar uma obra esgotada, para que eu possa garantir a leitura do material.

Critério de Aceite: A renovação só é permitida se não houver reserva pendente de outro usuário.

US08 - Relatórios e Indicadores (RF15):

Como Bibliotecário, quero emitir relatórios de obras mais emprestadas e usuários em atraso, para que a gestão da biblioteca possa tomar decisões administrativas.

3. Procedimento de Controle de Mudanças e Manutenção

Para lidar com solicitações de alteração de requisitos ou ajustes durante o ciclo de desenvolvimento, estabelece-se o seguinte fluxo formal:

Solicitação de Mudança: Registra-se a proposta de alteração contendo a justificativa e o impacto estimado.

Análise de Impacto: O grupo analisa o impacto da alteração no cronograma de 5 semanas, no código-fonte já desenvolvido e na modelagem UML.

Aprovação/Rejeição: A mudança só é aceita se não comprometer as entregas essenciais dos 15 RFs principais.

Atualização da Documentação: Em caso de aprovação, atualizam-se a Matriz de Rastreabilidade, o Product Backlog e a versão do repositório Git com commit explicativo.