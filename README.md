# dielectric_processor

## 环境要求
- Python 3.x
- numpy

## 使用方法
- 将 dielectric_processor.py 和同一样品不同温度段需要合并处理的介温谱 txt 文件置于同一目录
- 设置厚度、电极面积等关键参数
- 运行 dielectric_processor.py

你将得到以下参数相对于温度和频率的矩阵：
1. 介电常数 (permittivity)
2. 介电损耗 (loss)
3. 电阻率 Z'
4. 容抗率 -Z''

## 已实现功能
- 合并不同温度段数据时，后一段 (高温) 数据按照相同温度下的值等比例校正至前一段数据；
- 有重叠的温度段时，以后一段 (高温) 为准。
