import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
import operator

VALID_CR_STRAT_TYPES = [
    'linear_probing',
    'quadratic_probing',
    'double_hashing',
    'separate_chaining'

]


ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,  # use operator.div for Python 2
    'mod' : operator.mod,
    '^' : operator.xor,
}


class CollisionResolutionFactory:
    def __init__(self):
        self._cr_strats = {}
        for cr_strat in CollosionResolution.__subclasses__():
            cr_strat_obj = cr_strat()
            self._cr_strats[cr_strat_obj.get_strategy_type()] = cr_strat_obj

    def get_strategy(self, strategy_type):
        if strategy_type not in VALID_CR_STRAT_TYPES:
            raise ValueError('The collision resolution strategy type type supplied is not valid.'
                             'You Must enter a Valid strategy Type')
        return self._cr_strats[strategy_type]


# noinspection PyAbstractClass
class CollosionResolution(ABC):
    @abstractmethod
    def get_strategy_type(self):
        pass

    @abstractmethod
    def probe(self, **kwargs):
        pass

class SeparateChaining(CollosionResolution):

    def get_strategy_type(self):
        return 'separate_chaining'

    h_k = lambda self, k: k % self.N

    # def __init__(self, **kwargs):
    #     self.input_seq = kwargs.get('input_seq')
    #     self.N = kwargs.get('N')
    #     self.hash_array = np.empty(N)
    #     self._prepare_probe_table()

    def _prepare_data(self,**kwargs):

        self.input_seq = kwargs.get('input_seq')
        self.N = kwargs.get('N')
        self.hash_table = {i:[] for i in range(self.N)}


        self.hash_func = f'h(k) = k mod {self.N}'


        #self.lp_df.index = lp_df['k']
        #self.lp_df.drop(columns='k', inplace=True)


    def probe(self, **kwargs):
        self._prepare_data(**kwargs)
        print('Initiating separate chaining')
        print(f'\nInput Sequence: \n{self.input_seq}\n')
        print(self.hash_func)

        for s in self.input_seq:
            print(f'\nKey: {s}')
            print(f'Hash value h(k) = {s} mod {self.N} = {self.h_k(s)}')
            print(f'Inserted at {self.h_k(s)}')
            self.hash_table[self.h_k(s)].append(s)




        print(f'\nFinal Hash Table: \n')
        self.print_table()

    def print_table(self):
        for key in self.hash_table.keys():
            if len(self.hash_table[key])==0:
                print(key)
            else:
                vals = [str(v) for v in self.hash_table[key]]
                print(f"{key}-->{'--'.join(vals)}")



class LinearProbing(CollosionResolution):

    def get_strategy_type(self):
        return 'linear_probing'

    h_k = lambda self, k: k % self.N

    # def __init__(self, **kwargs):
    #     self.input_seq = kwargs.get('input_seq')
    #     self.N = kwargs.get('N')
    #     self.hash_array = np.empty(N)
    #     self._prepare_probe_table()

    def _prepare_data(self,**kwargs):

        self.input_seq = kwargs.get('input_seq')
        self.N = kwargs.get('N')
        self.hash_array = [None] * self.N

        self.hash_func = f'h(k) = k mod {self.N}'

        self.lp_df = pd.DataFrame(columns=['k', self.hash_func, 'Probes'])
        self.lp_df['k'] = self.input_seq
        self.lp_df[self.hash_func] = self.lp_df['k'].apply(self.h_k)
        self.collisions = []
        #self.lp_df.index = lp_df['k']
        #self.lp_df.drop(columns='k', inplace=True)


    def probe(self, **kwargs):
        self._prepare_data(**kwargs)
        print('Initiating linear probing')
        print(f'\nInput Sequence: \n{self.input_seq}\n')
        print(self.hash_func)
        print('ith probe = (h(k) + i^2) mod N, i = 0 to N-1')
        print(f'\nProbe Table: \n{self.lp_df}')
        self.lp_df['Probes'] = self.lp_df.apply(self._probe_and_insert, axis=1)


        print(f'\nFinal Probe Table: \n{self.lp_df}')
        print(f'\nFinal Hash Table: \n{self.hash_array}')
        str_colls = [str(x) for x in self.collisions]
        print(f"\nTotal collisions: {'+'.join(str_colls)} = {sum(self.collisions)}")

    def _probe_and_insert(self, x):
        probes = ''
        print(f'\nInsert key: {x.k}')
        print(f'\nh(k): {x[self.hash_func]}')
        print(f'Hash Table before insertion: \n{self.hash_array}\n')
        inserted = False
        colls = 0
        for i in range(self.N):
            print(f'For i = {i}')

            probe_index = (x[self.hash_func] + i) % self.N
            probe_index_str = f'probe: {i} = ({x[self.hash_func]} + {i}) mod {self.N} = {probe_index}'
            probes += f'{str(probe_index)}, '
            if self.hash_array[probe_index] is None:
                self.hash_array[probe_index] = x['k']
                probes = probes[:-2]
                print(probe_index_str, ' - Inserted')
                print(f'\nHash_Table[{probe_index}] = {x.k}')
                inserted = True
                print(f'\nHash Table after insertion: \n{self.hash_array}\n')
                break
            else:
                print(probe_index_str, ' - Occupied')
                colls +=1
        if not inserted:
            k = x['k']
            print(f'\nk = {k} could not be inserted after {self.N} probes')

        print(f'Collisions : {colls}')
        self.collisions.append(colls)
        return probes

class QuadraticProbing(CollosionResolution):

    def get_strategy_type(self):
        return 'quadratic_probing'

    h_k = lambda self, k: k % self.N

    # def __init__(self, **kwargs):
    #     self.input_seq = kwargs.get('input_seq')
    #     self.N = kwargs.get('N')
    #     self.hash_array = np.empty(N)
    #     self._prepare_probe_table()

    def _prepare_data(self,**kwargs):

        self.input_seq = kwargs.get('input_seq')
        self.N = kwargs.get('N')
        self.hash_array = [None] * self.N

        self.hash_func = f'h(k) = k mod {self.N}'
        self.collisions = []

        self.lp_df = pd.DataFrame(columns=['k', self.hash_func, 'Probes'])
        self.lp_df['k'] = self.input_seq
        self.lp_df[self.hash_func] = self.lp_df['k'].apply(self.h_k)
        #self.lp_df.index = lp_df['k']
        #self.lp_df.drop(columns='k', inplace=True)


    def probe(self, **kwargs):
        self._prepare_data(**kwargs)
        print('Initiating quadratic probing')
        print(f'\nInput Sequence: \n{self.input_seq}\n')
        print(self.hash_func)
        print('ith probe = (h(k) + i^2) mod N, i = 0 to N-1')
        print(f'\nProbe Table: \n{self.lp_df}')
        self.lp_df['Probes'] = self.lp_df.apply(self._probe_and_insert, axis=1)


        print(f'\nFinal Probe Table: \n{self.lp_df}')
        print(f'\nFinal Hash Table: \n{self.hash_array}')
        str_colls = [str(x) for x in self.collisions]
        print(f"\nTotal collisions: {'+'.join(str_colls)} = {sum(self.collisions)}")

    def _probe_and_insert(self, x):
        probes = ''
        print(f'\nInsert key: {x.k}')
        print(f'\nh(k): {x[self.hash_func]}')
        print(f'Hash Table before insertion: \n{self.hash_array}\n')
        inserted = False
        colls = 0
        for i in range(self.N):
            print(f'For i = {i}')

            probe_index = (x[self.hash_func] + i**2) % self.N
            probe_index_str = f'probe: {i} = ({x[self.hash_func]} + {i}^2) mod {self.N} = {probe_index}'
            probes += f'{str(probe_index)}, '
            if self.hash_array[probe_index] is None:
                self.hash_array[probe_index] = x['k']
                probes = probes[:-2]
                print(probe_index_str, ' - Inserted')
                print(f'\nHash_Table[{probe_index}] = {x.k}')
                inserted = True
                print(f'\nHash Table after insertion: \n{self.hash_array}\n')
                break
            else:
                print(probe_index_str, ' - Occupied')
                colls += 1
        if not inserted:
            k = x['k']
            print(f'\nk = {k} could not be inserted after {self.N} probes')

        print(f'Collisions : {colls}')
        self.collisions.append(colls)
        return probes

class DoubleHashing(CollosionResolution):

    def get_strategy_type(self):
        return 'double_hashing'

    h_k = lambda self, k: k % self.N

    # def __init__(self, **kwargs):
    #     self.input_seq = kwargs.get('input_seq')
    #     self.N = kwargs.get('N')
    #     self.hash_array = np.empty(N)
    #     self._prepare_probe_table()

    def _prepare_data(self,**kwargs):

        self.input_seq = kwargs.get('input_seq')
        self.N = kwargs.get('N')
        self.hash_array = [None] * self.N

        self.collisions = []

        d_K_str = kwargs.get('d_k')
        d_k = d_K_str.split()
        self.operand1 = int(d_k[0])
        self.operator1 = d_k[1]

        self.operand2 = int(d_k[4])
        self.operator2 = d_k[3]

        self.d_k = lambda k: ops[self.operator1](self.operand1, ops[self.operator2](k, self.operand2))

        self.hash_func = f'h(k) = k mod {self.N}'
        self.d_k_func = f'd(k) = {d_K_str}'

        self.lp_df = pd.DataFrame(columns=['k', self.hash_func,self.d_k_func, 'Probes'])
        self.lp_df['k'] = self.input_seq
        self.lp_df[self.hash_func] = self.lp_df['k'].apply(self.h_k)
        self.lp_df[self.d_k_func] = self.lp_df['k'].apply(self.d_k)
        #self.lp_df.index = lp_df['k']
        #self.lp_df.drop(columns='k', inplace=True)


    def probe(self, **kwargs):
        self._prepare_data(**kwargs)
        print('Initiating double hashing')
        print(f'\nInput Sequence: \n{self.input_seq}\n')
        print(self.hash_func)
        print(self.d_k_func)
        print('ith probe = (h(k) + i*d(k)) mod N, i = 0 to N-1')

        print(f'\nProbe Table: \n{self.lp_df}')
        self.lp_df['Probes'] = self.lp_df.apply(self._probe_and_insert, axis=1)
        print(f'\nFinal Probe Table: \n{self.lp_df}')
        print(f'\nFinal Hash Table: \n{self.hash_array}')
        str_colls = [str(x) for x in self.collisions]
        print(f"\nTotal collisions: {'+'.join(str_colls)} = {sum(self.collisions)}")

    def _probe_and_insert(self, x):
        probes = ''
        print(f'\nInsert key: {x.k}')
        print(f'\nh(k): {x[self.hash_func]}')
        print(f'd(k): {x[self.d_k_func]}')
        print(f'Hash Table before insertion: \n{self.hash_array}\n')
        inserted = False
        colls = 0
        for i in range(self.N):
            print(f'For i = {i}')
            probe_index = (x[self.hash_func] + i*x[self.d_k_func]) % self.N
            probe_index_str = f'probe: {i} = ({x[self.hash_func]} + {i}*{x[self.d_k_func]}) mod {self.N} = {probe_index}'
            probes += f'{str(probe_index)}, '
            if self.hash_array[probe_index] is None:
                self.hash_array[probe_index] = x['k']
                probes = probes[:-2]
                print(probe_index_str, ' - Inserted')
                print(f'\nHash_Table[{probe_index}] = {x.k}')
                inserted = True
                print(f'\nHash Table after insertion: \n{self.hash_array}\n')
                inserted = True
                break
            else:
                print(probe_index_str, ' - Occupied')
                colls += 1
        if not inserted:
            k = x['k']
            print(f'\nk = {k} could not be inserted after {self.N} probes')

        print(f'Collisions : {colls}')
        self.collisions.append(colls)
        return probes



if __name__ == '__main__':
    crf = CollisionResolutionFactory()
    # crf.get_strategy(strategy_type='quadratic_probing').probe(input_seq = [1, 22, 34, 47, 31, 57, 83, 14, 5], d_k = '1 + k mod 9', N = 11)
    crf.get_strategy(strategy_type='quadratic_probing').probe(input_seq=[31, 45, 15, 99, 11, 5, 47, 4, 11, 28],
                                                           d_k='1 + k mod 9', N=11)