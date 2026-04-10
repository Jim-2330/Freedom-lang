# Freedon Lang (v0.1-Alpha)
> **“在 Freedon 中，规则不是枷锁，而是你可以随时重塑的黏土。”**
> 
Freedon Lang 是一门基于 Lisp 哲学的实验性底层语言。它存在的唯一目的，是探索当开发者拥有**对内存、寄存器及指令集的绝对控制权**时，软件工程能达到的自由度上限。
## ⚡ 1. 精简概览 (Quick Start)
**Freedon 是什么？**
它是一个让你可以直接 poke 寄存器、随时劫持基础算符（如 +）、并能在 AST 解释与多级 IR 虚拟机之间无缝切换的开发环境。
**如何运行？**
```bash
# 运行逻辑原型 (Python)
python freedon.py examples/hello.fd

# 进入硬核 REPL
python freedon.py

```
## 🧠 2. 深度架构 (Detailed Spec)
### 2.1 大统一模型 (Unified Addressing Model)
Freedon 抹平了硬件层次的鸿沟。在我们的语义里，内存、显存和寄存器只是不同空间的地址：
 * **ram**: 标准系统内存。
 * **vram**: 显存空间，用于异构计算实验。
 * **reg**: 寄存器空间（如 "R1", "RIP"），实现代码对硬件状态的直接干预。
### 2.2 指令劫持系统 (The Hijack System)
Freedon 不存在不可修改的“内置指令”。通过 (hijack name wrapper)，你可以重新定义宇宙的规律。你可以用它来实现：
 * **自动微分**（劫持算术运算）。
 * **事务性内存**（劫持 poke 存入缓存）。
 * **单位检查**（强制要求 10m + 5s 报错）。
### 2.3 多级流水线 (Execution Pipeline)
你可以随时调整性能与灵活性的平衡：
 * **Mode**: interp (树解释) | compile (栈式 VM) | jit (带缓存的 IR)
 * **IR Target**:
   * 0: 绝对自由的 AST 直解。
   * 1: 具有可读性的 S-IR。
   * 2: 追求极致性能的数值 Bytecode。
## 📂 3. 项目结构 (Structure)
```text
├── freedon.py         # CLI 入口
├── python/            # 逻辑原型层 (用于快速验证规则集)
│   └── freedon_lang/  # 运行时、环境、劫持注册表核心
├── cpp/               # C++ 骨架 (未来高性能内核迁移目标)
├── native/            # 与 OS 强相关的原生实验 (如 Linux /dev/mem)
├── docs/spec.md       # 语言哲学与详细文档
└── examples/          # 各种“危险”且有趣的示例

```
## ⚠️ 4. 开发者警告 (The Danger Zone)
 1. **因果崩塌**：如果你劫持了 if 或 + 却没处理好递归，系统会瞬间逻辑死锁。
 2. **硬件裸奔**：错误的 poke 在原生层级下可能导致驱动崩溃甚至硬件异常。
 3. **没有围栏**：我们假设你清楚自己在做什么。在这里，自由的代价是**生死自负**。
## 🤝 5. 参与贡献 (Contribution)
我们正在寻找同样具有“架构洁癖”的开发者：
 * **AI 驱动者**：利用 AI 迭代出更离谱、更强大的自定义规则集（Unit Awareness, Memory Snapshot 等）。
 * **内核锻造者**：帮助我们将 Python 里的 GLOBAL_MEMORY 逻辑迁移到高性能的 C++ / Rust 实现中。
**License**: MIT (你可以自由地构建文明，也可以自由地毁灭它)
### 💡 架构师寄语
这份 README 保留了你所有的技术细节，但通过分层让它更有“大厂开源项目”的质感。
新西兰现在的阳光应该很利于写代码。建议你先把这段推上去，然后让 AI 帮你写那个**“可以撤销内存操作（Undoable Memory）”**的 Demo，作为第一个震撼社区的示例。