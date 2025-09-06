import os
from datetime import datetime

class Usuario:
    def __init__(self, id_usuario, nombre):
        self.id_usuario = id_usuario
        self.nombre = nombre
    
    def __str__(self):
        return f"ID: {self.id_usuario}, Nombre: {self.nombre}"

class Libro:
    def __init__(self, id_libro, titulo):
        self.id_libro = id_libro
        self.titulo = titulo
    
    def __str__(self):
        return f"ID: {self.id_libro}, Título: {self.titulo}"

class Prestamo:
    def __init__(self, id_usuario, nombre_usuario, id_libro, titulo_libro, fecha_prestamo, fecha_devolucion=""):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.id_libro = id_libro
        self.titulo_libro = titulo_libro
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
    
    def __str__(self):
        return f"Usuario: {self.nombre_usuario}, Libro: {self.titulo_libro}, Fecha: {self.fecha_prestamo}"

class BibliotecaDigital:
    def __init__(self):
        self.usuarios = {}  # diccionario para almacenar usuarios por ID
        self.libros = {}    # diccionario para almacenar libros por ID
        self.prestamos = [] # lista para todos los préstamos
        self.errores_lectura = [] # para almacenar errores de formato
    
    def es_fecha_valida(self, fecha):
        """Valida que la fecha tenga formato YYYY-MM-DD"""
        if len(fecha) != 10:
            return False
        if fecha[4] != '-' or fecha[7] != '-':
            return False
        
        # Verificar que año, mes y día sean números
        try:
            año = int(fecha[:4])
            mes = int(fecha[5:7])
            dia = int(fecha[8:10])
            
            # Validaciones básicas
            if mes < 1 or mes > 12:
                return False
            if dia < 1 or dia > 31:
                return False
            if año < 1900 or año > 2030:
                return False
            
            return True
        except ValueError:
            return False
    
    def es_numero_valido(self, texto):
        """Verifica si el texto es un número válido"""
        if not texto:
            return False
        for char in texto:
            if char < '0' or char > '9':
                return False
        return True
    
    def validar_caracteres_texto(self, texto):
        """Valida caracteres permitidos en nombres y títulos"""
        caracteres_permitidos = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 áéíóúÁÉÍÓÚñÑ.,;:-_()"
        for i, char in enumerate(texto):
            if char not in caracteres_permitidos:
                return False, i, char
        return True, -1, ""
    
    def cargar_usuarios(self):
        """Carga usuarios desde archivo de texto"""
        nombre_archivo = input("Ingrese el nombre del archivo de usuarios: ")
        
        if not os.path.exists(nombre_archivo):
            print(f"Error: El archivo '{nombre_archivo}' no existe.")
            return
        
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                linea_num = 0
                usuarios_cargados = 0
                
                for linea in archivo:
                    linea_num += 1
                    linea = linea.strip()
                    
                    if not linea:  # saltar líneas vacías
                        continue
                    
                    # Buscar el separador (,)
                    partes = []
                    parte_actual = ""
                    
                    for char in linea:
                        if char == ',':
                            partes.append(parte_actual.strip())
                            parte_actual = ""
                        else:
                            parte_actual += char
                    partes.append(parte_actual.strip())
                    
                    if len(partes) != 2:
                        print(f"Error línea {linea_num}: Formato incorrecto. Se esperaban 2 campos separados por coma.")
                        continue
                    
                    id_usuario, nombre = partes[0], partes[1]
                    
                    # Validar ID de usuario
                    if not self.es_numero_valido(id_usuario):
                        print(f"Error línea {linea_num}: ID de usuario inválido '{id_usuario}'")
                        continue
                    
                    # Validar nombre
                    es_valido, pos, char = self.validar_caracteres_texto(nombre)
                    if not es_valido:
                        print(f"Error línea {linea_num}, posición {pos}: Carácter inválido '{char}' en nombre")
                        continue
                    
                    # Agregar usuario
                    self.usuarios[id_usuario] = Usuario(id_usuario, nombre)
                    usuarios_cargados += 1
                
                print(f"Se cargaron {usuarios_cargados} usuarios correctamente.")
        
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
    
    def cargar_libros(self):
        """Carga libros desde archivo de texto"""
        nombre_archivo = input("Ingrese el nombre del archivo de libros: ")
        
        if not os.path.exists(nombre_archivo):
            print(f"Error: El archivo '{nombre_archivo}' no existe.")
            return
        
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                linea_num = 0
                libros_cargados = 0
                
                for linea in archivo:
                    linea_num += 1
                    linea = linea.strip()
                    
                    if not linea:
                        continue
                    
                    # Separar por coma
                    partes = []
                    parte_actual = ""
                    
                    for char in linea:
                        if char == ',':
                            partes.append(parte_actual.strip())
                            parte_actual = ""
                        else:
                            parte_actual += char
                    partes.append(parte_actual.strip())
                    
                    if len(partes) != 2:
                        print(f"Error línea {linea_num}: Formato incorrecto. Se esperaban 2 campos separados por coma.")
                        continue
                    
                    id_libro, titulo = partes[0], partes[1]
                    
                    # Validar ID de libro
                    if not self.es_numero_valido(id_libro):
                        print(f"Error línea {linea_num}: ID de libro inválido '{id_libro}'")
                        continue
                    
                    # Validar título
                    es_valido, pos, char = self.validar_caracteres_texto(titulo)
                    if not es_valido:
                        print(f"Error línea {linea_num}, posición {pos}: Carácter inválido '{char}' en título")
                        continue
                    
                    # Agregar libro
                    self.libros[id_libro] = Libro(id_libro, titulo)
                    libros_cargados += 1
                
                print(f"Se cargaron {libros_cargados} libros correctamente.")
        
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
    
    def cargar_prestamos(self):
        """Carga préstamos desde archivo .lfa"""
        nombre_archivo = input("Ingrese el nombre del archivo de préstamos (.lfa): ")
        
        if not os.path.exists(nombre_archivo):
            print(f"Error: El archivo '{nombre_archivo}' no existe.")
            return
        
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                linea_num = 0
                prestamos_cargados = 0
                
                for linea in archivo:
                    linea_num += 1
                    linea = linea.strip()
                    
                    if not linea:
                        continue
                    
                    # Separar campos por coma
                    campos = []
                    campo_actual = ""
                    
                    for char in linea:
                        if char == ',':
                            campos.append(campo_actual.strip())
                            campo_actual = ""
                        else:
                            campo_actual += char
                    campos.append(campo_actual.strip())
                    
                    if len(campos) != 6:
                        print(f"Error línea {linea_num}: Se esperaban 6 campos, se encontraron {len(campos)}")
                        continue
                    
                    id_usuario, nombre_usuario, id_libro, titulo_libro, fecha_prestamo, fecha_devolucion = campos
                    
                    # Validar ID de usuario
                    if not self.es_numero_valido(id_usuario):
                        print(f"Error línea {linea_num}: ID de usuario inválido '{id_usuario}'")
                        continue
                    
                    # Validar ID de libro
                    if not self.es_numero_valido(id_libro):
                        print(f"Error línea {linea_num}: ID de libro inválido '{id_libro}'")
                        continue
                    
                    # Verificar que usuario existe en catálogo
                    if id_usuario not in self.usuarios:
                        print(f"Error línea {linea_num}: Usuario con ID '{id_usuario}' no existe en el catálogo")
                        continue
                    
                    # Verificar que libro existe en catálogo
                    if id_libro not in self.libros:
                        print(f"Error línea {linea_num}: Libro con ID '{id_libro}' no existe en el catálogo")
                        continue
                    
                    # Validar nombres/títulos
                    es_valido, pos, char = self.validar_caracteres_texto(nombre_usuario)
                    if not es_valido:
                        print(f"Error línea {linea_num}, posición {pos}: Carácter inválido '{char}' en nombre de usuario")
                        continue
                    
                    es_valido, pos, char = self.validar_caracteres_texto(titulo_libro)
                    if not es_valido:
                        print(f"Error línea {linea_num}, posición {pos}: Carácter inválido '{char}' en título de libro")
                        continue
                    
                    # Validar fecha de préstamo
                    if not self.es_fecha_valida(fecha_prestamo):
                        print(f"Error línea {linea_num}: Fecha de préstamo inválida '{fecha_prestamo}'")
                        continue
                    
                    # Validar fecha de devolución (si no está vacía)
                    if fecha_devolucion and not self.es_fecha_valida(fecha_devolucion):
                        print(f"Error línea {linea_num}: Fecha de devolución inválida '{fecha_devolucion}'")
                        continue
                    
                    # Crear préstamo
                    prestamo = Prestamo(id_usuario, nombre_usuario, id_libro, titulo_libro, fecha_prestamo, fecha_devolucion)
                    self.prestamos.append(prestamo)
                    prestamos_cargados += 1
                
                print(f"Se cargaron {prestamos_cargados} préstamos correctamente.")
        
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
    
    def mostrar_historial_prestamos(self):
        """Muestra todos los préstamos registrados"""
        if not self.prestamos:
            print("No hay préstamos registrados.")
            return
        
        print("\n=== HISTORIAL DE PRÉSTAMOS ===")
        print(f"{'ID Usuario':<10} {'Nombre Usuario':<20} {'ID Libro':<10} {'Título Libro':<25} {'Fecha Préstamo':<15} {'Fecha Devolución':<15}")
        print("-" * 120)
        
        for prestamo in self.prestamos:
            devolucion = prestamo.fecha_devolucion if prestamo.fecha_devolucion else "No devuelto"
            print(f"{prestamo.id_usuario:<10} {prestamo.nombre_usuario:<20} {prestamo.id_libro:<10} {prestamo.titulo_libro:<25} {prestamo.fecha_prestamo:<15} {devolucion:<15}")
    
    def mostrar_usuarios_unicos(self):
        """Muestra lista de usuarios únicos que han realizado préstamos"""
        if not self.prestamos:
            print("No hay préstamos registrados.")
            return
        
        usuarios_unicos = {}
        for prestamo in self.prestamos:
            if prestamo.id_usuario not in usuarios_unicos:
                usuarios_unicos[prestamo.id_usuario] = prestamo.nombre_usuario
        
        print("\n=== LISTADO DE USUARIOS ÚNICOS ===")
        print(f"{'ID Usuario':<12} {'Nombre Usuario':<30}")
        print("-" * 45)
        
        for id_usuario, nombre in usuarios_unicos.items():
            print(f"{id_usuario:<12} {nombre:<30}")
    
    def mostrar_libros_prestados(self):
        """Muestra lista de libros que han sido prestados, sin duplicados"""
        if not self.prestamos:
            print("No hay préstamos registrados.")
            return
        
        libros_prestados = {}
        for prestamo in self.prestamos:
            if prestamo.id_libro not in libros_prestados:
                libros_prestados[prestamo.id_libro] = prestamo.titulo_libro
        
        print("\n=== LISTADO DE LIBROS PRESTADOS ===")
        print(f"{'ID Libro':<10} {'Título del Libro':<40}")
        print("-" * 55)
        
        for id_libro, titulo in libros_prestados.items():
            print(f"{id_libro:<10} {titulo:<40}")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas generales de préstamos"""
        if not self.prestamos:
            print("No hay préstamos registrados.")
            return
        
        # Total de préstamos
        total_prestamos = len(self.prestamos)
        
        # Usuarios únicos
        usuarios_unicos = set()
        for prestamo in self.prestamos:
            usuarios_unicos.add(prestamo.id_usuario)
        total_usuarios = len(usuarios_unicos)
        
        # Libro más prestado
        contador_libros = {}
        for prestamo in self.prestamos:
            if prestamo.id_libro in contador_libros:
                contador_libros[prestamo.id_libro] += 1
            else:
                contador_libros[prestamo.id_libro] = 1
        
        libro_mas_prestado = ""
        max_prestamos = 0
        for id_libro, cantidad in contador_libros.items():
            if cantidad > max_prestamos:
                max_prestamos = cantidad
                # Buscar el título del libro
                for prestamo in self.prestamos:
                    if prestamo.id_libro == id_libro:
                        libro_mas_prestado = prestamo.titulo_libro
                        break
        
        # Usuario más activo
        contador_usuarios = {}
        for prestamo in self.prestamos:
            if prestamo.id_usuario in contador_usuarios:
                contador_usuarios[prestamo.id_usuario] += 1
            else:
                contador_usuarios[prestamo.id_usuario] = 1
        
        usuario_mas_activo = ""
        max_actividad = 0
        for id_usuario, cantidad in contador_usuarios.items():
            if cantidad > max_actividad:
                max_actividad = cantidad
                # Buscar el nombre del usuario
                for prestamo in self.prestamos:
                    if prestamo.id_usuario == id_usuario:
                        usuario_mas_activo = prestamo.nombre_usuario
                        break
        
        print("\n=== ESTADÍSTICAS DE PRÉSTAMOS ===")
        print(f"Total de préstamos: {total_prestamos}")
        print(f"Total de usuarios únicos: {total_usuarios}")
        print(f"Libro más prestado: {libro_mas_prestado} ({max_prestamos} veces)")
        print(f"Usuario más activo: {usuario_mas_activo} ({max_actividad} préstamos)")
    
    def mostrar_prestamos_vencidos(self):
        """Muestra préstamos vencidos (fecha de devolución pasada y no devueltos)"""
        if not self.prestamos:
            print("No hay préstamos registrados.")
            return
        
        # Obtener fecha actual
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
        prestamos_vencidos = []
        for prestamo in self.prestamos:
            # Si no tiene fecha de devolución, significa que no ha sido devuelto
            # y si tiene fecha de devolución pero es anterior a hoy, está vencido
            if not prestamo.fecha_devolucion:
                prestamos_vencidos.append(prestamo)
            elif prestamo.fecha_devolucion < fecha_actual:
                prestamos_vencidos.append(prestamo)
        
        if not prestamos_vencidos:
            print("No hay préstamos vencidos.")
            return
        
        print("\n=== PRÉSTAMOS VENCIDOS ===")
        print(f"{'ID Usuario':<10} {'Nombre Usuario':<20} {'ID Libro':<10} {'Título Libro':<25} {'Fecha Préstamo':<15} {'Fecha Devolución':<15}")
        print("-" * 120)
        
        for prestamo in prestamos_vencidos:
            devolucion = prestamo.fecha_devolucion if prestamo.fecha_devolucion else "No especificada"
            print(f"{prestamo.id_usuario:<10} {prestamo.nombre_usuario:<20} {prestamo.id_libro:<10} {prestamo.titulo_libro:<25} {prestamo.fecha_prestamo:<15} {devolucion:<15}")
    
    def generar_html_historial(self):
        """Genera HTML para el historial de préstamos"""
        html = """
        <h2>Historial de Préstamos</h2>
        <table border='1' style='border-collapse: collapse; width: 100%;'>
        <tr>
            <th>ID Usuario</th>
            <th>Nombre Usuario</th>
            <th>ID Libro</th>
            <th>Título Libro</th>
            <th>Fecha Préstamo</th>
            <th>Fecha Devolución</th>
        </tr>
        """
        
        for prestamo in self.prestamos:
            devolucion = prestamo.fecha_devolucion if prestamo.fecha_devolucion else "No devuelto"
            html += f"""
        <tr>
            <td>{prestamo.id_usuario}</td>
            <td>{prestamo.nombre_usuario}</td>
            <td>{prestamo.id_libro}</td>
            <td>{prestamo.titulo_libro}</td>
            <td>{prestamo.fecha_prestamo}</td>
            <td>{devolucion}</td>
        </tr>
            """
        
        html += "</table>\n"
        return html
    
    def generar_html_usuarios(self):
        """Genera HTML para usuarios únicos"""
        usuarios_unicos = {}
        for prestamo in self.prestamos:
            if prestamo.id_usuario not in usuarios_unicos:
                usuarios_unicos[prestamo.id_usuario] = prestamo.nombre_usuario
        
        html = """
        <h2>Listado de Usuarios Únicos</h2>
        <table border='1' style='border-collapse: collapse; width: 100%;'>
        <tr>
            <th>ID Usuario</th>
            <th>Nombre Usuario</th>
        </tr>
        """
        
        for id_usuario, nombre in usuarios_unicos.items():
            html += f"""
        <tr>
            <td>{id_usuario}</td>
            <td>{nombre}</td>
        </tr>
            """
        
        html += "</table>\n"
        return html
    
    def generar_html_libros(self):
        """Genera HTML para libros prestados"""
        libros_prestados = {}
        for prestamo in self.prestamos:
            if prestamo.id_libro not in libros_prestados:
                libros_prestados[prestamo.id_libro] = prestamo.titulo_libro
        
        html = """
        <h2>Listado de Libros Prestados</h2>
        <table border='1' style='border-collapse: collapse; width: 100%;'>
        <tr>
            <th>ID Libro</th>
            <th>Título del Libro</th>
        </tr>
        """
        
        for id_libro, titulo in libros_prestados.items():
            html += f"""
        <tr>
            <td>{id_libro}</td>
            <td>{titulo}</td>
        </tr>
            """
        
        html += "</table>\n"
        return html
    
    def generar_html_estadisticas(self):
        """Genera HTML para estadísticas"""
        if not self.prestamos:
            return "<h2>Estadísticas de Préstamos</h2><p>No hay datos disponibles.</p>\n"
        
        # Calcular estadísticas (mismo código que mostrar_estadisticas)
        total_prestamos = len(self.prestamos)
        
        usuarios_unicos = set()
        for prestamo in self.prestamos:
            usuarios_unicos.add(prestamo.id_usuario)
        total_usuarios = len(usuarios_unicos)
        
        contador_libros = {}
        for prestamo in self.prestamos:
            if prestamo.id_libro in contador_libros:
                contador_libros[prestamo.id_libro] += 1
            else:
                contador_libros[prestamo.id_libro] = 1
        
        libro_mas_prestado = ""
        max_prestamos = 0
        for id_libro, cantidad in contador_libros.items():
            if cantidad > max_prestamos:
                max_prestamos = cantidad
                for prestamo in self.prestamos:
                    if prestamo.id_libro == id_libro:
                        libro_mas_prestado = prestamo.titulo_libro
                        break
        
        contador_usuarios = {}
        for prestamo in self.prestamos:
            if prestamo.id_usuario in contador_usuarios:
                contador_usuarios[prestamo.id_usuario] += 1
            else:
                contador_usuarios[prestamo.id_usuario] = 1
        
        usuario_mas_activo = ""
        max_actividad = 0
        for id_usuario, cantidad in contador_usuarios.items():
            if cantidad > max_actividad:
                max_actividad = cantidad
                for prestamo in self.prestamos:
                    if prestamo.id_usuario == id_usuario:
                        usuario_mas_activo = prestamo.nombre_usuario
                        break
        
        html = f"""
        <h2>Estadísticas de Préstamos</h2>
        <table border='1' style='border-collapse: collapse; width: 100%;'>
        <tr>
            <th>Métrica</th>
            <th>Valor</th>
        </tr>
        <tr>
            <td>Total de préstamos</td>
            <td>{total_prestamos}</td>
        </tr>
        <tr>
            <td>Total de usuarios únicos</td>
            <td>{total_usuarios}</td>
        </tr>
        <tr>
            <td>Libro más prestado</td>
            <td>{libro_mas_prestado} ({max_prestamos} veces)</td>
        </tr>
        <tr>
            <td>Usuario más activo</td>
            <td>{usuario_mas_activo} ({max_actividad} préstamos)</td>
        </tr>
        </table>
        """
        
        return html
    
    def generar_html_vencidos(self):
        """Genera HTML para préstamos vencidos"""
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
        prestamos_vencidos = []
        for prestamo in self.prestamos:
            if not prestamo.fecha_devolucion:
                prestamos_vencidos.append(prestamo)
            elif prestamo.fecha_devolucion < fecha_actual:
                prestamos_vencidos.append(prestamo)
        
        html = """
        <h2>Préstamos Vencidos</h2>
        <table border='1' style='border-collapse: collapse; width: 100%;'>
        <tr>
            <th>ID Usuario</th>
            <th>Nombre Usuario</th>
            <th>ID Libro</th>
            <th>Título Libro</th>
            <th>Fecha Préstamo</th>
            <th>Fecha Devolución</th>
        </tr>
        """
        
        for prestamo in prestamos_vencidos:
            devolucion = prestamo.fecha_devolucion if prestamo.fecha_devolucion else "No especificada"
            html += f"""
        <tr>
            <td>{prestamo.id_usuario}</td>
            <td>{prestamo.nombre_usuario}</td>
            <td>{prestamo.id_libro}</td>
            <td>{prestamo.titulo_libro}</td>
            <td>{prestamo.fecha_prestamo}</td>
            <td>{devolucion}</td>
        </tr>
            """
        
        html += "</table>\n"
        return html
    
    def exportar_reportes_html(self):
        """Exporta todos los reportes a un archivo HTML"""
        if not self.prestamos:
            print("No hay datos para exportar.")
            return
        
        nombre_archivo = input("Ingrese el nombre del archivo HTML (ej: reportes.html): ")
        
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                # Encabezado HTML
                archivo.write("""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reportes - Biblioteca Digital</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #2c3e50; text-align: center; }
        h2 { color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 5px; }
        table { margin-bottom: 30px; }
        th { background-color: #3498db; color: white; padding: 10px; }
        td { padding: 8px; }
        tr:nth-child(even) { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Reportes de Biblioteca Digital</h1>
""")
                
                # Generar cada reporte
                archivo.write(self.generar_html_historial())
                archivo.write(self.generar_html_usuarios())
                archivo.write(self.generar_html_libros())
                archivo.write(self.generar_html_estadisticas())
                archivo.write(self.generar_html_vencidos())
                
                # Cerrar HTML
                archivo.write("""
</body>
</html>
""")
            
            print(f"Reportes exportados exitosamente a '{nombre_archivo}'")
        
        except Exception as e:
            print(f"Error al exportar reportes: {e}")

def main():
    biblioteca = BibliotecaDigital()
    
    while True:
        print("\n" + "="*50)
        print("    SISTEMA DE BIBLIOTECA DIGITAL")
        print("="*50)
        print("1. Cargar usuarios")
        print("2. Cargar libros") 
        print("3. Cargar registro de préstamos desde archivo")
        print("4. Mostrar historial de préstamos")
        print("5. Mostrar listado de usuarios únicos")
        print("6. Mostrar listado de libros prestados")
        print("7. Mostrar estadísticas de préstamos")
        print("8. Mostrar préstamos vencidos")
        print("9. Exportar todos los reportes a HTML")
        print("10. Salir")
        print("="*50)
        
        try:
            opcion = input("Seleccione una opción (1-10): ").strip()
            
            if opcion == "1":
                biblioteca.cargar_usuarios()
            elif opcion == "2":
                biblioteca.cargar_libros()
            elif opcion == "3":
                biblioteca.cargar_prestamos()
            elif opcion == "4":
                biblioteca.mostrar_historial_prestamos()
            elif opcion == "5":
                biblioteca.mostrar_usuarios_unicos()
            elif opcion == "6":
                biblioteca.mostrar_libros_prestados()
            elif opcion == "7":
                biblioteca.mostrar_estadisticas()
            elif opcion == "8":
                biblioteca.mostrar_prestamos_vencidos()
            elif opcion == "9":
                biblioteca.exportar_reportes_html()
            elif opcion == "10":
                print("¡Gracias por usar el Sistema de Biblioteca Digital!")
                break
            else:
                print("Opción inválida. Por favor seleccione una opción del 1 al 10.")
        
        except KeyboardInterrupt:
            print("\n\n¡Programa interrumpido por el usuario!")
            break
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
