#Escribir una función que reciba el mensaje a cifrar (cadena de caracteres) y la clave de
#cifrado, y devuelva el mensaje cifrado, mediante el cifrado césar. Probarla utilizando doctest,
#con al menos 10 casos diferentes.

from tkinter import *
import os.path

#***********************************************************

def crearRelacion():
    #Autor: José Daniel Arturo Segura Valer

    caracter_a_pos = {}
    pos_a_caracter = {}
    
    # Creamos una tabla con los caracteres que pueden desplazarse;
    # en nuestro caso  son sólo los alfanuméricos. La tabla asigna
    # al caracter "a" la posición 0, al "b" la posición 1 y así su-
    # cesivamente hasta llegar a la posición 63, que está asignada
    # al caracter "9". Esta tabla se opera con dos diccionarios, uno
    # que dado un caracter devuelve su posición, y otro que dada una
    # posición devuelve un caracter
    
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

    # cantidad : Tamaño del grupo según tipo de caracter. Hay 27 minúsculas, 27 mayúsculas y 10 dígitos
    # offset   : distancia del primer caracter del grupo al inicio de la tabla. La "a" dista 0 posiciones, 
    #            la "A" 27 y el "0" 54
    # alnum    : Indicador de caracter alfanumérico. Si es falso el caracter hallado no se altera.

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

    # dist_ini : Distancia del caracter a la posición 0 dentro de su grupo
    # pos_fin  : La mayor posición dentro del grupo. Por ejemplo, dentro de los
    #            dígitos es la posición 9.

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
    
#***************************************************************

def validarUsuario(usuario):

        """
        
        >>> validarUsuario("")
        False
        
        >>> validarUsuario("UsuarioDemasiadoExtenso")
        False
        
        >>> validarUsuario("Usuario&&&")
        False
        
        >>> validarUsuario("12345678")
        True
        
        >>> validarUsuario("Agamenón")
        True
        
        >>> validarUsuario("Ayante_Oileo")
        True
        
        >>> validarUsuario("Diomedes_1282")
        True
        
        >>> validarUsuario("Pony.infernal")
        True
        
        >>> validarUsuario("##$")
        False
        
        >>> validarUsuario("--------")
        True

        """

        longitud_valida = True if(len(usuario) >= 5 and len(usuario) <= 15) else False
        caracteres_validos = True
        
        if(longitud_valida):
            i = 0;
            while(i < len(usuario) and caracteres_validos):
                if(not usuario[i].isalnum() and not usuario[i] in "_-."):
                    caracteres_validos = False
                
                i += 1
                
        return longitud_valida and caracteres_validos
        
        
def validarClave(clave):

    """
        
    Demasiado corta:
    >>> validarClave("123")
    False
    
    Sin mayúsculas:
    >>> validarClave("jirafa1#")
    False
    
    Sin minúsculas:
    >>> validarClave("JIRAFA5*")
    False
    
    Sin dígitos:
    >>> validarClave("Jirafas-")
    False
    
    Sin símbolos requeridos:
    >>> validarClave("Jirafa7/")
    False
    
    Con todos los requisitos:
    >>> validarClave("Jirafa9#")
    True
    
    Demasiado larga:
    >>> validarClave("Hipopótamo3#")
    False
    
    Con caracteres adyacentes repetidos:
    >>> validarClave("Sello42#")
    False
    
    >>> validarClave("Cabra12*")
    True
    
    >>> validarClave("Dodo76-#")
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
                
    return longitud_valida and hay_mayus and hay_minus and hay_digit and hay_simbolo and not adyacentes
    
    
#***************************************************************
    
if __name__ == "__main__":
    import doctest  
    doctest.testmod()


#--------------------------------------INTERFAZ GRAFICA--------------------------------------#

#--------------------------------------VENTANA PRINCIPAL-------------------------------------#
# Autor: Lucas Ezequiel Zenobio

def crearVentanaPrincipal():

    ventana_principal = Tk()
    ventana_principal.resizable(False,False)
    ventana_principal.geometry("400x300")
    ventana_principal.title("TP Grupal Parte 1 - Grupo: Supernova")
    ventana_principal.config(cursor="hand2",bg="#1C2833")
    ventana_principal.iconbitmap("supernova.ico")

    MAIN_SECTION_Y = 30

    texto_bienvenida = "Bienvenido a la aplicación de mensajes secretos del grupo Supernova:"
    bienvenida = Label(ventana_principal, text = texto_bienvenida, wraplength = 350)
    bienvenida.config(font = "Arial 11 bold", bg = "#1C2833", fg = "white")
    bienvenida.place(x = 25, y = MAIN_SECTION_Y)

    #Boton para acceder a la siguiente ventana ---primera ventana----

    btn_crear_usuario = Button(ventana_principal,text="Crear usuario", command = click_nuevo_usuario)
    btn_crear_usuario.config(width=12 , height=1,font="Arial 10 bold", relief="raised", bd=4)
    btn_crear_usuario.place(x=85, y = MAIN_SECTION_Y + 80)

    #Boton para salir ----primera ventana----

    btn_salir = Button(ventana_principal, text="Ingreso usuario", command = click_acceso_usuario)
    btn_salir.config(width=12 , height=1,font="Arial 10 bold", relief="raised", bd=4)
    btn_salir.place(x=205, y = MAIN_SECTION_Y + 80)

    #Sección de autores

    MADE_BY_Y = 200

    t_integrantes = Label(ventana_principal, text="Construida por:")
    t_integrantes.place(x=140,y = MADE_BY_Y)
    t_integrantes.config(font="Arial 11 bold",bg="#1C2833",fg="white")

    text_integrantes = "Matias Agustin Martinez, Josue Daniel Arturo Segura Valer, Bryan Hernán Serrantes Ochoa, Lucas Ezequiel Zenobio, Federico Aguilar "
    integrantes = Label(ventana_principal, text=text_integrantes, wraplength=280)
    integrantes.config(bg="#1C2833", fg="white")
    integrantes.place(x=65,y = MADE_BY_Y + 20)
    
    return ventana_principal
    
    
    
#------------------------------VENTANA DE CREACIÓN DE USUARIO--------------------------------#

USUARIO_X = 85
USUARIO_Y = 40

def crearVentanaNuevoUsuario():

    ventana_nuevo_usuario = Tk()
    ventana_nuevo_usuario.resizable(False,False)
    ventana_nuevo_usuario.geometry("400x350")
    ventana_nuevo_usuario.title("Crear usuario")
    ventana_nuevo_usuario.iconbitmap("supernova.ico")
    ventana_nuevo_usuario.config(cursor="hand2", bg="#1C2833")

    # Entrada de texto de usuario

    label_entrada_usuario = Label(ventana_nuevo_usuario, text="Usuario:")
    label_entrada_usuario.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
    label_entrada_usuario.place(x = USUARIO_X, y = USUARIO_Y)
    
    entrada_usuario = Text(ventana_nuevo_usuario,width = 15, height = 1) #Para obtener todo el texto usamos .get("1.0", "end-1c")
    entrada_usuario.place(x = USUARIO_X + 75, y = USUARIO_Y)

    # Entrada de texto de clave

    label_entrada_clave = Label(ventana_nuevo_usuario, text="Clave:")
    label_entrada_clave.config(font = "Arial 11 bold",bg="#1C2833",fg="white")
    label_entrada_clave.place(x = USUARIO_X + 8, y = USUARIO_Y + 30)

    entrada_clave = Text(ventana_nuevo_usuario, width = 15, height = 1)
    entrada_clave.place(x = USUARIO_X + 75, y = USUARIO_Y + 30)
    
    # Menú de opciones pregunta de seguridad
    
    label_pregunta = Label(ventana_nuevo_usuario, text="Pregunta secreta:")
    label_pregunta.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
    label_pregunta.place(x = USUARIO_X + 55, y = USUARIO_Y + 70)
    
    pregunta_actual = StringVar(ventana_nuevo_usuario)
    pregunta_actual.set("Selecciona una pregunta") 
    option_menu_pregunta = OptionMenu(ventana_nuevo_usuario, pregunta_actual, *leerPreguntas())
    option_menu_pregunta.config(width = 30)
    option_menu_pregunta.place(x = USUARIO_X + 8, y = USUARIO_Y + 100)
    
    # Entrada de texto respuesta
    
    label_entrada_respuesta = Label(ventana_nuevo_usuario, text = "Respuesta:")
    label_entrada_respuesta.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
    label_entrada_respuesta.place(x = USUARIO_X + 80, y = USUARIO_Y + 140)
    
    entrada_respuesta = Text(ventana_nuevo_usuario, width = 15, height = 1)
    entrada_respuesta.place(x = USUARIO_X + 58, y = USUARIO_Y + 170)
    
    # Botón de creación de usuario
    
    btn_crear = Button(ventana_nuevo_usuario, text = "Crear", width = 10, height = 1, command = lambda: guardarDatos(ventana_nuevo_usuario, \
    entrada_usuario, entrada_clave, entrada_respuesta, pregunta_actual))
    
    btn_crear.config(font="Arial 12 bold")
    btn_crear.place(x = USUARIO_X + 67, y = USUARIO_Y + 240)
    
    #entrada_pregunta = Text(ventana_nuevo_usuario, width = 30, height = 1)
    #entrada_pregunta.place(x = USUARIO_X, y = USUARIO_Y + 110)
    
    return ventana_nuevo_usuario



def guardarDatos(ventana_nuevo_usuario, entrada_usuario, entrada_clave, entrada_respuesta, pregunta_actual):
    usuarios = open("usuarios.csv", "a")
    preguntas = leerPreguntas()
    
    nuevo_usuario = entrada_usuario.get("1.0", "end-1c")
    nueva_clave   = entrada_clave.get("1.0", "end-1c")
    respuesta     = entrada_respuesta.get("1.0", "end-1c")
    
    # Si no se selecciona ninguna, la pregunta por defecto es la primera
    if(pregunta_actual.get() not in preguntas):
        pregunta_actual.set(preguntas[0])
        
    id_pregunta   = preguntas.index(pregunta_actual.get()) + 1
    
    # Validación y verificación de existencia
    if(not usuarioExiste(nuevo_usuario)):
        if(validarUsuario(nuevo_usuario) and validarClave(nueva_clave) and respuesta != ""):
            usuarios.write(nuevo_usuario + "," + nueva_clave + "," + str(id_pregunta) + "," + respuesta + "," + "0\n")
        else:
            temp = Label(ventana_nuevo_usuario, text = "Usuario, clave o respuesta inválidos")
            temp.config(font = "Arial 9 bold",bg="#1C2833", fg="white")
            temp.place(x = USUARIO_X + 10, y = USUARIO_Y + 280)
            temp.after(3000, lambda: temp.destroy())
            
    else:
        temp = Label(ventana_nuevo_usuario, text = "¡Identificador en uso!")
        temp.config(font = "Arial 9 bold",bg="#1C2833", fg="white")
        temp.place(x = USUARIO_X + 59, y = USUARIO_Y + 280)
        temp.after(3000, lambda: temp.destroy())
    
    usuarios.close()



def leerRegistro(archivo):
    linea = archivo.readline()
    linea = linea.rstrip()
    return linea.split(",")



def usuarioExiste(usuario):
    clave_usuario = ""
    
    USUARIO = 0
    CLAVE   = 1
    
    if(os.path.isfile("./usuarios.csv")):
        usuarios = open("usuarios.csv", "r")
        registro = leerRegistro(usuarios)
        
        while(registro != [""] and not clave_usuario):
            if(usuario == registro[USUARIO]):
                clave_usuario = registro[CLAVE]
            
            registro = leerRegistro(usuarios)
        
        usuarios.close()
        
    return clave_usuario
    


def registroUsuario(usuario):
    USUARIO = 0
    
    if(os.path.isfile("./usuarios.csv")):
        usuarios = open("usuarios.csv", "r")
        registro = leerRegistro(usuarios)
        
        while(registro != [""] and usuario != registro[USUARIO]):
            registro = leerRegistro(usuarios)
        
        usuarios.close()
        
    return registro

    

def leerPreguntas():
    archivo = open("preguntas.csv", "r")
    preguntas = []
    PREGUNTA  = 1
    
    linea = archivo.readline()
    while(linea):
        linea = linea.rstrip()
        registro = linea.split(",")
        preguntas.append(registro[PREGUNTA])
        linea = archivo.readline()
    
    archivo.close()
    return preguntas    



def click_nuevo_usuario():
    ventana_nuevo_usuario = crearVentanaNuevoUsuario()
    ventana_nuevo_usuario.mainloop()
    
#--------------------------------VENTANA DE INGRESO DE USUARIO-------------------------------#   

def crearVentanaAcceso():

    ventana_acceso = Tk()
    ventana_acceso.resizable(False,False)
    ventana_acceso.geometry("400x300")
    ventana_acceso.title("Identificación para acceso")
    ventana_acceso.iconbitmap("supernova.ico")
    ventana_acceso.config(cursor="hand2", bg="#1C2833")

    # Entrada de texto de usuario

    label_entrada_usuario = Label(ventana_acceso, text="Usuario:")
    label_entrada_usuario.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
    label_entrada_usuario.place(x = USUARIO_X, y = USUARIO_Y)
    
    entrada_usuario = Text(ventana_acceso,width = 15, height = 1) #Para obtener todo el texto usamos .get("1.0", "end-1c")
    entrada_usuario.place(x = USUARIO_X + 75, y = USUARIO_Y)

    # Entrada de texto de clave

    label_entrada_clave = Label(ventana_acceso, text="Clave:")
    label_entrada_clave.config(font = "Arial 11 bold",bg="#1C2833",fg="white")
    label_entrada_clave.place(x = USUARIO_X + 8, y = USUARIO_Y + 30)

    entrada_clave = Text(ventana_acceso, width = 15, height = 1)
    entrada_clave.place(x = USUARIO_X + 75, y = USUARIO_Y + 30)
    
    # Botón de ingreso
    
    btn_ingresar = Button(ventana_acceso, text = "Ingresar", width = 10, height = 1, command = lambda: acceder(ventana_acceso, entrada_usuario, entrada_clave))
    btn_ingresar.config(font="Arial 10 bold")
    btn_ingresar.place(x = USUARIO_X + 90, y = USUARIO_Y + 70)
    
    # Botón de recuperación de clave
    
    btn_recuperar = Button(ventana_acceso, text = "Recuperar clave", width = 15, height = 1, command = lambda: click_recuperar_usuario(ventana_acceso, entrada_usuario))
    btn_recuperar.config(font="Arial 10 bold")
    btn_recuperar.place(x = USUARIO_X + 65, y = USUARIO_Y + 190)
    
    #entrada_pregunta = Text(ventana_acceso, width = 30, height = 1)
    #entrada_pregunta.place(x = USUARIO_X, y = USUARIO_Y + 110)
    
    return ventana_acceso 
    
    
   
def acceder(ventana_acceso, entrada_usuario, entrada_clave):
    usuario      = entrada_usuario.get("1.0", "end-1c")
    clave_actual = entrada_clave.get("1.0", "end-1c")
    
    clave = usuarioExiste(usuario)  # Si el usuario existe la clave es no nula
    if(clave != "" and clave_actual == clave):
        print("INGRESO EXITOSO")
        click_ventana_cifrado()
    else:
        temp1 = Label(ventana_acceso, text = "Identificador inexistente o clave errónea")
        temp1.config(font = "Arial 9 bold",bg="#1C2833", fg="white")
        temp1.place(x = USUARIO_X + 10, y = USUARIO_Y + 110)
        
        temp2 = Label(ventana_acceso, text = "Si no se encuentra registrado debe registrarse previamente o\nsi olvidó la clave presione el botón [Recuperar clave]")
        temp2.config(font = "Arial 9 bold",bg="#1C2833", fg="white")
        temp2.place(x = USUARIO_X - 60, y = USUARIO_Y + 130)
        
        temp1.after(5000, lambda: temp1.destroy())
        temp2.after(5000, lambda: temp2.destroy())
    
def click_acceso_usuario():
    ventana_acceso = crearVentanaAcceso()
    ventana_acceso.mainloop()
    
#------------------------------VENTANA DE RECUPERACIÓN DE CLAVE------------------------------#

def crearVentanaRecup(usuario):
    PREGUNTA  = 2
    RESPUESTA = 3
 
    ventana_recup = Tk()
    ventana_recup.resizable(False,False)
    ventana_recup.geometry("400x300")
    ventana_recup.title("Recuperación Clave")
    ventana_recup.iconbitmap("supernova.ico")
    ventana_recup.config(cursor="hand2", bg="#1C2833") 
    
    # Label de pregunta
    
    registro = registroUsuario(usuario)
    pregunta = leerPreguntas()[int(registro[PREGUNTA]) - 1]
    
    label_pregunta = Label(ventana_recup, text = pregunta + ":")
    label_pregunta.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
    label_pregunta.place(x = USUARIO_X - 50, y = USUARIO_Y)
    
    # Entrada de texto respuesta
    """
    label_entrada_respuesta = Label(ventana_recup, text = "Respuesta:")
    label_entrada_respuesta.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
    label_entrada_respuesta.place(x = USUARIO_X + 80, y = USUARIO_Y + 120)
    """
    
    entrada_respuesta = Text(ventana_recup, width = 15, height = 1)
    entrada_respuesta.place(x = USUARIO_X + 58, y = USUARIO_Y + 60)
    
    # Botón de ingreso de respuesta
    
    btn_ingresar = Button(ventana_recup, text = "Ingresar", width = 10, height = 1, command = lambda: click_probar_recup(ventana_recup,\
    entrada_respuesta, registro))
    btn_ingresar.config(font="Arial 9 bold")
    btn_ingresar.place(x = USUARIO_X + 80, y = USUARIO_Y + 90)    
    
    return ventana_recup
    
 
 
def click_recuperar_usuario(ventana_acceso, entrada_usuario):
    usuario = entrada_usuario.get("1.0", "end-1c")
    
    if(usuarioExiste(usuario)):
        ventana_recup = crearVentanaRecup(usuario)
        ventana_recup.mainloop()
    else:
        temp = Label(ventana_acceso, text = "Usuario inexistente")
        temp.config(font = "Arial 9 bold",bg="#1C2833", fg="white")
        temp.place(x = USUARIO_X + 70, y = USUARIO_Y + 220)
        temp.after(3000, lambda: temp.destroy())
        
        
        
def click_probar_recup(ventana_recup, entrada_respuesta, registro):
    CLAVE     = 1
    RESPUESTA = 3
    
    respuesta = entrada_respuesta.get("1.0", "end-1c")
  
    if(registro[RESPUESTA] == respuesta):
        temp = Label(ventana_recup, text = "Su clave es: " + registro[CLAVE])
        temp.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
        temp.place(x = USUARIO_X + 50, y = USUARIO_Y + 150)
        temp.after(5000, lambda: temp.destroy())
    else:
        temp = Label(ventana_recup, text = "¡Respuesta incorrecta!")
        temp.config(font = "Arial 11 bold",bg="#1C2833", fg="white")
        temp.place(x = USUARIO_X + 35, y = USUARIO_Y + 150)
        temp.after(2000, lambda: temp.destroy())
        
    
#-------------------------------------VENTANA DE CIFRADO-------------------------------------#
# Autor: Matías Agustín Martínez   
    
def crearVentanaCifrado():
    
    MAIN_Y = 10

    ventana_cifrado = Tk()
    ventana_cifrado.resizable(False,False)
    ventana_cifrado.geometry("400x250")
    ventana_cifrado.title("TP Grupal Parte 1 - Grupo: Supernova")
    ventana_cifrado.iconbitmap("supernova.ico")
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



def click_ventana_cifrado():
    ventana_cifrado = crearVentanaCifrado()
    ventana_cifrado.mainloop()
    
  

#-------------------SECCIÓN MAIN-------------------#

def main():
    ventana_principal = crearVentanaPrincipal()
    ventana_principal.mainloop()
    
main()
