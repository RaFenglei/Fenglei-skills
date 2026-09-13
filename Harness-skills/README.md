# Harness-skills

根据当前项目API、原始benchmark、预算和任务负载重建设计与执行/独立复审路由。标准调用名：`$harness-skills`。

## 安装与使用

从 `RaFenglei/Fenglei-skills` 安装目录 `Harness-skills/harness-skills` 到Codex用户skills目录。可让skill-installer安装该GitHub路径，技能下一轮可发现。

> $harness-skills 根据本项目现有API与最新benchmark重新设计harness，明确各模块执行/复审并按我选择的模式执行。

API改变时更新当前项目 `.harness/providers.json`，重新核对来源、协议与能力。不预置账号、密钥、内部地址或固定模型版本。脚本只做离线初始化/验证，实际请求和命令由Codex及已审客户端执行。

`codex-mode-policy.md` 是每轮模式询问模板；仅安装技能不会自动修改全局指令，需用户要求后追加到用户级AGENTS。模式选择回复不重复询问。额度不足时不使用重置卡；只在既有授权范围内调用可用API递补，不自动购买额度。

## 隔离与验收

先依据当前已安装的相关skills适配工作，再给出候选更新及具体差异。你可选择保持现状、只更新指定项或批准全部所列更新；运行Harness不会自动更新skill。批准后先备份，再仅修改选定路径。普通模块默认1执行+1复审，批量分块与关键双复审按需启用。

本目录只属于Harness技能。其它skill另建同级目录和独立README。项目API清单、回执、样本结果和记忆保留在实际项目 `.harness/`，不写进技能仓库，不与其它skill共享凭据或默认启用规则。

官方格式校验及独立离线边界测试通过；不等于所有API、网关工具调用和实际科学分析均已验收。

