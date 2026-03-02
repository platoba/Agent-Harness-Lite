"""
测试Harness核心功能
"""
import pytest
import tempfile
from pathlib import Path
from harness import Harness


@pytest.fixture
def temp_storage():
    """临时存储目录"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_harness_initialization(temp_storage):
    """测试初始化"""
    harness = Harness(storage_path=temp_storage)
    assert harness.model == "default"
    assert harness.storage == "json"


def test_run_task(temp_storage):
    """测试执行任务"""
    harness = Harness(storage_path=temp_storage)
    
    result = harness.run(
        task="测试任务",
        context={"key": "value"}
    )
    
    assert result.task_id is not None
    assert result.success is True
    assert result.output is not None
    assert result.duration >= 0


def test_success_rate(temp_storage):
    """测试成功率"""
    harness = Harness(storage_path=temp_storage)
    
    # 执行多个任务
    for i in range(5):
        harness.run(f"任务{i}")
    
    assert harness.success_rate == 1.0
    assert harness._total_tasks == 5


def test_get_dataset(temp_storage):
    """测试获取数据集"""
    harness = Harness(storage_path=temp_storage)
    
    # 执行任务
    harness.run("任务1")
    harness.run("任务2")
    
    dataset = harness.get_dataset()
    assert dataset.total_tasks == 2
    assert dataset.success_count == 2
    assert dataset.success_rate == 1.0


def test_export_dataset(temp_storage):
    """测试导出数据集"""
    harness = Harness(storage_path=temp_storage)
    
    # 执行任务
    harness.run("任务1")
    
    # 导出JSON
    json_path = Path(temp_storage) / "export.json"
    harness.export_dataset(str(json_path), format="json")
    assert json_path.exists()
    
    # 导出CSV
    csv_path = Path(temp_storage) / "export.csv"
    harness.export_dataset(str(csv_path), format="csv")
    assert csv_path.exists()


def test_get_stats(temp_storage):
    """测试获取统计"""
    harness = Harness(storage_path=temp_storage)
    
    harness.run("任务1")
    harness.run("任务2")
    
    stats = harness.get_stats()
    assert stats["total_tasks"] == 2
    assert stats["success_count"] == 2
    assert stats["failure_count"] == 0
    assert stats["success_rate"] == 1.0
