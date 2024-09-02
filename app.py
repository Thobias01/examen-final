from flask import Flask, render_template, request, redirect, url_for,flash
from dao.PaisesDao import PaisDao

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/paises-index')
def paises_index():
    # Creacion de la instancia de paisesDao
    paisDao = PaisDao()
    lista_paises = paisDao.getPaises()
    return render_template('paises-index.html', lista_paises=lista_paises)


@app.route('/paises')
def paises():
    return render_template('paises.html')

@app.route('/guardar-pais', methods=['POST'])
def guardarPais():
    pais = request.form.get('txtDescripcion').strip()
    if pais == None or len(pais) < 1:
        # mostrar un mensaje al usuario
        flash('Debe escribir algo en la descripcion', 'warning')

        # redireccionar a la vista paises
        return redirect(url_for('paises'))

    paisdao = PaisDao()
    paisdao.guardarPais(pais.upper())

    # mostrar un mensaje al usuario 
    flash('Guardado exitoso', 'success')

    # redireccionar a la vista paises
    return redirect(url_for('paises_index'))

@app.route('/paises-editar/<id>')
def paisesEditar(id):
    paisdao = PaisDao()
    return render_template('paises-editar.html', pais=paisdao.getPaisById(id))

@app.route('/actualizar-paises', methods=['POST'])
def actualizarPaises():
    id = request.form.get('txtIdPais')
    descripcion = request.form.get('txtDescripcion').strip()

    if descripcion == None or len(descripcion) == 0:
        flash('No debe estar vacia la descripcion')
        return redirect(url_for('paisesEditar', id=id)) 

    # actualizar
    paisdao = PaisDao()
    paisdao.updatePais(id, descripcion.upper())

    return redirect(url_for('paises_index'))


@app.route('/paises-eliminar/<id>')
def paisesEliminar(id):
    paisdao = PaisDao()
    paisdao.deletePais(id)
    return redirect(url_for('paises_index'))


if __name__=='__main__':
    app.run(debug=True)
    