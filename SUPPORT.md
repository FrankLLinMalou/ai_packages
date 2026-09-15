# 支持

## 使用问题

请先确认：

1. 整个仓库都已复制到 Agent Skills 目录，而不是只复制 `SKILL.md`；
2. 目录名仍为 `zh-complex-project-orchestrator`；
3. 已重启客户端或新建线程；
4. 调用时明确包含 `$zh-complex-project-orchestrator`；
5. 宿主是否支持 Plan、子 agent 和持久文件。
6. `python3 scripts/module_manifest.py verify` 是否确认三个内置快照完整。

无法解决时可创建 GitHub Issue，并提供宿主名称与版本、调用方式、期望行为、实际行为和已去除敏感信息的最小复现。不要提交密钥、完整私人对话或真实敏感项目数据。

安全问题请遵循 [SECURITY.md](SECURITY.md)，不要公开报告可利用细节。
