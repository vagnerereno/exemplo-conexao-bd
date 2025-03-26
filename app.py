from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Para mensagens flash

# Função para conectar ao banco de dados
def get_connection():
    try:
        conexao = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="", # Sua senha aqui.
            database="sistema_ingressos"
        )
        return conexao
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        return None

# Função para cadastrar ingresso no banco de dados
def cadastrar_ingresso(tipo, preco, quantidade, evento_id):
    conexao = get_connection()
    if conexao is None:
        flash("Erro ao conectar ao banco de dados", "danger")
        return
    try:
        cursor = conexao.cursor()
        sql = """
        INSERT INTO Ingresso (tipo, preco, quantidadeDisponivel, Evento_idEvento)
        VALUES (%s, %s, %s, %s)
        """
        valores = (tipo, preco, quantidade, evento_id)
        cursor.execute(sql, valores)
        conexao.commit()
        flash("Ingresso cadastrado com sucesso!", "success")
    except mysql.connector.Error as erro:
        flash(f"Erro ao cadastrar ingresso: {erro}", "danger")
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

@app.route('/')
def home():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    tipo = request.form['tipo']
    preco = request.form['preco']
    quantidade = request.form['quantidade']
    evento_id = request.form['evento_id']
    cadastrar_ingresso(tipo, preco, quantidade, evento_id)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
