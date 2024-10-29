# -*- coding: utf-8 -*-
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import time
import threading
import random

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
    """Gera uma mensagem de marketing aleatória."""
    messages = [
        "🌟 Olá! Sabia que a vida é como uma quentinha? Às vezes precisa de um pouco mais de tempero! 🔥",
        "✨ Ei, você! Estamos com saudades do seu paladar! Venha dar uma espiadinha no nosso cardápio! 😋",
        "🍽️ Seu estômago está gritando por comida! Passe no Lar Brasa e faça ele sorrir. 😄",
        "🥳 Estamos esperando você para uma festa no seu paladar! 🎉",
        "🎈 Oi! Se a sua fome tivesse um nome, seria 'Lar Brasa'. Venha nos visitar! 🍽️💖"
    ]
    return random.choice(messages)

def schedule_marketing_message(to):
    """Agenda uma mensagem de marketing se nenhum pedido for feito em 5 minutos."""
    def delayed_message():
        time.sleep(300)  # Espera 5 minutos
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
        response.message(marketing_queue.pop(from_number))

    # Verifica se é um pedido usando padrões comuns
    if "total do pedido" in msg or "====== pedido" in msg:
        order_message = """
🎉 Pedido Recebido! 🎉

✅ Seu pedido foi registrado com sucesso! 
   Agradecemos pela preferência e estamos ansiosos para servi-lo! 😊

🛵 Prazo de entrega: 40 a 60 minutos.
"""
        response.message(order_message)
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
        response.message("💬 Mande uma mensagem e responderemos o mais rápido possível!")
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
    app.run(port=5000)
