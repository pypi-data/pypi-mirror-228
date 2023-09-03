from .fea_distribution import FeatureDistribution
from .line_chart_percent import LineChartPercent
from .line_chart_percent_kde import LineChartPercentKde
from .line_chart_percent_hue import LineChartPercentHue
from .line_chart_percent_2group import LineChartPercent2Group
from .heat_map_percent import HeatMapPercent
from .sankey import Sankey, SankeyOne

# 下面需要
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ['SimHei']
plt.rcParams["axes.unicode_minus"] = False
