# EMRA - Extract, MIUI, Rename APKs

EMRA 是一个用于提取、修改和重命名 Android ROM 中的 APK 文件的 Python 脚本。它可以帮助开发者和用户轻松地获取 APK 文件，并根据需要对其进行定制。

## 功能

- 从 ROM 下载链接下载 ROM
- 从 ZIP 文件中提取 payload.bin
- 从 payload.bin 文件中提取 product.img
- 提取 erofs 镜像
- 删除指定的 APK
- 重命名 APK 文件
- 更新 APK 版本
- 更新 APK 文件名
- 删除多余文件

## 如何使用

1. 确保已安装 Python 3.x，并安装以下依赖库：
    ```
    pip install apkfile
    ```

2. 克隆此仓库或下载脚本文件：
    ```
    git clone https://github.com/hosizoraru/emra.git
    ```

3. 运行脚本：
    ```
    python main.py
    ```

4. 按照提示选择相应的操作。

## 贡献

欢迎向该项目提出改进建议或提交错误报告。请通过 [GitHub Issues](https://github.com/hosizoraru/emra/issues) 提交。

## 许可证

本项目基于 [WTFPL License](https://github.com/rpherrera/WTFPL/blob/master/LICENSE) 许可。
