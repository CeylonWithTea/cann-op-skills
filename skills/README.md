# CANN 算子开发技能包

版本：1.0.0（2026-11-18）。将四个技能目录整体复制即可跨设备复用；不需要历史支持目录、CANNBot、固定 Docker 镜像或某个账号。开发和环境配置在目标机器上独立确认。

## 入口

| Skill | 使用时机 |
| --- | --- |
| [cann-op-develop](cann-op-develop/SKILL.md) | 开始或继承算子开发、补功能、数值修复、demo 优化 |
| [cann-op-review](cann-op-review/SKILL.md) | 优化自审、独立代码检视、PR 整改复核 |
| [cann-op-env-check](cann-op-env-check/SKILL.md) | 确认已有环境、换机器/工具链、诊断旧包混用 |
| [cann-op-submit](cann-op-submit/SKILL.md) | 管理 fork/分支、准备 issue/PR、提交及评审跟进 |

日常只需主入口，其他部分按需加载。每个技能的入口保持简短，详细方法和模板位于各自目录中。不安装这些配套工具时，主入口仍给出必要的检查底线；推荐整包安装以便独立调用。

## 复制与安装

发布包位于同级上层的 `releases/cann-op-skills-1.0.0.zip`。也可直接复制本 `skills/` 目录。归档中的 `cann-op-skills-1.0.0/` 与此目录内容一致，附有 `SHA256SUMS` 供校验。

1. 将技能包复制或解压到目标机器。
2. 确认目标客户端的技能目录，把四个 `cann-op-*` 完整目录放入其中；不要只复制 SKILL.md。不支持技能发现的工具，可以明确让其读取主入口及按需引用的资源。
3. 重新加载客户端的技能列表或开启新会话。不同客户端的刷新方式以实际支持能力为准。

可使用仅依赖 Python 3 标准库的安装脚本：

```bash
# 在本技能包根目录执行；--dest 填目标客户端实际技能目录
python3 install.py --dest /path/to/client/skills --dry-run
python3 install.py --dest /path/to/client/skills

# Codex 用户级目录示例；如已设置 CODEX_HOME，则使用它
python3 install.py --dest "${CODEX_HOME:-$HOME/.codex}/skills"
```

脚本只复制四个技能目录；遇到任一同名目标立即停止，不覆盖、不合并、不改 AGENTS.md/CLAUDE.md 或环境。升级时先比较并备份目标旧目录，再自行移走旧版后安装。客户端目录可写且安装获授权时才执行。

本工作区直接通过根 AGENTS.md 指向源目录，未额外复制到用户级技能目录。迁移时无需携带本工作区 AGENTS.md：如需项目入口，可参考 [可选项目指引](AGENTS.fragment.md)，与目标项目现有规则合并。skill 不会自行取消目标项目的审批或工作流约定。

## 使用示例

```text
使用 cann-op-develop 开发 <算子>。仓库为 <位置>，目标平台为 <SoC/CANN>。
先读取已有支持资料，集中提出真正缺失的规格问题；之后自主完成 demo 迭代。

使用 cann-op-review 检视当前分支相对 <目标分支> 的差异。
重点关注本次 tiling 与类型转换变化，只报告有依据的问题。

使用 cann-op-env-check 确认当前环境，沿用已有容器，不安装或修改共享依赖。

使用 cann-op-submit 准备 <算子> 的 issue 和 PR 正文，暂不发布。
```

需要发布时明确平台、fork/目标分支及是否授权推送、创建 issue/PR、回复评审。身份与认证沿用已确认配置；skill 不携带任何密钥。

## 来源与适用边界

方法来自 AdaptiveThreshold、FloodFill、LaplacianOfGaussian 的迭代和 18 个 PR 的审查经验，出处与取舍见 [来源说明](PROVENANCE.md)。这些历史结果不代表新算子或新设备已经通过验证。

技能包不固化 CANN 版本、API 数值限制、物理卡号、golden 容差或性能目标。具体任务以当前仓库、目标平台资料及用户确认的约定为准；主 skill 不绑定 CANN Bench 的直调评测接口，也不强制采用某个开发框架。
