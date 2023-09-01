import pandas as pd
import warnings
from pandas.core.dtypes.common import is_dtype_equal


def _pandas_merge_cast(left_df, left_on, right_df, right_on, relationship=None, warn=True):

    if not isinstance(left_on, str) or not isinstance(right_on, str):
        raise TypeError(f"Unexpected types {type(left_on)} and {type(right_on)}: not strings")

    string_types = ["string", "unicode", "mixed", "bytes", "empty"]

    # Try to cast some common type issues to make pandas behave more nicely
    if not is_dtype_equal(left_df[left_on], right_df[right_on]):
        left_dtype = pd.api.types.infer_dtype(left_df[left_on])
        right_dtype = pd.api.types.infer_dtype(right_df[right_on])
        msg = f"Mismatching dtypes in merging along relationship {relationship}."
        if (left_dtype in string_types):
            if (right_dtype in string_types):
                # both are string
                pass
            else:
                # left is string but right is not
                if warn:
                    warnings.warn(msg)
                right_df = right_df.astype({right_on: str})

        elif right_dtype in string_types:
            # right is string but left is not
            if warn:
                warnings.warn(msg)
            left_df = left_df.astype({left_on: str})

    return left_df, right_df
