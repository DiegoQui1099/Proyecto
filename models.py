import mysql.connector

database = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Diego10'
)

cursor = database.cursor()

def get_cursor():
    try:
        if not database.is_connected():
            database.reconnect()
        return database.cursor(dictionary=True)
    except mysql.connector.Error as err:
        print(f"Error al conectar con la base de datos: {err}")
        return None

def find_user_by_email(correo):
    cursor = get_cursor()
    if cursor:
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        result = cursor.fetchone()
        cursor.close()
        return result
    return None

def find_user_by_id(user_id):
    cursor = get_cursor()
    if cursor:
        cursor.execute("SELECT * FROM usuarios WHERE idUsuario = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    return None

def get_id_cliente_by_user_id(user_id):
    cursor = get_cursor()
    if cursor:
        cursor.execute("SELECT idCliente FROM clientes WHERE idUsuario = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result['idCliente'] if result else None
    return None

def get_id_empleado_by_user_id(user_id):
    cursor = get_cursor()
    if cursor:
        cursor.execute("SELECT idEmpleado FROM empleados WHERE idUsuario = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result['idEmpleado'] if result else None
    return None

def get_empleado_info(user_id):
    cursor = get_cursor()
    if cursor:
        try:
            cursor.execute("""
                SELECT e.*, eps.nomEps, cargo.nomCargo
                FROM empleados e
                JOIN eps ON e.idEps = eps.idEps
                JOIN cargo ON e.idCargo = cargo.idCargo
                WHERE e.idUsuario = %s
            """, (user_id,))
            empleado = cursor.fetchone()
            cursor.close()
            return empleado
        except mysql.connector.Error as err:
            print(f"Error al obtener información del empleado: {err}")
    return None

def get_cliente_info(user_id):
    cursor = get_cursor()
    if cursor:
        try:
            cursor.execute("""
                SELECT nombreCliente, apeCliente, telefono
                FROM clientes
                WHERE idUsuario = %s
            """, (user_id,))
            cliente = cursor.fetchone()
            cursor.close()
            return cliente
        except mysql.connector.Error as err:
            print(f"Error al obtener información del cliente: {err}")
    return None

def update_user_password(correo, new_password_hash):
    cursor = get_cursor()
    if cursor:
        cursor.execute("UPDATE usuarios SET contraseña = %s WHERE correo = %s", (new_password_hash, correo))
        database.commit()
        cursor.close()

def get_eps_list():
    try:
        cursor = get_cursor()
        if cursor:
            cursor.execute("SELECT * FROM eps")
            result = cursor.fetchall()
            cursor.close()
            return result
    except mysql.connector.Error as err:
        print(f"Error al obtener la lista de EPS: {err}")
    return []

def get_cargo_list():
    try:
        cursor = get_cursor()
        if cursor:
            cursor.execute("SELECT * FROM cargo")
            result = cursor.fetchall()
            cursor.close()
            return result
    except mysql.connector.Error as err:
        print(f"Error al obtener la lista de cargos: {err}")
    return []

def get_id_eps_by_name(nomEps):
    cursor = get_cursor()
    if cursor:
        cursor.execute("SELECT idEps FROM eps WHERE nomEps = %s", (nomEps,))
        result = cursor.fetchone()
        cursor.close()
        return result['idEps'] if result else None
    return None

def get_id_cargo_by_name(nomCargo):
    cursor = get_cursor()
    if cursor:
        cursor.execute("SELECT idCargo FROM cargo WHERE nomCargo = %s", (nomCargo,))
        result = cursor.fetchone()
        cursor.close()
        return result['idCargo'] if result else None
    return None

def get_proyecto_list():
    cursor = get_cursor()
    if cursor:
        cursor.execute("SELECT idProyecto, nomProyecto FROM proyectos")
        result = cursor.fetchall()
        cursor.close()
        return result
    return []

def insert_solicitud(desc_solicitud, id_usuario, id_proyecto):
    try:
        id_cliente = get_id_cliente_by_user_id(id_usuario)
        if id_cliente is None:
            print(f"No se encontró un cliente asociado al usuario con idUsuario={id_usuario}")
            return False

        cursor = get_cursor()
        if cursor:
            cursor.execute("""
                INSERT INTO solicitudesp (desc_solicitud, idCliente, idProyecto)
                VALUES (%s, %s, %s)
            """, (desc_solicitud, id_cliente, id_proyecto))
            database.commit()
            cursor.close()
            return True
    except mysql.connector.Error as err:
        print(f"Error al insertar la solicitud: {err}")
        database.rollback()
    return False

def get_solicitudes_del_cliente(id_cliente):
    try:
        cursor = get_cursor()
        if cursor:
            cursor.execute("""
                SELECT s.idSolicitud, s.desc_solicitud, p.nomProyecto, s.Estado
                FROM solicitudesp s
                JOIN proyectos p ON s.idProyecto = p.idProyecto
                WHERE s.idCliente = %s
            """, (id_cliente,))
            result = cursor.fetchall()
            cursor.close()
            return result
    except mysql.connector.Error as err:
        print(f"Error al obtener las solicitudes del cliente: {err}")
    return []

def insert_solicitud_empleado(tipoSolicitud, motivo, fechaSolicitud, id_usuario):
    try:
        id_empleado = get_id_empleado_by_user_id(id_usuario)
        if id_empleado is None:
            print(f"No se encontró un empleado asociado al usuario con idUsuario={id_usuario}")
            return False

        cursor = get_cursor()
        if cursor:
            cursor.execute("""
                INSERT INTO solicitudese (tipoSolicitud, motivo, fechaSolicitud, idEmpleado)
                VALUES (%s, %s, %s, %s)
            """, (tipoSolicitud, motivo, fechaSolicitud, id_empleado))
            database.commit()
            cursor.close()
            return True
    except mysql.connector.Error as err:
        print(f"Error al insertar la solicitud: {err}")
        database.rollback()
    return False

def get_solicitudes_del_empleado(id_empleado):
    try:
        cursor = get_cursor()
        if cursor:
            cursor.execute("""
                SELECT se.idSolicitud, se.tipoSolicitud, se.motivo, se.fechaSolicitud, se.estado, se.fechaRespuesta, se.respuesta
                FROM solicitudese se
                WHERE se.idEmpleado = %s
            """, (id_empleado,))
            result = cursor.fetchall()
            cursor.close()
            return result
    except mysql.connector.Error as err:
        print(f"Error al obtener las solicitudes del empleado: {err}")
    return []


def get_contratos_cliente(user_id):
    cursor = get_cursor()
    if cursor:
        try:
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
                JOIN usuarios u ON cl.idUsuario = u.idUsuario
                WHERE u.idUsuario = %s
            """, (user_id,))
            contratos = cursor.fetchall()
            cursor.close()
            return contratos
        except mysql.connector.Error as err:
            print(f"Error al obtener información de los contratos: {err}")
    return []


def get_contratos_empleados(user_id):
    cursor = get_cursor()
    if cursor:
        try:
            cursor.execute("""
                SELECT ce.idContratoE, ce.banco, ce.fechaI, ce.fechaF, ce.salario, ce.tipoContrato, ce.tipoCuenta, a.nomAdmin AS nombre_admin, e.nomEmpleado AS nombre_empleado
                FROM contempleado ce
                JOIN admin a ON ce.idAdmin = a.idAdmin
                JOIN empleados e ON ce.idEmpleado = e.idEmpleado
                WHERE ce.idEmpleado = %s
            """, (user_id,))
            contratos = cursor.fetchall()
            cursor.close()
            return contratos
        except mysql.connector.Error as err:
            print(f"Error al obtener información de los contratos: {err}")
    return []


