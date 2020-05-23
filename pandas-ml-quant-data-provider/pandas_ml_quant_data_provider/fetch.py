from typing import List, Callable, Dict, Any, Tuple, Iterable

import pandas as pd

from pandas_ml_common.utils import call_callable_dynamic_args, add_multi_index, inner_join
from pandas_ml_quant_data_provider.provider import PROVIDER_MAP


def fetch_timeseries(providers: Dict[Callable[[Any], pd.DataFrame], List[str]],
                     multi_index: bool = None,
                     ffill: bool = False,
                     **kwargs):
    symbol_type = (List, Tuple, Iterable)
    expected_frames = sum(len(s) if isinstance(s, symbol_type) else 1 for s in providers.values())
    df = None

    if multi_index is None and expected_frames > 1:
        multi_index = True

    for provider, symbols in providers.items():
        # make sure provider is an actual provider -> a callable
        if not callable(provider):
            provider = PROVIDER_MAP[provider]

        # make sure the symbols are iterable -> wrap single symbols into a list
        if not isinstance(symbols, symbol_type):
            symbols = [symbols]

        # fetch all symbols of all providers (later we could do this in parallel)
        for symbol in symbols:
            _df = call_callable_dynamic_args(provider, symbol, multi_index=multi_index, **kwargs)

            if _df is None:
                continue

            if multi_index and not isinstance(_df.columns, pd.MultiIndex):
                _df = add_multi_index(_df, symbol, True)

            if df is None:
                df = _df
            else:
                df = inner_join(df, _df, force_multi_index=multi_index, ffill=ffill)

    return df

