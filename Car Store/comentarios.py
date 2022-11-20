import conexion

db = conexion.conexion()

class comentarios:
    def consultar_comentario(self):
        sql = "SELECT * FROM comentario"
        return db.consultar(sql)

    def administrar_comentario(self, contenido):
        try:
            if contenido["accion"]=="nuevo":
                sql = "INSERT INTO comentario (texto, id_usuarios, id_res, tipo_comentario, nombre) VALUES (%s, %s, %s, %s, %s)"
                val = (contenido["texto"], contenido["id_usuarios"], contenido["id_res"], contenido["tipo_comentario"], contenido["nombre"])

            elif contenido["accion"]=="modificar":
                sql = "UPDATE alumnos SET codigo=%s, nombre=%s, telefono=%s WHERE idAlumno=%s"
                val = (contenido["codigo"], contenido["nombre"], contenido["telefono"], contenido["idAlumno"])

            elif contenido["accion"]=="eliminar":
                sql = "DELETE FROM alumnos WHERE idAlumno=%s"
                val = (contenido["idAlumno"],)

            return db.ejecutar_consulta(sql, val)
        except Exception as e:
            return str(e)