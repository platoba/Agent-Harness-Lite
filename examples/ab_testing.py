"""
A/B测试示例 - 对比不同策略
"""
from harness import Harness

# 策略A
harness_a = Harness(model="strategy-a")

# 策略B
harness_b = Harness(model="strategy-b")

# 相同任务
tasks = ["任务1", "任务2", "任务3", "任务4", "任务5"]

for task in tasks:
    harness_a.run(task)
    harness_b.run(task)

# 对比结果
stats_a = harness_a.get_stats()
stats_b = harness_b.get_stats()

print("策略A:")
print(f"  成功率: {stats_a['success_rate']:.1%}")

print("\n策略B:")
print(f"  成功率: {stats_b['success_rate']:.1%}")

# 导出数据
harness_a.export_dataset("strategy_a_data.json")
harness_b.export_dataset("strategy_b_data.json")
