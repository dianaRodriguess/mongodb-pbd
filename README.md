# Sistema de Gestão de Atividades

Sistema completo de gerenciamento de atividades desenvolvido com **Python 3** e **MongoDB**, implementando operações CRUD e consultas complexas com agregação.

## Sobre o Projeto

Este projeto foi desenvolvido como parte da disciplina de Projeto e Administração de Banco de Dados, demonstrando:

- Modelagem de dados NoSQL (MongoDB)
- Operações CRUD completas
- Consultas complexas com agregação
- Padrão de projeto (MVC adaptado)

## Tecnologias Utilizadas

- **Python 3.13.5**
- **MongoDB 7.0** (via Docker)
- **PyMongo** - Driver Python para MongoDB
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## Estrutura do Projeto

```
mongodb-pbd/
├── .env                                 # Variáveis de ambiente (não versionado)
├── .gitignore                           # Arquivos ignorados pelo Git
├── README.md                            # Documentação do projeto
├── requirements.txt                     # Dependências Python
├── main.py                              # Arquivo principal de execução
├── config/
│   └── database.py                      # Configuração e conexão MongoDB
├── models/
│   ├── usuario.py                       # Modelo de Usuário
│   └── atividade.py                     # Modelo de Atividade
├── controllers/
│   ├── usuario_controller.py            # CRUD de Usuários
│   └── atividade_controller.py          # CRUD de Atividades
└── queries/
    ├── __init__.py                      # Torna queries um pacote Python
    ├── att_andamento_responsa.py        # Consulta 1: JOIN com agregação
    └── att_stats_user.py                # Consulta 2: Estatísticas agrupadas
```

## Modelagem do Banco de Dados

### Coleção: `usuarios`
```json
{
  "_id": ObjectId,
  "nome": String,
  "email": String (único),
  "cargo": String,
  "data_criacao": DateTime
}
```

### Coleção: `atividades`
```json
{
  "_id": ObjectId,
  "titulo": String,
  "descricao": String,
  "responsavel_id": ObjectId (referência a usuarios),
  "status": String ("pendente" | "em_andamento" | "concluida"),
  "prazo": DateTime,
  "data_criacao": DateTime,
  "data_conclusao": DateTime
}
```

## Operações Implementadas

### CRUD de Usuários

#### Create (Criar)
```python
usuario_ctrl.criar(
    nome="Maria Silva",
    email="maria.silva@email.com",
    cargo="Desenvolvedora"
)
```

#### Read (Ler)
```python
usuario = usuario_ctrl.buscar_por_id(usuario_id)

usuario = usuario_ctrl.buscar_por_email("maria.silva@email.com")

usuarios = usuario_ctrl.listar_todos()
```

#### Update (Atualizar)
```python
usuario_ctrl.atualizar(
    usuario_id=usuario_id,
    nome="Maria Santos",
    cargo="Tech Lead"
)
```

#### Delete (Deletar)
```python
usuario_ctrl.deletar(usuario_id)
```

### CRUD de Atividades

#### Create (Criar)
```python
atividade_ctrl.criar(
    titulo="Implementar API REST",
    descricao="Desenvolver endpoints da API",
    responsavel_id=usuario_id,
    status="em_andamento",
    prazo=datetime.now() + timedelta(days=7)
)
```

#### Read (Ler)
```python
atividade = atividade_ctrl.buscar_por_id(atividade_id)

atividades = atividade_ctrl.listar_todas()

atividades = atividade_ctrl.listar_por_status("em_andamento")

atividades = atividade_ctrl.listar_por_responsavel(usuario_id)
```

#### Update (Atualizar)
```python
atividade_ctrl.atualizar(
    atividade_id=atividade_id,
    status="concluida",
    descricao="Descrição atualizada"
)
```

#### Delete (Deletar)
```python
atividade_ctrl.deletar(atividade_id)
```

## Consultas Complexas

### Consulta 1: Atividades em Andamento com Responsável

Lista todas as atividades com status "em_andamento" junto com os dados completos do responsável.

**Exemplo de saída:**
```
--- Atividade 1 ---
ID: 674c5a1b2e3f4a5b6c7d8e9f
Título: Implementar autenticação JWT
Descrição: Desenvolver sistema de autenticação com tokens JWT
Status: em_andamento
Prazo: 15/12/2024 14:30
Responsável: Maria Silva
Email: maria.silva@email.com
Cargo: Tech Lead
```

### Consulta 2: Estatísticas por Usuário

Agrupa atividades por usuário mostrando estatísticas detalhadas de cada status.

**Exemplo de saída:**
```
--- Usuário 1 ---
Nome: Maria Silva
Email: maria.silva@email.com
Cargo: Tech Lead

Estatísticas:
  • Total de atividades: 5
  • Pendentes: 2
  • Em andamento: 2
  • Concluídas: 1
  • Taxa de conclusão: 20.0%

Atividades:
    - Implementar autenticação JWT (em_andamento)
    - Documentar API REST (pendente)
    - Implementar testes unitários (concluida)
```

## Saída Completa da Execução

Ao executar `python main.py`, o sistema:

1. Conecta ao MongoDB
2. Limpa o banco (apenas para demonstração)
3. Cria 3 usuários de exemplo
4. Cria 5 atividades de exemplo
5. Exibe estatísticas gerais
6. Executa as 2 consultas complexas
7. Fecha a conexão

## Licença

Este projeto é de uso educacional.

---

**Disciplina:** Projeto e Administração de Banco de Dados  
**Instituição:** UFRN
**Ano:** 2025
