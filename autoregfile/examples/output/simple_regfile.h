/**
 * @file example_regfile.h
 * @brief 自动生成的寄存器定义头文件
 * @note 生成时间: 2025-03-24 20:09:52
 * @version 2.0.0
 */

#ifndef EXAMPLE_REGFILE_H
#define EXAMPLE_REGFILE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* 寄存器地址定义 */
#define EXAMPLE_REGFILE_CTRL_REG_ADDR      0x0U  /**< 控制寄存器 */
#define EXAMPLE_REGFILE_STATUS_REG_ADDR      0x0U  /**< 状态寄存器 */
#define EXAMPLE_REGFILE_INT_FLAGS_ADDR      0x0U  /**< 中断标志寄存器，读取后自动清零 */
#define EXAMPLE_REGFILE_INT_ENABLE_ADDR      0x0U  /**< 中断使能寄存器 */

/* 寄存器位宽定义 */
#define EXAMPLE_REGFILE_DATA_WIDTH     32U
#define EXAMPLE_REGFILE_ADDR_WIDTH     8U

/* 寄存器位域定义 */
/* CTRL_REG - ENABLE */
#define EXAMPLE_REGFILE_CTRL_REG_ENABLE_POS      0U
#define EXAMPLE_REGFILE_CTRL_REG_ENABLE_MASK     (1U << 0U)
/* CTRL_REG - MODE */
#define EXAMPLE_REGFILE_CTRL_REG_MODE_POS      1U
#define EXAMPLE_REGFILE_CTRL_REG_MODE_MASK     (0x3U << 1U)
/* CTRL_REG - START */
#define EXAMPLE_REGFILE_CTRL_REG_START_POS      3U
#define EXAMPLE_REGFILE_CTRL_REG_START_MASK     (1U << 3U)
/* STATUS_REG - BUSY */
#define EXAMPLE_REGFILE_STATUS_REG_BUSY_POS      0U
#define EXAMPLE_REGFILE_STATUS_REG_BUSY_MASK     (1U << 0U)
/* STATUS_REG - ERROR */
#define EXAMPLE_REGFILE_STATUS_REG_ERROR_POS      1U
#define EXAMPLE_REGFILE_STATUS_REG_ERROR_MASK     (1U << 1U)
/* INT_FLAGS - DATA_READY */
#define EXAMPLE_REGFILE_INT_FLAGS_DATA_READY_POS      0U
#define EXAMPLE_REGFILE_INT_FLAGS_DATA_READY_MASK     (1U << 0U)
/* INT_FLAGS - ERROR_FLAG */
#define EXAMPLE_REGFILE_INT_FLAGS_ERROR_FLAG_POS      1U
#define EXAMPLE_REGFILE_INT_FLAGS_ERROR_FLAG_MASK     (1U << 1U)
/* INT_ENABLE - DATA_READY_EN */
#define EXAMPLE_REGFILE_INT_ENABLE_DATA_READY_EN_POS      0U
#define EXAMPLE_REGFILE_INT_ENABLE_DATA_READY_EN_MASK     (1U << 0U)
/* INT_ENABLE - ERROR_EN */
#define EXAMPLE_REGFILE_INT_ENABLE_ERROR_EN_POS      1U
#define EXAMPLE_REGFILE_INT_ENABLE_ERROR_EN_MASK     (1U << 1U)

/* 寄存器访问宏定义 */
/* CTRL_REG - ENABLE 读写宏 */
#define EXAMPLE_REGFILE_GET_CTRL_REG_ENABLE(reg_val)  \
    (((reg_val) & EXAMPLE_REGFILE_CTRL_REG_ENABLE_MASK) >> 0U)
    
#define EXAMPLE_REGFILE_SET_CTRL_REG_ENABLE(reg_val, value)  \
    (((reg_val) & ~EXAMPLE_REGFILE_CTRL_REG_ENABLE_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* CTRL_REG - MODE 读写宏 */
#define EXAMPLE_REGFILE_GET_CTRL_REG_MODE(reg_val)  \
    (((reg_val) & EXAMPLE_REGFILE_CTRL_REG_MODE_MASK) >> 1U)
    
#define EXAMPLE_REGFILE_SET_CTRL_REG_MODE(reg_val, value)  \
    (((reg_val) & ~EXAMPLE_REGFILE_CTRL_REG_MODE_MASK) | \
    (((value) << 1U) & EXAMPLE_REGFILE_CTRL_REG_MODE_MASK))
/* CTRL_REG - START 读写宏 */
#define EXAMPLE_REGFILE_GET_CTRL_REG_START(reg_val)  \
    (((reg_val) & EXAMPLE_REGFILE_CTRL_REG_START_MASK) >> 3U)
    
#define EXAMPLE_REGFILE_SET_CTRL_REG_START(reg_val, value)  \
    (((reg_val) & ~EXAMPLE_REGFILE_CTRL_REG_START_MASK) | \
    (((value) ? 1U : 0U) << 3U))
/* STATUS_REG - BUSY 读写宏 */
#define EXAMPLE_REGFILE_GET_STATUS_REG_BUSY(reg_val)  \
    (((reg_val) & EXAMPLE_REGFILE_STATUS_REG_BUSY_MASK) >> 0U)
    
#define EXAMPLE_REGFILE_SET_STATUS_REG_BUSY(reg_val, value)  \
    (((reg_val) & ~EXAMPLE_REGFILE_STATUS_REG_BUSY_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* STATUS_REG - ERROR 读写宏 */
#define EXAMPLE_REGFILE_GET_STATUS_REG_ERROR(reg_val)  \
    (((reg_val) & EXAMPLE_REGFILE_STATUS_REG_ERROR_MASK) >> 1U)
    
#define EXAMPLE_REGFILE_SET_STATUS_REG_ERROR(reg_val, value)  \
    (((reg_val) & ~EXAMPLE_REGFILE_STATUS_REG_ERROR_MASK) | \
    (((value) ? 1U : 0U) << 1U))
/* INT_FLAGS - DATA_READY 读写宏 */
#define EXAMPLE_REGFILE_GET_INT_FLAGS_DATA_READY(reg_val)  \
    (((reg_val) & EXAMPLE_REGFILE_INT_FLAGS_DATA_READY_MASK) >> 0U)
    
#define EXAMPLE_REGFILE_SET_INT_FLAGS_DATA_READY(reg_val, value)  \
    (((reg_val) & ~EXAMPLE_REGFILE_INT_FLAGS_DATA_READY_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* INT_FLAGS - ERROR_FLAG 读写宏 */
#define EXAMPLE_REGFILE_GET_INT_FLAGS_ERROR_FLAG(reg_val)  \
    (((reg_val) & EXAMPLE_REGFILE_INT_FLAGS_ERROR_FLAG_MASK) >> 1U)
    
#define EXAMPLE_REGFILE_SET_INT_FLAGS_ERROR_FLAG(reg_val, value)  \
    (((reg_val) & ~EXAMPLE_REGFILE_INT_FLAGS_ERROR_FLAG_MASK) | \
    (((value) ? 1U : 0U) << 1U))
/* INT_ENABLE - DATA_READY_EN 读写宏 */
#define EXAMPLE_REGFILE_GET_INT_ENABLE_DATA_READY_EN(reg_val)  \
    (((reg_val) & EXAMPLE_REGFILE_INT_ENABLE_DATA_READY_EN_MASK) >> 0U)
    
#define EXAMPLE_REGFILE_SET_INT_ENABLE_DATA_READY_EN(reg_val, value)  \
    (((reg_val) & ~EXAMPLE_REGFILE_INT_ENABLE_DATA_READY_EN_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* INT_ENABLE - ERROR_EN 读写宏 */
#define EXAMPLE_REGFILE_GET_INT_ENABLE_ERROR_EN(reg_val)  \
    (((reg_val) & EXAMPLE_REGFILE_INT_ENABLE_ERROR_EN_MASK) >> 1U)
    
#define EXAMPLE_REGFILE_SET_INT_ENABLE_ERROR_EN(reg_val, value)  \
    (((reg_val) & ~EXAMPLE_REGFILE_INT_ENABLE_ERROR_EN_MASK) | \
    (((value) ? 1U : 0U) << 1U))

/* 寄存器类型定义 */
typedef struct {
    uint32_t ctrl_reg;  /**< 控制寄存器 */
    uint32_t status_reg;  /**< 状态寄存器 */
    uint32_t int_flags;  /**< 中断标志寄存器，读取后自动清零 */
    uint32_t int_enable;  /**< 中断使能寄存器 */
} example_regfile_regs_t;

#ifdef __cplusplus
}
#endif

#endif /* EXAMPLE_REGFILE_H */ 