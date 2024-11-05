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

    # **Comentado**: A função que verifica se o restaurante está aberto
    # if not is_restaurant_open():
    #     response.message("🚫 O restaurante está fechado no momento. Funcionamos de segunda a sábado, das 11h às 14h. Volte mais tarde!")
    #     return str(response)

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
        response.message("💬 Mande uma mensagem e responderemos o mais rápido possível!")
    else:
        # Responde com o menu para qualquer outra mensagem
        response.message(MENU)

    return str(response)
