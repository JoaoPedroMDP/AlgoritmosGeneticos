import numpy as np

from convert_data import get_sorted_indexes, to_matrix, translate_matrix_values
from display_data import print_matrix_as_dataframe
from ga_qiEinstein import COLUMNS, ROWS, TRANSLATION_DICTS
from ga_qiEinstein.fit_func import fit


sol = np.array([1, 2, 5, 4, 3, 9, 7, 8, 6, 10, 11, 14, 15, 12, 13, 18, 16, 19, 20, 17, 23, 22, 24, 25, 21])
mtrx = to_matrix(sol, 5)
mtrx = [get_sorted_indexes(row) for row in mtrx]
translated = translate_matrix_values(mtrx, TRANSLATION_DICTS)
print_matrix_as_dataframe(translated, columns=COLUMNS, index=ROWS)
print(fit(sol))
