msgbox "Hola, gracias por descargar este archivo subido por JimmyTutoriales. Se va a abrir mi canal en una ventana del navegador, suscribete! Es 100% gratis!", vbinformation, "Suscríbete :)"
Set abrirPagina= CreateObject("WScript.Shell")
abrirPagina.Run "http://bit.ly/jimmytutoriales"