# This version is: E
# add retry caso a conexão caia, caso erro de OS, e caso simconnect falhe. 

# Configurações básicas
bypass_sim = 0 # Caso SIM, rodar o app sem a necessidade do Simulador rodando

import tkinter
import socket
import threading
import time
import json
try:
    from SimConnect import *
    print("importou SimConnect")
except ModuleNotFoundError:
    print("O módulo SimConnect não foi encontrado. Certifique-se de que está instalado.")

# Create SimConnect link
if bypass_sim == 0:
    sm = SimConnect()
    ae = AircraftEvents(sm)
    aq = AircraftRequests(sm, _time=50)
    print("bypass sim: ", bypass_sim)
else:
    print("bypass sim: ", bypass_sim)


# cria janela principal
window = tkinter.Tk()
window.title("Server")



# Configuração do socket do servidor e escuta de cliente
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.0.75', 12345))
server_socket.listen(2)
print("Aguardando conexão do cliente...")






    
    
    
    

# Função para receber dados do cliente
def receive_data(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                # Se não houver dados, a conexão foi perdida, então quebre o loop
                break
            print(data)
            handle_command(data)
        except ConnectionResetError:
            # Se ocorrer um erro de reinicialização de conexão, o cliente se desconectou
            break
        except Exception as e:
            print(f"Erro durante a recepção de dados: {e}")

    # Se a execução chegar aqui, a conexão foi perdida
    print("Conexão com o cliente perdida.")


# Função para lidar com os comandos recebidos
def handle_command(command):
    event_to_trigger = ae.find(command)
    event_to_trigger()  
    
    
 # Função para enviar dados ao cliente
def send_data_to_client(client_socket):
    while True:
        # Obtém os dados do simulador
        dados = obter_dados()

        # Cria um dicionário com os dados
        data_dict = {
            'altitude': dados[0],
            'ias': dados[1],
            'heading': dados[2],
            'fuel': dados[3],
            'hora': dados[4],
            'windspeed': dados[5],
            'windmag': dados[6],
            'oatc': dados[7],
            'baro': dados[8],
            'com1si': dados[9],
            'com1sd': dados[10],
            'com1ai': dados[11],
            'com1ad': dados[12],
            'nav1si': dados[13],
            'nav1sd': dados[14],
            'nav1ai': dados[15],
            'nav1ad': dados[16],
            'com2si': dados[17],
            'com2sd': dados[18],
            'com2ai': dados[19],
            'com2ad': dados[20],
            'nav2si': dados[21],
            'nav2sd': dados[22],
            'nav2ai': dados[23],
            'nav2ad': dados[24],
            
        }

        # Converte o dicionário para uma string JSON
        data_to_send = json.dumps(data_dict)

        # Exibe os dados no console para verificação
        print(f"Dados a serem enviados: {data_to_send}")

        # Envia os dados codificados para o cliente
        client_socket.send(data_to_send.encode('utf-8'))

        # Aguarda por algum tempo antes de enviar os próximos dados
        # ps o mx linux não aguenta muito rápido
        time.sleep(2)

# Função para aceitar conexões e iniciar uma thread para cada cliente
def accept_connections():
    while True:
        global client_socket  # Adicione esta linha
        client_socket, client_address = server_socket.accept()
        print(f"Conectado ao cliente address: {client_address}")
        print(f"Conectado ao cliente socket: {client_socket}")

        # Inicia uma thread para receber dados do cliente em segundo plano
        threading.Thread(target=receive_data, args=(client_socket,)).start()
        
        # Inicia a thread para enviar dados ao cliente em segundo plano
        threading.Thread(target=send_data_to_client, args=(client_socket,)).start()




   
   





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
    
    com1s = aq.get("COM_STANDBY_FREQUENCY:1")
    com1si, com1sd = (int(com1s), int(round(com1s % 1, 3) * 1000)) if com1s is not None else (None, None)

    com1a = aq.get("COM_ACTIVE_FREQUENCY:1")
    com1ai, com1ad = (int(com1a), int(round(com1a % 1, 3) * 1000)) if com1a is not None else (None, None)

    nav1s = aq.get("NAV_STANDBY_FREQUENCY:1")
    nav1si, nav1sd = (int(nav1s), int(round(nav1s % 1, 3) * 100)) if nav1s is not None else (None, None)

    nav1a = aq.get("NAV_ACTIVE_FREQUENCY:1")
    nav1ai, nav1ad = (int(nav1a), int(round(nav1a % 1, 3) * 100)) if nav1a is not None else (None, None)

    com2s = aq.get("COM_STANDBY_FREQUENCY:2")
    com2si, com2sd = (int(com2s), int(round(com2s % 1, 3) * 1000)) if com2s is not None else (None, None)

    com2a = aq.get("COM_ACTIVE_FREQUENCY:2")
    com2ai, com2ad = (int(com2a), int(round(com2a % 1, 3) * 1000)) if com2a is not None else (None, None)

    nav2s = aq.get("NAV_STANDBY_FREQUENCY:2")
    nav2si, nav2sd = (int(nav2s), int(round(nav2s % 1, 3) * 100)) if nav2s is not None else (None, None)

    nav2a = aq.get("NAV_ACTIVE_FREQUENCY:2")
    nav2ai, nav2ad = (int(nav2a), int(round(nav2a % 1, 3) * 100)) if nav2a is not None else (None, None)

    return altitude, ias, heading, fuel, hora, windspeed, windmag, oatc, baro, com1si, com1sd, com1ai, com1ad, nav1si, nav1sd, nav1ai, nav1ad, com2si, com2sd, com2ai, com2ad, nav2si, nav2sd, nav2ai, nav2ad


# Função para atualizar os campos de texto (interface do server)
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
        window.after(500, atualizar_dados)  # Chama a função novamente após x ms
    else:
        print("BypassSim:", bypass_sim)        
        


frame = tkinter.LabelFrame(window, text="Server")
frame.grid(row=0, column=0)






# define classe do labelframe principal
class mylabelframe(tkinter.LabelFrame):
    def __init__(self, master=None, **kwargs):
        tkinter.LabelFrame.__init__(self, master, **kwargs)
        self.configure( font=("verdana", 6))    
    
    















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
com1_active_int_label = tkinter.Label(var_info_frame)



# Por no grid as var infos
com1_active_int_label.grid(row=0, column=0)





# configura o campo de texto do var info 
for widget in var_info_frame.winfo_children():
    widget.configure(bg="#1A1A1A", fg="yellow", font=("Verdana", 7))
    widget.grid_configure(pady=0, sticky="w")






# Inicia uma thread para aceitar conexões e lidar com os clientes em segundo plano
threading.Thread(target=accept_connections).start()




#send_data_to_client()
atualizar_dados()
window.mainloop()
