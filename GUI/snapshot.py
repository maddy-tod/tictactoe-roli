"""
Used to regenerate the Bloch Sphere images

"""


"""
import qiskit.extensions.simulator

qr = QuantumRegister(1)
circuit = QuantumCircuit(qr)
circuit.h(qr[0])
circuit.s(qr[0])
circuit.snapshot(1)
circuit.t(qr[0])
circuit.snapshot(2)
circuit.t(qr[0])
circuit.snapshot(3)
circuit.t(qr[0])
circuit.snapshot(4)
circuit.t(qr[0])
circuit.snapshot(5)
circuit.t(qr[0])
circuit.snapshot(6)
circuit.t(qr[0])
circuit.snapshot(7)
circuit.t(qr[0])
circuit.snapshot(8)
circuit.t(qr[0])
circuit.snapshot(9)


backend = Aer.get_backend('statevector_simulator')
result = execute(circuit, backend).result()

print(result.data()['snapshots'])
"""

import numpy as np
from qiskit.tools.visualization import plot_bloch_vector
res = {'1': [[0.7071067811865476, 0.0], [0.4999999999999999, 0.4999999999999999]],
       '2': [[0.7071067811865476, 0.0], [0.0, 0.7071067811865474]],
       '3': [[0.7071067811865476, 0.0], [-0.49999999999999983, 0.49999999999999983]],
       '4': [[0.7071067811865476, 0.0], [-0.7071067811865472, 0.0]],
       '5': [[0.7071067811865476, 0.0], [-0.4999999999999998, -0.4999999999999998]],
       '6': [[0.7071067811865476, 0.0], [0.0, -0.7071067811865471]],
       '7': [[0.7071067811865476, 0.0], [0.49999999999999967, -0.49999999999999967]],
       '8': [[0.7071067811865476, 0.0], [0.707106781186547, 0.0]],
       '9': [[0.7071067811865476, 0.0], [0.4999999999999996, 0.4999999999999996]]}

x = [[0, 1], [1, 0]]
y = [[0, -1j], [1j, 0]]
z = [[1, 0], [0, -1]]

for key, mat in res.items():
    print('*'*15, key, '*'*15)
    print('mat : ', mat)
    new_mat = [0, 0]
    new_mat[0] = mat[0][0] + mat[0][1] * 1j
    new_mat[1] = mat[1][0] + mat[1][1] * 1j
    new_mat = [new_mat]
    new_mat = np.transpose(new_mat)
    print('new mat : ', new_mat)
    print('transp  : ', np.transpose(np.conj(new_mat)))
    state_matrix = np.matmul(new_mat, np.transpose(np.conj(new_mat)))
    print('STATE MATRIX \n', state_matrix)
    x1 = np.matmul(x, state_matrix)
    y1 = np.matmul(y, state_matrix)
    z1 = np.matmul(z, state_matrix)
    # matrices are correct

    print('x1 : ', x1)
    print('y1 : ', y1)
    print('z1 : ', z1)

    trcx = np.trace(x1)
    trcy = np.trace(y1)
    trcz = np.trace(z1)

    vals = [trcx.real, trcy.real, trcz.real]

    print('VALS : ', vals)

    print()

    blch = plot_bloch_vector(vals)
    blch.savefig('/Users/madeleinetod/Documents/NoughtsAndCrosses/GUI/imgs/testing/bloch' + key + '.png')




