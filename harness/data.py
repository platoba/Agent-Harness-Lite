"""
数据收集器 - Harness = Dataset
"""
import json
import csv
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class Dataset:
    """数据集"""
    total_tasks: int
    success_count: int
    failure_count: int
    success_rate: float
    avg_duration: float
    data: List[Dict[str, Any]]


class DataCollector:
    """
    数据收集器
    
    核心价值: 数据就是护城河
    """
    
    def __init__(self, storage_path: str = "./data"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.data_file = self.storage_path / "harness_data.jsonl"
        self.data_file.touch()
    
    def collect(self, data: Dict[str, Any]) -> str:
        """
        收集数据
        
        每次交互都是宝贵的数据
        """
        # 追加到JSONL文件
        with open(self.data_file, "a") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
        
        return str(self.data_file)
    
    def get_dataset(self) -> Dataset:
        """获取数据集"""
        data = []
        total_duration = 0
        success_count = 0
        
        with open(self.data_file, "r") as f:
            for line in f:
                if line.strip():
                    record = json.loads(line)
                    data.append(record)
                    total_duration += record.get("duration", 0)
                    if record.get("success"):
                        success_count += 1
        
        total_tasks = len(data)
        failure_count = total_tasks - success_count
        success_rate = success_count / total_tasks if total_tasks > 0 else 0
        avg_duration = total_duration / total_tasks if total_tasks > 0 else 0
        
        return Dataset(
            total_tasks=total_tasks,
            success_count=success_count,
            failure_count=failure_count,
            success_rate=success_rate,
            avg_duration=avg_duration * 1000,  # ms
            data=data
        )
    
    def export(self, path: str, format: str = "json"):
        """导出数据集"""
        dataset = self.get_dataset()
        path = Path(path)
        
        if format == "json":
            with open(path, "w") as f:
                json.dump(dataset.data, f, indent=2, ensure_ascii=False)
        
        elif format == "csv":
            if dataset.data:
                keys = dataset.data[0].keys()
                with open(path, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(dataset.data)
        
        return str(path)
