import requests
import json
import telebot


api = "5782662896:AAHAvG2PFRG58cw4yI6L418jZyrMnASkks2"     #colocar seu token do bot
chat_id = "-1001853680252"                                  #colocar id do chat, para super grupo colocar -100 antes

bot = telebot.TeleBot(api)

bot.send_message(chat_id, text="bot iniciado")

    
analise_sinal = False
entrada = 0
max_gale = 2                   #escolher a quantidade de gale que o bot vai mandar

resultado = []
check_resultado = []

def reset():
    global analise_sinal
    global entrada
    
    entrada = 0
    analise_sinal = False
    return


def martingale():
    global entrada
    entrada += 1
    
    if entrada <= max_gale:
        bot.send_message(chat_id, text=f"⚠️atenção gale {entrada}⚠️")
    else:
        loss()
        reset()
    return


def api():
    global resultado
    req = requests.get('https://blaze.com/api/roulette_games/recent')
    a = json.loads(req.content)
    jogo = [x['roll'] for x in a]
    resultado = jogo
    return jogo

def win():
    bot.send_message(chat_id, text="✅")                          #para enviar esticker basta trocar para: bot.send_sticker(chat_id, sticker"colocar o id do sticker aqui")
    return 
def loss():
    bot.send_message(chat_id, text="❌")
    return
 
def correcao(results, color):
    if results[0:1] == ['P'] and color == '⚫️':
        win()
        reset()
        return
    
    elif results[0:1] == ['V'] and color == '🛑':
        win()
        reset()
        return
    
    elif results[0:1] == ['P'] and color == '🛑':
        martingale()
        return
    
    elif results[0:1] == ['V'] and color == '⚫️':
        martingale()
        return
    
    
    elif results[0:1] == ['B']:
        win()
        reset()

def enviar_sinal(cor, padrao):          
    bot.send_message(chat_id, text=f'''
🚨sinal encontrado🚨

⏯️ Padrão: {padrao}

💶entrar no {cor}

🦾proteger no ⚪️

🐓2 martingale: (opcional)''')
    return


def estrategy(resultado):
    global analise_sinal
    global cor_sinal
    global cores
    
    cores = []
    for x in resultado:
        if x >= 1 and x <= 7:
            color = 'V'
            cores.append(color)
        elif x >= 8 and x <= 14:
            color = 'P'
            cores.append(color)
        else:
            color = 'B'
            cores.append(color)
    print(cores)
    
    
    if analise_sinal == True:
        correcao(cores, cor_sinal)
    else:
        #aqui você coloca suas estratégias, para adicionar mais estratégia, é só copiar o if e colar em baixo na mesma linha, e modificar a estretegia e o nome do padrao
        if cores[0:4] == ['P','V','P','V']:
            cor_sinal = '🛑'
            padrao = '👻Ghost👻'
            enviar_sinal(cor_sinal, padrao)
            analise_sinal = True
            print('sinal enviado')
        
        if cores[0:3] == ['V','P','V']:
            cor_sinal = '⚫️'
            padrao = '👑King👑'
            enviar_sinal(cor_sinal, padrao)
            analise_sinal = True
            print('sinal enviado')  
        
        if cores[0:2] == ['V','P']:
            cor_sinal = '⚫️'
            padrao = '🥷🏽Samurai🥷🏽'
            enviar_sinal(cor_sinal, padrao)
            analise_sinal = True
            print('sinal enviado') 

while True:
    api()
    if resultado != check_resultado:
        check_resultado = resultado
        #print(resultado)
        estrategy(resultado)


    
        
        
        
        
