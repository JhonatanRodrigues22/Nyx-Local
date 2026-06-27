# Sprint Report

## Resumo da Sprint 02.5

Sprint 02.5 refinou o Core e adicionou suporte operacional para preparação segura de Git/Pull Request.

O fluxo principal agora mantém `main.py` limpo, delegando a renderização da resposta para uma interface de console.

Também foram aplicadas as preferências da Tech Leader:

- `Request.text` foi renomeado para `Request.message`.
- `Application.process()` foi renomeado para `Application.handle()`.

Nenhuma IA, memória, banco de dados, Skill, Provider, integração, push automático ou Pull Request real foi implementado.

## Arquivos Criados

- `src/nyx_local/interfaces/console.py`
- `scripts/prepare_pr.py`
- `tests/test_console_interface.py`
- `tests/test_prepare_pr.py`

## Arquivos Alterados

- `src/nyx_local/core/models.py`
- `src/nyx_local/application/application.py`
- `src/nyx_local/core/app.py`
- `src/nyx_local/main.py`
- `src/nyx_local/interfaces/__init__.py`
- `tests/test_models.py`
- `tests/test_application.py`
- `README.md`
- `DEVELOPMENT_RULES.md`
- `.ai/WORKFLOW.md`
- `.ai/ARCHITECTURE.md`
- `.ai/ADR.md`
- `.ai/ROADMAP.md`
- `.ai/TESTING.md`
- `.ai/PROJECT.md`
- `SPRINT_REPORT.md`

## Atualizações na `.ai`

- `WORKFLOW.md`: Registrado o fluxo Git/Pull Request oficial e a regra de revisão antes do push.
- `ARCHITECTURE.md`: Registrados `Request.message`, `Application.handle()` e `ConsoleInterface`.
- `ADR.md`: Registradas decisões sobre preparação de PR e refinamento de nomes.
- `ROADMAP.md`: Registrada a Sprint 02.5.
- `TESTING.md`: Atualizado o foco dos testes mínimos.
- `PROJECT.md`: Atualizada a fase atual do projeto.

## Testes Executados

- `pytest`
- `ruff check .`
- `mypy src scripts main.py`
- `python main.py`

## Status do Script de Empacotamento

`scripts/package_project.py` foi executado com sucesso e gerou `dist/nyx_local_project.zip`.

## Status do Script de Preparação Git/PR

`scripts/prepare_pr.py` foi criado.

O script:

- verifica se Git está instalado;
- verifica se o projeto está dentro de um repositório Git;
- mostra a branch atual;
- cria ou troca para a branch informada;
- roda testes;
- gera pacote limpo;
- mostra arquivos alterados;
- sugere título e descrição de commit;
- informa comandos de commit, push e Pull Request;
- não executa push automático;
- não cria Pull Request real automaticamente.

O diretório local atual ainda não está dentro de um repositório Git, então a execução completa do fluxo de branch não foi realizada nesta máquina.

## Sugestões para Tech Leader

Nenhuma sugestão arquitetural nova identificada nesta Sprint.

## Riscos Encontrados

- O fluxo Git/PR depende de o projeto estar dentro de um repositório Git para criar branch e listar alterações.
- O GitHub CLI é opcional; quando ausente, o script fornece instruções manuais.
