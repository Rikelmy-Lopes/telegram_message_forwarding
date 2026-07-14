# Telegram Message Forwarding

Bot do Telegram para encaminhamento e filtragem automática de mensagens de canais ou grupos.

## 🛠️ Variáveis de Ambiente

O bot necessita de três variáveis de ambiente configuradas para funcionar:

* **`API_ID`**: ID da API obtido em [my.telegram.org](https://my.telegram.org).
* **`API_HASH`**: Hash da API obtido em [my.telegram.org](https://my.telegram.org).
* **`BOT_TOKEN`**: Token do bot gerado pelo [@BotFather](https://t.me/BotFather).

---

## 🚀 Como Executar

Para iniciar o bot, execute o seguinte comando no terminal:

```bash
python ./src/main.py
```
Na primeira execução, o terminal solicitará que você insira o seu número de telefone e o código de verificação enviado pelo Telegram para autorizar a conexão.

---


## 🤖 Comandos Disponíveis

* **`/words`** - Gerenciar a lista de palavras filtradas.
* **`/chats`** - Gerenciar os canais e grupos monitorados.
* **`/cancel`** - Cancelar a operação atual a qualquer momento.
