import os
import datetime
import re

class Token:
    def __init__(self, tipo, lexema, linea, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f"Token({self.tipo}, '{self.lexema}', {self.linea}, {self.columna})"

class AnalizadorLexico:
    def __init__(self):
        
        self.tokens_def = [
            # 1. PALABRAS RESERVADAS
            ('OPERACION', r'Operacion'),
            ('NUMERO_KW', r'Numero'),
            
            # 2. OPERACIONES ARITMETICAS 
            ('SUMA', r'SUMA|suma'),
            ('RESTA', r'RESTA|resta'),
            ('MULTIPLICACION', r'MULTIPLICACION|multiplicacion'),
            ('DIVISION', r'DIVISION|division'),
            ('POTENCIA', r'POTENCIA|potencia'),
            ('RAIZ', r'RAIZ|raiz'),
            ('INVERSO', r'INVERSO|inverso'),
            ('MOD', r'MOD|mod'),
            ('P', r'P'),
            ('R', r'R'),
            
            # 3. VALORES NUMERICOS
            ('NUMBER', r'\d+(\.\d+)?'),
            
            # 4. SIMBOLOS INDIVIDUALES 
            ('OPEN_TAG', r'<'),
            ('CLOSE_TAG', r'>'),
            ('SLASH', r'/'),
            ('EQUALS', r'='),
        ]
        
        # mis expresiones regulares
        self.patrones = []
        for nombre, patron in self.tokens_def:
            self.patrones.append((nombre, re.compile(patron)))

    def analizar(self, codigo):
        tokens = []
        errores = []
        linea = 1
        columna = 1
        pos = 0
        total_caracteres = len(codigo)

        while pos < total_caracteres:
            # Saltar espacios en blanco
            if codigo[pos] in ' \t':
                columna += 1
                pos += 1
                continue
            
            # Saltar saltos de linea
            if codigo[pos] == '\n':
                linea += 1
                columna = 1
                pos += 1
                continue

            # Intentar hacer que me cuadren match con cada patron 
            match_encontrado = False
            for nombre, patron in self.patrones:
                match = patron.match(codigo, pos)
                if match:
                    lexema = match.group()
                    tokens.append(Token(nombre, lexema, linea, columna))
                    columna += len(lexema)
                    pos = match.end()
                    match_encontrado = True
                    break

            # Si no hubo match, es un error lexico
            if not match_encontrado:
                # Caracter individual no reconocido
                char = codigo[pos]
                errores.append({
                    'lexema': char,
                    'linea': linea,
                    'columna': columna,
                    'tipo': 'Error Lexico'
                })
                columna += 1
                pos += 1

        return tokens, errores

class GeneradorHTML:
    @staticmethod
    def generar_reporte_tokens(tokens, nombre_archivo):
        """Genera reporte HTML de tokens encontrados"""
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Reporte de Tokens - {nombre_archivo}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .info {{
            background: #d4edda;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 5px solid #28a745;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #34495e;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e3f2fd;
        }}
        .timestamp {{
            text-align: right;
            color: #6c757d;
            font-style: italic;
            margin-top: 20px;
        }}
        .token-count {{
            background: #007bff;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: bold;
        }}
        .success {{
            background: #28a745;
            color: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1> Reporte de Tokens </h1>
        
        <div class="info">
            <strong> Archivo analizado:</strong> {nombre_archivo}<br>
            <strong> Total de tokens:</strong> <span class="token-count">{len(tokens)}</span><br>
            <strong> Orden corregido:</strong> Palabras completas  Simbolos individuales
        </div>
        
        <div class="success">
            ...
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Tipo de Token</th>
                    <th>Lexema</th>
                    <th>Linea</th>
                    <th>Columna</th>
                </tr>
            </thead>
            <tbody>"""
        
        for i, token in enumerate(tokens, 1):
            html += f"""
                <tr>
                    <td>{i}</td>
                    <td><strong>{token.tipo}</strong></td>
                    <td><code>{token.lexema}</code></td>
                    <td>{token.linea}</td>
                    <td>{token.columna}</td>
                </tr>"""
        
        html += f"""
            </tbody>
        </table>
        
        <div class="timestamp">
             Generado el: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>"""
        
        return html

    @staticmethod
    def generar_reporte_errores(errores, nombre_archivo):
        """Genera reporte HTML de errores encontrados"""
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Reporte de Errores - {nombre_archivo}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #dc3545;
            text-align: center;
            border-bottom: 3px solid #dc3545;
            padding-bottom: 10px;
        }}
        .info {{
            background: #f8d7da;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 5px solid #dc3545;
        }}
        .no-errors {{
            background: #d4edda;
            padding: 30px;
            border-radius: 5px;
            text-align: center;
            border-left: 5px solid #28a745;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #dc3545;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #ffe6e6;
        }}
        .error-count {{
            background: #dc3545;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: bold;
        }}
        .timestamp {{
            text-align: right;
            color: #6c757d;
            font-style: italic;
            margin-top: 20px;
        }}
        .fixed-info {{
            background: #d1ecf1;
            color: #0c5460;
            padding: 15px;
            border-radius: 5px;
            border-left: 5px solid #17a2b8;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1> Reporte de Errores </h1>
        
        <div class="fixed-info">
    
        
        </div>"""
        
        if not errores:
            html += f"""
            <div class="no-errors">
                <h2> ANALISIS EXITOSO!</h2>
                <p>El archivo <strong>{nombre_archivo}</strong> fue analizado sin errores.</p>
                <p><strong>Correccion aplicada:</strong>.</p>
            </div>"""
        else:
            html += f"""
            <div class="info">
                <strong> Archivo analizado:</strong> {nombre_archivo}<br>
                <strong> Total de errores:</strong> <span class="error-count">{len(errores)}</span><br>
                <strong> Estos son errores:</strong> Caracteres no validos en el lenguaje
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Linea</th>
                        <th>Columna</th>
                        <th>Lexema No Valido</th>
                        <th>Tipo de Error</th>
                    </tr>
                </thead>
                <tbody>"""
            
            for i, error in enumerate(errores, 1):
                html += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{error['linea']}</td>
                        <td>{error['columna']}</td>
                        <td><strong><code>"{error['lexema']}"</code></strong></td>
                        <td>{error['tipo']}</td>
                    </tr>"""
            
            html += """
                </tbody>
            </table>"""
        
        html += f"""
        <div class="timestamp">
             Generado el: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>"""
        
        return html

def main():
    """Funcion principal del analizador lexico """
    
    print("ANALIZADOR LEXICO ")
    print("="*70)
    print("............")
    print(" ............")
    print("="*70)
    
    while True:
        print("\nOpciones:")
        print("1. Analizar archivo")
        print("2. Salir")
        
        opcion = input("\nSeleccione una opcion (1-2): ").strip()
        
        if opcion == "1":
            analizar_archivo()
        elif opcion == "2":
            print("todo bien")
            break
        else:
            print(" Opcion no valida. Intente nuevamente.")

def analizar_archivo():
    """Funcion para analizar un archivo especifico"""
    
    archivo_path = input("\n Ingrese la ruta del archivo .txt a analizar: ").strip()
    
    if not os.path.exists(archivo_path):
        print(" Error: El archivo no existe.")
        return
    
    if not archivo_path.lower().endswith('.txt'):
        print(" Error: El archivo debe tener extension .txt")
        return
    
    try:
        with open(archivo_path, 'r', encoding='utf-8') as file:
            codigo = file.read()
        
        print(f"\n Leyendo archivo: {os.path.basename(archivo_path)}")
        print("    ORDEN : Palabras completas  Simbolos individuales")
        
        analizador = AnalizadorLexico()
        print(" Analizando codigo...")
        
        tokens, errores = analizador.analizar(codigo)
        
        print(f"\n  RESULTADOS:")
        print(f"    Tokens reconocidos: {len(tokens)}")
        print(f"    Errores reales: {len(errores)}")
        print(f"    Orden de patrones ")
        
        generador = GeneradorHTML()
        nombre_archivo = os.path.basename(archivo_path)
        
        html_tokens = generador.generar_reporte_tokens(tokens, nombre_archivo)
        with open('reporte_tokens.html', 'w', encoding='utf-8') as f:
            f.write(html_tokens)
        
        html_errores = generador.generar_reporte_errores(errores, nombre_archivo)
        with open('reporte_errores.html', 'w', encoding='utf-8') as f:
            f.write(html_errores)
        
        print("\n REPORTES GENERADOS:")
        print(f"   reporte_tokens.html")
        print(f"    reporte_errores.html")
        print(f"\n ----------------------->")
        
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    main()
