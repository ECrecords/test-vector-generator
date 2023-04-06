import numpy as np
import json

NUM_BITS: int = 32
OPCODE_BITS: int = 4

with open('input.json', 'r') as input_file:
    json_data: dict = json.load(input_file)
    encoding: dict = json_data['encoding']
    test_vectors: dict = json_data['test_vectors']

    with open('test_vectors.txt', 'w') as output_file:

        code_label = [f'OP{idx}' for idx in range(0, OPCODE_BITS)]
        flag_label = [f'Z', f'N', f'C', f'V']
        abc_label = np.stack([np.array(
            [f'A{idx}', f'B{idx}', f'C{idx}'], dtype='S3', ) for idx in range(0, NUM_BITS)]).astype(str)
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
                zf_bin: np.array = np.array(
                    [bit for bit in np.binary_repr(zf, 1)]).astype(str)
                nf_bin: np.array = np.array(
                    [bit for bit in np.binary_repr(nf, 1)]).astype(str)
                cf_bin: np.array = np.array(
                    [bit for bit in np.binary_repr(cf, 1)]).astype(str)
                vf_bin: np.array = np.array(
                    [bit for bit in np.binary_repr(vf, 1)]).astype(str)

                line = np.hstack([opcode, a_bin, b_bin, c_bin, zf_bin, nf_bin, cf_bin, vf_bin])
                np.savetxt(output_file, line, fmt='%s', newline='\t\t')
                output_file.write('\n')    
            
            comment = ['---------' for i in range(0, len(line)-10)]
            comment[0] = '#'
            comment[-1] = '#'
            np.savetxt(output_file, comment, fmt='%s', newline='')
            output_file.write('\n')