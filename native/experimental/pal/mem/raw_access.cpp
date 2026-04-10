#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <cstdint>
#include <iostream>

// Freedon 全域指针结构的底层实现
struct FreedonRawPointer {
    uintptr_t physical_addr;
};

class PhysicalMemoryGate {
public:
    // 上帝函数：直接读取物理地址上的原始字节
    static uint8_t peek_byte(uintptr_t addr) {
        int fd = open("/dev/mem", O_RDWR | O_SYNC);
        if (fd < 0) return 0; // 权限不足时的失败，未来由 Freedon 内核模块解决

        // 计算页对齐
        off_t page_base = (addr & ~(getpagesize() - 1));
        off_t page_offset = addr - page_base;

        // 强行映射物理内存到用户空间
        void* mapped = mmap(NULL, getpagesize(), PROT_READ | PROT_WRITE, 
                            MAP_SHARED, fd, page_base);
        
        uint8_t value = *(static_cast<uint8_t*>(mapped) + page_offset);

        munmap(mapped, getpagesize());
        close(fd);
        return value;
    }

    // 上帝函数：直接改写物理内存的 0 和 1
    static void poke_byte(uintptr_t addr, uint8_t value) {
        // ... 实现逻辑与 peek 类似，但进行写操作 ...
    }
};
