# 评测说明

- V5 step54 的正式本地 Legacy100 为 44/100；step60 没有跑正式 Legacy100。
- 8/10 视频属于展示用 10-env batch，不替代 44/100 全量结果。
- Official RL 80/100 是官方已训练 checkpoint 的本地 reference，不是本项目训练结果。
- Stage Profiler 来自 V3 step10，用于定位阶段瓶颈，不等同于 V5 的最终 stage success。
- 24 env 失败原因是 host RAM cgroup OOM；V5 固定使用 16 env。
- 完整 checkpoint、仿真缓存和原始训练日志体积较大，不直接提交到 Git。