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

    def __init__(self, file, dataframe = None, matrix = None) -> None:
        if dataframe is not None:
            self.filename = ""
            self.atributos = dataframe.atributos
            self.dados = dataframe.get_data()
            self.numEntradas = len(self.dados)
            self.targetVar = self.atributos[-1]
            self.targetCol = len(self.atributos) - 1
            self.filename = file
        elif matrix is not None:
            self.filename = ""
            self.atributos = matrix[0]
            self.dados = matrix[1:]
            self.numEntradas = len(self.dados)
            self.targetVar = self.atributos[-1]
            self.targetCol = len(self.atributos) - 1
            self.filename = file
        else:
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

        # format continuous values to default ranges


    def format_continuous(self):
        # Normalizing values from Weather dataset
            if self.filename == "datasets/weather.csv":
                for i in self.dados:
                    if int(i[1]) > 80:
                        i[1] = ">80"
                    elif int(i[1]) > 75:
                        i[1] = "76-80"
                    elif int(i[1]) > 70:
                        i[1] = "71-75"
                    else:
                        i[1] = "64-70"

                    if int(i[2]) > 90:
                        i[2] = ">90"
                    elif int(i[2]) > 80:
                        i[2] = "81-90"
                    elif int(i[2]) > 70:
                        i[2] = "71-80"
                    else:
                        i[2] = "65-70"

        # Normalizing values from Iris dataset
            if self.filename == "datasets/iris.csv":
                for i in self.dados:
                    if float(i[0]) > 7.0:
                        i[0] = ">7"
                    elif float(i[0]) > 6.0:
                        i[0] = "6-7"
                    elif float(i[0]) > 5.0:
                        i[0] = "5-6"
                    else:
                        i[0] = "4-5"

                    if float(i[2]) > 4.0:
                        i[2] = ">4"
                    elif float(i[2]) > 3.5:
                        i[2] = "3.5-4"
                    elif float(i[2]) > 3.0:
                        i[2] = "3-3.5"
                    elif float(i[2]) > 2.5:
                        i[2] = "2.5-3"
                    else:
                        i[2] = "2-2.5"

                    if float(i[3]) > 6.0:
                        i[3] = ">6"
                    elif float(i[3]) > 5.0:
                        i[3] = "5-6"
                    elif float(i[3]) > 4.0:
                        i[3] = "4-5"
                    elif float(i[3]) > 3.0:
                        i[3] = "3-4"
                    elif float(i[3]) > 2.0:
                        i[3] = "2-3"
                    else:
                        i[3] = "1-2"
                    if float(i[1]) > 2.0:
                        i[1] = ">2"
                    elif float(i[1])  > 1.5:
                        i[1] = "1.5-2"
                    elif float(i[1]) > 1.0:
                        i[1] = "1-1.5"
                    elif float(i[1]) > 0.5:
                        i[1] = "0.5-1"
                    else:
                        i[1] = "0-0.5"

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

    def copy(self):
        ''' Returns a copy of the dataframe'''
        df = DataFrame(self.filename)
        df.atributos = self.atributos
        df.dados = self.dados
        df.numEntradas = self.numEntradas
        df.targetVar = self.targetVar
        df.targetCol = self.targetCol
        return df

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

    def CountUniqueOfValue(self, col: int, value: str) -> int:
        unique_values = []
        for i in self.dados:
            a = i[col]
            if a == value and i not in unique_values:
                unique_values.append(i)
        return len(unique_values)

    def get_data_wo_target(self):
        data_no_target = []
        for i in self.dados:
            data_no_target.append(i[:self.targetCol])
        return data_no_target
    
    def if_contains(self, val: str) -> list:
        list = []
        for i in self.dados:
            if val in i:
                list.append(i)
        return list
    
    def if_contains_in_column(self, val: str, col: int) -> list:
        list = []
        for i in self.dados:
            if val in i[col]:
                list.append(i)
        return list
    
    # ---------------------------------------------------------------

    def getColumn(self, string: str) -> int:
        for i in self.atributos:
            if(i == string):
                return self.atributos.index(i)

    def get_unique_values(self, col: int) -> list:
        unique_values = []
        for i in self.dados:
            if i[col] not in unique_values:
                unique_values.append(i[col])
        return unique_values
    
    def DropAllExceptWhereEqual(self, Pos: int, value: str):
        for i in self.dados:
            if i[Pos] != value:
                self.dados.remove(i)

    def get_most_common_class(self):
        return max(set(self.get_target_col()), key=self.get_target_col().count)
    # MODIFY DATAFRAME METHODS
    

    # ---------------------------------------------------------------

    def drop(self, col) -> None:

        """Remove a column from the dataframe, given its index (begins at 0)"""

        for i in range(0,len(self.dados)):
            del self.dados[i][col]

        del self.atributos[col]
        self.targetCol -= 1

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

    def dropColumnsExcept(self, cols: list):
        """
        Remove all columns from the dataframe except the ones given.
        
        Parameters
        ----------------
            cols: list of column indexes to keep (begins at 0)
        """

        for i in cols:
            inde = self.atributos.index(i)
            self.atributos.remove(i)
            for j in range(0,len(self.dados)):
                del self.dados[j][inde]

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