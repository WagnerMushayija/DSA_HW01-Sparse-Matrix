
## Implementation in Python

### SparseMatrix Class
The `SparseMatrix` class handles the representation of a sparse matrix using a dictionary to store non-zero elements. This class includes methods for:
- Loading a matrix from a file.
- Performing addition, subtraction, and multiplication.
- Converting the matrix to a string format.

### Methods
- `__init__(self, matrix_file_path=None, num_rows=None, num_cols=None)`: Initializes the sparse matrix. If a file path is provided, it loads the matrix from the file.
- `_read_matrix_from_file(self, matrix_file_path)`: Reads the matrix dimensions and entries from a specified file.
- `_parse_entry(self, entry)`: Parses a matrix entry from a string format.
- `get_element(self, curr_row, curr_col)`: Returns the value at the specified position in the matrix.
- `set_element(self, curr_row, curr_col, value)`: Sets the value at the specified position in the matrix.
- `__str__(self)`: Converts the matrix to a string format.
- `__add__(self, other)`: Adds two matrices.
- `__sub__(self, other)`: Subtracts one matrix from another.
- `__mul__(self, other)`: Multiplies two matrices.

### Main Function
The `main` function demonstrates how to create sparse matrices from files and perform operations on them. It also handles user input for selecting the operation and the matrices to use.

### Main Function
The `main` function demonstrates how to create sparse matrices from files and perform operations on them. It also handles user input for selecting the operation and the matrices to use.

### Error Handling
The code includes error handling for:
- Incorrect file formats.
- Dimension mismatches during operations.

### Testing
Create sample input files in the `/sample_inputs/` directory to test the implementation. Ensure that the files follow the specified format.

### Why Subtraction Might Give Zero Data
If the subtraction operation results in a matrix with all zero values, it means that the two matrices being subtracted are identical. In such cases, all corresponding elements cancel each other out, resulting in zero values for all positions. Since the sparse matrix representation only stores non-zero values, the resulting matrix will appear empty.

### Conclusion
This implementation provides a solid foundation for handling sparse matrices and performing the required operations while adhering to the constraints specified in the assignment. Adjust the code as necessary to fit your specific requirements.
