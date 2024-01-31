import time
import numpy as np
from scipy.optimize import linear_sum_assignment


def markM(mat):
    current = mat
    count_row = mat.shape[0]

    # попытка образовать паросочетание
    row_ind, col_ind = linear_sum_assignment(mat)
    marked_zero = np.column_stack((row_ind, col_ind))[mat[row_ind, col_ind] == 0]
    # marked_zero = []
    # added_rows = set()
    # for i in range(len(row_ind)):
    #     for j in range(len(col_ind)):
    #         r, c = row_ind[i], col_ind[i]
    #         if mat[r][c] == 0 and (r, c) not in marked_zero and r not in added_rows:
    #             marked_zero.append((r, c))
    #             added_rows.add(r)

    if marked_zero.shape[0] == count_row:
        marked_rows = np.arange(count_row)
        marked_columns = np.array([], dtype=int)
        return (marked_zero, marked_rows, marked_columns)

    # вычёркивание всех нулей за минимально количество вычёркиваний
    marked_row = []
    marked_column = []
    zeroM = (current == 0)
    for i in range(len(marked_zero)):
        marked_row.append(marked_zero[i][0])
        marked_column.append(marked_zero[i][1])
    n_marked_row = list(set(range(current.shape[0])) - set(marked_row))
    marked_columns = []
    check = True
    while check:
        check = False
        for i in range(len(n_marked_row)):
            row_array = zeroM[n_marked_row[i], :]
            for j in range(row_array.shape[0]):
                if row_array[j] == True and j not in marked_columns:
                    marked_columns.append(j)
                    check = True

        for row_num, col_num in marked_zero:
            if row_num not in n_marked_row and col_num in marked_columns:
                n_marked_row.append(row_num)
                check = True
    marked_rows = list(set(range(mat.shape[0])) - set(n_marked_row))
    return (marked_zero, marked_rows, marked_columns)


def adjust_matrix(mat, cover_rows, cover_columns):
    current = mat.copy()
    n_zero_element = []
    # создание массива из чисел, которые остались невычеркнуты
    for row in range(len(current)):
        if row not in cover_rows:
            for i in range(len(current[row])):
                if i not in cover_columns:
                    n_zero_element.append(current[row][i])
    min_num = min(n_zero_element)
    # вычитание минимального элемента среди невычеркнутых чисел из всех этих чисел
    for row in range(len(current)):
        if row not in cover_rows:
            for i in range(len(current[row])):
                if i not in cover_columns:
                    current[row, i] = current[row, i] - min_num
    # прибавление минимального элемента ко всем элементам, которые находятся на пересечении вычёркивания столбцов и строк
    for row in range(len(cover_rows)):
        for col in range(len(cover_columns)):
            current[cover_rows[row], cover_columns[col]] = current[cover_rows[row], cover_columns[col]] + min_num
    return current


def hungarian_algorithm(mat):
    count_row = mat.shape[0]
    cur_mat = mat
    # вычитание минимального элемента из каждой строки матрицы и проверка на паросочетание
    for row_num in range(mat.shape[0]):
        cur_mat[row_num] = cur_mat[row_num] - np.min(cur_mat[row_num])
    ans_pos, marked_rows, marked_cols = markM(cur_mat)
    zero_count = len(ans_pos)
    if zero_count == count_row:
        return ans_pos
    else:
        # вычитание минимального элемента из каждого столбца матрицы и проверка на паросочетание
        for col_num in range(mat.shape[1]):
            cur_mat[:, col_num] = cur_mat[:, col_num] - np.min(cur_mat[:, col_num])
        ans_pos, marked_rows, marked_cols = markM(cur_mat)
        zero_count = len(ans_pos)
        if zero_count == count_row:
            return ans_pos
        else:
            # вычёркивание строк и столбцов матрицы до тех пор, пока не будет найдено паросочетание
            zero_count = 0
            while zero_count < count_row:
                ans_pos, marked_rows, marked_cols = markM(cur_mat)
                zero_count = len(ans_pos)
                if zero_count < count_row:
                    cur_mat = adjust_matrix(cur_mat, marked_rows, marked_cols)
            return ans_pos


def calculating_summ(mat, pos):
    total = 0
    for i in range(len(pos)):
        total += mat[pos[i][0], pos[i][1]]
    return total


with open("matrix.csv", "r") as f:
    lines = f.readlines()

matrix = []
for line in lines:
    row = list(map(int, line.strip().split()))
    matrix.append(row)


start = time.time()
start_matrix = np.array(matrix)
input_matrix = np.array(matrix)
# start_matrix = np.array([[7,8,8,6,6,9],
#                         [10,3,9,6,5,5],
#                         [8,6,1,9,7,2],
#                         [2,10,9,2,3,6]])
# input_matrix = np.array([[7,8,8,6,6,9],
#                         [10,3,9,6,5,5],
#                         [8,6,1,9,7,2],
#                         [2,10,9,2,3,6]])
for i in range(input_matrix.shape[0]):
    max_value = np.max(input_matrix[i])
    input_matrix[i] = input_matrix[i] - max_value

cost_matrix = -1 * input_matrix
count_row = cost_matrix.shape[0]
answ_pos, marked_rows, marked_cols = markM(cost_matrix)
zero_count = len(answ_pos)
if zero_count == count_row:
    otvet = answ_pos
    print("Pairs of elements in the maximum matching:")
    for row, col in otvet:
        print(f"({row}, {col})")
    answer = calculating_summ(start_matrix, answ_pos)
    print(f"The value of the maximum matching >>>> {answer}")
    print(f"Program was completed >>>> {time.time() - start} seconds")
else:
    ans_pos = hungarian_algorithm(cost_matrix.copy())
    print("Pairs of elements in the maximum matching:")
    for row, col in ans_pos:
        print(f"({row}, {col})")
    ans = calculating_summ(start_matrix, ans_pos)
    print(f"The value of the maximum matching >>>> {ans}")
    print(f"Program was completed >>>> {time.time()-start} seconds")