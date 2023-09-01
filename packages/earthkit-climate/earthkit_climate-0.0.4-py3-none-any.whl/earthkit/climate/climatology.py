import typing as T

import xarray as xr

from . import aggregate


def mean(
    dataarray: T.Union[xr.Dataset, xr.DataArray],
    frequency: str = None,
    bin_widths: int = None,
    time_dim: str = "time",
) -> xr.DataArray:
    """
    Calculate the climatological mean.

    Parameters
    ----------
    dataarray : xr.DataArray
        The DataArray over which to calculate the climatological mean. Must
        contain a `time` dimension.
    frequency : str (optional)
        Valid options are `day`, `week` and `month`.
    bin_widths : int or list (optional)
        If `bin_widths` is an `int`, it defines the width of each group bin on
        the frequency provided by `frequency`. If `bin_widths` is a sequence
        it defines the edges of each bin, allowing for non-uniform bin widths.

    Returns
    -------
    xr.DataArray
    """
    grouped_data = aggregate._groupby_time(
        dataarray, frequency=frequency, bin_widths=bin_widths, time_dim=time_dim
    )
    return aggregate.reduce(grouped_data, dim=time_dim)


def stdev(
    dataarray: T.Union[xr.Dataset, xr.DataArray],
    frequency: str = None,
    bin_widths: int = None,
    time_dim: str = "time",
) -> xr.DataArray:
    """
    Calculate of the climatological standard deviation.

    Parameters
    ----------
    dataarray : xr.DataArray
        The DataArray over which to calculate the climatological standard deviation.
        Must contain a `time` dimension.
    frequency : str (optional)
        Valid options are `day`, `week` and `month`.
    bin_widths : int or list (optional)
        If `bin_widths` is an `int`, it defines the width of each group bin on
        the frequency provided by `frequency`. If `bin_widths` is a sequence
        it defines the edges of each bin, allowing for non-uniform bin widths.

    Returns
    -------
    xr.DataArray
    """
    grouped_data = aggregate._groupby_time(dataarray, frequency, bin_widths)
    return aggregate.reduce(grouped_data, how="std", dim=time_dim)


def median(dataarray: T.Union[xr.Dataset, xr.DataArray], **kwargs) -> xr.DataArray:
    """
    Calculate the climatological median.

    Parameters
    ----------
    dataarray : xr.DataArray
        The DataArray over which to calculate the climatological median. Must
        contain a `time` dimension.
    frequency : str (optional)
        Valid options are `day`, `week` and `month`.
    bin_widths : int or list (optional)
        If `bin_widths` is an `int`, it defines the width of each group bin on
        the frequency provided by `frequency`. If `bin_widths` is a sequence
        it defines the edges of each bin, allowing for non-uniform bin widths.

    Returns
    -------
    xr.DataArray
    """
    result = quantiles(dataarray, [0.5], **kwargs)
    return result.isel(quantile=0)


def max(
    dataarray: T.Union[xr.Dataset, xr.DataArray],
    frequency: str = None,
    bin_widths: int = None,
    time_dim: str = "time",
) -> xr.DataArray:
    """
    Calculate the climatological maximum.

    Parameters
    ----------
    dataarray : xr.DataArray
        The DataArray over which to calculate the climatological mean. Must
        contain a `time` dimension.
    frequency : str (optional)
        Valid options are `day`, `week` and `month`.
    bin_widths : int or list (optional)
        If `bin_widths` is an `int`, it defines the width of each group bin on
        the frequency provided by `frequency`. If `bin_widths` is a sequence
        it defines the edges of each bin, allowing for non-uniform bin widths.

    Returns
    -------
    xr.DataArray
    """
    grouped_data = aggregate._groupby_time(dataarray, frequency, bin_widths)
    return aggregate.reduce(grouped_data, how="max", dim=time_dim)


def min(
    dataarray: T.Union[xr.Dataset, xr.DataArray],
    frequency: str = None,
    bin_widths: int = None,
    time_dim: str = "time",
) -> xr.DataArray:
    """
    Calculate the climatological minimum.

    Parameters
    ----------
    dataarray : xr.DataArray
        The DataArray over which to calculate the climatological mean. Must
        contain a `time` dimension.
    frequency : str (optional)
        Valid options are `day`, `week` and `month`.
    bin_widths : int or list (optional)
        If `bin_widths` is an `int`, it defines the width of each group bin on
        the frequency provided by `frequency`. If `bin_widths` is a sequence
        it defines the edges of each bin, allowing for non-uniform bin widths.

    Returns
    -------
    xr.DataArray
    """
    grouped_data = aggregate._groupby_time(dataarray, frequency, bin_widths)
    return aggregate.reduce(grouped_data, how="min", dim=time_dim)


def quantiles(
    dataarray: xr.DataArray,
    quantiles: list,
    frequency: str = None,
    bin_widths: int = None,
    skipna: bool = False,
    time_dim: str = "time",
    **kwargs,
) -> xr.DataArray:
    """
    Calculate a set of climatological quantiles.

    Parameters
    ----------
    dataarray : xr.DataArray
        The DataArray over which to calculate the climatological quantiles. Must
        contain a `time` dimension.
    quantiles : list
        The list of climatological quantiles to calculate.
    frequency : str (optional)
        Valid options are `day`, `week` and `month`.
    bin_widths : int or list (optional)
        If `bin_widths` is an `int`, it defines the width of each group bin on
        the frequency provided by `frequency`. If `bin_widths` is a sequence
        it defines the edges of each bin, allowing for non-uniform bin widths.

    Returns
    -------
    xr.DataArray
    """
    grouped_data = aggregate._groupby_time(
        dataarray.chunk({time_dim: -1}), frequency, bin_widths
    )
    results = []
    for quantile in quantiles:
        results.append(
            grouped_data.quantile(
                q=quantile,
                dim=time_dim,
                skipna=skipna,
                **kwargs,
            )
        )
    result = xr.concat(results, dim="quantile")
    return result


def percentiles(
    dataarray: xr.DataArray,
    percentiles: list,
    **kwargs,
) -> xr.DataArray:
    """
    Calculate a set of climatological percentiles.

    Parameters
    ----------
    dataarray : xr.DataArray
        The DataArray over which to calculate the climatological percentiles. Must
        contain a `time` dimension.
    percentiles : list
        The list of climatological percentiles to calculate.
    frequency : str (optional)
        Valid options are `day`, `week` and `month`.
    bin_widths : int or list (optional)
        If `bin_widths` is an `int`, it defines the width of each group bin on
        the frequency provided by `frequency`. If `bin_widths` is a sequence
        it defines the edges of each bin, allowing for non-uniform bin widths.

    Returns
    -------
    xr.DataArray
    """
    quantiles = [p * 1e-2 for p in percentiles]
    quantile_data = quantiles(
        dataarray,
        quantiles,
        **kwargs,
    )
    result = quantile_data.assign_coords(percentile=("quantile", percentiles))
    result = result.swap_dims({"quantile": "percentile"})
    result = result.drop("quantile")
    return result


def anomaly(
    dataarray: xr.DataArray,
    climatology: xr.DataArray = None,
    climatology_range: tuple = (None, None),
    frequency: str = None,
    bin_widths: int = None,
):
    """
    Calculate the anomaly from a reference climatology.

    Parameters
    ----------
    dataarray : xr.DataArray
        The DataArray over which to calculate the anomaly from the reference
        climatology. Must contain a `time` dimension.
    climatology :  (xr.DataArray, optional)
        Reference climatology data against which the anomaly is to be calculated.
        If not provided then the climatological mean is calculated from dataarray.
    climatology_range : (list or tuple, optional)
        Start and end year of the period to be used for the reference climatology. Default
        is to use the entire time-series.
    frequency : str (optional)
        Valid options are `day`, `week` and `month`.
    bin_widths : int or list (optional)
        If `bin_widths` is an `int`, it defines the width of each group bin on
        the frequency provided by `frequency`. If `bin_widths` is a sequence
        it defines the edges of each bin, allowing for non-uniform bin widths.

    Returns
    -------
    xr.DataArray
    """
    if climatology is None:
        if all(c_r is not None for c_r in climatology_range):
            selection = dataarray.sel(time=slice(*climatology_range))
        else:
            selection = dataarray
        climatology = mean(selection, frequency=frequency, bin_widths=bin_widths)
    anomaly = aggregate._groupby_time(dataarray, frequency, bin_widths) - climatology
    anomaly.assign_attrs(dataarray.attrs)

    if "standard_name" in anomaly.attrs:
        anomaly.attrs["standard_name"] += "_anomaly"
    if "long_name" in anomaly.attrs:
        anomaly.attrs["long_name"] += " anomaly"

    return anomaly
