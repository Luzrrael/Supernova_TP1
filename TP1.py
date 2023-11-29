from tkinter import *
from tkinter import messagebox
import os, os.path

def crearRelacion():
    #Autor: José Daniel Arturo Segura Valer

    caracter_a_pos = {}
    pos_a_caracter = {}
    
    minusculas = "abcdefghijklmnñopqrstuvwxyz"
    mayusculas = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    digitos    = "0123456789"
    
    caracteres = minusculas + mayusculas + digitos
    
    i = 0
    while(i < len(caracteres)):
        caracter_a_pos[caracteres[i]] = i
        pos_a_caracter[i] = caracteres[i]
        i += 1
        
    return (caracter_a_pos, pos_a_caracter)
    
# Diccionarios de caracter a posición y viceversa. Se crea una sola
# vez para evitar construirlos reiteradas veces en cada llamada a las
# funciones de cifrado.

relacion = crearRelacion()
caracter_a_pos = relacion[0]
pos_a_caracter = relacion[1]
del relacion

#***************************************************************

def desplazar(caracter, clave):

    # Desplaza un solo caracter hacia la derecha 'clave' veces, usando
    # la tabla de caracteres y posiciones definida por los diccionarios
    # caracter_a_pos y pos_a_caracter

    cantidad = 0
    offset   = 0
    alnum = True
    
    if(caracter.isalpha() and caracter in caracter_a_pos):
        if(caracter.islower()):
            cantidad = 27
            offset   = 0
        else:
            cantidad = 27
            offset   = 27
    elif(caracter.isdigit()):
        cantidad = 10
        offset   = 54
    else:
        alnum = False
        
    if(alnum):
        valor = ((caracter_a_pos[caracter] - offset) + clave) % cantidad
        caracter = pos_a_caracter[valor + offset]
        
    return caracter
    
    
def cifrar_c(cadena, clave):

    #Autor: Federico Aguilar

    """
    
    >>> cifrar_c("A", 4)
    'E'
    
    Se desplaza último caracter del abecedario:
    >>> cifrar_c("Z", 3)
    'C'
    
    Los caracteres que no son alfanuméricos no se desplazan (tampoco letras acentuadas ni extrañas):
    >>> cifrar_c("$#---/ABCÁÍÍÍÚ", 5)
    '$#---/FGHÁÍÍÍÚ'
    
    >>> cifrar_c("PERRO", 1)
    'QFSSP'
    
    >>> cifrar_c("     ", 10)
    '     '
    
    """

    codigo = ""
    
    for c in cadena:
        codigo += desplazar(c, clave)
        
    return codigo
    
    
def descifrar_c(codigo, clave):

    #Autor: Federico Aguilar

    """
    
    >>> descifrar_c("PERRO", 1) == descifrar_c("PERRO", 1 + 27)
    True
    
    >>> descifrar_c("HOLA MUNDO%%%&%/...;", 7) == descifrar_c("HOLA MUNDO%%%&%/...;", 7 + 27 * 8000)
    True
    
    >>> descifrar_c("7111-4399", 1)
    '6000-3288'
    
    >>> descifrar_c("0000-0000-dbop", 1)
    '9999-9999-caño'
    
    >>> descifrar_c("Illuminatis", 0) == "Illuminatis"
    True
    
    """

    return cifrar_c(codigo, -clave)
    
#***************************************************************
    
def asignar(caracter):

    # Asigna a cada caracter su opuesto correspondiente, haciéndolo
    # mayúscula si es minúscula y viceversa

    offset    = 0
    dist_ini  = 0
    pos_fin   = 0
    alnum = True
    
    if(caracter.isalpha() and caracter in caracter_a_pos):
        if(caracter.islower()):
            caracter = caracter.upper()
            offset   = 27
            pos_fin  = 26
        else:
            caracter = caracter.lower()
            offset   = 0
            pos_fin  = 26
    elif(caracter.isdigit()):
            offset = 54
            pos_fin = 9
    else:
        alnum = False
        
    if(alnum):
    
        dist_ini = caracter_a_pos[caracter] - offset
        caracter = pos_a_caracter[pos_fin - dist_ini + offset] 
            
    return caracter
    
def cifrar_atbash(cadena):

    #Autor: Bryan Hernán Serrantes Ochoa

    """
    
    >>> cifrar_atbash("A")
    'z'
    
    >>> cifrar_atbash ("z")
    'A'
    
    >>> cifrar_atbash(cifrar_atbash("QUEDA IGUAL"))
    'QUEDA IGUAL'
    
    >>> cifrar_atbash("0000-0000 %&10?")
    '9999-9999 %&89?'
    
    >>> cifrar_atbash(cifrar_atbash("PERRO")) == descifrar_atbash(cifrar_atbash("PERRO")) 
    True
    
    """

    codigo = ""
    
    for c in cadena:
        codigo += asignar(c)
        
    return codigo
    
# Para descifrar un código atbash basta aplicar de nuevo
# el algoritmo de cifrado.    
    
def descifrar_atbash(cadena):

    #Autor: Bryan Hernán Serrantes Ochoa

    """
        
    >>> descifrar_atbash("$$$$$===?")
    '$$$$$===?'
    
    >>> descifrar_atbash("ZYXWVUTSRQPOÑNMLKJIHGFEDCBA")
    'abcdefghijklmnñopqrstuvwxyz'
    
    >>> descifrar_atbash("9")
    '0'
    
    >>> descifrar_atbash("AÉÍÓü")
    'zÉÍÓü'
    
    >>> descifrar_atbash("abcdefghijklmnñopqrstuvwxyz")
    'ZYXWVUTSRQPOÑNMLKJIHGFEDCBA'
        
    """
    
    return cifrar_atbash(cadena)

#*******************************************************************************************************************************
#*******************************************************************************************************************************
#********************************SEGUNDA PARTE DEL TRABAJO PRACTICO*************************************************************
#*******************************************************************************************************************************
#*******************************************************************************************************************************

#*************************************************************************************
#********************************CONSTANTES*******************************************
#*************************************************************************************

#constantes para archivo usuarios.csv
POSICION_USUARIO = 0
POSICION_CLAVE = 1
ID_PREGUNTA_DATOS = 2
ID_RESPUESTA = 3
POSICION_INTENTOS = 4
#constantes para preguntas.csv
ID_PREGUNTA_PREGUNTAS = 0
POSICION_PREGUNTA_PREGUNTAS = 1
#constante de final de archivo
LINEA_FIN = ",,,,"
#mensaje de condiciones al ingresar usuario o clave invalido
REQUISITOS_USUARIO_CLAVE = "USUARIO: De 5 a 15 caracteres, simbolos validos “_” “-” “.”.\n\
CLAVE: De 4 a 8 caracteres, una mayusucula, una minuscula, un numero y alguno de estos simbolos “_”,“-”,“#”,“*”.\n\
No puede haber caracteres repetidos\nSe debe agregar una pregunta de recuperación"


#*************************************************************************************
#********************************FUNCIONES DE MAYOR USO*******************************
#*************************************************************************************
def leer_archivo(archivo):
    """
    Retorna una linea del archivo recibido en formatos lista,
    si el archivo esta vacio o se llega al final enviara una lista
    de 5 elementos para evitar en index of range
    """
    linea = archivo.readline()
    linea = linea.rstrip()
    if linea == "":
        linea = LINEA_FIN
    return linea.split(",")

def verificar_existencia_de_archivo(archivo):
    if os.path.exists(archivo):
        modo = "r+"
    else:
        modo = "w"
    return modo

def crearLabelTemporal(raiz, texto, xp, yp, tiempo):
    temp_label = Label(raiz, text = texto)
    temp_label.config(font = "Arial 9 bold",bg="#1C2833", fg="white")
    temp_label.place(x = xp, y = yp)
    temp_label.after(tiempo, lambda: temp_label.destroy())   

#*******************************************************************************************
#**********************************VENTANA PRINCIPAL****************************************
#*******************************************************************************************

def crearVentanaPrincipal():

    ventana_principal = Tk()
    ventana_principal.resizable(False,False)
    ventana_principal.geometry("400x260")
    ventana_principal.title("TP Grupal Parte 1 - Grupo: Supernova")
    ventana_principal.config(cursor="hand2",bg="#1C2833")
    ventana_principal.iconbitmap("supernova.ico")
    
    #****************************TEXTO ENTRADA************************************

    texto_bienvenida = "Bienvenido a la aplicación de mensajes secretos del grupo Supernova:"
    bienvenida = Label(ventana_principal, text = texto_bienvenida, wraplength = 350)
    bienvenida.config(font = "Arial 11 bold", bg = "#1C2833", fg = "white")
    bienvenida.place(x = 25, y = 30)


    #****************************BOTONES*********************************************
    

    btn_crear_usuario = Button(ventana_principal, text="Registrarse", command=crear_ventana_registrarse)
    btn_crear_usuario.config(width=12 , height=1,font="Arial 10 bold", relief="raised", bd=4)
    btn_crear_usuario.place(x=85, y =100)

    btn_crear_usuario = Button(ventana_principal, text="Ingresar",command=crear_ventana_ingresar)
    btn_crear_usuario.config(width=12 , height=1,font="Arial 10 bold", relief="raised", bd=4)
    btn_crear_usuario.place(x=205, y =100)

    #**************************INTEGRANTES**********************************************

    t_integrantes = Label(ventana_principal, text="Construida por:")
    t_integrantes.place(x=140,y =160)
    t_integrantes.config(font="Arial 11 bold",bg="#1C2833",fg="white")

    text_integrantes = "Matias Agustin Martinez, Josue Daniel Arturo Segura Valer, Bryan Hernán Serrantes Ochoa, Lucas Ezequiel Zenobio, Federico Aguilar "
    integrantes = Label(ventana_principal, text=text_integrantes, wraplength=280)
    integrantes.config(bg="#1C2833", fg="white")
    integrantes.place(x=65,y = 180)

    return ventana_principal


#********************************************************************************************
#*************************FUNCIONES NECESARIAS PARA VENTANA REGISTRARSE**********************
#********************************************************************************************

#**************************REQUISITOS PARA USUARIO Y CLAVE***********************************

def validar_usuario(usuario):
    """
        
    >>> validar_usuario("")
    False
        
    >>> validar_usuario("UsuarioDemasiadoExtenso")
    False
        
    >>> validar_usuario("Usuario&&&")
    False
        
    >>> validar_usuario("12345678")
    True
        
    >>> validar_usuario("Agamenón")
    True
        
    >>> validar_usuario("Ayante_Oileo")
    True
        
    >>> validar_usuario("Diomedes_1282")
    True
        
    >>> validar_usuario("Pony.infernal")
    True
        
    >>> validar_usuario("##$")
    False
        
    >>> validar_usuario("--------")
    True

    """
    

    caracteres_validos = "_-."
    usuario_valido = True
    longitud = len(usuario)

    """Valida la longitud y si contiene algun caracter que no
    en los caracteres validos"""

    #Retorna un booleano

    if longitud >= 5 and longitud <= 15:
        iterador = 0
        while usuario_valido == True and iterador != longitud:
            caracter = usuario[iterador]
            if caracter.isalnum() or caracter in caracteres_validos:
                usuario_valido = True
            else:
                usuario_valido = False
            iterador += 1
    else:
        usuario_valido = False
    return usuario_valido


def validar_clave(clave):

    """
        
    Demasiado corta:
    >>> validar_clave("123")
    False
    
    Sin mayúsculas:
    >>> validar_clave("jirafa1#")
    False
    
    Sin minúsculas:
    >>> validar_clave("JIRAFA5*")
    False
    
    Sin dígitos:
    >>> validar_clave("Jirafas-")
    False
    
    Sin símbolos requeridos:
    >>> validar_clave("Jirafa7/")
    False
    
    Con todos los requisitos:
    >>> validar_clave("Jirafa9#")
    True
    
    Demasiado larga:
    >>> validar_clave("Hipopótamo3#")
    False
    
    Con caracteres adyacentes repetidos:
    >>> validar_clave("Sello42#")
    False
    
    >>> validar_clave("Cabra12*")
    True
    
    >>> validar_clave("Dodo76-#")
    True
    
    """

    longitud_valida = True if(len(clave) >= 4 and len(clave) <= 8) else False
    hay_mayus   = False
    hay_minus   = False
    hay_digit   = False
    hay_simbolo = False
    adyacentes  = False
    
    if(longitud_valida):
        i = 0
        while(i < len(clave) and not adyacentes):
            if(clave[i].isupper()):
                hay_mayus = True
            elif(clave[i].islower()):
                hay_minus = True
            elif(clave[i].isdigit()):
                hay_digit = True
            elif(clave[i] in "_-#*"):
                hay_simbolo = True
                
            i += 1
            
            if(i < len(clave) and clave[i] == clave[i - 1]):
                adyacentes = True
                
    if longitud_valida and hay_mayus and hay_minus and hay_digit and hay_simbolo and not adyacentes:
            valido = True
    else:
        valido = False
    return valido



#**************FUNCION COMPROBAR QUE USUARIO ESTE EN ARCHIVO*************************

def buscar_usuario(usuario,archivo):
    """
    Revisa la existencia del usuario ingresado
    en el archivo pertinente, 
    retornando un boleano
    """
    #usuario pertenece a la variable ingresada
    #user pertenece al archivo

    registro = leer_archivo(archivo)
    user = registro[POSICION_USUARIO]
    existencia = False

    while user != "" and existencia == False:
        if usuario == user:
            existencia = True
        registro = leer_archivo(archivo)
        user = registro[POSICION_USUARIO]
    return existencia

#**************FUNCION OBTENER INDICE DE PREGUNTA****************************

def obtener_indice_de_pregunta(pregunta):
    archivo = open("preguntas.csv")
    preguntas = leer_archivo(archivo)
    pregunta_archivo = preguntas[1]
    while pregunta != pregunta_archivo:
         preguntas = leer_archivo(archivo)
         pregunta_archivo = preguntas[1]
    archivo.close()
    return preguntas[0]

#***********FUNCION REGISTRAR DATOS EN ARCHIVO USUARIOS.CSV**************

def registar_datos(usuario,clave,id_pregunta,respuesta,intentos_recuperacion,archivo):
    archivo.write(usuario + "," + clave + "," + id_pregunta + "," + respuesta + "," + intentos_recuperacion + "\n")


#********************************************************************************************
#****************************VENTANA REGISTRARSE*********************************************
#********************************************************************************************


def crear_ventana_registrarse():

    ventana_registrarse = Tk()
    ventana_registrarse.resizable(False,False)
    ventana_registrarse.geometry("240x280")
    ventana_registrarse.title("Crear usuario")
    ventana_registrarse.iconbitmap("supernova.ico")
    ventana_registrarse.config(cursor="hand2", bg="#1C2833")

    #LABEL USUARIO

    label_entrada_usuario = Label(ventana_registrarse, text="Usuario:")
    label_entrada_usuario.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
    label_entrada_usuario.place(x =5, y =40)

    #CASILLA USUARIO

    usuario = StringVar()
    casilla_usuario = Entry(ventana_registrarse, textvariable=usuario)
    casilla_usuario.config(width=24)
    casilla_usuario.place(x = 80, y = 40)

    # LABEL CLAVE

    label_entrada_clave = Label(ventana_registrarse, text="Clave:")
    label_entrada_clave.config(font = "Arial 11 bold",bg="#1C2833",fg="white")
    label_entrada_clave.place(x = 5 , y =70)

    #CASILLA CLAVE

    clave = StringVar()
    casilla_clave = Entry(ventana_registrarse, textvariable=clave)
    casilla_clave.config(width=24)
    casilla_clave.place(x = 80, y = 70)
    
    #OBTENER PREGUNTAS

    def opciones():
        #Obtener las preguntas del archivo de preguntas
        archivo = open("preguntas.csv")
        registro = leer_archivo(archivo)
        pregunta = registro[POSICION_PREGUNTA_PREGUNTAS]
        lista_preguntas = []
        while registro != LINEA_FIN.split(","):
            lista_preguntas.append(pregunta)
            registro = leer_archivo(archivo)
            pregunta = registro[POSICION_PREGUNTA_PREGUNTAS]
        archivo.close()
        return lista_preguntas
    
    #LABEL RECUPERACION

    label_pregunta = Label(ventana_registrarse, text="Pregunta de recuperacion:")
    label_pregunta.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
    label_pregunta.place(x = 5 , y =110)

    #MENU PREGUNTA RECUPERACION

    pregunta_actual = StringVar(ventana_registrarse)
    pregunta_actual.set("Selecciona una pregunta") 
    option_menu_pregunta = OptionMenu(ventana_registrarse, pregunta_actual, *opciones())
    option_menu_pregunta.config(width = 30,font = "Arial 8 bold")
    option_menu_pregunta.place(x = 5, y = 140)

    #LABEL RESPUESTA RECUPERACION

    label_respuesta = Label(ventana_registrarse, text = "Respuesta:")
    label_respuesta.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
    label_respuesta.place(x = 5 , y = 190)

    #CASILLA RESPUESTA

    respuesta = StringVar()
    casilla_respuesta = Entry(ventana_registrarse, textvariable= respuesta)
    casilla_respuesta.config(width=22)
    casilla_respuesta.place(x = 95, y = 190)

    #FUNCION QUE REDIRECCIONA LOS DATOS INGRESADOS A:
    #  "FUNCIONES NECESARIAS PARA VENTANA REGISTRARSE"

    def enviar_a_validar():

        """Envia a validar el usuario y la clave a sus respectivas funciones,
        muestra mensajes de informacion de error y correcta validación,
        tambien las condiciones para que estos sean validos"""

        usuario = casilla_usuario.get()
        clave = casilla_clave.get()
        pregunta = pregunta_actual.get()
        respuesta = casilla_respuesta.get()

        modo_de_apertura =  verificar_existencia_de_archivo("usuarios.csv")
        archivo = open("usuarios.csv", modo_de_apertura)

        #Suponiendo que nadie ingrese un usuario que no cumpla las condiciones
        #primero busco la existencia de este, luego lo valido al mismo tiempo que la clave

        if buscar_usuario(usuario,archivo):
            messagebox.showerror("Error","Usuario Existente")
        else:
            if validar_usuario(usuario) and validar_clave(clave) and respuesta != "" and pregunta!="Selecciona una pregunta":
                messagebox.showinfo("Validación", "Creado correctamente")
                indice_pregunta = obtener_indice_de_pregunta(pregunta)
                registar_datos(usuario,clave,indice_pregunta,respuesta,"0",archivo)
                archivo.close()
            else:
                messagebox.showerror("Usuario o Constraseña invalido", REQUISITOS_USUARIO_CLAVE)
            
        archivo.close()


    #BOTON REGISTRAR

    btn_confirmar = Button(ventana_registrarse, text="Registrar",command=enviar_a_validar)
    btn_confirmar.config(font="Arial 12 bold")
    btn_confirmar.place(x = 72, y = 230)

    ventana_registrarse.mainloop()


#*****************************************************************************************************
#*************************************FUNCIONES VENTANA INGRESAR**************************************
#*****************************************************************************************************

def comprobar_usuario_clave(usuario,clave):
    modo_de_apertura =  verificar_existencia_de_archivo("usuarios.csv")
    archivo = open("usuarios.csv", modo_de_apertura)

    #usuario y clave ingresados por el usuario
    #user and password son obtenidos del archivo
    #verifica la existencia del usuario y clave

    registro = leer_archivo(archivo)
    user = registro[POSICION_USUARIO]
    password = registro[POSICION_CLAVE]

    existencia = False

    while registro != LINEA_FIN.split(",") and existencia == False:
        if usuario == user and clave == password:
            existencia = True
        registro = leer_archivo(archivo)
        user = registro[POSICION_USUARIO]
        password = registro[POSICION_CLAVE]
    
    archivo.close()
    return existencia

#***************************************************************************************
#**********************************VENTANA INGRESAR*************************************
#***************************************************************************************

def crear_ventana_ingresar():

    ventana_ingresar = Tk()
    ventana_ingresar.resizable(False,False)
    ventana_ingresar.geometry("260x180")
    ventana_ingresar.title("Identificación para acceso")
    ventana_ingresar.iconbitmap("supernova.ico")
    ventana_ingresar.config(cursor="hand2", bg="#1C2833")

    #LABEL USUARIO

    label_usuario = Label(ventana_ingresar, text="Usuario:")
    label_usuario.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
    label_usuario.place(x = 10, y = 30)

    #CASILLA USUARIO

    usuario = StringVar()
    casilla_usuario = Entry(ventana_ingresar, textvariable=usuario)
    casilla_usuario.place(x = 80, y = 30)

    # LABEL CLAVE

    label_clave = Label(ventana_ingresar, text="Clave:")
    label_clave.config(font = "Arial 11 bold",bg="#1C2833",fg="white")
    label_clave.place(x = 10 , y = 60)

    #CASILLA CLAVE

    clave = StringVar()
    casilla_clave = Entry(ventana_ingresar, textvariable=clave)
    casilla_clave.place(x = 80, y = 60)

    #FUNCION AL PRESION BOTON INGRESAR

    def presionar_ingresar():
        usuario = casilla_usuario.get()
        clave = casilla_clave.get()

        modo_de_apertura =  verificar_existencia_de_archivo("usuarios.csv")
        archivo = open("usuarios.csv", modo_de_apertura)

        if not(buscar_usuario(usuario,archivo) and not usuarioBloqueado(usuario)):
            archivo.close()
            messagebox.showerror("Error","Usuario inexistente o bloqueado")
        elif clave == "" or usuario == "":
            messagebox.showerror("Error","Ingrese usuario y clave")
        else:
            existencia_clave_usuario = comprobar_usuario_clave(usuario,clave)
            if existencia_clave_usuario:
                messagebox.showinfo("Acceso","Correcto")
                ventana_ingresar.destroy()
                click_ventana_cifrado(usuario)
            else:
                messagebox.showerror("Identificador inexistente o clave errónea"\
                                     ,"Si no se encuentra registrado debe registrarse\
 previamente o si olvidaste la clave presiona el botón recuperar clave")
        archivo.close()
    #BOTON INGRESAR

    btn_ingresar_usuario = Button(ventana_ingresar, text="Ingresar", command=presionar_ingresar)
    btn_ingresar_usuario.config(width=12 , height=1,font="Arial 10 bold")
    btn_ingresar_usuario.place(x=10, y = 100)

    #FUNCION AL PRESIONAR [RECUPERAR CLAVE]

    def click_recuperar_usuario():
        usuario = casilla_usuario.get() 
        
        modo_de_apertura =  verificar_existencia_de_archivo("usuarios.csv")
        archivo = open("usuarios.csv", modo_de_apertura)


        if(buscar_usuario(usuario,archivo) and not usuarioBloqueado(usuario)):
            archivo.close()
            ventana_recup = crearVentanaRecup(usuario)
            ventana_recup.mainloop()
        else:
            messagebox.showerror("Error","Usuario inexistente o bloqueado")
        archivo.close() 

     #BOTON RECUPERAR CLAVE

    btn_recuperar_clave = Button(ventana_ingresar, text="Recuperar clave",command=click_recuperar_usuario)
    btn_recuperar_clave.config(width=12 , height=1,font="Arial 10 bold", padx=10)
    btn_recuperar_clave.place(x=125, y = 100)

    ventana_ingresar.mainloop()

#************************************************************************************************
#************************FUNCIONES RECUPERACION DE CLAVE*****************************************
#************************************************************************************************

def obtener_pregunta(registro):
        archivo = open("preguntas.csv")
        preguntas = leer_archivo(archivo)
        id_preg_archivo = preguntas[ID_PREGUNTA_PREGUNTAS] 
        id_preg_registro = registro[ID_PREGUNTA_DATOS]

        #guardo por si es la primera pregunta
        #ya que no entraria al while

        pregunta = preguntas[POSICION_PREGUNTA_PREGUNTAS]
        while id_preg_registro != id_preg_archivo:
            preguntas = leer_archivo(archivo)
            id_preg_archivo = preguntas[ID_PREGUNTA_PREGUNTAS]
            pregunta = preguntas[POSICION_PREGUNTA_PREGUNTAS]

        archivo.close()
        return pregunta

def actualizarIntentos(usuario, acceso_exitoso):
    intentos = 0
    os.rename("usuarios.csv", "usuarios_old.csv")
    usuarios_new = open("usuarios.csv", "w")
    usuarios_old = open("usuarios_old.csv", "r")
    
    registro = leer_archivo(usuarios_old)
    while(registro != LINEA_FIN.split(",")):
        if(registro[POSICION_USUARIO] == usuario):
            intentos = 0 if(acceso_exitoso) else int(registro[POSICION_INTENTOS]) + 1
            registro[POSICION_INTENTOS] = str(intentos)
        
        usuarios_new.write(convertirRegistro(registro))
        registro = leer_archivo(usuarios_old)
        
    usuarios_new.close()
    usuarios_old.close()
    os.remove("usuarios_old.csv")
    
    return intentos
    
def convertirRegistro(registro):
    linea = ""
    
    for c in range(len(registro)):
        linea += registro[c] + ","
        
    linea = linea[ : -1]
    linea += "\n" 
    
    return linea

def registroUsuario(usuario):
    
    if(os.path.isfile("./usuarios.csv")):
        usuarios = open("usuarios.csv", "r")
        registro = leer_archivo(usuarios)
        
        while(registro != LINEA_FIN.split(",") and usuario != registro[POSICION_USUARIO]):
            registro = leer_archivo(usuarios)
        
        usuarios.close()
        
    return registro
    
def usuarioBloqueado(usuario):
    INTENTOS = 4
    registro = registroUsuario(usuario)
    return int(registro[INTENTOS]) > 3
        

#***********************************************************************************************
#**************************VENTANA DE RECUPERACIÓN DE CLAVE**********************************
#***************************************************************************************************

USUARIO_X = 10
USUARIO_Y = 15

def crearVentanaRecup(usuario):

    ventana_recup = Tk()
    ventana_recup.resizable(False,False)
    ventana_recup.geometry("240x180")
    ventana_recup.title("Recuperación Clave")
    ventana_recup.iconbitmap("supernova.ico")
    ventana_recup.config(cursor="hand2", bg="#1C2833") 
    
    # Label de pregunta
    
    registro = registroUsuario(usuario)
    pregunta = obtener_pregunta(registro)
    
    label_pregunta = Label(ventana_recup, text = pregunta + ":")
    label_pregunta.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
    label_pregunta.place(x = USUARIO_X, y = USUARIO_Y)
    
    label_respuesta = Label(ventana_recup, text="Respuesta:")
    label_respuesta.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
    label_respuesta.place(x = USUARIO_X, y = USUARIO_Y + 30)

    usuario_respuesta = StringVar()
    entrada_respuesta = Entry(ventana_recup,textvariable=usuario_respuesta)
    entrada_respuesta.place(x = USUARIO_X + 90 , y = USUARIO_Y + 30)
    
    #Al apretar [Recuperar]

    def click_probar_recup(ventana_recup, entrada_respuesta, registro):
    
        respuesta = entrada_respuesta.get()
    
        if(registro[ID_RESPUESTA] == respuesta):
            crearLabelTemporal(ventana_recup, "Su clave es: " + registro[POSICION_CLAVE], USUARIO_X, USUARIO_Y + 80, 6000)
            actualizarIntentos(registro[POSICION_USUARIO], True)
        else:
            crearLabelTemporal(ventana_recup, "¡Respuesta incorrecta!", USUARIO_X, USUARIO_Y + 100, 1000)
            intentos = actualizarIntentos(registro[POSICION_USUARIO], False)
            
            if(intentos > 3):
                crearLabelTemporal(ventana_recup, "Usuario bloqueado", USUARIO_X, USUARIO_Y + 120, 2000)
                ventana_recup.after(1000, lambda: ventana_recup.destroy())   
    
    # Botón de ingreso de respuesta
    
    btn_recuperar = Button(ventana_recup, text = "Recuperar", width = 10, height = 1, command = lambda: click_probar_recup(ventana_recup,\
    entrada_respuesta, registro))
    btn_recuperar.config(font="Arial 10 bold")
    btn_recuperar.place(x = USUARIO_X, y = USUARIO_Y + 60)    
    
    return ventana_recup  

#****************************************************************************************************
#***********************************VENTANA DE CIFRADO***********************************************
#****************************************************************************************************
# Autor: Matías Agustín Martínez   
    
def crearVentanaCifrado(usuario):
    
    MAIN_Y = 10

    ventana_cifrado = Tk()
    ventana_cifrado.resizable(False,False)
    ventana_cifrado.geometry("400x400")
    ventana_cifrado.title("Cifrado y envío de mensajes")
    ventana_cifrado
    ventana_cifrado.config(cursor="hand2", bg="#1C2833")

    #ENTRADA DE TEXTO LABEL Y CASILLA -----SEGUNDA VENTANA-------
            #uso Text para mejor visualizacion del texto

    label_entrada_texto = Label(ventana_cifrado, text="Por favor, introduzca el texto a cifrar:")
    label_entrada_texto.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
    label_entrada_texto.place(x = 65, y = MAIN_Y)
    entrada_texto = Text(ventana_cifrado,width=40,height=5)#Para obtener todo el texto usamos .get("1.0", "end-1c")
    entrada_texto.place(x = 38, y = MAIN_Y + 30)

    #ENTRADA DE CLAVE PARA CIFRADO CESAR -----SEGUNDA VENTANA-------

    CLAVE_X = 130

    label_entrada_clave = Label(ventana_cifrado, text="Clave (sólo César)")
    label_entrada_clave.config(font = "Arial 10 bold",bg="#1C2833",fg="white")
    label_entrada_clave.place(x = CLAVE_X - 15, y = MAIN_Y + 125)

    clave = IntVar()
    entrada_clave = Entry(ventana_cifrado, textvariable=clave, width = 5)
    entrada_clave.place(x = CLAVE_X + 105, y = MAIN_Y + 125)

    #BOTONES
    
    BUTTON_WIDTH = 15
    
    TOP_LEFT_X = 75
    TOP_LEFT_Y = MAIN_Y + 170

    btn_cifrado_cesar = Button(ventana_cifrado, text="Cifrar (César)", width = BUTTON_WIDTH, command=lambda: al_presionar("c-cesar", entrada_texto, entrada_clave))
    btn_cifrado_cesar.config(font="Arial 10 bold", relief="raised", bd=3)
    btn_cifrado_cesar.place(x = TOP_LEFT_X - 5, y = TOP_LEFT_Y - 5)

    btn_decifrado_cesar = Button(ventana_cifrado, text="Descifrar (César)", width = BUTTON_WIDTH, command=lambda: al_presionar("d-cesar", entrada_texto, entrada_clave))
    btn_decifrado_cesar.config(font="Arial 10 bold", relief="raised", bd=3)
    btn_decifrado_cesar.place(x = TOP_LEFT_X + 130 + 5, y = TOP_LEFT_Y - 5 )

    btn_cifrado_atbash = Button(ventana_cifrado, text="Cifrar (Atbash)", width = BUTTON_WIDTH, command=lambda: al_presionar("c-atbash", entrada_texto, entrada_clave))
    btn_cifrado_atbash.config(font="Arial 10 bold", relief="raised", bd=3)
    btn_cifrado_atbash.place(x = TOP_LEFT_X - 5, y = TOP_LEFT_Y + 30)

    btn_decifrado_atbash = Button(ventana_cifrado, text="Descifrar (Atbash)", width = BUTTON_WIDTH, command=lambda: al_presionar("d-atbash", entrada_texto, entrada_clave))
    btn_decifrado_atbash.config(font="Arial 10 bold", relief="raised", bd=3)
    btn_decifrado_atbash.place(x = TOP_LEFT_X + 130 + 5, y = TOP_LEFT_Y + 30)
    
    # Botones de envío de mensajes
    
    btn_enviar_cesar = Button(ventana_cifrado, text="Enviar mensaje cifrado César", width = 30, command = lambda: click_enviar(usuario, "C", entrada_clave, entrada_texto))
    btn_enviar_cesar.config(font="Arial 10 bold", relief="raised", bd=3)
    btn_enviar_cesar.place(x = TOP_LEFT_X, y = TOP_LEFT_Y + 90)
    
    btn_enviar_atbash = Button(ventana_cifrado, text="Enviar mensaje cifrado Atbash", width = 30, command = lambda: click_enviar(usuario, "A", entrada_clave, entrada_texto))
    btn_enviar_atbash.config(font="Arial 10 bold", relief="raised", bd=3)
    btn_enviar_atbash.place(x = TOP_LEFT_X, y = TOP_LEFT_Y + 120)
    
    # Botón de consulta de mensajes
    
    btn_consultar = Button(ventana_cifrado, text = "Consultar mensajes", width = 20, command = lambda: click_consultarMensajes(usuario))
    btn_consultar.config(font="Arial 10 bold", relief="raised", bd=3)
    btn_consultar.place(x = TOP_LEFT_X + 40, y = TOP_LEFT_Y + 170)
    
    return ventana_cifrado



def al_presionar(boton, entrada_texto, entrada_clave):
    texto_obtenido = entrada_texto.get("1.0", "end-1c")
    clave_string = entrada_clave.get()
        
    #Si el campo está vacío o no es numérico se establece
    #la clave en 0
        
    if(clave_string == "" or not clave_string.isdigit()):
        clave = 0
        entrada_clave.delete(0, END)
        entrada_clave.insert(0, "0")
    else:
        clave = int(clave_string)
        
    #Llamado de funciones --- botones
        
    if boton == "c-cesar":
        texto_cifrado = cifrar_c(texto_obtenido, clave)
    elif boton == "c-atbash":
        texto_cifrado = cifrar_atbash(texto_obtenido)
    elif boton == "d-cesar":
        texto_cifrado = descifrar_c(texto_obtenido, clave)
    elif boton == "d-atbash":
        texto_cifrado = descifrar_atbash(texto_obtenido)
            
    entrada_texto.delete("1.0", "end")
    entrada_texto.insert("1.0",texto_cifrado)



def click_consultarMensajes(usuario):
    mensajes = None
    
    if(os.path.isfile("mensajes.csv")):
        mensajes = open("mensajes.csv", "r")
    else:
        mensajes = open("mensajes.csv", "w+")
      
    a_todos = []
    propios = []
    
    DESTINATARIO = 0
    REMITENTE    = 1
    CIFRADO      = 2
    MENSAJE      = 3
    
#buscar_usuario

    registro = leer_archivo(mensajes)
    while(registro != LINEA_FIN.split(",")):
        if(registro[DESTINATARIO] == "*"):
            descifrado = descifrar_c(registro[MENSAJE], int((registro[CIFRADO])[1 : ])) if(registro[CIFRADO][0] == "C") else descifrar_atbash(registro[MENSAJE])
            a_todos.append("#" + registro[REMITENTE] + ": " + descifrado)
        elif(registro[DESTINATARIO] == usuario):
            descifrado = descifrar_c(registro[MENSAJE], int((registro[CIFRADO])[1 : ])) if(registro[CIFRADO][0] == "C") else descifrar_atbash(registro[MENSAJE])
            propios.append(registro[REMITENTE] + ": " + descifrado)
            
        registro = leer_archivo(mensajes)
        
    for i in range(len(a_todos)):
        print(a_todos[i])
        
    for i in range(len(propios)):
        print(propios[i])
        
    mostrarVentanaMensajes(a_todos, propios)
        
    mensajes.close()
    
    
    
def mostrarVentanaMensajes(m_a_todos, m_propios):

    ventana_mensajes = Tk()
    ventana_mensajes.resizable(False,False)
    ventana_mensajes.geometry("400x400")
    ventana_mensajes.title("Mensajes")
    ventana_mensajes
    ventana_mensajes.config(cursor="hand2", bg="#1C2833")
    
    # Lista de mensajes
    
    mensajes = Listbox(ventana_mensajes, activestyle = NONE)
    mensajes.config(font = "Arial 10 bold",bg="#1C2833",fg="white")
    mensajes.pack(fill = BOTH, expand = 1)
    
    mensajes.insert(END, "Lista de mensajes: ")
    mensajes.insert(END, "---------------------------------------------------------------------------------------------------")
    
    for m in range(len(m_a_todos)):
        mensajes.insert(END, m_a_todos[m])
        mensajes.insert(END, "---------------------------------------------------------------------------------------------------")
 
    for m in range(len(m_propios)):
        mensajes.insert(END, m_propios[m])
        mensajes.insert(END, "---------------------------------------------------------------------------------------------------")  

    mensajes.insert(END, "Total de mensajes: " + str(len(m_a_todos) + len(m_propios)))
    
    mensajes.mainloop()
    

def click_enviar(remitente, cifrado, entrada_clave, entrada_texto):
    ventana_envio = crearVentanaEnvio(remitente, cifrado, entrada_clave, entrada_texto)
    ventana_envio.mainloop()


def click_ventana_cifrado(usuario):
    ventana_cifrado = crearVentanaCifrado(usuario)
    ventana_cifrado.mainloop()
      
    
#---------------------------VENTANA DE ENVÍO DE MENSAJES-----------------------#

def crearVentanaEnvio(remitente, cifrado, entrada_clave, entrada_texto):
    
    titulo = ""
    if(cifrado == "C"):
        titulo = "Enviar mensaje cifrado César"
    else:
        titulo = "Enviar mensaje cifrado Atbash"
    
    ventana_envio = Tk()
    ventana_envio.resizable(False,False)
    ventana_envio.geometry("400x200")
    ventana_envio.title(titulo)
    ventana_envio
    ventana_envio.config(cursor="hand2", bg="#1C2833")

    # Entrada de texto de destinatario

    label_entrada_usuario = Label(ventana_envio, text="Usuario:")
    label_entrada_usuario.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
    label_entrada_usuario.place(x = USUARIO_X - 10, y = USUARIO_Y)
    
    entrada_usuario = Text(ventana_envio,width = 15, height = 1) #Para obtener todo el texto usamos .get("1.0", "end-1c")
    entrada_usuario.place(x = USUARIO_X + 65, y = USUARIO_Y)
    
    # Botón de ingreso
    
    btn_ingresar = Button(ventana_envio, text = "Ingresar", width = 10, height = 1, command = lambda: click_probarEnvio(ventana_envio, \
    remitente, entrada_usuario, cifrado, entrada_clave, entrada_texto))
    
    btn_ingresar.config(font="Arial 10 bold")
    btn_ingresar.place(x = USUARIO_X + 80, y = USUARIO_Y + 40)
   
    return ventana_envio



def click_probarEnvio(ventana, remitente, entrada_usuario, cifrado, entrada_clave, entrada_texto):
    texto_cifrado = entrada_texto.get("1.0", "end-1c")
    clave_cifrado = entrada_clave.get()
    destinatario  = entrada_usuario.get("1.0", "end-1c")
    
         # Archivo donde se almacenan los mensajes
    archivo = open("usuarios.csv")
        
    if((destinatario == "*" or buscar_usuario(destinatario,archivo)) and destinatario != remitente and texto_cifrado != ""):
        guardarMensaje(destinatario, remitente, cifrado, clave_cifrado, texto_cifrado)
        archivo.close()
        crearLabelTemporal(ventana, "Mensaje enviado", USUARIO_X + 70, USUARIO_Y + 80, 3000)
    else:
        crearLabelTemporal(ventana, "Usuario inexistente", USUARIO_X + 65, USUARIO_Y + 80, 3000)
        archivo.close()
    
        
def guardarMensaje(destinatario, remitente, cifrado, clave, mensaje_cifrado):
    mensajes = open("mensajes.csv", "a")
    cifrado = "A" if(cifrado == "A") else "C" + clave
    nueva_linea = destinatario + "," + remitente + "," + cifrado + "," + mensaje_cifrado + "\n"
    mensajes.write(nueva_linea)
    mensajes.close()
    
    
    
def leerUsuarios():
    archivo = open("usuarios.csv", "r+")
    usuarios = []
    USUARIO  = 0
    
    linea = archivo.readline()
    while(linea):
        linea = linea.rstrip()
        registro = linea.split(",")
        usuarios.append(registro[USUARIO])
        linea = archivo.readline()
    
    archivo.close()
    return usuarios


#****************************************************************************************
#**********************************MAIN VENTANA PRINCIPAL********************************
#****************************************************************************************

def main():
    ventana_principal = crearVentanaPrincipal()
    ventana_principal.mainloop()
    

if __name__ == "__main__":
    import doctest  
    doctest.testmod()

main()

