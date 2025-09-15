"""字符串工具

提供字符串处理功能
"""
import re
import unicodedata


def slugify(value):
    """将字符串转换为URL友好的格式
    
    Args:
        value: 要转换的字符串
    
    Returns:
        str: 转换后的字符串
    """
    # 将字符串转换为ASCII
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    # 转换为小写
    value = value.lower()
    # 移除非字母数字字符
    value = re.sub(r'[^\w\s-]', '', value)
    # 将空格替换为连字符
    value = re.sub(r'[\s]+', '-', value)
    # 移除连续的连字符
    value = re.sub(r'-+', '-', value)
    # 移除开头和结尾的连字符
    value = value.strip('-')
    
    return value


def truncate(value, length=100, suffix='...'):
    """截断字符串
    
    Args:
        value: 要截断的字符串
        length: 最大长度
        suffix: 截断后添加的后缀
    
    Returns:
        str: 截断后的字符串
    """
    if len(value) <= length:
        return value
    
    return value[:length].rstrip() + suffix


def camel_to_snake(value):
    """将驼峰命名转换为蛇形命名
    
    Args:
        value: 要转换的字符串
    
    Returns:
        str: 转换后的字符串
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel(value):
    """将蛇形命名转换为驼峰命名
    
    Args:
        value: 要转换的字符串
    
    Returns:
        str: 转换后的字符串
    """
    components = value.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])