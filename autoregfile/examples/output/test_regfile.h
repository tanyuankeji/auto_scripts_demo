/**
 * @file test_regfile.h
 * @brief 自动生成的寄存器定义头文件
 * @note 生成时间: 2025-03-24 19:53:08
 * @version 2.0.0
 */

#ifndef TEST_REGFILE_H
#define TEST_REGFILE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* 寄存器地址定义 */
#define TEST_REGFILE_CTRL_REG_ADDR      0x0U  /**< 控制寄存器 */
#define TEST_REGFILE_STATUS_REG_ADDR      0x0U  /**< 状态寄存器 */
#define TEST_REGFILE_INT_EN_REG_ADDR      0x0U  /**< 中断使能寄存器 */
#define TEST_REGFILE_INT_STATUS_REG_ADDR      0x0U  /**< 中断状态寄存器，写1清零 */
#define TEST_REGFILE_VERSION_REG_ADDR      0x0U  /**< 版本寄存器 */
#define TEST_REGFILE_CONFIG_REG_ADDR      0x0U  /**< 配置寄存器，只能写入一次 */

/* 寄存器位宽定义 */
#define TEST_REGFILE_DATA_WIDTH     32U
#define TEST_REGFILE_ADDR_WIDTH     8U

/* 寄存器位域定义 */
/* CTRL_REG - ENABLE */
#define TEST_REGFILE_CTRL_REG_ENABLE_POS      0U
#define TEST_REGFILE_CTRL_REG_ENABLE_MASK     (1U << 0U)
/* CTRL_REG - MODE */
#define TEST_REGFILE_CTRL_REG_MODE_POS      1U
#define TEST_REGFILE_CTRL_REG_MODE_MASK     (0x3U << 1U)
/* CTRL_REG - RESET */
#define TEST_REGFILE_CTRL_REG_RESET_POS      3U
#define TEST_REGFILE_CTRL_REG_RESET_MASK     (1U << 3U)
/* STATUS_REG - BUSY */
#define TEST_REGFILE_STATUS_REG_BUSY_POS      0U
#define TEST_REGFILE_STATUS_REG_BUSY_MASK     (1U << 0U)
/* STATUS_REG - ERROR */
#define TEST_REGFILE_STATUS_REG_ERROR_POS      1U
#define TEST_REGFILE_STATUS_REG_ERROR_MASK     (1U << 1U)
/* STATUS_REG - STATE */
#define TEST_REGFILE_STATUS_REG_STATE_POS      2U
#define TEST_REGFILE_STATUS_REG_STATE_MASK     (0xFU << 2U)
/* INT_EN_REG - DATA_READY_EN */
#define TEST_REGFILE_INT_EN_REG_DATA_READY_EN_POS      0U
#define TEST_REGFILE_INT_EN_REG_DATA_READY_EN_MASK     (1U << 0U)
/* INT_EN_REG - ERROR_EN */
#define TEST_REGFILE_INT_EN_REG_ERROR_EN_POS      1U
#define TEST_REGFILE_INT_EN_REG_ERROR_EN_MASK     (1U << 1U)
/* INT_EN_REG - TIMEOUT_EN */
#define TEST_REGFILE_INT_EN_REG_TIMEOUT_EN_POS      2U
#define TEST_REGFILE_INT_EN_REG_TIMEOUT_EN_MASK     (1U << 2U)
/* INT_STATUS_REG - DATA_READY */
#define TEST_REGFILE_INT_STATUS_REG_DATA_READY_POS      0U
#define TEST_REGFILE_INT_STATUS_REG_DATA_READY_MASK     (1U << 0U)
/* INT_STATUS_REG - ERROR */
#define TEST_REGFILE_INT_STATUS_REG_ERROR_POS      1U
#define TEST_REGFILE_INT_STATUS_REG_ERROR_MASK     (1U << 1U)
/* INT_STATUS_REG - TIMEOUT */
#define TEST_REGFILE_INT_STATUS_REG_TIMEOUT_POS      2U
#define TEST_REGFILE_INT_STATUS_REG_TIMEOUT_MASK     (1U << 2U)
/* VERSION_REG - MAJOR */
#define TEST_REGFILE_VERSION_REG_MAJOR_POS      16U
#define TEST_REGFILE_VERSION_REG_MAJOR_MASK     (0xFFFFU << 16U)
/* VERSION_REG - MINOR */
#define TEST_REGFILE_VERSION_REG_MINOR_POS      0U
#define TEST_REGFILE_VERSION_REG_MINOR_MASK     (0xFFFFU << 0U)
/* CONFIG_REG - DEVICE_ID */
#define TEST_REGFILE_CONFIG_REG_DEVICE_ID_POS      0U
#define TEST_REGFILE_CONFIG_REG_DEVICE_ID_MASK     (0xFFU << 0U)
/* CONFIG_REG - FEATURES */
#define TEST_REGFILE_CONFIG_REG_FEATURES_POS      8U
#define TEST_REGFILE_CONFIG_REG_FEATURES_MASK     (0xFFU << 8U)

/* 寄存器访问宏定义 */
/* CTRL_REG - ENABLE 读写宏 */
#define TEST_REGFILE_GET_CTRL_REG_ENABLE(reg_val)  \
    (((reg_val) & TEST_REGFILE_CTRL_REG_ENABLE_MASK) >> 0U)
    
#define TEST_REGFILE_SET_CTRL_REG_ENABLE(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_CTRL_REG_ENABLE_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* CTRL_REG - MODE 读写宏 */
#define TEST_REGFILE_GET_CTRL_REG_MODE(reg_val)  \
    (((reg_val) & TEST_REGFILE_CTRL_REG_MODE_MASK) >> 1U)
    
#define TEST_REGFILE_SET_CTRL_REG_MODE(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_CTRL_REG_MODE_MASK) | \
    (((value) << 1U) & TEST_REGFILE_CTRL_REG_MODE_MASK))
/* CTRL_REG - RESET 读写宏 */
#define TEST_REGFILE_GET_CTRL_REG_RESET(reg_val)  \
    (((reg_val) & TEST_REGFILE_CTRL_REG_RESET_MASK) >> 3U)
    
#define TEST_REGFILE_SET_CTRL_REG_RESET(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_CTRL_REG_RESET_MASK) | \
    (((value) ? 1U : 0U) << 3U))
/* STATUS_REG - BUSY 读写宏 */
#define TEST_REGFILE_GET_STATUS_REG_BUSY(reg_val)  \
    (((reg_val) & TEST_REGFILE_STATUS_REG_BUSY_MASK) >> 0U)
    
#define TEST_REGFILE_SET_STATUS_REG_BUSY(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_STATUS_REG_BUSY_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* STATUS_REG - ERROR 读写宏 */
#define TEST_REGFILE_GET_STATUS_REG_ERROR(reg_val)  \
    (((reg_val) & TEST_REGFILE_STATUS_REG_ERROR_MASK) >> 1U)
    
#define TEST_REGFILE_SET_STATUS_REG_ERROR(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_STATUS_REG_ERROR_MASK) | \
    (((value) ? 1U : 0U) << 1U))
/* STATUS_REG - STATE 读写宏 */
#define TEST_REGFILE_GET_STATUS_REG_STATE(reg_val)  \
    (((reg_val) & TEST_REGFILE_STATUS_REG_STATE_MASK) >> 2U)
    
#define TEST_REGFILE_SET_STATUS_REG_STATE(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_STATUS_REG_STATE_MASK) | \
    (((value) << 2U) & TEST_REGFILE_STATUS_REG_STATE_MASK))
/* INT_EN_REG - DATA_READY_EN 读写宏 */
#define TEST_REGFILE_GET_INT_EN_REG_DATA_READY_EN(reg_val)  \
    (((reg_val) & TEST_REGFILE_INT_EN_REG_DATA_READY_EN_MASK) >> 0U)
    
#define TEST_REGFILE_SET_INT_EN_REG_DATA_READY_EN(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_INT_EN_REG_DATA_READY_EN_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* INT_EN_REG - ERROR_EN 读写宏 */
#define TEST_REGFILE_GET_INT_EN_REG_ERROR_EN(reg_val)  \
    (((reg_val) & TEST_REGFILE_INT_EN_REG_ERROR_EN_MASK) >> 1U)
    
#define TEST_REGFILE_SET_INT_EN_REG_ERROR_EN(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_INT_EN_REG_ERROR_EN_MASK) | \
    (((value) ? 1U : 0U) << 1U))
/* INT_EN_REG - TIMEOUT_EN 读写宏 */
#define TEST_REGFILE_GET_INT_EN_REG_TIMEOUT_EN(reg_val)  \
    (((reg_val) & TEST_REGFILE_INT_EN_REG_TIMEOUT_EN_MASK) >> 2U)
    
#define TEST_REGFILE_SET_INT_EN_REG_TIMEOUT_EN(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_INT_EN_REG_TIMEOUT_EN_MASK) | \
    (((value) ? 1U : 0U) << 2U))
/* INT_STATUS_REG - DATA_READY 读写宏 */
#define TEST_REGFILE_GET_INT_STATUS_REG_DATA_READY(reg_val)  \
    (((reg_val) & TEST_REGFILE_INT_STATUS_REG_DATA_READY_MASK) >> 0U)
    
#define TEST_REGFILE_SET_INT_STATUS_REG_DATA_READY(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_INT_STATUS_REG_DATA_READY_MASK) | \
    (((value) ? 1U : 0U) << 0U))
/* INT_STATUS_REG - ERROR 读写宏 */
#define TEST_REGFILE_GET_INT_STATUS_REG_ERROR(reg_val)  \
    (((reg_val) & TEST_REGFILE_INT_STATUS_REG_ERROR_MASK) >> 1U)
    
#define TEST_REGFILE_SET_INT_STATUS_REG_ERROR(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_INT_STATUS_REG_ERROR_MASK) | \
    (((value) ? 1U : 0U) << 1U))
/* INT_STATUS_REG - TIMEOUT 读写宏 */
#define TEST_REGFILE_GET_INT_STATUS_REG_TIMEOUT(reg_val)  \
    (((reg_val) & TEST_REGFILE_INT_STATUS_REG_TIMEOUT_MASK) >> 2U)
    
#define TEST_REGFILE_SET_INT_STATUS_REG_TIMEOUT(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_INT_STATUS_REG_TIMEOUT_MASK) | \
    (((value) ? 1U : 0U) << 2U))
/* VERSION_REG - MAJOR 读写宏 */
#define TEST_REGFILE_GET_VERSION_REG_MAJOR(reg_val)  \
    (((reg_val) & TEST_REGFILE_VERSION_REG_MAJOR_MASK) >> 16U)
    
#define TEST_REGFILE_SET_VERSION_REG_MAJOR(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_VERSION_REG_MAJOR_MASK) | \
    (((value) << 16U) & TEST_REGFILE_VERSION_REG_MAJOR_MASK))
/* VERSION_REG - MINOR 读写宏 */
#define TEST_REGFILE_GET_VERSION_REG_MINOR(reg_val)  \
    (((reg_val) & TEST_REGFILE_VERSION_REG_MINOR_MASK) >> 0U)
    
#define TEST_REGFILE_SET_VERSION_REG_MINOR(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_VERSION_REG_MINOR_MASK) | \
    (((value) << 0U) & TEST_REGFILE_VERSION_REG_MINOR_MASK))
/* CONFIG_REG - DEVICE_ID 读写宏 */
#define TEST_REGFILE_GET_CONFIG_REG_DEVICE_ID(reg_val)  \
    (((reg_val) & TEST_REGFILE_CONFIG_REG_DEVICE_ID_MASK) >> 0U)
    
#define TEST_REGFILE_SET_CONFIG_REG_DEVICE_ID(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_CONFIG_REG_DEVICE_ID_MASK) | \
    (((value) << 0U) & TEST_REGFILE_CONFIG_REG_DEVICE_ID_MASK))
/* CONFIG_REG - FEATURES 读写宏 */
#define TEST_REGFILE_GET_CONFIG_REG_FEATURES(reg_val)  \
    (((reg_val) & TEST_REGFILE_CONFIG_REG_FEATURES_MASK) >> 8U)
    
#define TEST_REGFILE_SET_CONFIG_REG_FEATURES(reg_val, value)  \
    (((reg_val) & ~TEST_REGFILE_CONFIG_REG_FEATURES_MASK) | \
    (((value) << 8U) & TEST_REGFILE_CONFIG_REG_FEATURES_MASK))

/* 寄存器类型定义 */
typedef struct {
    uint32_t ctrl_reg;  /**< 控制寄存器 */
    uint32_t status_reg;  /**< 状态寄存器 */
    uint32_t int_en_reg;  /**< 中断使能寄存器 */
    uint32_t int_status_reg;  /**< 中断状态寄存器，写1清零 */
    uint32_t version_reg;  /**< 版本寄存器 */
    uint32_t config_reg;  /**< 配置寄存器，只能写入一次 */
} test_regfile_regs_t;

#ifdef __cplusplus
}
#endif

#endif /* TEST_REGFILE_H */ 