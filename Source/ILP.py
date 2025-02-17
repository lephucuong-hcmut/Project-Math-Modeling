
import numpy as np
from numpy import linalg as LA
# Tạo ma trận A
A = np.array([[1, 2, 3],
              [4, 5, 6]])

# Thực hiện SVD
U, S, VT = np.linalg.svd(A)

# Chuyển đổi S thành ma trận chéo
Sigma = np.zeros((U.shape[0], VT.shape[0]))
np.fill_diagonal(Sigma, S)

# In kết quả
print("Ma trận U:")
print(U)
print("\nMa trận Sigma:")
print(Sigma)
print("\nMa trận V^T:")
print(VT)