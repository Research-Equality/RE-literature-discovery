# Skills Catalog

这里是仓库内唯一维护的文献综述 skills 目录。

## Routing Rules

推荐按这条 authority-aware 主链使用：

1. `literature-search`
2. `venue-authority-resolver`
3. `paper-quality-filter`
4. `authority-ranking`
5. `evidence-grading`
6. `literature-review` 或 `systematic-review`
7. `related-work-writing` 或 `survey-generation`

补充规则：

1. `authority-ranking` 是唯一允许写 `final_score` 的 skill
2. `evidence-grading` 可以读取 authority metadata，但不能把 venue prestige 直接当作 evidence strength
3. `ccf-ranking` 在 CS 语料场景优先
4. `journal-metrics` 必须保持可插拔
5. `related-work-writing` 与 `survey-generation` 应按 `selection_bucket` 控制选材

## Shared Artifacts

- `outputs/<topic-slug>/search_results/<source>.jsonl`
- `outputs/<topic-slug>/paper_db.raw.jsonl`
- `outputs/<topic-slug>/paper_db.triaged.jsonl`
- `outputs/<topic-slug>/paper_db.jsonl`
- `outputs/<topic-slug>/paper_db.evidence.jsonl`
- `outputs/<topic-slug>/review/`
- `outputs/<topic-slug>/phase*/`
- `outputs/<topic-slug>/survey/`
- `references.bib`

## Core Skills

### `literature-search`

用途：检索、合并、去重、初筛，并把语料移交给 authority layer。

目录：[`skills/literature-search/`](literature-search/)

### `venue-authority-resolver`

用途：补齐 `venue_type`、`peer_reviewed`、`is_preprint`、`ccf_rank`、`jcr_quartile` 等 authority metadata。

目录：[`skills/venue-authority-resolver/`](venue-authority-resolver/)

### `paper-quality-filter`

用途：生成 `quality_flags` 与 `caution_flags`，并按元数据策略做可选过滤。

目录：[`skills/paper-quality-filter/`](paper-quality-filter/)

### `authority-ranking`

用途：唯一的 `final_score` 和 `selection_bucket` 计算入口。

目录：[`skills/authority-ranking/`](authority-ranking/)

### `evidence-grading`

用途：生成 `evidence_score` 与证据标签，服务于下游写作校准。

目录：[`skills/evidence-grading/`](evidence-grading/)

### `literature-review`

用途：对已排序语料做主题归纳和证据整合。

目录：[`skills/literature-review/`](literature-review/)

### `systematic-review`

用途：多阶段系统化调研工作区，Phase 2 现在必须产出 authority-aware corpus。

目录：[`skills/systematic-review/`](systematic-review/)

### `related-work-writing`

用途：按 `selection_bucket` 和证据标签生成单篇论文的 Related Work。

目录：[`skills/related-work-writing/`](related-work-writing/)

### `survey-generation`

用途：按 bucket-aware 逻辑生成完整 survey manuscript。

目录：[`skills/survey-generation/`](survey-generation/)

## Authority and Metadata Skills

### `ccf-ranking`

用途：CS 场景下的会议权威性补充层。

目录：[`skills/ccf-ranking/`](ccf-ranking/)

### `journal-metrics`

用途：期刊分区、影响因子、核心级别等可插拔指标层。

目录：[`skills/journal-metrics/`](journal-metrics/)

### `field-ranking-profile`

用途：控制不同领域的 authority-aware ranking 权重和阈值。

目录：[`skills/field-ranking-profile/`](field-ranking-profile/)

## Discovery, Database, and Analysis Companions

- `arxiv-database`
- `biorxiv-database`
- `openalex-database`
- `pubmed-database`
- `pyzotero`
- `arxiv-monitor`
- `citation-graph`
- `gap-detection`
- `claim-tracker`
- `consensus-mapping`
- `contradiction-detection`
- `cross-paper-synthesis`
- `citation-management`

## Maintenance Rules

- 新 skill 必须直接服务于文献发现、authority-aware 排序、证据整合或综述写作
- 如果一个新来源的能力只是 authority metadata 补充，应优先并入 authority layer，而不是复制第二套排序逻辑
- 不要让 `literature-search`、`evidence-grading`、`authority-ranking` 同时各自计算不同版本的最终总分
