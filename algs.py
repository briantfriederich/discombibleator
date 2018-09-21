import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from reference_lists import Reference_Lists

measures = pd.read_csv("data/measures.csv", header = 0, index_col = 0, squeeze=True).to_dict()

measurement_roots = pd.read_csv('data/measurement_roots.csv', header=0, index_col=1, squeeze=True).to_dict()

def Concat_Multiword(self):
        """Method finding and concatenating tokenized multi-word measure words.

        Args:
            None

        Returns:
            None
        """
        if any(np.intersect1d(self.arr, self.multiword_signifiers)):
            for i, j in enumerate(self.arr):
                if j in self.multiword_signifiers:
                    if self.arr[i-1] in self.ordinal_times:
                        self.arr[i-2:i+1] = [" ".join(self.arr[i-2:i+1])]
                    elif j in ("journey", "walk"):
                        if self.arr[i-2] in ("Sabbath", "sabbath"):
                            self.arr[i-2:i+1] = ["sabbath day's journey"]
                        else:
                            self.arr[i-1:i+1] = ["day's journey"]
                    elif j in ("cubit", "cubits"):
                        if self.arr[i-1] == 'long':
                            self.arr[i-1:i+1] = [" ".join(arr[i-1:i+1])]
        self.tokenized_string = self.arr

    def Has_Measure_Words(self):
        """Method checking whether a valid measurement can be found in the input.

        Args:
            None

        Returns:
            None
        """
        arr = self.tokenized_string
        if any(s in arr for s in measurement_roots.keys()): # concatenate keys and values into one list
            self.measurement_found = True
        elif any(s in arr for s in measurement_roots.values()): # change to assertion
            self.measurement_found = True
        else:
            print("Measurement to be converted not found in input text:\n{}".format(self.string))
        self.tokenized_string = arr

    def Lemmatize_Measure_Words(self):
        """Method lemmatizing measure words in input.

        Args:
            None

        Returns:
            None
        """
        arr = self.tokenized_string
        if self.measurement_found: #change to assertion
            for word in set(arr).intersection(measurement_roots.keys()):
                arr[:] = [measurement_roots[word] if x == word else x for x in arr]
            self.lemmatized = True
        self.tokenized_string = arr

    def Represents_Int(self, s):
        """Method checking whether an input is a string representation of an integer.

        Args:
            s (string): string item to be checked

        Returns:
            (bool): whether the input is a string representation of an integer
        """
        try:
            int(s)
            return True
        except ValueError:
            return False

    def Number_Converter(self, n, measure_word):
        """Method converting number from units in Ancient Hebrew measurements to
        units in modern measurements.

        Args:
            n (int): number to be converted
            measure_word (str): Ancient Hebrew units in which n was measured

        Returns:
            (str): string of the float of n converted into Imperial or Metric units
        """
        if self.units == "metric":
            n = float(n) * float(measures['metric_multiplier'][measure_word])
        else:
            n = float(n) * float(measures['imperial_multiplier'][measure_word])
        return str(n)

    def Measure_Word_Converter(self, word):
        """Method converting measure words into Imperial or Metric measures.

        Args:
            word(str): Ancient Hebrew measure word to be converted

        Returns:
            (str): string of corresponding metric or imperial measure
        """
        return (measures[self.units][word])

    def Find_Convert_Numbers(self):
        """Method locating and converting relevant numbers.

        Args:
            None

        Returns:
            None
        """
        arr = self.tokenized_string
        if self.lemmatized: # turn into assertion
            for i, j in enumerate(arr):
                if j in measurement_roots.values():
                    for unit in arr[:i]: # I don't like that this might look so extensively back.
                        if (i - arr.index(unit)) <= 4:
                            unit_locator = arr.index(unit)
                            if self.Represents_Int(unit):
                                arr[unit_locator] = self.Number_Converter(unit, j)
                            elif unit in ("a", "an", "the", "A", "An", "The"):
                                if(arr.index(j) - unit_locator) in range(2):
                                    arr[unit_locator] = self.Number_Converter(1, j)
            self.nums_converted = True
        self.tokenized_string = arr

    def Convert_Measure_Words(self):
        """Method locating and converting relevant numbers.

        Args:
            None

        Returns:
            None
        """
        arr = self.tokenized_string
        if self.nums_converted: # turn into assertion
            for i, j in enumerate(arr):
                if j in measurement_roots.values():
                    arr[i] = self.Measure_Word_Converter(j)
        self.mw_converted = True
        self.tokenized_string = arr

    def Join_Elements(self):
        """Method detokenizing array of words into final sentence.

        Args:
            None

        Returns:
            None
        """
        arr = self.tokenized_string
        for element in arr:
            output = "".join([" "+i if not i.startswith("'") and i not in self.punctuation else i for i in arr]).strip()
        self.tokenized_string = arr
        return output