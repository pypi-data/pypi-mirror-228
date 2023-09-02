"""
This module contains the function to get the number of objects per rejection reason. The rejection reason is given in
the description of the ``AMPEL`` ``T2DustEchoEval`` unit output.

* :func:`get_rejection_reason` gets the number of objects per rejection reason
"""

import logging
import json
import numpy as np
import pandas as pd

from timewise_sup.mongo import DatabaseConnector


logger = logging.getLogger(__name__)


def get_rejection_reason(
        base_name: str,
        database_name: str
) -> dict:
    """
    Get the number of objects per rejection reason. The rejection reason is given in the description of the
    ``AMPEL`` ``T2DustEchoEval`` unit output.

    :param base_name: base name of the wise data
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :return: dictionary with the rejection reason as key and the number of objects as value
    :rtype: dict
    """
    logger.info(f"getting rejection reason for {base_name}")
    rejected = (
        "No further investigation",
        "1_maybe_interesting",
        "2_maybe_interesting",
        "3", "3_maybe_interesting",
        "4", "4_maybe_interesting"
    )
    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    ids = database_connector.get_ids(rejected)
    desc = database_connector.get_t2_dust_echo_eval_descriptions(ids)
    desc_counts = desc.description.value_counts()  # type: pd.Series

    individual_reasons = dict()
    for ir, n in desc_counts.items():
        for irsi in ir.split(", "):
            if irsi not in individual_reasons:
                individual_reasons[irsi] = n
            else:
                individual_reasons[irsi] += n

    # sort by number
    individual_reasons_df = pd.DataFrame.from_dict(individual_reasons, orient="index").sort_values(0, ascending=False)

    # find individual reasons in descriptions
    accept = ['Baseline before excess region', 'Excess region exists']
    masks: dict[str, bool] = {
        rt: desc_counts.index.str.contains(rt)
        for rt in individual_reasons_df.index if rt not in accept
    }

    # find individual reasons that exclude the object with descending order of appearance
    masks_exclusive = {rt: im & ~np.logical_or.reduce(list(masks.values())[:i])
                       for i, (rt, im) in enumerate(masks.items())}

    # find the corresponding numbers of objects
    numbers_exclusive = {rt: int(desc_counts[m].sum()) for rt, m in masks_exclusive.items()}
    logger.debug(json.dumps(numbers_exclusive, indent=4))

    return numbers_exclusive
