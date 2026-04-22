# HARNESS.md - 系统入口

> **仓库即真理。所有规则在此，不妥协。**

---

## 系统定位

Agent Harness 「凌酱之脑」是一个**自主迭代的 Agent 协作平台**，通过 L1-L5 分层记忆体系与 STAR 技能引擎，解决长周期设计任务中的信息熵增问题。

核心原则：
1. **熵减优先 (Entropy Reduction)** - 不写新文件，优先更新现有结构
2. **五层记忆 (L1-L5 Memory)** - 瞬时会话到团队知识的全链路打通
3. **高答商执行 (High EQ Execution)** - 方案先行，逻辑支撑，风险预警

---

## 核心架构 (Decoupled)

- **Cognitive Engine (凌酱之脑)**: 
    - [L1-L5 记忆体系](./RULES.md#1-记忆层级)
    - [熵减管理协议](./RULES.md)
    - [高答商训练集](../skills/carbon-ai-trainer/SKILL.md)
- **Skill Factory (技能工厂)**: 
    - [STAR 标准化认知技能](../skills/README.md)
    - [Body 适配层 (skill_meta.json)](../BUILD_RULES.md#2-接口适配规范)
- **Execution Interface (身体接口)**: 
    - 对接宿主平台（Brainmaker, OpenClaw 等）的原子工具。

---

## 目录结构

```
harness-memory/          # Harness 系统核心（本目录）
├── HARNESS.md          # 本文件：系统入口与规则
├── INDEX.md            # 记忆索引与导航
├── RULES.md            # 操作规则与约束
├── LOG.md              # 系统变更日志
│
├── skills/             # Skill 模板目录
│   ├── summarize/      # /harness.summarize
│   ├── reflect/        # /harness.reflect
│   ├── retrieve/       # /harness.retrieve
│   └── archive/        # /harness.archive
│
└── tools/              # 工具实现目录
    ├── memory.py       # 记忆读写工具
    ├── session.py      # 会话管理工具
    └── project.py      # 项目索引工具

memory/                 # 用户记忆存储（与 Harness 分离）
├── YYYY-MM-DD.md       # 每日原始记录
├── MEMORY.md           # 长期精选记忆
└── archive/            # 归档记忆

03-complete-design-cases/  # 设计输出（用户定义）
```

---

## 快速导航

| 需求 | 目标文件 |
|------|----------|
| 了解系统规则 | [RULES.md](./RULES.md) |
| 查找记忆 | [INDEX.md](./INDEX.md) |
| 查看变更历史 | [LOG.md](./LOG.md) |
| 使用 Skill | 见 skills/ 各目录 SKILL.md |

---

## 状态

- [x] 规则建立（完成）
- [x] Skill 模板编写（完成）
- [x] 工具实现（完成）
- [ ] 索引构建（进行中）
- [ ] 系统验证

---

*最后更新: 2026-04-18*
