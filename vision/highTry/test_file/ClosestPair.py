import sys

# 定义一个函数来计算两点之间的欧几里得距离
def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

# 定义一个函数来找到一组点中的最近点对
def closest_pair(points, left, right):
    # 当点的数量少于等于3时，直接使用暴力方法计算最小距离
    if right - left <= 3:
        return brute_force(points[left:right + 1])

    # 找到中点，将点集分成两部分
    mid = (left + right) // 2
    p1 = points[left:mid + 1]
    p2 = points[mid + 1:right + 1]

    # 递归地在两个子集中找到最近点对
    d1, pair1 = closest_pair(points, left, mid)
    d2, pair2 = closest_pair(points, mid + 1, right)
    d_min = min(d1, d2)
    best_pair = pair1 if d1 <= d2 else pair2

    # 合并两个子集，并找到横跨中点的最近点对
    merge_points = merge(p1, p2)
    d_strip, strip_pair = closest_in_strip(merge_points, d_min)
    if d_strip < d_min:
        d_min = d_strip
        best_pair = strip_pair

    return d_min, best_pair

# 合并两个子集的函数
def merge(p1, p2):
    # 合并两个列表，并按照y坐标排序
    return sorted(p1 + p2, key=lambda x: x[1])

# 找到横跨中点的最近点对的函数
def closest_in_strip(points, d_min):
    # 按照x坐标排序
    points = sorted(points, key=lambda x: x[0])
    d = d_min
    best_pair = None

    # 遍历每个点，找到横跨中点的最近点对
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if points[j][0] - points[i][0] >= d:
                break
            if dist(points[i], points[j]) < d:
                d = dist(points[i], points[j])
                best_pair = (points[i], points[j])

    return d, best_pair

# 暴力方法计算最近点对的函数
def brute_force(points):
    # 初始化最小距离为无穷大
    min_dist = sys.float_info.max
    best_pair = None
    # 计算所有点对的距离，找出最小值
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if dist(points[i], points[j]) < min_dist:
                min_dist = dist(points[i], points[j])
                best_pair = (points[i], points[j])
    # 返回最小距离和最近点对
    return min_dist, best_pair

# 示例使用
points = [(1, 2), (3, 4), (2, 3), (5, 1), (7, 7), (9, 1), (3, 5)]
distance, pair = closest_pair(points, 0, len(points) - 1)
print("The closest pair is:", pair)