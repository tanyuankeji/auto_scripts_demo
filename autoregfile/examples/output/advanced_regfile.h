/**
 * @file advanced_regfile.h
 * @brief 自动生成的寄存器定义头文件
 * @note 生成时间: 2025-03-24 20:16:00
 * @version 2.0.0
 */

#ifndef ADVANCED_REGFILE_H
#define ADVANCED_REGFILE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* 寄存器地址定义 */
#define ADVANCED_REGFILE_CTRL_REG_ADDR      0x0U  /**< 主控寄存器 */
#define ADVANCED_REGFILE_STATUS_REG_ADDR      0x0U  /**< 状态寄存器 */
#define ADVANCED_REGFILE_INT_FLAGS_ADDR      0x0U  /**< 中断标志寄存器，读取后自动清零 */
#define ADVANCED_REGFILE_INT_ENABLE_ADDR      0x0U  /**< 中断使能寄存器 */
#define ADVANCED_REGFILE_INT_CLEAR_ADDR      0x0U  /**< 中断清除寄存器，写1清零对应位 */
#define ADVANCED_REGFILE_INT_SET_ADDR      0x0U  /**< 中断设置寄存器，写1置位对应位 */
#define ADVANCED_REGFILE_TX_DATA_ADDR      0x0U  /**< 发送数据寄存器，只能写入 */
#define ADVANCED_REGFILE_RX_DATA_ADDR      0x0U  /**< 接收数据寄存器，只能读取 */
#define ADVANCED_REGFILE_CONFIG_ADDR      0x0U  /**< 配置寄存器 */
#define ADVANCED_REGFILE_LOCK_REG_ADDR      0x0U  /**< 锁定寄存器，只能写入一次 */
#define ADVANCED_REGFILE_STAT_COUNT_ADDR      0x0U  /**< 统计计数器，读取后自动置位 */
#define ADVANCED_REGFILE_W0C_REG_ADDR      0x0U  /**< 写0清零寄存器，写0清零对应位 */
#define ADVANCED_REGFILE_W0S_REG_ADDR      0x0U  /**< 写0置位寄存器，写0置位对应位 */
#define ADVANCED_REGFILE_TOG_REG_ADDR      0x0U  /**< 翻转寄存器，写1翻转对应位 */
#define ADVANCED_REGFILE_VER_REG_ADDR      0x0U  /**< 版本信息寄存器 */

/* 寄存器位宽定义 */
#define ADVANCED_REGFILE_DATA_WIDTH     32U
#define ADVANCED_REGFILE_ADDR_WIDTH     8U

/* 寄存器位域定义 */
/* CTRL_REG - ENABLE */
#define ADVANCED_REGFILE_CTRL_REG_ENABLE_POS      0U
#define ADVANCED_REGFILE_CTRL_REG_ENABLE_MASK     (1U << 0U)
/* CTRL_REG - MODE */
#define ADVANCED_REGFILE_CTRL_REG_MODE_POS      1U
#define ADVANCED_REGFILE_CTRL_REG_MODE_MASK     (0x3U << 1U)
/* CTRL_REG - START */
#define ADVANCED_REGFILE_CTRL_REG_START_POS      3U
#define ADVANCED_REGFILE_CTRL_REG_START_MASK     (1U << 3U)
/* CTRL_REG - STOP */
#define ADVANCED_REGFILE_CTRL_REG_STOP_POS      4U
#define ADVANCED_REGFILE_CTRL_REG_STOP_MASK     (1U << 4U)
/* CTRL_REG - RESET */
#define ADVANCED_REGFILE_CTRL_REG_RESET_POS      8U
#define ADVANCED_REGFILE_CTRL_REG_RESET_MASK     (1U << 8U)
/* STATUS_REG - BUSY */
#define ADVANCED_REGFILE_STATUS_REG_BUSY_POS      0U
#define ADVANCED_REGFILE_STATUS_REG_BUSY_MASK     (1U << 0U)
/* STATUS_REG - ERROR */
#define ADVANCED_REGFILE_STATUS_REG_ERROR_POS      1U
#define ADVANCED_REGFILE_STATUS_REG_ERROR_MASK     (1U << 1U)
/* STATUS_REG - DATA_VALID */
#define ADVANCED_REGFILE_STATUS_REG_DATA_VALID_POS      2U
#define ADVANCED_REGFILE_STATUS_REG_DATA_VALID_MASK     (1U << 2U)
/* STATUS_REG - FIFO_FULL */
#define ADVANCED_REGFILE_STATUS_REG_FIFO_FULL_POS      3U
#define ADVANCED_REGFILE_STATUS_REG_FIFO_FULL_MASK     (1U << 3U)
/* STATUS_REG - FIFO_EMPTY */
#define ADVANCED_REGFILE_STATUS_REG_FIFO_EMPTY_POS      4U
#define ADVANCED_REGFILE_STATUS_REG_FIFO_EMPTY_MASK     (1U << 4U)
/* STATUS_REG - FIFO_COUNT */
#define ADVANCED_REGFILE_STATUS_REG_FIFO_COUNT_POS      8U
#define ADVANCED_REGFILE_STATUS_REG_FIFO_COUNT_MASK     (0x1FU << 8U)
/* INT_FLAGS - DATA_READY */
#define ADVANCED_REGFILE_INT_FLAGS_DATA_READY_POS      0U
#define ADVANCED_REGFILE_INT_FLAGS_DATA_READY_MASK     (1U << 0U)
/* INT_FLAGS - ERROR_FLAG */
#define ADVANCED_REGFILE_INT_FLAGS_ERROR_FLAG_POS      1U
#define ADVANCED_REGFILE_INT_FLAGS_ERROR_FLAG_MASK     (1U << 1U)
/* INT_FLAGS - TIMEOUT */
#define ADVANCED_REGFILE_INT_FLAGS_TIMEOUT_POS      2U
#define ADVANCED_REGFILE_INT_FLAGS_TIMEOUT_MASK     (1U << 2U)
/* INT_FLAGS - FIFO_FULL_FLAG */
#define ADVANCED_REGFILE_INT_FLAGS_FIFO_FULL_FLAG_POS      3U
#define ADVANCED_REGFILE_INT_FLAGS_FIFO_FULL_FLAG_MASK     (1U << 3U)
/* INT_FLAGS - FIFO_EMPTY_FLAG */
#define ADVANCED_REGFILE_INT_FLAGS_FIFO_EMPTY_FLAG_POS      4U
#define ADVANCED_REGFILE_INT_FLAGS_FIFO_EMPTY_FLAG_MASK     (1U << 4U)
/* INT_ENABLE - DATA_READY_EN */
#define ADVANCED_REGFILE_INT_ENABLE_DATA_READY_EN_POS      0U
#define ADVANCED_REGFILE_INT_ENABLE_DATA_READY_EN_MASK     (1U << 0U)
/* INT_ENABLE - ERROR_EN */
#define ADVANCED_REGFILE_INT_ENABLE_ERROR_EN_POS      1U
#define ADVANCED_REGFILE_INT_ENABLE_ERROR_EN_MASK     (1U << 1U)
/* INT_ENABLE - TIMEOUT_EN */
#define ADVANCED_REGFILE_INT_ENABLE_TIMEOUT_EN_POS      2U
#define ADVANCED_REGFILE_INT_ENABLE_TIMEOUT_EN_MASK     (1U << 2U)
/* INT_ENABLE - FIFO_FULL_EN */
#define ADVANCED_REGFILE_INT_ENABLE_FIFO_FULL_EN_POS      3U
#define ADVANCED_REGFILE_INT_ENABLE_FIFO_FULL_EN_MASK     (1U << 3U)
/* INT_ENABLE - FIFO_EMPTY_EN */
#define ADVANCED_REGFILE_INT_ENABLE_FIFO_EMPTY_EN_POS      4U
#define ADVANCED_REGFILE_INT_ENABLE_FIFO_EMPTY_EN_MASK     (1U << 4U)
/* CONFIG - CLK_DIV */
#define ADVANCED_REGFILE_CONFIG_CLK_DIV_POS      0U
#define ADVANCED_REGFILE_CONFIG_CLK_DIV_MASK     (0xFFU << 0U)
/* CONFIG - FIFO_THR */
#define ADVANCED_REGFILE_CONFIG_FIFO_THR_POS      8U
#define ADVANCED_REGFILE_CONFIG_FIFO_THR_MASK     (0x1FU << 8U)
/* CONFIG - TIMEOUT_VAL */
#define ADVANCED_REGFILE_CONFIG_TIMEOUT_VAL_POS      16U
#define ADVANCED_REGFILE_CONFIG_TIMEOUT_VAL_MASK     (0xFFU << 16U)
/* CONFIG - AUTO_MODE */
#define ADVANCED_REGFILE_CONFIG_AUTO_MODE_POS      24U
#define ADVANCED_REGFILE_CONFIG_AUTO_MODE_MASK     (1U << 24U)
/* LOCK_REG - LOCK_KEY */
#define ADVANCED_REGFILE_LOCK_REG_LOCK_KEY_POS      0U
#define ADVANCED_REGFILE_LOCK_REG_LOCK_KEY_MASK     (0xFFFFFFFFU << 0U)
/* VER_REG - MINOR_VER */
#define ADVANCED_REGFILE_VER_REG_MINOR_VER_POS      0U
#define ADVANCED_REGFILE_VER_REG_MINOR_VER_MASK     (0xFFFFU << 0U)
/* VER_REG - MAJOR_VER */
#define ADVANCED_REGFILE_VER_REG_MAJOR_VER_POS      16U
#define ADVANCED_REGFILE_VER_REG_MAJOR_VER_MASK     (0xFFFFU << 16U)

/* 寄存器访问宏定义 */
/* CTRL_REG - ENABLE 读写宏 */
#define ADVANCED_REGFILE_GET_CTRL_REG_ENABLE(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_CTRL_REG_ENABLE_MASK) >> 0U)
    
#define ADVANCED_REGFILE_SET_CTRL_REG_ENABLE(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_CTRL_REG_ENABLE_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* CTRL_REG - MODE 读写宏 */
#define ADVANCED_REGFILE_GET_CTRL_REG_MODE(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_CTRL_REG_MODE_MASK) >> 1U)
    
#define ADVANCED_REGFILE_SET_CTRL_REG_MODE(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_CTRL_REG_MODE_MASK) | \
    (((value) << 1U) & ADVANCED_REGFILE_CTRL_REG_MODE_MASK))
/* CTRL_REG - START 读写宏 */
#define ADVANCED_REGFILE_GET_CTRL_REG_START(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_CTRL_REG_START_MASK) >> 3U)
    
#define ADVANCED_REGFILE_SET_CTRL_REG_START(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_CTRL_REG_START_MASK) | \
    (((value) ? 1U : 0U) << 3U))
/* CTRL_REG - STOP 读写宏 */
#define ADVANCED_REGFILE_GET_CTRL_REG_STOP(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_CTRL_REG_STOP_MASK) >> 4U)
    
#define ADVANCED_REGFILE_SET_CTRL_REG_STOP(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_CTRL_REG_STOP_MASK) | \
    (((value) ? 1U : 0U) << 4U))
/* CTRL_REG - RESET 读写宏 */
#define ADVANCED_REGFILE_GET_CTRL_REG_RESET(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_CTRL_REG_RESET_MASK) >> 8U)
    
#define ADVANCED_REGFILE_SET_CTRL_REG_RESET(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_CTRL_REG_RESET_MASK) | \
    (((value) ? 1U : 0U) << 8U))
/* STATUS_REG - BUSY 读写宏 */
#define ADVANCED_REGFILE_GET_STATUS_REG_BUSY(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_STATUS_REG_BUSY_MASK) >> 0U)
    
#define ADVANCED_REGFILE_SET_STATUS_REG_BUSY(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_STATUS_REG_BUSY_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* STATUS_REG - ERROR 读写宏 */
#define ADVANCED_REGFILE_GET_STATUS_REG_ERROR(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_STATUS_REG_ERROR_MASK) >> 1U)
    
#define ADVANCED_REGFILE_SET_STATUS_REG_ERROR(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_STATUS_REG_ERROR_MASK) | \
    (((value) ? 1U : 0U) << 1U))
/* STATUS_REG - DATA_VALID 读写宏 */
#define ADVANCED_REGFILE_GET_STATUS_REG_DATA_VALID(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_STATUS_REG_DATA_VALID_MASK) >> 2U)
    
#define ADVANCED_REGFILE_SET_STATUS_REG_DATA_VALID(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_STATUS_REG_DATA_VALID_MASK) | \
    (((value) ? 1U : 0U) << 2U))
/* STATUS_REG - FIFO_FULL 读写宏 */
#define ADVANCED_REGFILE_GET_STATUS_REG_FIFO_FULL(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_STATUS_REG_FIFO_FULL_MASK) >> 3U)
    
#define ADVANCED_REGFILE_SET_STATUS_REG_FIFO_FULL(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_STATUS_REG_FIFO_FULL_MASK) | \
    (((value) ? 1U : 0U) << 3U))
/* STATUS_REG - FIFO_EMPTY 读写宏 */
#define ADVANCED_REGFILE_GET_STATUS_REG_FIFO_EMPTY(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_STATUS_REG_FIFO_EMPTY_MASK) >> 4U)
    
#define ADVANCED_REGFILE_SET_STATUS_REG_FIFO_EMPTY(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_STATUS_REG_FIFO_EMPTY_MASK) | \
    (((value) ? 1U : 0U) << 4U))
/* STATUS_REG - FIFO_COUNT 读写宏 */
#define ADVANCED_REGFILE_GET_STATUS_REG_FIFO_COUNT(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_STATUS_REG_FIFO_COUNT_MASK) >> 8U)
    
#define ADVANCED_REGFILE_SET_STATUS_REG_FIFO_COUNT(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_STATUS_REG_FIFO_COUNT_MASK) | \
    (((value) << 8U) & ADVANCED_REGFILE_STATUS_REG_FIFO_COUNT_MASK))
/* INT_FLAGS - DATA_READY 读写宏 */
#define ADVANCED_REGFILE_GET_INT_FLAGS_DATA_READY(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_INT_FLAGS_DATA_READY_MASK) >> 0U)
    
#define ADVANCED_REGFILE_SET_INT_FLAGS_DATA_READY(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_INT_FLAGS_DATA_READY_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* INT_FLAGS - ERROR_FLAG 读写宏 */
#define ADVANCED_REGFILE_GET_INT_FLAGS_ERROR_FLAG(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_INT_FLAGS_ERROR_FLAG_MASK) >> 1U)
    
#define ADVANCED_REGFILE_SET_INT_FLAGS_ERROR_FLAG(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_INT_FLAGS_ERROR_FLAG_MASK) | \
    (((value) ? 1U : 0U) << 1U))
/* INT_FLAGS - TIMEOUT 读写宏 */
#define ADVANCED_REGFILE_GET_INT_FLAGS_TIMEOUT(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_INT_FLAGS_TIMEOUT_MASK) >> 2U)
    
#define ADVANCED_REGFILE_SET_INT_FLAGS_TIMEOUT(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_INT_FLAGS_TIMEOUT_MASK) | \
    (((value) ? 1U : 0U) << 2U))
/* INT_FLAGS - FIFO_FULL_FLAG 读写宏 */
#define ADVANCED_REGFILE_GET_INT_FLAGS_FIFO_FULL_FLAG(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_INT_FLAGS_FIFO_FULL_FLAG_MASK) >> 3U)
    
#define ADVANCED_REGFILE_SET_INT_FLAGS_FIFO_FULL_FLAG(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_INT_FLAGS_FIFO_FULL_FLAG_MASK) | \
    (((value) ? 1U : 0U) << 3U))
/* INT_FLAGS - FIFO_EMPTY_FLAG 读写宏 */
#define ADVANCED_REGFILE_GET_INT_FLAGS_FIFO_EMPTY_FLAG(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_INT_FLAGS_FIFO_EMPTY_FLAG_MASK) >> 4U)
    
#define ADVANCED_REGFILE_SET_INT_FLAGS_FIFO_EMPTY_FLAG(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_INT_FLAGS_FIFO_EMPTY_FLAG_MASK) | \
    (((value) ? 1U : 0U) << 4U))
/* INT_ENABLE - DATA_READY_EN 读写宏 */
#define ADVANCED_REGFILE_GET_INT_ENABLE_DATA_READY_EN(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_INT_ENABLE_DATA_READY_EN_MASK) >> 0U)
    
#define ADVANCED_REGFILE_SET_INT_ENABLE_DATA_READY_EN(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_INT_ENABLE_DATA_READY_EN_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* INT_ENABLE - ERROR_EN 读写宏 */
#define ADVANCED_REGFILE_GET_INT_ENABLE_ERROR_EN(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_INT_ENABLE_ERROR_EN_MASK) >> 1U)
    
#define ADVANCED_REGFILE_SET_INT_ENABLE_ERROR_EN(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_INT_ENABLE_ERROR_EN_MASK) | \
    (((value) ? 1U : 0U) << 1U))
/* INT_ENABLE - TIMEOUT_EN 读写宏 */
#define ADVANCED_REGFILE_GET_INT_ENABLE_TIMEOUT_EN(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_INT_ENABLE_TIMEOUT_EN_MASK) >> 2U)
    
#define ADVANCED_REGFILE_SET_INT_ENABLE_TIMEOUT_EN(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_INT_ENABLE_TIMEOUT_EN_MASK) | \
    (((value) ? 1U : 0U) << 2U))
/* INT_ENABLE - FIFO_FULL_EN 读写宏 */
#define ADVANCED_REGFILE_GET_INT_ENABLE_FIFO_FULL_EN(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_INT_ENABLE_FIFO_FULL_EN_MASK) >> 3U)
    
#define ADVANCED_REGFILE_SET_INT_ENABLE_FIFO_FULL_EN(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_INT_ENABLE_FIFO_FULL_EN_MASK) | \
    (((value) ? 1U : 0U) << 3U))
/* INT_ENABLE - FIFO_EMPTY_EN 读写宏 */
#define ADVANCED_REGFILE_GET_INT_ENABLE_FIFO_EMPTY_EN(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_INT_ENABLE_FIFO_EMPTY_EN_MASK) >> 4U)
    
#define ADVANCED_REGFILE_SET_INT_ENABLE_FIFO_EMPTY_EN(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_INT_ENABLE_FIFO_EMPTY_EN_MASK) | \
    (((value) ? 1U : 0U) << 4U))
/* CONFIG - CLK_DIV 读写宏 */
#define ADVANCED_REGFILE_GET_CONFIG_CLK_DIV(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_CONFIG_CLK_DIV_MASK) >> 0U)
    
#define ADVANCED_REGFILE_SET_CONFIG_CLK_DIV(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_CONFIG_CLK_DIV_MASK) | \
    (((value) << 0U) & ADVANCED_REGFILE_CONFIG_CLK_DIV_MASK))
/* CONFIG - FIFO_THR 读写宏 */
#define ADVANCED_REGFILE_GET_CONFIG_FIFO_THR(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_CONFIG_FIFO_THR_MASK) >> 8U)
    
#define ADVANCED_REGFILE_SET_CONFIG_FIFO_THR(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_CONFIG_FIFO_THR_MASK) | \
    (((value) << 8U) & ADVANCED_REGFILE_CONFIG_FIFO_THR_MASK))
/* CONFIG - TIMEOUT_VAL 读写宏 */
#define ADVANCED_REGFILE_GET_CONFIG_TIMEOUT_VAL(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_CONFIG_TIMEOUT_VAL_MASK) >> 16U)
    
#define ADVANCED_REGFILE_SET_CONFIG_TIMEOUT_VAL(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_CONFIG_TIMEOUT_VAL_MASK) | \
    (((value) << 16U) & ADVANCED_REGFILE_CONFIG_TIMEOUT_VAL_MASK))
/* CONFIG - AUTO_MODE 读写宏 */
#define ADVANCED_REGFILE_GET_CONFIG_AUTO_MODE(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_CONFIG_AUTO_MODE_MASK) >> 24U)
    
#define ADVANCED_REGFILE_SET_CONFIG_AUTO_MODE(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_CONFIG_AUTO_MODE_MASK) | \
    (((value) ? 1U : 0U) << 24U))
/* LOCK_REG - LOCK_KEY 读写宏 */
#define ADVANCED_REGFILE_GET_LOCK_REG_LOCK_KEY(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_LOCK_REG_LOCK_KEY_MASK) >> 0U)
    
#define ADVANCED_REGFILE_SET_LOCK_REG_LOCK_KEY(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_LOCK_REG_LOCK_KEY_MASK) | \
    (((value) << 0U) & ADVANCED_REGFILE_LOCK_REG_LOCK_KEY_MASK))
/* VER_REG - MINOR_VER 读写宏 */
#define ADVANCED_REGFILE_GET_VER_REG_MINOR_VER(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_VER_REG_MINOR_VER_MASK) >> 0U)
    
#define ADVANCED_REGFILE_SET_VER_REG_MINOR_VER(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_VER_REG_MINOR_VER_MASK) | \
    (((value) << 0U) & ADVANCED_REGFILE_VER_REG_MINOR_VER_MASK))
/* VER_REG - MAJOR_VER 读写宏 */
#define ADVANCED_REGFILE_GET_VER_REG_MAJOR_VER(reg_val)  \
    (((reg_val) & ADVANCED_REGFILE_VER_REG_MAJOR_VER_MASK) >> 16U)
    
#define ADVANCED_REGFILE_SET_VER_REG_MAJOR_VER(reg_val, value)  \
    (((reg_val) & ~ADVANCED_REGFILE_VER_REG_MAJOR_VER_MASK) | \
    (((value) << 16U) & ADVANCED_REGFILE_VER_REG_MAJOR_VER_MASK))

/* 寄存器类型定义 */
typedef struct {
    uint32_t ctrl_reg;  /**< 主控寄存器 */
    uint32_t status_reg;  /**< 状态寄存器 */
    uint32_t int_flags;  /**< 中断标志寄存器，读取后自动清零 */
    uint32_t int_enable;  /**< 中断使能寄存器 */
    uint32_t int_clear;  /**< 中断清除寄存器，写1清零对应位 */
    uint32_t int_set;  /**< 中断设置寄存器，写1置位对应位 */
    uint32_t tx_data;  /**< 发送数据寄存器，只能写入 */
    uint32_t rx_data;  /**< 接收数据寄存器，只能读取 */
    uint32_t config;  /**< 配置寄存器 */
    uint32_t lock_reg;  /**< 锁定寄存器，只能写入一次 */
    uint32_t stat_count;  /**< 统计计数器，读取后自动置位 */
    uint32_t w0c_reg;  /**< 写0清零寄存器，写0清零对应位 */
    uint32_t w0s_reg;  /**< 写0置位寄存器，写0置位对应位 */
    uint32_t tog_reg;  /**< 翻转寄存器，写1翻转对应位 */
    uint32_t ver_reg;  /**< 版本信息寄存器 */
} advanced_regfile_regs_t;

#ifdef __cplusplus
}
#endif

#endif /* ADVANCED_REGFILE_H */ 