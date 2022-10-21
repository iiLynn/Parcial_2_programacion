# importar las librerias
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
from urllib import parse #Se usan estas dos para correr un server en python
from http.server import HTTPServer, BaseHTTPRequestHandler #Se usan estas dos para correr un server en python

conversor = pd.read_csv("C:\\Users\\kerin\\Desktop\\Parcial_2\\conversor.csv",sep=";")
print (conversor)

# datos de entrada y salida
farenheit = conversor["farenheit "]
kelvin = conversor["kelvin"]

#modelo de entrenamiento
modelo = tf.keras.Sequential()
modelo.add(tf.keras.layers.Dense(units=1,input_shape=[1]))

#compilar el modelo
modelo.compile(optimizer=tf.keras.optimizers.Adam(1), loss='mean_squared_error')

#entrenar el modelo
epocas = modelo.fit(farenheit,kelvin , epochs=250, verbose=1)

# hacer prediciones .. verificar si el resultado es el esperado
f = modelo.predict([-30])
print("Prediccion kelvin a farenheit", f[0][0])

#1. Realizamos la clase del servidor en Python para recibir las peticiones enviadas por AJAX desde la página web.
#Clase para iniciar un servidor en python
class servidorBasico(BaseHTTPRequestHandler):
  def do_GET(self):
    print("Prediccion por GET")
    self.send_response(200)
    self.send_header("Access-Control-Allow-Origin", "*")
    self.end_headers()
    self.wfile.write("Hola Mundo".encode())

  def do_POST(self):
    print("Peticion recibida")
    
    #1. Obtener los datos del cliente / obtener los datos enviados por AJAX
    content_length = int(self.headers['Content-Length'])
    data = self.rfile.read(content_length)
    data = data.decode().replace('pixels=', '')
    data = parse.unquote(data)
    
    #2. Transformamos los datos como las matrices que usamos de MNIST
    #Hacemos las transformaciones necesarias para predecir la imagen
    arr = np.fromstring(data, np.float32, sep = ",")
    arr = arr.reshape(28, 28)
    arr = np.array(arr)
    arr = arr.reshape(1, 28, 28, 1)

    #3. Realizamos la prediccion con nuestra red neuronal
    valor_predicho = modelo.predict(arr, batch_size = 1)
    prediccion = str(np.argmax(valor_predicho))

    #4. Regresamos la respuesta al cliente
    self.send_response(200)
    #5. Evitar problemas de cruce de dominio
    self.send_header("Access-Control-Allow-Origin", "*")
    self.end_headers()
    self.wfile.write(prediccion.encode())

#6. Iniciamos el server en el puerto 3007
print("Iniciando el server en el puerto 3007")
servidor = HTTPServer(("localhost", 3007), servidorBasico)
servidor.serve_forever()