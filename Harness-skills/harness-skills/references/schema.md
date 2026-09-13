# 本地工作目录与字段

家族规范：新Codex路线使用family=openai、client=codex、protocol=external；GPT API也属于openai，但client不可冒写codex。旧family=codex仅兼容读取，跨家族比较归一为openai。新仅Codex回执的executor/reviewer都需client=codex。校验器只检查显式字段，不能证明真实身份或自动执行多复审/合并作者/最终门槛；这些记录与检查由协调者负责。

`.harness/providers.json`：schema_version=1、project_root、providers映射。每route含family、model、base_url、protocol、key_env（仅变量名）、quota_group、allowed_hosts、enabled、status、verified_at、source_urls。外部当前Codex用protocol=external，不填虚构API。

`.harness/plan.json`：mode=codex/harness/ask、max_calls、max_output_tokens、max_input_chars、modules列表；每模块id、execute与review路线列表、acceptance、depends_on。每条route必须存在；每个可选执行者至少有一个不同family reviewer（仅Codex模式要求双方均Codex）。图必须无环。

`.harness/benchmark.md`保存原始来源和适用性推论；`.harness/runs/<run>/`保存脱敏任务、证据、产物和receipt.json。receipt含mode、status、artifact_sha256（UTF-8文件原始字节）、executor和reviewer（family/session）、review（verdict、artifact_sha256、issues数组，每项severity/evidence/fix）。结构校验不是数字签名，不替代如实执行。

记忆由实际运行器管理：scope=off/project/cohort/sample，project_id，sample_id/cohort_id，kind=method/project_conclusion/sample_result，text，source_receipt，artifact_sha256，status。共享必须能重新验证源回执及精确文本；本包不带数据库服务。仅复制符合用户选择且仍有效的条目，不能跨项目自动加载。

私密项目清单、凭证、回执、样本信息不进入技能仓库。可分享能力摘要时先脱敏，不能只依赖自动正则。

