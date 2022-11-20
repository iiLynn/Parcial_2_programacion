import conexion

db = conexion.conexion()

class usuarios:
    def consultar_usuarios(self):
        sql = "SELECT * FROM usuario"
        return db.consultar(sql)

    def administrar_usuarios(self, contenido):
        try:
            if contenido["accion"]=="nuevo":
                sql = "INSERT INTO usuario (nombre, apellido, correo, contra, direccion) VALUES (%s, %s, %s, %s, %s)"
                val = (contenido["nombre"], contenido["apellido"], contenido["correo"], contenido["contra"], contenido["direccion"])

            elif contenido["accion"]=="modificar":
                sql = "UPDATE usuario SET nombre=%s, apellido=%s, correo=%s, contra=%s, direccion=%s WHERE id_usuarios=%s"
                val = (contenido["nombre"], contenido["apellido"], contenido["correo"], contenido["contra"], contenido["direccion"], contenido["id_usuarios"])

            elif contenido["accion"]=="eliminar":
                sql = "DELETE FROM alumnos WHERE idUsuario=%s"
                val = (contenido["idUsuario"],)

            return db.ejecutar_consulta(sql, val)
        except Exception as e:
            return str(e)