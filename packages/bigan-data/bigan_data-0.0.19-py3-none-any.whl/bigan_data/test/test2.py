import numpy as np

if __name__ == '__main__':
    factor = [[0, 0, 0, 0, 0, 0],
              [1.78, 1.76, 0.58, 0.85, 0.91, 2.29],
              [1.74, 1.94, 0.82, 0.86, 0.93, 1.79],
              [1.13, 2.86, 0.85, 0.87, 0.94, 2.45],
              [1.11, 2.65, 0.91, 0.88, 0.92, 2.38],
              [1.92, 2.18, 0.47, 0.82, 0.91, 2.57],
              [1.99, 2.32, 0.51, 0.83, 0.9, 2.22],
              [2.07, 1.87, 0.88, 0.98, 0.85, 2.36]]
    left = [[0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]]
    right = [0, 0, 0, 0, 0, 0]
    for j in range(2, 8):
        sum = 0
        for i in range(0, 6):
            print("v1i:" + str(factor[1][i]))
            print("v" + str(j) + "i:" + str(factor[j][i]))
            print("v1i-v" + str(j) + "i:" + str(factor[1][i] - factor[j][i]))
            left[j - 2][i] = 2 * (factor[1][i] - factor[j][i])
            sum += factor[1][i] * factor[1][i] - factor[j][i] * factor[j][i]
        print(sum)
        right[j - 2] = sum
    # np.linalg.solve
    a = np.array(left)
    b = np.array(right)
    print(np.linalg.solve(a, b))
    