#!/usr/bin/env python3

"""
** Evaluation dynamic of atomic sympy expression. **
----------------------------------------------------

It is faster to initialise than the compilated version but it is slower to evaluate.
Contrary to the compilated version, it is more safe about the security.

Implemented functions:

    * sympy.Abs
    * sympy.acos
    * sympy.acosh
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

import numbers
import typing

from sympy.core.basic import Basic
from sympy.core.numbers import nan, oo
import torch



def _dyn_eval(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None
) -> typing.Union[torch.Tensor, numbers.Real, tuple]:
    """
    ** Recursive replacement of sympy element by numerical elements. **

    Parameters
    ----------
    expr : sympy.core.basic.Basic
        The sympy expression to eval.
    input_args : dict[str, torch.Tensor]
        To each variable name present in the expression, associate the numerical value.
    new_var : str, optional
        If provide, complete inplace the dictionary ``input_args``.
        If the variable is already present in the ``input_args``,
        the values of the tensor are changed inplace.
    """
    if expr.is_Atom:
        if expr.is_symbol:
            return input_args[str(expr)]
        if expr.is_integer:
            return int(expr)
        if expr.is_real:
            return float(expr)
        if expr.is_complex:
            return complex(expr)
        try:
            return {nan: torch.nan, oo: torch.inf, -oo: -torch.inf}[expr]
        except KeyError as err:
            raise NotImplementedError(f"unknown atomic {expr}") from err
    try:
        func = globals()[f"_{expr.__class__.__name__.lower()}"]
    except KeyError as err:
        raise NotImplementedError(f"no function {expr.__class__.__name__} for {expr}") from err
    return func(expr, input_args, new_var)


def _abs(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    """
    >>> from sympy.abc import x
    >>> import torch
    >>> from cutcutcodec.core.compilation.sympy_to_torch.dynamic import _dyn_eval
    >>> input_args = {"x": torch.tensor([-2.0, 2.0])}
    >>> _dyn_eval(abs(x), input_args, "y")
    tensor([2., 2.])
    >>> _ is input_args["y"]
    True
    >>>
    """
    out = None if new_var is None else input_args.get(new_var, None)
    abs_value = torch.abs(_dyn_eval(expr.args[0], input_args), out=out)
    if new_var is not None:
        input_args[new_var] = abs_value
    return abs_value


def _acos(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    out = None if new_var is None else input_args.get(new_var, None)
    acos_value = torch.acos(_dyn_eval(expr.args[0], input_args), out=out)
    if new_var is not None:
        input_args[new_var] = acos_value
    return acos_value


def _acosh(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    out = None if new_var is None else input_args.get(new_var, None)
    acosh_value = torch.acosh(_dyn_eval(expr.args[0], input_args), out=out)
    if new_var is not None:
        input_args[new_var] = acosh_value
    return acosh_value


def _add(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    """
    >>> from sympy.abc import x, y
    >>> import torch
    >>> from cutcutcodec.core.compilation.sympy_to_torch.dynamic import _dyn_eval
    >>> input_args = {"x": torch.tensor([[0.0], [1.0]]), "y": torch.tensor([[2.0, 4.0]])}
    >>> _dyn_eval(1 + x + y, input_args, "z")
    tensor([[3., 5.],
            [4., 6.]])
    >>> _ is input_args["z"]
    True
    >>>
    """
    args = [_dyn_eval(a, input_args) for a in expr.args]
    args.sort(key=(lambda x: torch.numel(x) if isinstance(x, torch.Tensor) else 1))
    try:
        index = list(map(str, expr.args)).index(new_var)
    except ValueError:
        sum_value = args.pop(0)
    else: # case inplace (x = ... + x + ...)
        sum_value = args.pop(index)

    out = None if new_var is None else input_args.get(new_var, None)
    for arg in args:
        sum_value = torch.add(sum_value, arg, out=out)
    if new_var is not None:
        input_args[new_var] = sum_value
    return sum_value


def _asin(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    out = None if new_var is None else input_args.get(new_var, None)
    asin_value = torch.asin(_dyn_eval(expr.args[0], input_args), out=out)
    if new_var is not None:
        input_args[new_var] = asin_value
    return asin_value


def _atan(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    out = None if new_var is None else input_args.get(new_var, None)
    atan_value = torch.atan(_dyn_eval(expr.args[0], input_args), out=out)
    if new_var is not None:
        input_args[new_var] = atan_value
    return atan_value


def _cos(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    out = None if new_var is None else input_args.get(new_var, None)
    cos_value = torch.cos(_dyn_eval(expr.args[0], input_args), out=out)
    if new_var is not None:
        input_args[new_var] = cos_value
    return cos_value


def _cosh(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    out = None if new_var is None else input_args.get(new_var, None)
    cosh_value = torch.cosh(_dyn_eval(expr.args[0], input_args), out=out)
    if new_var is not None:
        input_args[new_var] = cosh_value
    return cosh_value


def _exp(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    out = None if new_var is None else input_args.get(new_var, None)
    exp_value = torch.exp(_dyn_eval(expr.args[0], input_args), out=out)
    if new_var is not None:
        input_args[new_var] = exp_value
    return exp_value


def _im(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    im_value = _dyn_eval(expr.args[0], input_args).imag
    if str(expr.args[0]) != new_var:
        im_value = im_value.clone()
    if new_var is not None:
        input_args[new_var] = im_value
    return im_value


def _log(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    out = None if new_var is None else input_args.get(new_var, None)
    log_value = torch.log(_dyn_eval(expr.args[0], input_args), out=out)
    if new_var is not None:
        input_args[new_var] = log_value
    return log_value


def _mul(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    """
    >>> from sympy.abc import x, y
    >>> import torch
    >>> from cutcutcodec.core.compilation.sympy_to_torch.dynamic import _dyn_eval
    >>> input_args = {"x": torch.tensor([[0.0], [1.0]]), "y": torch.tensor([[2.0, 4.0]])}
    >>> _dyn_eval(2 * x * y, input_args, "z")
    tensor([[0., 0.],
            [4., 8.]])
    >>> _ is input_args["z"]
    True
    >>>
    """
    args = [_dyn_eval(a, input_args) for a in expr.args]
    args.sort(key=(lambda x: torch.numel(x) if isinstance(x, torch.Tensor) else 1))
    try:
        index = list(map(str, expr.args)).index(new_var)
    except ValueError:
        mul_value = args.pop(0)
    else: # case inplace (x = ... * x * ...)
        mul_value = args.pop(index)

    out = None if new_var is None else input_args.get(new_var, None)
    for arg in args:
        if isinstance(arg, numbers.Integral) and arg == -1:
            mul_value = torch.neg(mul_value, out=out)
        else:
            mul_value = torch.mul(mul_value, arg, out=out)
    if new_var is not None:
        input_args[new_var] = mul_value
    return mul_value


def _pow(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    """
    >>> from sympy.abc import x, y
    >>> import torch
    >>> from cutcutcodec.core.compilation.sympy_to_torch.dynamic import _dyn_eval
    >>> input_args = {"x": torch.tensor([[2.0], [4.0]]), "y": torch.tensor([[0.5, 2.0]])}
    >>> _dyn_eval(x**y, input_args, "z")
    tensor([[ 1.4142,  4.0000],
            [ 2.0000, 16.0000]])
    >>> _ is input_args["z"]
    True
    >>> _dyn_eval(x**.5, input_args, "x") # sqrt
    tensor([[1.4142],
            [2.0000]])
    >>> _dyn_eval(x**-1, input_args, "x") # 1/x
    tensor([[0.7071],
            [0.5000]])
    >>>
    """
    base, exp = _dyn_eval(expr.base, input_args), _dyn_eval(expr.exp, input_args)
    out = None if new_var is None else input_args.get(new_var, None)
    pow_value = None
    if isinstance(exp, numbers.Real):
        if exp == -1:
            pow_value = torch.div(1, base, out=out)
        elif exp == .5:
            pow_value = torch.sqrt(base, out=out)
    if pow_value is None:
        pow_value = torch.pow(base, exp, out=out)
    if new_var is not None:
        input_args[new_var] = pow_value
    return pow_value


def _re(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    re_value = _dyn_eval(expr.args[0], input_args).real
    if str(expr.args[0]) != new_var:
        re_value = re_value.clone()
    if new_var is not None:
        input_args[new_var] = re_value
    return re_value


def _sign(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    out = None if new_var is None else input_args.get(new_var, None)
    arg = _dyn_eval(expr.args[0], input_args)
    if arg.dtype.is_floating_point:
        sign_value = torch.sign(arg, out=out)
    else:
        sign_value = torch.where(arg==0, torch.zeros_like(arg), arg/abs(arg), out=out)
    if new_var is not None:
        input_args[new_var] = sign_value
    return sign_value


def _sin(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    out = None if new_var is None else input_args.get(new_var, None)
    sin_value = torch.sin(_dyn_eval(expr.args[0], input_args), out=out)
    if new_var is not None:
        input_args[new_var] = sin_value
    return sin_value


def _sinh(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    out = None if new_var is None else input_args.get(new_var, None)
    sinh_value = torch.sinh(_dyn_eval(expr.args[0], input_args), out=out)
    if new_var is not None:
        input_args[new_var] = sinh_value
    return sinh_value


def _tan(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    out = None if new_var is None else input_args.get(new_var, None)
    tan_value = torch.tan(_dyn_eval(expr.args[0], input_args), out=out)
    if new_var is not None:
        input_args[new_var] = tan_value
    return tan_value


def _tanh(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    out = None if new_var is None else input_args.get(new_var, None)
    tanh_value = torch.tanh(_dyn_eval(expr.args[0], input_args), out=out)
    if new_var is not None:
        input_args[new_var] = tanh_value
    return tanh_value


def _tuple(
    expr: Basic, input_args: dict[str, torch.Tensor], new_var: typing.Optional[str]=None,
) -> typing.Union[torch.Tensor, numbers.Real]:
    if new_var is None:
        return tuple(_dyn_eval(a, input_args) for a in expr)
    input_args[new_var] = _tuple(expr, input_args)
    return input_args[new_var]
