import os
import shutil
import subprocess
import sys
from datetime import datetime

# GalSceneEditor 打包脚本
# 这个脚本使用PyInstaller将项目打包成可执行文件

def main():
    print("开始打包GalSceneEditor...")
    
    # 获取当前目录（使用os.getcwd()确保获取正确的当前工作目录）
    current_dir = os.getcwd()
    print(f"当前工作目录: {current_dir}")
    
    # 明确设置输出目录为当前工作目录下的dist
    dist_dir = os.path.join(current_dir, 'dist')
    build_dir = os.path.join(current_dir, 'build')
    spec_file = os.path.join(current_dir, 'GalSceneEditor.spec')
    
    print(f"输出目录设置为: {dist_dir}")
    
    # 尝试创建输出目录（如果不存在）
    if not os.path.exists(dist_dir):
        try:
            os.makedirs(dist_dir)
            print(f"已创建输出目录: {dist_dir}")
        except Exception as e:
            print(f"创建输出目录失败: {str(e)}")
    
    # 清理之前的构建文件
    build_dir = os.path.join(current_dir, 'build')
    dist_dir = os.path.join(current_dir, 'dist')
    spec_file = os.path.join(current_dir, 'GalSceneEditor.spec')
    
    # 尝试清理build目录，处理可能的权限错误
    if os.path.exists(build_dir):
        try:
            print(f"清理目录: {build_dir}")
            shutil.rmtree(build_dir)
        except PermissionError:
            print(f"警告: 无法完全清理{build_dir}，可能有文件正在被占用")
    
    # 尝试清理dist目录，处理可能的权限错误
    if os.path.exists(dist_dir):
        try:
            print(f"清理目录: {dist_dir}")
            shutil.rmtree(dist_dir)
        except PermissionError:
            print(f"警告: 无法完全清理{dist_dir}，可能有文件正在被占用")
            # 继续执行，PyInstaller可能会覆盖现有文件
    
    # 尝试删除spec文件
    if os.path.exists(spec_file):
        try:
            print(f"删除文件: {spec_file}")
            os.remove(spec_file)
        except PermissionError:
            print(f"警告: 无法删除{spec_file}，可能有文件正在被占用")
    
    # 执行PyInstaller命令
    print("正在执行PyInstaller命令...")
    
    # 构建正确的资源路径格式
    resources_path = os.path.join(current_dir, 'resources')
    # Windows系统下使用分号作为路径分隔符
    add_data_param = f'{resources_path};resources'
    
    # 构建图标路径
    icon_path = os.path.join(current_dir, 'resources', 'icon', 'GalSceneEditor.ico')
    
    # 构建主脚本路径
    main_script = os.path.join(current_dir, 'src', 'main.py')
    
    cmd = [
        'pyinstaller',
        '--name=GalSceneEditor',
        '--onefile',
        '--windowed',
        f'--distpath={dist_dir}',
        f'--workpath={build_dir}',
        f'--add-data={add_data_param}',
        f'--icon={icon_path}',
        main_script
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"PyInstaller输出: {result.stdout}")
    except subprocess.CalledProcessError as e:
        # 检查是否是权限错误
        if "拒绝访问" in e.stderr or "PermissionError" in e.stderr:
            print(f"警告: 打包过程中出现权限错误，可能有文件正在被使用: {e.stderr}")
            # 尝试手动重命名或跳过
            if os.path.exists(os.path.join(dist_dir, 'GalSceneEditor.exe')):
                try:
                    # 重命名现有文件以允许新文件生成
                    old_exe = os.path.join(dist_dir, 'GalSceneEditor.exe')
                    new_exe = os.path.join(dist_dir, f"GalSceneEditor_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.exe")
                    os.rename(old_exe, new_exe)
                    print(f"已将现有可执行文件重命名为: {new_exe}")
                    # 再次尝试运行打包命令
                    print("正在尝试再次打包...")
                    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                    print(f"PyInstaller输出: {result.stdout}")
                except Exception as inner_e:
                    print(f"重命名文件或再次打包失败: {str(inner_e)}")
                    sys.exit(1)
        else:
            print(f"打包失败！错误: {e.stderr}")
            sys.exit(1)
    
    # 复制资源文件到dist目录（额外保障）
    print("正在复制资源文件到dist目录...")
    resources_src = resources_path
    resources_dst = os.path.join(dist_dir, 'resources')
    
    if os.path.exists(resources_dst):
        shutil.rmtree(resources_dst)
    
    shutil.copytree(resources_src, resources_dst)
    
    # 复制文档文件
    print("正在复制文档文件...")
    files_to_copy = ['README.md', 'LICENSE']
    for file in files_to_copy:
        src_file = os.path.join(current_dir, file)
        dst_file = os.path.join(dist_dir, file)
        if os.path.exists(src_file):
            shutil.copy2(src_file, dst_file)
    
    # 在dist目录下创建output文件夹
    output_dir = os.path.join(dist_dir, 'output')
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"已在dist目录下创建output文件夹: {output_dir}")
        except Exception as e:
            print(f"创建output文件夹失败: {str(e)}")
    
    print("打包完成！可执行文件位于 dist 目录下")

if __name__ == '__main__':
    main()