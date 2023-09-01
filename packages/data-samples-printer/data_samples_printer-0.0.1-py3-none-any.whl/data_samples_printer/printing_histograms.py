from typing import Optional, Sequence

from data_samples_printer.making_histograms import (
    Annotations,
    generate_annotated_hists,
    make_header,
    make_min_max_footer,
)


def print_hist(
    *xs: Sequence[float],
    max_bins: int = 50,
    num_bins: Optional[int] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    annotations: Annotations = Annotations(0),
    markdown_mode: bool = False,
    print_header: bool = False,
    print_footer: bool = False,
    **named_xs: Sequence[float],
) -> None:
    header = make_header(annotations, add_names_column=len(named_xs) > 0)
    annotated_hists = list(
        generate_annotated_hists(
            *xs,
            max_bins=max_bins,
            num_bins=num_bins,
            min_value=min_value,
            max_value=max_value,
            annotations=annotations,
            **named_xs,
        )
    )

    join_str = " | " if markdown_mode else " "

    if print_header:
        print(join_str.join(header))

    if markdown_mode:
        if print_header:
            # Print line below header to make markdown-compatible tables
            print("-|-".join("-" * len(i) for i in header))

        # Wrap the histogram in backticks and ONE EIGHTH BLOCKs
        # In markdown this enables fixed with rendering.
        # Unfortunately, the backticks are not always enough, and some spaces are eaten,
        # so we add the ONE EIGHTH BLOCKs to make sure the histogram is rendered
        # correctly.
        for idx, (hist, *_) in enumerate(annotated_hists):
            annotated_hists[idx][0] = f"`▕{hist}▏`"

    print("\n".join(join_str.join(hl) for hl in annotated_hists))

    if print_footer and len(annotated_hists) > 0:
        footer = make_min_max_footer(
            *xs,
            min_value=min_value,
            max_value=max_value,
            width=len(annotated_hists[0][0]),
            **named_xs,
        )
        if markdown_mode:
            print(f"`▕{footer}▏`{join_str}")
        else:
            print(footer)


def pprint_hist(
    *xs: Sequence[float],
    max_bins: int = 50,
    num_bins: Optional[int] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    annotations: Annotations = Annotations.ADD_MEAN | Annotations.ADD_STD,
    markdown_mode: bool = False,
    print_header: bool = False,
    print_footer: bool = False,
    **named_xs: Sequence[float],
) -> None:  # pragma: no cover
    if markdown_mode:
        print_footer = True
        print_header = True
    print_hist(
        *xs,
        max_bins=max_bins,
        num_bins=num_bins,
        min_value=min_value,
        max_value=max_value,
        annotations=annotations,
        markdown_mode=markdown_mode,
        print_header=print_header,
        print_footer=print_footer,
        **named_xs,
    )


def mprint_hist(
    *xs: Sequence[float],
    max_bins: int = 50,
    num_bins: Optional[int] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    annotations: Annotations = Annotations.ADD_MEAN | Annotations.ADD_STD,
    print_header: bool = False,
    print_footer: bool = False,
    **named_xs: Sequence[float],
) -> None:
    pprint_hist(
        *xs,
        max_bins=max_bins,
        num_bins=num_bins,
        min_value=min_value,
        max_value=max_value,
        annotations=annotations,
        markdown_mode=True,
        print_header=print_header,
        print_footer=print_footer,
        **named_xs,
    )  # pragma: no cover
