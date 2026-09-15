# 安全策略 / Security Policy

## 支持范围

仅维护默认分支和最新发布版本。旧版本中的问题应先在最新版本复现。

## 私密报告漏洞

请优先使用 GitHub 仓库的 **Private vulnerability reporting**，不要在公开 Issue 中披露可利用细节、密钥、个人数据或未修复的攻击路径。

报告请包含：

- 受影响的文件和版本；
- 最小复现步骤；
- 预期影响和所需前置条件；
- 建议缓解措施（如有）；
- 是否已经公开披露。

公开发布前必须启用 GitHub Private vulnerability reporting。如果无法启用，仓库所有者必须先在本节加入一个受监控的私密安全邮箱；在此之前不要公开可利用细节。普通功能问题可按 [SUPPORT.md](SUPPORT.md) 使用公开渠道。

## 安全边界

本项目是工作流指令，不是安全沙箱。它不能替代宿主平台的访问控制、审批、凭据隔离或审计。

以下情况属于安全问题：

- 未经用户授权安装或运行第三方代码；
- 绕过计划、smoke test 或外部副作用授权门禁；
- 将协调 agent 的自检冒充独立验收；
- 在状态文件、日志或子 agent brief 中泄露密钥或不必要的个人数据；
- 通过翻译或压缩改变否定词、权限范围或安全约束；
- GitHub Actions 或维护脚本出现命令注入、凭据暴露或不受控下载。

第三方 Skill 仅作为可选来源被引用，不由本仓库维护或担保。使用前应检查其版本、脚本、hooks、权限和许可证。

## Disclosure language

Security reports may be submitted in Chinese or English. User-facing project communication remains Chinese unless the user explicitly requests another language.
