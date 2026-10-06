# Stage Profiler

V3 step10 的阶段统计：

| Stage | 累计通过 | 条件通过率 |
|---|---:|---:|
| Lift | 18/20（90%） | — |
| Align | 15/20（75%） | 15/18（83.3%） |
| Insert | 8/20（40%） | 8/15（53.3%） |
| Place | 8/20（40%） | 8/8（100%） |

主要损失发生在 **Align → Insert**：15 条完成 Align 的轨迹只有 8 条进入 Insert。Insert 完成后，8/8 最终通过 Place。

Profiler 的唯一轨迹 ID 最终使用 `(seed, EnvWorker PID, local env_id)`；只用 `(seed, env_id)` 会把不同 worker 的 local env 误合并。