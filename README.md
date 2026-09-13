# Fenglei-skills

RaFenglei 的个人 Codex skills 仓库。每个 skill 都放在独立的同级目录中，拥有自己的说明、入口、资源和版本范围。

## 学术论文阅读 skills

面向中文科研阅读的三个 Codex skill：

- `academic-paper-zh`：通用学术文献精读、中文全文翻译与 Word 输出。
- `evolution-omics-paper-zh`：新基因、进化与多组学方向加强版。
- `medical-omics-paper-zh`：医学与组学方向加强版。

| Skill | 适用重点 | 说明 |
|---|---|---|
| [academic-paper-zh](academic-paper-zh/) | 跨学科通用精读 | [README](academic-paper-zh/README.md) · [SKILL.md](academic-paper-zh/SKILL.md) |
| [evolution-omics-paper-zh](evolution-omics-paper-zh/) | 新基因、进化基因组学和调控创新 | [README](evolution-omics-paper-zh/README.md) · [SKILL.md](evolution-omics-paper-zh/SKILL.md) |
| [medical-omics-paper-zh](medical-omics-paper-zh/) | 医学、临床和组学证据评价 | [README](medical-omics-paper-zh/README.md) · [SKILL.md](medical-omics-paper-zh/SKILL.md) |

默认输出两份 Word：中文全文译本、独立精读报告；中英逐段对照为可选模式。报告包含主题、主要结论、创新点、技术路线与配图说明、数量随论文决定的“核心问题及资料解答”、详细推荐文献，以及 3 个优先科学问题和 10 个发散问题。正文默认 1.5 倍行距，图注与书目 1.2 倍。

三个目录均可单独安装，保持各自 `SKILL.md`、`references/`、`assets/`、`scripts/` 的相对路径。

## Harness-skills

[Harness-skills](Harness-skills/) 根据实际可用 API、benchmark、预算和任务负载设计多模型执行、递补、补充与独立复审流程。入口是 [`$harness-skills`](Harness-skills/harness-skills/SKILL.md)，详细规则见 [Harness-skills/README.md](Harness-skills/README.md)。

调用后先检查当前项目实际可用的 API、客户端、模型版本、协议、端点、配额组和已安装 skills，再生成候选路由。每个任务明确四个角色：

- **主执行**：完成主要分析、代码、文稿或报告。
- **主执行递补**：仅在主执行不可用、认证失败、配额冷却或任务失败时接替，并记录切换原因。
- **独立补充**：使用独立会话和证据补充检索、反例、方法核查或候选实现；主执行成功也不会跳过。
- **独立复审**：由不同模型家族的新会话复核产物，结果绑定输入和输出 hash，并给出 `pass`、`revise` 或 `block`。

每轮任务开始时选择运行方式：仅 Codex，或按当前项目授权路由运行的 Harness。Harness 不会自动更新 skill；它会先报告版本、hash、兼容性和精确 diff，由用户选择保持现状、批准部分更新或批准全部更新。获批后才备份、修改指定路径并重新验证。

## 仓库边界与安装

新增 skill 请建立新的同级目录，并提供独立的 `README.md` 和安装入口。不要覆盖其它 skill 的 README、配置、资源或记忆。

本仓库不包含 API 凭证、账号密码、内部地址、原始表达矩阵、患者信息、私密研究资料、样本结果、运行回执或临时日志。项目级 API 清单、调用回执、备份、样本结果和可选记忆保存在实际项目的 `.harness/` 中。跨样本记忆默认只共享方法与已复审结论，样本结果保持隔离。

额度不足时不使用 Codex 重置卡、不自动购买额度，也不复制其它对话中的密钥。只有在当前项目已授权且端点已核验时，才允许使用其它 API 递补。

可从 GitHub 安装整个仓库或指定目录：

```text
https://github.com/RaFenglei/Fenglei-skills
```

安装不会自动修改其它 skill、用户级全局指令或项目凭证；全局规则变更必须由用户明确授权。

