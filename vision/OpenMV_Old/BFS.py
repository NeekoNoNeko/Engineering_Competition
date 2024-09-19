from ulab import numpy as np
#from collections import deque
import collections
#class Solution:

    #定义了 Solution 类中的一个方法 updateMatrix，它接受一个二维列表 matrix 作为参数，并返回一个同样大小的二维列表 dist。
class Solution:
#    def updateMatrix(self, matrix: List[List[int]]) -> List[List[int]]:
    def updateMatrix(self, matrix):

        m, n = len(matrix), len(matrix[0])   #获取输入矩阵的行数和列数，分别存储在变量 m 和 n 中
        dist = [[0] * n for _ in range(m)]  #创建一个与输入矩阵同样大小的二维列表 dist，初始化所有元素为0。
        zeroes_pos = [(i, j) for i in range(m) for j in range(n) if matrix[i][j] == 0]
        # 将所有的 0 添加进初始队列中,使用列表推导式找出矩阵中所有值为0的元素的位置，并存储在列表 zeroes_pos 中。
        print("yes")

        q = zeroes_pos[:]#将 zeroes_pos 中的元素添加到 collections.deque 对象 q 中，这是一个双端队列，用于实现广度优先搜索。
        seen = set(zeroes_pos)  #将 zeroes_pos 中的元素添加到集合 seen 中，用于记录已经访问过的元素。

        # 广度优先搜索
        while q:         #开始一个循环，只要队列 q 中还有元素，就继续执行循环。
            i, j = q.pop(0) #从队列 q 中弹出（即移除并返回）第一个元素，即当前要处理的元素的行索引 i 和列索引 j。
            for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]: #对当前元素的四个相邻元素（上、下、左、右）进行遍历。
                if 0 <= ni < m and 0 <= nj < n and (ni, nj) not in seen:  #检查相邻元素是否在矩阵范围内，并且是否尚未被访问过。
                    dist[ni][nj] = dist[i][j] + 1   #如果满足条件，将该相邻元素在 dist 矩阵中对应的值设置为当前元素的 dist 值加1，表示从最近的0到这个位置的距离。
                    q.append((ni, nj))    #将满足条件的相邻元素添加到队列 q 的末尾，以便后续处理。
                    seen.add((ni, nj))   #将新访问的元素添加到 seen 集合中，以避免重复访问。

        return dist  #在所有元素都被处理后，返回最终的 dist 矩阵。

mat = np.array([
    [1, 1, 0, 1, 1],
    [0, 1, 1, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0]
])

mat = mat.tolist()
solutions = Solution()

# 计算距离矩阵
distance_matrix = solutions.updateMatrix(mat)
distance_matrix = np.array(distance_matrix, dtype=np.uint8)
print(distance_matrix)
print(type(distance_matrix))
