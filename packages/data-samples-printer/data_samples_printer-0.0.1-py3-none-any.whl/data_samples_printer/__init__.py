from data_samples_printer.making_histograms import Annotations
from data_samples_printer.printing_histograms import (
    mprint_hist,
    pprint_hist,
    print_hist,
)

ADD_MEAN = Annotations.ADD_MEAN
ADD_STD = Annotations.ADD_STD
ADD_NUM_VALUES = Annotations.ADD_NUM_VALUES
ADD_MIN = Annotations.ADD_MIN
ADD_MAX = Annotations.ADD_MAX

print = print_hist  # noqa: A001
pprint = pprint_hist
mprint = mprint_hist
