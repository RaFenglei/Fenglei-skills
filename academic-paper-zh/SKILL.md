---
name: academic-paper-zh
description: Translate academic papers into faithful Chinese with original figures and produce a separate source-grounded critical reading report in Word. Use for full-paper translation and study across disciplines; prefer a domain edition when explicitly requested.
metadata:
  version: "0.5.0"
---

# 学术文献中文精读通用版

面向需要准确阅读英文文献的中文研究者。默认交付中文全文译本与独立精读报告两份 Word；中英逐段对照为可选模式。全文、原图、中文图注、主要结论、创新判断、按相关性确定数量的推荐文献和关键问题的检索解答共同构成任务；用户要求局部处理时遵循其范围。

## 执行入口
1. 读取 [执行规范](references/workflow.md)，核对来源与范围并建立内容/图表映射。
2. 翻译前读取 [Word规范](references/word-output.md)，使用 [工作记录](references/work-record.md) 保存可恢复账本。
3. 精读和联网阶段读取 [检索规范](references/search-evidence.md)，按 [报告模板](assets/report-outline.md) 成文。
4. 按论文类型选择审查方法，不默认套用医学或组学规范。若用户明确选择领域加强版，采用对应版本，避免重复生成两套文件。

## 使用边界
本技能可以独立安装，所有必要规范均在本目录；不依赖另外两个版本或其他第三方研究 skill。文档/网页工具根据当前环境使用，缺少能力要报告实际缺口。技能定义流程，不自带全文获取权限、模型服务或 Word 渲染引擎。

对无法核实的来源、缺图、未译内容和未完成视觉检查如实记录。不伪造相关文献推荐、DOI、实验结果或验证通过。普通精读不扩展为全领域系统综述或原始数据分析。不要默认上传论文到额外翻译网站，也不因使用技能而自动发布到 GitHub。

## 新增必读分支
精读报告默认按[后续科学问题](references/research-opportunities.md)提供3个优先问题与另外10个发散问题，和本文核心质疑分开。涉及组学时按[组学路由](references/omics-review.md)选择实际测量分支；通用版遇非组学论文不加载该模块。仅在开发维护skill且获用户授权时，按[审核规范](references/independent-review.md)让DeepSeek独立审核skill；不送审论文，不在论文报告中附模型审核记录。这三项不能替代全文翻译、原图与中文图注、相关文献推荐和核心问题检索解答。

本目录随包携带全部引用文件与校验脚本；通用规范使用相同副本，发布时通过哈希一致性检查同步更新。领域版另有专属domain.md：进化版侧重起源、同源与功能层级；医学版侧重研究设计、患者独立性和转化证据。

## 面向读者的报告
详细解释论文主题、主要结论、创新点和技术路线，默认嵌入[技术路线图](references/technical-route.md)。核心问题和推荐文献均不设固定数量；原文定位使用实际章节/小节名及必要图表号，不用页码。内部检查记录不作为报告章节。

## 双文件与阅读设计
生成前读取[双文件阅读设计](references/reading-design.md)。交付前运行 scripts/audit_pair.py 核对两个独立Word及共同来源版本，再完成内容和逐页视觉检查。不得仅有报告便宣称全文译本完成；最终分别链接两份Word。
