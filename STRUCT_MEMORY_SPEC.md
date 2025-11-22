# Struct Memory Layout - Technical Specification

**Program**: struct_memory_demo.c  
**Version**: 1.0  
**Date**: November 16, 2025  
**Language**: C (C99 standard)  
**Platform**: macOS/Linux/Unix

---

## 1. OVERVIEW

An educational demonstration program that provides comprehensive understanding of C struct memory layout, padding, alignment, and optimization techniques. This program is designed to help programmers understand low-level memory management and structure optimization.

### 1.1 Purpose

- **Educational Tool**: Teach struct memory layout fundamentals
- **Performance Optimization**: Demonstrate impact of member ordering
- **Platform Understanding**: Show compiler alignment behavior
- **Practical Applications**: Real-world examples (network packets, hardware registers)

### 1.2 Key Concepts Covered

1. Basic struct declaration and initialization
2. Memory padding and alignment requirements
3. Struct layout optimization
4. Packed structures (`__attribute__((packed))`)
5. Nested structures
6. Bit fields for compact storage
7. Unions vs structs (memory sharing vs separation)
8. sizeof() operator behavior
9. Practical examples (IPv4 packet headers)
10. Best practices and pitfalls

---

## 2. TECHNICAL ARCHITECTURE

### 2.1 Program Structure

```
struct_memory_demo.c
├── Section 1: Basic Struct Declaration
├── Section 2: Memory Padding and Alignment
├── Section 3: Optimized Struct Layout
├── Section 4: Packed Structures
├── Section 5: Nested Structures
├── Section 6: Bit Fields
├── Section 7: Unions vs Structs
├── Section 8: sizeof() Operator
├── Section 9: Practical Example (Network Packet)
└── Section 10: Key Takeaways
```

### 2.2 Module Components

**Demonstration Functions:**
- `demo_basic_struct()` - Basic struct usage
- `demo_padding()` - Alignment and padding
- `demo_optimization()` - Size optimization
- `demo_packing()` - Packed struct comparison
- `demo_nested_structs()` - Nested structures
- `demo_bit_fields()` - Bit-level packing
- `demo_union_vs_struct()` - Memory model comparison
- `demo_sizeof()` - Size calculations
- `demo_practical_packet()` - IPv4 packet header
- `demo_key_takeaways()` - Summary

**Data Structures:**
- 10+ example structs
- 2 unions
- 1 practical packet header
- Nested structure examples

---

## 3. DATA STRUCTURES

### 3.1 Basic Struct

```c
struct BasicStruct {
    int id;        // 4 bytes
    char grade;    // 1 byte
    double score;  // 8 bytes
};
// Size: 16 bytes (with padding)
// Without padding: 13 bytes
// Padding: 3 bytes
```

**Memory Layout:**
```
Offset  Field      Size    Padding
0       id         4       0
4       grade      1       3
8       score      8       0
Total: 16 bytes
```

### 3.2 Padding Demonstration

```c
struct PaddingDemo {
    char a;      // 1 byte
    int b;       // 4 bytes (requires 4-byte alignment)
    char c;      // 1 byte
    double d;    // 8 bytes (requires 8-byte alignment)
};
// Size: 24 bytes
// Without padding: 14 bytes
// Padding: 10 bytes (71% overhead!)
```

**Memory Layout:**
```
[a][PPP][bbbb][c][PPPPPPP][dddddddd]
 1   3    4     1    7        8      = 24 bytes

Offset  Field    Size    Padding
0       a        1       3
4       b        4       0
8       c        1       7
16      d        8       0
```

### 3.3 Optimized vs Unoptimized

**Unoptimized (Poor Ordering):**
```c
struct UnoptimizedStruct {
    char a;
    int b;
    char c;
    int d;
};
// Size: 16 bytes
```

**Optimized (Better Ordering):**
```c
struct OptimizedStruct {
    int b;
    int d;
    char a;
    char c;
};
// Size: 12 bytes
// Savings: 25% reduction
```

**Rule:** Group members by size, largest first

### 3.4 Packed Structures

```c
struct PackedStruct {
    char a;
    int b;
    char c;
} __attribute__((packed));
// Size: 6 bytes (no padding)
// Performance: Slower (unaligned access)
```

**Trade-off:**
- **Space**: 50% reduction (12 bytes → 6 bytes)
- **Speed**: Potential performance penalty on some architectures
- **Use Case**: Network protocols, file formats, embedded systems

### 3.5 Nested Structures

```c
struct Address {
    char street[50];
    char city[30];
    int zipcode;
};
// Size: 84 bytes

struct Person {
    char name[50];
    int age;
    struct Address addr;
};
// Size: 140 bytes

Offsets:
- name: 0
- age: 52
- addr: 56 (entire Address struct)
```

### 3.6 Bit Fields

```c
struct BitFields {
    unsigned int flag1 : 1;     // 1 bit
    unsigned int flag2 : 1;     // 1 bit
    unsigned int value : 6;     // 6 bits
    unsigned int type : 3;      // 3 bits
    unsigned int reserved : 21; // 21 bits
};
// Total: 32 bits = 4 bytes
```

**Use Cases:**
- Hardware register mapping
- Flag storage (compact boolean sets)
- Protocol headers
- Embedded systems with limited memory

**Limitations:**
- Cannot take address of bit field
- Platform-dependent bit ordering
- May be slower than full bytes

### 3.7 Unions

```c
union DataUnion {
    int i;         // 4 bytes
    float f;       // 4 bytes
    char str[20];  // 20 bytes
};
// Size: 20 bytes (largest member)
// All members share the same memory!
```

**vs Struct:**
```c
struct DataStruct {
    int i;         // 4 bytes
    float f;       // 4 bytes
    char str[20];  // 20 bytes
};
// Size: 28 bytes (separate storage)
```

**Key Difference:**
- Union: Only one member valid at a time
- Struct: All members independently accessible

### 3.8 Practical Example - IPv4 Packet Header

```c
struct PacketHeader {
    uint8_t version : 4;
    uint8_t header_len : 4;
    uint8_t type_of_service;
    uint16_t total_length;
    uint16_t identification;
    uint16_t flags_fragment;
    uint8_t time_to_live;
    uint8_t protocol;
    uint16_t checksum;
    uint32_t source_ip;
    uint32_t dest_ip;
} __attribute__((packed));
// Size: 20 bytes (standard IPv4 header)
```

**Real-World Application:**
- Network packet parsing
- Wire protocol implementation
- Binary file format reading/writing

---

## 4. ALIGNMENT RULES

### 4.1 Fundamental Alignment Requirements

**On x86-64 (macOS/Linux):**

| Type          | Size    | Alignment |
|---------------|---------|-----------|
| char          | 1 byte  | 1 byte    |
| short         | 2 bytes | 2 bytes   |
| int           | 4 bytes | 4 bytes   |
| long          | 8 bytes | 8 bytes   |
| long long     | 8 bytes | 8 bytes   |
| float         | 4 bytes | 4 bytes   |
| double        | 8 bytes | 8 bytes   |
| pointer       | 8 bytes | 8 bytes   |

### 4.2 Struct Alignment Rules

1. **Member Alignment**: Each member aligned to its natural boundary
2. **Struct Alignment**: Struct aligned to largest member alignment
3. **Padding**: Added to satisfy alignment requirements
4. **Tail Padding**: Added at end to make struct size multiple of alignment

### 4.3 Padding Calculation Example

```c
struct Example {
    char a;    // offset 0, size 1
    // 3 bytes padding (to align int)
    int b;     // offset 4, size 4
    char c;    // offset 8, size 1
    // 7 bytes padding (to align double)
    double d;  // offset 16, size 8
};
// Total: 24 bytes
```

**Calculation:**
1. `char a` at offset 0
2. Padding to 4-byte boundary (offset 4)
3. `int b` at offset 4
4. `char c` at offset 8
5. Padding to 8-byte boundary (offset 16)
6. `double d` at offset 16
7. Total size: 24 bytes (multiple of 8)

---

## 5. OPTIMIZATION TECHNIQUES

### 5.1 Reordering Members

**Before:**
```c
struct Unoptimized {
    char a;    // 1 byte + 3 padding
    int b;     // 4 bytes
    char c;    // 1 byte + 3 padding
    int d;     // 4 bytes
};
// Size: 16 bytes
```

**After:**
```c
struct Optimized {
    int b;     // 4 bytes
    int d;     // 4 bytes
    char a;    // 1 byte
    char c;    // 1 byte + 2 padding
};
// Size: 12 bytes (25% reduction)
```

**Strategy:** Group by size (largest → smallest)

### 5.2 Using Smaller Types

```c
// Before
struct Config {
    int enabled;      // 4 bytes (only need 0/1)
    int mode;         // 4 bytes (only need 0-3)
    int status;       // 4 bytes (only need 0-255)
};
// Size: 12 bytes

// After
struct Config {
    uint8_t enabled;  // 1 byte
    uint8_t mode;     // 1 byte
    uint8_t status;   // 1 byte
    // 1 byte padding
};
// Size: 4 bytes (67% reduction)
```

### 5.3 Packing for Space-Critical Applications

```c
struct Packed {
    char flag;
    int value;
    char code;
} __attribute__((packed));
// Size: 6 bytes (vs 12 bytes normal)
```

**Trade-offs:**
- ✅ Minimal memory usage
- ❌ Potential performance penalty
- ❌ Architecture-dependent behavior

### 5.4 Cache Line Alignment

```c
struct CacheAligned {
    int data[16];
} __attribute__((aligned(64)));
// Aligned to 64-byte cache line
```

**Benefits:**
- Prevents false sharing in multithreaded code
- Improves cache performance
- Critical for high-performance computing

---

## 6. COMPILER DIRECTIVES

### 6.1 GCC/Clang Attributes

**Packed:**
```c
struct Packed {
    char a;
    int b;
} __attribute__((packed));
```

**Aligned:**
```c
struct Aligned {
    char a;
} __attribute__((aligned(16)));
```

**Both:**
```c
struct Example {
    char a;
    int b;
} __attribute__((packed, aligned(8)));
```

### 6.2 Pragma Pack (MSVC Compatible)

```c
#pragma pack(push, 1)
struct TightlyPacked {
    char a;
    int b;
    char c;
};
#pragma pack(pop)
```

### 6.3 offsetof() Macro

```c
#include <stddef.h>

size_t offset = offsetof(struct MyStruct, member);
```

**Usage:**
- Calculate member positions
- Verify padding
- Binary format parsing

---

## 7. COMMON PATTERNS

### 7.1 Configuration Structures

```c
struct Config {
    uint32_t magic;        // File magic number
    uint16_t version;      // Format version
    uint16_t flags;        // Option flags
    uint64_t timestamp;    // Creation time
    char description[256]; // Text description
} __attribute__((packed));
```

### 7.2 Hardware Register Mapping

```c
struct GPIOControl {
    unsigned int pin0 : 1;
    unsigned int pin1 : 1;
    unsigned int pin2 : 1;
    unsigned int pin3 : 1;
    unsigned int pin4 : 1;
    unsigned int pin5 : 1;
    unsigned int pin6 : 1;
    unsigned int pin7 : 1;
    unsigned int reserved : 24;
} __attribute__((packed));
```

### 7.3 Variant Data (Tagged Union)

```c
enum DataType { INT, FLOAT, STRING };

struct Variant {
    enum DataType type;
    union {
        int i;
        float f;
        char *str;
    } data;
};
```

### 7.4 Flexible Array Member (C99)

```c
struct Buffer {
    size_t length;
    char data[];  // Flexible array member
};

// Allocate with variable size
struct Buffer *buf = malloc(sizeof(struct Buffer) + 100);
```

---

## 8. PLATFORM CONSIDERATIONS

### 8.1 Architecture Differences

**32-bit vs 64-bit:**
```c
struct PointerStruct {
    void *ptr;
    int value;
};
// 32-bit: 8 bytes (4 + 4)
// 64-bit: 16 bytes (8 + 4 + 4 padding)
```

### 8.2 Endianness

**Little Endian (x86, ARM):**
- Least significant byte at lowest address

**Big Endian (Network order, some ARM):**
- Most significant byte at lowest address

**Bit Fields:**
- Order may vary between compilers
- Use with caution for portable code

### 8.3 ABI (Application Binary Interface)

**System V AMD64 ABI (Linux/macOS x86-64):**
- Natural alignment for basic types
- Structs aligned to largest member
- No tail padding optimization across structs

**ARM AAPCS:**
- Similar but may differ for long long
- NEON types have special alignment

---

## 9. PERFORMANCE IMPLICATIONS

### 9.1 Alignment Performance

**Aligned Access:**
```c
struct Aligned {
    int a;  // 4-byte aligned
    int b;  // 4-byte aligned
};
// Fast: Single CPU instruction per access
```

**Unaligned Access:**
```c
struct Unaligned {
    char c;
    int a;  // Potentially unaligned if packed
} __attribute__((packed));
// Slow: May require multiple CPU instructions or trap
```

### 9.2 Cache Line Effects

**Cache Line Size:** 64 bytes (typical)

**False Sharing:**
```c
struct Shared {
    int thread1_data;  // Used by thread 1
    int thread2_data;  // Used by thread 2
};
// Both in same cache line → false sharing → poor performance
```

**Solution:**
```c
struct NoSharing {
    int thread1_data;
    char padding[60];
    int thread2_data;
} __attribute__((aligned(64)));
```

### 9.3 Memory Bandwidth

**Tight Packing:**
- Less memory traffic
- Better for bandwidth-limited scenarios
- May hurt if requires multiple accesses

**Natural Alignment:**
- More memory traffic
- Better for compute-limited scenarios
- Optimal CPU performance

---

## 10. USE CASES

### 10.1 Network Protocols

**Example: TCP Header**
```c
struct TCPHeader {
    uint16_t source_port;
    uint16_t dest_port;
    uint32_t seq_num;
    uint32_t ack_num;
    uint8_t data_offset : 4;
    uint8_t reserved : 4;
    uint8_t flags;
    uint16_t window;
    uint16_t checksum;
    uint16_t urgent_ptr;
} __attribute__((packed));
```

### 10.2 File Formats

**Example: BMP Header**
```c
struct BMPHeader {
    uint16_t type;
    uint32_t size;
    uint16_t reserved1;
    uint16_t reserved2;
    uint32_t offset;
} __attribute__((packed));
```

### 10.3 Embedded Systems

**Example: Sensor Data**
```c
struct SensorReading {
    uint16_t temperature : 12;  // 0-4095
    uint16_t humidity : 12;     // 0-4095
    uint8_t battery_level;      // 0-100
    uint8_t flags;
} __attribute__((packed));
```

### 10.4 Database Records

```c
struct PersonRecord {
    uint64_t id;
    char name[64];
    char email[128];
    uint32_t age;
    uint32_t salary;
} __attribute__((aligned(256)));  // Align to page boundary
```

---

## 11. DEBUGGING AND TOOLS

### 11.1 Inspecting Struct Layout

**Using offsetof():**
```c
printf("Offset of member: %zu\n", offsetof(struct MyStruct, member));
```

**Using GDB:**
```
(gdb) ptype struct MyStruct
```

**Using Compiler:**
```bash
gcc -fdump-tree-original struct.c  # GCC
clang -Xclang -fdump-record-layouts struct.c  # Clang
```

### 11.2 Detecting Padding

**Manual Calculation:**
```c
size_t total_size = sizeof(struct MyStruct);
size_t member_sum = sizeof(type1) + sizeof(type2) + ...;
size_t padding = total_size - member_sum;
```

**Static Analysis:**
```c
_Static_assert(sizeof(struct MyStruct) == expected_size,
               "Unexpected struct size");
```

### 11.3 Pahole Tool

```bash
pahole struct_demo
```

Output shows:
- Member offsets
- Padding bytes
- Holes in structure
- Optimization suggestions

---

## 12. BEST PRACTICES

### 12.1 Design Guidelines

1. **Order by Size**: Largest members first
2. **Group Related Fields**: Logical cohesion
3. **Consider Alignment**: Understand platform requirements
4. **Document Packing**: Comment why packed if used
5. **Use sizeof()**: Never hardcode sizes
6. **Static Assertions**: Verify size assumptions

### 12.2 Do's

✅ Use natural alignment by default  
✅ Group members by size for optimization  
✅ Use offsetof() for member positions  
✅ Add static assertions for critical sizes  
✅ Document alignment requirements  
✅ Use bit fields for flags and hardware registers  

### 12.3 Don'ts

❌ Don't pack unless necessary  
❌ Don't assume struct sizes across platforms  
❌ Don't take addresses of bit fields  
❌ Don't rely on bit field ordering  
❌ Don't ignore alignment warnings  
❌ Don't mix pointer sizes in portable code  

### 12.4 Code Review Checklist

- [ ] Struct members ordered by size?
- [ ] Padding acceptable or optimized?
- [ ] Packing justified with comment?
- [ ] Size verified with static assertion?
- [ ] Platform assumptions documented?
- [ ] Endianness handled if needed?
- [ ] Cache line alignment considered?

---

## 13. COMPILATION AND EXECUTION

### 13.1 Build Commands

```bash
# Standard build
gcc -Wall -Wextra -g -O2 struct_memory_demo.c -o bin/struct_memory_demo

# With Makefile
make run-struct-demo

# Show struct layouts (Clang)
clang -Xclang -fdump-record-layouts struct_memory_demo.c

# Check padding with pahole
gcc -g struct_memory_demo.c -o struct_demo
pahole struct_demo
```

### 13.2 Compiler Flags

- `-Wall -Wextra`: Enable warnings
- `-g`: Debug symbols
- `-O2`: Optimization level
- `-fpack-struct`: Force packing (not recommended)
- `-Wpadded`: Warn about padding

### 13.3 Output

Program displays 10 sections with formatted tables showing:
- Struct sizes and offsets
- Memory layout visualizations
- Padding calculations
- Comparison tables
- Practical examples

---

## 14. EDUCATIONAL VALUE

### 14.1 Learning Objectives

After running this demo, programmers should understand:

1. ✅ Why structs are larger than sum of members
2. ✅ How alignment affects performance
3. ✅ When to use packed structs
4. ✅ Difference between unions and structs
5. ✅ How to optimize struct layout
6. ✅ Bit field use cases and limitations
7. ✅ Platform-dependent behavior
8. ✅ Real-world applications

### 14.2 Target Audience

- **Beginners**: Understand basic struct concepts
- **Intermediate**: Learn optimization techniques
- **Advanced**: Master platform-specific details
- **Embedded Developers**: Hardware register mapping
- **Network Programmers**: Protocol implementation
- **Performance Engineers**: Cache optimization

### 14.3 Follow-up Topics

- Memory allocation (malloc/free)
- Cache-friendly data structures
- SIMD alignment requirements
- Lock-free programming
- Memory-mapped I/O

---

## 15. REFERENCES

### 15.1 Standards

- **C99**: ISO/IEC 9899:1999
- **C11**: ISO/IEC 9899:2011
- **POSIX**: IEEE Std 1003.1

### 15.2 Documentation

- GCC Manual: Structure Layout
- Clang Documentation: Data Structures
- System V ABI: AMD64 Architecture Processor Supplement

### 15.3 Related Programs

- `array_pointer_demo.c`: Array and pointer arithmetic
- `linked_list.c`: Dynamic data structures
- Performance benchmarking tools

---

**Document Version**: 1.0  
**Last Updated**: November 16, 2025  
**Author**: C Programming Educational Series  
**License**: MIT
