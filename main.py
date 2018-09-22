from reference_lists import Reference_Lists
from algs import *
from inputs import *

class Discombibleator:

    """Class taking an object and converting it into an output string with
    measurements converted into imperial or metric units.

    """

    def __init__(self, object, units):
        """Method initializing Discombibleator tool.
        Method initializing Biblical_Measurement object.

        Args:
            string (str)
            units (str)

        Attributes:
            string (str): String of text to be converted into modern measurements.
            arr (arr): Class' string attribute word-tokenized through NLTK.
            units (string): String indicating whether output units will be in
                Imperial or Metric units. Default is Imperial units.
            measurement_found (bool): Boolean indicating a valid Ancient Hebrew
                measurement has been found in self.arr and can be processed.
            lemmatized (bool): Boolean indicating the lemitization step has been
                executed.
            nums_converted (bool): Boolean indicating numbers have been converted.
            mw_converted (bool): Boolean indicating measure words have been converted.
            multiword signifiers (arr): Array of words signaling the possible
                presence of multiword measure words tokenized into multiple items.
            ordinal_times (arr): Array of words indicating a specific time.
            punctuation (arr): List if punctuation to ease detokenizing sentences.
        """
        self.string = object.string
        self.units = units.units

    def __run__(self):
        "Method running algorithms on "
        tokenized = Tokenize(self.string)
        concatenated = Concat_Multiword.run(tokenized)
        multi_handled = Has_Multiword.run(concatenated)
        lemmatized = Lemmatize_Measure_Words.run(multi_handled)
        converted = Find_Convert_Numbers.run(lemmatized, self.units)
        Join_Elements.run(converted)
