"""
核心引擎 - 极简设计，零控制流
"""
import time
import uuid
from typing import Dict, Any, Optional
from dataclasses import dataclass
from .data import DataCollector


@dataclass
class TaskResult:
    """任务结果"""
    task_id: str
    success: bool
    output: Any
    error: Optional[str]
    duration: float
    data_path: str
    
    @property
    def failure_data(self) -> Optional[Dict[str, Any]]:
        """失败数据"""
        if not self.success:
            return {
                "task_id": self.task_id,
                "error": self.error,
                "duration": self.duration
            }
        return None


class Harness:
    """
    Agent Harness - 数据驱动的AI运行时
    
    核心原则:
    1. 零控制流 - 不写if/else
    2. 纯数据驱动 - 所有决策来自数据
    3. 为删除而写 - 随时可以重构
    """
    
    def __init__(
        self,
        model: str = "default",
        storage: str = "json",
        storage_path: str = "./data",
        model_config: Optional[Dict[str, Any]] = None
    ):
        self.model = model
        self.storage = storage
        self.storage_path = storage_path
        self.model_config = model_config or {}
        
        # 数据收集器
        self.collector = DataCollector(storage_path)
        
        # 统计
        self._total_tasks = 0
        self._success_count = 0
    
    def run(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None
    ) -> TaskResult:
        """
        执行任务 - 纯数据驱动
        
        不写控制流，不写状态机，让数据说话
        """
        task_id = str(uuid.uuid4())
        start_time = time.time()
        
        try:
            # 执行任务（简化实现）
            output = self._execute(task, context or {})
            
            duration = time.time() - start_time
            success = True
            error = None
            
        except Exception as e:
            duration = time.time() - start_time
            output = None
            success = False
            error = str(e)
        
        # 收集数据
        data_path = self.collector.collect({
            "task_id": task_id,
            "task": task,
            "context": context,
            "output": output,
            "success": success,
            "error": error,
            "duration": duration,
            "model": self.model,
            "timestamp": time.time()
        })
        
        # 更新统计
        self._total_tasks += 1
        if success:
            self._success_count += 1
        
        return TaskResult(
            task_id=task_id,
            success=success,
            output=output,
            error=error,
            duration=duration,
            data_path=data_path
        )
    
    def _execute(self, task: str, context: Dict[str, Any]) -> Any:
        """
        执行任务（简化实现）
        
        实际应用中，这里会调用LLM API
        """
        # 简化实现：返回任务描述
        return {
            "task": task,
            "context": context,
            "result": f"Executed: {task}"
        }
    
    @property
    def success_rate(self) -> float:
        """成功率"""
        if self._total_tasks == 0:
            return 0.0
        return self._success_count / self._total_tasks
    
    def get_dataset(self):
        """获取数据集"""
        return self.collector.get_dataset()
    
    def export_dataset(self, path: str, format: str = "json"):
        """导出数据集"""
        return self.collector.export(path, format)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_tasks": self._total_tasks,
            "success_count": self._success_count,
            "failure_count": self._total_tasks - self._success_count,
            "success_rate": self.success_rate,
            "model": self.model
        }
