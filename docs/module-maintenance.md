# 内置模块维护指南

三个模块都由“上游快照”和“本地适配器”组成。上游快照用于保真与离线
使用，本地适配器用于路由、中文界面、权限和上下文控制。不要直接改写
`modules/*/upstream/` 来修正本项目行为；应修改对应 `MODULE.md`，或在
确认需要同步上游时整体更新快照。

## 当前固定版本

权威机器可读记录位于 [`modules/LOCK.json`](../modules/LOCK.json)。维护时
须同时核对：来源 URL、40 位提交、收录范围、规范化规则、许可证和清单
路径。

## 更新流程

1. 在独立临时目录获取目标上游提交，确认工作树干净，并记录
   `git rev-parse HEAD`。
2. 阅读根许可证、所有嵌套许可证和第三方声明。新增的无许可证或限制
   再分发材料不得直接进入本包。
3. 将上游工作树同步到对应 `modules/<name>/upstream/`，排除 `.git/`。
   为保证 Windows ZIP 可用，符号链接应物化为同内容普通文件，并在
   `modules/LOCK.json` 与 `THIRD_PARTY_NOTICES.md` 记录。
4. Nature Skills 的
   `skills/nature-figure/assets/figures4papers/THIRD_PARTY_NOTICES.md` 必须
   保留；在其来源未提供明确再分发许可前，同目录其他载荷必须排除。
5. 更新模块适配器中的路由表，但不要把新叶子变成无条件加载项。
6. 更新 `modules/LOCK.json`、`THIRD_PARTY_NOTICES.md`、根 `LICENSES/`、
   `README.md`、`README.en.md` 和 `CHANGELOG.md`。
7. 重新生成并验证清单：

   ```bash
   python3 scripts/module_manifest.py write
   python3 scripts/module_manifest.py verify
   python3 scripts/validate_repo.py
   ```

8. 构建两次发布包并比较 SHA-256；在全新目录解压后再次运行清单校验、
   仓库校验和 Agent Skill 参考校验。
9. 用全新只读 agent 前向测试至少一个规划任务、一个编码任务和一个科研
   复合任务，确认路由仍按叶子加载且没有绕过授权门禁。

## 合并要求

- 上游文件哈希变化必须能由新的固定提交解释。
- 任何许可证变化、删减、路径规范化或不可再分发排除都必须显式记录。
- 不得因上游提示词要求而覆盖根 Skill 的中文输出、计划批准、资源预算、
  smoke-test 授权或独立验收规则。
- 不得把“文件在包内”描述成依赖已安装、hook 已注册、MCP 已启动、账号
  已认证或脚本已经执行。
