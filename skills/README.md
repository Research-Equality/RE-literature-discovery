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

## Environment Contract

需要外部配置的 skill 必须在 `SKILL.md` frontmatter 中声明 `requires.env`。

| Variable | Skills | Required | Purpose |
| --- | --- | --- | --- |
| `S2_API_KEY` | `literature-search`, `systematic-review`, `citation-management` | No | Semantic Scholar higher rate limits |
| `OPENALEX_EMAIL` | `literature-search`, `openalex-database` | No | OpenAlex polite-pool requests |
| `CROSSREF_EMAIL` | `literature-search` | No | Crossref User-Agent contact email |
| `NCBI_API_KEY` | `pubmed-database` | No | PubMed higher rate limits |
| `NCBI_EMAIL` | `pubmed-database` | No | PubMed workflow contact email |
| `ZOTERO_LIBRARY_ID`, `ZOTERO_API_KEY`, `ZOTERO_LIBRARY_TYPE` | `pyzotero` | Yes | Zotero library access |

## Core Skills

推荐星级说明：
- `5/5`：默认优先使用，或对大多数文献调研流程都关键
- `4/5`：强力配套，常用
- `3/5`：偏专用，按需使用

| Skill | 功能 | 参考仓库 | 推荐星级 | 目录 |
| --- | --- | --- | --- | --- |
| `literature-search` | 检索、合并、去重、初筛，并把语料移交给 authority layer | `agent-research-skills` | `5/5` | [`skills/literature-search/`](literature-search/) |
| `venue-authority-resolver` | 统一 `venue_type`、`peer_reviewed`、`is_preprint`，并接入 CCF 与 journal metrics resolver | `repository-native` | `5/5` | [`skills/venue-authority-resolver/`](venue-authority-resolver/) |
| `paper-quality-filter` | 生成 `quality_flags` 与 `caution_flags`，并标出 `preprint_only`、`weak_metadata` 等写作风险 | `repository-native` | `4/5` | [`skills/paper-quality-filter/`](paper-quality-filter/) |
| `authority-ranking` | 唯一的 `final_score`、`selection_bucket`、`authority_reason`、`ranking_components` 计算入口 | `repository-native` | `5/5` | [`skills/authority-ranking/`](authority-ranking/) |
| `evidence-grading` | 生成 `evidence_score` 与证据标签，并补 `high_authority_low_evidence` 等 caution flag | `PaperClaw` | `5/5` | [`skills/evidence-grading/`](evidence-grading/) |
| `literature-review` | 对已排序语料做主题归纳和证据整合，同时承接 comparison / consensus / contradiction / gap 等分析模式 | `agent-research-skills` | `5/5` | [`skills/literature-review/`](literature-review/) |
| `systematic-review` | 多阶段系统化调研工作区，Phase 2 必须产出 authority-aware corpus、evidence summary 和 ranking audit | `agent-research-skills + AI-research-SKILLs` | `5/5` | [`skills/systematic-review/`](systematic-review/) |
| `related-work-writing` | 按 `core / supporting / frontier` 与 caution flags 控制 Related Work 语气 | `agent-research-skills + AI-research-SKILLs` | `4/5` | [`skills/related-work-writing/`](related-work-writing/) |
| `survey-generation` | 按 bucket-aware 规则规划和写 survey manuscript | `agent-research-skills + AI-research-SKILLs` | `4/5` | [`skills/survey-generation/`](survey-generation/) |

## Authority and Metadata Skills

| Skill | 功能 | 参考仓库 | 推荐星级 | 目录 |
| --- | --- | --- | --- | --- |
| `ccf-ranking` | 基于官方 snapshot、alias 层和 resolver 的可审计 CCF 解析 | `repository-native` | `5/5` | [`skills/ccf-ranking/`](ccf-ranking/) |
| `journal-metrics` | 基于 source-of-record、open fallback、local override 的可审计期刊指标解析 | `repository-native` | `4/5` | [`skills/journal-metrics/`](journal-metrics/) |
| `field-ranking-profile` | 控制不同领域的 authority-aware ranking 权重和阈值 | `repository-native` | `3/5` | [`skills/field-ranking-profile/`](field-ranking-profile/) |

## Source and Citation Companions

| Skill | 功能 | 参考仓库 | 推荐星级 | 目录 |
| --- | --- | --- | --- | --- |
| `arxiv-database` | arXiv 定向检索和下载 | `claude-scientific-skills` | `4/5` | [`skills/arxiv-database/`](arxiv-database/) |
| `biorxiv-database` | bioRxiv 定向预印本检索 | `claude-scientific-skills` | `3/5` | [`skills/biorxiv-database/`](biorxiv-database/) |
| `openalex-database` | OpenAlex 来源、作者与 citation metadata 检索 | `claude-scientific-skills` | `4/5` | [`skills/openalex-database/`](openalex-database/) |
| `pubmed-database` | PubMed / MEDLINE 生物医学检索 | `claude-scientific-skills` | `4/5` | [`skills/pubmed-database/`](pubmed-database/) |
| `citation-management` | BibTeX 校验、修复与 cite key 管理 | `agent-research-skills + AI-research-SKILLs` | `4/5` | [`skills/citation-management/`](citation-management/) |
| `pyzotero` | Zotero 库同步、导出与自动化 | `claude-scientific-skills` | `3/5` | [`skills/pyzotero/`](pyzotero/) |

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
