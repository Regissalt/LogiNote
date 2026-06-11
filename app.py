from flask import Flask, render_template, request
import os

app = Flask(__name__)

# RUTA 1: La página de inicio (Donde el alumno carga las notas)
@app.route('/')
def index():
    return render_template('index.html')

# RUTA 2: El procesador (Donde se hacen las cuentas al tocar el botón)
@app.route('/calcular', methods=['POST'])
def calcular():
    # Recibimos los datos del formulario de index.html
    materia = request.form.get('materia', 'Materia')
    sistema = request.form.get('sistema', 'numerico')
    
    # Intentamos capturar las notas de los trimestres (si están vacías quedan en None)
    t1 = request.form.get('t1')
    t2 = request.form.get('t2')
    t3 = request.form.get('t3')
    
    nota1 = float(t1) if t1 else None
    nota2 = float(t2) if t2 else None
    nota3 = float(t3) if t3 else None

    # LÓGICA DE CONTROL DE PROMEDIOS
    nota_aprobacion = 6.0
    promedio_actual = 0.0
    mensaje = ""
    color_texto = "#00ffcc" # Color neón por defecto (Aprobado/Buen camino)

    # Caso 1: Tiene solo el primer trimestre cargado
    if nota1 is not None and nota2 is None and nota3 is None:
        promedio_actual = nota1
        nota_necesaria = (nota_aprobacion * 3) - nota1
        # Dividimos el resto en las dos materias que quedan
        nota_por_trimestre = nota_necesaria / 2
        
        if nota_por_trimestre > 10:
            mensaje = f"Alerta en {materia}: Necesitás más de 10 en los próximos trimestres. ¡A meterle garra!"
            color_texto = "#ff3333" # Rojo de alerta
        else:
            mensaje = f"Vas por buen camino en {materia}. Necesitás un promedio de {nota_por_trimestre:.1f} en los próximos trimestres para aprobar."

    # Caso 2: Tiene el primero y el segundo trimestre cargados
    elif nota1 is not None and nota2 is not None and nota3 is None:
        promedio_actual = (nota1 + nota2) / 2
        nota_necesaria = (nota_aprobacion * 3) - (nota1 + nota2)
        
        if nota_necesaria <= 0:
            mensaje = f"¡Felicidades en {materia}! Ya aprobaste la materia con las notas del 1° y 2° trimestre."
        elif nota_necesaria > 10:
            mensaje = f"Alerta en {materia}: Necesitás un {nota_necesaria:.1f} en el 3° trimestre. Se define en diciembre."
            color_texto = "#ff3333"
        else:
            mensaje = f"Para aprobar {materia}, necesitás sacarte un {nota_necesaria:.1f} en el 3° trimestre."

    # Caso 3: Tiene los tres trimestres cargados (Fin de año)
    elif nota1 is not None and nota2 is not None and nota3 is not None:
        promedio_actual = (nota1 + nota2 + nota3) / 3
        if promedio_actual >= nota_aprobacion:
            mensaje = f"¡Materia aprobada! Tu promedio final en {materia} es de {promedio_actual:.1f}."
        else:
            mensaje = f"Materia a diciembre/febrero. El promedio final en {materia} quedó en {promedio_actual:.1f}."
            color_texto = "#ff3333"
            
    else:
        promedio_actual = 0.0
        mensaje = "Por favor, carga al menos la nota del primer trimestre para calcular."
        color_texto = "#ff3333"

    # Retornamos las respuestas al diseño de resultados.html
    return render_template(
        'resultados.html',
        materia=materia,
        promedio=promedio_actual,
        mensaje=mensaje,
        color_texto=color_texto
    )

# ARRANQUE DEL SERVIDOR (Configurado para Render o Local)
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    