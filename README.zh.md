[English](README.md) | [简体中文](README.zh.md)

# RE-literature-discovery

权威的文献调研、证据整合与综述写作相关 Skills 仓库。

这个仓库聚焦学术文献工作流中最核心的一条主链：检索、阅读、归纳、引用管理、数据库检索、Related Work 写作，以及完整 Survey 生成。它不是通用科研全流程工具箱，而是专门收录和维护所有与 literature discovery、literature review、survey writing 直接相关的技能。

## 定位

- 只保留文献调研、综述撰写、引用治理与学术源发现相关 skills
- 统一整理为仓库内可移植的目录结构，不依赖某个作者的本地绝对路径
- 作为后续新增相关 skills 的唯一权威入口

## 当前收录

技能集合位于 [`skills/`](skills/)。

### 工作流技能

- `literature-search`: 多源学术检索，生成结构化 JSONL/BibTeX
- `literature-review`: 多视角文献综述与知识归纳
- `systematic-review`: 六阶段系统化文献调研流水线
- `citation-management`: BibTeX 采集、校验、去重、补全
- `related-work-writing`: 论文 Related Work 写作
- `survey-generation`: 完整综述论文生成

### 数据库与参考管理技能

- `arxiv-database`: arXiv 预印本检索与 PDF 拉取
- `biorxiv-database`: 面向生命科学文献的 bioRxiv 检索
- `openalex-database`: OpenAlex 学术检索与文献计量分析
- `pubmed-database`: PubMed 高级检索与 E-utilities 工作流
- `pyzotero`: Zotero 文献库自动化与参考文献管理集成

### 监控与分析技能

- `arxiv-monitor`: 持续 arXiv 监控与 digest 生成
- `citation-graph`: 基于引用网络寻找基础论文与桥接论文
- `gap-detection`: 识别开放问题与潜在创新空间
- `claim-tracker`: 追踪关键 claim 的来源、挑战与更新状态
- `consensus-mapping`: 区分领域共识与争议点
- `contradiction-detection`: 识别并组织相互冲突的研究结论
- `cross-paper-synthesis`: 生成跨论文对比表、时间线与主线归纳
- `evidence-grading`: 对论文或 claim 做证据强度分级

技能目录说明见 [`skills/README.md`](skills/README.md)。

## Skill 分工

为了避免职责重叠，这个仓库采用分层工作流：

- `literature-search` 是默认的多源文献发现入口
- `arxiv-database`、`biorxiv-database`、`openalex-database`、`pubmed-database` 负责各自数据库的高级能力
- `arxiv-monitor` 负责 topic 已定义后的持续监控
- `systematic-review` 负责端到端系统化调研
- `literature-review` 负责在已有论文集基础上做综述归纳
- `citation-graph`、`gap-detection`、`claim-tracker`、`consensus-mapping`、`contradiction-detection`、`cross-paper-synthesis`、`evidence-grading` 负责语料分析与跨论文综合
- `citation-management` 和 `pyzotero` 负责参考文献与文献库治理
- `related-work-writing` 只写单篇论文的 Related Work
- `survey-generation` 只生成完整综述稿件

共享产物约定：

- `outputs/<topic-slug>/search_results/*.jsonl` 保存原始检索结果
- `outputs/<topic-slug>/paper_db.jsonl` 作为统一论文语料主文件
- `outputs/<topic-slug>/research_log.md` 和 `outputs/<topic-slug>/findings.md` 用于长周期调研状态记录
- `references.bib` 作为当前写作任务的参考文献主文件
- `outputs/<topic-slug>/review/`、`outputs/<topic-slug>/phase*/`、`outputs/<topic-slug>/survey/` 作为下游写作产物目录

## 仓库结构

```text
skills/
  arxiv-monitor/
  arxiv-database/
  biorxiv-database/
  citation-graph/
  claim-tracker/
  consensus-mapping/
  contradiction-detection/
  cross-paper-synthesis/
  openalex-database/
  pubmed-database/
  pyzotero/
  evidence-grading/
  gap-detection/
  literature-search/
  literature-review/
  systematic-review/
  citation-management/
  related-work-writing/
  survey-generation/
```

## 使用约定

命令示例默认从仓库根目录执行。

```bash
python skills/systematic-review/scripts/search_semantic_scholar.py \
  --query "long-context reasoning agents" \
  --max-results 20 \
  --api-key "$S2_API_KEY"
```

推荐环境：

- Python 3.10+
- 可选环境变量：`S2_API_KEY`
- 可选依赖：`PyMuPDF`（PDF 提取）

系统化综述产物默认建议写入 `outputs/<topic-slug>/`，避免污染技能目录本身。

## 收录原则

- 必须直接服务于文献发现、阅读、综述、引用或 related work 写作
- 不收录与实验、代码实现、投稿排版、答辩汇报等主线无关的 skills
- 优先保留可脚本化、可复用、可审计的能力

## 来源

当前技能集主要由四个本地来源快照筛选和重构而来：

- `agent-research-skills/`：偏工作流的学术研究技能集
- `claude-scientific-skills/`：偏数据库、引用管理与学术工具的科学技能集
- `PaperClaw/`：偏文献监控、跨论文分析与团队知识管理的技能集
- `AI-research-SKILLs/`：偏 AI 研究编排与论文写作的技能集

这里只保留与文献调研和综述直接相关的技能。存在明显重叠的能力没有做一比一复制，而是合并进当前主链 skill 的职责边界中。规范化后的权威版本以 [`skills/`](skills/) 为准。

典型的合并关系包括：

- `PaperClaw/living-review` -> 由 `literature-review` 与 `systematic-review` 覆盖
- `PaperClaw/semantic-scholar` -> 由 `literature-search` 与 `systematic-review` 的检索工具覆盖
- `PaperClaw/zotero-integration` -> 由 `pyzotero` 与 `citation-management` 覆盖
- `AI-research-SKILLs/autoresearch` -> 被提炼为 `systematic-review` 的 workspace discipline 和可恢复模板
- `AI-research-SKILLs/ml-paper-writing` -> 被提炼为 `citation-management`、`related-work-writing` 与 `survey-generation` 的引用核验规则
