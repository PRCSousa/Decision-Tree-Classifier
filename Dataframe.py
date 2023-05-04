import random

class DataFrame:
    """
    Dataframe class for reading and manipulating csv files. (To the likes of pandas)
    
    Parameters
    ----------------
        file: path to the csv file to be read

    """
    
    nanlist = ["?", "", " ", "NaN", "nan", "NAN", "Nan"]

    # ---------------------------------------------------------------

    def __init__(self, file) -> None:
        self.filename = ""
        self.atributos = []
        self.dados = []
        self.numEntradas = 0
        self.targetVar = ""
        self.targetCol = 0
        self.filename = file

    # ---------------------------------------------------------------

    def read_csv(self):
        with open(self.filename, "r") as csv:
            count = 0

            for line in csv:

                if count == 0:
                    line = line.strip()
                    self.atributos=line.split(',')
                    self.targetVar = self.atributos[-1]
                    self.targetCol = len(self.atributos) - 1

                else:
                    entrada=[]
                    line = line.strip()
                    entrada=line.split(',')
                    # append the data to the list
                    self.dados.append(entrada)

                count += 1
            self.numEntradas = count - 1

    # ---------------------------------------------------------------

    def print_csv(self):
        print(self.atributos)
        for i in self.dados:
            print(i)

    # ---------------------------------------------------------------
    
    def get_dataframe(self):
        # add both attributes and data to the same matrix and return it
        df = []
        df.append(self.atributos)
        for i in self.dados:
            df.append(i)
        
        return df

    # ---------------------------------------------------------------

    def get_target_col(self):
        target_col = []
        for i in self.dados:
            target_col.append(i[self.targetCol])
        return target_col
    
    # ---------------------------------------------------------------

    def get_data(self):
        data = []
        for i in self.dados:
            data.append(i)
        return data
    
    # ---------------------------------------------------------------

    def get_data_wo_target(self):
        data_no_target = []
        for i in self.dados:
            data_no_target.append(i[:self.targetCol])
        return data_no_target
    
    # ---------------------------------------------------------------

    # MODIFY DATAFRAME METHODS

    # ---------------------------------------------------------------

    def drop(self, col):

        """Remove a column from the dataframe, given its index (begins at 0)"""

        for i in range(0,len(self.dados)):
            del self.dados[i][col]
        del self.atributos[col]

    # ---------------------------------------------------------------

    def dropna(self):
        """
        Remove entries with missing values from the dataframe.
        """

        for i in range(0,len(self.dados)):
            for j in range(0,len(self.dados[i])):
                if (self.dados[i][j] in self.nanlist):
                    del self.dados[i]
                    break

    # ---------------------------------------------------------------

    def fillna(self, col, value):
        """
        Replace missing values in the chosen column with the value given.
        
        Parameters
        ----------------
            col: column index (begins at 0)
            value: value to replace missing values with
        """

        for i in range(0,len(self.dados)):
            if self.dados[i][col] == "?":
                self.dados[i][col] = value

    # ---------------------------------------------------------------

    def train_test_split(self, test_size, seed=42):
        random.seed(seed)
        test_size=int(self.numEntradas*test_size)
        lista = random.sample(range(0, self.numEntradas), test_size)

        lista.sort()
        
        X_test = []
        X_train = []
        
        for i in range(0,len(self.dados)):
            if i in lista:
                X_train.append(self.dados[i])
            else:
                X_test.append(self.dados[i])

        Y_train = []
        Y_test = []

        for i in range(0,len(X_train)):
            Y_train.append(X_train[i][self.targetCol])
            del X_train[i][self.targetCol]
        
        for i in range(0,len(X_test)):
            Y_test.append(X_test[i][self.targetCol])
            del X_test[i][self.targetCol]

        return X_train, X_test, Y_train, Y_test
    
    # ---------------------------------------------------------------

    

    #ola pepe!