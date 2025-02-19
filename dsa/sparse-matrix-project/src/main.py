import re
import os

class SparseMatrix:
    def __init__(self, matrix_file_path=None, num_rows=None, num_cols=None):
        if matrix_file_path:
            self.num_rows, self.num_cols, self.elements = self._read_matrix_from_file(matrix_file_path)
        else:
            self.num_rows = num_rows
            self.num_cols = num_cols
            self.elements = {}

    def _read_matrix_from_file(self, matrix_file_path):
        elements = {}
        try:
            with open(matrix_file_path, 'r') as file:
                lines = file.readlines()
                # Read matrix dimensions
                num_rows = int(lines[0].split('=')[1].strip())
                num_cols = int(lines[1].split('=')[1].strip())
                # Read non-zero elements
                for line in lines[2:]:
                    if line.strip():
                        row, col, value = self._parse_entry(line.strip())
                        elements[(row, col)] = value
        except Exception as e:
            raise ValueError(f"Input file has wrong format: {e}")
        return num_rows, num_cols, elements

    def _parse_entry(self, entry):
        try:
            entry = entry.strip('()')
            row, col, value = map(int, entry.split(','))
            return row, col, value
        except Exception as e:
            raise ValueError(f"Invalid entry format: {entry}. Expected format: (row,col,value)")

    def get_element(self, curr_row, curr_col):
        return self.elements.get((curr_row, curr_col), 0)

    def set_element(self, curr_row, curr_col, value):
        if value != 0:
            self.elements[(curr_row, curr_col)] = value
        elif (curr_row, curr_col) in self.elements:
            del self.elements[(curr_row, curr_col)]

    def __str__(self):
        result = [f"rows={self.num_rows}", f"cols={self.num_cols}"]
        for (row, col), value in sorted(self.elements.items()):
            result.append(f"({row}, {col}, {value})")
        return '\n'.join(result)

    def __add__(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices dimensions do not match for addition")
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        # Add elements from self
        for key, value in self.elements.items():
            result.set_element(key[0], key[1], value + other.get_element(key[0], key[1]))
        # Add elements from other that are not in self
        for key, value in other.elements.items():
            if key not in self.elements:
                result.set_element(key[0], key[1], value)
        return result

    def __sub__(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices dimensions do not match for subtraction")
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        # Subtract elements from self
        for key, value in self.elements.items():
            result.set_element(key[0], key[1], value - other.get_element(key[0], key[1]))
        # Subtract elements from other that are not in self
        for key, value in other.elements.items():
            if key not in self.elements:
                result.set_element(key[0], key[1], -value)
        return result

    def __mul__(self, other):
        if self.num_cols != other.num_rows:
            raise ValueError("Matrices dimensions do not match for multiplication")
        result = SparseMatrix(num_rows=self.num_rows, num_cols=other.num_cols)
        # Precompute non-zero columns in the second matrix
        other_non_zero_cols = {}
        for (k, j), value in other.elements.items():
            if k not in other_non_zero_cols:
                other_non_zero_cols[k] = []
            other_non_zero_cols[k].append(j)
        # Perform multiplication
        for (i, k), value1 in self.elements.items():
            if k in other_non_zero_cols:
                for j in other_non_zero_cols[k]:
                    value2 = other.get_element(k, j)
                    result.set_element(i, j, result.get_element(i, j) + value1 * value2)
        return result


def read_matrix_file(file_path):
    """Read a sparse matrix from a file and return a SparseMatrix object."""
    return SparseMatrix(matrix_file_path=file_path)


def write_matrix_to_file(matrix, file_path):
    """Write the string representation of a SparseMatrix to a file."""
    with open(file_path, 'w') as file:
        file.write(str(matrix))


def list_matrix_files(input_dir):
    """List all matrix files in the input directory."""
    matrix_files = [f for f in os.listdir(input_dir) if f.startswith('matrix') and f.endswith('.txt')]
    if not matrix_files:
        print("No matrix files found in the input directory.")
        return None
    return matrix_files


def select_matrix(input_dir, matrix_files, recommended_indices=None):
    """Let the user select a matrix from the list of available files."""
    print("Available matrix files:")
    for i, file in enumerate(matrix_files):
        recommendation = " (recommended)" if recommended_indices and i in recommended_indices else ""
        print(f"{i + 1}. {file}{recommendation}")
    try:
        choice = int(input("Select a matrix (by number): ")) - 1
        if choice < 0 or choice >= len(matrix_files):
            print("Invalid selection. Please choose a number from the list.")
            return None
        return os.path.join(input_dir, matrix_files[choice])
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


def perform_addition(input_dir, output_dir):
    """Perform matrix addition."""
    matrix_files = list_matrix_files(input_dir)
    if not matrix_files:
        return

    # Recommend matrices with the same dimensions
    recommended_indices = []
    for i, file1 in enumerate(matrix_files):
        matrix1 = read_matrix_file(os.path.join(input_dir, file1))
        for j, file2 in enumerate(matrix_files):
            if i != j:
                matrix2 = read_matrix_file(os.path.join(input_dir, file2))
                if matrix1.num_rows == matrix2.num_rows and matrix1.num_cols == matrix2.num_cols:
                    recommended_indices.append(i)
                    recommended_indices.append(j)

    print("\nSelect matrices for addition:")
    matrix1_file = select_matrix(input_dir, matrix_files, recommended_indices)
    matrix2_file = select_matrix(input_dir, matrix_files, recommended_indices)

    if not matrix1_file or not matrix2_file:
        return

    matrix1 = read_matrix_file(matrix1_file)
    matrix2 = read_matrix_file(matrix2_file)

    if matrix1.num_rows != matrix2.num_rows or matrix1.num_cols != matrix2.num_cols:
        print("Addition Error: Matrices dimensions do not match for addition")
        return

    try:
        result_add = matrix1 + matrix2
        print("\nAddition Result:")
        print(result_add)
        write_matrix_to_file(result_add, os.path.join(output_dir, 'result_addition.txt'))
    except ValueError as e:
        print(f"Addition Error: {e}")


def perform_subtraction(input_dir, output_dir):
    """Perform matrix subtraction."""
    matrix_files = list_matrix_files(input_dir)
    if not matrix_files:
        return

    # Recommend matrices with the same dimensions
    recommended_indices = []
    for i, file1 in enumerate(matrix_files):
        matrix1 = read_matrix_file(os.path.join(input_dir, file1))
        for j, file2 in enumerate(matrix_files):
            if i != j:
                matrix2 = read_matrix_file(os.path.join(input_dir, file2))
                if matrix1.num_rows == matrix2.num_rows and matrix1.num_cols == matrix2.num_cols:
                    recommended_indices.append(i)
                    recommended_indices.append(j)

    print("\nSelect matrices for subtraction:")
    matrix1_file = select_matrix(input_dir, matrix_files, recommended_indices)
    matrix2_file = select_matrix(input_dir, matrix_files, recommended_indices)

    if not matrix1_file or not matrix2_file:
        return

    matrix1 = read_matrix_file(matrix1_file)
    matrix2 = read_matrix_file(matrix2_file)

    if matrix1.num_rows != matrix2.num_rows or matrix1.num_cols != matrix2.num_cols:
        print("Subtraction Error: Matrices dimensions do not match for subtraction")
        return

    try:
        result_sub = matrix1 - matrix2
        print("\nSubtraction Result:")
        print(result_sub)
        write_matrix_to_file(result_sub, os.path.join(output_dir, 'result_subtraction.txt'))
    except ValueError as e:
        print(f"Subtraction Error: {e}")


def perform_multiplication(input_dir, output_dir):
    """Perform matrix multiplication."""
    matrix_files = list_matrix_files(input_dir)
    if not matrix_files:
        return

    # Recommend matrices with switched dimensions
    recommended_indices = []
    for i, file1 in enumerate(matrix_files):
        matrix1 = read_matrix_file(os.path.join(input_dir, file1))
        for j, file2 in enumerate(matrix_files):
            if i != j:
                matrix2 = read_matrix_file(os.path.join(input_dir, file2))
                if matrix1.num_cols == matrix2.num_rows:
                    recommended_indices.append(i)
                    recommended_indices.append(j)

    print("\nSelect matrices for multiplication:")
    matrix1_file = select_matrix(input_dir, matrix_files, recommended_indices)
    matrix2_file = select_matrix(input_dir, matrix_files, recommended_indices)

    if not matrix1_file or not matrix2_file:
        return

    matrix1 = read_matrix_file(matrix1_file)
    matrix2 = read_matrix_file(matrix2_file)

    if matrix1.num_cols != matrix2.num_rows:
        print("Multiplication Error: Matrices dimensions do not match for multiplication")
        return

    try:
        result_mul = matrix1 * matrix2
        print("\nMultiplication Result:")
        print(result_mul)
        write_matrix_to_file(result_mul, os.path.join(output_dir, 'result_multiplication.txt'))
    except ValueError as e:
        print(f"Multiplication Error: {e}")


def main():
    # Define the directory for input files
    input_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../sample_inputs/'))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../results/'))

    # Ensure the input directory exists
    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        return

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Let the user choose the operation
    print("Choose an operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    try:
        operation = int(input("Enter the operation number: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    if operation == 1:
        perform_addition(input_dir, output_dir)
    elif operation == 2:
        perform_subtraction(input_dir, output_dir)
    elif operation == 3:
        perform_multiplication(input_dir, output_dir)

if __name__ == "__main__":
    main()
