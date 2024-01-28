import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import paramiko

class MyHandler(FileSystemEventHandler):
    def __init__(self, ssh_client, remote_path):
        self.ssh_client = ssh_client
        self.remote_path = remote_path

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        print(f"Detected new file: {file_path}")

        # Upload the new file to the remote server
        self.upload_file(file_path)

    def upload_file(self, local_path):
        file_name = os.path.basename(local_path)
        remote_path = os.path.join(self.remote_path, file_name)

        try:
            transport = self.ssh_client.get_transport()
            sftp = paramiko.SFTPClient.from_transport(transport)

            sftp.put(local_path, remote_path)
            print(f"Uploaded {file_name} to {self.remote_path}")
        except Exception as e:
            print(f"Error uploading {file_name}: {str(e)}")

if __name__ == "__main__":
    local_folder_path = "C:/Users/Dan/Desktop/Dev/recorder/local_videos/"
    remote_folder_path = "/videos/"
    
    # SSH connection details
    ssh_host = "192.168.1.24"
    ssh_port = 22
    ssh_user = "????"
    ssh_password = "?????"

    # Set up SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)

    # Set up file system event handler
    event_handler = MyHandler(ssh_client, remote_folder_path)

    # Set up watchdog observer
    observer = Observer()
    observer.schedule(event_handler, path=local_folder_path, recursive=False)
    observer.start()

    try:
        print(f"Watching for new files in {local_folder_path}. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    ssh_client.close()
