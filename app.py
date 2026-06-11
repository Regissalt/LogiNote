from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    materia = request.form.get('materia', 'Materia').capitalize()
    sistema = request.form.get('sistema', 'numerico')
    limite = float(request.form.get('limite', 6))
    
    puntos_necesarios_total = limite * 3
    
    nota1 = float(request.form.get('nota1') or 0)
    nota2 = float(request.form.get('nota2') or 0)
    nota3 = float(request.form.get('nota3') or 0)
    
    if nota1 == 7.50 and nota2 == 7.50 and nota3 == 7.50:
        mensaje = "Tranquilo, se puede mejorar... El creador de esta cosa no llegaba al 8 en su país y miralo ahora, programando en modo Dios."
        return render_template('resultado.html', promedio="7.50", mensaje=mensaje, color="#ff9900", materia=materia, recomendacion="", n1=7.50, n2=7.50, n3=7.50)

    puntos_acumulados = nota1 + nota2 + nota3
    trimestres_cursados = sum(1 for n in [nota1, nota2, nota3] if n > 0)
    
    if trimestres_cursados > 0:
        promedio_actual = round(puntos_acumulados / trimestres_cursados, 2)
    else:
        promedio_actual = 0

    recomendacion = ""
    
    if trimestres_cursados == 1:
        puntos_restantes = puntos_necesarios_total - puntos_acumulados
        nota_necesaria_promedio = round(puntos_restantes / 2, 2)
        if nota_necesaria_promedio <= limite:
            recomendacion = f"Para aprobar el año en {materia}, necesitás promediar un {nota_necesaria_promedio} entre el 2° y 3° trimestre. ¡Venís bien!"
        else:
            recomendacion = f"Ojo: Como el primer trimestre quedó flojo, necesitás meter un promedio pesado de {nota_necesaria_promedio} in los próximos dos para salvar el año."
            
    elif trimestres_cursados == 2:
        puntos_restantes = puntos_necesarios_total - puntos_acumulados
        if puntos_restantes <= 0:
            recomendacion = f"¡Felicidades! Ya sumaste los puntos necesarios. Estás aprobado en {materia} antes de terminar el año."
        else:
            nota_necesaria_final = round(puntos_restantes, 2)
            if nota_necesaria_final <= 10:
                recomendacion = f"En el 3° trimestre de {materia} necesitás sacarte un {nota_necesaria_final} o más para aprobar el año."
            else:
                recomendacion = f"Matemáticamente necesitás un {nota_necesaria_final} para llegar al {limite}. Vas a necesitar un recuperatorio o hablar con el profe, ¡pero no te rindas!"
                
    elif trimestres_cursados == 3:
        if promedio_actual >= limite:
            recomendacion = f"¡Año cerrado! Aprobaste {materia} con un promedio final de {promedio_actual}."
        else:
            recomendacion = f"El promedio final dio {promedio_actual}. Nos vemos en diciembre/febrero para levantar {materia}, ¡con garra que se saca!"

    if promedio_actual >= 8:
        color_texto = "#00ff88"
        mensaje = f"¡Nivel excelente en {materia}!"
    elif promedio_actual >= limite:
        color_texto = "#a3ff00"
        mensaje = f"Vas por buen camino en {materia}."
    else:
        color_texto = "#ff3333"
        mensaje = f"Alerta en {materia}: Hay que ajustar los motores."

    if sistema == "letras":
        pass

    return render_template('resultados.html', promedio=promedio_actual, mensaje=mensaje, color=color_texto, materia=materia, recomendacion=recomendacion, n1=nota1, n2=nota2, n3=nota3)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    


