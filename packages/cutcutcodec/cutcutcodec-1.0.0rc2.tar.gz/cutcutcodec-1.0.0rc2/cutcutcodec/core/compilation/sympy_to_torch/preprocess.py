#!/usr/bin/env python3

"""
** Prepares the work for the Printer, decompose and analyse. **
---------------------------------------------------------------
"""

import itertools
import re

from sympy.core.basic import Basic
from sympy.core.containers import Tuple
from sympy.core.numbers import NumberSymbol, Zero
from sympy.core.symbol import Symbol
from sympy.functions.special.delta_functions import DiracDelta
from sympy.simplify.cse_main import cse



def _expr_to_atomic(expr: Basic, *, _symbols=None) -> list[tuple[Symbol, Basic]]:
    """
    ** Apply ``cse`` and split the sub patterns. **

    Parameters
    ----------
    expr : sympy.core.basic.Basic
        The sympy expression to split.

    Returns
    -------
    replacements : list of (Symbol, expression) pairs
        All of the common subexpressions that were replaced.
        All subexpressions are atomic.

    Examples
    --------
    >>> from pprint import pprint
    >>> from sympy.abc import x, y, z
    >>> from sympy.functions.elementary.trigonometric import sin
    >>> from cutcutcodec.core.compilation.sympy_to_torch.preprocess import _expr_to_atomic
    >>> exp = (x + y - z - 1)**2 * ((x + y - z)/(x + 1) + (x + y - z - 1)**2) * (x + 1)**(x + y - z)
    >>> pprint(_expr_to_atomic(exp)) # case cse and sub-patterns
    [(_0, x + 1),
     (_4, -z),
     (_1, _4 + x + y),
     (_5, _1 - 1),
     (_2, _5**2),
     (_6, _0**_1),
     (_9, 1/_0),
     (_8, _1*_9),
     (_7, _2 + _8),
     (_3, _2*_6*_7)]
    >>> pprint(_expr_to_atomic(sin(sin(sin(1))))) # case replace in func
    [(_2, sin(1)), (_1, sin(_2)), (_0, sin(_1))]
    >>>
    """
    if _symbols is None:
        _symbols = iter(Symbol(f"_{i}") for i in itertools.count())
        rep, final = cse(expr, symbols=_symbols, order="none", list=False) # fastest as possible
        rep.append((next(_symbols), final))
    else: # if cse is already called
        rep = [(next(_symbols), expr)]

    atom_rep = []
    for var, sub_expr in rep:
        if sub_expr.is_Atom:
            atom_rep.append((var, sub_expr))
            continue
        subs = {}
        for arg in sub_expr.args:
            if not arg.is_Atom:
                atom_rep += _expr_to_atomic(arg, _symbols=_symbols)
                subs[arg] = atom_rep[-1][0]
        if subs:
            sub_expr = sub_expr.xreplace(subs)
        atom_rep.append((var, sub_expr))
    return atom_rep


def _get_args(symb_expr: list[tuple[Symbol, Basic]]) -> tuple[set[Symbol], set[Symbol]]:
    """
    ** Search the parameters and islotate wich one are changing inplace. **

    Complexity o(n).

    Parameters
    ----------
    symb_expr : list[tuple[sympy.core.symbol.Symbol, sympy.core.basic.Basic]]
        The list of symbols and atomic expressions.

    Returns
    -------
    all_args : set[sympy.core.symbol.Symbol]
        All the input arguments
    args_no_safe : set[sympy.core.symbol.Symbol]
        All the non copy safe arguments.

    Examples
    --------
    >>> from sympy.abc import x, y, z
    >>> from sympy.core.symbol import symbols
    >>> from cutcutcodec.core.compilation.sympy_to_torch.preprocess import _get_args
    >>> _0, _1, _2, _3, _4, _5, _6, _7, _8, _9 = symbols("_:10")
    >>> symb_expr = [
    ...     (_0, x + 1),
    ...     (_4, -z),
    ...     (_1, _4 + x + y),
    ...     (_5, _1 - 1),
    ...     (_2, _5**2),
    ...     (_6, _0**_1),
    ...     (_9, 1/_0),
    ...     (_8, _1*_9),
    ...     (_7, _2 + _8),
    ...     (_3, _2*_6*_7),
    ... ]
    >>> sorted(_get_args(symb_expr)[1], key=str)
    []
    >>> symb_expr = [
    ...     (_0, x + 1),
    ...     (z, -z),
    ...     (z, x + y + z),
    ...     (x, z - 1),
    ...     (x, x**2),
    ...     (y, _0**z),
    ...     (_0, 1/_0),
    ...     (z, _0*z),
    ...     (z, x + z),
    ...     (x, x*y*z),
    ... ]
    >>> sorted(_get_args(symb_expr)[1], key=str)
    [x, y, z]
    >>>
    """
    all_args = set()
    inplace = set()
    no_args = set()
    for symb, expr in symb_expr:
        symbs = expr.free_symbols
        all_args |= symbs - no_args
        if symb in all_args and expr != symb:
            inplace.add(symb)
        else:
            no_args.add(symb)
    return all_args, inplace


def _isolate_cst_dyn(
    symb_expr: list[tuple[Symbol, Basic]], cst_args: set[Symbol]
) -> tuple[list[tuple[Symbol, Basic]], list[tuple[Symbol, Basic]]]:
    """
    ** Isolate the constant subexpressions. **

    Complexity o(n).

    Parameters
    ----------
    symb_expr : list[tuple[sympy.core.symbol.Symbol, sympy.core.basic.Basic]]
        Returned value of ``_expr_to_atomic``.
    cst_args : set[sympy.core.symbol.Symbol]
        The constants input parameters.
        The subexpressions of this parameters will be cached.

    Returns
    -------
    cst_tree : list[tuple[sympy.core.symbol.Symbol, sympy.core.basic.Basic]]
        The graph to compute the constant sub expressions.
        The last value is a ``sympy.core.containers.Tuple``.
    dyn_tree : list[tuple[sympy.core.symbol.Symbol, sympy.core.basic.Basic]]
        The main tree containing only dynamic expressions.

    Examples
    --------
    >>> from pprint import pprint
    >>> from sympy.abc import x, y, z
    >>> from sympy.core.symbol import symbols
    >>> from sympy.functions.elementary.trigonometric import sin
    >>> from cutcutcodec.core.compilation.sympy_to_torch.preprocess import _isolate_cst_dyn
    >>> _0, _1, _2, _3, _4, _5, _6, _7, _8, _9 = symbols("_:10")
    >>> symb_expr = [
    ...     (_0, x + 1),
    ...     (_4, -z),
    ...     (_1, _4 + x + y),
    ...     (_5, _1 - 1),
    ...     (_2, _5**2),
    ...     (_6, _0**_1),
    ...     (_9, 1/_0),
    ...     (_8, _1*_9),
    ...     (_7, _2 + _8),
    ...     (_3, _2*_6*_7),
    ... ]
    >>> cst, dyn = _isolate_cst_dyn(symb_expr, {x})
    >>> pprint(cst)
    [(_0, x + 1), (_9, 1/_0), (_, (_0, _9))]
    >>> pprint(dyn)
    [(_4, -z),
     (_1, _4 + x + y),
     (_5, _1 - 1),
     (_2, _5**2),
     (_6, _0**_1),
     (_8, _1*_9),
     (_7, _2 + _8),
     (_3, _2*_6*_7)]
    >>> symb_expr = [(_2, sin(1)), (_1, sin(_2)), (_0, sin(_1))]
    >>> cst, dyn = _isolate_cst_dyn(symb_expr, set())
    >>> cst
    [(_2, sin(1)), (_1, sin(_2)), (_0, sin(_1)), (_, (_0,))]
    >>> dyn
    [(_, _0)]
    >>>
    """
    # detection of cst sub expressions
    csts = set() # contains all the cst sub symbols
    for symb, expr in symb_expr:
        if all(s in cst_args or s in csts for s in expr.free_symbols):
            csts.add(symb) # if no free symbols, it is constant

    # split the constant and the dynamic sub graphs
    cst_tree = []
    dyn_tree = []
    for symb, expr in symb_expr:
        if symb in csts: # if the expression is constant
            cst_tree.append((symb, expr))
        else:
            dyn_tree.append((symb, expr))

    # special case all the tree is constant
    if not dyn_tree:
        dyn_tree.append((Symbol("_"), symb_expr[-1][0]))

    # selection of usefull cst symbols
    final_csts = set()
    final_csts_ordered = []
    for symb, expr in dyn_tree:
        for sub_symb in expr.free_symbols:
            if sub_symb in csts and sub_symb not in final_csts: # we keep the statics parts
                final_csts.add(sub_symb)
                final_csts_ordered.append(sub_symb)
    cst_tree.append((Symbol("_"), Tuple(*final_csts_ordered)))

    return cst_tree, dyn_tree


def _limit_realoc(
    symb_expr: list[tuple[Symbol, Basic]], shapes: dict[Symbol, frozenset[Symbol]]
) -> dict[Symbol, set[Symbol]]:
    """
    ** Optimises memory by reusing as many old variables as possible. **

    Complexity o(n**2).
    The ``sympy.core.containers.Tuple`` expressions are not considered.

    Parameters
    ----------
    symb_expr : list[tuple[sympy.core.symbol.Symbol, sympy.core.basic.Basic]]
        The list of symbols and atomic expressions.
    shapes : dict[sympy.core.symbol.Symbol, frozenset[sympy.core.symbol.Symbol]]
        Transmitted to ``cutcutcodec.core.compilation.sympy_to_torch.preprocess._shapes``.

    Returns
    -------
    alloc : dict[sympy.core.symbol.Symbol, set[sympy.core.symbol.Symbol]]
        The intermediate variables to be declared and their respective dimensions.
    symb_expr : list[tuple[sympy.core.symbol.Symbol, sympy.core.basic.Basic]]
        The new equivalent tree that minimize the realocation and take care of the shapes.

    Examples
    --------
    >>> from pprint import pprint
    >>> from sympy.abc import x, y, z
    >>> from sympy.core.symbol import symbols
    >>> from cutcutcodec.core.compilation.sympy_to_torch.preprocess import _limit_realoc
    >>> _0, _1, _2, _3, _4, _5, _6, _7, _8, _9 = symbols("_:10")
    >>> symb_expr = [
    ...     (_0, x + 1),
    ...     (_4, -z),
    ...     (_1, _4 + x + y),
    ...     (_5, _1 - 1),
    ...     (_2, _5**2),
    ...     (_6, _0**_1),
    ...     (_9, 1/_0),
    ...     (_8, _1*_9),
    ...     (_7, _2 + _8),
    ...     (_3, _2*_6*_7),
    ... ]
    >>> alloc, tree = _limit_realoc(symb_expr, {})
    >>> pprint({v: sorted(alloc[v], key=str) for v in sorted(alloc, key=str)}, sort_dicts=False)
    {_0: [x], _1: [x, y, z], _5: [x, y, z], _6: [x, y, z]}
    >>> pprint(tree)
    [(_0, x + 1),
     (z, -z),
     (_1, x + y + z),
     (_5, _1 - 1),
     (_5, _5**2),
     (_6, _0**_1),
     (_0, 1/_0),
     (_1, _0*_1),
     (_1, _1 + _5),
     (_5, _1*_5*_6)]
    >>> alloc, tree = _limit_realoc(symb_expr, {y: frozenset((x,)), z: frozenset((x,))})
    >>> pprint({v: sorted(alloc[v], key=str) for v in sorted(alloc, key=str)}, sort_dicts=False)
    {_0: [x]}
    >>> pprint(tree)
    [(_0, x + 1),
     (z, -z),
     (z, x + y + z),
     (x, z - 1),
     (x, x**2),
     (y, _0**z),
     (_0, 1/_0),
     (z, _0*z),
     (z, x + z),
     (x, x*y*z)]
    >>>
    """
    # find the shape of each intermediary tensors
    shapes = _shapes(symb_expr, shapes)

    # at each step, find the new free sub symbols
    used = [set()]
    for _, expr in reversed(symb_expr):
        used.insert(0, used[0] | expr.free_symbols)
    free = [u1-u2 for u1, u2 in zip(used[:-1], used[1:])] # each step, the useless new vars o(n**2)

    # groups independent variables that can be replaced by a single same variable
    groups = {}
    shape_free = {} # to each shape, associate the free vars of the current step
    for new_free, (symb, expr) in zip(free, symb_expr):
        if isinstance(expr, Tuple): # particular case of tuples
            continue
        # update free vars
        for var in sorted(new_free, key=str, reverse=True): # for repetability
            shape = shapes.get(var, frozenset((var,)))
            shape_free[shape] = shape_free.get(shape, []) # next line, limit inplace of arguments
            shape_free[shape].insert((0 if re.fullmatch(r"_\d+", str(var)) else -1), var)
        # select a free var to reused
        shape = shapes[symb]
        if shape in shape_free:
            groups[symb] = shape_free[shape].pop(0)
            groups[symb] = groups.get(groups[symb], groups[symb]) # {2: 3, 1: 2} to {2: 3, 1: 3}
            if not shape_free[shape]:
                del shape_free[shape]

    # rename and select vars to alloc
    new_tree = [(groups.get(symb, symb), expr.xreplace(groups)) for symb, expr in symb_expr]
    used = {s for s, _ in symb_expr} # when provided shape is not empty
    alloc = {var: set(shape) for var, shape in shapes.items() if var not in groups and var in used}

    return alloc, new_tree


def _rename(
    symb_expr: list[tuple[Symbol, Basic]], subs: dict[Symbol, Symbol], *, return_subs=False
) -> list[tuple[Symbol, Basic]]:
    """
    ** Replace and rename the symbols in canonical order. **

    Complexity o(n).

    Parameters
    ----------
    symb_expr : list[tuple[sympy.core.symbol.Symbol, sympy.core.basic.Basic]]
        The list of symbols and atomic expressions.
    subs : dict[sympy.core.symbol.Symbol, sympy.core.symbol.Symbol]
        The replacement name of some symbols.

    Returns
    -------
    new_tree : list[tuple[sympy.core.symbol.Symbol, sympy.core.basic.Basic]]
        The renamed elements.

    Examples
    --------
    >>> from pprint import pprint
    >>> from sympy.abc import x, y, z
    >>> from sympy.core.symbol import symbols, Symbol
    >>> from cutcutcodec.core.compilation.sympy_to_torch.preprocess import _rename
    >>> _0, _1, _2, _3, _4, _5, _6, _7, _8, _9 = symbols("_:10")
    >>> symb_expr = [
    ...     (_0, x + 1),
    ...     (_4, -z),
    ...     (_1, _4 + x + y),
    ...     (_5, _1 - 1),
    ...     (_2, _5**2),
    ...     (_6, _0**_1),
    ...     (_9, 1/_0),
    ...     (_8, _1*_9),
    ...     (_7, _2 + _8),
    ...     (_3, _2*_6*_7),
    ... ]
    >>> pprint(_rename(symb_expr, {_3: Symbol("rep_1"), _6: Symbol("rep_2")}))
    [(_0, x + 1),
     (_1, -z),
     (_2, _1 + x + y),
     (_3, _2 - 1),
     (_4, _3**2),
     (rep_2, _0**_2),
     (_5, 1/_0),
     (_6, _2*_5),
     (_7, _4 + _6),
     (rep_1, _4*_7*rep_2)]
    >>>
    """
    subs_local = subs.copy()
    renamed_tree = []
    symbols = iter(Symbol(f"_{i}") for i in itertools.count())

    for symb, expr in symb_expr:
        if symb not in subs_local and re.fullmatch(r"_\d+", str(symb)):
            subs_local[symb] = next(symbols)
        renamed_tree.append((subs_local.get(symb, symb), expr.xreplace(subs_local)))

    if return_subs:
        return subs_local, renamed_tree
    return renamed_tree


def _shapes(
    symb_expr: list[tuple[Symbol, Basic]], shapes: dict[Symbol, frozenset[Symbol]]
) -> dict[Symbol, frozenset[Symbol]]:
    r"""
    ** Find the shape of all the sub vars. **

    Complexity o(n).

    Parameters
    ----------
    symb_expr : list[tuple[sympy.core.symbol.Symbol, sympy.core.basic.Basic]]
        The list of symbols and atomic expressions.
    shapes : dict[sympy.core.symbol.Symbol, frozenset[sympy.core.symbol.Symbol]]
        The initials shapes.

    Returns
    -------
    shapes : dict[sympy.core.symbol.Symbol, frozenset[sympy.core.symbol.Symbol]]
        All the shapes, for each intermediate vars, associate the broadcast shape of the tensor.

    Examples
    --------
    >>> from pprint import pprint
    >>> from sympy.abc import x, y, z
    >>> from sympy.core.symbol import symbols
    >>> from cutcutcodec.core.compilation.sympy_to_torch.preprocess import _shapes
    >>> _0, _1, _2, _3, _4, _5, _6, _7, _8, _9 = symbols("_:10")
    >>> symb_expr = [
    ...     (_0, x + 1),
    ...     (_4, -z),
    ...     (_1, _4 + x + y),
    ...     (_5, _1 - 1),
    ...     (_2, _5**2),
    ...     (_6, _0**_1),
    ...     (_9, 1/_0),
    ...     (_8, _1*_9),
    ...     (_7, _2 + _8),
    ...     (_3, _2*_6*_7),
    ... ]
    >>> shapes = _shapes(symb_expr, {})
    >>> pprint({v: sorted(shapes[v], key=str) for v in sorted(shapes, key=str)}, sort_dicts=False)
    {_0: [x],
     _1: [x, y, z],
     _2: [x, y, z],
     _3: [x, y, z],
     _4: [z],
     _5: [x, y, z],
     _6: [x, y, z],
     _7: [x, y, z],
     _8: [x, y, z],
     _9: [x],
     x: [x],
     y: [y],
     z: [z]}
    >>> shapes = _shapes(symb_expr, {y: frozenset((x,)), z: frozenset((x,))})
    >>> pprint({v: sorted(shapes[v], key=str) for v in sorted(shapes, key=str)}, sort_dicts=False)
    {_0: [x],
     _1: [x],
     _2: [x],
     _3: [x],
     _4: [x],
     _5: [x],
     _6: [x],
     _7: [x],
     _8: [x],
     _9: [x],
     x: [x],
     y: [x],
     z: [x]}
    >>>
    """
    all_shapes = shapes.copy()
    for symb, expr in symb_expr:
        free_symbols = expr.free_symbols
        all_shapes[symb] = frozenset.union(
            frozenset(), *(all_shapes.get(s, frozenset((s,))) for s in free_symbols)
        ) # will be used as dictionary key
        for free_symbol in free_symbols:
            all_shapes[free_symbol] = all_shapes.get(free_symbol, frozenset((free_symbol,)))
    return all_shapes


def evalf(expr: Basic) -> Basic:
    """
    ** Numerical eval and simplification of the expression. **

    Parameters
    ----------
    expr : sympy.Expr
        The sympy expression to symplify as numerical evaluable.

    Returns
    -------
    sympy.Expr
        The quite equivalent expression with floats.

    Examples
    --------
    >>> import sympy
    >>> from cutcutcodec.core.compilation.sympy_to_torch.preprocess import evalf
    >>> evalf(sympy.DiracDelta(0))
    0
    >>> evalf(sympy.pi)
    3.1415926535897932384626433832795
    >>>
    """
    assert isinstance(expr, Basic), expr.__class__.__name__
    if isinstance(expr, Tuple):
        return Tuple(*map(evalf, expr))
    if sub := expr.atoms(DiracDelta):
        expr = expr.xreplace({d: Zero() for d in sub})
    if sub := expr.atoms(NumberSymbol):
        expr = expr.xreplace({s: s.evalf(n=32) for s in sub})
    return expr.evalf(n=32)


def preprocess(
    expr: Basic, cst_args: set[Symbol]=None, shapes: dict[Symbol, frozenset[Symbol]]=None
) -> tuple[list[tuple[Symbol, Basic]], dict[Symbol, set[Symbol]], list[tuple[Symbol, Basic]]]:
    """
    ** Decompose and analyse the expression for the printer. **

    Parameters
    ----------
    expr : sympy.core.basic.Basic
        The complete sympy expression to compile.
    cst_args : set[sympy.core.symbol.Symbol], optional
        Arguments that change infrequently enough to be cached.
    shapes : dict[sympy.core.symbol.Symbol, frozenset[sympy.core.symbol.Symbol]], optional
        If some parameters have the same shape, it is possible to give this information
        in order to find a more optimal solution for limited the allocations.
        The keys ares the arguments symbols (not necessarily all), and the values as well.

    Returns
    -------
    tree : dict
        cst_copy : set[sympy.core.symbol.Symbol]
            The arguments that have to be copied before calling the function of the cst tree.
        cst_args : set[sympy.core.symbol.Symbol]
            All the inputs arguments required for the cst tree input.
        cst_alloc : dict[sympy.core.symbol.Symbol, set[sympy.core.symbol.Symbol]]
            The intermediate variables to be declared and their respective dimensions for cst tree.
        cst_tree : list[tuple[sympy.core.symbol.Symbol, typing.Union[sympy.core.basic.Basic, None]]]
            Each steps of the cached function.
        dyn_copy : set[sympy.core.symbol.Symbol]
            The arguments that have to be copied before calling the function of the dyn tree.
        dyn_args : set[sympy.core.symbol.Symbol]
            All the inputs arguments required for the dyn tree input.
        dyn_alloc : dict[sympy.core.symbol.Symbol, set[sympy.core.symbol.Symbol]]
            The intermediate variables to be declared and their respective dimensions for dyn tree.
        dyn_tree : list[tuple[sympy.core.symbol.Symbol, typing.Union[sympy.core.basic.Basic, None]]]
            Each steps of the main function.

    Examples
    --------
    >>> from pprint import pprint
    >>> from sympy.abc import x, y, z
    >>> from cutcutcodec.core.compilation.sympy_to_torch.preprocess import preprocess
    >>> exp = (x + y - z - 1)**2 * ((x + y - z)/(x + 1) + (x + y - z - 1)**2) * (x + 1)**(x + y - z)
    >>> def print_tree(tree):
    ...     print("cst_copy:", sorted(tree["cst_copy"], key=str))
    ...     print("cst_alloc:", {s: sorted(b, key=str) for s, b in tree["cst_alloc"].items()})
    ...     print("cst_tree:")
    ...     pprint(tree["cst_tree"])
    ...     print("dyn_copy:", sorted(tree["dyn_copy"], key=str))
    ...     print("dyn_alloc:", {s: sorted(b, key=str) for s, b in tree["dyn_alloc"].items()})
    ...     print("dyn_tree:")
    ...     pprint(tree["dyn_tree"])
    ...
    >>> tree = preprocess(exp)
    >>> print_tree(tree)
    cst_copy: []
    cst_alloc: {}
    cst_tree:
    [(_, ())]
    dyn_copy: [z]
    dyn_alloc: {_0: [x], _1: [x, y, z], _2: [x, y, z], _3: [x, y, z]}
    dyn_tree:
    [(_0, x + 1),
     (z, -z),
     (_1, x + y + z),
     (_2, _1 - 1),
     (_2, _2**2),
     (_3, _0**_1),
     (_0, 1/_0),
     (_1, _0*_1),
     (_1, _1 + _2),
     (_2, _1*_2*_3)]
    >>>
    >>> tree = preprocess(exp, shapes={y: frozenset((x,)), z: frozenset((x,))})
    >>> print_tree(tree)
    cst_copy: []
    cst_alloc: {}
    cst_tree:
    [(_, ())]
    dyn_copy: [x, y, z]
    dyn_alloc: {_0: [x]}
    dyn_tree:
    [(_0, x + 1),
     (z, -z),
     (z, x + y + z),
     (x, z - 1),
     (x, x**2),
     (y, _0**z),
     (_0, 1/_0),
     (z, _0*z),
     (z, x + z),
     (x, x*y*z)]
    >>>
    >>> tree = preprocess(exp, cst_args={x})
    >>> print_tree(tree)
    cst_copy: [x]
    cst_alloc: {_cst_1: [x]}
    cst_tree:
    [(x, x + 1), (_cst_1, 1/x), (_, (x, _cst_1))]
    dyn_copy: [z]
    dyn_alloc: {_0: [x, y, z], _1: [x, y, z], _2: [x, y, z]}
    dyn_tree:
    [(z, -z),
     (_0, x + y + z),
     (_1, _0 - 1),
     (_1, _1**2),
     (_2, _cst_0**_0),
     (_0, _0*_cst_1),
     (_0, _0 + _1),
     (_1, _0*_1*_2)]
    >>>
    >>> tree = preprocess(exp, cst_args={x}, shapes={y: frozenset((x,)), z: frozenset((x,))})
    >>> print_tree(tree)
    cst_copy: [x]
    cst_alloc: {_cst_1: [x]}
    cst_tree:
    [(x, x + 1), (_cst_1, 1/x), (_, (x, _cst_1))]
    dyn_copy: [_cst_0, x, z]
    dyn_alloc: {}
    dyn_tree:
    [(z, -z),
     (z, x + y + z),
     (x, z - 1),
     (x, x**2),
     (_cst_0, _cst_0**z),
     (z, _cst_1*z),
     (z, x + z),
     (x, _cst_0*x*z)]
    >>> tree = preprocess(exp, cst_args={x, y, z}, shapes={y: frozenset((x,)), z: frozenset((x,))})
    >>> print_tree(tree)
    cst_copy: [x, y, z]
    cst_alloc: {_0: [x]}
    cst_tree:
    [(_0, x + 1),
     (z, -z),
     (z, x + y + z),
     (x, z - 1),
     (x, x**2),
     (y, _0**z),
     (_0, 1/_0),
     (z, _0*z),
     (z, x + z),
     (x, x*y*z),
     (_, (x,))]
    dyn_copy: []
    dyn_alloc: {}
    dyn_tree:
    [(_cst_0, _cst_0)]
    >>>
    """
    assert isinstance(expr, Basic), expr.__class__.__name__
    if cst_args is None:
        cst_args = set()
    else:
        assert isinstance(cst_args, set), cst_args.__class__.__name__
        assert all(isinstance(s, Symbol) for s in cst_args), cst_args
        assert cst_args.issubset(expr.free_symbols), f"{cst_args} not in {expr}"
    if shapes is None:
        shapes = {}
    else:
        assert isinstance(shapes, dict), shapes.__class__.__name__
        assert all(isinstance(k, Symbol) for k in shapes), shapes
        assert all(isinstance(v, frozenset) for v in shapes.values()), shapes
        assert all(all(isinstance(s, Symbol) for s in v) for v in shapes.values()), shapes

    # optimize
    atomic_tree = _expr_to_atomic(expr) # decompose to atomic steps
    cst_tree, dyn_tree = _isolate_cst_dyn(atomic_tree, cst_args) # isolate the cachable operations
    old_names = cst_tree[-1][1]
    cst_alloc, cst_tree = _limit_realoc(cst_tree, _shapes(cst_tree, shapes)) # optimize the memory
    del cst_alloc[Symbol("_")]
    dyn_alloc, dyn_tree = _limit_realoc(
        dyn_tree,
        _shapes(cst_tree[:-1] + list(zip(old_names, cst_tree[-1][1])) + dyn_tree, shapes),
    )

    # rename for human readable
    new_names, cst_tree = _rename(
        cst_tree,
        {
            s: Symbol(f"_cst_{i}")
            for i, s in enumerate(cst_tree[-1][1])
            if re.fullmatch(r"_\d+", str(s))
        },
        return_subs=True
    )
    cst_alloc = {new_names.get(symb, symb): shape for symb, shape in cst_alloc.items()}
    new_names, dyn_tree = _rename(
        dyn_tree,
        {
            s: Symbol(f"_cst_{i}")
            for i, s in enumerate(old_names)
        },
        return_subs=True
    )
    dyn_alloc = {new_names.get(symb, symb): shape for symb, shape in dyn_alloc.items()}

    # avoid bag surprise by inplace undesirated modification
    cst_args, cst_copy = _get_args(cst_tree[:-1])
    cst_copy |= {s for s in cst_tree[-1][1] if s in cst_args} # against bad pointers behavour
    dyn_args, dyn_copy = _get_args(dyn_tree)

    return {
        "cst_copy": cst_copy,
        "cst_args": cst_args,
        "cst_alloc": cst_alloc,
        "cst_tree": cst_tree,
        "dyn_copy": dyn_copy,
        "dyn_args": dyn_args,
        "dyn_alloc": dyn_alloc,
        "dyn_tree": dyn_tree,
    }
