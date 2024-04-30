class Matrix:

    def __init__(self, r, c):
        self.vals = []
        self.rows_amount = r
        self.cols_amount = c
        for i in range(r):
            self.vals.append([])
            for j in range(c):
                self.vals[i].append(None)

    def copy(self):
        new_m = Matrix(self.rows_amount, self.cols_amount)
        for i in range(self.rows_amount):
            for j in range(self.cols_amount):
                new_m[i][j] = self[i][j]
        return new_m

    def __getitem__(self, item):
        return self.vals[item]

    def __str__(self):
        return str(self.vals)

    def normalise(self):
        res = [0 for i in range(self.cols_amount)]
        for i in range(self.cols_amount):
            for j in range(self.rows_amount):
                res[i] += self[j][i]
        new_m = self.copy()


        for i in range(self.cols_amount):
            for j in range(self.rows_amount):
                new_m[j][i] /= res[i]
        return new_m

    @staticmethod
    def build_weight_table(other):
        weight_matrix = Matrix(other.rows_amount, 1)
        for i in range(other.rows_amount):
            weight_matrix[i][0] = sum(other[i])/len(other[i])
        return weight_matrix

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            return
        if self.cols_amount != other.rows_amount:
            raise Exception("Error at multiplying of matrixes: columns amount and rows amount dont match")
        new_m = Matrix(self.rows_amount, other.cols_amount)
        for i in range(self.rows_amount):
            for j in range(other.cols_amount):
                msum = 0
                for a in range(self.cols_amount):
                    msum += self[i][a] * other[a][j]
                new_m[i][j] = msum
        return new_m

    def vert_unit_conc(self, other):
        for i in range(self.rows_amount):
            self.vals[i].append(other[i][0])
        self.cols_amount = len(self.vals[i])