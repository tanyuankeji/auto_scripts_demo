/**
 * @file hierarchical_regfile.h
 * @brief 自动生成的寄存器定义头文件
 * @note 生成时间: 2025-03-27 21:39:49
 * @version 2.0.0
 */

#ifndef HIERARCHICAL_REGFILE_H
#define HIERARCHICAL_REGFILE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* 寄存器地址定义 */
#define HIERARCHICAL_REGFILE_CTRL_REG_ADDR      0x0U  /**< 控制寄存器 */
#define HIERARCHICAL_REGFILE_STATUS_REG_ADDR      0x0U  /**< 状态寄存器 */
#define HIERARCHICAL_REGFILE_INT_FLAG_REG_ADDR      0x0U  /**< 中断标志寄存器 */
#define HIERARCHICAL_REGFILE_WRITEONLY_REG_ADDR      0x0U  /**< 只写寄存器 */
#define HIERARCHICAL_REGFILE_WRITE1SET_REG_ADDR      0x0U  /**< 写1置位寄存器 */

/* 寄存器位宽定义 */
#define HIERARCHICAL_REGFILE_DATA_WIDTH     32U
#define HIERARCHICAL_REGFILE_ADDR_WIDTH     8U

/* 寄存器位域定义 */
/* CTRL_REG - ENABLE */
#define HIERARCHICAL_REGFILE_CTRL_REG_ENABLE_POS      0U
#define HIERARCHICAL_REGFILE_CTRL_REG_ENABLE_MASK     (1U << 0U)
/* CTRL_REG - MODE */
#define HIERARCHICAL_REGFILE_CTRL_REG_MODE_POS      1U
#define HIERARCHICAL_REGFILE_CTRL_REG_MODE_MASK     (0x3U << 1U)
/* CTRL_REG - START */
#define HIERARCHICAL_REGFILE_CTRL_REG_START_POS      3U
#define HIERARCHICAL_REGFILE_CTRL_REG_START_MASK     (1U << 3U)
/* STATUS_REG - BUSY */
#define HIERARCHICAL_REGFILE_STATUS_REG_BUSY_POS      0U
#define HIERARCHICAL_REGFILE_STATUS_REG_BUSY_MASK     (1U << 0U)
/* STATUS_REG - ERROR */
#define HIERARCHICAL_REGFILE_STATUS_REG_ERROR_POS      1U
#define HIERARCHICAL_REGFILE_STATUS_REG_ERROR_MASK     (1U << 1U)
/* INT_FLAG_REG - DATA_READY */
#define HIERARCHICAL_REGFILE_INT_FLAG_REG_DATA_READY_POS      0U
#define HIERARCHICAL_REGFILE_INT_FLAG_REG_DATA_READY_MASK     (1U << 0U)
/* WRITE1SET_REG - BIT0 */
#define HIERARCHICAL_REGFILE_WRITE1SET_REG_BIT0_POS      0U
#define HIERARCHICAL_REGFILE_WRITE1SET_REG_BIT0_MASK     (1U << 0U)

/* 寄存器访问宏定义 */
/* CTRL_REG - ENABLE 读写宏 */
#define HIERARCHICAL_REGFILE_GET_CTRL_REG_ENABLE(reg_val)  \
    (((reg_val) & HIERARCHICAL_REGFILE_CTRL_REG_ENABLE_MASK) >> 0U)
    
#define HIERARCHICAL_REGFILE_SET_CTRL_REG_ENABLE(reg_val, value)  \
    (((reg_val) & ~HIERARCHICAL_REGFILE_CTRL_REG_ENABLE_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* CTRL_REG - MODE 读写宏 */
#define HIERARCHICAL_REGFILE_GET_CTRL_REG_MODE(reg_val)  \
    (((reg_val) & HIERARCHICAL_REGFILE_CTRL_REG_MODE_MASK) >> 1U)
    
#define HIERARCHICAL_REGFILE_SET_CTRL_REG_MODE(reg_val, value)  \
    (((reg_val) & ~HIERARCHICAL_REGFILE_CTRL_REG_MODE_MASK) | \
    (((value) << 1U) & HIERARCHICAL_REGFILE_CTRL_REG_MODE_MASK))
/* CTRL_REG - START 读写宏 */
#define HIERARCHICAL_REGFILE_GET_CTRL_REG_START(reg_val)  \
    (((reg_val) & HIERARCHICAL_REGFILE_CTRL_REG_START_MASK) >> 3U)
    
#define HIERARCHICAL_REGFILE_SET_CTRL_REG_START(reg_val, value)  \
    (((reg_val) & ~HIERARCHICAL_REGFILE_CTRL_REG_START_MASK) | \
    (((value) ? 1U : 0U) << 3U))
/* STATUS_REG - BUSY 读写宏 */
#define HIERARCHICAL_REGFILE_GET_STATUS_REG_BUSY(reg_val)  \
    (((reg_val) & HIERARCHICAL_REGFILE_STATUS_REG_BUSY_MASK) >> 0U)
    
#define HIERARCHICAL_REGFILE_SET_STATUS_REG_BUSY(reg_val, value)  \
    (((reg_val) & ~HIERARCHICAL_REGFILE_STATUS_REG_BUSY_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* STATUS_REG - ERROR 读写宏 */
#define HIERARCHICAL_REGFILE_GET_STATUS_REG_ERROR(reg_val)  \
    (((reg_val) & HIERARCHICAL_REGFILE_STATUS_REG_ERROR_MASK) >> 1U)
    
#define HIERARCHICAL_REGFILE_SET_STATUS_REG_ERROR(reg_val, value)  \
    (((reg_val) & ~HIERARCHICAL_REGFILE_STATUS_REG_ERROR_MASK) | \
    (((value) ? 1U : 0U) << 1U))
/* INT_FLAG_REG - DATA_READY 读写宏 */
#define HIERARCHICAL_REGFILE_GET_INT_FLAG_REG_DATA_READY(reg_val)  \
    (((reg_val) & HIERARCHICAL_REGFILE_INT_FLAG_REG_DATA_READY_MASK) >> 0U)
    
#define HIERARCHICAL_REGFILE_SET_INT_FLAG_REG_DATA_READY(reg_val, value)  \
    (((reg_val) & ~HIERARCHICAL_REGFILE_INT_FLAG_REG_DATA_READY_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* WRITE1SET_REG - BIT0 读写宏 */
#define HIERARCHICAL_REGFILE_GET_WRITE1SET_REG_BIT0(reg_val)  \
    (((reg_val) & HIERARCHICAL_REGFILE_WRITE1SET_REG_BIT0_MASK) >> 0U)
    
#define HIERARCHICAL_REGFILE_SET_WRITE1SET_REG_BIT0(reg_val, value)  \
    (((reg_val) & ~HIERARCHICAL_REGFILE_WRITE1SET_REG_BIT0_MASK) | \
    (((value) ? 1U : 0U) << 0U))

/* 寄存器类型定义 */
typedef struct {
    uint32_t ctrl_reg;  /**< 控制寄存器 */
    uint32_t status_reg;  /**< 状态寄存器 */
    uint32_t int_flag_reg;  /**< 中断标志寄存器 */
    uint32_t writeonly_reg;  /**< 只写寄存器 */
    uint32_t write1set_reg;  /**< 写1置位寄存器 */
} hierarchical_regfile_regs_t;

#ifdef __cplusplus
}
#endif

#endif /* HIERARCHICAL_REGFILE_H */ 