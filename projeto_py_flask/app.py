from flask import Flask, render_template, request, jsonify
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

sabores = ["maracuja", "brigadeiro", "amendoim",
           "cappuccino", "morango", "ninho", "beijinho"]
dias_da_semana = ["terça-feira", "quarta-feira",
                  "quinta-feira", "sexta-feira", "sábado"]
horarios_manha = ("11:30", "13:30")
horarios_noite = ("16:00", "20:00")
vendas = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))


def horario_valido(hora_venda):
    manha_inicio = datetime.strptime(horarios_manha[0], '%H:%M').time()
    manha_fim = datetime.strptime(horarios_manha[1], '%H:%M').time()
    noite_inicio = datetime.strptime(horarios_noite[0], '%H:%M').time()
    noite_fim = datetime.strptime(horarios_noite[1], '%H:%M').time()
    return manha_inicio <= hora_venda <= manha_fim or noite_inicio <= hora_venda <= noite_fim


@app.route("/")
def index():
    return render_template("front.html")


@app.route("/registrar", methods=["POST"])
def registrar_venda():
    data = request.json
    dia = data.get("dia")
    hora = data.get("hora")
    sabor = data.get("sabor")
    quantidade = data.get("quantidade", 0)

    if dia not in dias_da_semana:
        return jsonify({"error": f"'{dia}' não é um dia válido."}), 400

    try:
        hora_venda = datetime.strptime(hora, '%H:%M').time()
    except ValueError:
        return jsonify({"error": f"'{hora}' não é um horário válido."}), 400

    if not horario_valido(hora_venda):
        return jsonify({"error": f"'{hora}' está fora do intervalo permitido."}), 400

    if sabor not in sabores:
        return jsonify({"error": f"'{sabor}' não é um sabor válido."}), 400

    vendas[dia][hora][sabor] += quantidade
    return jsonify({"message": f"Venda registrada: {quantidade} trufas de {sabor} no dia {dia} às {hora}."})


@app.route("/resumo")
def exibir_resumo_vendas():
    resumo = {
        dia: {hora: dict(sabores_venda)
              for hora, sabores_venda in horas_venda.items()}
        for dia, horas_venda in vendas.items()
    }
    return jsonify(resumo)


@app.route("/top-sellers")
def sabores_mais_vendidos():
    mais_vendidos = defaultdict(lambda: defaultdict(tuple))

    for dia, horas_venda in vendas.items():
        for hora, sabores_venda in horas_venda.items():
            if sabores_venda:
                sabor_mais_vendido = max(
                    sabores_venda.items(), key=lambda x: x[1])
                mais_vendidos[dia][hora] = sabor_mais_vendido

    return jsonify({dia: dict(horas) for dia, horas in mais_vendidos.items()})


@app.route("/best-hours")
def horario_com_mais_vendas():
    total_vendas_horario = defaultdict(int)

    for dia, horas_venda in vendas.items():
        for hora, sabores_venda in horas_venda.items():
            total_vendas_horario[hora] += sum(sabores_venda.values())

    if total_vendas_horario:
        horario_mais_vendido = max(
            total_vendas_horario.items(), key=lambda x: x[1])
        return jsonify({"horario": horario_mais_vendido[0], "quantidade": horario_mais_vendido[1]})
    return jsonify({"message": "Nenhuma venda registrada."})


if __name__ == "__main__":
    app.run(debug=True)
