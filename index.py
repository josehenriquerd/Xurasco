from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configurações
PRECOS_CARNE = {"picanha": 80, "frango": 20, "linguica": 30, "costela": 50}
PRECOS_ACOMPANHAMENTOS = {"arroz": 8, "farofa": 10, "vinagrete": 5, "pao_alho": 3}
TEMPOS_PREPARO = {"picanha": 40, "frango": 30, "linguica": 20, "costela": 120}
PRECOS_BEBIDAS = {"cerveja": 3, "refrigerante": 5, "agua": 2, "carvao": 5}

def calcular_carne(adultos, criancas, tipo, carnes):
    base_adulto, base_crianca = 0.4, 0.2
    if tipo == "hamburguer":
        base_adulto, base_crianca = 0.2, 0.1
    elif tipo == "pao_alho":
        base_adulto, base_crianca = 0.1, 0.05

    total_carne_kg = 0
    preco_carne = 0
    for carne in carnes:
        carne_adultos = adultos * base_adulto / len(carnes)
        carne_criancas = criancas * base_crianca / len(carnes)
        total_carne_kg += carne_adultos + carne_criancas
        preco_carne += (carne_adultos + carne_criancas) * PRECOS_CARNE.get(carne, 50)
    return total_carne_kg, preco_carne

def calcular_bebidas(adultos, criancas, modo_festa):
    multiplicador = 1.5 if modo_festa else 1
    cerveja = adultos * 2 * multiplicador
    refrigerante = (adultos * 0.5 + criancas * 0.7) * multiplicador
    agua = (adultos * 0.4 + criancas * 0.5) * multiplicador
    preco_bebidas = (cerveja * PRECOS_BEBIDAS["cerveja"]) + (refrigerante * PRECOS_BEBIDAS["refrigerante"]) + (agua * PRECOS_BEBIDAS["agua"])
    return {"cerveja_latas": cerveja, "refrigerante_litros": refrigerante, "agua_litros": agua, "preco_bebidas": preco_bebidas}

def calcular_acompanhamentos(adultos, criancas, acompanhamentos):
    quantidades = {
        "arroz": (adultos * 0.1) + (criancas * 0.05),
        "farofa": (adultos * 0.08) + (criancas * 0.04),
        "vinagrete": (adultos * 0.05) + (criancas * 0.03),
        "pao_alho": adultos + (criancas * 0.5)
    }
    total_acompanhamentos = {k: quantidades[k] for k in acompanhamentos}
    preco_acompanhamentos = sum(quantidades[k] * PRECOS_ACOMPANHAMENTOS[k] for k in acompanhamentos)
    return total_acompanhamentos, preco_acompanhamentos

def calcular_carvao(total_carne_kg):
    carvao_kg = total_carne_kg * 1.2
    preco_carvao = carvao_kg * PRECOS_BEBIDAS["carvao"]
    return carvao_kg, preco_carvao

def calcular_tempo_preparo(carnes):
    return sum(TEMPOS_PREPARO.get(carne, 30) for carne in carnes) // len(carnes)

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.get_json()
    adultos = dados.get('adultos', 0)
    criancas = dados.get('criancas', 0)
    tipo = dados.get('tipo', 'completo')
    carnes = dados.get('carnes', ['picanha'])
    acompanhamentos = dados.get('acompanhamentos', [])
    modo_festa = dados.get('modo_festa', False)

    if not isinstance(adultos, int) or not isinstance(criancas, int) or adultos < 0 or criancas < 0:
        return jsonify({"error": "Valores inválidos"}), 400

    total_carne_kg, preco_carne = calcular_carne(adultos, criancas, tipo, carnes)
    bebidas = calcular_bebidas(adultos, criancas, modo_festa)
    acompanhamentos, preco_acompanhamentos = calcular_acompanhamentos(adultos, criancas, acompanhamentos)
    carvao_kg, preco_carvao = calcular_carvao(total_carne_kg)
    tempo_preparo = calcular_tempo_preparo(carnes)

    preco_total = preco_carne + bebidas["preco_bebidas"] + preco_acompanhamentos + preco_carvao
    lista_compras = {
        "carnes": {carne: f"{total_carne_kg / len(carnes):.2f} kg" for carne in carnes},
        "bebidas": {k: f"{v:.1f}" for k, v in bebidas.items() if k != "preco_bebidas"},
        "acompanhamentos": {k: f"{v:.2f}" for k, v in acompanhamentos.items()},
        "carvao": f"{carvao_kg:.2f} kg"
    }

    return jsonify({
        "total_carne_kg": total_carne_kg,
        "preco_carne": preco_carne,
        "bebidas": bebidas,
        "acompanhamentos": acompanhamentos,
        "preco_acompanhamentos": preco_acompanhamentos,
        "carvao_kg": carvao_kg,
        "preco_carvao": preco_carvao,
        "tempo_preparo": tempo_preparo,
        "preco_total": preco_total,
        "lista_compras": lista_compras
    })

if __name__ == '__main__':
    app.run(debug=True)