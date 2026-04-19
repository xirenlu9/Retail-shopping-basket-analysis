# 商品零售购物篮分析 (Market Basket Analysis)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

这是一个基于 Apriori 算法的商品零售购物篮分析项目。通过分析超市零售数据，挖掘商品之间的关联规则，为商场的商品陈列、库存管理和捆绑销售提供数据支持。

## 📖 项目简介

关联规则分析（Market Basket Analysis）是数据挖掘中的经典案例。本项目通过对 `GoodsOrder.csv` 和 `GoodsTypes.csv` 数据集的处理与分析，实现了以下目标：
1.  **数据探索性分析 (EDA)**：分析商品销售频率、各类别商品销售占比。
2.  **关联规则挖掘**：利用 `apyori` 库实现 Apriori 算法，挖掘高频项集和关联规则。
3.  **结果可视化**：通过柱状图、饼图直观展示分析结果。
4.  **业务洞察**：根据提升度（Lift）和置信度（Confidence）提供实际的业务建议。

## ✨ 功能特性

-   **销量排名分析**：自动统计并可视化销量前十的商品。
-   **类别占比分析**：多层次分析商品大类及细分类别的销售分布。
-   **深度关联挖掘**：基于支持度、置信度和提升度筛选有价值的关联规则。
-   **可配置性**：灵活调整 Apriori 算法的参数以适应不同规模的数据集。

## 📂 项目结构

```text
.
├── data/               # 原始数据集 (CSV)
├── docs/               # 项目文档与 PDF 说明
│   └── images/         # 自动生成的分析图表
├── src/                # 源代码
│   └── main.py         # 主分析脚本
├── .gitignore          # 忽略文件配置
├── LICENSE             # MIT 许可证
├── README.md           # 项目说明文档
└── requirements.txt    # 依赖库列表
```

## 🚀 快速开始

### 1. 环境准备

确保您的系统中已安装 Python 3.7+。克隆项目后，安装依赖项：

```bash
pip install -r requirements.txt
```

### 2. 运行分析

在项目根目录下运行主脚本：

```bash
python src/main.py
```

脚本将自动读取 `data/` 中的数据，执行分析过程，并将生成的可视化图表保存至 `docs/images/` 目录下。

## 📊 分析示例

### 商品销量排名
![商品销量排名](docs/images/商品销量排名水平柱状图.png)

### 类别销售占比
![各类别商品销售占比](docs/images/各类别商品销售占比饼图.png)

### 关联规则示例
输出示例：
```text
酸奶,其他蔬菜 --> ['全脂牛奶']
支持度：0.02 置信度：0.51 提升度：2.01
----------------------------------------
```

## 🤝 贡献指南

我们欢迎任何形式的贡献！如果您有好的建议或发现了 Bug，请：
1.  提交 Issue 描述问题。
2.  Fork 本仓库并提交 Pull Request。

详情请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 📜 开源许可证

本项目采用 [MIT License](LICENSE) 开源。

---
**免责声明**：本项目所使用的数据集仅用于学术研究和教学演示，请勿用于商业用途。
