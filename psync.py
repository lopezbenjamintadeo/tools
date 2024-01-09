import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pysftp

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        # Aquí puedes agregar la lógica para mover el archivo a un servidor SFTP
        # en este ejemplo, simplemente imprimiremos el nombre del archivo
        print(f'Modificado: {event.src_path}')

        # Lógica para transferir el archivo a un servidor SFTP
        sftp_host = 'sftp.server.com'
        sftp_user = 'my_user'
        sftp_password = 'my_password'
        sftp_port = 22  # El puerto SFTP suele ser el 22, pero puedes ajustarlo según tu configuración

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None  # Desactiva la verificación de la clave del host

        with pysftp.Connection(sftp_host, username=sftp_user, password=sftp_password, port=sftp_port, cnopts=cnopts) as sftp:
            sftp.put(event.src_path)

def main():
    folder_to_watch = 'carpeta_que_deseas_monitorear'

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
