from urllib import parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import usuarios
import comentarios
import detalles

usuarios = usuarios.usuarios()
comentarios = comentarios.comentarios()

detalles = detalles.detalles()

#obtencion de los datoas de entrenamiento
temperaturas = pd.read_csv("dataset.csv", sep=";")

#datos de entrada y salida
celsius = temperaturas["comentario"]
fahrenheit = temperaturas['tipo']

#modelo de entrenamiento
modelo = tf.keras.Sequential()
modelo.add(tf.keras.layers.Dense(units=1, input_shape=[1]))

#compilar el modelo
modelo.compile(optimizer=tf.keras.optimizers.Adam(1),loss='mean_squared_error')

#entrenamiento del modelo
epocas = modelo.fit(celsius, fahrenheit, epochs=100)

class servidorBasico(SimpleHTTPRequestHandler):
    def do_GET(self):
         if self.path == '/':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        
         elif self.path == '/consultar-usuario':
            resp = usuarios.consultar_usuarios()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resp=resp)).encode('utf-8'))

         elif self.path == '/consultar-comentarios':
            resp = comentarios.consultar_comentario()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resp=resp)).encode('utf-8'))

         elif self.path == '/consultar-detalle':
            resp = detalles.consultar_detalle()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resp=resp)).encode('utf-8'))
        
        
         else:
            return SimpleHTTPRequestHandler.do_GET(self)
            
    def do_POST(self):
        print("Peticion recibida")

        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode('utf-8')
        data = parse.unquote(data)
        data = json.loads(data)
        if self.path == '/usuario':
            resp = usuarios.administrar_usuarios(data)
        elif self.path == '/comentarios':
            resp = comentarios.administrar_comentario(data)  
        elif self.path == '/prediccion':
            #Obtener datos de la peticion y limpiar los datos
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data = data.decode()
            data = parse.unquote(data)
            data = float(data)

            #Realizar y obtener la prediccion
            prediction_values = modelo.predict([data])
            print('Prediccion final: ', prediction_values)
            prediction_values = str(prediction_values[0][0])

            #Regresar respuesta a la peticion HTTP
            self.send_response(200)
            #Evitar problemas con CORS
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(prediction_values.encode())
            
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(dict(resp=resp)).encode('utf-8'))

    
#Iniciar el servidor en el puerto 3001 
print("Iniciando el servidor en el puerto 3001")
server = HTTPServer(('localhost', 3001), servidorBasico)
server.serve_forever()