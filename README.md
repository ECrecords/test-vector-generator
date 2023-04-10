# ALU Test Vector Generator

This is a Python script that generates test vectors for a 32-bit Arithmetic Logic Unit (ALU). The test vectors can be used to test the functionality of the ALU and detect any errors or bugs.

## Usage

To use this script, you need to provide a JSON file containing test data for various ALU operations. The JSON file should have the following format:

```json
{
    "operation1": {
        "inputs": {
            "encoding": "0100",
            "a_vectors": [2147483647, 0, 1],
            "b_vectors": [1, 2, 3]
        },
        "outputs": {
            "c_output": [2147483647, 2, 4],
            "z_flag": [0, 0, 0],
            "n_flag": [0, 0, 0],
            "c_flag": [0, 0, 0],
            "v_flag": [0, 0, 0]
        }
    },
    "operation2": {
        ...
    }
}
```

The `inputs` and `outputs` objects contain lists of input and output values for each ALU operation. The `encoding` key is used to specify the opcode for the operation. The input and output values should be in decimal format.

To generate test vectors from the JSON file, run the `TestVectorGenerator.py` script and provide the path to the JSON file as an argument:

```bash
python TestVectorGenerator.py -j input.json
```

The script will generate a text file called `test_vectors.txt` containing the test vectors.

## Requirements
This script requires Python 3 and the following Python packages:
- numpy
- argparse
- json

## License
This script is released under the MIT license. See the LICENSE file for more details.