# Skills Catalog

这里是仓库内唯一维护的文献综述 skills 目录。

## Authority-Aware Workflow

唯一权威主链：

`literature-search -> venue-authority-resolver -> paper-quality-filter -> authority-ranking -> evidence-grading -> authority-ranking -> literature-review/systematic-review -> related-work-writing/survey-generation`

约束：

1. `authority-ranking` 是唯一允许写 `final_score` 的 skill
2. `evidence-grading` 可以读取 authority metadata，但不能把 venue prestige 直接当作 evidence strength
3. `evidence-grading` 之后必须重新运行一次 `authority-ranking`
4. `weak_metadata` 是结构性元数据不足，不等于某个 authority source 没命中
5. `ccf-ranking` 优先服务 CS / AI / security 语料
6. `journal-metrics` 必须保持 source-of-record / open-fallback / local-override 三层可替换
7. 写作层必须根据 `selection_bucket` 和 `caution_flags` 调整语气

## Shared Artifacts

- `outputs/<topic-slug>/search_results/<source>.jsonl`
- `outputs/<topic-slug>/paper_db.raw.jsonl`
- `outputs/<topic-slug>/paper_db.triaged.jsonl`
- `outputs/<topic-slug>/paper_db.jsonl`
- `outputs/<topic-slug>/paper_db.evidence.jsonl`
- `outputs/<topic-slug>/analysis/ranking_report.md`
- `outputs/<topic-slug>/analysis/resolution_audit.jsonl`
- `outputs/<topic-slug>/analysis/evidence_summary.md`
- `outputs/<topic-slug>/review/`
- `outputs/<topic-slug>/phase*/`
- `outputs/<topic-slug>/survey/`
- `references.bib`

## Core Skills

### `literature-search`

用途：检索、合并、去重、初筛，并把语料移交给 authority layer。

目录：[`skills/literature-search/`](literature-search/)

### `venue-authority-resolver`

用途：统一 `venue_type`、`peer_reviewed`、`is_preprint`，并接入 CCF 与 journal metrics resolver。

目录：[`skills/venue-authority-resolver/`](venue-authority-resolver/)

### `paper-quality-filter`

用途：生成 `quality_flags` 与 `caution_flags`，并标出 `preprint_only`、`weak_metadata` 等写作风险。

目录：[`skills/paper-quality-filter/`](paper-quality-filter/)

### `authority-ranking`

用途：唯一的 `final_score`、`selection_bucket`、`authority_reason`、`ranking_components` 计算入口。

目录：[`skills/authority-ranking/`](authority-ranking/)

### `evidence-grading`

用途：生成 `evidence_score` 与证据标签，并补 `high_authority_low_evidence` 等 caution flag。

目录：[`skills/evidence-grading/`](evidence-grading/)

### `literature-review`

用途：对已排序语料做主题归纳和证据整合，同时承接 comparison / consensus / contradiction / gap 等分析模式。

目录：[`skills/literature-review/`](literature-review/)

### `systematic-review`

用途：多阶段系统化调研工作区，Phase 2 必须产出 authority-aware corpus、evidence summary 和 ranking audit；citation expansion 与 monitoring 也作为内置模式放在这里。

目录：[`skills/systematic-review/`](systematic-review/)

### `related-work-writing`

用途：按 `core / supporting / frontier` 与 caution flags 控制 Related Work 语气。

目录：[`skills/related-work-writing/`](related-work-writing/)

### `survey-generation`

用途：按 bucket-aware 规则规划和写 survey manuscript。

目录：[`skills/survey-generation/`](survey-generation/)

## Authority and Metadata Skills

### `ccf-ranking`

用途：基于官方 snapshot、alias 层和 resolver 的可审计 CCF 解析。

目录：[`skills/ccf-ranking/`](ccf-ranking/)

### `journal-metrics`

用途：基于 source-of-record、open fallback、local override 的可审计期刊指标解析。

目录：[`skills/journal-metrics/`](journal-metrics/)

### `field-ranking-profile`

用途：控制不同领域的 authority-aware ranking 权重和阈值。

目录：[`skills/field-ranking-profile/`](field-ranking-profile/)

## Source and Citation Companions

- `arxiv-database`
- `biorxiv-database`
- `openalex-database`
- `pubmed-database`
- `pyzotero`
- `citation-management`

## Embedded Analysis Modes

以下能力不再作为单独顶层 skill 维护，而是作为 `literature-review` / `systematic-review` 的内置模式保留：

- cross-paper synthesis
- consensus mapping
- contradiction analysis
- claim tracking
- gap detection
- citation-graph expansion
- arXiv monitoring

## Maintenance Rules

- 新 skill 必须直接服务于文献发现、authority-aware 排序、证据整合或综述写作
- 如果一个能力只有说明、没有独立脚本和数据契约，应优先并入已有主 skill，而不是拆成新的顶层 skill
- 如果一个新来源只是 metadata 或 authority 补充，应优先并入现有 authority layer，而不是复制第二套总排序逻辑
- 所有匹配与指标解析都必须可审计、可解释、可替换
