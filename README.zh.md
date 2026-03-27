[English](README.md) | [简体中文](README.zh.md)

# RE-literature-discovery

权威的文献发现、authority-aware 排序、证据整合与综述写作 skills 仓库。

仓库围绕一条完全同步的主链组织：

`literature-search -> venue-authority-resolver -> paper-quality-filter -> authority-ranking -> evidence-grading -> authority-ranking -> literature-review/systematic-review -> related-work-writing/survey-generation`

## 定位

- 只保留文献综述主链相关 skills
- 把 authority layer 的数据源质量、可审计性、可维护性补硬
- 用统一 paper schema 串起所有下游环节
- 让排序逻辑可解释，而不是埋在搜索脚本里
- 支持作为 ResearchClaw 外部 skills 源，从 `skills/` 直接加载

## Authority-Aware Workflow

### 1. Discovery

`literature-search` 负责检索、合并、去重和初筛。

### 2. Venue 与指标解析

- `venue-authority-resolver` 负责统一 authority metadata
- `ccf-ranking` 使用 `data/ccf_official_snapshot.json` 与 `data/ccf_aliases.json`
- `journal-metrics` 使用 source-of-record、open fallback、local override 三层来源

### 3. 排序与审计

只有 `authority-ranking` 可以写入：
- `final_score`
- `selection_bucket`
- `authority_reason`
- `ranking_components`
- `ranking_profile`

同时它会输出：
- `outputs/<topic-slug>/analysis/ranking_report.md`
- `outputs/<topic-slug>/analysis/resolution_audit.jsonl`

### 4. 证据、重排与写作

- `evidence-grading` 会读取 authority metadata，但不会把 venue prestige 直接等同于 evidence strength
- `evidence-grading` 之后必须再跑一次 `authority-ranking`，保证 `final_score` 与 `selection_bucket` 仍然是权威结果
- `related-work-writing` 与 `survey-generation` 使用 bucket-aware 语气控制：
  - `core`: canonical / backbone
  - `supporting`: comparative / supportive
  - `frontier`: cautious / tentative

Frontier paper 不允许写成 established consensus。

## 当前收录

### 发现与主工作流

- `literature-search`
- `evidence-grading`
- `literature-review`
- `systematic-review`
- `related-work-writing`
- `survey-generation`

### 权威性与排序

- `venue-authority-resolver`
- `authority-ranking`
- `ccf-ranking`
- `journal-metrics`
- `paper-quality-filter`
- `field-ranking-profile`

### 数据库与参考管理

- `arxiv-database`
- `biorxiv-database`
- `openalex-database`
- `pubmed-database`
- `citation-management`
- `pyzotero`

## 内嵌分析模式

仓库不再把只有说明、没有独立实现的分析类能力保留为单独顶层 skill。

下面这些能力已经并入 `literature-review` 和 `systematic-review` 的内置分析模式：

- comparison table 与 cross-paper synthesis
- consensus / contested claim mapping
- contradiction 与 claim tracking
- gap detection 与 positioning
- citation-graph expansion 与持续 arXiv monitoring

技能目录见 [`skills/README.md`](skills/README.md)。

## 统一 Paper Schema

权威主语料文件是 `outputs/<topic-slug>/paper_db.jsonl`。

每条记录至少包含：

- bibliographic 字段：`paper_id`, `title`, `authors`, `year`, `venue`, `venue_type`, `doi`, `citation_count`
- authority 字段：`peer_reviewed`, `is_preprint`, `ccf_rank`, `core_rank`, `jcr_quartile`, `impact_factor`, `cas_quartile`
- score 字段：`authority_score`, `relevance_score`, `citation_score`, `recency_score`, `evidence_score`, `final_score`
- 写作控制字段：`selection_bucket`, `ranking_reason`, `caution_flags`, `quality_flags`
- 审计字段：`source_of_truth`, `source_version`, `resolved_from`, `match_confidence`, `authority_reason`, `ranking_components`, `ranking_profile`, `last_verified_at`

完整 JSON schema 位于 [`skills/authority-ranking/schemas/paper_record.schema.json`](skills/authority-ranking/schemas/paper_record.schema.json)。

## 共享产物

- `outputs/<topic-slug>/search_results/*.jsonl`
- `outputs/<topic-slug>/paper_db.raw.jsonl`
- `outputs/<topic-slug>/paper_db.triaged.jsonl`
- `outputs/<topic-slug>/paper_db.jsonl`
- `outputs/<topic-slug>/paper_db.evidence.jsonl`
- `outputs/<topic-slug>/analysis/ranking_report.md`
- `outputs/<topic-slug>/analysis/resolution_audit.jsonl`
- `outputs/<topic-slug>/analysis/evidence_summary.md`
- `outputs/<topic-slug>/research_log.md`
- `outputs/<topic-slug>/findings.md`
- `references.bib`
- `outputs/<topic-slug>/review/`
- `outputs/<topic-slug>/phase*/`
- `outputs/<topic-slug>/survey/`

## 最小工作流示例

见 [`examples/authority-aware-minimal/README.md`](examples/authority-aware-minimal/README.md)。

## ResearchClaw 兼容性

这个仓库可以作为 [ResearchClaw](https://github.com/ymx10086/ResearchClaw) 的外部 skills 来源。

在 ResearchClaw 中使用时，应把本仓库的 [`skills/`](skills/) 目录视为权威可加载 skill 集合；根 README 和 skills catalog 负责说明路由规则、共享产物与边界。

## 收录原则

- skill 必须直接服务于文献发现、authority-aware 排序、证据整合、引用治理或综述写作
- 如果某个分析模式不需要独立脚本或独立数据契约，应优先并入 `literature-review` 或 `systematic-review` 的 references，而不是继续保留单独顶层 skill
- 实验、实现、排版、演示类 skill 不应放在这里
- 优先保留可脚本化、可审计的工作流
