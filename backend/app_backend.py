from flask import Flask, jsonify, request
import sqlite3
app = Flask(__name__)

# Conexão com o banco de dados
conn = sqlite3.connect("pdv.db", check_same_thread=False)
c = conn.cursor()

# Criar tabelas se não existirem
c.execute('''CREATE TABLE IF NOT EXISTS produtos (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             nome TEXT NOT NULL,
             preco REAL NOT NULL,
             estoque INTEGER NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS vendas (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             produto_id INTEGER,
             quantidade INTEGER,
             total REAL,
             data TEXT DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# Rota para listar todos os produtos
@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    c.execute("SELECT * FROM produtos")
    produtos = c.fetchall()
    return jsonify(produtos)

# Rota para cadastrar um novo produto
@app.route('/api/produtos', methods=['POST'])
def cadastrar_produto():
    data = request.json
    nome = data.get("nome")
    preco = data.get("preco")
    estoque = data.get("estoque")

    if not nome or not preco or not estoque:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    try:
        c.execute("INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)", (nome, preco, estoque))
        conn.commit()
        return jsonify({"mensagem": "Produto cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota para atualizar o estoque de um produto
@app.route('/api/produtos/<int:id>', methods=['PUT'])
def atualizar_estoque(id):
    data = request.json
    quantidade = data.get("quantidade")

    if quantidade is None or quantidade <= 0:
        return jsonify({"erro": "Quantidade inválida"}), 400

    c.execute("UPDATE produtos SET estoque = estoque - ? WHERE id = ?", (quantidade, id))
    conn.commit()
    return jsonify({"mensagem": "Estoque atualizado com sucesso!"})

# Rota para registrar uma venda
@app.route('/api/vendas', methods=['POST'])
def registrar_venda():
    data = request.json
    produto_id = data.get("produto_id")
    quantidade = data.get("quantidade")
    total = data.get("total")

    if not produto_id or not quantidade or not total:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    try:
        c.execute("INSERT INTO vendas (produto_id, quantidade, total) VALUES (?, ?, ?)", (produto_id, quantidade, total))
        conn.commit()
        return jsonify({"mensagem": "Venda registrada com sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota para listar o histórico de vendas
@app.route('/api/historico', methods=['GET'])
def listar_historico():
    c.execute("SELECT * FROM vendas")
    vendas = c.fetchall()
    return jsonify(vendas)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)