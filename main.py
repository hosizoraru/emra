from config import *  # 从config.py模块中导入所有内容
from defs import *  # 从defs.py模块中导入所有内容
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="EMRA: A tool to process Android ROM and APK files")

    parser.add_argument('-d', '--download', metavar='URL',
                        help='Download ROM from given URL')
    parser.add_argument('-e', '--extract-payload', action='store_true',
                        help='Extract payload.bin from zip files')
    parser.add_argument('-p', '--product-img', action='store_true',
                        help='Extract product.img from payload.bin')
    parser.add_argument('-r', '--erofs', action='store_true',
                        help='Extract files from EROFS product.img')
    parser.add_argument('-a', '--apk', action='store_true',
                        help='Remove specified APKs')
    parser.add_argument('-n', '--rename', action='store_true',
                        help='Rename APK files')
    parser.add_argument('-u', '--update-version',
                        action='store_true', help='Update APK versions')
    parser.add_argument('-m', '--update-name',
                        action='store_true', help='Update APK names')
    parser.add_argument('-c', '--clean', action='store_true',
                        help='Delete unnecessary files and folders')

    return parser.parse_args()


def main():
    args = parse_arguments()

    init_folder()
    exclude_apk, apk_version, apk_code = init_json()

    if args.download:
        download_rom(args.download)
    if args.extract_payload:
        extract_payload_bin(zip_files)
    if args.product_img:
        extract_product_img()
    if args.erofs:
        extract_erofs_product()
    if args.apk:
        remove_some_apk(exclude_apk)
    if args.rename:
        rename_apk(apk_files)
    if args.update_version:
        update_apk_version(apk_version, apk_code)
    if args.update_name:
        update_apk_name()
    if args.clean:
        delete_files_and_folders()


if __name__ == "__main__":  # 如果这个脚本文件是被直接运行的
    main()  # 调用main()函数
