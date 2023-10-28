#Escribir una función que reciba el mensaje a cifrar (cadena de caracteres) y la clave de
#cifrado, y devuelva el mensaje cifrado, mediante el cifrado césar. Probarla utilizando doctest,
#con al menos 10 casos diferentes.

#***********************************************************

def crearRelacion():
    caracter_a_pos = {}
    pos_a_caracter = {}
    
    # Creamos una tabla con los caracteres que pueden desplazarse;
    # en nuestro caso  son sólo los alfanuméricos. La tabla asigna
    # al caracter "a" la posición 0, al "b" la posición 1 y así su-
    # cesivamente hasta llegar a la posición 63, que está asignada
    # al caracter "9". Esta tabla se opera con dos diccionarios, uno
    # que dado un caracter devuelve su posición, y otro que dada una
    # posición devuelve un caracter
    
    digitos    = "0123456789"
    minusculas = "abcdefghijklmnñopqrstuvwxyz"
    mayusculas = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
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
    
if __name__ == "__main__":
    import doctest  
    doctest.testmod()

########################################################################################
#--------------------------------INTERFAZ GRAFICA--------------------------------------#
########################################################################################


from tkinter import *

"""---------FUNCIONES------------"""

def salir():
    ventana.destroy()

def click_continuar():

#--------------------------------INTERFAZ CIFRADO Y DECIFRADO------------------------------------------

    MAIN_Y = 10

    new_ventana = Tk()
    new_ventana.resizable(False,False)
    new_ventana.geometry("400x250")
    new_ventana.title("TP Grupal Parte 1 - Grupo: Supernova")
    new_ventana.config(cursor="hand2")

    #ENTRADA DE TEXTO LABEL Y CASILLA -----SEGUNDA VENTANA-------
            #uso Text para mejor visualizacion del texto

    label_entrada_texto = Label(new_ventana, text="Por favor, introduzca el texto a cifrar:")
    label_entrada_texto.config(font = "Arial 11 bold")
    label_entrada_texto.place(x = 65, y = MAIN_Y)
    entrada_texto = Text(new_ventana,width=40,height=5)#Para obtener todo el texto usamos .get("1.0", "end-1c")
    entrada_texto.place(x = 38, y = MAIN_Y + 30)

    #ENTRADA DE CLAVE PARA CIFRADO CESAR -----SEGUNDA VENTANA-------

    CLAVE_X = 130

    label_entrada_clave = Label(new_ventana, text="Clave (sólo César)")
    label_entrada_clave.place(x = CLAVE_X, y = MAIN_Y + 125)
    clave = IntVar()
    entrada_clave = Entry(new_ventana, textvariable=clave, width = 5)
    entrada_clave.place(x = CLAVE_X + 105, y = MAIN_Y + 125)

    #UNA SOLA FUNCION ENCARGADA DE REDIRIGIR A LAS FUNCIONES DE  CIFRADO Y DECIFRADO -----SEGUNDA VENTANA-------

    def alpresionar(boton):
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
        
        #Llamado de funciones
        
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


    #BOTONES -----SEGUNDA VENTANA-------
    
    BUTTON_WIDTH = 15
    
    TOP_LEFT_X = 75
    TOP_LEFT_Y = MAIN_Y + 170

    btn_cifrado_cesar = Button(new_ventana, text="Cifrar (César)", width = BUTTON_WIDTH, command=lambda: alpresionar("c-cesar"))
    btn_cifrado_cesar.place(x = TOP_LEFT_X, y = TOP_LEFT_Y)

    btn_cifrado_atbash = Button(new_ventana, text="Descifrar (César)", width = BUTTON_WIDTH, command=lambda: alpresionar("d-cesar"))
    btn_cifrado_atbash.place(x = TOP_LEFT_X + 130, y = TOP_LEFT_Y)

    btn_decifrado_cesar = Button(new_ventana, text="Cifrar (Atbash)", width = BUTTON_WIDTH, command=lambda: alpresionar("c-atbash"))
    btn_decifrado_cesar.place(x = TOP_LEFT_X, y = TOP_LEFT_Y + 30)

    btn_decifrado_atbash = Button(new_ventana, text="Descifrar (Atbash)", width = BUTTON_WIDTH, command=lambda: alpresionar("d-atbash"))
    btn_decifrado_atbash.place(x = TOP_LEFT_X + 130, y = TOP_LEFT_Y + 30)

    new_ventana.mainloop()

"""---------VENTANA PRINCIPAL------------"""

ventana = Tk()
ventana.resizable(False,False)
ventana.geometry("400x300")
ventana.title("TP Grupal Parte 1 - Grupo: Supernova")
ventana.config(cursor="hand2",bg="#1C2833")
ventana.iconbitmap("supernova.ico")

#Integrantes ---acerca de------

MAIN_SECTION_Y = 30

texto_bienvenida = "Bienvenido a la aplicación de mensajes secretos del grupo Supernova. Para continuar presione [Continuar]; de lo contrario [Salir]:"
bienvenida = Label(ventana, text = texto_bienvenida, wraplength = 350)
bienvenida.config(font = "Arial 11 bold", bg = "#1C2833", fg = "white")
bienvenida.place(x = 25, y = MAIN_SECTION_Y)

#Boton para acceder a la siguiente ventana ---primera ventana----

btn_continuar = Button(ventana,text="Continuar", command=click_continuar)
btn_continuar.config(width=12 , height=1,font="Arial 10 bold", relief="raised", bd=4)
btn_continuar.place(x=85, y = MAIN_SECTION_Y + 80)

#Boton para salir ----primera ventana----

btn_salir = Button(ventana, text="Salir", command=salir)
btn_salir.config(width=12 , height=1,font="Arial 10 bold", relief="raised", bd=4)
btn_salir.place(x=205, y = MAIN_SECTION_Y + 80)

#Sección de autores

MADE_BY_Y = 200

t_integrantes = Label(ventana, text="Construida por:")
t_integrantes.place(x=140,y = MADE_BY_Y)
t_integrantes.config(font="Arial 11 bold",bg="#1C2833",fg="white")

text_integrantes = "Matias Agustin Martinez, Josue Daniel Arturo Segura Valer, Bryan Hernán Serrantes Ochoa, Lucas Ezequiel Zenobio, Federico Aguilar "
integrantes = Label(ventana, text=text_integrantes, wraplength=280)
integrantes.config(bg="#1C2833", fg="white")
integrantes.place(x=65,y = MADE_BY_Y + 20)



ventana.mainloop()
    

    