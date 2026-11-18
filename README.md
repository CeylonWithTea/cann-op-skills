# CANN Operator Development Skills

一套轻量、可跨设备复用的 CANN Ascend C 算子开发技能，覆盖调研、规格、实现、测试、demo 迭代、性能比较、自审和 issue/PR 提交。主要说明使用中文。

## 技能

| 技能 | 作用 |
| --- | --- |
| [cann-op-develop](skills/cann-op-develop/SKILL.md) | 调研、确定规格、从基础实现迭代到通过验证的 demo |
| [cann-op-review](skills/cann-op-review/SKILL.md) | 依据真实缺陷模式检查语义、数值、资源、同步和测试 |
| [cann-op-env-check](skills/cann-op-env-check/SKILL.md) | 确认现有环境，不强制远程连接、Docker 或重装 CANN |
| [cann-op-submit](skills/cann-op-submit/SKILL.md) | 管理 fork/分支、准备 issue/PR、按授权发布和处理评审 |

日常使用开发主入口，其余技能按需调用。默认由当前 Agent 连续执行，不依赖 CANNBot/harness 或逐节点审批。

## 安装

下载或克隆本仓库，在仓库根目录执行：

```bash
# 将路径替换为你的客户端实际技能目录
python3 skills/install.py --dest /path/to/client/skills --dry-run
python3 skills/install.py --dest /path/to/client/skills

# Codex 用户级目录示例
python3 skills/install.py --dest "${CODEX_HOME:-$HOME/.codex}/skills"
```

安装器只依赖 Python 3 标准库，复制四个完整技能目录；已有同名技能时停止，不覆盖或合并，也不修改项目指引。安装后按客户端要求重新加载技能或开启新会话。

也可手动复制 `skills/cann-op-*` 四个目录。无法自动发现技能的工具，可以明确读取相应 SKILL.md 和按需引用的资源。项目入口可参考 [AGENTS.fragment.md](skills/AGENTS.fragment.md)，与项目已有规则合并。

## 使用

```text
使用 cann-op-develop 开发 <算子>，仓库为 <位置>，目标平台为 <SoC/CANN>。
先读取已有资料，集中确认真正缺失的规格问题，再自主完成 demo 迭代。
```

具体使用和授权边界见 [完整说明](skills/README.md)。不绑定某台设备、固定容器、账号、密钥或统一精度容差。

## 版本与迁移包

当前版本：1.0.0。

- [ZIP 迁移包](releases/cann-op-skills-1.0.0.zip)
- [ZIP SHA256](releases/cann-op-skills-1.0.0.zip.sha256)

ZIP 内含完整技能目录、安装脚本、说明和逐文件校验清单。源码用于维护与审查，迁移包便于直接复制到另一台设备。

## 来源与验证

方法提炼自 AdaptiveThreshold、FloodFill、LaplacianOfGaussian 的开发过程及一批 CANN ops-cv PR 检视意见；详见 [来源与取舍](skills/PROVENANCE.md)。历史记录不代表新算子已通过验证，API 和平台限制需核对实际版本。

首版已检查四个技能的格式、相对链接、跨目录安装、覆盖保护、失败恢复及四类独立使用场景，并验证迁移包完整性。尚未在所有客户端或另一台物理机器上实测自动发现。
