# Failure Analysis

视频复核主要使用 8/10 qualitative demo 和一组 3/10 对照视频。

## 1. Grasp / Retention Failure

物体在双手操作过程中滑脱或掉回托盘，后续难以恢复稳定控制。

## 2. Fine Alignment / Insertion Failure

已经完成抓取和粗对准，但长时间停在近同轴状态，没有满足插入的轴向、姿态或深度条件。该类型在失败样本中最常见。

## 3. Late-stage Place / Release Failure

已经完成或接近插入，但最终 placement / release 条件没有满足。

Stage Profiler 与视频复核指向同一个瓶颈：策略已经能完成大部分任务前半段，剩余问题主要集中在 **contact-rich 的精细对准和插入阶段**。