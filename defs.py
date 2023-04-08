from config import *  # 导入config.py中定义的全局变量
import shutil  # 导入shutil模块，用于复制、移动、删除文件和目录
import subprocess  # 导入subprocess模块，用于执行系统命令
import fnmatch  # 导入fnmatch模块，用于文件名匹配
import json  # 导入json模块，用于读写JSON格式的数据
from apkfile import ApkFile  # 导入apkfile.py中定义的ApkFile类
# import tkinter as tk
# from tkinter import ttk


def init_folder():
    """检查并创建所需的文件夹"""
    if not os.path.exists("output_apk"):
        os.mkdir("output_apk")

    if not os.path.exists("output_img"):
        os.mkdir("output_img")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def init_json():
    """初始化排除APK列表和APK版本号字典"""
    exclude_apk = []
    apk_version = {}
    if os.path.exists(EXCLUDE_APK_PATH):
        with open(EXCLUDE_APK_PATH, 'r') as f:
            exclude_apk = [line.strip() for line in f.readlines()]

    if os.path.exists(APK_VERSION):
        with open(APK_VERSION, 'r') as f:
            apk_version = json.load(f)
    else:
        apk_version = {}
    return exclude_apk, apk_version


def download_rom(url):
    """从给定的URL下载ROM"""
    subprocess.run(["wget", url])


def extract_payload_bin(zip_files):
    """从ZIP文件中提取payload.bin文件"""
    for f in zip_files:
        subprocess.run(["unzip", f, "payload.bin"])


def extract_product_img():
    # 使用subprocess模块运行shell命令，执行payload-dumper-go的命令，从payload.bin文件中提取product镜像文件
    # -c参数指定最大并发数为8，-output指定提取后的文件输出到output_img目录下
    # -p参数指定提取product镜像，"payload.bin"为输入文件
    subprocess.run(["./payload-dumper-go", "-c", "8", "-output",
                    "output_img", "-p", "product", "payload.bin"])

    # 循环遍历output_img目录下的所有文件，执行os.rename函数将提取的文件移动到当前目录下
    for filename in os.listdir("output_img"):
        src_path = os.path.join("output_img", filename)
        dst_path = os.path.join(".", filename)
        os.rename(src_path, dst_path)


def extract_erofs_product():
    # 使用subprocess模块运行shell命令，执行extract.erofs的命令，提取product.img镜像文件中的文件
    # -i参数指定输入的镜像文件为product.img，-x参数指定提取文件，-T16参数指定使用16个线程提取文件
    subprocess.run(["./extract.erofs", "-i", "product.img", "-x", "-T16"])


def remove_some_apk(exclude_apk):
    # 遍历当前目录及其子目录
    for root, _, files in os.walk('.'):
        for file in files:
            # 判断文件是否为apk文件，且不在要排除的列表中
            if file.endswith('.apk') and file not in exclude_apk:
                src = os.path.join(root, file)
                dst = os.path.join(output_dir, file)
                # 将文件移动到output_dir目录下
                shutil.move(src, dst)

    # 遍历output_dir目录及其子目录
    for root, _, files in os.walk(output_dir):
        for filename in fnmatch.filter(files, "*.apk"):
            # 判断文件名中是否包含"Overlay"或"_Sys"，若包含则删除该文件
            if "Overlay" in filename or "_Sys" in filename or "MiuiBiometric" in filename:
                os.remove(os.path.join(root, filename))


def rename_apk(apk_files):
    # 遍历每个apk文件
    for apk_file in apk_files:
        apk_path = os.path.join(output_dir, apk_file)

        # 使用apkfile库读取apk包信息
        apk = ApkFile(apk_path)

        # 获取apk的包名和版本号
        package_name = apk.package_name
        version_name = apk.version_name
        # version_code
        # version_code = apk.version_code

        # 构建新文件名
        new_name = f"{package_name}^{version_name}.apk"

        # 重命名apk文件
        os.rename(apk_path, os.path.join(output_dir, new_name))


# 定义更新apk版本的函数，遍历输出目录下的apk文件，并更新本地词典
def update_apk_version(apk_version):
    # 遍历输出目录下的apk文件
    for apk_file in os.listdir(output_dir):
        # 如果文件名以".apk"结尾
        if apk_file.endswith('.apk'):
            # 解析文件名，获取包名和版本号
            x, y = os.path.splitext(apk_file)[0].split('^')
            # 如果包名在本地词典中
            if x in apk_version:
                # 如果本地词典中的版本号比当前版本号高
                if apk_version[x] < y:
                    print(f'更新 {x}：{apk_version[x]} -> {y}')
                    # 更新本地词典中的版本号
                    apk_version[x] = y
            # 如果包名不在本地词典中
            else:
                print(f'添加 {x}:{y}')
                # 在本地词典中添加新的包名和版本号
                apk_version[x] = y

    # 保存本地词典到json文件
    with open(APK_VERSION, 'w') as f:
        json.dump(apk_version, f)

# 定义更新apk文件名的函数，读取第二个词典并修改apk文件名


def update_apk_name():
    # 如果第二个词典文件存在，则读取其中的内容
    if os.path.exists(APK_APP_NAME):
        with open(APK_APP_NAME, 'r') as f:
            apk_name = json.load(f)
    # 如果第二个词典文件不存在，则将其设为空字典
    else:
        apk_name = {}

    # 遍历输出目录下的apk文件
    for apk_file in os.listdir(output_dir):
        # 如果文件名以".apk"结尾
        if apk_file.endswith('.apk'):
            # 解析文件名，获取包名和版本号
            x, y = os.path.splitext(apk_file)[0].split('^')
            # 如果包名在第二个词典中
            if x in apk_name:
                new_x = apk_name[x]
                # 构建新的文件名，包含新的应用名和原来的版本号
                new_apk_file = f'{new_x}_{y}.apk'
                # 重命名apk文件
                os.rename(os.path.join(output_dir, apk_file),
                          os.path.join(output_dir, new_apk_file))
                print(f'修改 {apk_file} -> {new_apk_file}')

def delete_files_and_folders():
    """删除指定的文件和文件夹"""
    files_to_delete = ["payload.bin", "product.img"]
    folders_to_delete = ["output_img", "config"]
    
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            print(f"{file} 删除成功")
        else:
            print(f"{file} 不存在")
            
    for folder in folders_to_delete:
        if os.path.exists(folder):
            os.rmdir(folder)
            print(f"{folder} 删除成功")
        else:
            print(f"{folder} 不存在")

def main():
    while True:
        init_folder()
        exclude_apk, apk_version = init_json()
        print("请选择一个选项：")
        print("1 - 下载ROM")
        print("2 - 提取payload.bin")
        print("3 - 提取product.img")
        print("4 - 提取erofs镜像")
        print("5 - 删除指定的APK")
        print("6 - 重命名APK文件")
        print("7 - 更新APK版本")
        print("8 - 更新APK文件名")
        print("9 - 删除多余文件")
        print("0 - 退出程序")

        choice = input("请输入数字选择对应操作：")
        if choice == "1":
            download_rom(input("请输入ROM下载链接："))
        elif choice == "2":
            extract_payload_bin(zip_files)
        elif choice == "3":
            extract_product_img()
        elif choice == "4":
            extract_erofs_product()
        elif choice == "5":
            remove_some_apk(exclude_apk)
        elif choice == "6":
            rename_apk(apk_files)
        elif choice == "7":
            update_apk_version(apk_version)
        elif choice == "8":
            update_apk_name()
        elif choice == "9":
            delete_files_and_folders()
        elif choice == "0":
            print("程序已终止")
            break
        else:
            print("输入非法，请重新输入")

# def main():
#     init_folder()
#     exclude_apk, apk_version = init_json()
#     root = tk.Tk()
#     root.title("ROM 工具")

#     # 创建选项列表
#     options = [
#         "从网上下载 ROM",
#         "提取 payload.bin 文件",
#         "解压 product.img 文件",
#         "解压 EROFS 格式的 product.img 文件",
#         "移除指定 APK 文件",
#         "重命名 APK 文件",
#         "更新 APK 文件名",
#         "更新 APK 版本号",
#         "退出程序"
#     ]

#     # 创建选择器
#     choice_var = tk.StringVar(value=options[0])
#     choice_label = ttk.Label(root, text="请选择一个操作：")
#     choice_dropdown = ttk.Combobox(
#         root, textvariable=choice_var, values=options)

#     # 创建运行按钮
#     def run_selected_operation():
#         choice = choice_var.get()
#         if choice == options[0]:
#             download_rom(input("请输入ROM下载链接："))
#         elif choice == options[1]:
#             extract_payload_bin()
#         elif choice == options[2]:
#             extract_product_img()
#         elif choice == options[3]:
#             extract_erofs_product()
#         elif choice == options[4]:
#             remove_some_apk(exclude_apk)
#         elif choice == options[5]:
#             rename_apk()
#         elif choice == options[6]:
#             update_apk_name()
#         elif choice == options[7]:
#             update_apk_version(apk_version)
#         else:
#             root.destroy()

#     run_button = ttk.Button(root, text="运行", command=run_selected_operation)

#     # 将控件放置在主窗口中
#     choice_label.pack(side="left")
#     choice_dropdown.pack(side="left")
#     run_button.pack(side="left")

#     root.mainloop()