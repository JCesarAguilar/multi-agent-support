# VPN y conexión remota - Andina Obras S.A.C.

Guía del área de TI para conectarse a los sistemas de la empresa desde fuera de la sede central. Documento ficticio con fines de formación.

## Qué es la VPN y cuándo se usa

La VPN (red privada virtual) crea una conexión cifrada entre la laptop institucional y la red de Andina Obras, como si el colaborador estuviera dentro de la sede central. Es necesaria para acceder desde casa, desde una obra o desde cualquier red externa al ERP, a las carpetas compartidas del servidor de archivos y a la plataforma de planos. No es necesaria para usar el correo, Teams ni Andina360, que funcionan directamente por internet. La empresa usa el cliente AndinaVPN, que viene instalado en todas las laptops institucionales.

## Cómo conectarse a la VPN

Para conectarse, el colaborador abre la aplicación AndinaVPN, selecciona el perfil "Andina Obras - Principal", ingresa su usuario corporativo (nombre.apellido) y su contraseña, y aprueba la notificación de autenticación en dos pasos en Microsoft Authenticator. Cuando la conexión es exitosa, el ícono del escudo en la barra de tareas se pone verde. La sesión de VPN se desconecta automáticamente después de 10 horas o tras 30 minutos sin actividad. Si el colaborador trabaja desde una obra con la red de la empresa, no necesita conectarse a la VPN.

## Error de credenciales en la VPN

Si AndinaVPN muestra el mensaje "Credenciales inválidas", lo más común es que el usuario esté escribiendo su correo completo en lugar de solo nombre.apellido, o que su contraseña haya vencido. El colaborador debe verificar que puede iniciar sesión en el correo web con la misma contraseña; si no puede, debe restablecerla en clave.andinaobras.pe y esperar 15 minutos antes de volver a intentar en la VPN, porque el cambio tarda en sincronizarse. Si después de eso el error persiste, puede que su usuario no tenga habilitado el permiso de VPN: debe crear un ticket indicando el mensaje exacto.

## La VPN no conecta o se queda cargando

Cuando la VPN se queda en "Conectando..." o muestra un error de tiempo de espera agotado, el problema suele estar en la red desde la que se conecta el colaborador. Pasos recomendados: verificar que hay internet abriendo cualquier página web, reiniciar el router de casa, desactivar otras VPN personales que puedan estar activas y, si se está en una red pública (hotel, aeropuerto, cafetería), probar con los datos móviles del celular compartidos por wifi. Algunas redes públicas bloquean las conexiones VPN. Si con otra red funciona, el problema no es de la cuenta. Si no funciona con ninguna red, se debe crear un ticket de prioridad alta.

## Error de puerta de enlace al acceder a los sistemas

Si la VPN conecta correctamente pero al abrir el ERP o la plataforma de planos aparece un error de puerta de enlace (por ejemplo, "502 Bad Gateway") o "Servicio no disponible", el problema no está en la laptop del colaborador sino en el servidor del sistema. Antes de crear un ticket, el colaborador puede revisar la página de estado estado.andinaobras.pe, donde TI publica las caídas y los mantenimientos programados. Si la caída ya está publicada, no es necesario crear un ticket: TI informará por correo cuando el servicio se restablezca. Si no está publicada, se debe reportar como prioridad crítica.

## Lentitud con la VPN

Es normal que la conexión sea algo más lenta con la VPN activa, porque el tráfico viaja cifrado hasta la sede central. Para mejorar la velocidad, se recomienda conectarse por cable o cerca del router, cerrar descargas o videos en streaming en otros dispositivos de la casa y no abrir archivos de planos muy pesados directamente desde la carpeta compartida: es mejor descargarlos primero a la laptop. Para trabajar de forma remota, la empresa recomienda una conexión de al menos 20 Mbps. Si la lentitud es extrema y ocurre con cualquier red, se debe crear un ticket para que TI revise el equipo.

## Carpetas compartidas desde casa

Las carpetas compartidas del servidor de archivos, como la unidad P: de proyectos, solo están disponibles con la VPN conectada. Si la unidad aparece con una X roja o pide credenciales, el colaborador debe primero conectar la VPN y luego, en el explorador de archivos, hacer clic derecho sobre la unidad y elegir "Conectar". Los documentos que no requieren estar en el servidor se recomienda guardarlos en OneDrive corporativo, que funciona sin VPN y se sincroniza automáticamente.

## Microsoft Teams y videollamadas

Microsoft Teams es la herramienta oficial de reuniones y mensajería interna. No requiere VPN; de hecho, se recomienda desconectar la VPN durante videollamadas largas para mejorar la calidad del audio y video. Si Teams no permite iniciar sesión, muestra la pantalla en blanco o no sincroniza los mensajes, el primer paso es cerrar sesión, salir completamente de la aplicación y volver a ingresar. Si el micrófono o la cámara no funcionan, hay que revisar que Teams tenga los permisos del sistema operativo y que el dispositivo correcto esté seleccionado en Configuración > Dispositivos.

## Impresión desde casa

Las impresoras de la sede central y de las obras no están disponibles desde casa, ni siquiera con la VPN. Si un colaborador necesita imprimir un documento de trabajo, puede enviarlo a la cola de impresión segura cuando esté en la oficina: el documento se libera al acercar el fotocheck a la impresora. La empresa no instala impresoras personales en las laptops institucionales ni reembolsa tinta o papel usado en casa, salvo que Finanzas lo apruebe como gasto excepcional.

## Uso de redes públicas y seguridad

Al trabajar desde redes públicas, como cafeterías, aeropuertos u hoteles, siempre se debe conectar la VPN antes de abrir cualquier sistema de la empresa, incluso el correo. No se debe dejar la laptop desatendida ni desbloqueada; para bloquearla rápidamente se usa la combinación Windows + L. Está prohibido conectar la laptop institucional a redes que piden instalar un certificado o un programa para tener internet. Si la laptop se pierde o es robada, el colaborador debe llamar de inmediato al número de emergencias de TI 01-555-2020 para que bloqueen el equipo y su cuenta.

## Internet y wifi en casa

Andina Obras no administra ni da soporte a las redes de internet de los hogares de los colaboradores. Si el wifi de la casa no funciona o es muy lento, el colaborador debe comunicarse con su proveedor de internet. TI solo puede ayudar a verificar que la laptop institucional no tenga un problema propio de red, por ejemplo cuando todos los demás dispositivos de la casa sí tienen internet. La empresa tampoco cubre el costo del servicio de internet del hogar, como lo indica la política de trabajo híbrido de Recursos Humanos.
