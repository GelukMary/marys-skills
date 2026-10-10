# marys-skills

> 我在秋招和产品实习里在用的 Agent Skills，跑顺了才放出来。

[![License: MIT](https://img.shields.io/badge/License-MIT-111111?style=flat-square)](./LICENSE)
![Skills](https://img.shields.io/badge/Skills-6-111111?style=flat-square)
![Standard](https://img.shields.io/badge/Agent_Skills-Standard-111111?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude_Code-compatible-111111?style=flat-square)
![Codex](https://img.shields.io/badge/Codex-compatible-111111?style=flat-square)

每个 Skill 都是一个包含 `SKILL.md` 的目录，遵循开放标准；Claude Code、Codex 等兼容 Agent 会根据 `description` 字段自动加载触发。这里的东西都在真实任务里跑过：简历改到能扛住面试追问、AB 实验复盘到口径对得上、竞品拆解到每条结论有来源，才沉淀成 Skill。

## 目录

|  | Skill | 一句话 | 依赖 |
|---|---|---|---|
| 🎤 | [case-coach](#case-coach面试-case-陪练) | 产品面试 case 陪练 | 无 |
| 📊 | [ab-experiment-review](#ab-experiment-reviewab-实验复盘) | AB 实验复盘 | Python 3 |
| 📄 | [resume-audit](#resume-audit简历改写) | 简历改写 | 无 |
| 📝 | [prd-writer](#prd-writerprd-prd撰写) | PRD 撰写 | 无 |
| 🔍 | [market-research](#market-research市场调研) | 市场调研 | 无 |
| 🧭 | [pm-competitor-teardown](#pm-competitor-teardown竞品分析) | 竞品分析| Python 3 |

两条链路：

```text
产品线：market-research → pm-competitor-teardown → prd-writer → ab-experiment-review
求职线：resume-audit → case-coach
```

## 安装方式

Skill 本质是一个目录，放进 Agent 的 skills 路径即可，无需安装命令。

也可以直接跟你的 Agent 说：

```text
帮我安装这个 skill：https://github.com/GelukMary/marys-skills/tree/main/case-coach
```

手动安装（软链方式，仓库 `git pull` 即完成升级）：

```bash
git clone https://github.com/GelukMary/marys-skills.git ~/marys-skills

# Claude Code
mkdir -p ~/.claude/skills
for s in case-coach ab-experiment-review resume-audit prd-writer market-research pm-competitor-teardown; do
  ln -s ~/marys-skills/$s ~/.claude/skills/$s
done

# Codex 同理，路径换成 ~/.codex/skills
```

Windows（管理员 CMD），或直接复制文件夹：

```bat
mklink /D "%USERPROFILE%\.codex\skills\case-coach" "%USERPROFILE%\marys-skills\case-coach"
```

装完新开会话即生效。你的 Agent 不支持 Skill 也没关系：把对应目录的 `SKILL.md` 全文当成项目规则文件，或直接贴进对话。

## Skills

### case-coach（面试 case 陪练）

把商业化/产品面试 case 练成结构化表达：先给框架让你答一轮，再按六维评分，指出关键漏洞和面试官会追问的点。练题模式先要口径、再给反馈。

```text
帮我练一道商业化 case
用 $case-coach 复盘我刚才的回答
收入下滑 30% 怎么分析
```

产出：评分 + 漏洞 + 追问清单。依赖：无。

### ab-experiment-review（AB 实验复盘）

复盘 AB 实验：检查口径（相对还是百分点、基线、分母）、样本量、护栏指标与外部事件，判断结论能不能全量。附带两比例显著性脚本 `scripts/significance_check.py`。

```text
复盘这次定价实验
这个实验能不能全量
埋点支付成功和 ODS 订单对不上
```

产出：复盘卡片 + 可信度评分 + 补实验建议。依赖：Python 3。

### resume-audit（简历审校）

对着目标 JD 审简历：检查量化口径、个人贡献、项目角色一致性，给出改写示例和面试追问清单。改 docx 后要重新渲染验证版式。

```text
帮我改简历
对着这个 JD 审一下我的简历
这条 bullet 怎么写
```

产出：审计清单 + 改写示例 + 追问清单。依赖：无。

### prd-writer（PRD 撰写与评审）

写与评审可落地 PRD：数值三件套（默认值 / 是否远程配置 / 生效层级）、指标与埋点对账、待定项闭环、评审回填。禁用"适当增加"这类模糊词。

```text
帮我写这个功能的 PRD
评审这份 PRD
埋点怎么对账
```

产出：PRD + 埋点对账表 + 待定项清单。依赖：无。

### market-research（市场与用户调研）

先立假设再用证据打靶：每条数据标注来源、时间、口径，区分实测 / 统计 / 推断；n=1 就写 n=1。交付前主动写"什么证据会推翻结论"。

```text
做一份出海市场调研
帮我写访谈提纲
把这个竞品研究整理成结论先行的报告
```

产出：结论先行的报告 + 证据链 + 不确定性说明。依赖：无。

### pm-competitor-teardown（竞品拆解）

面向 C 端订阅 / AI 产品的竞品拆解 SOP，默认 URL 驱动：用户给网址或粘贴材料，一次性批量抓取，读不到就标"未获取"。商业化拆解覆盖付费墙、套餐与默认项、地区定价、单位经济代理；AI 功能按效果 / 成本 / 性能 / 付费意愿四维评分；缝隙用评分卡，低于阈值不写进结论。

```text
拆解这几个竞品
竞品定价怎么对比
AI 功能值不值得做
```

产出：对标矩阵 + 缝隙评分卡 + 验证计划 + 来源账本。依赖：Python 3 + 自备来源 URL。

```bash
python scripts/fetch_sources.py --urls urls.txt --out sources
```

## 前置要求

| Skill | 依赖 |
|---|---|
| case-coach | 无（纯提示词） |
| resume-audit | 无（纯提示词） |
| prd-writer | 无（纯提示词） |
| market-research | 无（纯提示词） |
| ab-experiment-review | Python 3（仅标准库） |
| pm-competitor-teardown | Python 3（仅标准库）+ 自备来源 URL |
