#!/usr/bin/env python3

"""
** Allows to delete the obsolete node cache of the graph. **
-------------------------------------------------------------
"""

import itertools

import networkx

from cutcutcodec.core.optimisation.cache.hashes.graph import compute_graph_items_hash



def clean_graph(graph: networkx.MultiDiGraph) -> networkx.MultiDiGraph:
    """
    ** Update inplace the `cache` attribute of each nodes of the graph. **

    Parameters
    ----------
    graph : networkx.MultiDiGraph
        The assembly graph.

    Returns
    -------
    updated_graph : networkx.MultiDiGraph
        The same graph with the updated `cache` node attribute.
        The underground data are shared, operate in-place.

    Examples
    --------
    >>> from pprint import pprint
    >>> from cutcutcodec.core.classes.container import ContainerOutput
    >>> from cutcutcodec.core.compilation.tree_to_graph import tree_to_graph
    >>> from cutcutcodec.core.filters.basic.meta.subclip import FilterSubclip
    >>> from cutcutcodec.core.generation.audio.noise import GeneratorAudioNoise
    >>> from cutcutcodec.core.optimisation.cache.clean.graph import clean_graph
    >>> container_out = ContainerOutput(
    ...     FilterSubclip(GeneratorAudioNoise.default().out_streams, 0, 1).out_streams
    ... )
    >>> graph = tree_to_graph(container_out)
    >>> pprint(dict(clean_graph(graph).nodes("cache")))
    {'container_output_1': ('82175bd070ae0dc4a5660ece58769ac6', {}),
     'filter_subclip_1': ('24e06e1439ecde8cffaad3cb6ce94c17', {}),
     'generator_audio_noise_1': ('b60c0f567ed5ef0ded54d08ea1f6c80a', {})}
    >>> pprint(list(graph.edges(keys=True, data=True)))
    [('filter_subclip_1',
      'container_output_1',
      '0->0',
      {'cache': ('24e06e1439ecde8cffaad3cb6ce94c17|0', {})}),
     ('generator_audio_noise_1',
      'filter_subclip_1',
      '0->0',
      {'cache': ('b60c0f567ed5ef0ded54d08ea1f6c80a|0', {})})]
    >>> for _, data in graph.nodes(data=True):
    ...     data["cache"][1]["key"] = "value"
    ...
    >>> for *_, data in graph.edges(keys=True, data=True):
    ...     data["cache"][1]["key"] = "value"
    ...
    >>> graph.nodes["filter_subclip_1"]["state"]["duration_max"] = "2"
    >>> pprint(dict(clean_graph(graph).nodes("cache")))
    {'container_output_1': ('0e8acfd5b57aadc31921d9fbd9412f6c', {}),
     'filter_subclip_1': ('aeeb918de83807f1cfc64605e885bf66', {}),
     'generator_audio_noise_1': ('b60c0f567ed5ef0ded54d08ea1f6c80a',
                                 {'key': 'value'})}
    >>> pprint(list(graph.edges(keys=True, data=True)))
    [('filter_subclip_1',
      'container_output_1',
      '0->0',
      {'cache': ('aeeb918de83807f1cfc64605e885bf66|0', {})}),
     ('generator_audio_noise_1',
      'filter_subclip_1',
      '0->0',
      {'cache': ('b60c0f567ed5ef0ded54d08ea1f6c80a|0', {'key': 'value'})})]
    >>>
    """
    new_hashes = compute_graph_items_hash(graph) # assertions are done here
    edges_iter = (((s, d, k), data) for s, d, k, data in graph.edges(keys=True, data=True))
    for item, data in itertools.chain(graph.nodes(data=True), edges_iter):
        new_hash = new_hashes[item]
        if "cache" not in data or data["cache"][0] != new_hash:
            data["cache"] = (new_hashes[item], {})
    return graph
