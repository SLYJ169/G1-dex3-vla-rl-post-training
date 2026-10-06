# G1 + Dex3 VLA RL Post-Training

基于 **Unitree G1 29-DOF + Dex3 双灵巧手**，在 Isaac Sim / Isaac Lab 中完成 Assemble Trocar 精细装配任务的 **GR00T-N1.5 + PPO Full-Parameter RL Post-Training**。

完成内容：

- 从 clean SFT checkpoint 开始进行 **60 次 PPO update**，累计 **7,680 trajectories / ≈1.97M environment steps**；
- 使用 **2× RTX PRO 6000 Blackwell + FSDP full_shard** 完成 Full-Parameter 训练；
- 通过 Stage Profiler 将主要瓶颈定位到 **Align → Insert**；
- 对训练并行环境、host RAM、rollout/update 行为和失败视频做完整分析。

| 项目 | 配置 |
|---|---|
| Robot | Unitree G1 29-DOF + Dex3 |
| Task | Assemble Trocar |
| VLA | GR00T-N1.5 |
| RL | RLinf PPO |
| Simulator | Isaac Sim 5.1 + IsaacLab + IsaacLab-Arena |
| Fine-tuning | Full-Parameter |
| Training | 60 PPO updates / 7,680 trajectories / ≈1.97M env steps |
| Compute | 2× RTX PRO 6000 Blackwell |

---

## Demo

展示双臂完成 **抓取 → 对准 → 插入 → 放置** 的完整过程。该 10-env Demo 中 **8/10 完成任务，成功率 80%**。

<p align="center">
  <a href="assets/demo/step54_8of10_demo.mp4">
    <img src="assets/demo/step54_8of10_demo.webp" width="900">
  </a>
</p>

---

## 任务

<p align="center">
  <img src="assets/overview/task_setup.jpg" width="850">
</p>

任务指令：

~~~text
install trocar from box
~~~

Rheo v0.5.0 将任务分为四个阶段：

| Stage | 任务 |
|---|---|
| 1 | Lift |
| 2 | Align |
| 3 | Insert |
| 4 | Place |

策略输入为 front + left wrist + right wrist 三路图像和 28D robot state，输出 28D policy action。评测沿用 Rheo v0.5.0 的 Stage4 success 定义。

运行环境与任务合同见 [`docs/runtime.md`](docs/runtime.md)。

---

## PPO Post-Training

最终训练从 clean SFT checkpoint 直接进行 Stage4 full-task PPO。

| 参数 | 配置 |
|---|---|
| Train env | 16 |
| Rollout / episode length | 256 |
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
| Global steps | 60 |

每个 global step 采集 128 条 trajectory，完整训练共 **7,680 trajectories**；按 rollout length 256 计算约 **1.97M environment steps**。训练耗时 **43h27m**。

<p align="center">
  <img src="assets/training/v5_progress.svg" width="820">
</p>

按 10-step block 统计，online `success_once` 从前 10 步的 22.42% 提升到最后 10 步的 40.78%，mean return 从 1.960 提升到 2.634。

详细配置见 [`configs/v5_final.yaml`](configs/v5_final.yaml) 和 [`docs/training.md`](docs/training.md)。

---

## Stage Profiler

整体 success 只能说明最终是否完成任务，Stage Profiler 用来继续追踪失败发生在哪个阶段。

<p align="center">
  <img src="assets/analysis/stage_profiler.svg" width="760">
</p>

| Stage | 累计通过 | 条件通过率 |
|---|---:|---:|
| Lift | 18/20（90%） | — |
| Align | 15/20（75%） | 15/18（83.3%） |
| Insert | 8/20（40%） | 8/15（53.3%） |
| Place | 8/20（40%） | 8/8（100%） |

主要损失出现在 **Align → Insert**：完成 Align 的 15 条轨迹中只有 8 条进入 Insert；完成 Insert 后 8/8 通过 Place。

详细记录见 [`docs/stage_profiler.md`](docs/stage_profiler.md)。

---

## Failure Analysis

结合 Stage Profiler 和评测视频，失败主要分为三类：

| 类型 | 表现 |
|---|---|
| Grasp / Retention | 零件滑脱、掉落后无法恢复稳定双手控制 |
| Fine Alignment / Insertion | 已完成粗对准，但长时间停在近同轴接触状态，无法满足插入条件 |
| Late-stage Place / Release | 已完成或接近插入，但最终 placement / release 条件未满足 |

最常见的是 **Fine Alignment / Insertion stall**。策略通常能完成任务前半段，主要困难集中在精细接触和插入阶段。

详细视频复核见 [`docs/failure_analysis.md`](docs/failure_analysis.md)。

---

## 工程记录

训练过程中遇到的关键问题主要集中在并行环境、PPO 更新强度和阶段诊断：

- **Parallel env**：24 env 可以启动 rollout，但后续触发 host RAM cgroup OOM；最终固定为 16 env；
- **PPO update**：早期版本的 KL / clip fraction 较小，后续调整 actor LR 和 batch 后继续观察独立评测；
- **Stage diagnosis**：V3 增加 Stage Profiler 后确认 Align → Insert 是主要瓶颈；
- **Final route**：最终回到 clean SFT → direct Stage4 full-task PPO，避免把自定义 stage handoff 混进主结果。

完整版本演进见 [`docs/training_evolution.md`](docs/training_evolution.md)。

---

## System Profiling

训练使用 **2× RTX PRO 6000 Blackwell Server Edition**，host RAM cgroup 上限约 220 GiB。

- 24 env：host RAM cgroup OOM / SIGKILL；
- 16 env：稳定完成训练；
- 16 env 期间 host RAM 峰值接近 218/220 GiB；
- Full-Parameter + FSDP `full_shard`；
- bf16；
- actor offload = false，rollout offload = true。

实际瓶颈主要在 host RAM，而不是 GPU 显存。

详细记录见 [`docs/system_profiling.md`](docs/system_profiling.md)。

---

## 结果与复现资料

- [`results/v5_training_blocks.csv`](results/v5_training_blocks.csv)：训练区间指标
- [`results/stage_profiler.csv`](results/stage_profiler.csv)：Stage Profiler
- [`docs/evaluation.md`](docs/evaluation.md)：完整评测记录
- [`docs/limitations.md`](docs/limitations.md)：评测说明
- [`configs/v5_final.yaml`](configs/v5_final.yaml)：最终训练配置

---

## Repository Structure

~~~text
G1-dex3-vla-rl-post-training/
├── assets/
│   ├── analysis/
│   ├── demo/
│   ├── overview/
│   └── training/
├── configs/
│   └── v5_final.yaml
├── docs/
├── results/
└── scripts/
~~~

上游项目：

- [IsaacLab](https://github.com/isaac-sim/IsaacLab)
- [IsaacLab-Arena](https://github.com/isaac-sim/IsaacLab-Arena)
- [Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T)
- [RLinf](https://github.com/RLinf/RLinf)

完整模型 checkpoint、Isaac Sim 缓存和大体积训练日志不直接提交到 Git。