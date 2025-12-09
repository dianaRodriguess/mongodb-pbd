from datetime import datetime, timedelta
from config.database import db_instance
from controllers.usuario_controller import UsuarioController
from controllers.atividade_controller import AtividadeController
from queries import att_andamento_responsa, att_stats_user


def limpar_banco():
    db = db_instance.get_database()
    if db is not None:
        db["usuarios"].delete_many({})
        db["atividades"].delete_many({})
        print("Banco de dados limpo!\n")
    else:
        print("Erro: Não foi possível limpar o banco, conexão inválida.\n")


def crud_usuarios():
    print("\n" + "=" * 70)
    print("CRUD DE USUÁRIOS")
    print("=" * 70 + "\n")

    usuario_ctrl = UsuarioController()

    # CREATE
    print("--- Criando usuários ---")
    usuario1 = usuario_ctrl.criar(
        nome="Maria Silva", email="maria.silva@email.com", cargo="Desenvolvedora Senior"
    )

    usuario2 = usuario_ctrl.criar(
        nome="João Santos", email="joao.santos@email.com", cargo="Gerente de Projetos"
    )

    usuario3 = usuario_ctrl.criar(
        nome="Ana Costa", email="ana.costa@email.com", cargo="Designer UX/UI"
    )

    print()

    # READ
    print("--- Lista todos os usuários ---")
    usuarios = usuario_ctrl.listar_todos()
    for u in usuarios:
        print(f"  • {u.nome} - {u.email} ({u.cargo})")
    print()

    print("--- Busca usuário por ID ---")
    if usuario1 is not None:
        usuario_encontrado = usuario_ctrl.buscar_por_id(usuario1._id)
        if usuario_encontrado is not None:
            print(f"Encontrado: {usuario_encontrado}\n")
        else:
            print("Usuário não encontrado")

    # UPDATE
    print("--- Atualiza cargo do usuário ---")
    if usuario1 is not None:
        usuario_ctrl.atualizar(usuario_id=usuario1._id, cargo="Tech Lead")
    print()

    # DELETE
    print("--- DELETE: Deletando usuários ---")
    print(f"  Comando: usuario_ctrl.deletar(usuario_id)\n")

    return [usuario1, usuario2, usuario3]


def crud_atividades(usuarios):
    print("\n" + "=" * 70)
    print("CRUD DE ATIVIDADES")
    print("=" * 70 + "\n")

    atividade_ctrl = AtividadeController()

    # CREATE 
    print("--- Criando atividades ---")

    ativ1 = atividade_ctrl.criar(
        titulo="Implementar autenticação JWT",
        descricao="Desenvolver sistema de autenticação com tokens JWT para a API",
        responsavel_id=usuarios[0]._id,
        status="em_andamento",
        prazo=datetime.now() + timedelta(days=7),
    )

    ativ2 = atividade_ctrl.criar(
        titulo="Revisar código do módulo de pagamentos",
        descricao="Code review completo do módulo de pagamentos antes do deploy",
        responsavel_id=usuarios[1]._id,
        status="pendente",
        prazo=datetime.now() + timedelta(days=3),
    )

    ativ3 = atividade_ctrl.criar(
        titulo="Criar protótipo da tela de dashboard",
        descricao="Design e protótipo interativo da nova tela de dashboard",
        responsavel_id=usuarios[2]._id,
        status="em_andamento",
        prazo=datetime.now() + timedelta(days=5),
    )

    ativ4 = atividade_ctrl.criar(
        titulo="Documentar API REST",
        descricao="Documentação completa dos endpoints da API usando Swagger",
        responsavel_id=usuarios[0]._id,
        status="pendente",
        prazo=datetime.now() + timedelta(days=10),
    )

    ativ5 = atividade_ctrl.criar(
        titulo="Implementar testes unitários",
        descricao="Criar testes unitários para os controllers principais",
        responsavel_id=usuarios[0]._id,
        status="concluida",
    )

    print()

    # READ 
    print("--- Lista todas as atividades ---")
    atividades = atividade_ctrl.listar_todas()
    for a in atividades:
        print(f"  • [{a.status}] {a.titulo}")
    print()

    # READ 
    print("--- Atividades em andamento ---")
    em_andamento = atividade_ctrl.listar_por_status("em_andamento")
    for a in em_andamento:
        print(f"  • {a.titulo}")
    print()

    # READ 
    print(f"--- Atividades de {usuarios[0].nome} ---")
    atividades_maria = atividade_ctrl.listar_por_responsavel(usuarios[0]._id)
    for a in atividades_maria:
        print(f"  • [{a.status}] {a.titulo}")
    print()

    # UPDATE
    print("--- Muda status de uma atividade ---")
    if ativ2 is not None:
        atividade_ctrl.atualizar(atividade_id=ativ2._id, status="em_andamento")
    print()

    # DELETE 
    print("--- DELETE: Deletando atividades ---")
    print(f"  Comando: atividade_ctrl.deletar(atividade_id)\n")

    return atividades


def executa_queries():
    att_andamento_responsa.executar()
    att_stats_user.executar()


def exibir_estatisticas():
    print("\n" + "=" * 70)
    print("ESTATÍSTICAS GERAIS DO SISTEMA")
    print("=" * 70 + "\n")

    usuario_ctrl = UsuarioController()
    atividade_ctrl = AtividadeController()

    total_usuarios = usuario_ctrl.contar()
    total_atividades = atividade_ctrl.contar()
    pendentes = atividade_ctrl.contar_por_status("pendente")
    em_andamento = atividade_ctrl.contar_por_status("em_andamento")
    concluidas = atividade_ctrl.contar_por_status("concluida")

    print(f"Total de usuários: {total_usuarios}")
    print(f"Total de atividades: {total_atividades}")
    print(f" • Pendentes: {pendentes}")
    print(f" • Em andamento: {em_andamento}")
    print(f" • Concluídas: {concluidas}")
    print()


def main():
    print("\n" + "=" * 70)
    print("SISTEMA DE GESTÃO DE ATIVIDADES")
    print("=" * 70)

    try:
        db_instance.connect()
        limpar_banco()

        usuarios = crud_usuarios()
        atividades = crud_atividades(usuarios)

        exibir_estatisticas()
        executa_queries()

        print("\n" + "=" * 70)
        print("PROJETO DE BANCO DE DADOS COM PYTHON E MONGODB")
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"\nErro na execução: {e}\n")

    finally:
        db_instance.close()


if __name__ == "__main__":
    main()
