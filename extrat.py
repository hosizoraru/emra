import os
import shutil
import subprocess
import glob
import fnmatch
from apkfile import ApkFile
import json

src_dir = os.path.abspath(__file__)

if not os.path.exists("output_apk"):
    os.mkdir("output_apk")
    
if not os.path.exists("output_img"):
    os.mkdir("output_img")

src_img_dir = "output_img"
dst_back_dir = "."

dst_dir = os.path.join(src_dir, "output_apk")

url = input("请输入下载链接: ")
subprocess.run(["wget", url])

zip_files = glob.glob("*.zip")

for f in zip_files:
    subprocess.run(["unzip", f, "payload.bin"])
    
subprocess.run(["./payload-dumper-go", "-c", "8", "-output", "output_img", "-p", "product", "payload.bin"])

for filename in os.listdir(src_img_dir):
    src_path = os.path.join(src_img_dir, filename)
    dst_path = os.path.join(dst_back_dir, filename)
    os.rename(src_path, dst_path)
    
subprocess.run(["./extract.erofs", "-i", "product.img", "-x", "-T16"])

# 将排除的文件列表独立到一个文件中
EXCLUDE_FILE_PATH = 'exclude_files.txt'
exclude_files = []

if os.path.exists(EXCLUDE_FILE_PATH):
    with open(EXCLUDE_FILE_PATH, 'r') as f:
        exclude_files = [line.strip() for line in f.readlines()]

output_dir = 'output_apk'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.apk') and file not in exclude_files:
            src = os.path.join(root, file)
            dst = os.path.join(output_dir, file)
            shutil.move(src, dst)
            
for root, dirs, files in os.walk(output_dir):
    for filename in fnmatch.filter(files, "*.apk"):
        if "Overlay" in filename or "_Sys" in filename:
            os.remove(os.path.join(root, filename))

# 获取当前文件夹下所有以.apk为后缀的文件
apk_files = [f for f in os.listdir('output_apk') if f.endswith('.apk')]

# 遍历每个apk文件
for apk_file in apk_files:
    apk_path = os.path.join('output_apk', apk_file)

    # 使用apkfile库读取apk包信息
    apk = ApkFile(apk_path)

    # 获取apk的包名和版本号
    package_name = apk.package_name
    version_name = apk.version_name
    version_code = apk.version_code

    # 构建新文件名
    new_name = f"{package_name}^{version_name}.apk"

    # 重命名apk文件
    os.rename(apk_path, os.path.join('output_apk', new_name))

# 读取本地词典
LOCAL_DICT_FILE = 'local_dict.json'

if os.path.exists(LOCAL_DICT_FILE):
    with open(LOCAL_DICT_FILE, 'r') as f:
        local_dict = json.load(f)
else:
    local_dict = {}

# 遍历输出目录下的apk文件，并更新本地词典
APK_DIR = 'output_apk'

for apk_file in os.listdir(APK_DIR):
    if apk_file.endswith('.apk'):
        x, y = os.path.splitext(apk_file)[0].split('^')
        if x in local_dict:
            if local_dict[x] != y:
                print(f'更新 {x}：{local_dict[x]} -> {y}')
                local_dict[x] = y
        else:
            print(f'添加 {x}:{y}')
            local_dict[x] = y

# 保存本地词典到json文件
with open(LOCAL_DICT_FILE, 'w') as f:
    json.dump(local_dict, f)

# 读取第二个词典并修改apk文件名
SECOND_DICT_FILE = 'second_dict.json'

if os.path.exists(SECOND_DICT_FILE):
    with open(SECOND_DICT_FILE, 'r') as f:
        second_dict = json.load(f)
else:
    second_dict = {}

for apk_file in os.listdir(APK_DIR):
    if apk_file.endswith('.apk'):
        x, y = os.path.splitext(apk_file)[0].split('^')
        if x in second_dict:
            new_x = second_dict[x]
            new_apk_file = f'{new_x}_{y}.apk'
            os.rename(os.path.join(APK_DIR, apk_file), os.path.join(APK_DIR, new_apk_file))
            print(f'修改 {apk_file} -> {new_apk_file}')

