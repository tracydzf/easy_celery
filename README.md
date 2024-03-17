# Easy Celery

Easy Celery 是一个旨在简化 Celery 在生产环境中无缝集成和高效使用的全面指南和实用工具集。Celery 是一个广泛用于 Python 应用程序的分布式任务队列，用于异步和实时执行任务。

## 功能特性

- 简化的 Celery 配置
- 流畅的日志设置---logurus输出json格式日志
- 高效的异步函数配置---asyncio
- 任务结果追踪----结果保存
- 全面的任务监控---statsd埋点，flower结合grafana

## 使用技巧

### Celery 配置

配置 Celery 可能很复杂，但 Easy Celery 通过提供直观的配置选项来简化此过程。您只需按照提供的指南即可轻松为项目设置 Celery。

### 启动

```shell
 celery -A app worker -l info 
```


