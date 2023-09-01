import pandas as pd
import uuid

from sempy.relationships._multiplicity import Multiplicity

from typing import Dict, List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from sempy.fabric import FabricDataFrame


def _get_relationships(named_dataframes: Dict[str, "FabricDataFrame"]) -> pd.DataFrame:

    from sempy.fabric import FabricDataFrame

    relationship_tuples: List[Tuple] = []

    for name, df in named_dataframes.items():
        if not isinstance(df, FabricDataFrame):
            raise TypeError(f"Unexpected type {type(df)} for '{name}': not an FabricDataFrame")
        if df.column_metadata:
            for col, metadata in df.column_metadata.items():
                rel_metadata = metadata.get("relationship")
                if rel_metadata:
                    if rel_metadata['multiplicity'] not in Multiplicity._valid_multiplicities:
                        raise ValueError(f"Invalid multiplicity '{rel_metadata['multiplicity']}', which must be one of {Multiplicity._valid_multiplicities}")
                    relationship_tuples.append((
                        rel_metadata['multiplicity'],
                        name,
                        col,
                        rel_metadata['to_table'],
                        rel_metadata['to_column']
                    ))

    return pd.DataFrame(
        relationship_tuples,
        columns=[
            'Multiplicity',
            'From Table',
            'From Column',
            'To Table',
            'To Column'
        ]
    )


def is_valid_uuid(val: str):
    try:
        uuid.UUID(val)
        return True
    except ValueError:
        return False
