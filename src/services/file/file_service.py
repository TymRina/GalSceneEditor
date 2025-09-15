"""

提供统一的文件操作功能，使用pathlib.Path处理路径
"""
import json
import os
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List, Union
from utils.helpers.logger import log_error, log_debug, log_warning


class FileService:
    """文件服务，负责统一的文件操作"""
    
    @staticmethod
    def ensure_directory(directory_path: str) -> bool:
        """确保目录存在，如果不存在则创建
        
        Args:
            directory_path: 目录路径
            
        Returns:
            bool: 是否成功创建或目录已存在
        """
        try:
            Path(directory_path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            log_error(f"创建目录失败: {e}")
            return False
    
    @staticmethod
    def load_json(file_path: str) -> Optional[Dict[str, Any]]:
        """从文件加载JSON数据
        
        Args:
            file_path: 文件路径
            
        Returns:
            Optional[Dict[str, Any]]: 加载的数据，如果失败则返回None
        """
        try:
            if not file_path:
                log_debug("文件路径为空")
                return None
            
            path = Path(file_path)
            if not path.exists():
                log_debug(f"文件不存在: {file_path}")
                return None
            
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            log_error(f"JSON格式错误: {file_path}")
            return None
        except UnicodeDecodeError:
            log_error(f"编码错误: {file_path}")
            return None
        except Exception as e:
            log_error(f"加载文件失败: {file_path}, 错误: {str(e)}")
            return None
    
    @staticmethod
    def save_json(file_path: str, data: Dict[str, Any]) -> bool:
        """将JSON数据保存到文件
        
        Args:
            file_path: 文件路径
            data: 要保存的数据
            
        Returns:
            bool: 是否成功保存
        """
        try:
            if not file_path:
                log_debug("保存文件路径为空")
                return False
            
            # 确保输出目录存在
            path = Path(file_path)
            output_dir = path.parent
            if not FileService.ensure_directory(str(output_dir)):
                return False
            
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except TypeError as e:
            log_error(f"数据类型错误，无法序列化: {str(e)}")
            return False
        except PermissionError:
            log_warning(f"无权限写入文件: {file_path}")
            return False
        except Exception as e:
            log_error(f"保存文件失败: {file_path}, 错误: {str(e)}")
            return False
    
    @staticmethod
    def copy_file(source_path: str, destination_path: str) -> bool:
        """复制文件
        
        Args:
            source_path: 源文件路径
            destination_path: 目标文件路径
            
        Returns:
            bool: 是否成功复制
        """
        try:
            if not source_path or not destination_path:
                log_debug("源文件路径或目标文件路径为空")
                return False
            
            source = Path(source_path)
            if not source.exists():
                log_debug(f"源文件不存在: {source_path}")
                return False
            
            # 确保目标目录存在
            destination = Path(destination_path)
            output_dir = destination.parent
            if not FileService.ensure_directory(str(output_dir)):
                return False
            
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            log_error(f"复制文件失败: {e}")
            return False
    
    @staticmethod
    def get_file_name_without_extension(file_path: str) -> str:
        """获取不带扩展名的文件名
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 不带扩展名的文件名
        """
        if not file_path:
            return ""
        
        return Path(file_path).stem
    
    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """获取文件扩展名
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 文件扩展名（小写）
        """
        if not file_path:
            return ""
        
        return Path(file_path).suffix.lower()
    
    @staticmethod
    def scan_directory(directory_path: str, extensions: Optional[List[str]] = None) -> List[Tuple[str, str]]:
        """扫描目录中的文件
        
        Args:
            directory_path: 目录路径
            extensions: 文件扩展名列表，只扫描指定扩展名的文件
            
        Returns:
            List[Tuple[str, str]]: (文件名, 文件路径)的列表
        """
        results = []
        try:
            if not directory_path:
                log_debug("目录路径为空")
                return results
            
            dir_path = Path(directory_path)
            if not dir_path.exists():
                log_debug(f"目录不存在: {directory_path}")
                return results
            
            # 标准化扩展名格式，确保都包含点号
            normalized_extensions = None
            if extensions:
                normalized_extensions = []
                for ext in extensions:
                    if not ext.startswith('.'):
                        ext = '.' + ext
                    normalized_extensions.append(ext.lower())
            
            for root, _, files in os.walk(str(directory_path)):
                for file in files:
                    file_path = str(Path(root) / file)
                    
                    # 检查文件扩展名
                    if normalized_extensions:
                        if FileService.get_file_extension(file_path) in normalized_extensions:
                            results.append((FileService.get_file_name_without_extension(file), file_path))
                    else:
                        results.append((FileService.get_file_name_without_extension(file), file_path))
            return results
        except Exception as e:
            log_error(f"扫描目录失败: {e}")
        
        return results
    
    @staticmethod
    def save_xml(file_path: str, data: Dict[str, Any]) -> bool:
        """将数据保存为XML格式
        
        Args:
            file_path: 文件路径
            data: 要保存的数据
            
        Returns:
            bool: 是否成功保存
        """
        try:
            if not file_path:
                log_debug("保存文件路径为空")
                return False
            
            # 确保输出目录存在
            path = Path(file_path)
            output_dir = path.parent
            if not FileService.ensure_directory(str(output_dir)):
                return False
            
            # 将数据转换为XML格式
            root = FileService.convert_json_to_xml(data)
            
            # 创建XML树并写入文件
            tree = ET.ElementTree(root)
            
            # 定义XML声明
            xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>'
            
            # 格式化XML并写入文件
            with open(path, 'w', encoding='utf-8') as f:
                f.write(xml_declaration + '\n')
                FileService._indent(root)
                tree.write(f, encoding='unicode', xml_declaration=False)
            
            return True
        except Exception as e:
            log_error(f"保存XML文件失败: {file_path}, 错误: {str(e)}")
            return False
    
    @staticmethod
    def load_xml(file_path: str) -> Optional[Dict[str, Any]]:
        """从XML文件加载数据
        
        Args:
            file_path: 文件路径
            
        Returns:
            Optional[Dict[str, Any]]: 加载的数据，如果失败则返回None
        """
        try:
            if not file_path:
                log_debug("文件路径为空")
                return None
            
            path = Path(file_path)
            if not path.exists():
                log_debug(f"文件不存在: {file_path}")
                return None
            
            # 解析XML文件
            tree = ET.parse(path)
            root = tree.getroot()
            
            # 将XML转换为JSON格式
            data = FileService.convert_xml_to_json(root)
            
            return data
        except ET.ParseError as e:
            log_error(f"XML解析错误: {file_path}, 错误: {str(e)}")
            return None
        except UnicodeDecodeError:
            log_error(f"编码错误: {file_path}")
            return None
        except Exception as e:
            log_error(f"加载XML文件失败: {file_path}, 错误: {str(e)}")
            return None
    
    @staticmethod
    def convert_json_to_xml(data: Any, parent_tag: str = 'root') -> ET.Element:
        """将JSON数据转换为XML元素
        
        Args:
            data: JSON数据
            parent_tag: 父元素标签名
        
        Returns:
            ET.Element: XML元素
        """
        # 处理特殊标签名，避免与XML/HTML保留标签冲突
        tag_map = {
            'audio': 'audio_data',  # 重命名audio标签以避免特殊处理
        }
        
        # 确保标签名合法（不能包含空格等特殊字符）
        safe_parent_tag = parent_tag.replace(' ', '_')
        # 应用标签映射
        safe_parent_tag = tag_map.get(safe_parent_tag, safe_parent_tag)
        
        root = ET.Element(safe_parent_tag)
        
        if isinstance(data, dict):
            for key, value in data.items():
                # 确保键名合法
                safe_key = key.replace(' ', '_')
                # 应用标签映射
                safe_key = tag_map.get(safe_key, safe_key)
                # 处理特殊情况：如果值是字典或列表，递归处理
                if isinstance(value, (dict, list)):
                    child = FileService.convert_json_to_xml(value, safe_key)
                    root.append(child)
                else:
                    # 普通值作为元素内容
                    element = ET.SubElement(root, safe_key)
                    if value is not None:
                        element.text = str(value)
        elif isinstance(data, list):
            # 列表元素使用统一的item标签
            for index, item in enumerate(data):
                item_tag = f"{safe_parent_tag}_item"
                child = FileService.convert_json_to_xml(item, item_tag)
                # 添加索引属性
                child.set('index', str(index))
                root.append(child)
        else:
            # 基本数据类型直接作为文本内容
            if data is not None:
                root.text = str(data)
        
        return root
    
    @staticmethod
    def convert_xml_to_json(element: ET.Element) -> Any:
        """将XML元素转换为JSON数据
        
        Args:
            element: XML元素
        
        Returns:
            Any: 转换后的JSON数据
        """
        # 定义反向标签映射，用于还原特殊标签名
        reverse_tag_map = {
            'audio_data': 'audio',
        }
        
        result = {}
        
        # 处理属性
        if element.attrib:
            result['@attributes'] = element.attrib
        
        # 处理子元素
        children = list(element)
        if children:
            child_dict = {}
            for child in children:
                # 应用反向标签映射
                tag_name = reverse_tag_map.get(child.tag, child.tag)
                child_data = FileService.convert_xml_to_json(child)
                
                if tag_name in child_dict:
                    # 如果有多个相同标签的子元素，转换为列表
                    if not isinstance(child_dict[tag_name], list):
                        child_dict[tag_name] = [child_dict[tag_name]]
                    child_dict[tag_name].append(child_data)
                else:
                    child_dict[tag_name] = child_data
            result.update(child_dict)
        
        # 处理文本内容
        text = element.text.strip() if element.text else ""
        if text and not children:
            # 如果没有子元素但有文本内容，直接返回文本值
            # 尝试转换为数字类型
            if text.isdigit():
                return int(text)
            try:
                return float(text)
            except ValueError:
                # 如果不是数字，返回字符串
                return text
        elif text:
            result['#text'] = text
        
        return result
    
    @staticmethod
    def _indent(elem: ET.Element, level: int = 0) -> None:
        """为XML元素添加缩进，使XML文件格式更美观
        
        Args:
            elem: XML元素
            level: 当前缩进级别
        """
        i = "\n" + level * "    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "    "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                FileService._indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i