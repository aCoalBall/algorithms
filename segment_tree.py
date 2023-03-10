class segment_tree:
    nums1: list[int]
    l : int
    d : list[int]
    v : list[int]
    lazy : list[int]
    
    def __init__(self, nums:list[int]):
        self.nums1 = nums
        self.l = len(nums)
        self.d = [None,] * self.l * 4
        self.v = [0,] * self.l * 4
        self.lazy = [None,] * self.l * 4
        self.__build(p=1, l=0, r=self.l - 1)

    '''build the segment tree (self.d)'''
    def __build(self, p:int, l:int, r:int):
        if l == r:
            self.d[p] = self.nums1[l]
        else:
            m = (l + r) >> 1
            self.__build(p * 2, l, m); self.__build(p * 2 + 1, m + 1, r)
            self.d[p] = self.d[p * 2] + self.d[p * 2 + 1]
    
    def __lazy_propagation(self, p:int, l:int, r:int, m:int, mode = None):
        if self.v[p]:
            self.v[p * 2] = 1
            self.v[p * 2 + 1] = 1
            self.d[p * 2] = (m - l + 1) * self.lazy[p] 
            self.d[p * 2 + 1] = (r - m) * self.lazy[p]
            self.lazy[p * 2] = self.lazy[p]
            self.lazy[p * 2 + 1] = self.lazy[p]
            self.lazy[p] = 0
            self.v[p] = 0
    
    '''access the sum of the given interval in the segment tree'''
    def query(self, s:int, t:int):
        return self.__query(p=1, l=0, r=self.l - 1, s=s, t=t)
    
    '''access the sum of the given interval in the segment tree'''
    def __query(self, p:int, l:int, r:int, s:int, t:int):
        if s <= l and t >= r:
            return self.d[p]
        else:
            sum = 0
            m = (l + r) >> 1
            self.__lazy_propagation(p, l, r, m)
            if s <= m:
                sum = sum + self.__query(p * 2, l, m, s, t)
            if t > m:
                sum = sum + self.__query(p * 2 + 1, m + 1, r, s, t)
            return sum
    
    '''update the intervals in the segment tree'''
    def update(self, s:int, t:int, val:int):
        self.__update(p=1, l=0, r=self.l - 1, s=s, t=t, val=val)

    '''update the intervals in the segment tree'''
    def __update(self, p:int, l:int, r:int, s:int, t:int, val:int):
        if s <= l and t >= r:
            self.d[p] = (r - l + 1) * val
            self.v[p] = 1
            self.lazy[p] = val
        else:
            m = (l + r) >> 1
            self.__lazy_propagation(p, l, r, m)
            if s <= m:
                self.__update(p * 2, l, m, s, t, val)
            if t > m:
                self.__update(p * 2 + 1, m + 1, r, s, t, val)
            self.d[p] = self.d[p * 2] + self.d[p * 2 + 1]

    def array(self):
        nums = []
        for i in range(self.l):
            x = self.__query(p=1, l=0, r=self.l - 1, s=i, t=i)
            nums.append(x)
        return nums