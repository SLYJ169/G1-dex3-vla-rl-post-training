# 评测协议

## Legacy100

正式对比使用 10×10 的本地 Legacy100 evaluation protocol，共 100 条 rollout。日志中存在 fixed reset state 配置，但没有证据证明 100 个场景数学上完全唯一，因此不写成“100 个严格唯一 deterministic scenes”。

| 模型 | Success | Mean return |
|---|---:|---:|
| Clean SFT | 35/100 | 2.580 |
| V5 step54 | **44/100** | **2.830** |
| Official RL checkpoint | 80/100 | 4.350 |

Official RL checkpoint 是官方已训练模型在本地同任务下的 reference，不是 V5 训练产物。

`step60` 没有跑正式 Legacy100，因此没有填写 step60 的全量结果。

## Demo

README 展示的 8/10 视频是一组 10-env qualitative demo，用来展示完整任务动作链。正式结果仍以 step54 的 44/100 Legacy100 为准。