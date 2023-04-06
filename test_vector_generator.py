import numpy as np
import json

NUM_BITS: int = 32
OPCODE_BITS: int = 4

with open('operation_encoding.json', 'r') as input_file:
    json_data: dict = json.load(input_file)
    encoding: dict = json_data['encoding']
    test_vectors: dict = json_data['test_vectors']

    with open('test_vectors.txt', 'w') as output_file:

        code_label = [f'op{idx}' for idx in range(0, OPCODE_BITS)]
        flag_label = [f'Z', f'N', f'C', f'V']
        abc_label = np.stack([np.array(
            [f'a{idx}', f'b{idx}', f'c{idx}'], dtype='S3', ) for idx in range(0, NUM_BITS)]).astype(str)
        abc_label = abc_label.transpose().reshape(-1)

        labels = np.hstack([code_label, abc_label, flag_label])

        np.savetxt(output_file, labels, fmt='%s', newline='\t\t')
        output_file.write('\n')

        for operation, data in test_vectors.items():
            a_vectors: dict = data['inputs']['a_vectors']
            b_vectors: dict = data['inputs']['b_vectors']
            c_outputs: dict = data['outputs']['c_output']
            z_flags: dict = data['outputs']['z_flag']
            n_flags: dict = data['outputs']['n_flag']
            c_flags: dict = data['outputs']['c_flag']
            v_flags: dict = data['outputs']['v_flag']

            for a, b, c, zf, nf, cf, vf in zip(a_vectors, b_vectors, c_outputs, z_flags, n_flags, c_flags, v_flags):
                opcode: str = np.array(
                    [bit for bit in encoding[operation]]).astype(str)
                a_bin: np.array = np.array(
                    [bit for bit in np.binary_repr(a, NUM_BITS)]).astype(str)
                b_bin: np.array = np.array(
                    [bit for bit in np.binary_repr(b, NUM_BITS)]).astype(str)
                c_bin: np.array = np.array(
                    [bit for bit in np.binary_repr(c, NUM_BITS)]).astype(str)
                z_bin: np.array = np.array(
                    [bit for bit in np.binary_repr(zf, 1)]).astype(str)
                n_bin: np.array = np.array(
                    [bit for bit in np.binary_repr(nf, 1)]).astype(str)
                c_bin: np.array = np.array(
                    [bit for bit in np.binary_repr(cf, 1)]).astype(str)
                v_bin: np.array = np.array(
                    [bit for bit in np.binary_repr(vf, 1)]).astype(str)

                line = np.hstack([opcode, a_bin, b_bin, c_bin, z_bin, n_bin, c_bin, v_bin])
                np.savetxt(output_file, line, fmt='%s', newline='\t\t')
                output_file.write('\b')

        # test = np.hstack([binary_list, binary_list, binary_list])
        # print(test.shape)
        # print(header.shape)
        # header = np.stack([header, test])

        # print(header)

        # np.savetxt(output_file, header.astype(str), fmt='%s', delimiter='\t\t')
        # # test_vectors.write('\t\t\t\t')
        # # np.savetxt(test_vectors, header[:, 1].astype(str).tolist(), fmt='%s', newline='\t\t')
        # # test_vectors.write('\n')
        # # np.savetxt(test_vectors, np.array(binary_list).astype(str), fmt='%s', newline='\t\t')
