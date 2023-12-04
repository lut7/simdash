# This version is: Segundou

# Configurações básicas
bypass_sim = 1 # Caso SIM, rodar o app sem a necessidade do Simulador rodando
bypass_net = 0 # Caso SIM, ignorar configurações de rede
acopladois = 0 # Caso SIM, o app inicia "acoplado" ao SIM

#ac selection
aircraft = 152

import tkinter
import pickle
import socket
import threading
import json
try:
    from SimConnect import *
    print("importou SimConnect")
except ModuleNotFoundError:
    print("O módulo SimConnect não foi encontrado. Certifique-se de que está instalado.")

# configuração do cliente e conexão ao servidor, caso bypass esteja 0
if bypass_net == 0:
    print("rodando nets")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(('192.168.0.75', 12345))
        print("Conectado ao servidor.")
    except Exception as e:
        print(f"Erro de Conexão: {e}")


else:
    print("bypassando nets")




 








# CRIAR JANELA PRINCIPAL
window = tkinter.Tk()
window.title("Flight Dashboard")
window.geometry("950x550")







################################################## VARIAVEIS



bypass_sim_tkbo = tkinter.BooleanVar(value=(bypass_sim != 0))  # Use BooleanVar to control the Checkbutton state
acoplado = tkinter.BooleanVar(value= True if acopladois == 1 else False)

# Variaveis python de estado da botoneira
var_alt = 0
var_bat = 0
var_dom = 0
var_pit = 0
var_nav = 0
var_stb = 0
var_bcn = 0
var_tax = 0
var_ldg = 0

# cria variaveis de controle tkinter
alt_tkin = tkinter.IntVar()
bat_tkin = tkinter.IntVar()
dom_tkin = tkinter.IntVar()
pit_tkin = tkinter.IntVar()
nav_tkin = tkinter.IntVar()
stb_tkin = tkinter.IntVar()
bcn_tkin = tkinter.IntVar()
tax_tkin = tkinter.IntVar()
ldg_tkin = tkinter.IntVar()

# Converte as variaveis master de estado do botão para tkinter. 
alt_tkin.set(var_alt)
bat_tkin.set(var_bat)
dom_tkin.set(var_dom)
pit_tkin.set(var_pit)
nav_tkin.set(var_nav)
stb_tkin.set(var_stb)
bcn_tkin.set(var_bcn)
tax_tkin.set(var_tax)
ldg_tkin.set(var_ldg)


# criar variaveis de informação
texto_altitude = tkinter.StringVar()
texto_ias = tkinter.StringVar()
texto_heading = tkinter.StringVar()
texto_fuel = tkinter.StringVar()
texto_hora = tkinter.StringVar()
texto_windspeed = tkinter.StringVar()
texto_windmag = tkinter.StringVar()
texto_oatc = tkinter.StringVar()
texto_baro = tkinter.StringVar()
texto_bateria_tkst = tkinter.StringVar()


# VARIAVEIS DE RADIO

# Variáveis comm1
com1_active_int = tkinter.IntVar(value=118)  # Valor inicial da parte inteira ativa
com1_active_dec = tkinter.IntVar(value=400)   # Valor inicial da parte decimal ativa

com1_standb_int = tkinter.IntVar(value=119)  # Valor inicial da parte inteira standby
com1_standb_dec = tkinter.IntVar(value=500)   # Valor inicial da parte decimal standby

com1_cached_int = tkinter.IntVar()
com1_cached_dec = tkinter.IntVar()

com1_active_txt = tkinter.StringVar(value=121.510)
com1_standb_txt = tkinter.StringVar()
com1_cached_txt = tkinter.StringVar()



# Variáveis nav1
nav1_standb_int = tkinter.IntVar(value=500)  # Valor inicial da parte inteira standby
nav1_standb_dec = tkinter.IntVar(value=50)   # Valor inicial da parte decimal standby

nav1_active_int = tkinter.IntVar(value=524)  # Valor inicial da parte inteira ativa
nav1_active_dec = tkinter.IntVar(value=24)   # Valor inicial da parte decimal ativa

nav1_cached_int = tkinter.IntVar()
nav1_cached_dec = tkinter.IntVar()

nav1_active_txt = tkinter.StringVar(value=900.10)
nav1_standb_txt = tkinter.StringVar()
nav1_cached_txt = tkinter.StringVar()



# Variáveis comm2
com2_standb_int = tkinter.IntVar(value=565)  # Valor inicial da parte inteira standby
com2_standb_dec = tkinter.IntVar(value=560)   # Valor inicial da parte decimal standby

com2_active_int = tkinter.IntVar(value=810)  # Valor inicial da parte inteira ativa
com2_active_dec = tkinter.IntVar(value=810)   # Valor inicial da parte decimal ativa

com2_cached_int = tkinter.IntVar()
com2_cached_dec = tkinter.IntVar()

com2_active_txt = tkinter.StringVar(value=121.510)
com2_standb_txt = tkinter.StringVar()
com2_cached_txt = tkinter.StringVar()



# Variáveis nav2
nav2_standb_int = tkinter.IntVar(value=121)  # Valor inicial da parte inteira standby
nav2_standb_dec = tkinter.IntVar(value=12)   # Valor inicial da parte decimal standby

nav2_active_int = tkinter.IntVar(value=800)  # Valor inicial da parte inteira ativa
nav2_active_dec = tkinter.IntVar(value=80)   # Valor inicial da parte decimal ativa

nav2_cached_int = tkinter.IntVar()
nav2_cached_dec = tkinter.IntVar()

nav2_active_txt = tkinter.StringVar(value=900.10)
nav2_standb_txt = tkinter.StringVar()
nav2_cached_txt = tkinter.StringVar()





################################################################ CLASSES 

# define classe do botão knobmenos
class knobmenos(tkinter.Button):
    def __init__(self, master=None, **kwargs):
        tkinter.Button.__init__(self, master, **kwargs)
        self.configure( text="<<", bg="gray", fg="white")

# define classe do botão knobmais
class knobmaiss(tkinter.Button):
    def __init__(self, master=None, **kwargs):
        tkinter.Button.__init__(self, master, **kwargs)
        self.configure( text=">>", bg="gray", fg="white")        

# define classe do labelframe principal
class mylabelframe(tkinter.LabelFrame):
    def __init__(self, master=None, **kwargs):
        tkinter.LabelFrame.__init__(self, master, **kwargs)
        self.configure( font=("verdana", 6))

# define classe do labelframe de radio
class radiolabelframe(tkinter.LabelFrame):
    def __init__(self, master=None, **kwargs):
        tkinter.LabelFrame.__init__(self, master, **kwargs)
        self.configure(bg="black", fg="white", font=("Verdana", 7), width=25)        

# define classe dos display de radio
class radiodisplay(tkinter.Label):
    def __init__(self, master=None, **kwargs):
        tkinter.Label.__init__(self, master, **kwargs)
        self.configure(font=("Digital-7", 20), fg="orange", bg="black")        

############################# classes dos RADIO

# define classe do botão swap
class botao_swap(tkinter.Button):
    def __init__(self, master=None, **kwargs):
        tkinter.Button.__init__(self, master, **kwargs)
        self.configure( text="<-->", bg="white", fg="black", font=("verdana", 6))

        
        
# NOVOS botoes seletora de frequencia 
class bot_freq_sel(tkinter.Button):
    def __init__(self, master=None, **kwargs):
        tkinter.Button.__init__(self, master, **kwargs)
        self.config(bg="black", fg="white", font=("verdana", 7))

class freq_sel():
    def __init__(self, master=None):
        # Criação dos botões no grupo
        self.botaoa = bot_freq_sel(master, text="-1")
        self.botaob = bot_freq_sel(master, text="+1")
        self.botaoc = bot_freq_sel(master, text="-5")
        self.botaod = bot_freq_sel(master, text="+5")
        
        # Posicionamento dos botões na grade
        self.botaoa.grid(row=0, column=0)
        self.botaob.grid(row=0, column=1)    
        self.botaoc.grid(row=0, column=2)
        self.botaod.grid(row=0, column=3)

class xpdr_sel(tkinter.Frame):  # Herde de tk.Frame
    def __init__(self, master=None):
        super().__init__(master)

        # Criação dos botões no grupo
        self.botaoa = bot_freq_sel(self, text="<")
        self.botaob = bot_freq_sel(self, text=">")

        # Posicionamento dos botões na grade
        self.botaoa.grid(row=0, column=0, sticky="ns")
        self.botaob.grid(row=0, column=1, sticky="ns")


class chave_pretoverde(tkinter.Button):
    def __init__(self, master=None, label="", *args, **kwargs):
        super().__init__(master, text=label, *args, **kwargs)
        self.config(bg="black", fg="red", font=("verdana", 8))
        self.botaois = 0

    def alternabotao(self):
        if self.botaois == 0:
            self.config(bg="black", fg="red", font=("verdana", 8))
        else:
            self.config(bg="#525754", fg="#0ceb47", font=("verdana", 8))        
        
class bot_simples_preto(tkinter.Button):
    def __init__(self, master=None, **kwargs):
        tkinter.Button.__init__(self, master, **kwargs)
        self.configure(bg="black", fg="white", font=("verdana", 8))

        
        
        
        
        

##################### classes da botoneira

# cria CLASSE de botoes vermelhos
class botaovermelho(tkinter.Button):
    def __init__(self, master=None,):
        
        tkinter.Button.__init__(self, master)
        self.botaoesta = 0
        self.configure(font=("verdana", 8))
        
        if self.botaoesta == 0:
            self.config(bg='red', fg='white')
        else:
            self.config(bg='lightcoral', fg='white')

    def alternabotaoesta(self):
        print("alternabotaoesta foi rodado")
        self.botaoesta = int(not self.botaoesta)
        print(self.botaoesta)

        if self.botaoesta == 0:
            self.config(bg='red', fg='white')
        else:
            self.config(bg='lightcoral', fg='white')
            
# cria CLASSE de botoes pretos
class botaopreto(tkinter.Button):
    def __init__(self, master=None,):
        tkinter.Button.__init__(self, master)
        self.botaoesta = 0
        self.configure(font=("verdana", 8))
        
        if self.botaoesta == 0:
            self.config(bg='black', fg='white')
        else:
            self.config(bg='#525754', fg='#0ceb47')

    def alternabotaoesta(self):
        print("alternabotaoesta foi rodado")
        self.botaoesta = int(not self.botaoesta)
        print(self.botaoesta)

        if self.botaoesta == 0:
            self.config(bg='black', fg='white')
        else:
            self.config(bg='#525754', fg='#0ceb47')



# cria CLASSE de botoes grandes
class botaogrand(tkinter.Button):
    def __init__(self, master=None,):
        tkinter.Button.__init__(self, master)
        self.botaoesta = 0
        self.config(font=("verdana", 8))
        
        
        if self.botaoesta == 0:
            self.config(bg='black', fg='red')
        else:
            self.config(bg='#525754', fg='#0ceb47')

    def alternabotaoesta(self):
        print("alternabotaoesta foi rodado")
        self.botaoesta = int(not self.botaoesta)
        print(self.botaoesta)

        if self.botaoesta == 0:
            self.config(bg='black', fg='red')
        else:
            self.config(bg='#525754', fg='#0ceb47')



# cria CLASSE de botoes brancos
class botaobranc(tkinter.Button):
    def __init__(self, master=None,):
        tkinter.Button.__init__(self, master)
        self.botaoesta = 0
        self.config(font=("verdana", 8))
        
        
        if self.botaoesta == 0:
            self.config(bg='white', fg='red')
        else:
            self.config(bg='#525754', fg='#0ceb47')

    def alternabotaoesta(self):
        print("alternabotaoesta foi rodado")
        self.botaoesta = int(not self.botaoesta)
        print(self.botaoesta)

        if self.botaoesta == 0:
            self.config(bg='white', fg='red')
        else:
            self.config(bg='#525754', fg='#0ceb47')

# cria CLASSE de botoes cinza
class botaocinza(tkinter.Button):
    def __init__(self, master=None,):
        tkinter.Button.__init__(self, master)
        
        self.config(font=("verdana", 8), bg="gray", fg="black")
        
        
  










########################################################## FUNÇÕES

#### funções de rede    

# configura função de enviar dados
if bypass_net == 0: 
    def send_data(data):
        print(f"Enviando dados: {data}")
        client_socket.send(data.encode('utf-8'))     

# configura função de receber dados
def receive_data():
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                handle_received_data(data)
        except ConnectionResetError:
            # Conexão resetada pelo servidor
            print("Conexão perdida com o servidor.")
            break

def handle_received_data(data):
    print(f"Dados recebidos do servidor: {data}")

    # Decodifica a string JSON para obter o dicionário
    data_dict = json.loads(data)

    # Acesse os valores do dicionário conforme necessário
    altitude = data_dict['altitude']
    ias = data_dict['ias']
    heading = data_dict['heading']
    fuel = data_dict['fuel']
    hora = data_dict['hora']
    windspeed = data_dict['windspeed']
    windmag = data_dict['windmag']
    oatc = data_dict['oatc']
    baro = data_dict['baro']

    # Atualiza as variáveis da interface gráfica
    texto_altitude.set(f"Altitude: {altitude} feet")
    texto_ias.set(f"ias: {ias} knots")
    texto_heading.set(f"Heading: {heading}°")
    texto_fuel.set(f"Fuel: {fuel} Gal")
    texto_hora.set(f"Hora local: {hora}")
    texto_windspeed.set(f"Windspeed: {windspeed} knots")
    texto_windmag.set(f"Wind direction: {windmag}")
    texto_oatc.set(f"OAT: {oatc}°C")
    texto_baro.set(f"Baro: {baro} qnh")

    #window.after(1000, handle_received_data)  # Chama a função novamente após x ms



# Create SimConnect link
if bypass_sim == 0:
    sm = SimConnect()
    ae = AircraftEvents(sm)
    aq = AircraftRequests(sm, _time=50)
    print("bypass sim: ", bypass_sim)
else:
    print("bypass sim: ", bypass_sim)
    

# Função para obter os dados do simulador, em variaveis
def obter_dados():
    altitude = int(aq.get("PLANE_ALTITUDE"))
    ias = int(aq.get("AIRSPEED_INDICATED"))
    heading = int(aq.get("MAGNETIC_COMPASS"))
    fuel = int(aq.get("FUEL_TOTAL_QUANTITY"))
    hora = int(aq.get("LOCAL_TIME"))
    windspeed = int(aq.get("AMBIENT_WIND_VELOCITY"))
    windmag = int(aq.get("AMBIENT_WIND_DIRECTION"))
    oatc = int(aq.get("AMBIENT_TEMPERATURE"))
    baro = int(aq.get("BAROMETER_PRESSURE"))

    return altitude, ias, heading, fuel, hora, windspeed, windmag, oatc, baro



# Função para atualizar os campos de texto
def atualizar_dados():
    if bypass_sim == 0:
        dados = obter_dados()
        texto_altitude.set(f"Altitude: {dados[0]} feet")
        texto_ias.set(f"ias: {dados[1]} knots")
        texto_heading.set(f"heading: {dados[2]}°")
        texto_fuel.set(f"fuel: {dados[3]} Gal")
        texto_hora.set(f"Hora local: {dados[4]}")
        texto_windspeed.set(f"Windspeed: {dados[5]} knots")
        texto_windmag.set(f"Wind direction: {dados[6]}")
        texto_oatc.set(f"OAT: {dados[7]}ºC")
        texto_baro.set(f"Baro: {dados[8]} qnh")
        window.after(1000, atualizar_dados)  # Chama a função novamente após x ms
    else:
        print("BypassSim:", bypass_sim)

































################## funções no developers frame
def alterna_acoplado():
    global acoplado
    acoplado = (not acoplado)
    print(f"App acoplado ao sim?: {acoplado}") 

# funcoes - define função botão tester alpha
def onclick_testeralpha():
    print("clicou tester alpha")
    send_data("TRIGGER_FUNC1")
    
# funcoes - define função botão tester beta
def onclick_testerbeta():
    global acoplado
    acoplado = (not acoplado)
    print(bypass_sim_tkbo.get()) 

# funcoes - define função botão tester charlie
def onclick_testercharlie():
    print("clicou tester charlie")
    acoplado.set(acoplado)
    
# funcoes - define função botão tester beta
def onclick_testerdelta():
    global acoplado
    acoplado = (not acoplado)
    print(bypass_sim_tkbo.get())     



############# funções knobs frame

  # Função para obter os dados dos knobs
def obter_knobs():
    ajustebussola = int(aq.get("PLANE_ALTITUDE"))

    return ajustebussola

# Função para atualizar os campos de texto
def atualizar_knobs():
    knobs = obter_knobs()
    #texto_ajustebussola.set(f"Altitude: {dados[0]} feet")
    #window.after(1000, atualizar_knobs)  # Chama a função novamente após x ms





################ funções de rádio
# Atualiza os campos de texto
def update_display():
    print("rodou update display")
    
    com1_active_txt.set(f"{com1_active_int.get():03d}.{com1_active_dec.get():03d}")
    com1_standb_txt.set(f"{com1_standb_int.get():03d}.{com1_standb_dec.get():03d}")
    
    nav1_active_txt.set(f"{nav1_active_int.get():03d}.{nav1_active_dec.get():02d}")
    nav1_standb_txt.set(f"{nav1_standb_int.get():03d}.{nav1_standb_dec.get():02d}")
    
    com2_active_txt.set(f"{com2_active_int.get():03d}.{com2_active_dec.get():03d}")
    com2_standb_txt.set(f"{com2_standb_int.get():03d}.{com2_standb_dec.get():03d}")

    nav2_active_txt.set(f"{nav2_active_int.get():03d}.{nav2_active_dec.get():02d}")
    nav2_standb_txt.set(f"{nav2_standb_int.get():03d}.{nav2_standb_dec.get():02d}")
    
    #com2_standb_txt.set(f"{com2_standb_int.get():03d}.{com2_standb_dec.get():03d}")
    #nav2_standb_txt.set(f"{nav2_standb_int.get():03d}.{nav2_standb_dec.get():02d}")

def clicou_intdec(botao):
    print("clicou intdec")
    botao.alternabotaoesta()
    
    
    
    
    
    
def clicoubotao_a_nogrupo_01():
    com1_standb_int.set((com1_standb_int.get() - 1) if com1_standb_int.get() != 118 else 136)
    update_display()
    if acoplado:
        send_data("COM_RADIO_WHOLE_DEC")
    
def clicoubotao_b_nogrupo_01():
    com1_standb_int.set((com1_standb_int.get() + 1) if com1_standb_int.get() != 136 else 118)
    update_display()
    if acoplado:
        send_data("COM_RADIO_WHOLE_INC")
        
def clicoubotao_c_nogrupo_01():
    numero_atual = com1_standb_dec.get() # decrementa o decimal da frequencia standby
    novo_numero = (numero_atual - 10) % 1000 if numero_atual % 100 in [25, 50, 75, 0] else (numero_atual - 5) % 1000
    com1_standb_dec.set(novo_numero)
    update_display()
    if acoplado:
        send_data("COM_RADIO_FRACT_DEC")
            
def clicoubotao_d_nogrupo_01():
    numero_atual = com1_standb_dec.get() # incrementa o decimal da frequencia standby
    novo_numero = (numero_atual + 10) % 1000 if numero_atual % 100 in [15, 40, 65, 90] else (numero_atual + 5) % 1000
    com1_standb_dec.set(novo_numero)
    update_display()
    if acoplado:
        send_data("COM_RADIO_FRACT_INC")







def clicoubotao_a_nogrupo_02():
    nav1_standb_int.set((nav1_standb_int.get() - 1) if nav1_standb_int.get() != 108 else 118)
    update_display()
    if acoplado:
        send_data("COM_RADIO_WHOLE_DEC")
    
def clicoubotao_b_nogrupo_02():
    nav1_standb_int.set((nav1_standb_int.get() + 1) if nav1_standb_int.get() != 118 else 108)
    update_display()
    if acoplado:
        send_data("COM_RADIO_WHOLE_INC")
        
def clicoubotao_c_nogrupo_02():
    numero_atual = nav1_standb_dec.get() # decrementa o decimal da frequencia standby
    novo_numero = (numero_atual - 10) % 1000 if numero_atual % 100 in [25, 50, 75, 0] else (numero_atual - 5) % 100
    nav1_standb_dec.set(novo_numero)
    update_display()
    if acoplado:
        send_data("COM_RADIO_FRACT_DEC")
            
def clicoubotao_d_nogrupo_02():
    numero_atual = nav1_standb_dec.get() # incrementa o decimal da frequencia standby
    novo_numero = (numero_atual + 10) % 1000 if numero_atual % 100 in [15, 40, 65, 90] else (numero_atual + 5) % 100
    nav1_standb_dec.set(novo_numero)
    update_display()
    if acoplado:
        send_data("COM_RADIO_FRACT_INC")










def clicoubotao_a_nogrupo_03():
    com2_standb_int.set((com2_standb_int.get() - 1) if com2_standb_int.get() != 118 else 136)
    update_display()
    if acoplado:
        send_data("COM_RADIO_WHOLE_DEC")
    
def clicoubotao_b_nogrupo_03():
    com2_standb_int.set((com2_standb_int.get() + 1) if com2_standb_int.get() != 136 else 118)
    update_display()
    if acoplado:
        send_data("COM_RADIO_WHOLE_INC")
        
def clicoubotao_c_nogrupo_03():
    numero_atual = com2_standb_dec.get() # decrementa o decimal da frequencia standby
    novo_numero = (numero_atual - 10) % 1000 if numero_atual % 100 in [25, 50, 75, 0] else (numero_atual - 5) % 1000
    com2_standb_dec.set(novo_numero)
    update_display()
    if acoplado:
        send_data("COM_RADIO_FRACT_DEC")
            
def clicoubotao_d_nogrupo_03():
    numero_atual = com2_standb_dec.get() # incrementa o decimal da frequencia standby
    novo_numero = (numero_atual + 10) % 1000 if numero_atual % 100 in [15, 40, 65, 90] else (numero_atual + 5) % 1000
    com2_standb_dec.set(novo_numero)
    update_display()
    if acoplado:
        send_data("COM_RADIO_FRACT_INC")


def clicoubotao_a_nogrupo_04():
    print("clicou botao a no grupo 04")
    
def clicoubotao_b_nogrupo_04():
    print("clicou botao b no grupo 04")    

def clicoubotao_c_nogrupo_04():
    print("clicou botao c no grupo 04")

def clicoubotao_d_nogrupo_04():
    print("clicou botao d no grupo 04")  





# funções do botão swap com 1    
def clicou_swap_com1():
    print("clicou swap com 1")
    
    # Cached pega as var do Active
    com1_cached_int.set(com1_active_int.get())
    com1_cached_dec.set(com1_active_dec.get())
    com1_cached_txt.set(com1_active_txt.get())

    # Active pega as var do StandBY
    com1_active_int.set(com1_standb_int.get())
    com1_active_dec.set(com1_standb_dec.get())
    com1_active_txt.set(com1_standb_txt.get())

    # Standby pega as var do Cached
    com1_standb_int.set(com1_cached_int.get())
    com1_standb_dec.set(com1_cached_dec.get())
    com1_standb_txt.set(com1_cached_txt.get())

    
    if acoplado:
        send_data("COM_STBY_RADIO_SWAP")    

# funções do botão swap nav 2 
def clicou_swap_nav1():
    print("clicou swap com 1")
    
    # Cached pega as var do Active
    nav1_cached_int.set(nav1_active_int.get())
    nav1_cached_dec.set(nav1_active_dec.get())
    nav1_cached_txt.set(nav1_active_txt.get())

    # Active pega as var do StandBY
    nav1_active_int.set(nav1_standb_int.get())
    nav1_active_dec.set(nav1_standb_dec.get())
    nav1_active_txt.set(nav1_standb_txt.get())

    # Standby pega as var do Cached
    nav1_standb_int.set(nav1_cached_int.get())
    nav1_standb_dec.set(nav1_cached_dec.get())
    nav1_standb_txt.set(nav1_cached_txt.get())

    
    if acoplado:
        send_data("COM_STBY_RADIO_SWAP")        



# funções do botão swap com  2 
def clicou_swap_com2():
    print("clicou swap com 2")
    
    # Cached pega as var do Active
    com2_cached_int.set(com2_active_int.get())
    com2_cached_dec.set(com2_active_dec.get())
    com2_cached_txt.set(com2_active_txt.get())

    # Active pega as var do StandBY
    com2_active_int.set(com2_standb_int.get())
    com2_active_dec.set(com2_standb_dec.get())
    com2_active_txt.set(com2_standb_txt.get())

    # Standby pega as var do Cached
    com2_standb_int.set(com2_cached_int.get())
    com2_standb_dec.set(com2_cached_dec.get())
    com2_standb_txt.set(com2_cached_txt.get())

    
    if acoplado:
        send_data("COM_STBY_RADIO_SWAP")                

# funções do botão swap nav  2 
def clicou_swap_nav2():
    print("clicou swap com 2")
    
    # Cached pega as var do Active
    nav2_cached_int.set(nav2_active_int.get())
    nav2_cached_dec.set(nav2_active_dec.get())
    nav2_cached_txt.set(nav2_active_txt.get())

    # Active pega as var do StandBY
    nav2_active_int.set(nav2_standb_int.get())
    nav2_active_dec.set(nav2_standb_dec.get())
    nav2_active_txt.set(nav2_standb_txt.get())

    # Standby pega as var do Cached
    nav2_standb_int.set(nav2_cached_int.get())
    nav2_standb_dec.set(nav2_cached_dec.get())
    nav2_standb_txt.set(nav2_cached_txt.get())

    
    if acoplado:
        send_data("COM_STBY_RADIO_SWAP")                


def fun_clicou_xpdr(botao):
    # Define botaois como 1 no botão clicado e como 0 nos demais botões
    for b in botoes_xpdr:
        b.botaois = 1 if b == botao else 0
        b.alternabotao()
        print(f"Botão {b.cget('text')} - Estado: {b.botaois}")

    # Condicional para executar funções específicas com base na opção do botão clicado
    if botao.cget('text') == 'tst':
        fun_clicou_tst()
    elif botao.cget('text') == 'alt':
        fun_clicou_alt()
    elif botao.cget('text') == 'onn':
        fun_clicou_onn()
    elif botao.cget('text') == 'sby':
        fun_clicou_sby()
    elif botao.cget('text') == 'off':
        fun_clicou_off()

# Funções específicas para cada opção do botão
def fun_clicou_tst():
    print("Função específica para o botão tst")

def fun_clicou_alt():
    print("Função específica para o botão alt")

def fun_clicou_onn():
    print("Função específica para o botão onn")

def fun_clicou_sby():
    print("Função específica para o botão sby")

def fun_clicou_off():
    print("Função específica para o botão off")



#################### funções na botoneira

# puxa do sim o estado do painel e atualiza
def puxaestadosdosim():
    if bypass_sim == 0:
        var_alt = (aq.get("LIGHT BEACON"))
        var_bat = (aq.get("ELECTRICAL_MASTER_BATTERY"))
        var_dom = (aq.get("LIGHT CABIN"))
        var_pit = (aq.get("PITOT HEAT"))
        var_nav = (aq.get("LIGHT NAV"))
        var_stb = (aq.get("LIGHT STROBE"))
        var_bcn = (aq.get("WISKEY_COMPASS_INDICATION_DEGREES"))
        var_tax = (aq.get("ELECTRICAL_TOTAL_LOAD_AMPS"))
        var_ldg = str(aq.get("ENGINE_CONTROL_SELECT"))
        
        window.after(1000, puxaestadosdosim)
    
# atualiza os botoes 
def atualizabotoes():
    print("atualiza botoes")

#funções individuais dos botoes
def click_pbk():
    bot_pbk.alternabotaoesta()
    if acoplado:
        send_data("PARKING_BRAKES")
        


def click_alt():
    bot_alt.alternabotaoesta()
    if acoplado:
        send_data("TOGGLE_MASTER_ALTERNATOR")
        
    

def click_bat():
    bot_bat.alternabotaoesta()
    if acoplado:    
        send_data("TOGGLE_MASTER_BATTERY")
          

def click_pan():
    print("clicou panel lights")
    bot_dom.alternabotaoesta()
    if acoplado:
        send_data("PANEL_LIGHTS_TOGGLE")
    
def click_pit():
    print("clicou pitot")
    bot_pit.alternabotaoesta()
    if acoplado:   
        send_data("PITOT_HEAT_TOGGLE")
    
def click_nav():
    print("clicou nav")
    bot_nav.alternabotaoesta()
    if acoplado:    
        send_data("TOGGLE_NAV_LIGHTS")
    
def click_stb():
    print("clicou stb")
    bot_stb.alternabotaoesta()
    if acoplado:
        send_data("STROBES_TOGGLE")
    
def click_bcn():
    print("clicou bcn")
    bot_bcn.alternabotaoesta()
    if acoplado:
        send_data("TOGGLE_BEACON_LIGHTS")
    
    
def click_tax():
    print("clicou tax")
    bot_tax.alternabotaoesta()
    if acoplado:
        send_data("TOGGLE_TAXI_LIGHTS")
   
    
def click_ldg():
    print("clicou landing")
    bot_ldg.alternabotaoesta()
    if acoplado:    
        send_data("LANDING_LIGHTS_TOGGLE")
        
def click_fuv():
    print("clicou fuvv")
    bot_fuv.alternabotaoesta()
    if acoplado:    
        send_data("TOGGLE_FUEL_VALVE_ALL")
 
def click_fup():
    print("clicou fuvv")
    bot_fup.alternabotaoesta()
    if acoplado:    
        send_data("TOGGLE_FUEL_VALVE_ALL")
      

def click_avm():
    print("clicou fuvv")
    bot_avm.alternabotaoesta()
    if acoplado:    
        send_data("TOGGLE_FUEL_VALVE_ALL")

def click_mde():
    print("clicou mag dec")
    if acoplado:    
        send_data("MAGNETO_DECR")

def click_min():
    print("clicou mde")
    if acoplado:    
        send_data("MAGNETO_INCR")


# converte a variavel do botaoesta py pra var tkin

def botaoestatkin():
    alt_botaoesta_tkin.set(bot_alt.botaoesta)
    bat_botaoesta_tkin.set(bot_bat.botaoesta)
    dom_botaoesta_tkin.set(bot_dom.botaoesta)
    pit_botaoesta_tkin.set(bot_pit.botaoesta)
    nav_botaoesta_tkin.set(bot_nav.botaoesta)
    stb_botaoesta_tkin.set(bot_stb.botaoesta)
    bcn_botaoesta_tkin.set(bot_bcn.botaoesta)
    tax_botaoesta_tkin.set(bot_tax.botaoesta)
    ldg_botaoesta_tkin.set(bot_ldg.botaoesta)







# FUNÇÕES NO CONSOLE

def clicou_send():
    if acoplado:
        send_data(console_entry.get())























































# main app frame
frame = tkinter.Frame(window, bg="gray")
frame.grid(row=0, column=0, padx=5, pady=5)

###################################### INFO - FRAME



################ info frame - interface

info_frame = mylabelframe(frame, text="Information Frame")
info_frame.grid(row=0, column=0, sticky="we")

# AC INFO - FRAME

ac_info_frame =mylabelframe(info_frame, text="Aircraft Info")
ac_info_frame.grid(row=0, column=0)

airspeed_label = tkinter.Label(ac_info_frame, text="Airspeed")
airspeed_label.grid(row=0, column=0)


# criar campo de texto atualizavel - ac info
label_altitude = tkinter.Label(ac_info_frame, textvariable=texto_altitude)
label_altitude.grid(row=0, column=0)


label_ias = tkinter.Label(ac_info_frame, textvariable=texto_ias)
label_ias.grid(row=1, column=0)


label_heading = tkinter.Label(ac_info_frame, textvariable=texto_heading)
label_heading.grid(row=2, column=0)


label_fuel = tkinter.Label(ac_info_frame, textvariable=texto_fuel)
label_fuel.grid(row=3, column=0)

# configura o campo de texto do ac info 
for widget in ac_info_frame.winfo_children():
    widget.configure(bg="#1A1A1A", fg="yellow", font=("Verdana", 7))
    widget.grid_configure(pady=0, sticky="w")


# WEA INFO - FRAME

wea_info_frame = mylabelframe(info_frame, text="Weather Information Info")
wea_info_frame.grid(row=0, column=1)

# criar campo de texto atualizavel - wea info
label_hora = tkinter.Label(wea_info_frame, textvariable=texto_hora)
label_hora.grid(row=0, column=0)


label_windspeed = tkinter.Label(wea_info_frame, textvariable=texto_windspeed)
label_windspeed.grid(row=1, column=0)


label_windmag = tkinter.Label(wea_info_frame, textvariable=texto_windmag)
label_windmag.grid(row=2, column=0)
########## corrigir o windmag, esta pegando wind true


label_oatc = tkinter.Label(wea_info_frame, textvariable=texto_oatc)
label_oatc.grid(row=3, column=0)


label_baro = tkinter.Label(wea_info_frame, textvariable=texto_baro)
label_baro.grid(row=4, column=0)

# configura o campo de texto do we info 
for widget in wea_info_frame.winfo_children():
    widget.configure(bg="#1A1A1A", fg="yellow", font=("Verdana", 7))
    widget.grid_configure(pady=0, sticky="w")





# FL INFO - FRAME

fl_info_frame = mylabelframe(info_frame, text="Flight Information")
fl_info_frame.grid(row=0, column=2)

elapsedtime_label = tkinter.Label(fl_info_frame, text="Elapsed Time")
elapsedtime_label.grid(row=0, column=0)

# pading 
for widget in info_frame.winfo_children():
    widget.grid_configure(padx=0, pady=0, sticky="news")




# VARiaveis INFO - FRAME
var_info_frame = mylabelframe(info_frame, text="Variaveis informations frame")
var_info_frame.grid(row=0, column=3,  sticky="news")



# criar campo de texto atualizavel - var info
com1_active_int_label = tkinter.Label(var_info_frame, textvariable=com1_active_txt)



# Por no grid as var infos
com1_active_int_label.grid(row=0, column=0)





# configura o campo de texto do var info 
for widget in var_info_frame.winfo_children():
    widget.configure(bg="#1A1A1A", fg="yellow", font=("Verdana", 7))
    widget.grid_configure(pady=0, sticky="w")











############################################### DEVeloper FRAME





################## interface developers frame
dev_frame = mylabelframe(frame, text="Developers frame")
dev_frame.grid(row=1, column=0, sticky="news")




# checkbox bypass
checkbox_bypass_sim = tkinter.Checkbutton(dev_frame, text="ByPass SimConection", variable=bypass_sim_tkbo, state="disabled")
checkbox_bypass_sim.grid(row=0, column=0, sticky="news")

# cria checkbutton acoplado
checkbutton_acoplado = tkinter.Checkbutton(dev_frame, variable=acoplado, text="App Acoplado ao SIM", command=alterna_acoplado)
checkbutton_acoplado.grid(row=0, column=1)

# botão testeralpha 
button_testeralpha = tkinter.Button(dev_frame, text="Tester Alpha", command=onclick_testeralpha)
button_testeralpha.grid(row=0, column=2, sticky="w")

# botão testerbeta
button_testerbeta = tkinter.Button(dev_frame, text="Tester Beta", command=onclick_testerbeta)
button_testerbeta.grid(row=0, column=3, sticky="w")

# botão testercharlie
button_testercharlie = tkinter.Button(dev_frame, text="Tester charlie", command=onclick_testercharlie)
button_testercharlie.grid(row=0, column=4, sticky="w")

# botão testerbeta
button_testerdelta = tkinter.Button(dev_frame, text="Tester delta", command=onclick_testerdelta)
button_testerdelta.grid(row=0, column=5, sticky="w")


#cria label
label_acoplado = tkinter.Label(dev_frame, text="decoy", fg="red")
label_acoplado.grid(row=0, column=6)


    



































###################################### CENTRAL - FRAME
central_frame = mylabelframe(frame, text="Central Frame")
central_frame.grid(row=2, column=0, sticky="ew")



###################################### KNOBS FRAME





knobs_frame = mylabelframe(central_frame, text="Knobs Frame")
knobs_frame.grid(row=0, column=0, sticky="ns")



aj_compass_label = tkinter.Label(knobs_frame, text="hdg")
aj_compass_label.grid(row=0, column=1)
aj_compass_spin = tkinter.Spinbox(knobs_frame, from_=1, to=360, width=10)
aj_compass_spin.grid(row=1, column=1)

sca_pan = tkinter.Scale(knobs_frame, orient="horizontal", bg="black", fg="white")
sca_pan.grid(row=2, column=1)
sca_rad = tkinter.Scale(knobs_frame, orient="horizontal", bg="black", fg="white")
sca_rad.grid(row=3, column=1)

knob_pan_menos = knobmenos(knobs_frame)
knob_pan_maiss = knobmaiss(knobs_frame)

knob_rad_menos = knobmenos(knobs_frame)
knob_rad_maiss = knobmaiss(knobs_frame)

knob_pan_menos.grid(row=2, column=0)
knob_pan_maiss.grid(row=2, column=3)

knob_rad_menos.grid(row=3, column=0)
knob_rad_maiss.grid(row=3, column=3)






# pading para os itens do knobs frame
for widget in knobs_frame.winfo_children():
    widget.grid_configure(padx=2, pady=5)







############################# RADIOS FRAME



   

# antiga posição das variaveis de rádio


##################### interface radio
# Big Radios Frame

radios_frame = radiolabelframe(central_frame, text="Radios Frame")
radios_frame.grid(row=0, column=1)

# Radio 1 

radio_01_frame = radiolabelframe(radios_frame, text="Radio 01")
radio_01_frame.grid(row=0, column=0)






# Frame - comm 1 - active
com1_active_frame = radiolabelframe(radio_01_frame, text="Comm 01 - Active")
com1_active_frame.grid(row=0, column=0)

actived_display = radiodisplay(com1_active_frame, textvariable=com1_active_txt)
actived_display.grid(row=0, column=0)

com1_swap_button = botao_swap(com1_active_frame)
com1_swap_button.grid(row=1, column=0)

# Frame - comm 1 - standby
com1_standb_frame = radiolabelframe(radio_01_frame, text="Comm 01 - StandBy")
com1_standb_frame.grid(row=0, column=1)

com1_standb_display = radiodisplay(com1_standb_frame, textvariable=com1_standb_txt)
com1_standb_display.grid(row=0, column=0)

com1_standb_buttons_frame = tkinter.Frame(com1_standb_frame, bg="black")
com1_standb_buttons_frame.grid(row=1, column=0)

# Criação da instância do grupo de botões
instancia_02_do_grupo = freq_sel(com1_standb_buttons_frame)
instancia_02_do_grupo.botaoa.config(command=clicoubotao_a_nogrupo_01)
instancia_02_do_grupo.botaob.config(command=clicoubotao_b_nogrupo_01)
instancia_02_do_grupo.botaoc.config(command=clicoubotao_c_nogrupo_01)
instancia_02_do_grupo.botaod.config(command=clicoubotao_d_nogrupo_01)









# Frame - nav1 - active
nav1_act_fr = radiolabelframe(radio_01_frame, text="Nav 01 - Active")
nav1_act_fr.grid(row=0, column=2)

nav1_act_disp = radiodisplay(nav1_act_fr, textvariable=nav1_active_txt)
nav1_act_disp.grid(row=0, column=0)

nav1_swap_button = botao_swap(nav1_act_fr)
nav1_swap_button.grid(row=1, column=0)

# Frame - nav1 - standby
nav1_standby_frame = radiolabelframe(radio_01_frame, text="Nav 01 - StandBy")
nav1_standby_frame.grid(row=0, column=3)

nav1_standby_display = radiodisplay(nav1_standby_frame, textvariable=nav1_standb_txt)
nav1_standby_display.grid(row=0, column=0)

nav1_standby_buttons_frame = tkinter.Frame(nav1_standby_frame, bg="black")
nav1_standby_buttons_frame.grid(row=1, column=0)








# Criação da instância do grupo de botões
instancia_02_do_grupo = freq_sel(nav1_standby_buttons_frame)
instancia_02_do_grupo.botaoa.config(command=clicoubotao_a_nogrupo_02)
instancia_02_do_grupo.botaob.config(command=clicoubotao_b_nogrupo_02)
instancia_02_do_grupo.botaoc.config(command=clicoubotao_c_nogrupo_02)
instancia_02_do_grupo.botaod.config(command=clicoubotao_d_nogrupo_02)





# Radio 2

radio_02_frame = radiolabelframe(radios_frame, text="Radio 02")
radio_02_frame.grid(row=1, column=0)

# Frame - comm 2 - active
com2_active_frame = radiolabelframe(radio_02_frame, text="Comm 02 - Active")
com2_active_frame.grid(row=0, column=0)

actived_display = radiodisplay(com2_active_frame, textvariable=com2_active_txt)
actived_display.grid(row=0, column=0)

com2_swap_button = botao_swap(com2_active_frame)
com2_swap_button.grid(row=1, column=0)

# Frame - comm 2 - standby
com2_standby_frame = radiolabelframe(radio_02_frame, text="Comm 02 - StandBy")
com2_standby_frame.grid(row=0, column=1)

com2_standby_display = radiodisplay(com2_standby_frame, textvariable=com2_standb_txt)
com2_standby_display.grid(row=0, column=0)

com2_standby_buttons_frame = tkinter.Frame(com2_standby_frame, bg="black")
com2_standby_buttons_frame.grid(row=1, column=0)

# Criação da instância dos botoes de seletora frequencia
instancia_03_do_grupo = freq_sel(com2_standby_buttons_frame)
instancia_03_do_grupo.botaoa.config(command=clicoubotao_a_nogrupo_03)
instancia_03_do_grupo.botaob.config(command=clicoubotao_b_nogrupo_03)
instancia_03_do_grupo.botaoc.config(command=clicoubotao_c_nogrupo_03)
instancia_03_do_grupo.botaod.config(command=clicoubotao_d_nogrupo_03)



# Frame - nav2 - active
nav2_act_fr = radiolabelframe(radio_02_frame, text="Nav 02 - Active")
nav2_act_fr.grid(row=0, column=2)

nav2_act_disp = radiodisplay(nav2_act_fr, textvariable=nav2_active_txt)
nav2_act_disp.grid(row=0, column=0)

nav2_swap_button = botao_swap(nav2_act_fr)
nav2_swap_button.grid(row=1, column=0)

# Frame - nav2 - standby
nav2_standby_frame = radiolabelframe(radio_02_frame, text="Nav 02 - StandBy")
nav2_standby_frame.grid(row=0, column=3)

nav2_standby_display = radiodisplay(nav2_standby_frame, textvariable=nav2_standb_txt)
nav2_standby_display.grid(row=0, column=0)

nav2_standby_buttons_frame = tkinter.Frame(nav2_standby_frame, bg="black")
nav2_standby_buttons_frame.grid(row=1, column=0)

# Criação da instância do grupo de botões
instancia_04_do_grupo = freq_sel(nav2_standby_buttons_frame)
instancia_04_do_grupo.botaoa.config(command=clicoubotao_a_nogrupo_04)
instancia_04_do_grupo.botaob.config(command=clicoubotao_b_nogrupo_04)
instancia_04_do_grupo.botaoc.config(command=clicoubotao_c_nogrupo_04)
instancia_04_do_grupo.botaod.config(command=clicoubotao_d_nogrupo_04)


# Configura os botões swap
com1_swap_button.config(command=clicou_swap_com1)
nav1_swap_button.config(command=clicou_swap_nav1)
com2_swap_button.config(command=clicou_swap_com2)
nav2_swap_button.config(command=clicou_swap_nav2)





# pading dos itens do radios frame (radio 01, radio 02, eventualmente xpdr e ap)
for widget in radios_frame.winfo_children():
    widget.grid_configure(padx=5, pady=5, sticky="news")




radio_03_frame = radiolabelframe(radios_frame, text="Transponder")
radio_03_frame.grid(row=3, column=0, sticky="news")

radio_03_subframe_0 = radiolabelframe(radio_03_frame, text="seletor")
radio_03_subframe_1 = radiolabelframe(radio_03_frame, text="ident")
radio_03_subframe_2 = radiolabelframe(radio_03_frame, text="digit 1")
radio_03_subframe_3 = radiolabelframe(radio_03_frame, text="digit 2")
radio_03_subframe_4 = radiolabelframe(radio_03_frame, text="digit 3")
radio_03_subframe_5 = radiolabelframe(radio_03_frame, text="digit 4")

radio_03_subframe_0.grid(row=0, column=0, sticky="ns")
radio_03_subframe_1.grid(row=0, column=1, sticky="ns")
radio_03_subframe_2.grid(row=0, column=2, sticky="ns")
radio_03_subframe_3.grid(row=0, column=3, sticky="ns")
radio_03_subframe_4.grid(row=0, column=4, sticky="ns")
radio_03_subframe_5.grid(row=0, column=5, sticky="ns")

xpdr_tst = chave_pretoverde(radio_03_subframe_0, label="tst", command=lambda: fun_clicou_xpdr(xpdr_tst))
xpdr_alt = chave_pretoverde(radio_03_subframe_0, label="alt", command=lambda: fun_clicou_xpdr(xpdr_alt))
xpdr_onn = chave_pretoverde(radio_03_subframe_0, label="onn", command=lambda: fun_clicou_xpdr(xpdr_onn))
xpdr_sby = chave_pretoverde(radio_03_subframe_0, label="sby", command=lambda: fun_clicou_xpdr(xpdr_sby))
xpdr_off = chave_pretoverde(radio_03_subframe_0, label="off", command=lambda: fun_clicou_xpdr(xpdr_off))

botoes_xpdr = [xpdr_tst, xpdr_alt, xpdr_onn, xpdr_sby, xpdr_off]

xpdr_tst.grid(row=0, column=0)
xpdr_alt.grid(row=0, column=1)
xpdr_onn.grid(row=1, column=0)
xpdr_sby.grid(row=1, column=1)
xpdr_off.grid(row=0, column=2)

bot_ident = bot_simples_preto(radio_03_subframe_1, text="Ident")
bot_ident.grid(row=0, column=0)

xpdr_digit_1 = radiodisplay(radio_03_subframe_2, text="1")
xpdr_digit_2 = radiodisplay(radio_03_subframe_3, text="2")
xpdr_digit_3 = radiodisplay(radio_03_subframe_4, text="3")
xpdr_digit_4 = radiodisplay(radio_03_subframe_5, text="4")
xpdr_digit_1.grid(row=0, column=0)
xpdr_digit_2.grid(row=0, column=0)
xpdr_digit_3.grid(row=0, column=0)
xpdr_digit_4.grid(row=0, column=0)

digit_1_sel = xpdr_sel(radio_03_subframe_2)
digit_2_sel = xpdr_sel(radio_03_subframe_3)
digit_3_sel = xpdr_sel(radio_03_subframe_4)
digit_4_sel = xpdr_sel(radio_03_subframe_5)
digit_1_sel.grid(row=1, column=0)
digit_2_sel.grid(row=1, column=0)
digit_3_sel.grid(row=1, column=0)
digit_4_sel.grid(row=1, column=0)

###################################### CALC FRAME

# variaveis

velocidade_var = tkinter.IntVar(value=90)   # Valor inicial da velocidade
distance_var = tkinter.IntVar(value=25)   # Valor inicial da distancia
temporota_var = tkinter.IntVar(value=10)   # Valor inicial do tempo em rota do trecho

# funcoes - define função botão calculate
def onclick_button_calculate():
    distance = float(distance_entry.get())
    velocidade = float(velocidade_entry.get())
    temporota = distance * 60 / velocidade
    temporota_entry.delete(0, tkinter.END)  # Limpa o campo de entrada
    temporota_entry.insert(0, "{:.2f}".format(temporota))

  


# interface

calc_frame = mylabelframe(central_frame, text="Calculator Frame")
calc_frame.grid(row=0, column=2, sticky="NEWS")

velocidade_label = tkinter.Label(calc_frame, text="Ias: ")
velocidade_label.grid(row=0, column=0)
velocidade_entry = tkinter.Entry(calc_frame, textvariable=velocidade_var, width=10)
velocidade_entry.grid(row=0, column=1)

distance_label = tkinter.Label(calc_frame, text="NM: ")
distance_label.grid(row=1, column=0)
distance_entry = tkinter.Entry(calc_frame, textvariable=distance_var, width=10)
distance_entry.grid(row=1, column=1)

temporota_label = tkinter.Label(calc_frame, text="ETA: ")
temporota_label.grid(row=2, column=0)
temporota_entry = tkinter.Entry(calc_frame, width=10)
temporota_entry.grid(row=2, column=1)


button_calculate = tkinter.Button(calc_frame, text="Calc", command=onclick_button_calculate)
button_calculate.grid(row=3, column=0, sticky="news")







# pading para os itens do calc frame
for widget in calc_frame.winfo_children():
    widget.grid_configure(padx=2, pady=5, sticky="news")



# pading dos itens do central frame (knob, radios e calc)
for widget in central_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10, sticky="news")













###################################### BOTONEIRA

################ interface botoneira

botoneira_frame = mylabelframe(frame, text="Botoneira", bg="#3d200a", fg="white")
botoneira_frame.grid(row=3, column=0, sticky="ew")

# criar instancias dos botões
bot_pbk = botaogrand(botoneira_frame)

bot_alt = botaovermelho(botoneira_frame)
bot_bat = botaovermelho(botoneira_frame)
bot_dom = botaopreto(botoneira_frame)
bot_pit = botaopreto(botoneira_frame)
bot_nav = botaopreto(botoneira_frame)
bot_stb = botaopreto(botoneira_frame)
bot_bcn = botaopreto(botoneira_frame)
bot_tax = botaopreto(botoneira_frame)
bot_ldg = botaopreto(botoneira_frame)
bot_fup = botaopreto(botoneira_frame)
bot_fuv = botaogrand(botoneira_frame)
bot_avm = botaobranc(botoneira_frame)
bot_mde = botaocinza(botoneira_frame)
bot_min = botaocinza(botoneira_frame)

# configura os botões

bot_pbk.config(command=click_pbk, text="Park B.")
bot_alt.config(command=click_alt, text="ALT")
bot_bat.config(command=click_bat, text="BAT")
bot_dom.config(command=click_pan, text="PAN")
bot_pit.config(command=click_pit, text="PTH")
bot_nav.config(command=click_nav, text="NAV")
bot_stb.config(command=click_stb, text="STB")
bot_bcn.config(command=click_bcn, text="BCN")
bot_tax.config(command=click_tax, text="TAX")
bot_ldg.config(command=click_ldg, text="LDG")
bot_fup.config(command=click_fup, text="FPP")
bot_fuv.config(command=click_fuv, text="Fuel Valve")
bot_avm.config(command=click_avm, text="AVIONICS")
bot_mde.config(command=click_mde, text="< Mag")
bot_min.config(command=click_min, text="Mag >")

# empacota o botão
if aircraft == 152:
    bot_pbk.grid(row=2, column=0)
    bot_fuv.grid(row=2, column=14)
    bot_alt.grid(row=2, column=2)
    bot_bat.grid(row=2, column=3)
    bot_mde.grid(row=2, column=4)
    bot_min.grid(row=2, column=5)
    bot_dom.grid(row=2, column=7)
    bot_pit.grid(row=2, column=8)
    bot_nav.grid(row=2, column=9)
    bot_stb.grid(row=2, column=10)
    bot_bcn.grid(row=2, column=11)
    bot_tax.grid(row=2, column=12)
    bot_ldg.grid(row=2, column=13)
    
elif aircraft == 172:
    bot_pbk.grid(row=2, column=0)
    bot_fuv.grid(row=2, column=1)
    bot_alt.grid(row=2, column=2)
    bot_bat.grid(row=2, column=3)
    bot_dom.grid(row=2, column=7)
    bot_pit.grid(row=2, column=8)
    bot_nav.grid(row=2, column=9)
    bot_stb.grid(row=2, column=10)
    bot_bcn.grid(row=2, column=11)
    bot_tax.grid(row=2, column=12)
    bot_ldg.grid(row=2, column=13)
    bot_fup.grid(row=2, column=14)



    
else:
    print("no ac")

""" 
#### Cria label do estado dos botoes 
label_alt = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", textvariable=alt_tkin, font=("verdana", 6))
label_bat = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", textvariable=bat_tkin, font=("verdana", 6))
label_dom = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", textvariable=dom_tkin, font=("verdana", 6))
label_pit = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", textvariable=pit_tkin, font=("verdana", 6))
label_nav = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", textvariable=nav_tkin, font=("verdana", 6))
label_stb = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", textvariable=stb_tkin, font=("verdana", 6))
label_bcn = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", textvariable=bcn_tkin, font=("verdana", 6))
label_tax = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", textvariable=tax_tkin, font=("verdana", 6))
label_ldg = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", textvariable=ldg_tkin, font=("verdana", 6))

#empacota as labels
label_alt.grid(row=3, column=0)
label_bat.grid(row=3, column=1)
label_dom.grid(row=3, column=2)
label_pit.grid(row=3, column=3)
label_nav.grid(row=3, column=4)
label_stb.grid(row=3, column=5)
label_bcn.grid(row=3, column=6)
label_tax.grid(row=3, column=7)
label_ldg.grid(row=3, column=8)

#### Cria label do estado dos botoes 
label_alt_is = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", text="b.is", font=("verdana", 6))
label_bat_is = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", text="b.is", font=("verdana", 6))
label_dom_is = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", text="b.is", font=("verdana", 6))
label_pit_is = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", text="b.is", font=("verdana", 6))
label_nav_is = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", text="b.is", font=("verdana", 6))
label_stb_is = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", text="b.is", font=("verdana", 6))
label_bcn_is = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", text="b.is", font=("verdana", 6))
label_tax_is = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", text="b.is", font=("verdana", 6))
label_ldg_is = tkinter.Label(botoneira_frame, bg="#3d200a", fg="white", text="b.is", font=("verdana", 6))

#empacota as labels
label_alt_is.grid(row=4, column=0)
label_bat_is.grid(row=4, column=1)
label_dom_is.grid(row=4, column=2)
label_pit_is.grid(row=4, column=3)
label_nav_is.grid(row=4, column=4)
label_stb_is.grid(row=4, column=5)
label_bcn_is.grid(row=4, column=6)
label_tax_is.grid(row=4, column=7)
label_ldg_is.grid(row=4, column=8)

 """



######################################### CONSOLE


console_frame = mylabelframe(frame, text="Console")
console_frame.grid(row=4, column= 0, sticky="news")
console_frame.columnconfigure(1, weight=1)

console_entry = tkinter.Entry(console_frame, bg="black", fg="#53f73e", text=">>>>>>")
console_entry.grid(row=3, column=0, sticky="news", columnspan=2)
console_entry.insert(1, ">> Settings Console >>")

console_button = tkinter.Button(console_frame, text="SEND", command=clicou_send)
console_button.grid(row=3, column=2)












# pading para o info, central e botoneira frames


for widget in frame.winfo_children():
    widget.grid_configure(padx=5, pady=5)





























############################################################## INICIA A APLICAÇÃO

# Inicia uma thread para receber dados do servidor em segundo plano
if bypass_net == 0:
    threading.Thread(target=receive_data, daemon=True).start()

update_display()
puxaestadosdosim()
atualizar_dados()

window.mainloop()