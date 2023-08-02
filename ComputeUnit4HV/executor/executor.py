import os


def check_admin_perm():
    ps_script = '%s\\scripts\\misc\\check_permission.ps1' % os.path.dirname(os.path.abspath(__file__))
    with os.popen('powershell.exe -command ' + ps_script) as f:
        f_encode = f.buffer.read()
    try:
        return f_encode.decode().strip()
    except UnicodeDecodeError:
        return f_encode.decode('gbk').strip()


def get_script_path(script_name):
    return '%s\\scripts\\%s' % (os.path.dirname(os.path.abspath(__file__)), script_name)


def execute_command(command, select_param=None, convert_to_json=False):
    other_param = ''
    startswith = 'powershell.exe -command '
    check_admin = True
    if check_admin:
        if check_admin_perm() == 'False':
            return 'Execute PowerShell command need Administrators permission'
    if select_param is None:
        select_param = []
    if len(select_param) > 0:
        other_param = ' | Select-Object ' + ','.join(select_param)
    if convert_to_json:
        other_param += ' | ConvertTo-Json'
    if command:
        command = startswith + '"' + command + other_param + '"'
        with os.popen(command) as f:
            f_encode = f.buffer.read()
        try:
            return f_encode.decode().strip()
        except UnicodeDecodeError:
            return f_encode.decode('gbk').strip()
    else:
        return 'Command is empty'
