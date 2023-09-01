import warnings
from enum import Flag, auto
from typing import Generator, List, Optional, Sequence, Tuple, cast

import numpy as np

# Note: we are not using whitespace here as the lowest value because it is often not
# rendered with the same width as the other block characters even in fixed-with fonts.
_DRAWING_CHARS = np.asarray(list(" ▁▂▃▄▅▆▇█"))
_NUM_DRAWING_CHARS = len(_DRAWING_CHARS)


class Annotations(Flag):
    ADD_MEAN = auto()
    ADD_STD = auto()
    ADD_NUM_VALUES = auto()
    ADD_MIN = auto()
    ADD_MAX = auto()


def _deduce_range(
    xs: Sequence[Sequence[float]],
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
) -> Tuple[float, float]:
    # Note: we can't use np.max(xs) and np.min(xs) here because numpy won't deal with
    # sequences of different lengths.
    if min_value is None:
        min_value = min(np.min(x) for x in xs if len(x) > 0)

    if max_value is None:
        max_value = max(np.max(x) for x in xs if len(x) > 0)

    if min_value > max_value:
        min_value, max_value = max_value, min_value
        warnings.warn(
            f"min_value was greater than max_value. "
            f"They were swapped to {min_value}, {max_value}",
            stacklevel=2,
        )
    return min_value, max_value


def _deduce_num_bins(
    xs: Sequence[Sequence[float]],
    max_bins: int = 50,
    num_bins: Optional[int] = None,
) -> int:
    if num_bins is None:
        num_bins = max(  # At least one bin
            min(  # Not more than max_bins
                max(len(x) for x in xs), max_bins  # At least one bin per sample
            ),
            1,
        )
    if num_bins > max_bins:
        raise ValueError(
            f"num_bins ({num_bins}) must be less than or equal to "
            f"max_bins ({max_bins})"
        )  # pragma: no cover
    return num_bins


def _check_for_sample_sizes_less_than_two(xs: Sequence[Sequence[float]]) -> None:
    for idx, x in enumerate(xs):
        if len(x) < 2:
            raise ValueError(
                f"xs[{idx}] has length {len(x)}. It must have at least 2 " f"elements."
            )  # pragma: no cover


def generate_hists(
    *xs: Sequence[float],
    max_bins: int = 50,
    num_bins: Optional[int] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
) -> Generator[str, None, None]:
    """Yields histogram strings for each set of samples.

    It will ensure that all histograms are aligned (have the same number of bins and
    ranges).

    :param xs: The sets of samples to make histograms from.
    :param max_bins: The maximum number of bins to use. Determines the maximum length
    of the yielded strings.
    :param num_bins: The number of bins to use. If None, it will be computed from the
    data.
    :param min_value: Where the histogram should start. If None, it will be computed
    from the data.
    :param max_value: Where the histogram should end. If None, it will be computed from
    the data.
    :raises ValueError: If num_bins > max_bins or min_value > max_value.
    """
    if len(xs) == 0:
        return

    _check_for_sample_sizes_less_than_two(xs)

    num_bins = _deduce_num_bins(xs, max_bins=max_bins, num_bins=num_bins)
    min_value, max_value = _deduce_range(xs, min_value=min_value, max_value=max_value)

    for x in xs:
        hist, bin_edges = np.histogram(x, bins=num_bins, range=(min_value, max_value))
        # scales from [0, max(hist)] to [0, num_drawing_chars-1]
        max_count = np.max(hist)
        if max_count == 0:
            scaling_factor = 0
        else:
            scaling_factor = (_NUM_DRAWING_CHARS - 1) / np.max(hist)
        char_indexes = np.round(hist * scaling_factor).astype(int)
        yield "".join(_DRAWING_CHARS[char_indexes])


def generate_annotated_hists(
    *xs: Sequence[float],
    max_bins: int = 50,
    num_bins: Optional[int] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    annotations: Annotations = Annotations(0),
    **named_xs: Sequence[float],
) -> Generator[List[str], None, None]:
    """Yields a histogram with annotations for each set of samples

    Depending on the style, it yields a header first

    It will ensure that all histograms are aligned (have the same number of bins and
    ranges).

    :param xs: The sets of samples to make histograms from.
    :param max_bins: The maximum number of bins to use. Determines the maximum length
    of the histogram string.
    :param num_bins: The number of bins to use. If None, it will be computed from the
    data.
    :param min_value: Where the histogram should start. If None, it will be computed
    from the data.
    :param max_value: Where the histogram should end. If None, it will be computed from
    the data.
    :param annotations: The annotations to add to each histogram such as
     mean/std/min/max/n.
    :param named_xs: The sets of values to make histograms from. The keys are used as
    names.
    :raises ValueError: If num_bins > max_bins or min_value > max_value
    or both xs and named_xs were specified.
    """
    if len(xs) > 0 and len(named_xs) > 0:
        raise ValueError(
            f"Can't have both unnamed and named arguments. "
            f"You passed {xs} and {named_xs}"
        )  # pragma: no cover

    names: Sequence[str]
    if len(named_xs) > 0:
        xs = cast(Tuple[Sequence[float]], named_xs.values())
        names = cast(Sequence[str], named_xs.keys())
        show_names = True
    else:
        names = [""] * len(xs)
        show_names = False

    for x, name, hist_str in zip(
        xs,
        names,
        generate_hists(
            *xs,
            max_bins=max_bins,
            num_bins=num_bins,
            max_value=max_value,
            min_value=min_value,
        ),
    ):
        hist_line = [hist_str]

        if Annotations.ADD_MEAN in annotations:
            hist_line.append(f"{np.mean(x):.2f}")

        if Annotations.ADD_STD in annotations:
            hist_line.append(f"±{np.std(x):.2f}")

        if Annotations.ADD_NUM_VALUES in annotations:
            hist_line.append(f"{len(x)}")

        if show_names:
            hist_line.append(name)

        yield hist_line


def make_header(annotations: Annotations, add_names_column: bool) -> List[str]:
    """Makes a header with the given annotations to print above annotated histograms."""
    header = ["dist"]

    if Annotations.ADD_MEAN in annotations:
        header.append("mean")

    if Annotations.ADD_STD in annotations:
        header.append("std")

    if Annotations.ADD_NUM_VALUES in annotations:
        header.append("n")

    if Annotations.ADD_MIN in annotations:
        header.append("min")

    if Annotations.ADD_MAX in annotations:
        header.append("max")

    if add_names_column:
        header.append("name")

    return header


def make_min_max_footer(
    *xs: Sequence[float],
    width: int,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    **named_xs: Sequence[float],
) -> str:
    """Makes a footer with the min and max values of the given samples.

    To be printed below and unannotated histogram.

    :param xs: The sets of samples to make histograms from.
    :param width: The width of the histogram in chars.
    :param min_value: Where the histogram should start. If None, it will be computed
    from the data.
    :param max_value: Where the histogram should end. If None, it will be computed from
    the data.
    """
    if len(named_xs) > 0:
        xs = cast(tuple, named_xs.values())

    if len(xs) == 0:
        return " " * width

    min_value, max_value = _deduce_range(xs, min_value=min_value, max_value=max_value)

    min_str = f"{min_value:.2f}"
    max_str = f"{max_value:.2f}"
    return min_str + " " * max(1, (width - len(min_str) - len(max_str) - 4)) + max_str
