[English](README.md) | [简体中文](README.zh.md)

# RE-literature-discovery

权威的文献发现、权威性排序、证据整合与综述写作 skills 仓库。

这个仓库围绕一条分层主链组织：
- discovery
- authority enrichment
- ranking
- evidence grading
- review writing
- survey writing

它不是通用科研工具箱，而是专门维护与文献调研、文献综述、survey 生成直接相关的技能集合。

## 定位

- 只保留文献综述主链相关 skill
- 用统一 paper schema 串起所有下游环节
- 让排序逻辑可审计，而不是藏在单个搜索脚本里
- 支持作为 ResearchClaw 外部 skills 源，从 `skills/` 直接加载

## Authority-Aware Workflow

推荐主链：

1. `literature-search`
2. `venue-authority-resolver`
3. `paper-quality-filter`
4. `authority-ranking`
5. `evidence-grading`
6. `literature-review` 或 `systematic-review`
7. `related-work-writing` 或 `survey-generation`

其中只有 `authority-ranking` 应该写入 `final_score`。

## 当前收录

技能集合位于 [`skills/`](skills/)。

### 发现与主工作流

- `literature-search`
- `literature-review`
- `systematic-review`
- `citation-management`
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
- `pyzotero`

### 监控与语料分析

- `arxiv-monitor`
- `citation-graph`
- `gap-detection`
- `claim-tracker`
- `consensus-mapping`
- `contradiction-detection`
- `cross-paper-synthesis`
- `evidence-grading`

技能目录见 [`skills/README.md`](skills/README.md)。

## 统一 Paper Schema

权威主语料文件是 `outputs/<topic-slug>/paper_db.jsonl`。

每条记录至少包含：

- `paper_id`, `title`, `authors`, `year`, `venue`, `venue_type`, `doi`, `citation_count`
- `peer_reviewed`, `is_preprint`, `ccf_rank`, `core_rank`, `jcr_quartile`, `impact_factor`, `cas_quartile`
- `authority_score`, `relevance_score`, `citation_score`, `recency_score`, `evidence_score`, `final_score`
- `selection_bucket`, `ranking_reason`, `caution_flags`, `quality_flags`

完整 JSON schema 位于 [`skills/authority-ranking/schemas/paper_record.schema.json`](skills/authority-ranking/schemas/paper_record.schema.json)。

## 共享产物

- `outputs/<topic-slug>/search_results/*.jsonl`
- `outputs/<topic-slug>/paper_db.raw.jsonl`
- `outputs/<topic-slug>/paper_db.triaged.jsonl`
- `outputs/<topic-slug>/paper_db.jsonl`
- `outputs/<topic-slug>/paper_db.evidence.jsonl`
- `outputs/<topic-slug>/research_log.md`
- `outputs/<topic-slug>/findings.md`
- `references.bib`
- `outputs/<topic-slug>/review/`
- `outputs/<topic-slug>/phase*/`
- `outputs/<topic-slug>/survey/`

## 最小工作流示例

见 [`examples/authority-aware-minimal/README.md`](examples/authority-aware-minimal/README.md)。

离线 smoke test：

```bash
python skills/literature-search/scripts/prepare_corpus.py \
  --query "language model reasoning agents" \
  --inputs examples/authority-aware-minimal/seed_papers.jsonl \
  --merged-output outputs/authority-offline/paper_db.raw.jsonl \
  --triaged-output outputs/authority-offline/paper_db.triaged.jsonl \
  --authority-output outputs/authority-offline/paper_db.jsonl \
  --profile cs
```

## ResearchClaw 兼容性

这个仓库可以作为 [ResearchClaw](https://github.com/ymx10086/ResearchClaw) 的外部 skills 来源。

在 ResearchClaw 中使用时，应把本仓库的 [`skills/`](skills/) 目录视为权威可加载 skill 集合；根 README 和 skills catalog 负责说明路由规则、共享产物与边界。

## 收录原则

- skill 必须直接服务于文献发现、authority-aware 排序、证据整合、引用治理或综述写作
- 实验、实现、排版、演示类 skill 不应放在这里
- 优先保留可脚本化、可审计的工作流

## 来源

仓库由以下本地来源整理而来：

- `agent-research-skills/`
- `claude-scientific-skills/`
- `PaperClaw/`
- `AI-research-SKILLs/`

这里只保留与文献综述直接相关的能力。规范化后的权威版本以 [`skills/`](skills/) 为准。
