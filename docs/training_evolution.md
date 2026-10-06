# 训练路线

| 版本 | 主要变化 | 结果 / 结论 |
|---|---|---|
| V1 | 8 env，micro2/global4，10 updates | 跑通 Full-FT PPO；critic 早期出现 EV NaN warning |
| V2 | 尝试 24 env，后改 16 env / global1024 / actor LR 5e-6 | 24 env 因 host RAM OOM 失败；16 env 稳定；actor 更新偏保守 |
| V3 | global512 / actor LR 1e-5 | 更新更明显，但成功率没有持续提高；转向 Stage Profiler |
| V4 | progressive sparse stage curriculum | 做过自动 stage handoff，但最终不作为正式主线 |
| V5 | clean SFT → direct Stage4 full-task PPO | 最终路线；60/60 updates 完成 |

V3 的 Stage Profiler 把主要瓶颈定位到 **Align → Insert**，因此后续分析重点转向接触丰富的精细对准与插入，而不是只看整体 success。

V5 回到最简单、可解释的 full-task PPO 路线，避免把自定义 stage handoff 混入最终结果。