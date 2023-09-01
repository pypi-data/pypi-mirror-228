#!/usr/bin/env python3

"""
** Interactive window for a specific edge properties. **
--------------------------------------------------------
"""

import math

from cutcutcodec.gui.base import CutcutcodecWidget



def edge_properties(parent: CutcutcodecWidget, edge_name: tuple[str, str, str]) -> str:
    """
    ** Serach the content of the tool tip of this edge. **
    """
    stream = parent.app.tree_edge(edge_name)
    properties = {}

    # the general type
    properties["Type"] = stream.type.title()

    # beginning
    beginning = float(stream.beginning)
    if beginning == math.inf:
        beginning = "infinite"
    else:
        beginning = (
            f"{round(beginning//3600):0>2}:{round(beginning%3600//60):0>2}:{beginning%60:.3f} "
            f"({stream.beginning} seconds)"
        )
    properties["Beginning"] = beginning

    # duration
    duration = float(stream.duration)
    if duration == math.inf:
        duration = "infinite"
    else:
        duration = (
            f"{round(duration//3600):0>2}:{round(duration%3600//60):0>2}:{duration%60:.3f} "
            f"({stream.duration} seconds)"
        )
    properties["Duration"] = duration

    # time continuous
    continuous = {True: "yes", False: "no"}[stream.is_time_continuous]
    properties["Time is continuous"] = continuous

    # space continuous
    if stream.type == "video":
        continuous = {True: "yes", False: "no"}[stream.is_space_continuous]
        properties["Space is continuous"] = continuous

    # channels
    if stream.type == "audio":
        properties["Profile"] = (
            f"{stream.profile.name} "
            f"({'+'.join(n for n, d in stream.profile.channels)})"
        )

    return "<br>".join(f"{k}: {v}" for k, v in properties.items())
