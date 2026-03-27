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

推荐星级说明：
- `5/5`：默认优先使用，或对大多数文献调研流程都关键
- `4/5`：强力配套，常用
- `3/5`：偏专用，按需使用

### 发现与主工作流

| Skill | 功能 | 参考仓库 | 推荐星级 |
| --- | --- | --- | --- |
| `literature-search` | 默认检索入口，负责 search、merge、dedup 和 early triage | `agent-research-skills` | `5/5` |
| `evidence-grading` | 评估证据强度，不把 venue prestige 直接当作 evidence | `PaperClaw` | `5/5` |
| `literature-review` | 把排序后的语料整理成主题化综述，并内置常见分析模式 | `agent-research-skills` | `5/5` |
| `systematic-review` | 运行从检索到报告编译的完整系统化综述工作区 | `agent-research-skills + AI-research-SKILLs` | `5/5` |
| `related-work-writing` | 按 bucket-aware 规则生成单篇论文的 Related Work | `agent-research-skills + AI-research-SKILLs` | `4/5` |
| `survey-generation` | 从 canonical corpus 规划并生成完整 survey manuscript | `agent-research-skills + AI-research-SKILLs` | `4/5` |

### 权威性与排序

| Skill | 功能 | 参考仓库 | 推荐星级 |
| --- | --- | --- | --- |
| `venue-authority-resolver` | 统一 venue metadata，并补 authority provenance | `repository-native` | `5/5` |
| `authority-ranking` | 计算仓库唯一 canonical 的 `final_score` 与 `selection_bucket` | `repository-native` | `5/5` |
| `ccf-ranking` | 为 CS / AI / security venue 提供可审计的 CCF 解析 | `repository-native` | `5/5` |
| `journal-metrics` | 用分层来源解析期刊分区和影响指标 | `repository-native` | `4/5` |
| `paper-quality-filter` | 在最终排序前补质量标签与 caution flags | `repository-native` | `4/5` |
| `field-ranking-profile` | 按学科切换 ranking 权重和阈值 | `repository-native` | `3/5` |

### 数据库与参考管理

| Skill | 功能 | 参考仓库 | 推荐星级 |
| --- | --- | --- | --- |
| `arxiv-database` | 执行 arXiv 定向检索与下载流程 | `claude-scientific-skills` | `4/5` |
| `biorxiv-database` | 执行 bioRxiv 定向预印本检索 | `claude-scientific-skills` | `3/5` |
| `openalex-database` | 查询 OpenAlex 的来源、作者和 citation metadata | `claude-scientific-skills` | `4/5` |
| `pubmed-database` | 执行 PubMed / MEDLINE 定向生物医学检索 | `claude-scientific-skills` | `4/5` |
| `citation-management` | 校验、修复并生成 BibTeX 与 cite key | `agent-research-skills + AI-research-SKILLs` | `4/5` |
| `pyzotero` | 将整理后的语料与 Zotero 库同步和导出 | `claude-scientific-skills` | `3/5` |

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

## 环境变量与 API Key

现在凡是依赖外部配置的 skill，都会在 `SKILL.md` frontmatter 的 `requires.env` 里声明。

建议统一使用这些环境变量：

| 变量 | 使用 Skill | 必需 | 用途 |
| --- | --- | --- | --- |
| `S2_API_KEY` | `literature-search`, `systematic-review`, `citation-management` | 否 | 提升 Semantic Scholar 限额 |
| `OPENALEX_EMAIL` | `literature-search`, `openalex-database` | 否 | OpenAlex polite pool 邮箱 |
| `CROSSREF_EMAIL` | `literature-search` | 否 | Crossref User-Agent 联系邮箱 |
| `NCBI_API_KEY` | `pubmed-database` | 否 | 提升 PubMed E-utilities 限额 |
| `NCBI_EMAIL` | `pubmed-database` | 否 | PubMed 自动化联系邮箱 |
| `ZOTERO_LIBRARY_ID` | `pyzotero` | 是 | Zotero 目标库 ID |
| `ZOTERO_API_KEY` | `pyzotero` | 是 | Zotero API Key |
| `ZOTERO_LIBRARY_TYPE` | `pyzotero` | 是 | Zotero 库类型 |

可以把 [`.env.example`](.env.example) 复制成你自己的本地环境文件，或者把这些键直接写进 ResearchClaw 的 env store。

## ResearchClaw 兼容性

这个仓库可以作为 [ResearchClaw](https://github.com/ymx10086/ResearchClaw) 的外部 skills 来源。

在 ResearchClaw 中使用时，应把本仓库的 [`skills/`](skills/) 目录视为权威可加载 skill 集合；根 README 和 skills catalog 负责说明路由规则、共享产物与边界。

和 ResearchClaw 对接时，关键契约是：

- 每个 skill 在 `SKILL.md` 里通过 `requires.env` 声明所需配置
- ResearchClaw 从 `/api/skills` 读取这些元数据
- 缺失的必需或推荐变量，应在启用 skill 前后明确提示出来

## 收录原则

- skill 必须直接服务于文献发现、authority-aware 排序、证据整合、引用治理或综述写作
- 如果某个分析模式不需要独立脚本或独立数据契约，应优先并入 `literature-review` 或 `systematic-review` 的 references，而不是继续保留单独顶层 skill
- 实验、实现、排版、演示类 skill 不应放在这里
- 优先保留可脚本化、可审计的工作流
