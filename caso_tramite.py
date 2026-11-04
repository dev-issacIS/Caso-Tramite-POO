
from abc import ABC, abstractmethod
from datetime import datetime


# I. GESTIÓN DE USUARIOS

class Usuario(ABC):
    """Clase abstracta que reúne las funciones comunes de un usuario."""

    def __init__(self, idUsuario, nombres, apellidos, correo, contraseña, estado=True):
        self.__idUsuario = idUsuario
        self.__nombres = nombres
        self.__apellidos = apellidos
        self.__correo = correo
        self.__contraseña = contraseña
        self.__estado = estado
        self.__sesionActiva = False

    def iniciarSesion(self):
        self.__sesionActiva = self.__estado
        return self.__sesionActiva

    def cerrarSesion(self):
        self.__sesionActiva = False

    def consultarPerfil(self):
        return f"{self.__nombres} {self.__apellidos} - {self.__correo}"

    def actualizarPerfil(self, nombres=None, apellidos=None, correo=None):
        if nombres is not None:
            self.__nombres = nombres
        if apellidos is not None:
            self.__apellidos = apellidos
        if correo is not None:
            self.__correo = correo

    @abstractmethod
    def mostrarOpciones(self):
        """Cada tipo de usuario presenta sus propias opciones."""
        pass


class UsuarioExterno(Usuario):
    """Usuario que presenta y consulta trámites."""

    def __init__(self, idUsuario, nombres, apellidos, correo, contraseña,
                 dni, telefono, direccion):
        super().__init__(idUsuario, nombres, apellidos, correo, contraseña)
        self.__dni = dni
        self.__telefono = telefono
        self.__direccion = direccion
        self.__tramites = []

    def registrarUsuario(self):
        print("Usuario externo registrado:", self.consultarPerfil())

    def crearTramite(self, tramite=None):
        if tramite is not None:
            self.__tramites.append(tramite)
        print("Solicitud de trámite registrada")

    def consultarTramites(self):
        return self.__tramites.copy()

    def mostrarOpciones(self):
        print("Usuario externo: registrar y consultar trámites")


class PersonalAdministrativo(Usuario):
    """Trabajador que atiende y deriva trámites."""

    def __init__(self, idUsuario, nombres, apellidos, correo, contraseña,
                 codigoTrabajador, cargo):
        super().__init__(idUsuario, nombres, apellidos, correo, contraseña)
        self.__codigoTrabajador = codigoTrabajador
        self.__cargo = cargo

    def recibirTramite(self):
        print("Trámite recibido")

    def atenderTramite(self):
        print("Trámite en atención")

    def derivarTramite(self):
        print("Trámite derivado")

    def aprobarDocumento(self):
        print("Documento aprobado")

    def mostrarOpciones(self):
        print("Personal administrativo: recibir, atender, derivar y aprobar")


class Rol:
    """Define un conjunto de permisos."""

    def __init__(self, idRol, nombreRol, descripcion, permisos=None):
        self.__idRol = idRol
        self.__nombreRol = nombreRol
        self.__descripcion = descripcion
        self.__permisos = list(permisos or [])

    def asignarPermiso(self, permiso):
        if permiso not in self.__permisos:
            self.__permisos.append(permiso)

    def revocarPermiso(self, permiso):
        if permiso in self.__permisos:
            self.__permisos.remove(permiso)

    def verificarPermiso(self, permiso):
        return permiso in self.__permisos

    def consultarPermisos(self):
        return self.__permisos.copy()


# II. GESTIÓN DE EXPEDIENTES Y TRÁMITES

class Expediente:
    """Contiene el número de expediente de un trámite."""

    def __init__(self, numeroExpediente, fechaRegistro=None, tipoRegistro="Externo",
                 estado="Registrado"):
        self.__numeroExpediente = numeroExpediente
        self.__fechaRegistro = fechaRegistro or datetime.now()
        self.__tipoRegistro = tipoRegistro
        self.__estado = estado

    def generarNumero(self):
        return self.__numeroExpediente

    def registrarExpediente(self):
        print("Expediente registrado:", self.__numeroExpediente)

    def consultarExpediente(self):
        return f"Expediente {self.__numeroExpediente}: {self.__estado}"


class Tramite:
    """Registra los datos de una solicitud documental."""

    def __init__(self, idTramite, remitente, destinatario, asunto,
                 fechaRecepcion=None, estado="Registrado", prioridad="Normal"):
        self.__idTramite = idTramite
        self.__fechaRecepcion = fechaRecepcion or datetime.now()
        self.__remitente = remitente
        self.__destinatario = destinatario
        self.__asunto = asunto
        self.__estado = estado
        self.__prioridad = prioridad
        self.__expediente = None
        self.__documentos = []

    def registrarTramite(self):
        print(f"Trámite {self.__idTramite} registrado: {self.__asunto}")

    def actualizarDatos(self, asunto=None, destinatario=None):
        if asunto is not None:
            self.__asunto = asunto
        if destinatario is not None:
            self.__destinatario = destinatario

    def consultarTramite(self):
        return f"Trámite {self.__idTramite}: {self.__asunto} ({self.__estado})"

    def cambiarEstado(self, nuevoEstado):
        self.__estado = nuevoEstado

    def asociarExpediente(self, expediente):
        """Relaciona un trámite con su expediente."""
        self.__expediente = expediente

    def agregarDocumento(self, documento):
        self.__documentos.append(documento)


class Documento:
    """Administra el archivo y su estado de conservación."""

    def __init__(self, idDocumento, nombreArchivo, formato, rutaArchivo,
                 fechaCarga=None, estado="Activo", motivoRecuperacion="",
                 fechaVencimiento=None):
        self.__idDocumento = idDocumento
        self.__nombreArchivo = nombreArchivo
        self.__formato = formato
        self.__rutaArchivo = rutaArchivo
        self.__fechaCarga = fechaCarga or datetime.now()
        self.__estado = estado
        self.__motivoRecuperacion = motivoRecuperacion
        self.__fechaVencimiento = fechaVencimiento

    def cargarDocumento(self):
        print("Documento cargado:", self.__nombreArchivo)

    def validarFormato(self):
        return self.__formato.lower() in ("pdf", "docx", "xlsx")

    def descargarDocumento(self):
        print("Ruta del documento:", self.__rutaArchivo)

    def archivarDocumento(self):
        self.__estado = "Archivado"

    def recuperarDocumento(self, motivo="Consulta administrativa"):
        self.__motivoRecuperacion = motivo
        self.__estado = "Activo"

    def verificarVencimiento(self):
        return (self.__fechaVencimiento is not None
                and datetime.now() > self.__fechaVencimiento)

    def eliminarDocumento(self):
        self.__estado = "Eliminado"

    def consultarEstado(self):
        return self.__estado

    def consultarNombre(self):
        return self.__nombreArchivo

    def consultarFechaCarga(self):
        return self.__fechaCarga


class Clasificacion:
    """Clasifica una solicitud documental."""

    def __init__(self, idClasificacion, categoria, tipoDocumento, prioridad):
        self.__idClasificacion = idClasificacion
        self.__categoria = categoria
        self.__tipoDocumento = tipoDocumento
        self.__prioridad = prioridad

    def clasificarTramite(self):
        print("Clasificación:", self.consultarClasificacion())

    def actualizarClasificacion(self, categoria=None, tipoDocumento=None,
                               prioridad=None):
        if categoria is not None:
            self.__categoria = categoria
        if tipoDocumento is not None:
            self.__tipoDocumento = tipoDocumento
        if prioridad is not None:
            self.__prioridad = prioridad

    def consultarClasificacion(self):
        return f"{self.__categoria} / {self.__tipoDocumento} / {self.__prioridad}"


class Cargo:
    """Comprobante de recepción de un trámite."""

    def __init__(self, idCargo, cantidadFolios, asunto, medioNotificacion,
                 fechaEmision=None):
        self.__idCargo = idCargo
        self.__fechaEmision = fechaEmision or datetime.now()
        self.__cantidadFolios = cantidadFolios
        self.__asunto = asunto
        self.__medioNotificacion = medioNotificacion

    def generarCargo(self):
        print("Cargo generado:", self.__idCargo)

    def mostrarCargo(self):
        print(f"Cargo {self.__idCargo}: {self.__asunto}, {self.__cantidadFolios} folios")

    def descargarCargo(self):
        print("Descarga de cargo simulada")


# III. SEGUIMIENTO Y DERIVACIONES

class Seguimiento:
    """Conserva los estados registrados durante la atención."""

    def __init__(self, idSeguimiento, estadoActual, observacion="",
                 fechaActualizacion=None):
        self.__idSeguimiento = idSeguimiento
        self.__fechaActualizacion = fechaActualizacion or datetime.now()
        self.__estadoActual = estadoActual
        self.__observacion = observacion
        self.__historial = [estadoActual]

    def actualizarEstado(self, nuevoEstado, observacion=""):
        self.__estadoActual = nuevoEstado
        self.__observacion = observacion
        self.__fechaActualizacion = datetime.now()
        self.__historial.append(nuevoEstado)

    def consultarEstado(self):
        return self.__estadoActual

    def obtenerHistorial(self):
        return " -> ".join(self.__historial)


class Derivacion:
    """Traslado de un trámite entre áreas."""

    def __init__(self, idDerivacion, areaOrigen, areaDestino, motivo,
                 fechaDerivacion=None, estado="Pendiente", proveido="",
                 motivoCorreccion=""):
        self.__idDerivacion = idDerivacion
        self.__fechaDerivacion = fechaDerivacion or datetime.now()
        self.__areaOrigen = areaOrigen
        self.__areaDestino = areaDestino
        self.__motivo = motivo
        self.__estado = estado
        self.__proveido = proveido
        self.__motivoCorreccion = motivoCorreccion
        self.__historial = [f"{areaOrigen} -> {areaDestino}"]

    def registrarDerivacion(self):
        print("Derivación registrada hacia:", self.__areaDestino)

    def consultarDerivacion(self):
        return f"{self.__areaOrigen} -> {self.__areaDestino} ({self.__estado})"

    def obtenerHistorial(self):
        return " | ".join(self.__historial)

    def derivarMasivamente(self):
        print("Derivación masiva solicitada")

    def derivarAutomaticamente(self):
        print("Derivación automática solicitada")

    def verificarAceptacion(self):
        return self.__estado == "Aceptada"

    def corregirDerivacion(self, nuevaArea, motivoCorreccion):
        if self.verificarAceptacion():
            return False
        self.__areaDestino = nuevaArea
        self.__motivoCorreccion = motivoCorreccion
        self.__historial.append(f"Corrección hacia {nuevaArea}")
        return True


class Asignacion:
    """Asigna documentos a un responsable."""

    def __init__(self, idAsignacion, cantidadDocumentos=0,
                 fechaAsignacion=None, estado="Pendiente"):
        self.__idAsignacion = idAsignacion
        self.__fechaAsignacion = fechaAsignacion or datetime.now()
        self.__cantidadDocumentos = cantidadDocumentos
        self.__estado = estado
        self.__responsable = None
        self.__documentos = []

    def asignarDocumento(self, documento):
        self.__documentos.append(documento)
        self.__cantidadDocumentos = len(self.__documentos)
        self.__estado = "Asignada"

    def asignarMasivamente(self, documentos):
        for documento in documentos:
            self.asignarDocumento(documento)

    def consultarAsignacion(self):
        return f"Asignación {self.__idAsignacion}: {self.__cantidadDocumentos} documentos"

    def actualizarResponsable(self, responsable):
        self.__responsable = responsable


class VistoBueno:
    """Registra solicitudes de aprobación."""

    def __init__(self, idVistoBueno, fechaSolicitud=None, fechaRespuesta=None,
                 estado="Pendiente", observacion=""):
        self.__idVistoBueno = idVistoBueno
        self.__fechaSolicitud = fechaSolicitud or datetime.now()
        self.__fechaRespuesta = fechaRespuesta
        self.__estado = estado
        self.__observacion = observacion

    def solicitarVistoBueno(self):
        self.__estado = "Pendiente"
        print("Solicitud de visto bueno enviada")

    def aprobarVistoBueno(self):
        self.__estado = "Aprobado"
        self.__fechaRespuesta = datetime.now()

    def rechazarVistoBueno(self, observacion=""):
        self.__estado = "Rechazado"
        self.__observacion = observacion
        self.__fechaRespuesta = datetime.now()

    def consultarEstado(self):
        return self.__estado


# IV. COMUNICACIONES Y NOTIFICACIONES

class Notificacion:
    """Prepara y simula el envío de notificaciones."""

    def __init__(self, idNotificacion, correoDestino, asunto, mensaje,
                 fechaEnvio=None, estadoEnvio="Pendiente"):
        self.__idNotificacion = idNotificacion
        self.__correoDestino = correoDestino
        self.__asunto = asunto
        self.__mensaje = mensaje
        self.__fechaEnvio = fechaEnvio
        self.__estadoEnvio = estadoEnvio

    def generarMensaje(self):
        return f"{self.__asunto}: {self.__mensaje}"

    def enviarCorreo(self):
        # Simulación: no se conecta a un servidor SMTP.
        self.__fechaEnvio = datetime.now()
        self.__estadoEnvio = "Simulado"
        print("Envío simulado a:", self.__correoDestino)
        return True

    def notificarRecepcion(self):
        self.__mensaje = "Su trámite fue recibido"
        self.enviarCorreo()

    def notificarCambioEstado(self):
        self.__mensaje = "El estado de su trámite fue actualizado"
        self.enviarCorreo()

    def notificarVistoBueno(self):
        self.__mensaje = "Tiene una solicitud de visto bueno"
        self.enviarCorreo()

    def consultarEstado(self):
        return self.__estadoEnvio


class Memorando:
    """Representa una comunicación institucional."""

    def __init__(self, idMemorando, numeroMemorando, asunto, contenido,
                 fechaEmision=None, destinatarios=None):
        self.__idMemorando = idMemorando
        self.__numeroMemorando = numeroMemorando
        self.__asunto = asunto
        self.__contenido = contenido
        self.__fechaEmision = fechaEmision or datetime.now()
        self.__destinatarios = list(destinatarios or [])

    def crearMemorando(self):
        print("Memorando creado:", self.__numeroMemorando)

    def agregarDestinatario(self, destinatario):
        self.__destinatarios.append(destinatario)

    def enviarMemorando(self):
        print("Envío simulado a:", ", ".join(self.__destinatarios))

    def consultarMemorando(self):
        return f"{self.__numeroMemorando}: {self.__asunto}"


# V. SEGURIDAD Y VALIDACIÓN

class Auditoria:
    """Registra acciones para consulta posterior."""

    def __init__(self, idAuditoria, accion, idUsuario, idDocumento,
                 descripcion, fechaHora=None):
        self.__idAuditoria = idAuditoria
        self.__fechaHora = fechaHora or datetime.now()
        self.__accion = accion
        self.__idUsuario = idUsuario
        self.__idDocumento = idDocumento
        self.__descripcion = descripcion
        self.__registros = []

    def registrarAccion(self):
        self.__registros.append(self)
        print("Acción registrada:", self.__accion)

    def consultarHistorial(self):
        return f"{self.__fechaHora}: {self.__accion} - {self.__descripcion}"

    def filtrarPorUsuario(self, idUsuario):
        return [r for r in self.__registros if r.__idUsuario == idUsuario]


class FirmaDigital:
    """Representa una firma con estado de validación."""

    def __init__(self, idFirma, nombreFirmante, certificadoDigital,
                 fechaFirma=None, estadoValidacion="Pendiente"):
        self.__idFirma = idFirma
        self.__nombreFirmante = nombreFirmante
        self.__fechaFirma = fechaFirma or datetime.now()
        self.__certificadoDigital = certificadoDigital
        self.__estadoValidacion = estadoValidacion

    def validarFirma(self):
        # Validación académica simple; no verifica criptografía real.
        valido = self.verificarCertificado()
        self.__estadoValidacion = "Válida" if valido else "Inválida"
        return valido

    def verificarCertificado(self):
        return bool(self.__certificadoDigital.strip())

    def consultarEstado(self):
        return self.__estadoValidacion


# VI. ARCHIVO, BÚSQUEDA Y REPORTES

class Archivador:
    """Agrupa documentos archivados."""

    def __init__(self, idArchivador, nombre, descripcion, ubicacion,
                 fechaCreacion=None):
        self.__idArchivador = idArchivador
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__ubicacion = ubicacion
        self.__fechaCreacion = fechaCreacion or datetime.now()
        self.__documentos = []

    def crearArchivador(self):
        print("Archivador creado:", self.__nombre)

    def archivarDocumento(self, documento):
        documento.archivarDocumento()
        self.__documentos.append(documento)

    def buscarDocumento(self, nombreArchivo=""):
        return [d for d in self.__documentos
                if nombreArchivo.lower() in d.consultarNombre().lower()]

    def listarDocumentos(self):
        return self.__documentos.copy()


class BuscadorDocumento:
    """Busca documentos de una colección mediante criterios sencillos."""

    def __init__(self, criterioBusqueda="", valorBusqueda="", fechaBusqueda=None):
        self.__criterioBusqueda = criterioBusqueda
        self.__valorBusqueda = valorBusqueda
        self.__fechaBusqueda = fechaBusqueda or datetime.now()
        self.__documentos = []

    def agregarDocumentos(self, documentos):
        self.__documentos.extend(documentos)

    def buscarPorExpediente(self, numeroExpediente):
        # Sin base de datos, se usa un valor de referencia en el nombre.
        return [d for d in self.__documentos
                if numeroExpediente.lower() in d.consultarNombre().lower()]

    def buscarPorAsunto(self, asunto):
        return [d for d in self.__documentos
                if asunto.lower() in d.consultarNombre().lower()]

    def buscarPorFecha(self, fecha):
        return [d for d in self.__documentos if d.consultarFechaCarga().date() == fecha]

    def buscarPorRemitente(self, remitente):
        # Ejemplo básico con el nombre del archivo como texto de búsqueda.
        return [d for d in self.__documentos
                if remitente.lower() in d.consultarNombre().lower()]


class Reporte:
    """Presenta indicadores sencillos de la gestión documental."""

    def __init__(self, idReporte, nombre, tipoReporte, periodoInicio,
                 periodoFin, formatoExportacion="PDF", fechaGeneracion=None):
        self.__idReporte = idReporte
        self.__nombre = nombre
        self.__tipoReporte = tipoReporte
        self.__fechaGeneracion = fechaGeneracion or datetime.now()
        self.__periodoInicio = periodoInicio
        self.__periodoFin = periodoFin
        self.__formatoExportacion = formatoExportacion

    def generarReporte(self):
        print("Reporte generado:", self.__nombre)

    def reporteEstados(self):
        print("Reporte de estados generado (demostración)")

    def calcularTiempoRespuesta(self, fechaInicio=None, fechaFin=None):
        inicio = fechaInicio or self.__periodoInicio
        fin = fechaFin or self.__periodoFin
        return (fin - inicio).total_seconds() / 3600

    def reporteCargaTrabajo(self):
        print("Reporte de carga de trabajo (demostración)")

    def personalizarReporte(self, nombre=None, tipoReporte=None):
        if nombre is not None:
            self.__nombre = nombre
        if tipoReporte is not None:
            self.__tipoReporte = tipoReporte

    def exportarPDF(self):
        print("Exportación a PDF simulada")

    def exportarExcel(self):
        print("Exportación a Excel simulada")


# VII. INTEGRACIÓN

class IntegracionPIDE:
    """Simula el intercambio de documentos con una plataforma externa."""

    def __init__(self, idIntegracion, urlServicio, estadoConexion="Desconectado",
                 fechaSincronizacion=None):
        self.__idIntegracion = idIntegracion
        self.__urlServicio = urlServicio
        self.__estadoConexion = estadoConexion
        self.__fechaSincronizacion = fechaSincronizacion
        self.__documentoRecibido = None

    def conectarPIDE(self):
        # Sin una API real, únicamente se simula la conexión.
        if not self.__urlServicio:
            return False
        self.__estadoConexion = "Conectado (simulado)"
        return True

    def enviarDocumento(self):
        if not self.verificarConexion():
            return False
        self.__fechaSincronizacion = datetime.now()
        print("Envío de documento simulado")
        return True

    def recibirDocumento(self):
        if not self.verificarConexion():
            return None
        return self.__documentoRecibido

    def verificarConexion(self):
        return self.__estadoConexion == "Conectado (simulado)"


# DEMOSTRACIÓN DE LOS PRINCIPIOS DE POO

if __name__ == "__main__":
    print("=== SISTEMA DE GESTIÓN DOCUMENTAL - UNSCH ===")

    externo = UsuarioExterno(1, "Ana", "Quispe", "ana@correo.com", "clave123",
                             "12345678", "999999999", "Ayacucho")
    administrativo = PersonalAdministrativo(2, "Luis", "Pérez", "luis@unsch.edu.pe",
                                            "clave456", "T001", "Secretario")

    # Polimorfismo: una misma operación se comporta según la clase hija.
    for usuario in (externo, administrativo):
        usuario.mostrarOpciones()

    expediente = Expediente("EXP-2026-001")
    tramite = Tramite(1, "Ana Quispe", "Secretaría", "Solicitud de constancia")
    documento = Documento(1, "constancia.pdf", "pdf", "archivos/constancia.pdf")

    tramite.asociarExpediente(expediente)
    tramite.agregarDocumento(documento)
    externo.crearTramite(tramite)
    tramite.registrarTramite()
    expediente.registrarExpediente()
    print(tramite.consultarTramite())
    print("Formato admitido:", documento.validarFormato())

    seguimiento = Seguimiento(1, "Registrado")
    seguimiento.actualizarEstado("En revisión")
    tramite.cambiarEstado("En revisión")
    print("Historial:", seguimiento.obtenerHistorial())

    archivador = Archivador(1, "Archivo general", "Documentos históricos", "Oficina")
    archivador.archivarDocumento(documento)
    print("Estado del documento:", documento.consultarEstado())