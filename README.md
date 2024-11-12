🍔 WhatsApp Bot para Restaurantes 🍔

Este projeto é um bot para WhatsApp, desenvolvido para automatizar o atendimento de restaurantes! Agora, os clientes podem fazer pedidos, ver o cardápio, consultar horário de funcionamento e muito mais de forma simples e rápida! 💬✨

Funcionalidades 🚀

🍽️ Menu Interativo: Escolha entre fazer um pedido, ver o cardápio, horário e localização.
✅ Confirmação de Pedido: Receba a confirmação e o prazo de entrega.
💌 Marketing Automático: Envie promoções se o cliente ficar inativo por mais de 5 minutos.
📝 Feedback: Solicite feedback após 1 hora do pedido.
Tecnologias ⚙️

🐍 Python + Flask: Framework web para criar a lógica do bot.
📱 Twilio API: Para integração com o WhatsApp e comunicação com os clientes.
⏳ Threading + time: Para agendar mensagens automáticas e interações.
🛠️ Instalação

Clone o repositório:
git clone https://github.com/allankdev/botwhats.git
cd botwhats
Instale as dependências:
pip install -r requirements.txt
Inicie o servidor:
python3 bot.py
Ou use Gunicorn para produção:

gunicorn app:app
💬 Uso

Configure a URL do Twilio para o endpoint /bot. O bot irá responder com o menu e processar as interações automaticamente.

💡 Contribuição

Sinta-se à vontade para sugerir melhorias, abrir issues ou enviar pull requests!
