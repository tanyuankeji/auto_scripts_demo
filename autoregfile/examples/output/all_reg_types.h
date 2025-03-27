/**
 * @file all_reg_types.h
 * @brief 自动生成的寄存器定义头文件
 * @note 生成时间: 2025-03-27 21:09:05
 * @version 2.0.0
 */

#ifndef ALL_REG_TYPES_H
#define ALL_REG_TYPES_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* 寄存器地址定义 */
#define ALL_REG_TYPES_READWRITE_REG_ADDR      0x0U  /**< ReadWrite类型寄存器 */
#define ALL_REG_TYPES_READONLY_REG_ADDR      0x0U  /**< ReadOnly类型寄存器 */
#define ALL_REG_TYPES_WRITEONLY_REG_ADDR      0x0U  /**< WriteOnly类型寄存器 */
#define ALL_REG_TYPES_WRITE1CLEAN_REG_ADDR      0x0U  /**< Write1Clean类型寄存器 */
#define ALL_REG_TYPES_WRITE1SET_REG_ADDR      0x0U  /**< Write1Set类型寄存器 */
#define ALL_REG_TYPES_WRITE0CLEAN_REG_ADDR      0x0U  /**< Write0Clean类型寄存器 */
#define ALL_REG_TYPES_WRITE0SET_REG_ADDR      0x0U  /**< Write0Set类型寄存器 */
#define ALL_REG_TYPES_WRITEONCE_REG_ADDR      0x0U  /**< WriteOnce类型寄存器 */
#define ALL_REG_TYPES_WRITEONLYONCE_REG_ADDR      0x0U  /**< WriteOnlyOnce类型寄存器 */
#define ALL_REG_TYPES_READCLEAN_REG_ADDR      0x0U  /**< ReadClean类型寄存器 */
#define ALL_REG_TYPES_READSET_REG_ADDR      0x0U  /**< ReadSet类型寄存器 */
#define ALL_REG_TYPES_WRITEREADCLEAN_REG_ADDR      0x0U  /**< WriteReadClean类型寄存器 */
#define ALL_REG_TYPES_WRITEREADSET_REG_ADDR      0x0U  /**< WriteReadSet类型寄存器 */
#define ALL_REG_TYPES_WRITE1PULSE_REG_ADDR      0x0U  /**< Write1Pulse类型寄存器 */
#define ALL_REG_TYPES_WRITE0PULSE_REG_ADDR      0x0U  /**< Write0Pulse类型寄存器 */

/* 寄存器位宽定义 */
#define ALL_REG_TYPES_DATA_WIDTH     32U
#define ALL_REG_TYPES_ADDR_WIDTH     10U

/* 寄存器位域定义 */
/* READWRITE_REG - VALUE */
#define ALL_REG_TYPES_READWRITE_REG_VALUE_POS      0U
#define ALL_REG_TYPES_READWRITE_REG_VALUE_MASK     (0xFFFFFFFFU << 0U)
/* READONLY_REG - VALUE */
#define ALL_REG_TYPES_READONLY_REG_VALUE_POS      0U
#define ALL_REG_TYPES_READONLY_REG_VALUE_MASK     (0xFFFFFFFFU << 0U)
/* WRITEONLY_REG - VALUE */
#define ALL_REG_TYPES_WRITEONLY_REG_VALUE_POS      0U
#define ALL_REG_TYPES_WRITEONLY_REG_VALUE_MASK     (0xFFFFFFFFU << 0U)
/* WRITE1CLEAN_REG - VALUE */
#define ALL_REG_TYPES_WRITE1CLEAN_REG_VALUE_POS      0U
#define ALL_REG_TYPES_WRITE1CLEAN_REG_VALUE_MASK     (0xFFFFFFFFU << 0U)
/* WRITE1CLEAN_REG - BIT0 */
#define ALL_REG_TYPES_WRITE1CLEAN_REG_BIT0_POS      0U
#define ALL_REG_TYPES_WRITE1CLEAN_REG_BIT0_MASK     (1U << 0U)
/* WRITE1CLEAN_REG - BITS */
#define ALL_REG_TYPES_WRITE1CLEAN_REG_BITS_POS      1U
#define ALL_REG_TYPES_WRITE1CLEAN_REG_BITS_MASK     (0xFU << 1U)
/* WRITE1SET_REG - VALUE */
#define ALL_REG_TYPES_WRITE1SET_REG_VALUE_POS      0U
#define ALL_REG_TYPES_WRITE1SET_REG_VALUE_MASK     (0xFFFFFFFFU << 0U)
/* WRITE1SET_REG - BIT0 */
#define ALL_REG_TYPES_WRITE1SET_REG_BIT0_POS      0U
#define ALL_REG_TYPES_WRITE1SET_REG_BIT0_MASK     (1U << 0U)
/* WRITE1SET_REG - BITS */
#define ALL_REG_TYPES_WRITE1SET_REG_BITS_POS      1U
#define ALL_REG_TYPES_WRITE1SET_REG_BITS_MASK     (0xFU << 1U)
/* WRITE0CLEAN_REG - VALUE */
#define ALL_REG_TYPES_WRITE0CLEAN_REG_VALUE_POS      0U
#define ALL_REG_TYPES_WRITE0CLEAN_REG_VALUE_MASK     (0xFFFFFFFFU << 0U)
/* WRITE0CLEAN_REG - BIT0 */
#define ALL_REG_TYPES_WRITE0CLEAN_REG_BIT0_POS      0U
#define ALL_REG_TYPES_WRITE0CLEAN_REG_BIT0_MASK     (1U << 0U)
/* WRITE0CLEAN_REG - BITS */
#define ALL_REG_TYPES_WRITE0CLEAN_REG_BITS_POS      1U
#define ALL_REG_TYPES_WRITE0CLEAN_REG_BITS_MASK     (0xFU << 1U)
/* WRITE0SET_REG - VALUE */
#define ALL_REG_TYPES_WRITE0SET_REG_VALUE_POS      0U
#define ALL_REG_TYPES_WRITE0SET_REG_VALUE_MASK     (0xFFFFFFFFU << 0U)
/* WRITE0SET_REG - BIT0 */
#define ALL_REG_TYPES_WRITE0SET_REG_BIT0_POS      0U
#define ALL_REG_TYPES_WRITE0SET_REG_BIT0_MASK     (1U << 0U)
/* WRITE0SET_REG - BITS */
#define ALL_REG_TYPES_WRITE0SET_REG_BITS_POS      1U
#define ALL_REG_TYPES_WRITE0SET_REG_BITS_MASK     (0xFU << 1U)
/* WRITEONCE_REG - VALUE */
#define ALL_REG_TYPES_WRITEONCE_REG_VALUE_POS      0U
#define ALL_REG_TYPES_WRITEONCE_REG_VALUE_MASK     (0xFFFFFFFFU << 0U)
/* WRITEONLYONCE_REG - VALUE */
#define ALL_REG_TYPES_WRITEONLYONCE_REG_VALUE_POS      0U
#define ALL_REG_TYPES_WRITEONLYONCE_REG_VALUE_MASK     (0xFFFFFFFFU << 0U)
/* READCLEAN_REG - VALUE */
#define ALL_REG_TYPES_READCLEAN_REG_VALUE_POS      0U
#define ALL_REG_TYPES_READCLEAN_REG_VALUE_MASK     (0xFFFFFFFFU << 0U)
/* READSET_REG - VALUE */
#define ALL_REG_TYPES_READSET_REG_VALUE_POS      0U
#define ALL_REG_TYPES_READSET_REG_VALUE_MASK     (0xFFFFFFFFU << 0U)
/* WRITEREADCLEAN_REG - VALUE */
#define ALL_REG_TYPES_WRITEREADCLEAN_REG_VALUE_POS      0U
#define ALL_REG_TYPES_WRITEREADCLEAN_REG_VALUE_MASK     (0xFFFFFFFFU << 0U)
/* WRITEREADSET_REG - VALUE */
#define ALL_REG_TYPES_WRITEREADSET_REG_VALUE_POS      0U
#define ALL_REG_TYPES_WRITEREADSET_REG_VALUE_MASK     (0xFFFFFFFFU << 0U)
/* WRITE1PULSE_REG - VALUE */
#define ALL_REG_TYPES_WRITE1PULSE_REG_VALUE_POS      0U
#define ALL_REG_TYPES_WRITE1PULSE_REG_VALUE_MASK     (0xFFFFFFFFU << 0U)
/* WRITE1PULSE_REG - BIT0 */
#define ALL_REG_TYPES_WRITE1PULSE_REG_BIT0_POS      0U
#define ALL_REG_TYPES_WRITE1PULSE_REG_BIT0_MASK     (1U << 0U)
/* WRITE1PULSE_REG - BITS */
#define ALL_REG_TYPES_WRITE1PULSE_REG_BITS_POS      1U
#define ALL_REG_TYPES_WRITE1PULSE_REG_BITS_MASK     (0xFU << 1U)
/* WRITE0PULSE_REG - VALUE */
#define ALL_REG_TYPES_WRITE0PULSE_REG_VALUE_POS      0U
#define ALL_REG_TYPES_WRITE0PULSE_REG_VALUE_MASK     (0xFFFFFFFFU << 0U)
/* WRITE0PULSE_REG - BIT0 */
#define ALL_REG_TYPES_WRITE0PULSE_REG_BIT0_POS      0U
#define ALL_REG_TYPES_WRITE0PULSE_REG_BIT0_MASK     (1U << 0U)
/* WRITE0PULSE_REG - BITS */
#define ALL_REG_TYPES_WRITE0PULSE_REG_BITS_POS      1U
#define ALL_REG_TYPES_WRITE0PULSE_REG_BITS_MASK     (0xFU << 1U)

/* 寄存器访问宏定义 */
/* READWRITE_REG - VALUE 读写宏 */
#define ALL_REG_TYPES_GET_READWRITE_REG_VALUE(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_READWRITE_REG_VALUE_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_READWRITE_REG_VALUE(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_READWRITE_REG_VALUE_MASK) | \
    (((value) << 0U) & ALL_REG_TYPES_READWRITE_REG_VALUE_MASK))
/* READONLY_REG - VALUE 读写宏 */
#define ALL_REG_TYPES_GET_READONLY_REG_VALUE(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_READONLY_REG_VALUE_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_READONLY_REG_VALUE(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_READONLY_REG_VALUE_MASK) | \
    (((value) << 0U) & ALL_REG_TYPES_READONLY_REG_VALUE_MASK))
/* WRITEONLY_REG - VALUE 读写宏 */
#define ALL_REG_TYPES_GET_WRITEONLY_REG_VALUE(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITEONLY_REG_VALUE_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITEONLY_REG_VALUE(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITEONLY_REG_VALUE_MASK) | \
    (((value) << 0U) & ALL_REG_TYPES_WRITEONLY_REG_VALUE_MASK))
/* WRITE1CLEAN_REG - VALUE 读写宏 */
#define ALL_REG_TYPES_GET_WRITE1CLEAN_REG_VALUE(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE1CLEAN_REG_VALUE_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITE1CLEAN_REG_VALUE(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE1CLEAN_REG_VALUE_MASK) | \
    (((value) << 0U) & ALL_REG_TYPES_WRITE1CLEAN_REG_VALUE_MASK))
/* WRITE1CLEAN_REG - BIT0 读写宏 */
#define ALL_REG_TYPES_GET_WRITE1CLEAN_REG_BIT0(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE1CLEAN_REG_BIT0_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITE1CLEAN_REG_BIT0(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE1CLEAN_REG_BIT0_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* WRITE1CLEAN_REG - BITS 读写宏 */
#define ALL_REG_TYPES_GET_WRITE1CLEAN_REG_BITS(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE1CLEAN_REG_BITS_MASK) >> 1U)
    
#define ALL_REG_TYPES_SET_WRITE1CLEAN_REG_BITS(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE1CLEAN_REG_BITS_MASK) | \
    (((value) << 1U) & ALL_REG_TYPES_WRITE1CLEAN_REG_BITS_MASK))
/* WRITE1SET_REG - VALUE 读写宏 */
#define ALL_REG_TYPES_GET_WRITE1SET_REG_VALUE(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE1SET_REG_VALUE_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITE1SET_REG_VALUE(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE1SET_REG_VALUE_MASK) | \
    (((value) << 0U) & ALL_REG_TYPES_WRITE1SET_REG_VALUE_MASK))
/* WRITE1SET_REG - BIT0 读写宏 */
#define ALL_REG_TYPES_GET_WRITE1SET_REG_BIT0(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE1SET_REG_BIT0_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITE1SET_REG_BIT0(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE1SET_REG_BIT0_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* WRITE1SET_REG - BITS 读写宏 */
#define ALL_REG_TYPES_GET_WRITE1SET_REG_BITS(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE1SET_REG_BITS_MASK) >> 1U)
    
#define ALL_REG_TYPES_SET_WRITE1SET_REG_BITS(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE1SET_REG_BITS_MASK) | \
    (((value) << 1U) & ALL_REG_TYPES_WRITE1SET_REG_BITS_MASK))
/* WRITE0CLEAN_REG - VALUE 读写宏 */
#define ALL_REG_TYPES_GET_WRITE0CLEAN_REG_VALUE(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE0CLEAN_REG_VALUE_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITE0CLEAN_REG_VALUE(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE0CLEAN_REG_VALUE_MASK) | \
    (((value) << 0U) & ALL_REG_TYPES_WRITE0CLEAN_REG_VALUE_MASK))
/* WRITE0CLEAN_REG - BIT0 读写宏 */
#define ALL_REG_TYPES_GET_WRITE0CLEAN_REG_BIT0(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE0CLEAN_REG_BIT0_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITE0CLEAN_REG_BIT0(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE0CLEAN_REG_BIT0_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* WRITE0CLEAN_REG - BITS 读写宏 */
#define ALL_REG_TYPES_GET_WRITE0CLEAN_REG_BITS(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE0CLEAN_REG_BITS_MASK) >> 1U)
    
#define ALL_REG_TYPES_SET_WRITE0CLEAN_REG_BITS(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE0CLEAN_REG_BITS_MASK) | \
    (((value) << 1U) & ALL_REG_TYPES_WRITE0CLEAN_REG_BITS_MASK))
/* WRITE0SET_REG - VALUE 读写宏 */
#define ALL_REG_TYPES_GET_WRITE0SET_REG_VALUE(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE0SET_REG_VALUE_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITE0SET_REG_VALUE(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE0SET_REG_VALUE_MASK) | \
    (((value) << 0U) & ALL_REG_TYPES_WRITE0SET_REG_VALUE_MASK))
/* WRITE0SET_REG - BIT0 读写宏 */
#define ALL_REG_TYPES_GET_WRITE0SET_REG_BIT0(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE0SET_REG_BIT0_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITE0SET_REG_BIT0(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE0SET_REG_BIT0_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* WRITE0SET_REG - BITS 读写宏 */
#define ALL_REG_TYPES_GET_WRITE0SET_REG_BITS(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE0SET_REG_BITS_MASK) >> 1U)
    
#define ALL_REG_TYPES_SET_WRITE0SET_REG_BITS(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE0SET_REG_BITS_MASK) | \
    (((value) << 1U) & ALL_REG_TYPES_WRITE0SET_REG_BITS_MASK))
/* WRITEONCE_REG - VALUE 读写宏 */
#define ALL_REG_TYPES_GET_WRITEONCE_REG_VALUE(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITEONCE_REG_VALUE_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITEONCE_REG_VALUE(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITEONCE_REG_VALUE_MASK) | \
    (((value) << 0U) & ALL_REG_TYPES_WRITEONCE_REG_VALUE_MASK))
/* WRITEONLYONCE_REG - VALUE 读写宏 */
#define ALL_REG_TYPES_GET_WRITEONLYONCE_REG_VALUE(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITEONLYONCE_REG_VALUE_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITEONLYONCE_REG_VALUE(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITEONLYONCE_REG_VALUE_MASK) | \
    (((value) << 0U) & ALL_REG_TYPES_WRITEONLYONCE_REG_VALUE_MASK))
/* READCLEAN_REG - VALUE 读写宏 */
#define ALL_REG_TYPES_GET_READCLEAN_REG_VALUE(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_READCLEAN_REG_VALUE_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_READCLEAN_REG_VALUE(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_READCLEAN_REG_VALUE_MASK) | \
    (((value) << 0U) & ALL_REG_TYPES_READCLEAN_REG_VALUE_MASK))
/* READSET_REG - VALUE 读写宏 */
#define ALL_REG_TYPES_GET_READSET_REG_VALUE(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_READSET_REG_VALUE_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_READSET_REG_VALUE(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_READSET_REG_VALUE_MASK) | \
    (((value) << 0U) & ALL_REG_TYPES_READSET_REG_VALUE_MASK))
/* WRITEREADCLEAN_REG - VALUE 读写宏 */
#define ALL_REG_TYPES_GET_WRITEREADCLEAN_REG_VALUE(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITEREADCLEAN_REG_VALUE_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITEREADCLEAN_REG_VALUE(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITEREADCLEAN_REG_VALUE_MASK) | \
    (((value) << 0U) & ALL_REG_TYPES_WRITEREADCLEAN_REG_VALUE_MASK))
/* WRITEREADSET_REG - VALUE 读写宏 */
#define ALL_REG_TYPES_GET_WRITEREADSET_REG_VALUE(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITEREADSET_REG_VALUE_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITEREADSET_REG_VALUE(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITEREADSET_REG_VALUE_MASK) | \
    (((value) << 0U) & ALL_REG_TYPES_WRITEREADSET_REG_VALUE_MASK))
/* WRITE1PULSE_REG - VALUE 读写宏 */
#define ALL_REG_TYPES_GET_WRITE1PULSE_REG_VALUE(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE1PULSE_REG_VALUE_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITE1PULSE_REG_VALUE(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE1PULSE_REG_VALUE_MASK) | \
    (((value) << 0U) & ALL_REG_TYPES_WRITE1PULSE_REG_VALUE_MASK))
/* WRITE1PULSE_REG - BIT0 读写宏 */
#define ALL_REG_TYPES_GET_WRITE1PULSE_REG_BIT0(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE1PULSE_REG_BIT0_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITE1PULSE_REG_BIT0(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE1PULSE_REG_BIT0_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* WRITE1PULSE_REG - BITS 读写宏 */
#define ALL_REG_TYPES_GET_WRITE1PULSE_REG_BITS(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE1PULSE_REG_BITS_MASK) >> 1U)
    
#define ALL_REG_TYPES_SET_WRITE1PULSE_REG_BITS(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE1PULSE_REG_BITS_MASK) | \
    (((value) << 1U) & ALL_REG_TYPES_WRITE1PULSE_REG_BITS_MASK))
/* WRITE0PULSE_REG - VALUE 读写宏 */
#define ALL_REG_TYPES_GET_WRITE0PULSE_REG_VALUE(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE0PULSE_REG_VALUE_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITE0PULSE_REG_VALUE(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE0PULSE_REG_VALUE_MASK) | \
    (((value) << 0U) & ALL_REG_TYPES_WRITE0PULSE_REG_VALUE_MASK))
/* WRITE0PULSE_REG - BIT0 读写宏 */
#define ALL_REG_TYPES_GET_WRITE0PULSE_REG_BIT0(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE0PULSE_REG_BIT0_MASK) >> 0U)
    
#define ALL_REG_TYPES_SET_WRITE0PULSE_REG_BIT0(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE0PULSE_REG_BIT0_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* WRITE0PULSE_REG - BITS 读写宏 */
#define ALL_REG_TYPES_GET_WRITE0PULSE_REG_BITS(reg_val)  \
    (((reg_val) & ALL_REG_TYPES_WRITE0PULSE_REG_BITS_MASK) >> 1U)
    
#define ALL_REG_TYPES_SET_WRITE0PULSE_REG_BITS(reg_val, value)  \
    (((reg_val) & ~ALL_REG_TYPES_WRITE0PULSE_REG_BITS_MASK) | \
    (((value) << 1U) & ALL_REG_TYPES_WRITE0PULSE_REG_BITS_MASK))

/* 寄存器类型定义 */
typedef struct {
    uint32_t readwrite_reg;  /**< ReadWrite类型寄存器 */
    uint32_t readonly_reg;  /**< ReadOnly类型寄存器 */
    uint32_t writeonly_reg;  /**< WriteOnly类型寄存器 */
    uint32_t write1clean_reg;  /**< Write1Clean类型寄存器 */
    uint32_t write1set_reg;  /**< Write1Set类型寄存器 */
    uint32_t write0clean_reg;  /**< Write0Clean类型寄存器 */
    uint32_t write0set_reg;  /**< Write0Set类型寄存器 */
    uint32_t writeonce_reg;  /**< WriteOnce类型寄存器 */
    uint32_t writeonlyonce_reg;  /**< WriteOnlyOnce类型寄存器 */
    uint32_t readclean_reg;  /**< ReadClean类型寄存器 */
    uint32_t readset_reg;  /**< ReadSet类型寄存器 */
    uint32_t writereadclean_reg;  /**< WriteReadClean类型寄存器 */
    uint32_t writereadset_reg;  /**< WriteReadSet类型寄存器 */
    uint32_t write1pulse_reg;  /**< Write1Pulse类型寄存器 */
    uint32_t write0pulse_reg;  /**< Write0Pulse类型寄存器 */
} all_reg_types_regs_t;

#ifdef __cplusplus
}
#endif

#endif /* ALL_REG_TYPES_H */ 