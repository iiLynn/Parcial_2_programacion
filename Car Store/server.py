from http.server import HTTPServer, SimpleHTTPRequestHandler


class servidorBasico(SimpleHTTPRequestHandler):
    def do_GET(self):
         if self.path=="/":
            self.path = "/Menu.html"
         return SimpleHTTPRequestHandler.do_GET(self)
    
#Iniciar el servidor en el puerto 3001 
print("Iniciando el servidor en el puerto 3001")
server = HTTPServer(('localhost',3001), servidorBasico)
server.serve_forever()