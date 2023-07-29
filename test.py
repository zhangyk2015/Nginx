# -*- Coding: UTF-8 -*-
# test.py
# @Author Zhangyk
# @CreatedDate 2023-04-27T00:05:01.081Z+08:00
# @LastModifiedDate 2023-06-13T19:58:53.367Z+08:00
#

# T2


def matrix_multiply(A, B):
    n = len(A)
    w = len(A[0])
    w1 = len(B)
    m = len(B[0])
    assert w == w1
    C = [[0 for j in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(w):
                C[i][j] += A[i][k] * B[k][j]
    return C


def matrix_dot(A, B):
    n = len(A)
    x = len(B)
    y = len(B[0])
    assert n == x
    C = [[0 for j in range(y)] for i in range(x)]
    for i in range(n):
        for j in range(y):
            C[i][j] = A[i] * B[i][j]
    return C


def matrix_reverse(A):
    n = len(A)
    m = len(A[0])
    B = [[0 for j in range(n)] for i in range(m)]
    for i in range(n):
        for j in range(m):
            B[j][i] = A[i][j]
    return B


if __name__ == "__main__":
    n, d = list(map(int, input().split()))
    Q = [[0 for j in range(d)] for i in range(n)]
    K = [[0 for j in range(d)] for i in range(n)]
    V = [[0 for j in range(d)] for i in range(n)]
    for i in range(n):
        Q[i] = list(map(int, input().split()))
    for i in range(n):
        K[i] = list(map(int, input().split()))
    for i in range(n):
        V[i] = list(map(int, input().split()))
    W = list(map(int, input().split()))
    Kt = matrix_reverse(K)
    KtV = matrix_multiply(Kt, V)
    QKtV = matrix_multiply(Q, KtV)
    res = matrix_dot(W, QKtV)
    for i in range(n):
        print(" ".join(str(i) for i in res[i]))
