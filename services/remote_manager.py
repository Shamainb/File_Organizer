import paramiko

def organize_remote_files():
    hostname = 'your.remote.server'
    username = 'your_username'
    password = 'your_password'
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    sftp = ssh.open_sftp()
    
    remote_path = '/remote/path/'
    files = sftp.listdir(remote_path)
    
    for file in files:
        file_path = f'{remote_path}/{file}'
        extension = file.split('.')[-1].lower()
        folder = categorize_extension(extension)
        
        target_folder = f'{remote_path}/{folder}/'
        try:
            sftp.mkdir(target_folder)
        except OSError:
            pass  # Directory already exists

        sftp.rename(file_path, target_folder + file)
    
    sftp.close()
    ssh.close()

def categorize_extension(extension):
    if extension in ['jpg', 'jpeg', 'png', 'gif']:
        return 'Images'
    elif extension in ['txt', 'pdf']:
        return 'Documents'
    elif extension in ['mp4', 'mkv']:
        return 'Videos'
    else:
        return 'Others'

