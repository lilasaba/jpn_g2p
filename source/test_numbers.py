# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import sys
import unittest
from number_converter import ConvertNumber

PY_VERSION = sys.version_info[0]

w2n = ConvertNumber()
tl = []
with open('jpn_number_test.txt') as testlines:
    for line in testlines:
        if PY_VERSION == 2:
            line = line.decode('utf-8')
        line = line.strip()
        ln = line.split('\t')
        tl.append(ln)

k2a_test_name = ['test_%s' % tl[i][0] for i in range(len(tl))]
a2k_test_name = ['test_%s' % tl[i][1] for i in range(len(tl))]
k2a_hyp = [w2n.kanji2num(line[0]) for line in tl]
a2k_hyp = [w2n.num2written(line[1])[0] for line in tl]
k2a_ref = [line[1] for line in tl] 
a2k_ref = [line[0] for line in tl]

class FullTest(unittest.TestCase):
    pass

def test_generator(a,b):
    def test(self):
        self.maxDiff = None
        self.assertEqual(a,b)
    return test

if __name__ == '__main__':

    for i in range(len(k2a_ref)):
        reference = k2a_ref[i]
        testmethodname = k2a_test_name[i]
        if PY_VERSION == 2:
            testmethodname = testmethodname.encode('utf-8')
        test = test_generator(reference,k2a_hyp[i])
        setattr(FullTest,testmethodname,test)
    for i in range(len(a2k_ref)):
        reference = a2k_ref[i]
        testmethodname = a2k_test_name[i]
        if PY_VERSION == 2:
            testmethodname = testmethodname.encode('utf-8')
        test = test_generator(reference,a2k_hyp[i])
        setattr(FullTest,testmethodname,test)
    unittest.main(verbosity=2)
