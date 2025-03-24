/**
 * @file custom_regfile.h
 * @brief 自动生成的寄存器定义头文件
 * @note 生成时间: 2025-03-24 19:30:49
 */

#ifndef CUSTOM_REGFILE_H
#define CUSTOM_REGFILE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* 寄存器地址定义 */
#define CUSTOM_REGFILE_CTRL_REG_ADDR      0x0U  /**< 控制寄存器 */
#define CUSTOM_REGFILE_STATUS_REG_ADDR      0x4U  /**< 状态寄存器 */
#define CUSTOM_REGFILE_INT_FLAGS_ADDR      0x8U  /**< 中断标志寄存器，读取后自动清零 */
#define CUSTOM_REGFILE_INT_ENABLE_ADDR      0xCU  /**< 中断使能寄存器 */
#define CUSTOM_REGFILE_TX_DATA_ADDR      0x10U  /**< 发送数据寄存器，只能写入 */
#define CUSTOM_REGFILE_RX_DATA_ADDR      0x14U  /**< 接收数据寄存器，只能读取 */
#define CUSTOM_REGFILE_CONFIG_ADDR      0x18U  /**< 配置寄存器 */
#define CUSTOM_REGFILE_INT_CLEAR_ADDR      0x1CU  /**< 中断清除寄存器，写1清零中断标志 */
#define CUSTOM_REGFILE_INT_SET_ADDR      0x20U  /**< 中断设置寄存器，写1设置中断标志 */
#define CUSTOM_REGFILE_LOCK_REG_ADDR      0x24U  /**< 锁定寄存器，只能写入一次 */

/* 寄存器位宽定义 */
#define CUSTOM_REGFILE_DATA_WIDTH     32U
#define CUSTOM_REGFILE_ADDR_WIDTH     8U

/* 寄存器位域定义 */
/* CTRL_REG - ENABLE */
#define CUSTOM_REGFILE_CTRL_REG_ENABLE_POS      0U
#define CUSTOM_REGFILE_CTRL_REG_ENABLE_MASK     (1U << 0U)
/* CTRL_REG - MODE */
#define CUSTOM_REGFILE_CTRL_REG_MODE_POS      2:1U
#define CUSTOM_REGFILE_CTRL_REG_MODE_MASK     (1U << 2:1U)
/* CTRL_REG - START */
#define CUSTOM_REGFILE_CTRL_REG_START_POS      3U
#define CUSTOM_REGFILE_CTRL_REG_START_MASK     (1U << 3U)
/* STATUS_REG - BUSY */
#define CUSTOM_REGFILE_STATUS_REG_BUSY_POS      0U
#define CUSTOM_REGFILE_STATUS_REG_BUSY_MASK     (1U << 0U)
/* STATUS_REG - ERROR */
#define CUSTOM_REGFILE_STATUS_REG_ERROR_POS      1U
#define CUSTOM_REGFILE_STATUS_REG_ERROR_MASK     (1U << 1U)
/* INT_FLAGS - TX_DONE */
#define CUSTOM_REGFILE_INT_FLAGS_TX_DONE_POS      0U
#define CUSTOM_REGFILE_INT_FLAGS_TX_DONE_MASK     (1U << 0U)
/* INT_FLAGS - RX_DONE */
#define CUSTOM_REGFILE_INT_FLAGS_RX_DONE_POS      1U
#define CUSTOM_REGFILE_INT_FLAGS_RX_DONE_MASK     (1U << 1U)
/* INT_FLAGS - ERROR */
#define CUSTOM_REGFILE_INT_FLAGS_ERROR_POS      2U
#define CUSTOM_REGFILE_INT_FLAGS_ERROR_MASK     (1U << 2U)

/* 寄存器类型定义 */
typedef struct {
    uint32_t ctrl_reg;  /**< 控制寄存器 */
    uint32_t status_reg;  /**< 状态寄存器 */
    uint32_t int_flags;  /**< 中断标志寄存器，读取后自动清零 */
    uint32_t int_enable;  /**< 中断使能寄存器 */
    uint32_t tx_data;  /**< 发送数据寄存器，只能写入 */
    uint32_t rx_data;  /**< 接收数据寄存器，只能读取 */
    uint32_t config;  /**< 配置寄存器 */
    uint32_t int_clear;  /**< 中断清除寄存器，写1清零中断标志 */
    uint32_t int_set;  /**< 中断设置寄存器，写1设置中断标志 */
    uint32_t lock_reg;  /**< 锁定寄存器，只能写入一次 */
} custom_regfile_regs_t;

#ifdef __cplusplus
}
#endif

#endif /* CUSTOM_REGFILE_H */ 