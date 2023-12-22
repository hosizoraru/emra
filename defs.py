from config import *  # 导入config.py中定义的全局变量
import shutil  # 导入shutil模块，用于复制、移动、删除文件和目录
import subprocess  # 导入subprocess模块，用于执行系统命令
import fnmatch  # 导入fnmatch模块，用于文件名匹配
import json  # 导入json模块，用于读写JSON格式的数据
from apkfile import ApkFile  # 导入apkfile.py中定义的ApkFile类

def move_json(backup, type_name):
    def move_files(type_n):
            if type_n == "ph":
                src_1 = os.path.join("./phone", "app_version.json")
                dst_1 = os.path.join(".", "app_version.json")
                src_2 = os.path.join("./phone", "app_code.json")
                dst_2 = os.path.join(".", "app_code.json")
                # 将文件复制到根目录下
                shutil.copy2(src_1, dst_1)
                shutil.copy2(src_2, dst_2)
                try:
                    with open(JSON_V, 'w') as file:
                        new_content = "Phone"
                        file.write(new_content)
                        print("字典库已变更为 Phone")
                except Exception as e:
                    print(f"异常: {e}")
            elif type_n == "f":
                src_1 = os.path.join("./fold", "app_version.json")
                dst_1 = os.path.join(".", "app_version.json")
                src_2 = os.path.join("./fold", "app_code.json")
                dst_2 = os.path.join(".", "app_code.json")
                # 将文件复制到根目录下
                shutil.copy2(src_1, dst_1)
                shutil.copy2(src_2, dst_2)
                try:
                    with open(JSON_V, 'w') as file:
                        new_content = "Fold"
                        file.write(new_content)
                        print("字典库已变更为 Fold")
                except Exception as e:
                    print(f"异常: {e}")
            elif type_n == "p":
                src_1 = os.path.join("./pad", "app_version.json")
                dst_1 = os.path.join(".", "app_version.json")
                src_2 = os.path.join("./pad", "app_code.json")
                dst_2 = os.path.join(".", "app_code.json")
                # 将文件复制到根目录下
                shutil.copy2(src_1, dst_1)
                shutil.copy2(src_2, dst_2)
                try:
                    with open(JSON_V, 'w') as file:
                        new_content = "Pad"
                        file.write(new_content)
                        print("字典库已变更为 Pad")
                except Exception as e:
                    print(f"异常: {e}")

    # 获取字典库当前列表
    try:
        with open(JSON_V, 'r') as file:
            line = file.readline()
            print("当前字典列表为:", line)
        
        # 同步字典库
        if int(backup) == 1:
            print(f"正在同步到 {line} 字典库目录")
            if line == "Phone":
                src_1 = os.path.join(".", "app_version.json")
                dst_1 = os.path.join("./phone", "app_version.json")
                src_2 = os.path.join(".", "app_code.json")
                dst_2 = os.path.join("./phone", "app_code.json")
                # 将文件移动到 phone 目录下
                shutil.move(src_1, dst_1)
                shutil.move(src_2, dst_2)
                print("字典库已同步到 Phone 目录，正在切换")
                move_files(type_name)
            elif line == "Fold":
                src_1 = os.path.join(".", "app_version.json")
                dst_1 = os.path.join("./fold", "app_version.json")
                src_2 = os.path.join(".", "app_code.json")
                dst_2 = os.path.join("./fold", "app_code.json")
                # 将文件移动到 fold 目录下
                shutil.move(src_1, dst_1)
                shutil.move(src_2, dst_2)
                print("字典库已同步到 Fold 目录，正在切换")
                move_files(type_name)
            elif line == "Pad":
                src_1 = os.path.join(".", "app_version.json")
                dst_1 = os.path.join("./pad", "app_version.json")
                src_2 = os.path.join(".", "app_code.json")
                dst_2 = os.path.join("./pad", "app_code.json")
                # 将文件移动到 pad 目录下
                shutil.move(src_1, dst_1)
                shutil.move(src_2, dst_2)
                print("字典库已同步到 Pad 目录，正在切换")
                move_files(type_name)
        elif int(backup) == 0:
            print("正在覆盖字典库目录")
            move_files(type_name)
    except FileNotFoundError as e:
        print(f"异常，找不到文件: {e}")
    except Exception as e:
        print(f"异常: {e}")

def init_folder():
    """检查并创建所需的文件夹"""
    if not os.path.exists("output_apk"):
        os.mkdir("output_apk")

    if not os.path.exists("output_img"):
        os.mkdir("output_img")

    if not os.path.exists("update_apk"):
        os.mkdir("update_apk")

    if not os.path.exists("update_name_apk"):
        os.mkdir("update_name_apk")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(update_apk_folder):
        os.makedirs(update_apk_folder)

    if not os.path.exists(update_apk_name_folder):
        os.makedirs(update_apk_name_folder)
    
    if not os.path.exists(APK_CODE) or not os.path.exists(APK_VERSION):
        print("检测到根目录下没有字典库，正在初始化字典库为 Phone")
        move_json(0, "ph")
        print("如有更换字典库需要，请使用 -j 命令进行切换")


def init_json():
    """初始化排除APK列表和APK版本号字典"""
    exclude_apk = []
    apk_version = {}
    apk_code = {}
    apk_code_name = {}
    # 查询 APK 排除列表
    if os.path.exists(EXCLUDE_APK_PATH):
        with open(EXCLUDE_APK_PATH, 'r') as f:
            exclude_apk = [line.strip() for line in f.readlines()]
    # 查询本地字典版本名
    if os.path.exists(APK_VERSION):
        with open(APK_VERSION, 'r') as f:
            apk_version = json.load(f)
    else:
        apk_version = {}
    # 查询本地字典版本号
    if os.path.exists(APK_CODE):
        with open(APK_CODE, 'r') as f:
            apk_code = json.load(f)
    else:
        apk_code = {}
    return exclude_apk, apk_version, apk_code, apk_code_name


def download_rom(url):
    """从给定的URL下载ROM"""
    subprocess.run(["wget", url])


def extract_payload_bin(zip_files):
    """从ZIP文件中提取payload.bin文件"""
    for f in zip_files:
        try:
            subprocess.run(["unzip", "{}".format(f), "payload.bin"])
        except FileNotFoundError as e:
            print('异常：unzip 命令执行存在问题，请先检查运行环境后重试')
            break
        except Exception as e:
            print(f"异常，报错信息: {e}")


def extract_product_img():
    # 使用 subprocess 模块运行 shell 命令，执行 payload-dumper-go 的命令，从 payload.bin 文件中提取 product 镜像文件
    # -c 参数指定最大并发数为 8，-output 指定提取后的文件输出到 output_img 目录下
    # -p 参数指定提取 product 镜像，"payload.bin" 为输入文件
    subprocess.run(["./payload-dumper-go", "-c", "8", "-output",
                    "output_img", "-p", "product", "payload.bin"])

    # 循环遍历 output_img 目录下的所有文件，执行 os.rename 函数将提取的文件移动到当前目录下
    for filename in os.listdir("output_img"):
        src_path = os.path.join("output_img", filename)
        dst_path = os.path.join(".", filename)
        os.rename(src_path, dst_path)


def extract_erofs_product():
    try:
        # 使用 subprocess 模块运行 shell 命令，执行 extract.erofs 的命令，提取 product.img 镜像文件中的文件
        # -i 参数指定输入的镜像文件为 product.img，-x 参数指定提取文件，-T16 参数指定使用 16 个线程提取文件
        subprocess.run(["./extract.erofs", "-i", "product.img", "-x", "-T16"])
    except Exception as e:
        print("该镜像不是 erofs 压缩格式，无法解包")
        return

    # 获取设备代号
    for root, _, files in os.walk("./product/etc/device_features/"):
        for filename in fnmatch.filter(files, "*.xml"): 
            device_name = os.path.splitext(filename)[0]

            # 建立一个表单，用来判断是否为 Fold 或者 Pad
            is_fold = {"cetus", "zizhan", "babylon"}
            is_pad = {"nabu", "elish", "enuma", "dagu", "pipa", "liuqin", "yudi", "yunluo", "xun", "sheng"}

            for pad in is_pad:
                if device_name == pad:
                    print("\n检测到包设备为 Pad")
                    break
            else:
                for fold in is_fold: 
                    if device_name == fold:
                        print("\n检测到包设备为 Fold")
                        break

def remove_some_apk(exclude_apk):
    # 遍历当前目录及其子目录
    for root, _, files in os.walk('.'):
        for file in files:
            # 判断文件是否为apk文件，且不在要排除的列表中
            if file.endswith('.apk') and file not in exclude_apk:
                src = os.path.join(root, file)
                dst = os.path.join(output_dir, file)
                # 将文件移动到output_dir目录下
                try:
                    shutil.move(src, dst)
                except PermissionError:
                    print(f"无法移动文件 {src}，请检查你的文件权限或关闭占用该文件的程序。")

    # 遍历output_dir目录及其子目录
    for root, _, files in os.walk(output_dir):
        for filename in fnmatch.filter(files, "*.apk"):
            # 判断文件名中是否包含"Overlay"或"_Sys"，若包含则删除该文件
            if "overlay" in filename.lower() or "_Sys" in filename:
                try:
                    os.remove(os.path.join(root, filename))
                except PermissionError:
                    print(f"无法删除文件 {filename}，请检查你的文件权限或关闭占用该文件的程序。")


def rename_apk(apk_files):
    # 遍历每个apk文件
    for apk_file in apk_files:
        apk_path = os.path.join(output_dir, apk_file)

        try:
            # 使用apkfile库读取apk包信息
            apk = ApkFile(apk_path)

            # 获取apk的包名和版本号
            package_name = apk.package_name
            version_name = apk.version_name
            # version_code
            version_code = apk.version_code

            # 构建新文件名
            new_name = f"{package_name}^{version_name}^{version_code}.apk"

            # 重命名apk文件
            if not os.path.exists(os.path.join(output_dir, new_name)):
                os.rename(apk_path, os.path.join(output_dir, new_name))
        except FileNotFoundError as e:
            print('异常：缺失 Android aapt 环境，请先安装依赖后重试')
            break
        except Exception as e:
            print(f"异常，报错信息: {e}")


# 定义更新apk版本的函数，遍历输出目录下的apk文件，并更新本地词典
def update_apk_version(apk_version, apk_code, apk_code_name):
    # 遍历输出目录下的apk文件
    for apk_file in os.listdir(output_dir):
        # 如果文件名以".apk"结尾
        if apk_file.endswith('.apk'):
            # 解析文件名，获取包名和版本号
            try:
                x, y, z = os.path.splitext(apk_file)[0].split('^')
                # 如果包名在本地词典中
                if x in apk_code:
                    # 如果本地词典中的版本号比 Apk 记录的版本号低
                    if apk_code[x] < int(z):
                        print(f'更新 {x}：{apk_code[x]} -> {z}')
                        if apk_version[x] == y:
                            # 更新本地词典中的版本号
                            apk_version[x] = y
                            apk_code[x] = int(z) # 以 int 格式写入
                            apk_code_name[x] = int(z) # 以 int 格式写入
                            # 复制新版本的 APK 文件到 update_apk 文件夹
                            src = os.path.join(output_dir, apk_file)
                            dst = os.path.join(update_apk_folder, apk_file)
                            shutil.copy2(src, dst)
                            print(f'已将 {apk_file} 复制到 {update_apk_folder} 文件夹\n')
                        else:
                            # 更新本地词典中的版本号
                            apk_version[x] = y
                            apk_code[x] = int(z) # 以 int 格式写入
                            # 复制新版本的 APK 文件到 update_apk 文件夹
                            src = os.path.join(output_dir, apk_file)
                            dst = os.path.join(update_apk_folder, apk_file)
                            shutil.copy2(src, dst)
                            print(f'已将 {apk_file} 复制到 {update_apk_folder} 文件夹\n')
                    elif apk_code[x] == int(z):
                        if apk_version[x] != y:
                            print(f'疑似更新 {x}：{apk_version[x]} -> {y}')
                            # 复制新版本的 APK 文件到 update_name_apk 文件夹
                            src = os.path.join(output_dir, apk_file)
                            dst = os.path.join(update_apk_name_folder, apk_file)
                            shutil.copy2(src, dst)
                            print(f'已将 {apk_file} 复制到 {update_apk_name_folder} 文件夹\n')
                # 如果包名不在本地词典中
                else:
                    print(f'添加新应用 {x}:{y}({z})\n')
                    # 在本地词典中添加新的包名和版本号
                    apk_version[x] = y
                    apk_code[x] = int(z) # 以 int 格式写入
            except Exception as e:
                print(f"异常，报错信息: {e}")
                return

    # 保存本地词典到json文件
    with open(APK_VERSION, 'w') as f:
        json.dump(apk_version, f)
    with open(APK_CODE, 'w') as f:
        json.dump(apk_code, f)
    with open(APK_CODE_NAME, 'w') as f:
        json.dump(apk_code_name, f)

# 定义更新apk文件名的函数，读取第二个词典并修改apk文件名


def update_apk_name():
    # 如果第二个词典文件存在，则读取其中的内容
    if os.path.exists(APK_APP_NAME):
        with open(APK_APP_NAME, 'r') as f:
            apk_name = json.load(f)
    # 如果第二个词典文件不存在，则将其设为空字典
    else:
        apk_name = {}

    # 如果临时词典文件存在，则读取其中的内容
    if os.path.exists(APK_CODE_NAME):
        with open(APK_CODE_NAME, 'r') as f:
            apk_code_name = json.load(f)
    # 如果临时词典文件不存在，则将其设为空字典
    else:
        apk_code_name = {}

    def rename_files_in_folder(folder, name_dict, code_dict):
        for apk_file in os.listdir(folder):
            # 如果文件名以".apk"结尾
            if apk_file.endswith('.apk'):
                # 解析文件名，获取包名和版本号
                x, y, z = os.path.splitext(apk_file)[0].split('^')
                # 如果解析的文件名在字典里
                if x in name_dict:
                    if x in code_dict:
                        # 定义修改的文件名
                        new_x = name_dict[x]
                        new_apk_file_1 = f'{new_x}_{y}({z}).apk'
                        # 修改为新定义的文件名
                        os.rename(os.path.join(folder, apk_file),
                                 os.path.join(folder, new_apk_file_1))
                        print(f'修改 {apk_file} -> {new_apk_file_1}')
                    else:
                        # 定义修改的文件名
                        new_x = name_dict[x]
                        new_apk_file_2 = f'{new_x}_{y}.apk'
                        # 修改为新定义的文件名
                        os.rename(os.path.join(folder, apk_file),
                                 os.path.join(folder, new_apk_file_2))
                        print(f'修改 {apk_file} -> {new_apk_file_2}')

    # 重命名 output_dir 中的 APK 文件
    rename_files_in_folder(output_dir, apk_name, apk_code_name)

    # 重命名 update_apk 文件夹中的 APK 文件
    rename_files_in_folder(update_apk_folder, apk_name, apk_code_name)

    # 重命名 update_name_apk 文件夹中的 APK 文件
    rename_files_in_folder(update_apk_name_folder, apk_name, apk_code_name)


def delete_files_and_folders():
    """删除指定的文件和文件夹"""
    files_to_delete = ["payload.bin", "product.img", "app_code_name.json"]
    folders_to_delete = ["output_img", "output_apk", "update_apk", "update_name_apk", "config", "product"]

    for file in files_to_delete:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"{file} 删除成功")
            except OSError as e:
                print(f"无法删除 {file}: {e}")

        else:
            print(f"{file} 不存在")

    for folder in folders_to_delete:
        if os.path.exists(folder):
            if os.path.isdir(folder):
                try:
                    shutil.rmtree(folder)
                    print(f"{folder} 删除成功")
                except OSError as e:
                    print(f"无法删除 {folder}: {e}")
            else:
                print(f"{folder} 不是文件夹")
        else:
            print(f"{folder} 不存在")
