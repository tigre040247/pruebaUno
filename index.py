# Importar la biblioteca de flask y librerias necesarias
from tkinter import messagebox
from flask import Flask, redirect, render_template, request, url_for
import pickle

# Instanciar la aplicación
# Nombre por defecto y ruta donde están los modelos
app = Flask(__name__)

# Arreglo para almacenar los clientes 
listaClientes = []

# 1. Funcion controlador que muestra lista actual de clientes con covid 
# Definicion de la ruta por defecto,
@app.route('/')
# Llamar a principal
def home():
    return render_template('index.html', listaClientes=listaClientes)

# 2. Funcion controlador para agregar lista a tarea de pendientes
# Definicion de la ruta
@app.route('/enviar', methods=['POST'])
# Llamar a enviar
def enviar():
    # Funcion condicional para enviar los datos del formulario
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        covid = request.form['covid']
        gerente = request.form['gerente']

        # Funcion condicional para no registrar en caso de datos vacios
        if nombre == '' or telefono == '' or covid == '':
            #Mensaje de alerta llenar todos los campos 
            messagebox.showwarning("¡Alerta!","Llenar todos los campos")
            return redirect(url_for('home'))

        else:
            #Mensaje de autorizacion de registro
            resultado = messagebox.askquestion("Registrar", "¿Está seguro que desea registrar los datos?")
            #Funcion condicional de confirmacion de registro
            if resultado == "yes":
                listaClientes.append({'nombre': nombre, 'telefono': telefono, 'covid': covid })
                return redirect(url_for('home'))
            else:
                return redirect(url_for('home'))


# 3. Funcion controlador para borrar la lista de tareas
@app.route('/borrar', methods=['POST'])
def borrar():
    if request.method == 'POST':
        # Funcion condicional para mostrar alerta en caso de no existir
        if listaClientes == []:
            messagebox.showwarning("¡Alerta!", " ")
            return redirect(url_for('home'))
        else:
            # Mensaje de autorizacion de borrado
            resultado = messagebox.askquestion(
                "Borrar cliente", "¿Está seguro de que desea borrar los datos?")
            # Funcion condicional de confirmacion de borrado
            if resultado == "yes":
                messagebox.showinfo("Info", "Los datos han sido borrados")
                listaClientes.clear()
                return redirect(url_for('home'))
            else:
                return redirect(url_for('home'))

# 4. Funcion controlador para guardar registros en archivo *.pickle
@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        # Funcion condicional para mostrar alerta en caso de no existir
        if listaClientes == []:
            messagebox.showwarning(
                "¡Alerta!", "No existen tareas para almacenar")
            return redirect(url_for('home'))
        else:
            # Mensaje de autorizacion de guardado
            resultado = messagebox.askquestion(
                "Guardar Cliente", "¿Está seguro de que desea guardar los datos?")
            # Funcion condicional de confirmacion de guardado
            if resultado == "yes":
                # Funcion de creacion y sobreescritura de archivo *.pickle
                with open('Tareas.pickle', 'wb') as f:
                    cliente = {'clientes': listaClientes}
                    pickle.dump(cliente, f)
                messagebox.showinfo("Info", "Los datos han sido guardados")
                return redirect(url_for('home'))
            else:
                return redirect(url_for('home'))



#ruta tienda
@app.route('/tienda')
#Llamar a index.html en la ruta principal
def tienda():
    return render_template('tienda.html')


#ruta admin
@app.route('/admin')
#Llamar a index.html en la ruta principal
def admin():
    return render_template('admin.html')

# Metodo main del programa
if __name__ == '__main__':
    # debug = True, para reiniciar automatica el servidor
    app.run(debug=True)
