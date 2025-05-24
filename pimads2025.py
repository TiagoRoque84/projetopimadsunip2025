import json, getpass, random

ARQUIVO = 'dados.json'
ADMIN_NOME = 'admin'
ADMIN_SENHA = 'admin123'

def carrega_dados():
    try:
        with open(ARQUIVO, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"usuarios": [], "questoes": {}}

def salva_dados(d):
    with open(ARQUIVO, 'w') as f:
        json.dump(d, f, indent=2)

def cadastro():
    d = carrega_dados()
    nome = input("Nome: ")
    senha = getpass.getpass("Senha: ")
    novo = {"id": len(d["usuarios"]) + 1, "nome": nome, "senha": senha, "acertos": []}
    d["usuarios"].append(novo)
    salva_dados(d)
    print("✅ Usuário cadastrado!")

def cadastro():
    d = carrega_dados()
    nome = input("Nome: ")
    if any(u["nome"] == nome for u in d["usuarios"]):
        print("❌ Nome de usuário já cadastrado. Tente outro.")
        return
    senha = getpass.getpass("Senha: ")
    novo = {"id": len(d["usuarios"]) + 1, "nome": nome, "senha": senha, "acertos": []}
    d["usuarios"].append(novo)
    salva_dados(d)
    print("✅ Usuário cadastrado!")

def login():
    d = carrega_dados()
    nome = input("Nome: ")
    senha = getpass.getpass("Senha: ")
    if nome == ADMIN_NOME and senha == ADMIN_SENHA:
        return {"nome": ADMIN_NOME, "id": 0, "admin": True}
    for u in d["usuarios"]:
        if u["nome"] == nome and u["senha"] == senha:
            return {**u, "admin": False}
    print("❌ Usuário ou senha incorretos.")
    return None

def alterar_senha(user):
    d = carrega_dados()
    for u in d["usuarios"]:
        if u["id"] == user["id"]:
            nova = getpass.getpass("Digite a nova senha: ")
            u["senha"] = nova
            salva_dados(d)
            print("🔐 Senha atualizada com sucesso!")
            return

def deletar_conta(user):
    d = carrega_dados()
    d["usuarios"] = [u for u in d["usuarios"] if u["id"] != user["id"]]
    salva_dados(d)
    print("🗑️ Conta deletada com sucesso.")
    return True

def adicionar_questao():
    d = carrega_dados()
    if "questoes" not in d:
        d["questoes"] = {}
    print("\nCategorias disponíveis para adicionar questões:")
    categorias = list(d["questoes"].keys())
    if not categorias:
        print("(nenhuma categoria ainda)")
    for i, cat in enumerate(categorias, 1):
        print(f"{i}. {cat}")
    cat_op = input("\nEscolha o número da categoria ou digite uma nova: ").strip()
    if cat_op.isdigit() and 1 <= int(cat_op) <= len(categorias):
        cat = categorias[int(cat_op)-1]
    else:
        cat = cat_op.lower()
        if cat not in d["questoes"]:
            d["questoes"][cat] = []
    pergunta = input("Digite a pergunta: ")
    resposta = input("Digite a resposta correta: ")
    d["questoes"][cat].append([pergunta, resposta])
    salva_dados(d)
    print("✅ Questão adicionada com sucesso!")

def editar_questao():
    d = carrega_dados()
    if not d["questoes"]:
        print("\n⚠️ Nenhuma questão cadastrada ainda.")
        return
    categorias = list(d["questoes"].keys())
    print("\nCategorias disponíveis:")
    for i, cat in enumerate(categorias, 1):
        print(f"{i}. {cat}")
    try:
        op = int(input("\nEscolha a categoria para editar (número): "))
        cat = categorias[op-1]
        perguntas = d["questoes"][cat]
        if not perguntas:
            print("⚠️ Nenhuma pergunta nessa categoria.")
            return
        print(f"\n📚 Questões da categoria '{cat}':")
        for i, (q, r) in enumerate(perguntas, 1):
            print(f"{i}. {q} -> {r}")
        idx = int(input("\nDigite o número da pergunta que deseja editar: ")) - 1
        if 0 <= idx < len(perguntas):
            nova_pergunta = input("Nova pergunta: ")
            nova_resposta = input("Nova resposta: ")
            d["questoes"][cat][idx] = [nova_pergunta, nova_resposta]
            salva_dados(d)
            print("✅ Questão atualizada com sucesso!")
        else:
            print("❌ Número inválido.")
    except:
        print("❌ Erro ao tentar editar questão.")

def listar_usuarios():
    d = carrega_dados()
    print("\n📋 Lista de usuários cadastrados:")
    for u in d["usuarios"]:
        print(f"ID: {u['id']} | Nome: {u['nome']} | Pontuação: {sum(u['acertos'])} pontos")

def excluir_usuario():
    d = carrega_dados()
    listar_usuarios()
    try:
        uid = int(input("\nDigite o ID do usuário a ser removido: "))
        usuario = next((u for u in d["usuarios"] if u["id"] == uid), None)
        if usuario:
            confirm = input(f"Tem certeza que deseja remover o usuário '{usuario['nome']}'? (s/n): ").lower()
            if confirm == 's':
                d["usuarios"] = [u for u in d["usuarios"] if u["id"] != uid]
                salva_dados(d)
                print("🗑️ Usuário removido com sucesso.")
            else:
                print("❌ Operação cancelada.")
        else:
            print("Usuário não encontrado.")
    except ValueError:
        print("ID inválido.")

def exibir_questoes():
    d = carrega_dados()
    if not d["questoes"]:
        print("\n⚠️ Nenhuma questão cadastrada ainda.")
        return
    print("\n📚 Questões cadastradas:")
    for categoria, perguntas in d["questoes"].items():
        print(f"\nCategoria: {categoria}")
        for i, (pergunta, resposta) in enumerate(perguntas, 1):
            print(f"{i}. {pergunta} -> Resposta: {resposta}")

def estatisticas():
    d = carrega_dados()
    todas = [a for u in d["usuarios"] for a in u["acertos"] if a > 0]
    if not todas:
        print("\n📊 Nenhuma estatística disponível ainda.")
        return
    media = sum(todas) / len(todas)
    maxima = max(todas)
    minima = min(todas)
    print("\n📈 Estatísticas Gerais:")
    print(f"- Tentativas registradas: {len(todas)}")
    print(f"- Média de acertos: {media:.2f}")
    print(f"- Maior pontuação: {maxima}")
    print(f"- Menor pontuação: {minima}")

def quiz(user):
    d = carrega_dados()
    u = next(u for u in d["usuarios"] if u["id"] == user["id"])
    categorias = list(d["questoes"].keys())
    if not categorias:
        print("Sem categorias disponíveis. Aguarde o administrador adicionar questões.")
        return
    print("\nCategorias disponíveis:")
    for i, cat in enumerate(categorias, 1):
        print(f"{i}. {cat}")
    print(f"{len(categorias)+1}. Todas misturadas")
    try:
        op = int(input("\nEscolha a categoria (digite o número): "))
        if op == len(categorias)+1:
            perguntas = [q for lista in d["questoes"].values() for q in lista]
        else:
            perguntas = d["questoes"][categorias[op-1]]
    except:
        print("Opção inválida.")
        return
    if not perguntas:
        print("Sem perguntas nessa categoria.")
        return
    random.shuffle(perguntas)
    acertos = sum(1 for q,a in perguntas if input(q+" ") == a)
    u["acertos"].append(acertos)
    salva_dados(d)
    print(f"🎯 Acertou {acertos}/{len(perguntas)}")

def ranking_por_categoria():
    d = carrega_dados()
    if not d["questoes"]:
        print("\n❌ Nenhuma categoria com questões cadastradas.")
        return
    for categoria in d["questoes"]:
        print(f"\n🏆 Ranking - Categoria: {categoria}")
        pontuacoes = []
        for u in d["usuarios"]:
            total = 0
            for quiz, perguntas in zip(u.get("categorias", []), u["acertos"]):
                if quiz == categoria:
                    total += perguntas
            if total:
                pontuacoes.append((u["nome"], total))
        if not pontuacoes:
            print("Nenhum usuário respondeu essa categoria.")
            continue
        pontuacoes.sort(key=lambda x: x[1], reverse=True)
        for i, (nome, pontos) in enumerate(pontuacoes, 1):
            print(f"{i}. {nome} - {pontos} pontos")


def ranking():
    d = carrega_dados()
    print("\n🏆 Ranking de Usuários por Pontuação Total:")
    ranking = [(u["nome"], sum(u["acertos"])) for u in d["usuarios"]]
    ranking.sort(key=lambda x: x[1], reverse=True)
    for i, (nome, pontos) in enumerate(ranking, 1):
        print(f"{i}. {nome} - {pontos} pontos")

def menu():
    user = None
    while True:
        if not user:
            print("\n1. Cadastrar\n2. Login\n3. Sair")
            op = input(">> ")
            if op == "1": cadastro()
            elif op == "2": user = login()
            elif op == "3": break
            else: print("Opção inválida.")
        elif user.get("admin"):
            print("\nADMINISTRADOR")
            print("1. Adicionar Questão")
            print("2. Editar Questão")
            print("3. Ver Ranking")
            print("4. Ver Estatísticas")
            print("5. Listar Usuários")
            print("6. Excluir Usuário")
            print("7. Exibir Questões")
            print("8. Logout")
            print("9. Sair")
            op = input(">> ")
            if op == "1": adicionar_questao()
            elif op == "2": editar_questao()
            elif op == "3": ranking()
            elif op == "4": estatisticas()
            elif op == "5": listar_usuarios()
            elif op == "6": excluir_usuario()
            elif op == "7": exibir_questoes()
            elif op == "8": user = None
            elif op == "9": break
            else: print("Opção inválida.")
        else:
            print(f"\nUsuário: {user['nome']} (ID: {user['id']})")
            print("1. Fazer Quiz")
            print("2. Ver Ranking")
            print("3. Alterar Senha")
            print("4. Deletar Conta")
            print("5. Logout")
            print("6. Sair")
            op = input(">> ")
            if op == "1": quiz(user)
            elif op == "2": ranking()
            elif op == "3": alterar_senha(user)
            elif op == "4":
                if deletar_conta(user):
                    user = None
            elif op == "5": user = None
            elif op == "6": break
            else: print("Opção inválida.")

if __name__ == "__main__":
    menu()
