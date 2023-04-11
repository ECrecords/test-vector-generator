import numpy as np
import json
import argparse
from io import TextIOWrapper
import sys

def read_json(json_file: str) -> dict:
    with open(json_file, 'r') as input_file:
        try:
            json_data: dict = json.load(input_file)
        except json.JSONDecodeError:
            print(f'FATAL ERROR: check syntax of {json_file}')
            sys.exit(1)
    return json_data


def write_header(output_file: TextIOWrapper, VECTOR_BITS: int, OPCODE_BITS: int) -> int:
    code_label = [
        f'OP{(OPCODE_BITS-1)-idx:01}' for idx in range(0, OPCODE_BITS)]
    flag_label = ['Z  ', 'N  ', 'C  ', 'V  ']
    abc_label = np.stack([np.array(
        [f'A{(VECTOR_BITS-1)-idx:02}', f'B{(VECTOR_BITS-1)-idx:02}', f'C{(VECTOR_BITS-1)-idx:02}'], dtype='S3', ) for idx in range(0, VECTOR_BITS)]).astype(str)
    abc_label = abc_label.transpose().reshape(-1)

    labels = '     '.join(np.hstack([code_label, abc_label, flag_label]))

    output_file.write(f'{labels}\n#{(len(labels)-2)*"-"}#\n')

    return len(labels)


def write_test(output_file: TextIOWrapper, json_data: dict, VECTOR_BITS: int, label_length: int) -> None:

    for operation, data in json_data.items():
        
        try:
            opcode: str = np.array(
                [bit for bit in data['inputs']['encoding']]).astype(str)
            a_vectors: dict = data['inputs']['a_vectors']
            b_vectors: dict = data['inputs']['b_vectors']
            c_outputs: dict = data['outputs']['c_output']
            z_flags: dict = data['outputs']['z_flag']
            n_flags: dict = data['outputs']['n_flag']
            c_flags: dict = data['outputs']['c_flag']
            v_flags: dict = data['outputs']['v_flag']
        except KeyError:
            print(f'ERROR: check \'{operation}\' operation')
            continue

        vector_lengths = [len(lst) for lst in [
            a_vectors, b_vectors, c_outputs, z_flags, n_flags, c_flags, v_flags]]
        if not all(length == vector_lengths[0] for length in vector_lengths):
            output_file.write(
                f'# \'{operation}\' section in the JSON contains mismatching lengths, all lists inside must be of same length.')
            output_file.write(f'\n#{(label_length-2)*"-"}#\n')

            print(f'ERROR: width mismatch in \'{operation}\' operation')
            continue

        print(f'\'{operation}\' operation found.')

        for a, b, c, zf, nf, cf, vf in zip(a_vectors, b_vectors, c_outputs, z_flags, n_flags, c_flags, v_flags):
            a_bin: np.array = np.array(
                [bit for bit in np.binary_repr(a, VECTOR_BITS)]).astype(str)
            b_bin: np.array = np.array(
                [bit for bit in np.binary_repr(b, VECTOR_BITS)]).astype(str)
            c_bin: np.array = np.array(
                [bit for bit in np.binary_repr(c, VECTOR_BITS)]).astype(str)
            zf_bin: np.array = np.array(
                [bit for bit in np.binary_repr(zf, 1)]).astype(str)
            nf_bin: np.array = np.array(
                [bit for bit in np.binary_repr(nf, 1)]).astype(str)
            cf_bin: np.array = np.array(
                [bit for bit in np.binary_repr(cf, 1)]).astype(str)
            vf_bin: np.array = np.array(
                [bit for bit in np.binary_repr(vf, 1)]).astype(str)

            line = np.hstack([opcode, a_bin, b_bin, c_bin,
                              zf_bin, nf_bin, cf_bin, vf_bin])
            np.savetxt(output_file, line, fmt='%s', newline='       ')
            output_file.write('\n')

        output_file.write(f'#{(label_length-2)*"-"}#\n')


def main():
    NUM_BITS: int = 32
    OPCODE_BITS: int = 4

    parser = argparse.ArgumentParser(
        description='Generate test vectors from a JSON file.')
    parser.add_argument('-j', '--json', type=str,
                        help='The name of the input JSON file.')
    parser.add_argument('-f', '--filename', type=str,
                        help='The name of the output text file.', default='test_vectors.txt', nargs='?')
    args = parser.parse_args()

    if not args.json:
        parser.error(
            'No input file specified. Please provide an input file name.')

    with open(args.filename, 'w') as output_file:
        json_data: dict = read_json(args.json)
        label_len: int = write_header(output_file, NUM_BITS, OPCODE_BITS)
        write_test(output_file, json_data, NUM_BITS, label_len)

    print(f'\ntest vectors written to {args.filename}.')


if __name__ == '__main__':
    main()
