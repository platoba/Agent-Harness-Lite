"""
基础示例 - 零控制流
"""
from harness import Harness

# 初始化
harness = Harness()

# 执行任务（纯数据驱动）
result = harness.run(
    task="分析这段代码的性能问题",
    context={"code": "def slow_function(): ..."}
)

print(f"任务ID: {result.task_id}")
print(f"成功: {result.success}")
print(f"输出: {result.output}")
print(f"耗时: {result.duration*1000:.2f}ms")

# 获取统计
stats = harness.get_stats()
print(f"\n统计:")
print(f"总任务数: {stats['total_tasks']}")
print(f"成功率: {stats['success_rate']:.1%}")
