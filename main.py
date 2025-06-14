import groq
import streamlit as st
#List           0                    1                  2
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192','mixtral-8x7b-32768']
#Modelos de IA que nos ofrece Groq.

#CONFIGURAR PÁGINA
def configurar_página():
 st.set_page_config(page_title="Mi primer Chatbot con Python" , page_icon="😼")
 st.title('Chatvalen')
 nombre = st.text_input ("¿Cuál es tu nombre chaval?")
 click = st.button("Saludar")
 if click:
    st.write(f'Hola {nombre}. Saludos desde TTT')
 
#CREAR UN CLIENTE GROQ
def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=groq_api_key)

#MOSTRAR LA BARRA LATERAL
def mostrar_sidebar():
  st.sidebar.title("Elegí tu modelo de IA favorito")
  modelo = st.sidebar.selectbox('', MODELOS, index=0)
  st.write(f'**Elegiste el modelo** {modelo}')
  return modelo
#Se desplegan opciones.

#INICIALIZAR EL ESTADO DEL CHAT
#streamlit => variable especial llamada session_state. {mensajes => []} almacenar todos nuestros mensajes, q en realidad es una lista[] q almacena datos
def inicializar_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [generar_contexto_piola()]
#si mensajes no existe en la session_state, creala.

#MOSTRAR MENSAJES PREVIOS, permite mostrar los mensajes anteriores en el chat.
def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes: 
         if mensaje["role"] in ("user", "assistant"): #con este bucle recorremos los mensajes de st.session_state.mensaje
          with st.chat_message(mensaje["role"]): #quien lo envia ?? corte, si es el user o la IA.
             st.markdown(mensaje["content"]) #que envia? el contenido del mensaje.

#OBTENER MENSAJE USUARIO
def obtener_mensaje_usuario():
    return st.chat_input("Envia tu mensaje")

#GUARDAR LOS MENSAJES
def agregar_mensajes_previos(role, content):
    st.session_state.mensajes.append({"role": role , "content": content})

#MOSTRAR LOS MENSAJES EN PANTALLA
def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)


#CREACION DEL MODELO DE GROQ
def obtener_respuesta_modelo(cliente, modelo, mensaje):
    respuesta =  cliente.chat.completions.create(
        model = modelo,
        messages = mensaje,
        stream= False
    )
    return respuesta.choices[0].message.content

def ejecutar_chat():
    configurar_página()
    cliente = crear_cliente_groq()
    modelo = mostrar_sidebar()
    
    inicializar_estado_chat()
    mensaje_usuario = obtener_mensaje_usuario()
    obtener_mensajes_previos()
    
    if mensaje_usuario:
        agregar_mensajes_previos("user",mensaje_usuario)
        mostrar_mensaje("user",mensaje_usuario)
    
        respuesta_contenido = obtener_respuesta_modelo(cliente, modelo,st.session_state.mensajes )

        agregar_mensajes_previos("assistant",respuesta_contenido)
        mostrar_mensaje("assistant",respuesta_contenido)

def generar_contexto_piola():
    return {
        "role": "system",
        "content": (
            "Soy Valentina, puedes llamarme Valu, Vali, Valenchu, chavalita, o cualquier apodo bonito."
            "Mi mejor amiga es Camila y tengo 2 perritos, Rocco y Luna."
        )
    }

    
#si esto es igual a esto, se ejecuta, sino no se ejecuta.
#streamlit run main.py

if __name__ == '__main__':
 ejecutar_chat()
