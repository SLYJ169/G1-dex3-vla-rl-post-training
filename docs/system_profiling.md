# 系统与资源记录

正式训练使用 **2× NVIDIA RTX PRO 6000 Blackwell Server Edition**，每卡约 96 GB 显存；host RAM cgroup 上限约 220 GiB。

## Parallel env

- 24 env：rollout 可以启动，但随后出现 Ray SYSTEM_ERROR / SIGKILL；确认根因是 **host RAM cgroup OOM**，不是 GPU OOM。
- 16 env：稳定完成训练，成为 V5 固定配置。

V2 期间 16 env 的 host RAM 峰值接近 218/220 GiB，因此继续增加并行环境没有实际空间。

## Distributed training

- Full-Parameter Fine-Tuning
- FSDP `full_shard`
- actor offload = false
- rollout offload = true
- bf16

资源优化的重点最终落在 host RAM，而不是单纯追求更高 GPU 利用率。