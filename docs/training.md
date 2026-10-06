# V5 Full-Parameter PPO

最终路线从 clean SFT checkpoint 直接做 full-task Stage4 PPO，不从 V3/V4 checkpoint 串联。

## 配置

| 参数 | V5 |
|---|---|
| Train env | 16 |
| Episode / rollout | 256 / 256 |
| Rollout epochs | 8 |
| Update epochs | 4 |
| Micro / global batch | 64 / 1024 |
| Actor LR | 5e-6 |
| Value LR | 1e-4 |
| Gamma / GAE lambda | 0.99 / 0.95 |
| PPO clip | 0.2 |
| Precision | bf16 |
| Fine-tuning | Full-Parameter |
| FSDP | full_shard |
| Max global steps | 60 |

每个 global step 采集 `16 env × 8 rollout epochs = 128` 条 trajectory。60 steps 共 **7,680 trajectories**；按 episode length 256 估算约 **1.97M environment steps**。

完整训练耗时 **43:27:21**。

训练后期 10-step block average 的 online `success_once` 从前 10 步的 22.42% 提升到最后 10 步的 40.78%，return 从 1.960 提升到 2.634。

`step54` 的单个 online batch 为 46.09%（59/128），但 checkpoint 选择仍以独立评测为准。