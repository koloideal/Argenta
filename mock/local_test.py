import readline

def startup_hook():
    readline.insert_text('from startup_hook')

def pre_input_hook():
    readline.insert_text('from pre_input_hook')
    readline.redisplay()

readline.set_startup_hook(startup_hook)
readline.set_pre_input_hook(pre_input_hook)
readline.parse_and_bind('tab: complete')

line = ''
while line != 'stop':
    line = input('!("stop" to quit) Ввод текста: => ')
    print (f'Отправка: {line}')