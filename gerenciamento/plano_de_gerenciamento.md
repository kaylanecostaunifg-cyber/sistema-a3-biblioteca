Plano de Gerenciamento do Projeto - A3

Tema: Gestão Integrada de Acervo e Empréstimos de Bibliotecas 
Disciplina: Projeto e Engenharia de Software
Professor: Christian Azonyetin
Equipe: Kaylane Cristinne, Anna Júlia e Bhyanca Vitoria

1.Objetivos do Projeto

Garantir o planejamento, especificação, modelagem, desenvolvimento, testes e documentação
de um sistema de gestão de acervo e empréstimo de bibliotecas, aplicando de forma rigirosa os princípios de Engenharia de Software, Orientação a Objetos, Arquitetura em Camadas e Controle de Versões.

2.Gerenciamento de Escopo

Dentro do Escopo (In-Scope)

-Gestão de Acervo: Cadastro, atualização e consulta de livros, revistas e exemplares;
-Gestão de Usuários: Cadastro e autenticação de perfis(Aluno, Professor, Bibliotecário);
-Controle de Empréstimos e Devoluções: Resgistro de empréstimos, devoluções, controle de prazo e limites;
-Gestão de Multas: Cálculo automático de penalidades por atraso;
-Reserva de Obras: Reserva de itens indisponíveis e controle de fila;
-Relatórios: Emissão de relatórios de obras mais emprestadas e inadimplência.

Fora do Escopo (Out-of-Scope)

-Aplicativo mobile nativo (sistema restrito a ambiente Desktop/Web);
-Processamento de pagamento real (PIX, Cartão) para taxas e multas;
-Sensores físicos e leitores de hardware para automação de portaria;
-Módulos de Inteligência Artificial para recomendação avançada.

3.Registro de Riscos (Risk Register)

Risco R01: Atraso na implementação das regras de negócio.

-Probabilidade: Média;
-Impacto: Alto;
-Nível de Risco: Alto;
-Ação de Mitigação: Dividir o backlong de desenvolvimento de Sprints semanais bem definidas e manter o foco estrito nas funcionalidades prioritárias dentro do escopo.

Risco R02: Perda de código-fonte ou sobrescrita acidental.

-Probabilidade: Baixa;
-Impacto: Crítico;
-Nível de Risco: Alto;
-Ação de Mitigação: Uso obrigatório do Git e GitHub para versionamento contínuo, utilizando branches separadas para desenvolvimento (develop) e funcionalidades (feature branches).

Risco R03: Mudança súbita ou alteração no escopo de requisitos.

-Probabilidade: Média;
-Impacto: Alto;
-Nível de Risco: Alto;
-Ação de Mitigação: Aplicar um procedimento formal de Controle de Mudanças com análise prévia de impacto no cronograma antes da aprovação de novos requisitos.

Risco R04: Indisponibilidade potual de membros da equipe.

-Probabilidade: Baixa;
-Impacto: Média;
-Nível de Risco: Médio;
-Ação de Mitigação: Definição transparente de papéis, documentação de tarefas no baklong e acompanhamento constante de cronograma de 5 semanas.

Risco R05: Incompatibilidade de ambiente de desenvolvimento entre a equipe.

-Probabilidade: Baixa;
-Impacto: Médio;
-Nível de Risco: Baixo;
-Ação de Mitigação: Padronização das ferramentas de desenvolvimento (VS Code e Git) e detalhamento de todas as configurações no arquivo README.md do repositótio.

4.estrutura de Comunicação de Ferramentas

-Repositório de Código: GitHub (Controle de versões e Pull Requests);
-Comunicaão: Reuniões rápidas de alinhamento ao início de cada ciclo/semana;
-Cristérios de Sucesso: Validação integral dos 15 RFs, 8 RNFs, execução da suíte de testes e aprovação final na demonstração prática com o professor.