from loguru import logger
import sys
import argparse

from src import check_dependencies, write_list_to_file, copy_dependencies, zip_folder, unzip_file, read_list_from_file, \
    execute_list

try:
    from restore_dependencies import __version__ as version
except ImportError:
    version = None

if len(sys.argv) == 1:
    sys.argv.append('--help')
try:
    from __init__ import __description__

    parser = argparse.ArgumentParser(description=__description__)
except ImportError:
    parser = argparse.ArgumentParser(description='restore_dependencies')

parser.add_argument('-v', '--version', help=f"显示版本;当前版本：{version}", action="store_true")
parser.add_argument('-f', '--found', type=str,
                    help='在缺少依赖的环境中执行,后跟需要检查的c++程序；查找c++程序的依赖,并将缺失的依赖记录至dependencies.txt中')
parser.add_argument('-c', '--copy', type=str,
                    help='在拥有依赖的环境中执行；复制缺失的依赖到lib路径下，并记录还原缺失依赖命令到cp_dep.txt中,然后将lib打包为lib.zip')
parser.add_argument('-r', '--restore', type=str,
                    help='在缺少依赖的环境中执行；根据cp_dep.txt中的命令，解压lib.zip并还原缺失的依赖')


def main():
    # 定义要记录not found的依赖名的文件路径
    file = "dependencies.txt"
    # 定义要复制依赖的文件夹路径
    folder = "lib"
    # 定义要记录还原命令的文件路径
    command_file = "cp_dep.txt"
    # 定义要压缩和解压的zip文件路径
    zip_file = "lib.zip"

    args = parser.parse_args()
    if args.version:
        logger.info(f"当前版本：{version}")
        exit(0)
    arguments = parser.parse_args()

    if args.found:
        # 调用check_dependencies函数，获取not found的依赖名列表
        not_found = check_dependencies(arguments.found)
        # 调用write_list_to_file函数，将依赖名列表写入到指定的文件中
        write_list_to_file(not_found, file)
    if args.copy:
        # 在有对应依赖的电脑上，调用copy_dependencies函数，根据文件内容，查找并复制依赖到指定文件夹内，并获取还原命令列表
        restore_commands = copy_dependencies(file, folder)
        # 调用write_list_to_file函数，将还原命令列表写入到指定的文件中
        write_list_to_file(restore_commands, command_file)
        # 调用zip_folder函数，将指定的文件夹压缩为一个zip文件
        zip_folder(folder, zip_file)
    if args.restore:
        # 在缺少依赖的电脑上，调用unzip_file函数，将指定的zip文件解压到一个文件夹中
        unzip_file(zip_file, folder)
        # # 调用read_list_from_file函数，从指定的文件中读取还原命令列表
        restore_commands = read_list_from_file(command_file)
        # 调用execute_list函数，根据还原命令列表，执行每一条命令，将依赖复制到原来的位置
        execute_list(restore_commands)
    if not arguments.input:
        logger.error("参数为必填项")


if __name__ == '__main__':
    main()
