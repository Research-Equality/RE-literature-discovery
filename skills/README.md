# Skills Catalog

这里是仓库内唯一维护的文献综述技能目录。

## Routing Rules

为了避免冲突和重复，仓库内 skill 按职责分层：

1. `literature-search` 负责默认的多源发现和初步筛选
2. `arxiv-database` / `biorxiv-database` / `openalex-database` / `pubmed-database` 只负责各自数据库的高级检索或分析
3. `arxiv-monitor` 负责持续预印本监控和 digest
4. `systematic-review` 负责完整的 6 阶段系统化调研
5. `literature-review` 与 `cross-paper-synthesis` 负责基于已有论文集做主题归纳和跨论文综合
6. `citation-graph` / `gap-detection` / `claim-tracker` / `consensus-mapping` / `contradiction-detection` / `evidence-grading` 负责语料分析与证据判断
7. `citation-management` / `pyzotero` 负责参考文献库与 BibTeX 治理
8. `related-work-writing` 只写单篇论文的 Related Work
9. `survey-generation` 只生成完整 survey manuscript

## Shared Artifacts

推荐所有可复用产物都落到这些共享位置：

- `outputs/<topic-slug>/search_results/<source>.jsonl`：原始检索结果
- `outputs/<topic-slug>/paper_db.jsonl`：统一后的论文语料主文件
- `outputs/<topic-slug>/research_log.md` / `findings.md`：长周期调研过程记录与运行中的综合结论
- `outputs/<topic-slug>/review/`：轻量综述产物
- `outputs/<topic-slug>/phase*/`：`systematic-review` 的阶段化产物
- `outputs/<topic-slug>/survey/`：完整 survey 稿件
- `references.bib`：当前写作任务的参考文献主文件

如果某个 source-specific skill 输出的是包装过的 JSON，而不是 JSONL，可先用：

```bash
python skills/literature-search/scripts/normalize_search_results.py --source arxiv-database --input raw.json --output normalized.jsonl
```

再并入 `paper_db.jsonl`。

## Workflow

推荐按这条主链使用：

1. `literature-search`
2. `literature-review`
3. `systematic-review`
4. `citation-management`
5. `related-work-writing`
6. `survey-generation`

## Discovery and Source Skills

这些技能为主链提供数据库检索、预印本发现和参考文献库集成能力：

1. `arxiv-database`
2. `biorxiv-database`
3. `openalex-database`
4. `pubmed-database`
5. `pyzotero`

## Monitoring and Corpus Analysis Skills

这些技能服务于持续跟踪、跨论文分析、共识判断和 gap 识别：

1. `arxiv-monitor`
2. `citation-graph`
3. `gap-detection`
4. `claim-tracker`
5. `consensus-mapping`
6. `contradiction-detection`
7. `cross-paper-synthesis`
8. `evidence-grading`

## Included Skills

### `literature-search`

用途：多源检索 Semantic Scholar、arXiv、OpenAlex、CrossRef，并统一输出结构化结果。

目录：[`skills/literature-search/`](literature-search/)

### `literature-review`

用途：通过多专家视角对话、主题归纳和证据整合，生成结构化文献综述。

目录：[`skills/literature-review/`](literature-review/)

### `systematic-review`

用途：执行 6 阶段系统化文献调研，产出 paper database、deep-dive notes、synthesis 和 final report。

目录：[`skills/systematic-review/`](systematic-review/)

### `citation-management`

用途：校验 `.tex` 与 `.bib` 一致性，收集缺失引用，生成或修复 BibTeX。

目录：[`skills/citation-management/`](citation-management/)

### `related-work-writing`

用途：按主题组织文献，对比现有方法并准确定位自身工作。

目录：[`skills/related-work-writing/`](related-work-writing/)

### `survey-generation`

用途：生成完整 survey paper，包括大纲、分节写作、引文校验和连贯性增强。

目录：[`skills/survey-generation/`](survey-generation/)

### `arxiv-database`

用途：搜索 arXiv 预印本，支持关键词、作者、分类、arXiv ID 与 PDF 下载。

目录：[`skills/arxiv-database/`](arxiv-database/)

### `arxiv-monitor`

用途：对指定主题、作者或类别做持续 arXiv 监控，输出 digest 和新增论文清单。

目录：[`skills/arxiv-monitor/`](arxiv-monitor/)

### `biorxiv-database`

用途：搜索 bioRxiv 生命科学预印本，支持按关键词、作者、日期与分类检索。

目录：[`skills/biorxiv-database/`](biorxiv-database/)

### `openalex-database`

用途：访问 OpenAlex 做学术检索、引用分析、研究趋势分析和文献计量研究。

目录：[`skills/openalex-database/`](openalex-database/)

### `pubmed-database`

用途：进行 PubMed 高级检索、MeSH 查询和 E-utilities 自动化。

目录：[`skills/pubmed-database/`](pubmed-database/)

### `pyzotero`

用途：通过 pyzotero 自动化管理 Zotero 文献库、条目、集合、附件和导出流程。

目录：[`skills/pyzotero/`](pyzotero/)

### `citation-graph`

用途：围绕已有论文集构建引用网络，识别基础论文、桥接论文和阅读缺口。

目录：[`skills/citation-graph/`](citation-graph/)

### `gap-detection`

用途：从已有语料中识别开放问题、方法盲点和潜在创新空间。

目录：[`skills/gap-detection/`](gap-detection/)

### `claim-tracker`

用途：跟踪关键科学 claim 的来源、支持证据、挑战证据和状态变化。

目录：[`skills/claim-tracker/`](claim-tracker/)

### `consensus-mapping`

用途：区分领域内哪些结论已形成共识，哪些仍然存在争议。

目录：[`skills/consensus-mapping/`](consensus-mapping/)

### `contradiction-detection`

用途：识别论文之间相互冲突的实验结论、解释或方法建议。

目录：[`skills/contradiction-detection/`](contradiction-detection/)

### `cross-paper-synthesis`

用途：生成跨论文对比表、时间线和主线归纳，服务于 review 与 survey 写作。

目录：[`skills/cross-paper-synthesis/`](cross-paper-synthesis/)

### `evidence-grading`

用途：按研究设计、复现状态、期刊会议层级和时效性评估证据强弱。

目录：[`skills/evidence-grading/`](evidence-grading/)

## Maintenance Rules

- 该目录下新增 skill 时，必须与文献发现、文献阅读、综述生成直接相关。
- 数据库型与参考管理型 skill 也允许收录，但必须直接服务于文献调研主链。
- 如果新来源中的 skill 与现有主链高度同责，优先合并其能力边界，而不是复制出第二个同类 skill。
- 来自通用 AI research 仓库的“总控型”或“通用论文写作型” skill，通常应拆解后并入 `systematic-review`、`citation-management`、`related-work-writing` 或 `survey-generation`，而不是整包引入。
- 如果一个 skill 主要服务于实验、代码开发、论文排版或演示汇报，不应放入这里。
- 优先把跨 skill 的绝对路径、私有目录和作者机器依赖清理为仓库内相对路径。
