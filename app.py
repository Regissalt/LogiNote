from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    materia = request.form.get('materia', 'Materia')
    
    n1_raw = request.form.get('nota1')
    n2_raw = request.form.get('nota2')
    n3_raw = request.form.get('nota3')
    
    nota1 = float(n1_raw) if n1_raw else None
    nota2 = float(n2_raw) if n2_raw else None
    nota3 = float(n3_raw) if n3_raw else None

    nota_aprobacion = 6.0
    promedio_actual = 0.0
    mensaje = ""
    color_texto = "#00ffcc"

    if nota1 is not None and nota2 is None and nota3 is None:
        promedio_actual = nota1
        
        if abs(nota1 - 7.50) < 0.01:
            mensaje = f"¡Easter Egg activado en {materia}! Clavaste un 7.50 justo. El sistema dice que vas sobre rieles, crack."
            color_texto = "#ff00ff"
        else:
            nota_necesaria = (nota_aprobacion * 3) - nota1
            nota_por_trimestre = nota_necesaria / 2
            
            if nota_por_trimestre > 10:
                mensaje = f"Alerta en {materia}: Necesitás promediar más de 10. ¡Hay que ajustar los motores!"
                color_texto = "#ff3333"
            else:
                mensaje = f"Vas por buen camino en {materia}. Necesitás un promedio de {nota_por_trimestre:.1f} en los trimestres que quedan."

    elif nota1 is not None and nota2 is not None and nota3 is None:
        promedio_actual = (nota1 + nota2) / 2
        nota_necesaria = (nota_aprobacion * 3) - (nota1 + nota2)
        
        if nota_necesaria <= 0:
            mensaje = f"¡Excelente en {materia}! Ya estás aprobado con lo que sumaste en el 1° y 2° trimestre."
        elif nota_necesaria > 10:
            mensaje = f"Alerta en {materia}: Necesitás un {nota_necesaria:.1f} en el 3° trimestre. Se define al final."
            color_texto = "#ff3333"
        else:
            mensaje = f"Para aprobar {materia}, tenés que sacarte un {nota_necesaria:.1f} en el 3° trimestre."

    elif nota1 is not None and nota2 is not None and nota3 is not None:
        promedio_actual = (nota1 + nota2 + nota3) / 3
        if promedio_actual >= nota_aprobacion:
            mensaje = f"¡Materia aprobada! Tu promedio final en {materia} es de {promedio_actual:.1f}."
        else:
            mensaje = f"Materia pendiente. El promedio final en {materia} cerró en {promedio_actual:.1f}."
            color_texto = "#ff3333"
            
    else:
        mensaje = "Poné al menos la nota del primer trimestre para poder calcular las metas."
        color_texto = "#ff3333"

    return render_template(
        'resultados.html',
        materia=materia,
        promedio=promedio_actual,
        mensaje=mensaje,
        color_texto=color_texto
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    