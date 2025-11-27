from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import models as db


app = Flask(__name__)
app.secret_key = 'jeje'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('index'))

#------ empleado -------#

@app.route('/index_empl')
def index_emp():
    if 'user_id' not in session or session.get('user_rol') != 1:
        return redirect(url_for('index'))
    return render_template('empleados/index_emp.html')

@app.route('/rechumE')
def rh_emp():
    return render_template('empleados/RH_emp.html')

#--- perfil empleado ------#

@app.route('/completar_perfilE', methods=['GET', 'POST'])
def completar_perfilE():
    if 'user_id' not in session:
        return redirect(url_for('iniciosesion'))

    user_id = session['user_id']

    if request.method == 'POST':
        nomEmpleado = request.form['nomEmpleado']
        apeEmpleado = request.form['apeEmpleado']
        edad = request.form['edad']
        documento = request.form['documento']
        telefono = request.form['telefono']
        nomEps = request.form['nomEps']
        nomCargo = request.form['nomCargo']

        # Insertar la información del empleado en la base de datos
        cursor = db.database.cursor()
        sql = """
            INSERT INTO empleados (nomEmpleado, apeEmpleado, edad, documento, telefono, idEps, idCargo, idUsuario)
            VALUES (%s, %s, %s, %s, %s, (SELECT idEps FROM eps WHERE nomEps = %s), (SELECT idCargo FROM cargo WHERE nomCargo = %s), %s)
        """
        data = (nomEmpleado, apeEmpleado, edad, documento, telefono, nomEps, nomCargo, user_id)
        cursor.execute(sql, data)
        db.database.commit()
        cursor.close()

        return redirect(url_for('perfilE'))

    # Obtener las EPS y los cargos de la base de datos
    eps_list = db.get_eps_list()
    cargo_list = db.get_cargo_list()

    return render_template('empleados/completar_perfilE.html', eps_list=eps_list, cargo_list=cargo_list)



@app.route('/perfilE')
def perfilE():
    if 'user_id' not in session:
        return redirect(url_for('iniciosesion'))

    user_id = session['user_id']

    # Lógica para obtener la información del empleado desde la base de datos
    empleado = db.get_empleado_info(user_id)


    return render_template('empleados/perfilE.html', empleado=empleado)

# ------ Solicitud Empleados --------#

@app.route('/solicitudEmp', methods=['GET', 'POST'])
def solicitudE():
    if request.method == 'POST':
        tipoSolicitud = request.form['tipoSolicitud']
        motivo = request.form['motivo']
        fechaSolicitud = request.form['fechaSolicitud']

        # Obtener el idUsuario del usuario actualmente autenticado
        if 'user_id' in session:
            id_usuario = session['user_id']

            # Asegúrate de que el usuario tenga el rol adecuado para hacer la solicitud
            user = db.find_user_by_id(id_usuario)
            if user and user['idRol'] == 1:  # idRol 1 corresponde al rol de empleado
                if db.insert_solicitud_empleado(tipoSolicitud, motivo, fechaSolicitud, id_usuario):
                    flash('Solicitud enviada exitosamente!', 'success')
                    return redirect(url_for('solicitud_exitoE'))
                else:
                    flash('Error al enviar la solicitud.', 'danger')
                    return redirect(url_for('solicitudE'))
            else:
                flash('No tienes permisos para realizar esta acción.', 'danger')
                return redirect(url_for('solicitudE'))
        else:
            flash('Debes iniciar sesión para realizar una solicitud.', 'danger')
            return redirect(url_for('iniciosesion'))

    return render_template('empleados/solicitudE.html')

@app.route('/solicitud_exitoE')
def solicitud_exitoE():
    return render_template('empleados/solicitud_exitoE.html')

@app.route('/empleados/consulta')
def consulta():
    if 'user_id' not in session:
        flash('Inicia sesión para ver tus solicitudes', 'warning')
        return redirect(url_for('iniciosesion'))

    # Obtener el idEmpleado del empleado actualmente autenticado
    user_id = session['user_id']
    id_empleado = db.get_id_empleado_by_user_id(user_id)

    if id_empleado is None:
        flash('Error al obtener el empleado', 'danger')
        return redirect(url_for('index_emp'))

    # Obtener las solicitudes del empleado desde la base de datos usando id_empleado
    consultas = db.get_solicitudes_del_empleado(id_empleado)

    if consultas is None:
        flash('Error al obtener las solicitudes del empleado', 'danger')
        consultas = []

    return render_template('empleados/consulta.html', consultas=consultas)

#--- cliente -----#

@app.route('/index_client')
def index_cl():
    if 'user_id' not in session or session.get('user_rol') != 2:
        return redirect(url_for('index'))
    return render_template('clientes/index_cl.html')

#--- perfil Cliente----#
@app.route('/completar_perfil', methods=['GET', 'POST'])
def completar_perfil():
    if 'user_id' not in session:
        return redirect(url_for('iniciosesion'))

    user_id = session['user_id']

    if request.method == 'POST':
        nombreCliente = request.form['nomCliente']
        apeCliente = request.form['apeCliente']
        telefono = request.form['telefono']

        # Insertar la información del cliente en la base de datos
        db.cursor.execute("INSERT INTO clientes (nombreCliente, apeCliente, telefono, idUsuario) VALUES (%s, %s, %s, %s)",
                          (nombreCliente, apeCliente, telefono, user_id))
        db.database.commit()

        return redirect(url_for('perfil'))

    return render_template('clientes/completar_perfil.html')


@app.route('/perfil')
def perfil():
    if 'user_id' not in session:
        return redirect(url_for('iniciosesion'))

    user_id = session['user_id']

    # Obtener la información del cliente desde la base de datos
    cliente = db.get_cliente_info(user_id)

    return render_template('clientes/perfil.html', cliente=cliente)


#--- proyecto -----#
@app.route('/proyecto')
def proyectos():
    return render_template('proyectos.html')

@app.route('/recontraseña', methods=['GET', 'POST'])
def rec_contraseña():
    if request.method == 'POST':
        correo = request.form['email']
        usuario = db.find_user_by_email(correo)
        if usuario:
            # Mostrar el formulario para cambiar la contraseña
            return render_template('rec_contraseña.html', correo=correo)
        else:
            flash('Correo no encontrado.', 'danger')
    return render_template('rec_contraseña.html')


@app.route('/change_password', methods=['POST'])
def change_password():
    correo = request.form['email']
    new_password = request.form['newPassword']
    usuario = db.find_user_by_email(correo)
    if usuario:
        db.update_user_password(correo, new_password)
        flash('Contraseña cambiada con éxito', 'success')
        return redirect(url_for('iniciosesion'))
    else:
        flash('Error al cambiar la contraseña.', 'danger')
        return redirect(url_for('rec_contraseña'))

@app.route('/proyectocl')
def proyectos_cl():
    return render_template('clientes/proyectos_cl.html')

@app.route('/rechum')
def rh():
    return render_template('RH.html')

#----- contacto --------#

@app.route('/contact')
def contacto():
    return render_template('contacto.html')

@app.route('/contacto')
def contacto_cl():
    return render_template('clientes/contacto_cl.html')

@app.route('/contactE')
def contacto_emp():
    return render_template('empleados/contacto_emp.html')

#---- solicitar cliente ----#

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        desc_solicitud = request.form['desc_solicitud']
        id_proyecto = request.form['id_proyecto']

        # Verificar si el usuario está autenticado
        if 'user_id' in session:
            id_usuario = session['user_id']

            # Obtener información del usuario
            user = db.find_user_by_id(id_usuario)
            if user and user['idRol'] == 2:  # Rol 2 corresponde a cliente
                # Intentar insertar la solicitud
                if db.insert_solicitud(desc_solicitud, id_usuario, id_proyecto):
                    flash('Solicitud enviada exitosamente!', 'success')
                    return redirect(url_for('solicitud_exito'))
                else:
                    flash('Error al enviar la solicitud. Inténtalo nuevamente más tarde.', 'danger')
                    app.logger.error('Error al insertar solicitud para usuario %s y proyecto %s', id_usuario, id_proyecto)
            else:
                flash('No tienes permisos para realizar esta acción.', 'danger')
        else:
            flash('Debes iniciar sesión para realizar una solicitud.', 'danger')
            return redirect(url_for('iniciosesion'))

    proyecto_list = db.get_proyecto_list()
    return render_template('clientes/formulario.html', proyectos=proyecto_list)

@app.route('/solicitud_exito')
def solicitud_exito():
    return render_template('clientes/solicitud_exito.html')  # Página de éxito después de enviar la solicitud

@app.route('/clientes/solicitud')
def solicitud():
    if 'user_id' not in session:
        flash('Inicia sesión para ver tus solicitudes', 'warning')
        return redirect(url_for('iniciosesion'))

    # Obtener el idCliente del cliente actualmente autenticado
    user_id = session['user_id']
    id_cliente = db.get_id_cliente_by_user_id(user_id)  # Esta función debe obtener el idCliente asociado con el user_id

    if id_cliente is None:
        flash('Error al obtener el cliente', 'danger')
        return redirect(url_for('index_cl'))  # Redirigir a otra página o manejar el error según tu flujo

    # Obtener las solicitudes del cliente desde la base de datos usando id_cliente
    solicitudes = db.get_solicitudes_del_cliente(id_cliente)

    if solicitudes is None:
        flash('Error al obtener las solicitudes del cliente', 'danger')
        solicitudes = []

    return render_template('clientes/solicitud.html', solicitudes=solicitudes)

@app.route('/contratosC')
def contratos():
    if 'user_id' not in session:
        return redirect(url_for('iniciosesion'))

    user_id = session['user_id']

    # Obtener la información de los contratos desde la base de datos
    contratos = db.get_contratos_cliente(user_id)

    return render_template('clientes/contratos.html', contratos=contratos)

@app.route('/contratosE')
def contratosE():
    if 'user_id' not in session:
        return redirect(url_for('iniciosesion'))

    user_id = session['user_id']

    # Obtener la información de los contratos desde la base de datos
    contratos = get_contratos_empleados(user_id)

    return render_template('empleados/contratosE.html', contratos=contratos)


@app.route('/edit_solicitudC/<string:id>', methods=['POST'])
def edit_solicitudC(id):
    if request.method == 'POST':
        Estado = request.form['estado']

        if Estado:
            cursor = db.database.cursor()
            sql = "UPDATE solicitudesp SET Estado = %s WHERE idSolicitud = %s"
            data = (Estado, id)
            cursor.execute(sql, data)
            db.database.commit()
            cursor.close()
            return redirect(url_for('solicitudes'))

    # Handle the case where not all parameters were provided or any other issue
    flash('Error updating solicitud. Please check your input.')
    return redirect(url_for('solicitudes'))

#---- Solicitudes ---#

@app.route('/solicitud')
def solicitudes():
    cursor = db.database.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            s.idSolicitud, s.desc_solicitud, s.Estado,
            cl.nombreCliente AS nom_cliente,
            p.nomProyecto As nom_proyecto
        FROM solicitudesp s
        JOIN clientes cl ON s.idCliente = cl.idCliente
        JOIN proyectos p ON s.idProyecto = p.idProyecto
    """)
    contratoP = cursor.fetchall()

    cursor.execute("SELECT nombreCliente FROM clientes")
    clientes = cursor.fetchall()

    cursor.execute("SELECT nomProyecto FROM proyectos")
    proyectos = cursor.fetchall()

    cursor.close()

    return render_template('solicitudes.html', data=contratoP, clientes=clientes, proyectos=proyectos)

#------ solicitudes de empleados ----------#

@app.route('/solicitudEmpl')
def solicitudesEmpleados():
    cursor = db.database.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            se.idSolicitud, se.tipoSolicitud, se.motivo, se.fechaSolicitud, se.estado, se.fechaRespuesta, se.respuesta,
            e.nomEmpleado AS nom_empleado,
            e.documento AS documento
        FROM solicitudese se
        JOIN empleados e ON se.idEmpleado = e.idEmpleado
    """)
    solicitudE = cursor.fetchall()

    cursor.execute("SELECT nomEmpleado FROM empleados")
    empleados = cursor.fetchall()

    cursor.close()

    return render_template('solicitudesEmpleados.html', data=solicitudE, empleados=empleados)

@app.route('/edit_solicitud/<string:id>', methods=['POST'])
def edit_solicitud(id):
    if request.method == 'POST':
        estado = request.form['estado']
        fechaRespuesta = request.form['fechaRespuesta']
        respuesta = request.form['respuesta']

        if estado and fechaRespuesta and respuesta:
            cursor = db.database.cursor()
            sql = "UPDATE solicitudese SET estado = %s, fechaRespuesta = %s, respuesta = %s WHERE idSolicitud = %s"
            data = (estado, fechaRespuesta, respuesta, id)
            cursor.execute(sql, data)
            db.database.commit()
            cursor.close()
            return redirect(url_for('solicitudesEmpleados'))

    # Handle the case where not all parameters were provided or any other issue
    flash('Error updating solicitud. Please check your input.')
    return redirect(url_for('solicitudesEmpleados'))


#--- contrato proyecto ----#
@app.route('/contractP')
def contratoProyecto():
    cursor = db.database.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            cp.idContratoP, cp.fechaI, cp.fechaF, cp.precio,
            a.nomAdmin AS nombre_admin,
            cl.nombreCliente AS nom_cliente,
            cd.nomCiudad AS nom_ciudad,
            e.nomEmpleado AS nombre_empleado,
            pr.nomProyecto AS nom_proyecto
        FROM contproyecto cp
        JOIN empleados e ON cp.idEmpleado = e.idEmpleado
        JOIN admin a ON cp.idAdmin = a.idAdmin
        JOIN clientes cl ON cp.idCliente = cl.idCliente
        JOIN ciudad cd ON cp.idCiudad = cd.idCiudad
        JOIN proyectos pr ON cp.idProyecto = pr.idProyecto
    """)
    contratoP = cursor.fetchall()


    cursor.execute("SELECT nomEmpleado FROM empleados")
    empleados = cursor.fetchall()

    cursor.execute("SELECT nomAdmin FROM admin")
    admin = cursor.fetchall()

    cursor.execute("SELECT nombreCliente FROM clientes")
    clientes = cursor.fetchall()

    cursor.execute("SELECT nomCiudad FROM ciudad")
    ciudades = cursor.fetchall()

    cursor.execute("SELECT nomProyecto FROM proyectos")
    proyectos = cursor.fetchall()

    cursor.close()
    return render_template('ContratoProyecto.html', data=contratoP, empleados=empleados, admin=admin, ciudades=ciudades, clientes=clientes, proyectos=proyectos)

@app.route('/add_contractP', methods=['POST'])
def add_contractP():
    fechaI = request.form['fechaI']
    fechaF = request.form['fechaF']
    precio = request.form['precio']
    nomAdmin = request.form['nombre_admin']
    nomEmpleado = request.form['nombre_empleado']
    nombreCliente = request.form['nom_cliente']
    nomCiudad = request.form['nom_ciudad']
    nomProyecto = request.form['nom_proyecto']

    if nomProyecto and fechaI and fechaF and precio and nombreCliente and nomCiudad and nomAdmin and nomEmpleado:
        cursor = db.database.cursor()
    sql = """
        INSERT INTO contproyecto (fechaI, fechaF, precio, idAdmin, idEmpleado, idCliente, idCiudad, idProyecto)
        VALUES (%s, %s, %s,
        (SELECT idAdmin FROM admin WHERE nomAdmin = %s),
        (SELECT idEmpleado FROM empleados WHERE nomEmpleado = %s),
        (SELECT idCliente FROM clientes WHERE nombreCliente = %s),
        (SELECT idCiudad FROM ciudad WHERE nomCiudad = %s),
        (SELECT idProyecto FROM proyectos WHERE nomProyecto = %s))
    """
    data = (fechaI, fechaF, precio, nomAdmin, nomEmpleado, nombreCliente, nomCiudad, nomProyecto)
    cursor.execute(sql, data)
    db.database.commit()
    cursor.close()

    return redirect(url_for('contratoProyecto'))


@app.route('/edit_contractP/<string:id>', methods=['POST'])
def edit_contractP(id):
    if request.method == 'POST':
        fechaI = request.form['fechaI']
        fechaF = request.form['fechaF']
        precio = request.form['precio']
        nombre_empleado = request.form['nombre_empleado']
        nom_cliente = request.form['nom_cliente']
        nom_ciudad = request.form['nom_ciudad']
        nom_proyecto = request.form['nom_proyecto']


    if fechaI and fechaF and precio and nom_ciudad and nom_cliente and nombre_empleado:
        cursor = db.database.cursor()
        sql = "UPDATE contproyecto SET fechaI = %s, fechaF = %s, precio = %s, idEmpleado = (SELECT idEmpleado FROM empleados WHERE nomEmpleado = %s), idCliente = (SELECT idCliente FROM clientes WHERE nombreCliente = %s), idCiudad = (SELECT idCiudad FROM ciudad WHERE nomCiudad = %s), idProyecto = (SELECT idProyecto FROM proyectos WHERE nomProyecto = %s) WHERE idContratoP = %s"
        data = (fechaI, fechaF, precio, nombre_empleado, nom_cliente, nom_ciudad, nom_proyecto, id)
        cursor.execute(sql, data)
        db.database.commit()
        cursor.close()
    return redirect(url_for('contratoProyecto'))


@app.route('/delete_contractP/<string:id>', methods=['GET'])
def delete_contractP(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM contproyecto WHERE idContratoP = %s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    cursor.close()
    return redirect(url_for('contratoProyecto'))

@app.route('/dashP')
def dashproyectos():
    return render_template('dashproyectos.html')

#---- inicio sesion -----#
@app.route('/inicioSesion', methods=['GET', 'POST'])
def iniciosesion():
    if request.method == 'POST':
        nombre_usuario = request.form['Nombre_Usuario']
        contraseña = request.form['contraseña']

        try:
            cursor = db.get_cursor()

            if cursor:
                sql = "SELECT idUsuario, contraseña, idRol, Nombre_Usuario FROM usuarios WHERE correo = %s"
                cursor.execute(sql, (nombre_usuario,))
                user = cursor.fetchone()

                if user and user['contraseña'] == contraseña:
                    # Almacenar datos del usuario en la sesión
                    session['user_id'] = user['idUsuario']
                    session['user_name'] = user['Nombre_Usuario']
                    session['user_rol'] = user['idRol']

                    # Redirigir según el rol del usuario o correo
                    if nombre_usuario == 'Jp_mendoza17@gmail.com':
                        return redirect(url_for('dashproyectos'))
                    elif nombre_usuario == 'MairaRechtp1@gmail.com':
                        return redirect(url_for('dashboard'))
                    elif user['idRol'] == 1:
                        return redirect(url_for('index_emp'))
                    else:
                        return redirect(url_for('index_cl'))
                else:
                    return render_template('iniciosesion.html', error="Usuario o contraseña incorrectos")
            else:
                return render_template('iniciosesion.html', error="Error de conexión")

        finally:
            if cursor:
                cursor.close()

    return render_template('iniciosesion.html')


#---Registro-----#
@app.route('/registrarse', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo = request.form['email']
        contraseña = request.form['password']  # Hashear la contraseña
        nombre_usuario = request.form['username']
        id_rol = request.form['id_rol']  # Aquí obtenemos el ID del rol seleccionado en el formulario

        # Insertar los datos en la tabla de usuarios
        cursor = db.database.cursor()
        sql = "INSERT INTO usuarios (correo, contraseña, nombre_usuario, idRol) VALUES (%s, %s, %s, %s)"
        data = (correo, contraseña, nombre_usuario, id_rol)
        cursor.execute(sql, data)
        db.database.commit()
        cursor.close()

        # Redireccionar a la página de inicio de sesión
        return redirect(url_for('iniciosesion'))
    else:
        # Obtener la lista de roles desde la base de datos
        cursor = db.database.cursor()
        cursor.execute("SELECT idRol, nombre_rol FROM roles")
        roles = cursor.fetchall()
        cursor.close()

        # Renderizar el formulario de registro con la lista de roles
        return render_template('registro.html', roles=roles)

@app.route('/map')
def MapaSitio():
    return render_template('MapaSitio.html')

@app.route('/dash_board')
def dashboard():
    return render_template('dashboard.html')

#----- Contratacion de empleados --------------
@app.route('/contract', methods=['GET'])
def contrato1():
    cursor = db.database.cursor(dictionary=True)
    cursor.execute("SELECT ce.idContratoE, ce.banco, ce.fechaI, ce.fechaF, ce.salario, ce.tipoContrato, ce.tipoCuenta, a.nomAdmin AS nombre_admin, e.nomEmpleado AS nombre_empleado FROM contempleado ce JOIN admin a ON ce.idAdmin = a.idAdmin JOIN empleados e ON ce.idEmpleado = e.idEmpleado")
    contratos = cursor.fetchall()

    # Obtener nombres de los administradores
    cursor.execute("SELECT nomAdmin FROM admin")
    admin = cursor.fetchall()

    # Obtener nombres de los empleados
    cursor.execute("SELECT nomEmpleado FROM empleados")
    empleados = cursor.fetchall()

    cursor.close()
    return render_template('contrato1.html', data=contratos, admin=admin, empleados=empleados)

@app.route('/add_contract', methods=['POST'])
def add_contract():
    banco = request.form['banco']
    fechaI = request.form['fechaI']
    fechaF = request.form['fechaF']
    salario = request.form['salario']
    tipoContrato = request.form['tipoContrato']
    tipoCuenta = request.form['tipoCuenta']
    nomAdmin = request.form['nombre_admin']
    nomEmpleado = request.form['nombre_empleado']

    if banco and fechaI and fechaF and salario and tipoContrato and tipoCuenta and nomAdmin and nomEmpleado:
        cursor = db.database.cursor()
        sql = "INSERT INTO contempleado (banco, fechaI, fechaF, salario, tipoContrato, tipoCuenta, idAdmin, idEmpleado) VALUES (%s, %s, %s, %s, %s, %s, (SELECT idAdmin FROM admin WHERE nomAdmin = %s), (SELECT idEmpleado FROM empleados WHERE nomEmpleado = %s))"
        data = (banco, fechaI, fechaF, salario, tipoContrato, tipoCuenta, nomAdmin, nomEmpleado)
        cursor.execute(sql, data)
        db.database.commit()
        cursor.close()
    return redirect(url_for('contrato1'))

@app.route('/delete_contract/<string:id>', methods=['GET'])
def delete_contract(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM contempleado WHERE idContratoE = %s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    cursor.close()
    return redirect(url_for('contrato1'))


@app.route('/edit_contract/<string:id>', methods=['POST'])
def edit_contract(id):
    if request.method == 'POST':
        banco = request.form['banco']
        fechaI = request.form['fechaI']
        fechaF = request.form['fechaF']
        salario = request.form['salario']
        tipoContrato = request.form['tipoContrato']
        tipoCuenta = request.form['tipoCuenta']
        nombre_admin = request.form['nombre_admin']
        nombre_empleado = request.form['nombre_empleado']

        if banco and fechaI and fechaF and salario and tipoContrato and tipoCuenta and nombre_admin and nombre_empleado:
            cursor = db.database.cursor()
            sql = "UPDATE contempleado SET banco = %s, fechaI = %s, fechaF = %s, salario = %s, tipoContrato = %s, tipoCuenta = %s, idAdmin = (SELECT idAdmin FROM admin WHERE nomAdmin = %s), idEmpleado = (SELECT idEmpleado FROM empleados WHERE nomEmpleado = %s) WHERE idContratoE = %s"
            data = (banco, fechaI, fechaF, salario, tipoContrato, tipoCuenta, nombre_admin, nombre_empleado, id)
            cursor.execute(sql, data)
            db.database.commit()
            cursor.close()
        return redirect(url_for('contrato1'))




# ------- certificados ----------
@app.route('/certificate', methods=['GET'])
def certificados():
    cursor = db.database.cursor(dictionary=True)
    cursor.execute("SELECT cf.idCertificados, cf.estado_cert, cf.num_certificado, e.nomEmpleado AS nombre_empleado FROM certificados cf JOIN empleados e ON cf.idEmpleado = e.idEmpleado")
    certificados = cursor.fetchall()

    cursor.execute("SELECT nomEmpleado FROM empleados")
    empleados = cursor.fetchall()

    cursor.close()
    return render_template('certificados.html', data=certificados, empleados=empleados)


@app.route('/add_certificate', methods=['POST'])
def add_certificate():
    estado_cert = request.form['estado_cert']
    num_certificado = request.form['num_certificado']
    nomEmpleado = request.form['nombre_empleado']

    if estado_cert and num_certificado and nomEmpleado:
        cursor = db.database.cursor()

        # Primero, obtenemos el idEmpleado de la tabla empleados
        sql_select = "SELECT idEmpleado FROM empleados WHERE nomEmpleado = %s"
        cursor.execute(sql_select, (nomEmpleado,))
        result = cursor.fetchone()

        if result:
            idEmpleado = result[0]

            # Luego, insertamos en la tabla certificados
            sql_insert = "INSERT INTO certificados (estado_cert, num_certificado, idEmpleado) VALUES (%s, %s, %s)"
            data = (estado_cert, num_certificado, idEmpleado)
            cursor.execute(sql_insert, data)

            db.database.commit()
            cursor.close()
        else:
            # Manejo del caso cuando no se encuentra el empleado
            print("Empleado no encontrado")

    return redirect(url_for('certificados'))

@app.route('/edit_certificate/<string:id>', methods=['POST'])
def edit_certificate(id):
    estado_cert = request.form['estado_cert']
    num_certificado = request.form['num_certificado']
    nomEmpleado = request.form['nombre_empleado']

    if estado_cert and num_certificado and nomEmpleado:
        cursor = db.database.cursor()

        # Primero, obtenemos el idEmpleado de la tabla empleados
        sql_select = "SELECT idEmpleado FROM empleados WHERE nomEmpleado = %s"
        cursor.execute(sql_select, (nomEmpleado,))
        result = cursor.fetchone()

        if result:
            idEmpleado = result[0]

            # Luego, actualizamos la tabla certificados
            sql_update = "UPDATE certificados SET estado_cert = %s, num_certificado = %s, idEmpleado = %s WHERE idCertificados = %s"
            data = (estado_cert, num_certificado, idEmpleado, id)
            cursor.execute(sql_update, data)

            db.database.commit()
            cursor.close()
        else:
            # Manejo del caso cuando no se encuentra el empleado
            print("Empleado no encontrado")

    return redirect(url_for('certificados'))

@app.route('/delete_certificate/<string:id>', methods=['GET'])
def delete_certificate(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM certificados WHERE idCertificados = %s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    cursor.close()
    return redirect(url_for('certificados'))

#----- empleados -----#

@app.route('/empleado')
def empleados():
    cursor = db.database.cursor(dictionary=True)
    cursor.execute("SELECT e.idEmpleado, e.nomEmpleado, e.apeEmpleado, e.edad, e.documento, e.telefono, ep.nomEps AS nom_eps, c.nomCargo AS nom_cargo FROM empleados e JOIN eps ep ON e.idEps = ep.idEps JOIN cargo c ON e.idCargo = c.idCargo")
    empleado = cursor.fetchall()

    cursor.execute("SELECT nomEps FROM eps")
    eps = cursor.fetchall()

    cursor.execute("SELECT nomCargo FROM cargo")
    cargo = cursor.fetchall()

    cursor.close()
    return render_template('empleados.html', data=empleado, eps=eps, cargo=cargo)


# -------- permission ------------
@app.route('/permission')
def permisos():
    cursor = db.database.cursor(dictionary=True)
    cursor.execute("SELECT p.idPermisos, p.duracion, p.numPermiso, p.fechaInicio, p.fechaFin, e.nomEmpleado AS nombre_empleado FROM permisos p JOIN empleados e ON p.idEmpleado = e.idEmpleado")
    Permisos = cursor.fetchall()

    cursor.execute("SELECT nomEmpleado FROM empleados")
    empleados = cursor.fetchall()

    cursor.close()
    return render_template('permisos.html', data=Permisos, empleados=empleados)

@app.route('/add_permission', methods=['POST'])
def add_permission():
    duracion = request.form['duracion']
    numPermiso = request.form['numPermiso']
    nomEmpleado = request.form['nombre_empleado']
    fechaInicio = request.form['fechaInicio']
    fechaFin = request.form['fechaFin']

    if duracion and numPermiso and fechaInicio and fechaFin and nomEmpleado:
        cursor = db.database.cursor()

        # Primero, obtenemos el idEmpleado de la tabla empleados
        sql_select = "SELECT idEmpleado FROM empleados WHERE nomEmpleado = %s"
        cursor.execute(sql_select, (nomEmpleado,))
        result = cursor.fetchone()

        if result:
            idEmpleado = result[0]

            # Luego, insertamos en la tabla permisos
            sql_insert = "INSERT INTO permisos (duracion, numPermiso, fechaInicio, fechaFin, idEmpleado) VALUES (%s, %s, %s)"
            data = (duracion, numPermiso, fechaInicio, fechaFin, idEmpleado)
            cursor.execute(sql_insert, data)

            db.database.commit()
            cursor.close()
        else:
            # Manejo del caso cuando no se encuentra el empleado
            print("Empleado no encontrado")

    return redirect(url_for('permisos'))

@app.route('/edit_permission/<string:id>', methods=['POST'])
def edit_permission(id):
    duracion = request.form['duracion']
    numPermiso = request.form['numPermiso']
    nomEmpleado = request.form['nombre_empleado']
    fechaInicio = request.form['fechaInicio']
    fechaFin = request.form['fechaFin']

    if duracion and numPermiso and fechaInicio and fechaFin and nomEmpleado:
        cursor = db.database.cursor()

        # Primero, obtenemos el idEmpleado de la tabla empleados
        sql_select = "SELECT idEmpleado FROM empleados WHERE nomEmpleado = %s"
        cursor.execute(sql_select, (nomEmpleado,))
        result = cursor.fetchone()

        if result:
            idEmpleado = result[0]

            # Luego, actualizamos la tabla permisos
            sql_update = "UPDATE permisos SET duracion = %s, numPermiso = %s, fechaInicio = %s, fechaFin = %s, idEmpleado = %s WHERE idPermisos = %s"
            data = (duracion, numPermiso, fechaInicio, fechaFin, idEmpleado)
            cursor.execute(sql_update, data)

            db.database.commit()
            cursor.close()
        else:
            # Manejo del caso cuando no se encuentra el empleado
            print("Empleado no encontrado")

    return redirect(url_for('permisos'))

@app.route('/delete_permission/<string:id>', methods=['GET'])
def delete_permission(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM permisos WHERE idPermisos = %s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    cursor.close()
    return redirect(url_for('permisos'))

# -------- incap ------------
@app.route('/incap')
def incapacidades():
    cursor = db.database.cursor(dictionary=True)
    cursor.execute("SELECT i.idIncapacidad, i.fecha_inicio, i.fecha_fin, i.numIncapacidad, i.duracion, e.nomEmpleado AS nombre_empleado FROM incapacidades i JOIN empleados e ON i.idEmpleado = e.idEmpleado")
    Incapacidad = cursor.fetchall()

    cursor.execute("SELECT nomEmpleado FROM empleados")
    empleados = cursor.fetchall()

    cursor.close()
    return render_template('incapacidades.html', data=Incapacidad, empleados=empleados)

@app.route('/add_incap', methods=['POST'])
def add_incap():
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']
    numIncapacidad = request.form['numIncapacidad']
    duracion = request.form['duracion']
    nomEmpleado = request.form['nombre_empleado']

    if fecha_inicio and fecha_fin and numIncapacidad and duracion and nomEmpleado:
        cursor = db.database.cursor()

        # Primero, obtenemos el idEmpleado de la tabla empleados
        sql_select = "SELECT idEmpleado FROM empleados WHERE nomEmpleado = %s"
        cursor.execute(sql_select, (nomEmpleado,))
        result = cursor.fetchone()

        if result:
            idEmpleado = result[0]

            # Luego, insertamos en la tabla incapacidad
            sql_insert = "INSERT INTO incapacidades (fecha_inicio, fecha_fin, numIncapacidad, duracion, idEmpleado) VALUES (%s, %s, %s, %s, %s)"
            data = (fecha_inicio, fecha_fin, numIncapacidad, duracion, idEmpleado)
            cursor.execute(sql_insert, data)

            db.database.commit()
            cursor.close()
        else:
            # Manejo del caso cuando no se encuentra el empleado
            print("Empleado no encontrado")

    return redirect(url_for('incapacidades'))

@app.route('/edit_incap/<string:id>', methods=['POST'])
def edit_incap(id):
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']
    numIncapacidad = request.form['numIncapacidad']
    duracion = request.form['duracion']
    nomEmpleado = request.form['nombre_empleado']


    if fecha_inicio and fecha_fin and numIncapacidad and duracion and nomEmpleado:
        cursor = db.database.cursor()

        # Primero, obtenemos el idEmpleado de la tabla empleados
        sql_select = "SELECT idEmpleado FROM empleados WHERE nomEmpleado = %s"
        cursor.execute(sql_select, (nomEmpleado,))
        result = cursor.fetchone()

        if result:
            idEmpleado = result[0]

            # Luego, actualizamos la tabla incapacidad
            sql_update = "UPDATE incapacidades SET fecha_inicio = %s, fecha_fin = %s, numIncapacidad = %s, duracion = %s, idEmpleado = %s WHERE idIncapacidad = %s"
            data = (fecha_inicio, fecha_fin, numIncapacidad, duracion, idEmpleado, id)
            cursor.execute(sql_update, data)

            db.database.commit()
            cursor.close()
        else:
            # Manejo del caso cuando no se encuentra el empleado
            print("Empleado no encontrado")

    return redirect(url_for('incapacidades'))

@app.route('/delete_incap/<string:id>', methods=['GET'])
def delete_incap(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM incapacidades WHERE idIncapacidad = %s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    cursor.close()
    return redirect(url_for('incapacidades'))


if __name__ == '__main__':
    app.run()