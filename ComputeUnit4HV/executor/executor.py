import os

def check_admin_perm():
    ps_script = '%s\\scripts\\misc\\check_permission.ps1' % os.path.dirname(os.path.abspath(__file__))
    with os.popen('powershell.exe -command ' + ps_script) as f:
        f_encode = f.buffer.read()
    try:
        return f_encode.decode().strip()
    except UnicodeDecodeError:
        return f_encode.decode('gbk').strip()