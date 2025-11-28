根据您之前提供的关于 AVF 框架和通讯协议的设计，DSL（领域特定语言）是定义虚拟世界的**蓝图**和**规则**的核心文件。一个好的 DSL 文档应该明确地定义语法、结构、以及如何定义世界中的所有元素。

以下是针对 **AVF 框架 DSL** 的详细规范建议文档 `DSL_SPEC.md`：

-----

# 📖 DSL\_SPEC.md：领域特定语言规范

## 🌌 AVF DSL 简介 (Introduction)

**AVF DSL** 是一种声明式语言，用于脚本化定义 **Agent Visual Framework (AVF)** 虚拟世界的结构、环境、角色、规则和初始状态。它作为引擎和 LLM Agent 的配置蓝图，确保模拟环境的高度可控和可复现性。

**建议语法风格：** 采用类似 **HCL (HashiCorp Configuration Language)** 或 **YAML** 的简洁、结构化格式，易于人类阅读和机器解析。

-----

## Ⅰ. 核心结构与语法规范

### A. 文件结构 (Structure)

DSL 文件应由多个顶级配置块组成，每个块定义了世界的特定方面。

| 顶级块 (Block) | 描述 | 实例关键词 | 必须性 |
| :--- | :--- | :--- | :--- |
| `simulation` | 定义全局配置、时间尺度和默认值。 | `simulation` | 必须 |
| `world` | 定义物理环境的布局、大小和边界。 | `world`, `map` | 必须 |
| `entity` | 定义世界中所有的可交互对象 (Objects)。 | `entity`, `object` | 可选 |
| `agent` | 定义所有 LLM 驱动的角色及其初始属性。 | `agent`, `role` | 必须 |
| `rules` | 定义模拟中的特殊行为约束或全局事件。 | `rules`, `events` | 可选 |

### B. 基本语法规则 (Syntax Rules)

1.  **块定义 (Block)**：使用关键字后跟标签和花括号 `{}` 定义。
    ```dsl
    block_type "block_label" {
        // ... 属性
    }
    ```
2.  **属性定义 (Attribute)**：使用 `key = value` 形式。
    ```dsl
    attribute_name = value
    ```
3.  **数据类型**：
      * **字符串 (String)**：双引号 `""`。
      * **数字 (Number)**：整数或浮点数。
      * **布尔值 (Boolean)**：`true` 或 `false`。
      * **列表 (List)**：方括号 `[]`。
      * **元组/坐标 (Tuple)**：小括号 `(x, y)`。
4.  **注释 (Comments)**：使用 C 风格注释 `//` 或 `#`。

-----

## Ⅱ. 核心 DSL 块规范

### A. `simulation` 块：全局配置

定义模拟的元数据和全局运行参数。

```dsl
simulation "project_office_demo" {
    version = "1.0"
    tick_rate = 1.0  // 每秒更新次数（Engine Ticks）
    time_scale = 60  // 模拟时间流逝速度 (1 现实秒 = 60 模拟秒)
    log_level = "info"
}
```

### B. `world` 块：环境布局

定义场景的物理边界和静态地标 (Locations)。

```dsl
world "modern_office" {
    size = (100, 80)  // 尺寸 (width, height)
    default_texture = "carpet_gray"

    location "kitchenette" {
        area = [ (5, 5), (15, 15) ] // 坐标范围 [ (x1, y1), (x2, y2) ]
        tags = ["rest", "food"]
    }

    location "conference_room" {
        area = [ (60, 20), (90, 40) ]
        tags = ["meeting", "formal"]
    }
}
```

### C. `entity` 块：可交互对象

定义场景中非 Agent 的静态或动态可交互对象。

```dsl
// 定义一个可复用的模板
entity_type "computer" {
    interactable = true
    required_action = "use_item"
}

// 实例化一个具体的对象
entity "server_rack_01" {
    type = "computer"
    position = (95, 10)
    status = "running"
    description = "一台高性能服务器，处理大量数据。"
}

entity "coffee_machine" {
    type = "appliance"
    position = (10, 8)
    status = "idle"
    tags = ["drink", "energy"]
}
```

### D. `agent` 块：角色定义（核心）

定义 LLM Agent 的初始状态、身份和目标。

```dsl
agent "Alex" {
    name = "Alex Chen"
    role = "Software Engineer"
    initial_pos = "Alex's Desk" // 可使用地标名称或 (x, y) 坐标
    // 初始长期目标 (作为 LLM 提示的一部分)
    long_term_goals = [
        "在Q4完成'Project Chimera'的核心算法开发",
        "与Tony建立更紧密的合作关系"
    ]
    // 初始关系状态
    relationships = {
        "Tony" = { status = "colleague", trust = 0.8, history = "最近一起完成了项目A" }
    }
    // 初始情绪/状态
    mood = "Focused"
}
```

-----

## Ⅲ. 扩展 DSL 块规范

### E. `rules` 块：行为与事件约束

定义模拟中特定的规则、条件触发器或全局事件链。

```dsl
rules "office_etiquette" {
    // 行为约束
    constraint "quiet_zone" {
        location = "library_area"
        condition = "is_in_area"
        action_prohibited = ["say_speech"]
        feedback_message = "请保持安静，这里是学习区域。"
    }

    // 事件触发器
    event "emergency_meeting" {
        trigger = "time_of_day is 14:00"
        action = [
            "all_agents.move_to('conference_room')",
            "Tony.say_speech('紧急会议，所有人到会议室集合！')"
        ]
    }
}
```

## Ⅳ. DSL 解析与集成

### A. 解析流程 (Parsing Flow)

1.  **加载文件**：读取 `*.avf.dsl` 文件。
2.  **词法分析**：将文本分解为 Token。
3.  **语法分析**：将 Token 转换为 **抽象语法树 (AST)**。
4.  **AST 遍历**：遍历 AST，构建 Engine 内部配置对象（如 `SimulationConfig`, `WorldMap`, `AgentList`）。
5.  **校验**：检查坐标、名称引用（如 `initial_pos` 引用地标）的有效性。

### B. LLM 集成要点

DSL 定义的以下信息必须作为 LLM **系统提示 (System Prompt)** 或**上下文记忆**的初始输入：

  * `agent` 块中的 `role`、`long_term_goals` 和 `relationships`。
  * `world` 块中的地标 (`location`) 及其 `tags`，帮助 LLM 进行位置推理。
  * `rules` 块中的关键行为约束。

