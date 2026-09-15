# GitHub 发布指南

本仓库根目录同时是 Agent Skill 根目录。建议 GitHub 仓库名称保持为 `zh-complex-project-orchestrator`；官方规范要求 Skill 的 `name` 与父目录名一致，仓库校验器也会检查这一点。

## 首次发布

1. 在 GitHub 创建空仓库 `zh-complex-project-orchestrator`，不要让 GitHub 自动生成 README、`.gitignore` 或许可证。
2. 将本仓库生成的“源码兼安装包”解压，进入同名目录。该压缩包包含运行所需文件、维护脚本、文档和 `.github/` 配置，不包含 Git 历史。
3. 初始化并检查本地仓库：

   ```bash
   git init
   git branch -M main
   python3 scripts/validate_repo.py
   git add .
   git commit -m "Publish zh-complex-project-orchestrator 2.1.0"
   ```

4. 在 GitHub 仓库页面复制远程 URL，将其作为下面命令的最后一个参数：

   ```bash
   git remote add origin REMOTE_URL_COPIED_FROM_GITHUB
   git push -u origin main
   ```

   `REMOTE_URL_COPIED_FROM_GITHUB` 是说明性占位符，执行前必须替换为刚复制的真实 URL。

## 建议的仓库设置

- 启用 Issues；
- 启用 Private vulnerability reporting；
- 将 Actions 的默认令牌权限设为只读；
- 保护 `main` 分支，要求 Pull Request 和 `Validate` 检查通过；
- 禁止强制推送和删除受保护分支；
- 根据协作规模决定是否要求至少一名审查者。

本仓库采用 MIT License。发布前确认 `LICENSE.md`、`SKILL.md` 的 `license` 字段、README 和贡献条款仍保持一致；任何许可证变更都必须同步更新这些位置。

## 创建 Release

1. 更新 `VERSION`、`SKILL.md` 中的 `metadata.version` 和 `CHANGELOG.md`。
2. 运行完整校验与构建：

   ```bash
   make validate
   make package
   unzip -t "dist/zh-complex-project-orchestrator-$(cat VERSION).zip"
   ```

3. 提交版本变更。
4. 创建并推送与版本一致的标签：

   ```bash
   git tag -a "v$(cat VERSION)" -m "Release $(cat VERSION)"
   git push origin "v$(cat VERSION)"
   ```

5. 在 GitHub Releases 中基于该标签创建 Release，将 `dist/` 中的源码兼安装包作为附件，并从 `CHANGELOG.md` 复制对应版本说明。

发布前检查压缩包中不存在 `.git/`、`dist/`、缓存、日志、密钥或项目状态文件，并确认解压后可直接运行 `python3 scripts/validate_repo.py`。
