# -*- coding: utf-8 -*-
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import time
import threading
import random
from datetime import datetime

# Inicializa o Flask
app = Flask(__name__)

# Menu principal
MENU = """
🍽️ Bem-vindo ao Lar Brasa restaurante! 🍽️
Como posso te ajudar hoje? 😊

1️⃣ - Fazer pedido  
2️⃣ - Ver cardápio  
3️⃣ - Horário de funcionamento  
4️⃣ - Nossa localização  
0️⃣ - Falar com atendente  
"""

# Armazenar estado do cliente e pedidos pendentes
customer_states = {}
marketing_queue = {}

def generate_marketing_message():
    """Gera uma mensagem de marketing mais criativa e engraçada."""
    messages = [
        "🍽️ Fala sério, quem não ama um prato delicioso? Vem pro Lar Brasa e transforma sua fome em felicidade! 😋",
        "🔥 Fome de verdade é aquela que só o Lar Brasa pode saciar! Não deixe ela te vencer, venha logo! 🍔",
        "🚨 Alerta de fome: seu estômago está chamando, e a única solução é o Lar Brasa!  Venha logo, a fome não espera! 😜",
        "🥳 A comida aqui no Lar Brasa é tão boa que até o GPS vai querer te levar até nós! 🍖",
        "🎉 A vida é curta, mas o prazer de comer no Lar Brasa dura o suficiente para te fazer sorrir o dia todo! 😍",
        "🛸 Já pensou em uma viagem para o sabor? Vem pro Lar Brasa e decola para o paraíso da comida boa! ✈️🍲",
        "⚡ Fome + Lar Brasa = Felicidade garantida! Não perca tempo, vem fazer seu pedido agora mesmo! 🍛💥",
        "🌟 Você e o Lar Brasa: uma combinação perfeita! Sabor incrível, alegria garantida! 😎",
        "💥 Explosão de sabor? Só no Lar Brasa! Vem e prova a nossa comida que é puro amor! 💖",
        "😜 Tá esperando o quê? A sua fome não vai esperar e o Lar Brasa tem exatamente o que você precisa! 🔥"
    ]
    return random.choice(messages)

def schedule_marketing_message(to):
    """Agenda uma mensagem de marketing se nenhum pedido for feito em 10 minutos."""
    def delayed_message():
        time.sleep(600)  # Espera 10 minutos
        # Se o cliente ainda estiver na espera e não tiver feito pedido
        if customer_states.get(to) == 'waiting':
            marketing_queue[to] = generate_marketing_message()

    threading.Thread(target=delayed_message).start()

@app.route('/bot', methods=['POST'])
def bot():
    """Recebe mensagens e responde automaticamente."""
    msg = request.form.get('Body', '').strip().lower()
    from_number = request.form.get('From')
    response = MessagingResponse()

    print(f"Mensagem recebida no bot: {msg}")  # Debugging

    # Verifica se há uma mensagem de marketing pendente e envia antes de qualquer outra resposta
    if from_number in marketing_queue:
        response.message(marketing_queue.pop(from_number))  # Envia a mensagem de marketing
        return str(response)  # Retorna sem o menu, apenas a mensagem de marketing

    # Verifica se é um pedido usando padrões comuns
    if "total do pedido" in msg or "====== pedido" in msg:
        order_message = f"""
        ✅ Seu pedido foi confirmado com sucesso e está em preparo!   
        Agradecemos pela preferência e estamos ansiosos para servi-lo! 😊

        🛵 Prazo de entrega: 40 a 60 minutos.
        """
        response.message(order_message.strip())
        customer_states[from_number] = 'ordered'  # Marca como pedido feito
        return str(response)

    # Se for a primeira mensagem ou o cliente não fez pedido ainda, agenda marketing
    if from_number not in customer_states:
        customer_states[from_number] = 'waiting'
        schedule_marketing_message(from_number)

    # Responde ao menu para outros comandos
    if msg in ['1', 'pedido']:
        response.message("🚀 Para fazer um pedido, acesse nosso site: https://larbrasa.com.br/pedidos")
    elif msg in ['2', 'cardapio']:
        response.message("🍽️ Nosso cardápio delicioso está em: https://larbrasa.com.br")
    elif msg in ['3', 'horario']:
        response.message("🕒 Funcionamos de segunda a sábado, das 11h às 14h. Não funcionamos no feriado. Venha nos visitar! 😊")
    elif msg in ['4', 'localizacao']:
        response.message("📍 Estamos na Rua José Serrano Navarro, 252 - Castelo Branco. Te esperamos!")
    elif msg in ['0', 'atendente']:
        # Alterando a resposta para instruir o cliente a ligar
        response.message("📞 Para falar com um atendente, por favor ligue para o número: 83 98612-9752.")
    else:
        # Responde com o menu para qualquer outra mensagem
        response.message(MENU)

    return str(response)

@app.route('/feedback', methods=['POST'])
def feedback():
    """Recebe feedback do cliente após 1 hora do pedido."""
    msg = request.form.get('Body', '').strip().lower()
    from_number = request.form.get('From')
    response = MessagingResponse()

    if msg:
        response.message("💬 Obrigado pelo seu feedback! Estamos sempre trabalhando para melhorar. Volte sempre! ❤️")
        customer_states[from_number] = None  # Limpa o estado do cliente após o feedback
    else:
        response.message("❓ Por favor, envie seu feedback para que possamos melhorar.")

    return str(response)

@app.route('/test', methods=['GET'])
def test():
    """Endpoint de teste para verificar se o bot está funcionando."""
    return "Bot está funcionando!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
