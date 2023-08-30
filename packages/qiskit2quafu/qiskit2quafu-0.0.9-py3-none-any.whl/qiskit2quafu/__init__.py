from quafu import QuantumCircuit as quafuQC
import re
from qiskit import transpile, QuantumCircuit
name = "qiskit2quafu"


def qiskit2quafu(qc: QuantumCircuit, regName='iii', basis_gates=['cx', 'cy', 'cz', 'cp', 'u1', 'u2', 'u3', 'h', 'id', 'swap', 'cswap', 'p', 'rx', 'ry',
                                                                 'rz', 'x', 'y', 'z', 's', 'sdg', 't', 'tdg', 'sx', 'ccx', 'rxx', 'ryy', 'rzz'], optimization_level=0):

    def regMerge(qstring: str, regName=regName):
        regList = []
        t = qstring.splitlines()
        for a in t:
            if (re.search('qreg', a)):
                asp = a.split(' ')
                regList.append(asp[-1][:-1])

        mlist = []  # MiddleList

        for a in regList:
            b = a.split('[')
            b[-1] = int(b[-1][:-1])
            mlist.append(b)

        addDict = {}
        base = 0
        for a in mlist:
            addDict[a[0]] = base
            base = base+a[1]

        repDict = {}  # Replace Dictionary
        mv = 0
        currAdd = 0
        for a in mlist:
            name = a[0]
            bit = a[1]
            while mv < bit:
                repDict[name+'['+str(mv)+']'] = regName+'['+str(currAdd)+']'
                mv += 1
                currAdd += 1
            mv = 0

        ts = qstring

        for old, new in repDict.items():
            ts = ts.replace(old, new)

        rm_reg_list = []
        for a in regList:
            rm_reg_list.append('qreg '+a+';\n')

        replace_str = ''
        for a in rm_reg_list:
            replace_str += a

        ts = ts.replace(replace_str, 'qreg '+regName+'['+str(currAdd)+'];\n')
        return ts

    qc_new = transpile(qc, basis_gates=basis_gates,
                       optimization_level=optimization_level)
    qc_merge = regMerge(qc_new.qasm(), regName=regName)
    quafu_qc = quafuQC(qc_new.num_qubits)
    quafu_qc.from_openqasm(qc_merge)
    return quafu_qc, qc_merge
