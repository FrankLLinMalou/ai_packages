# 一套用于提高agent工作效率的规则

[English](README.en.md)

面向中文用户的长期复杂项目 Agent Skill，它解决的不是“让 agent 多开几个子 agent”，而是控制复杂项目中最容易浪费资源的环节：需求丢失、过早实施、重复扫描、无边界并行、未经授权的测试，以及缺少独立验收。v3.0.0 将 Matt Pocock Skills、Ponytail 和 Nature Skills 的固定版本按“最大可合法再分发范围”模块化内置，用户不需要再安装这三个上游 Skill。

主要保证：

- 实质性中文或中英混合需求先被编译成紧凑、忠实的英文任务规格。
- 原始用户指令始终是最高权威，译文不得覆盖或弱化原始约束。
- 实施前必须先规划并获得确认；重大范围变化需要重新确认。
- 默认串行、节省 token；仅重型任务或明确追求速度时增加执行子 agent。
- smoke test 必须获得针对具体测试的许可，且未经检查不得编造命令或环境。
- 最终由未参与翻译和实施的全新只读 agent 独立验收。
- 先选择模块，再只加载当前任务需要的叶子 Skill；复合任务可以组合多个叶子，但不会把完整上游仓库塞入上下文。
- 内部可以全程使用英文，所有用户可见内容默认使用中文。

## 适用场景

适合：

- 多阶段、多交付物或预计跨线程的项目；
- 大型代码改造、平台建设、研究项目或长期文档工程；
- 需要显式资源预算、人工批准门禁和独立验收的任务。

不适合：

- 一次性简单问答；
- 用户没有显式启动本 Skill；项目状态文件不能代替显式调用；
- 只需要快速翻译、单文件小改或普通信息检索的任务。

## Intake 策略与执行模式

两个设置彼此独立，避免把翻译策略与执行速度混为一谈：

| 设置 | 可选值 | 行为 |
| --- | --- | --- |
| `intake_policy` | `economy`（默认） | 实质性中文需求使用一次性翻译 agent；简单批准、状态指令、英文或纯代码本地处理 |
| `intake_policy` | `strict` | 每条项目消息都经过全新 intake agent，适合要求严格前置处理的环境 |
| `execution_mode` | `economy`（默认） | 默认串行，优先减少上下文传递、重复扫描和 token 消耗 |
| `execution_mode` | `fast` | 优先缩短墙钟时间；仅在工作流真正独立时增加有边界的并行 agent |

## 安装

### Codex CLI / Codex 桌面端

将整个仓库克隆或复制到 Codex skills 目录，并保持目录名不变：

```text
~/.codex/skills/zh-complex-project-orchestrator/
```

Windows 通常对应：

```text
%USERPROFILE%\.codex\skills\zh-complex-project-orchestrator\
```

`~/.codex` 只是默认值；如果设置了 `CODEX_HOME`，请使用 `$CODEX_HOME/skills/zh-complex-project-orchestrator/`。完成后重启 Codex 或开始一个新线程。不同 Agent Skills 客户端的目录位置可能不同，请以对应客户端文档为准。

仓库根目录本身就是 Skill 根目录；不要只复制 `SKILL.md`，否则会丢失模块路由、完整上游快照、脚本、资产、许可证和行为测试。

## 使用

显式启动：

```text
使用 $zh-complex-project-orchestrator 管理这个项目。内部使用英文，所有面向我的输出使用中文。
```

切换为严格 intake：

```text
这个项目使用 intake_policy: strict，每条项目消息都先经过 intake agent。
```

优先速度：

```text
将 execution_mode 切换为 fast；只有独立工作流才并行。
```

启动后，Skill 会先给出中文计划、验收标准和资源预算，并等待确认。计划批准不自动授权发布、部署、生产写入、付费调用或第三方安装。

## 项目状态

代码项目优先使用：

```text
.codex/zh-complex-project-state.md
```

非代码项目可使用已获批准的持久文件位置；没有持久后端时，Skill 会提供中文 checkpoint，并明确说明无法保证跨线程恢复。状态文件不得包含密钥、凭据或不必要的个人数据。

## 模块化内置能力

三个上游工作树均固定到明确提交并最大化收录；Matt 的一个符号链接为跨平台 ZIP 解压物化为同内容普通文件，Nature 中明确未授权再分发的 `figures4papers` 载荷被排除并保留其声明，其余上游文件内容保持不变：

| 模块 | 收录范围 | 入口 | 典型能力 |
| --- | --- | --- | --- |
| [Matt Pocock Skills](https://github.com/mattpocock/skills) | 37 个 Skill 及其文档、模板和仓库配套文件 | [`modules/mattpocock-skills/MODULE.md`](modules/mattpocock-skills/MODULE.md) | Grill Me、规格、票据、TDD、诊断、代码审查、架构、交接、教学 |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | 6 个 Skill，以及命令、hooks、MCP、示例、测试和多平台适配 | [`modules/ponytail/MODULE.md`](modules/ponytail/MODULE.md) | 最小实现、复杂度审查、全库审计、技术债台账 |
| [Nature Skills](https://github.com/Yuan1z0825/nature-skills) | 20 个科研 Skill 目录及所有可再分发脚本、模板、静态资料和图像资产 | [`modules/nature-skills/MODULE.md`](modules/nature-skills/MODULE.md) | 检索、精读、写作、润色、统计、绘图、审稿、数据、专利、PPT |

一级入口只读取 [`modules/README.md`](modules/README.md) 和一个匹配的模块适配器，再读取具体叶子 Skill。大型资产和无关说明保持休眠，因此包体积与单次上下文消耗解耦。

“已经内置”表示指令和文件可直接访问，不表示 hooks、MCP、浏览器、Python/R/npm 依赖、数据库账号或付费服务已经安装或授权。涉及执行、依赖和外部访问时，Skill 会先检查脚本与环境，并在计划中单独说明。

固定提交、快照范围、排除项、许可证和归属见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)；机器可读版本见 [`modules/LOCK.json`](modules/LOCK.json)，每个已收录快照另有完整 SHA-256 清单。

## 仓库结构

```text
.
├── SKILL.md                    # Agent Skill 入口
├── agents/openai.yaml          # Codex UI 元数据
├── modules/                    # 三个最大可再分发快照、适配器、锁文件和哈希清单
├── references/                 # 按需加载的工作流与测试说明
├── LICENSES/                   # 内置上游片段的许可证副本
├── scripts/validate_repo.py    # 零依赖仓库校验
├── scripts/module_manifest.py  # 上游快照完整性校验
├── docs/architecture.md        # 设计、边界与降级策略
├── .github/                    # CI、Issue 和 PR 模板
├── THIRD_PARTY_NOTICES.md      # 上游版本、哈希、归属与修改说明
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE.md
```

## 验证

本地运行：

```bash
python3 scripts/module_manifest.py verify
python3 scripts/validate_repo.py
```

维护者还可以使用 Agent Skills 官方规范推荐的 `skills-ref`：

```bash
skills-ref validate .
```

GitHub Actions 会在 push 和 pull request 时运行仓库内的零依赖校验器。

## 已知边界

- Skill 无法让协调 agent 在收到消息前完全看不到原始 prompt；它只能要求协调 agent 在开始求解前先完成 intake。
- 新线程不会继承激活状态；用户必须重新调用 Skill，之后才可用明确、未过期的项目状态记录恢复进度。
- 缺少 Plan 或子 agent 能力时会明确降级，不能把本地自检描述为独立验收。
- 内置运行文件不自动注册宿主插件、hooks 或 MCP，也不自动安装第三方依赖。
- 本 Skill 管理工作流，不会绕过宿主平台的权限、审批或安全策略。

更多设计说明见 [docs/architecture.md](docs/architecture.md)。更新内置上游版本前阅读 [docs/module-maintenance.md](docs/module-maintenance.md)；参与贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [SECURITY.md](SECURITY.md)。

准备创建 GitHub 仓库、配置保护规则或制作 Release 时，请按 [GitHub 发布指南](docs/publishing.md) 操作。建议仓库名保持为 `zh-complex-project-orchestrator`，使仓库根目录名与 Skill 名一致。

## 许可证

本项目原创内容采用 [MIT License](LICENSE.md)。完整内置的第三方快照继续适用各自的 MIT 或 Apache-2.0 条款；重新分发时须保留快照中的许可证、[第三方声明](THIRD_PARTY_NOTICES.md) 和 `LICENSES/`。
