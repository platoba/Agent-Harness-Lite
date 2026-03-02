"""
失败学习示例 - 数据驱动进化
"""
from harness import Harness

harness = Harness()

# 模拟多次任务
tasks = [
    "简单任务1",
    "简单任务2",
    "复杂任务（可能失败）",
    "简单任务3",
]

for task in tasks:
    result = harness.run(task)
    
    if result.success:
        print(f"✅ {task}: 成功")
    else:
        print(f"❌ {task}: 失败 - {result.error}")
        print(f"   失败数据已保存: {result.data_path}")

# 查看数据集
dataset = harness.get_dataset()
print(f"\n数据集统计:")
print(f"总任务: {dataset.total_tasks}")
print(f"成功: {dataset.success_count}")
print(f"失败: {dataset.failure_count}")
print(f"成功率: {dataset.success_rate:.1%}")

# 导出数据
harness.export_dataset("training_data.json")
print(f"\n数据已导出: training_data.json")
