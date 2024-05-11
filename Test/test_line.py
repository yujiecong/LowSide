import numpy as np
import matplotlib.pyplot as plt
def find_perpendicular_point(line_point1, line_point2, point_A, distance):
    x1, y1 = line_point1
    x2, y2 = line_point2
    x_A, y_A = point_A

    # 计算直线斜率
    slope = (y2 - y1) / (x2 - x1)

    # 计算垂直斜率
    perpendicular_slope = -1 / slope

    # 计算垂直线的截距
    intercept = y_A - perpendicular_slope * x_A

    # 根据点斜式计算垂直线方程
    def perpendicular_line_equation(x):
        return perpendicular_slope * x + intercept

    # 找到垂直线上距离点 A 3 个单位的点 B
    x_B = x_A + distance / np.sqrt(1 + perpendicular_slope**2)
    y_B = perpendicular_line_equation(x_B)

    return np.array([x_B, y_B])
def calculate_control_points(p0, p3):
    p1 = p0 + (p3 - p0) / 3.0
    p2 = p3 - (p3 - p0) / 3.0

    c1=find_perpendicular_point(p0, p3, p1, 3)
    c2=find_perpendicular_point(p0, p3, p2, -3)

    return c1,c2

def bezier_curve(t, p0, p1, p2, p3):
    u = 1 - t
    return u**3 * p0 + 3 * u**2 * t * p1 + 3 * u * t**2 * p2 + t**3 * p3

def plot_bezier_curve(p0, p3, distance_factor):
    p1, p2 = calculate_control_points(p0, p3)
    t_values = np.linspace(0, 1, 1000)
    curve_points = np.array([bezier_curve(t, p0, p1, p2, p3) for t in t_values])

    plt.plot(curve_points[:, 0], curve_points[:, 1], label='Bezier Curve')
    plt.scatter([p0[0], p1[0], p2[0], p3[0]], [p0[1], p1[1], p2[1], p3[1]], color='red', label='Control Points')
    plt.title('Bezier Curve with Automatic Control Points Calculation')
    plt.legend()
    plt.show()

# 测试
p0 = np.array([0, 0])
p3 = np.array([12, 13])
distance_factor = 0.01  # 调整距离因子

plot_bezier_curve(p0, p3, distance_factor)
