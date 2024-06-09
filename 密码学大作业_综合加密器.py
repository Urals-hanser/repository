import tkinter as tk
from tkinter import messagebox
import string
import numpy as np
import time 

# 检查单表代换密钥输入的正确性
def check_key(key):
    if len(key) != 26:
        return False, "单表代换密钥长度必须为26个字母"
    if not key.isalpha():
        return False, "单表代换密钥必须只包含字母"
    if len(set(key)) != 26:
        return False, "单表代换密钥中不能有重复字母"
    return True, "单表代换密钥有效"

# 检查仿射密钥输入的正确性
def check_affine_keys(a, b):
    if not (a.isdigit() and b.isdigit()):
        return False, "仿射密钥a和b必须为整数"
    a, b = int(a), int(b)
    if np.gcd(a, 26) != 1:
        return False, "仿射密钥a必须与26互质"
    return True, "仿射密钥有效"

# 单表代换时创建字典
def create_mapping(key, flag):
    mapping = {}
    key = "".join(filter(str.isalpha, key))
    key=key.lower()
    if flag:
        for i, letter in enumerate(key):
            mapping[string.ascii_lowercase[i]] = letter
    else:
        for i, letter in enumerate(key):
            mapping[letter] = string.ascii_lowercase[i]
    return mapping

# 单表代换加解密函数
def monoalphabetic_crypt(text, key, flag):
    mapping = create_mapping(key, flag)
    text=text.lower()
    crypted_text = ''.join(mapping[char] if char in mapping else char for char in text)
    return crypted_text

# 仿射加解密实现函数
def affine_crypt(text, a, b, flag):
    crypted_text = ''
    for char in text:
        if char.isalpha():
            if flag:
                shift = (a * (ord(char.lower()) - ord('a')) + b) % 26
            else:
                c = ord(char.lower()) - ord('a') - b
                a_inv = pow(a , -1 , 26)
                shift = a_inv*c % 26
            crypted_text += chr(int(shift) + ord('a'))
        else:
            crypted_text += char
    return crypted_text

# 维吉尼亚加解密实现函数
def vigenere_crypt(text, key, flag):
    crypted_text = ''
    key = "".join(filter(str.isalpha, key))
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)].lower()) - ord('a')
            if flag:
                crypted_text += chr((ord(char.lower()) - ord('a') + shift) % 26 + ord('a'))
            else:
                crypted_text += chr((ord(char.lower()) - ord('a') - shift + 26) % 26 + ord('a'))
            key_index += 1
        else:
            crypted_text += char
    return crypted_text

# 自由组合加密函数
def combined_encrypt(text, methods):
    t = time.perf_counter()
    keys1 = [key.strip() for key in vigenere_key_input.get('1.0', tk.END).strip().split('，')]
    keys2 = [key.strip() for key in mono_key_input.get('1.0', tk.END).strip().split('，')]
    a1 = [a.strip() for a in a_input.get('1.0', tk.END).strip().split('，')]
    b1 = [b.strip() for b in b_input.get('1.0', tk.END).strip().split('，')]
    v = 0
    m = 0
    f = 0
    for method in methods:
        if method == '单表代换密码':
            key = keys2[m]
            if check_key(key)[0]:
                text = monoalphabetic_crypt(text, key, True)
                m += 1
            else:
                messagebox.showerror("错误", check_key(key)[1])
                return
        elif method == '仿射密码':
            a = a1[f]
            b = b1[f]
            if check_affine_keys(a, b)[0]:
                text = affine_crypt(text, int(a), int(b), True)
                f += 1
            else:
                messagebox.showerror("错误", check_affine_keys(a, b)[1])
                return
        elif method == '维吉尼亚密码':
            key = keys1[v]
            text = vigenere_crypt(text, key, True)
            v+=1
    print(f'coast:{time.perf_counter() - t:.8f}s')
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, text)
    

# 自由组合解密函数
def combined_decrypt(text, methods):
    t = time.perf_counter()
    keys1 = [key.strip() for key in vigenere_key_input.get('1.0', tk.END).strip().split('，')]
    keys2 = [key.strip() for key in mono_key_input.get('1.0', tk.END).strip().split('，')]
    a1 = [a.strip() for a in a_input.get('1.0', tk.END).strip().split('，')]
    b1 = [b.strip() for b in b_input.get('1.0', tk.END).strip().split('，')]
    keys1.reverse()
    keys2.reverse()
    a1.reverse()
    b1.reverse()
    m = 0
    f = 0
    v = 0
    for method in reversed(methods):
        if method == '单表代换密码':
            key = keys2[m]
            if check_key(key)[0]:
                text = monoalphabetic_crypt(text, key, False)
                m += 1
            else:
                messagebox.showerror("错误", check_key(key)[1])
                return
        elif method == '仿射密码':
            a = a1[f]
            b = b1[f]
            if check_affine_keys(a, b)[0]:
                text = affine_crypt(text, int(a), int(b), False)
                f += 1
            else:
                messagebox.showerror("错误", check_affine_keys(a, b)[1])
                return
        elif method == '维吉尼亚密码':
            key = keys1[v]
            text = vigenere_crypt(text, key, False)
            v+=1
    print(f'coast:{time.perf_counter() - t:.8f}s')
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, text)
    

# 与GUI有关的加密功能实现函数
def on_encrypt():
    text = text_input.get('1.0', tk.END).strip()
    methods = [method.strip() for method in method_input.get('1.0', tk.END).strip().split('，')]
    if text:
        combined_encrypt(text, methods)
    else:
        messagebox.showerror("错误", "文本不能为空！")
        
def on_decrypt():
    text = text_input.get('1.0', tk.END).strip()
    methods = [method.strip() for method in method_input.get('1.0', tk.END).strip().split('，')]
    if text:
        combined_decrypt(text, methods)
    else:
        messagebox.showerror("错误", "文本不能为空！")

# 创建GUI
window = tk.Tk()
window.title("加密工具")
window.geometry("800x800")  # 设置窗口大小

# 创建Frame
input_frame = tk.Frame(window)
input_frame.pack(pady=10)

# 创建一个用于显示结果的文本框
result_frame = tk.Frame(window)
result_frame.pack(pady=10)
tk.Label(result_frame, text="加密/解密结果：").grid(row=0, column=0, columnspan=2, pady=5)
result_text = tk.Text(result_frame, width=80, height=10)
result_text.grid(row=1, column=0, columnspan=2, pady=5)

key_frame = tk.Frame(window)
key_frame.pack(pady=10)

vigenere_key_frame = tk.Frame(window)
vigenere_key_frame.pack(pady=10)

affine_frame = tk.Frame(window)
affine_frame.pack(pady=10)

method_frame = tk.Frame(window)
method_frame.pack(pady=10)

button_frame = tk.Frame(window)
button_frame.pack(pady=20)

# 添加输入文本框
tk.Label(input_frame, text="请输入明文或密文：").grid(row=0, column=0, columnspan=2, pady=5)
text_input = tk.Text(input_frame, width=80, height=10)
text_input.grid(row=1, column=0, columnspan=2, pady=5)



# 添加单表代换密钥输入框
tk.Label(key_frame, text="请输入单表代换密钥：").grid(row=0, column=0, columnspan=2, pady=5)
mono_key_input = tk.Text(key_frame, width=80, height=2)
mono_key_input.grid(row=1, column=0, columnspan=2, pady=5)

# 添加维吉尼亚密钥输入框
tk.Label(vigenere_key_frame, text="请输入维吉尼亚密钥：").grid(row=0, column=0, columnspan=2, pady=5)
vigenere_key_input = tk.Text(vigenere_key_frame, width=80, height=2)
vigenere_key_input.grid(row=1, column=0, columnspan=2, pady=5)

# 添加仿射密码参数输入框
tk.Label(affine_frame, text="请输入仿射密码的a值：").grid(row=0, column=0, pady=5)
a_input = tk.Text(affine_frame, width=10, height=1)
a_input.grid(row=0, column=1, pady=5)

tk.Label(affine_frame, text="请输入仿射密码的b值：").grid(row=0, column=2, pady=5)
b_input = tk.Text(affine_frame, width=10, height=1)
b_input.grid(row=0, column=3, pady=5)

# 添加方法顺序输入框
tk.Label(method_frame, text="请输入加密方法和顺序（用逗号分隔，如 '单表代换密码， 仿射密码， 维吉尼亚密码'）：").grid(row=0, column=0, columnspan=4, pady=5)
method_input = tk.Text(method_frame, width=80, height=2)
method_input.grid(row=1, column=0, columnspan=4, pady=5)

# 添加按钮
encrypt_button = tk.Button(button_frame, text="组合加密", command=on_encrypt, width=20)
encrypt_button.grid(row=0, column=0, padx=10)

decrypt_button = tk.Button(button_frame, text="组合解密", command=on_decrypt, width=20)
decrypt_button.grid(row=0, column=1, padx=10)

window.mainloop()