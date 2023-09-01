#!/usr/bin/env python3

"""
** Compile a sympy atomic tree into a python source code. **
------------------------------------------------------------

It takes time to build but is the fastest mean to eval the expression.

Implemented functions:

    * sympy.Abs
    * sympy.acos
    * sympy.Add `+`
    * sympy.asin
    * sympy.atan
    * sympy.cos
    * sympy.cosh
    * sympy.exp
    * sympy.im
    * sympy.log
    * sympy.Mul `*`
    * sympy.Pow `/` and `**`
    * sympy.re
    * sympy.sin
    * sympy.sinh
    * sympy.sqrt
    * sympy.tan
    * sympy.tanh
    * sympy.Tuple

Not implemented functions:

    * sympy.acosh
    * sympy.Add `+` and `-`
    * sympy.And
    * sympy.arg
    * sympy.asinh
    * sympy.atan2
    * sympy.atanh
    * sympy.ceiling
    * sympy.Determinant
    * sympy.Eq
    * sympy.erf
    * sympy.floor
    * sympy.GreaterThan
    * sympy.HadamardProduct
    * sympy.LessThan
    * sympy.loggamma
    * sympy.MatAdd
    * sympy.Max
    * sympy.Min
    * sympy.Mod `%`
    * sympy.Ne
    * sympy.Not
    * sympy.Or
    * sympy.sign
    * sympy.StrictGreaterThan
    * sympy.StrictLessThan
    * sympy.Trace
"""

import typing

from sympy.core.basic import Atom, Basic
from sympy.core.numbers import nan, oo
from sympy.core.symbol import Symbol


def _compile(
    tree: list[tuple[Symbol, typing.Union[Basic, None]]],
    alloc: dict[Symbol, set[Symbol]],
    args: set[Symbol],
) -> str:
    """
    ** The complete source code of the compiled func. **

    Parameters
    ----------
    tree : list[tuple[sympy.core.symbol.Symbol, typing.Union[sympy.core.basic.Basic, None]]]
        Each steps.
    alloc : dict[sympy.core.symbol.Symbol, set[sympy.core.symbol.Symbol]]
        The intermediate variables to be declared and their respective dimensions.
    args : set[sympy.core.symbol.Symbol]
        All the inputs arguments required for this function.
    """
    lines = []

    lines.append('@torch.compile(mode="reduce-overhead")')
    lines.append(f"def torch_lambdify({', '.join(sorted(map(str, args)))}):")

    alloc = {str(s): sorted(map(str, b)) for s, b in alloc.items()}
    for symb in sorted(alloc):
        if len(broadcast := alloc[symb]) == 1:
            lines.append(f"    {symb} = torch.empty_like({broadcast.pop()})")
            continue
        lines.append(
            f"    {symb} = torch.empty("
            f"torch.broadcast_shapes({', '.join(f'{b}.shape' for b in broadcast)}), "
            f"dtype={broadcast[0]}.dtype, "
            f"layout={broadcast[0]}.layout, "
            f"device={broadcast[0]}.device)"
        )

    for out, expr in tree:
        lines.extend([f"    {l}" for l in _print_atomic(expr, str(out))])
    lines.append(f"    return {tree[-1][0]}")

    return "\n".join(lines)


def _print_atomic(expr: Basic, out: str) -> list[str]:
    """
    ** Write the sympy atomic expression as a valid source code lines. **

    Parameters
    ----------
    expr : sympy.core.basic.Basic
        The sympy atomic expression to eval.
    out : str, optional
        The variable name to set, assume that this var is already declared.
    """
    def _number_to_str(elem: Atom) -> typing.Union[Symbol, str]:
        if elem.is_symbol:
            return elem
        if elem.is_number:
            if elem.is_integer:
                return str(int(elem))
            if elem.is_real:
                return str(float(elem))
            if elem.is_complex:
                return str(complex(elem))
            try:
                return {nan: "torch.nan", oo: "torch.inf", -oo: "-torch.inf"}[elem]
            except KeyError as err:
                raise NotImplementedError(f"unknown number {elem}") from err
        raise RuntimeError(f"{elem} is not atomic")
    if expr.is_Atom:
        return [f"{out} = {_number_to_str(expr)}"]
    try:
        func = globals()[f"_{expr.__class__.__name__.lower()}"]
    except KeyError as err:
        raise NotImplementedError(f"no function {expr.__class__.__name__} for {expr}") from err
    try:
        return func(out, *map(_number_to_str, expr.args))
    except RuntimeError as err:
        raise RuntimeError(f"all args of {expr} are not atomic") from err


def _add(out: str, *parts: Atom) -> list[str]:
    """
    >>> from sympy.abc import x, y
    >>> from cutcutcodec.core.compilation.sympy_to_torch.printer import _print_atomic
    >>> _print_atomic(1 + x + y, "z")
    ['z = 1 + x + y']
    >>>
    """
    return [f"{out} = {' + '.join(map(str, parts))}"]


def _abs(out: str, symb: Atom) -> list[str]:
    return [f"{out} = abs({symb})"]


def _acos(out: str, symb: Atom) -> list[str]:
    return [f"{out} = torch.acos({symb}, out={out})"]


def _asin(out: str, symb: Atom) -> list[str]:
    return [f"{out} = torch.asin({symb}, out={out})"]


def _atan(out: str, symb: Atom) -> list[str]:
    return [f"{out} = torch.atan({symb}, out={out})"]


def _cos(out: str, symb: Atom) -> list[str]:
    return [f"{out} = torch.cos({symb}, out={out})"]


def _cosh(out: str, symb: Atom) -> list[str]:
    return [f"{out} = torch.cosh({symb}, out={out})"]


def _exp(out: str, symb: Atom) -> list[str]:
    return [f"{out} = torch.exp({symb}, out={out})"]


def _im(out: str, symb: Atom) -> list[str]:
    if out == str(symb):
        return [f"{out} = {symb}.imag"]
    return [f"{out} = {symb}.imag.clone()"]


def _log(out: str, symb: Atom) -> list[str]:
    return [f"{out} = torch.log({symb}, out={out})"]


def _mul(out: str, *parts: Atom) -> list[str]:
    """
    >>> from sympy.abc import x, y
    >>> from cutcutcodec.core.compilation.sympy_to_torch.printer import _print_atomic
    >>> _print_atomic(2 * x * y, "z")
    ['z = 2 * x * y']
    >>>
    """
    return [f"{out} = {' * '.join(map(str, parts))}"]


def _pow(out: str, base: Atom, exp: Atom) -> list[str]:
    """
    >>> from sympy.abc import x, y
    >>> from cutcutcodec.core.compilation.sympy_to_torch.printer import _print_atomic
    >>> _print_atomic(x**y, "z")
    ['z = x**y']
    >>> _print_atomic(x**.5, "z")
    ['z = torch.sqrt(x)']
    >>> _print_atomic(x**-1, "z")
    ['z = 1/x']
    >>>
    """
    if exp == "-1":
        return [f"{out} = 1/{base}"]
    if exp == "0.5":
        return [f"{out} = torch.sqrt({base})"]
    return [f"{out} = {base}**{exp}"]


def _re(out: str, symb: Atom) -> list[str]:
    if out == str(symb):
        return [f"{out} = {symb}.real"]
    return [f"{out} = {symb}.real.clone()"]

def _sign(out: str, symb: Atom) -> list[str]:
    return [
        f"if {symb}.dtype.is_floating_point:",
        f"    {out} = torch.sign({symb}, out={out})",
        "else:",
        (
            f"    {out} = torch.where({symb}==0, "
            f"torch.zeros_like({symb}), {symb}/abs({symb}), out={out})"
        ),
    ]

def _sin(out: str, symb: Atom) -> list[str]:
    return [f"{out} = torch.sin({symb}, out={out})"]


def _sinh(out: str, symb: Atom) -> list[str]:
    return [f"{out} = torch.sinh({symb}, out={out})"]


def _tan(out: str, symb: Atom) -> list[str]:
    return [f"{out} = torch.tan({symb}, out={out})"]


def _tanh(out: str, symb: Atom) -> list[str]:
    return [f"{out} = torch.tanh({symb}, out={out})"]


def _tuple(out: str, *parts: Atom) -> list[str]:
    if len(parts) == 0:
        return [f"{out} = ()"]
    if len(parts) == 1:
        return [f"{out} = ({parts[0]},)"]
    return [f"{out} = {', '.join(map(str, parts))}"]
