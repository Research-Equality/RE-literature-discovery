# RE-literature-discovery

权威的文献调研与综述相关 Skills 仓库。

这个仓库聚焦学术文献工作流中最核心的一条主链：检索、阅读、归纳、引用管理、Related Work 写作，以及完整 Survey 生成。它不是通用科研全流程工具箱，而是专门收录和维护所有与 literature discovery、literature review、survey writing 直接相关的技能。

## 定位

- 只保留文献调研、综述撰写、引用治理相关 skills
- 统一整理为仓库内可移植的目录结构，不依赖某个作者的本地绝对路径
- 作为后续新增相关 skills 的唯一权威入口

## 当前收录

主链技能位于 [`skills/`](skills/)：

- `literature-search`: 多源学术检索，生成结构化 JSONL/BibTeX
- `literature-review`: 多视角文献综述与知识归纳
- `deep-research`: 六阶段系统化文献调研流水线
- `citation-management`: BibTeX 采集、校验、去重、补全
- `related-work-writing`: 论文 Related Work 写作
- `survey-generation`: 完整综述论文生成

技能目录说明见 [`skills/README.md`](skills/README.md)。

## 仓库结构

```text
skills/
  literature-search/
  literature-review/
  deep-research/
  citation-management/
  related-work-writing/
  survey-generation/
```

## 使用约定

命令示例默认从仓库根目录执行。

```bash
python skills/deep-research/scripts/search_semantic_scholar.py \
  --query "long-context reasoning agents" \
  --max-results 20 \
  --api-key "$S2_API_KEY"
```

推荐环境：

- Python 3.10+
- 可选环境变量：`S2_API_KEY`
- 可选依赖：`PyMuPDF`（PDF 提取）

深度调研产物默认建议写入 `outputs/<topic-slug>/`，避免污染技能目录本身。

## ResearchClaw 一键加载

为了兼容 `ResearchClaw` 的 GitHub 一键安装流程，仓库根目录现在额外提供了：

- [`SKILL.md`](SKILL.md)：仓库级入口 skill
- [`references/`](references/)：给一键安装后的根 skill 使用的镜像参考资料
- [`scripts/`](scripts/)：给一键安装后的根 skill 使用的镜像脚本

也就是说：

- 本地/仓库内的权威技能目录仍然是 [`skills/`](skills/)
- `ResearchClaw` 如果直接从仓库 GitHub URL 安装，会命中根目录 [`SKILL.md`](SKILL.md)，并拿到可执行的 `scripts/` 与可读的 `references/`

这个兼容层是为了让“整个仓库”可以被一键加载，不改变 `skills/` 作为权威来源的定位。

## 收录原则

- 必须直接服务于文献发现、阅读、综述、引用或 related work 写作
- 不收录与实验、代码实现、投稿排版、答辩汇报等主线无关的 skills
- 优先保留可脚本化、可复用、可审计的能力

## 来源

当前技能集主要由本地 `agent-research-skills/` 来源快照中的相关技能筛选和重构而来。规范化后的权威版本以 [`skills/`](skills/) 为准。
