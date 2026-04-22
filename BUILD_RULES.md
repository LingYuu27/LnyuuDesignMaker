# BUILD_RULES.md - 构建规则文档 (Brain-Body Architecture)

> **将“凌酱之脑”装入任何“Agent之躯”。**

本规范定义了如何将 DesignMakerProject 的核心认知层（大脑）与底层执行平台（身体）解耦，以实现跨平台（OpenClaw, Brainmaker Cowork, etc.）的无缝移植。

---

## 1. 大脑与身体的定义

### 1.1 凌酱之脑 (The Brain) - 核心资产
- **五层记忆系统 (L1-L5)**: 存储在 `memory/` 和 `harness-memory/` 中的结构化知识。
- **认知 Skill**: 包含评审框架、拆环规范、高答商等不依赖特定工具的逻辑。
- **熵减协议**: [RULES.md](file:///c:/Users/Lnyuu/Documents/trae_projects/DesignMakerProject/harness-memory/RULES.md) 中定义的信息管理纪律。

### 1.2 执行之躯 (The Body) - 平台能力
- **底层工具 (Tools)**: 文件读写、浏览器操控、Office 自动化、Shell 执行。
- **环境 (Env)**: Sandbox、Python 运行时、API 权限。
- **通信 (Channel)**: Discord, WhatsApp, 桌面客户端 UI。

---

## 2. 接口适配规范 (Interface Standards)

为了实现解耦，大脑不应直接依赖平台私有工具名。

### 2.1 Skill 适配层 (`skill_meta.json`)
每个 Skill 必须包含一个适配元数据文件，用于在不同平台注册：
```json
{
  "id": "",
  "name": "Skill名称",
  "category": "planning",
  "description": "大脑认知逻辑描述",
  "version": "1.0.0",
  "dependencies": {
    "body_capabilities": ["read_file", "write_file", "search"]
  }
}
```

### 2.2 认知 Skill 编写准则
- **逻辑抽象**: 核心逻辑写在 `SKILL.md` 的描述中，而非硬编码工具调用。
- **工具调用映射**: 在 `Action` 部分，使用通用动词（如“检索”、“写入”），并指明所需能力（Capability）。
- **环境隔离**: Python 工具应放在 `tools/` 目录下，并确保不依赖特定平台的全局变量。

---

## 3. 移植与构建步骤

### Step 1: 提取大脑
1. 复制 `memory/` 目录。
2. 复制 `harness-memory/` 目录。
3. 复制 `skills/` 和 `gao-da-shang/` 中的认知 Skill。

### Step 2: 组装身体 (以 Brainmaker 为例)
1. 在宿主平台的 `.agents/skills/` 目录下创建对应的 Skill 文件夹。
2. 为每个 Skill 补齐 `skill_meta.json`。
3. 将 `memory/` 放入宿主的工作区（Workspace）。

### Step 3: 注入真理
1. 将 [AGENTS.md](file:///c:/Users/Lnyuu/Documents/trae_projects/DesignMakerProject/AGENTS.md) 的核心协议更新到宿主平台的 System Prompt。
2. 配置宿主平台的 `MEMORY.md` 以加载大脑的长期记忆。

---

## 4. 维护与自迭代 (Reflective Loop)

1. **持续熵减**: 每次会话结束必须触发 `harness.summarize`，确保信息不淤积。
2. **反思优化**: 每周检查 `LOG.md`，手动或自动调整 [RULES.md](file:///c:/Users/Lnyuu/Documents/trae_projects/DesignMakerProject/harness-memory/RULES.md)。
3. **身体升级**: 当宿主平台提供更强的能力（如 Excel 自动化）时，仅更新 `skill_meta.json` 的 `body_capabilities` 声明，无需重写大脑逻辑。

---

*版本: 1.0.0*
*状态: 正式发布*
