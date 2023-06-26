import numpy as np

A = np.array([[1, 0, 0], [0, 0.3, 0], [0, -0.24, 0.3], [0, -0.078, -0.24]])
print("A:", A)

Y = np.array([[0.3], [-0.24], [-0.078], [0.2784]])
print("Y:", Y)

B = np.matmul(A.T, A)

B = np.linalg.inv(B)

C = np.matmul(A.T, Y)

D = np.matmul(B, C)

print("D:", D)