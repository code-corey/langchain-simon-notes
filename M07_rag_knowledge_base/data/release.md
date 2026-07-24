# 发布流程

团队发布遵循以下步骤：

1. 功能合并到 `main` 前必须通过 CI（单测 + lint）。
2. 使用 `release` 流水线打 tag，版本号遵循语义化版本。
3. 先发布到 staging，观察 30 分钟黄金指标（错误率、延迟、CPU）。
4. staging 无异常后再发布 production，并在变更群同步发布说明。
5. 若 production 错误率 5 分钟内翻倍，立即执行回滚 playbook。
