# 工作记录格式

在每篇论文自己的工作目录保存 coverage.json，不能写回 skill 安装目录。顶层含 source（来源版本）、blocks、figures、qa。每块字段为 id、locator、kind、source_text、translation、status、note；status 仅用 translated、preserved、missing，保留原文的参考文献使用 preserved 并说明原因。译者审校后可加 reviewed=true，脚本不代替审校。

每图字段为 id、locator、caption_block_ids（非空列表）、asset、included（布尔）、visual_checked（布尔）。asset 用相对 coverage.json 的实际原图文件路径。qa.visual_review_completed 只有两个输出文档都逐页检查后才为 true。

检查命令：`python scripts/audit_paper.py coverage path/to/coverage.json`。输出 JSON 并在缺译块、缺图资产、无效图注关联或未视觉检查时返回非零退出码。不会因为缺口而删除结果。

结构检查命令：`python scripts/audit_paper.py docx path/to/paper.docx`。输出媒体数、绘图数、表格数、段落数与缺失的内部关系对象。它只做读取，不编辑文件；无图文档可合法通过结构检查，图完整性另由 coverage 核对。

额外保存内部测量核对记录、questions.json、先行研究查询覆盖、skill维护时另存的审核输入哈希和意见处理表。全文翻译与skill审核进度分开记录。

## 长文恢复指针
另外保存progress.json：source_sha256、source_version、chunks数组（chunk_id、start_locator、end_locator、block_ids、source_sha256、status=pending/drafted/reviewed）、next_chunk_id、terminology_version。每完成一个块先保存coverage再更新progress，禁止只更新完成标记。恢复时先比对源文件哈希；如改变，列出受影响块并重新核对。按next_chunk_id读取待处理块及前后文，核对coverage中的未完成块；全部块reviewed也不代替数值/图表/版式验收。

内部记录可用页码定位提取块，读者报告则转换为实际章节/小节与图表编号。内部文件不作为论文报告附录；skill审核材料与论文工作目录分开。
