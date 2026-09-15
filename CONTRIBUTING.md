# 贡献指南

感谢改进中文复杂项目编排器。贡献应优先修复真实行为问题，避免为假设场景不断增加全局规则。

## 开始之前

- 讨论重大工作流变化时先创建 Issue，说明用户场景、当前失败和可观察的预期行为。
- 安全漏洞不要创建公开 Issue，请按 [SECURITY.md](SECURITY.md) 报告。
- 提交贡献前请确认你有权提供相关内容。提交 Pull Request 即表示你同意按本项目的 [MIT License](LICENSE.md) 提供该贡献（inbound = outbound）。

## 修改原则

1. 保留原始用户意图和授权边界。
2. 所有用户可见输出默认中文，内部编排可以使用英文。
3. 不把完整内置快照变成无条件上下文；始终通过模块适配器选择叶子 Skill。
4. 不为减少代码或 token 而削弱安全、错误处理或必要验证。
5. 保持渐进披露：核心门禁放在 `SKILL.md`，条件性细节放入一层 `references/`。
6. 新增规则时补充能复现问题的行为测试场景。

## 本地验证

要求 Python 3.9 或更高版本，无第三方 Python 依赖：

```bash
python3 scripts/validate_repo.py
python3 scripts/module_manifest.py verify
```

如果已安装 Agent Skills 参考验证器，再运行：

```bash
skills-ref validate .
```

对工作流行为做前向测试时：

- 使用全新的只读测试 agent；
- 只提供 Skill、真实测试请求和完成任务所需的最小材料；
- 不提前告诉测试 agent 预期答案或已知缺陷；
- 在隔离目录运行，不安装依赖，不修改生产系统；
- 按 `references/test-cases.md` 的可观察行为验收，而不是匹配固定措辞。

## Pull Request 清单

- [ ] `python3 scripts/validate_repo.py` 通过。
- [ ] `SKILL.md` 的名称、描述、版本和兼容性仍符合规范。
- [ ] 所有相对链接存在，且没有新增深层引用链。
- [ ] 用户界面仍为中文，内部英文规则没有泄漏到用户界面。
- [ ] 新规则具有对应的行为回归用例。
- [ ] 权限、安装、smoke test 和独立验收门禁没有被弱化。
- [ ] `CHANGELOG.md` 已更新；版本变化符合语义化版本意图。
- [ ] 未加入密钥、凭据、真实敏感数据、生成缓存或构建产物。
- [ ] 未直接修改 `modules/*/upstream/`；更新上游后已重新生成快照清单。
- [ ] 修改内置上游快照时已更新 `modules/LOCK.json`、`THIRD_PARTY_NOTICES.md`、提交、许可证和 SHA-256 清单。
- [ ] 更新内置模块时已遵循 `docs/module-maintenance.md` 的版权排除和前向测试流程。

## 版本约定

- PATCH：措辞澄清、文档或不改变行为的修复。
- MINOR：向后兼容的新模式、状态字段或验证能力。
- MAJOR：触发条件、授权门禁或核心执行语义的不兼容变化。

提交信息使用简短祈使句。Pull Request 应说明问题、行为变化、验证证据和剩余风险。
