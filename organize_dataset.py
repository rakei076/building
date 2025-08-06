#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
花卉数据集整理脚本
将樱花、银杏、枫叶图片按80/20比例分配到训练集和测试集
"""

import os
import shutil
import random
from pathlib import Path

def organize_flower_dataset():
    """整理花卉数据集"""
    
    # 设置随机种子以确保可重现的结果
    random.seed(42)
    
    # 源目录和目标目录
    source_dir = Path("樱花等测试集")
    target_dir = Path("flower_dataset")
    
    # 类别映射 (原文件夹名 -> 新类别名)
    category_mapping = {
        "ichō": "icho",      # 银杏
        "momiji": "momiji",  # 枫叶
        "Sakura": "sakura"   # 樱花
    }
    
    print("开始整理花卉数据集...")
    print("=" * 50)
    
    # 处理每个类别
    for original_name, category_name in category_mapping.items():
        source_category_dir = source_dir / original_name
        
        if not source_category_dir.exists():
            print(f"警告: 源目录 {source_category_dir} 不存在，跳过...")
            continue
        
        # 获取所有图片文件
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
            image_files.extend(source_category_dir.glob(ext))
        
        # 过滤掉.DS_Store等系统文件
        image_files = [f for f in image_files if not f.name.startswith('.')]
        image_files.sort(key=lambda x: int(x.stem) if x.stem.isdigit() else 0)
        
        total_images = len(image_files)
        train_count = int(total_images * 0.8)  # 80%用于训练
        test_count = total_images - train_count  # 20%用于测试
        
        print(f"\n处理类别: {category_name} ({original_name})")
        print(f"总图片数: {total_images}")
        print(f"训练集: {train_count} 张")
        print(f"测试集: {test_count} 张")
        
        # 随机打乱图片列表
        random.shuffle(image_files)
        
        # 分配到训练集
        train_dir = target_dir / "train" / category_name
        for i, image_file in enumerate(image_files[:train_count]):
            # 统一文件扩展名为.jpg
            new_filename = f"{category_name}-{i+1:02d}.jpg"
            target_path = train_dir / new_filename
            
            try:
                shutil.copy2(image_file, target_path)
                print(f"  训练集: {image_file.name} -> {new_filename}")
            except Exception as e:
                print(f"  错误: 复制 {image_file.name} 失败: {e}")
        
        # 分配到测试集
        test_dir = target_dir / "test" / category_name
        for i, image_file in enumerate(image_files[train_count:]):
            # 统一文件扩展名为.jpg
            new_filename = f"{category_name}-{i+1:02d}.jpg"
            target_path = test_dir / new_filename
            
            try:
                shutil.copy2(image_file, target_path)
                print(f"  测试集: {image_file.name} -> {new_filename}")
            except Exception as e:
                print(f"  错误: 复制 {image_file.name} 失败: {e}")
    
    print("\n" + "=" * 50)
    print("数据集整理完成！")
    
    # 显示最终统计
    print("\n最终数据集统计:")
    for split in ['train', 'test']:
        print(f"\n{split.upper()}:")
        split_dir = target_dir / split
        for category in ['icho', 'momiji', 'sakura']:
            category_dir = split_dir / category
            if category_dir.exists():
                count = len(list(category_dir.glob('*.jpg')))
                print(f"  {category}: {count} 张图片")

if __name__ == "__main__":
    organize_flower_dataset() 