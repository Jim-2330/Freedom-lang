#pragma once

// Freedon Lang C++ 核心接口草稿。
// 目前只是占位，主要目的是为未来实现预留清晰的层次。

namespace freedon {

// 未来可以在这里定义：
// - AST 数据结构
// - IR 层（IR0 / IR1 / IR2）的 C++ 类型
// - 解析 / 编译 / 执行接口

struct Version {
    int major{0};
    int minor{1};
    int patch{0};
};

Version version();

}  // namespace freedon

