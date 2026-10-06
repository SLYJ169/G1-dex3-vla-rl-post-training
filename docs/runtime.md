# Runtime 与任务合同

## 技术栈

- Isaac Sim 5.1
- IsaacLab
- IsaacLab-Arena
- Isaac-GR00T / GR00T-N1.5
- RLinf PPO
- Rheo v0.5.0 workflow

冻结依赖：

| Component | Commit |
|---|---|
| IsaacLab | `941ebdf4ad1fbf89018777012bdfa4b5944c758f` |
| IsaacLab-Arena | `dba09956588dddae52897820686efd329d85da12` |
| RLinf | `649e7579775997ade74efff33a7c23e90c61e60a` |
| Isaac-GR00T | `4af2b622892f7dcb5aae5a3fb70bcb02dc217b96` |

## 任务

- Robot：Unitree G1 29-DOF + Dex3 双灵巧手
- Train task：`Isaac-Assemble-Trocar-G129-Dex3-Joint`
- Eval task：`Isaac-Assemble-Trocar-G129-Dex3-Joint-Eval`
- Instruction：`install trocar from box`
- Cameras：front + left_wrist + right_wrist
- Image：480×640
- State：28D
- Policy action：28D
- Scene action：43D；adapter 前置 15 个 zero
- Action horizon：16

主评测沿用 Rheo v0.5.0 的四阶段 Stage4 Place 成功定义。