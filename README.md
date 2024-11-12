WhatsApp Bot para Restaurantes

Este projeto é um bot para WhatsApp desenvolvido para automatizar o atendimento em restaurantes, permitindo gerenciar pedidos, responder a perguntas frequentes e enviar mensagens de marketing personalizadas aos clientes.

Funcionalidades

Menu Interativo: Oferece opções para fazer pedidos, visualizar o cardápio, horário de funcionamento e localização.
Confirmação de Pedidos: Recebe pedidos e confirma com o cliente, mostrando o prazo de entrega.
Marketing Automatizado: Envia mensagens promocionais se o cliente permanecer inativo por mais de 5 minutos.
Feedback: Solicita feedback do cliente após 1 hora do pedido.
Tecnologias Utilizadas

Python e Flask: Framework web para construir a lógica do bot.
Twilio API: Integração com o WhatsApp para envio e recebimento de mensagens.
Threading e time: Para agendamento e envio de mensagens automáticas.
Instalação

Clone este repositório:
git clone https://github.com/allankdev/botwhats.git
cd botwhats
Instale as dependências:
pip install -r requirements.txt
Inicie o servidor:
python3 bot.py
Ou, para ambientes de produção, use:

gunicorn app:app
Uso

Configure a URL do Twilio para apontar para o endpoint /bot do seu servidor. O bot responderá automaticamente com o menu de opções e processará as mensagens conforme o fluxo definido.

Contribuição

Sinta-se à vontade para abrir issues ou enviar PRs com sugestões e melhorias.

