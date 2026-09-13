# academic-paper-zh

学术文献中文精读通用版，适用于跨学科英文论文的全文翻译、图表保留和独立精读。

## 适用场景

- 需要中文全文译本，并保留原图、表格和中文图注；
- 需要单独的 Word 精读报告，包含主题、结论、创新判断、技术路线、核心问题解答和相关文献；
- 论文不属于明确的进化基因或医学组学领域，或用户希望使用通用阅读流程。

## 交付内容

默认交付两个独立 Word：

1. 中文全文译本；
2. 独立精读报告。

中英逐段对照、局部翻译或其他格式按用户要求启用。全文译本和报告分别完成内容检查与逐页视觉检查，不能用报告替代全文译本。

## 执行入口

使用前按顺序阅读：

- [SKILL.md](SKILL.md)：主流程和边界；
- references/workflow.md：来源、范围和图表映射；
- references/word-output.md：Word 输出规范；
- references/search-evidence.md：检索和证据记录；
- references/reading-design.md：双文件阅读设计；
- assets/report-outline.md：报告结构。

涉及组学时才加载 references/omics-review.md；不涉及组学的论文跳过该分支。

## 边界

本 skill 不自带全文获取权限、模型服务或 Word 渲染引擎。无法核实的来源、缺图、未译内容和未完成视觉检查必须如实记录；不伪造 DOI、文献、实验结果或验证结论。普通精读不会自动扩展为系统综述、原始数据分析或额外网站上传。

## 安装

可单独安装本目录，也可从仓库整体安装：

~~~text
https://github.com/RaFenglei/Fenglei-skills/tree/main/academic-paper-zh
~~~

本目录包含运行所需的规范、资源和脚本，不依赖另外两个文献阅读版本。