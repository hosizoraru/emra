from config import *
import shutil
import subprocess
import fnmatch
import json
from apkfile import ApkFile


def init_folder():
    if not os.path.exists("output_apk"):
        os.mkdir("output_apk")

    if not os.path.exists("output_img"):
        os.mkdir("output_img")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def init_json():
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
    subprocess.run(["wget", url])


def extract_payload_bin():
    for f in zip_files:
        subprocess.run(["unzip", f, "payload.bin"])


def extract_product_img():
    subprocess.run(["./payload-dumper-go", "-c", "8", "-output",
                    "output_img", "-p", "product", "payload.bin"])
    for filename in os.listdir("output_img"):
        src_path = os.path.join("output_img", filename)
        dst_path = os.path.join(".", filename)
        os.rename(src_path, dst_path)


def extract_erofs_product():
    subprocess.run(["./extract.erofs", "-i", "product.img", "-x", "-T16"])


def remove_some_apk(exclude_apk):
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.apk') and file not in exclude_apk:
                src = os.path.join(root, file)
                dst = os.path.join(output_dir, file)
                shutil.move(src, dst)
    for root, _, files in os.walk(output_dir):
        for filename in fnmatch.filter(files, "*.apk"):
            if "Overlay" in filename or "_Sys" in filename:
                os.remove(os.path.join(root, filename))


def rename_apk():
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


def update_apk_version(apk_version):
    # 遍历输出目录下的apk文件，并更新本地词典
    for apk_file in os.listdir(output_dir):
        if apk_file.endswith('.apk'):
            x, y = os.path.splitext(apk_file)[0].split('^')
            if x in apk_version:
                if apk_version[x] > y:
                    print(f'更新 {x}：{apk_version[x]} -> {y}')
                    apk_version[x] = y
            else:
                print(f'添加 {x}:{y}')
                apk_version[x] = y

    # 保存本地词典到json文件
    with open(APK_VERSION, 'w') as f:
        json.dump(apk_version, f)


def update_apk_name():
    # 读取第二个词典并修改apk文件名
    if os.path.exists(APK_APP_NAME):
        with open(APK_APP_NAME, 'r') as f:
            apk_name = json.load(f)
    else:
        apk_name = {}

    for apk_file in os.listdir(output_dir):
        if apk_file.endswith('.apk'):
            x, y = os.path.splitext(apk_file)[0].split('^')
            if x in apk_name:
                new_x = apk_name[x]
                new_apk_file = f'{new_x}_{y}.apk'
                os.rename(os.path.join(output_dir, apk_file),
                          os.path.join(output_dir, new_apk_file))
                print(f'修改 {apk_file} -> {new_apk_file}')


def main():
    init_folder()
    exclude_apk, apk_version = init_json()
    choice = input()
    if choice == "1":
        download_rom(input())
    elif choice == "2":
        extract_payload_bin()
    elif choice == "3":
        extract_product_img()
    elif choice == "4":
        extract_erofs_product()
    elif choice == "5":
        remove_some_apk(exclude_apk)
    elif choice == "6":
        rename_apk()
    elif choice == "7":
        update_apk_name()
    elif choice == "8":
        update_apk_version(apk_version)
    else:
        print("error input.")
