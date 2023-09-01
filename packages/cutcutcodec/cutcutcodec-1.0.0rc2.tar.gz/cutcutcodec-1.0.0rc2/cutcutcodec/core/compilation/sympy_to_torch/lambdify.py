#!/usr/bin/env python3

"""
** Convert a sympy expression into a torch function. **
-------------------------------------------------------

It is the main entry point.
The preprocessing is delegated to the
``cutcutcodec.core.compilation.sympy_to_torch.preprocess`` module.
The compilation is delegated to the
``cutcutcodec.core.compilation.sympy_to_torch.printer`` module.
"""

import logging
import numbers
import typing

from sympy.core.basic import Basic
from sympy.core.containers import Tuple
from sympy.core.symbol import Symbol
from torch._dynamo.exc import BackendCompilerFailed
import torch

from cutcutcodec.core.compilation.sympy_to_torch.dynamic import _dyn_eval
from cutcutcodec.core.compilation.sympy_to_torch.printer import _compile
from cutcutcodec.core.compilation.sympy_to_torch.preprocess import evalf, preprocess



class Lambdify:
    """
    ** Convert a sympy expression into an evaluable torch function. **

    Examples
    --------
    >>> from sympy.abc import x, y, z
    >>> import torch
    >>> from cutcutcodec.core.compilation.sympy_to_torch.lambdify import Lambdify
    >>> exp = (x + y - z - 1)**2 * ((x + y - z)/(x + 1) + (x + y - z - 1)**2) * (x + 1)**(x + y - z)
    >>> func = Lambdify(exp, cst_args=[x])
    >>> print(func) # doctest: +ELLIPSIS
    # this section is cached and dynamic
    x = x.clone()
    x = x + 1.0
    _cst_1 = 1/x
    _cst_0 = x.clone()
    <BLANKLINE>
    # this section only if `copy` is True
    z = z.clone()
    <BLANKLINE>
    # this section is compiled
    _0 = torch.empty(torch.broadcast_shapes(x.shape, y.shape, z.shape), ..., device=x.device)
    _1 = torch.empty(torch.broadcast_shapes(x.shape, y.shape, z.shape), ..., device=x.device)
    _2 = torch.empty(torch.broadcast_shapes(x.shape, y.shape, z.shape), ..., device=x.device)
    z = -1 * z
    _0 = x + y + z
    _1 = -1.0 + _0
    _1 = _1**2
    _2 = _cst_0**_0
    _0 = _0 * _cst_1
    _0 = _0 + _1
    _1 = _0 * _1 * _2
    return _1
    >>> func(x=torch.tensor([0.0, 1.0]), y=torch.tensor([2.0, 4.0]), z=torch.tensor([8.0, 16.0]))
    tensor([2107.0000,    9.7383])
    >>>
    """

    def __init__(self,
        expr: Basic,
        cst_args: typing.Optional[typing.Iterable[Symbol]]=None,
        shapes: dict[Symbol, typing.Union[Symbol, typing.Iterable[Symbol]]]=None,
        copy=True,
    ):
        """
        Parameters
        ----------
        expr : sympy.core.basic.Basic
            The sympy expression of the function.
        cst_args : typing.Iterable[sympy.core.symbol.Symbol], optional
            Arguments that change infrequently enough to be cached.
            The subexpressions computed from this parameters will be cached as well.
            If the parameters change frequently, don't specify them in ``cst_args``,
            This will slow down the function.
        shapes : dict[sympy.core.symbol.Symbol, ``shape broadcasting``], optional
            If some parameters have the same shape, it is possible to give this information
            in order to find a more optimal solution for limited the allocations.
            The keys ares the arguments symbols (not necessarily all), and the values as well.
        copy : boolean, default=True
            If False, some tensors arguments can be modified in place.
            If set to True, a clone of some tensors is performed in order to avoid bad surprises.
        """
        # verifications
        if isinstance(expr, (list, tuple, set, frozenset)):
            assert all(isinstance(e, Basic) for e in expr), expr
        else:
            assert isinstance(expr, Basic), expr.__class__.__name__
        if cst_args is None:
            cst_args = set()
        else:
            assert hasattr(cst_args, "__iter__"), cst_args.__class__.__name__
            cst_args = set(cst_args)
            assert all(isinstance(a, Symbol) for a in cst_args), cst_args
        if shapes is None:
            shapes = {}
        else:
            assert isinstance(shapes, dict) and all(isinstance(k, Symbol) for k in shapes), shapes
            assert all(isinstance(v, (Symbol, typing.Iterable)) for v in shapes.values()), shapes
            shapes = {k: frozenset((v,) if isinstance(v, Symbol) else v) for k, v in shapes.items()}
            assert all(all(isinstance(s, Symbol) for s in v) for v in shapes.values()), shapes
        assert isinstance(copy, bool), copy.__class__.__name__

        # internal attributes
        self._cast = type(expr) if type(expr) in {list, tuple, set, frozenset} else None
        self._copy = copy
        self._cst_cache = None

        # preprocessing
        if self._cast is not None:
            expr = Tuple(*expr)
        self._tree = preprocess(evalf(expr), cst_args=cst_args, shapes=shapes)

        # compile
        if (
            len(self._tree["dyn_tree"]) == 1
            and self._tree["dyn_tree"][0][0] == self._tree["dyn_tree"][0][1]
        ):
            self._tree["dyn_func"] = lambda **kwargs: kwargs[str(self._tree["dyn_tree"][0][0])]
            symb = self._tree["dyn_tree"][0][0]
            self._tree["dyn_func"].code = f"def torch_lambdify({symb}):\n    return {symb}"
        else: # if compilation is required
            func_str = (
                _compile(self._tree["dyn_tree"], self._tree["dyn_alloc"], self._tree["dyn_args"])
            )
            func_code = compile(func_str, filename="", mode="exec")
            context = {"torch": torch}
            exec(func_code, context, context) # load the references in context, not in locals()
            self._tree["dyn_func"] = context["torch_lambdify"]
            self._tree["dyn_func"].code = func_str

    def __str__(self):
        code = []

        # cst tree
        if self._tree["cst_tree"][-1][1]:
            code.append("# this section is cached and dynamic")
            clone = sorted(map(str, self._tree["cst_copy"]))
            clone = (", ".join(clone), ", ".join(f'{s}.clone()' for s in clone))
            code.append(f"{clone[0]} = {clone[1]}")
            for symb, expr in self._tree["cst_tree"][:-1]:
                code.append(f"{symb} = {expr}")
            for i, symb in enumerate(self._tree["cst_tree"][-1][1]):
                if f"_cst_{i}" != str(symb):
                    code.append(f"_cst_{i} = {symb}.clone()")
            code.append("")

        # dyn copy part
        if self._tree["dyn_copy"]:
            code.append("# this section only if `copy` is True")
            clone = sorted(map(str, self._tree["dyn_copy"]))
            clone = (", ".join(clone), ", ".join(f'{s}.clone()' for s in clone))
            code.append(f"{clone[0]} = {clone[1]}")
            code.append("")

        # dyn tree
        code.append("# this section is compiled")
        code.extend(self._tree["dyn_func"].code.split("\n    ")[1:])

        return "\n".join(code)

    def __call__(self,
        *args: typing.Union[torch.Tensor, numbers.Real],
        **kwargs: dict[str, typing.Union[torch.Tensor, numbers.Real]],
    ) -> torch.Tensor:
        """
        ** Evaluate the expression and return the numerical result. **

        Parameters
        ----------
        *args : tuple
            The numerical value of the symbol in the expression.
            Accepted if only one free symbol remains, otherwise, use ``kwargs``.
        **kwargs : dict
            To each variable name present in the expression, associate the numerical value.
        """
        # verifications
        if len(args) > 1:
            raise ValueError("only one non positional argument can be provided")
        provided = set(kwargs) | {f"_cst_{i}" for i in range(len(self._tree["cst_tree"][-1][1]))}
        if len(
            arg_left := set(map(str, self._tree["dyn_args"] | self._tree["cst_args"])) - provided
        ) > 1:
            raise ValueError(f"the arguments {sorted(arg_left)} are not provided")
        if not args and arg_left:
            raise ValueError(f"the argument {arg_left.pop()} is not provided")

        input_args = (kwargs | {arg_left.pop(): args[0]}) if arg_left else kwargs.copy()

        # numbers to tensor and verification
        device = (
            {v.device for v in input_args.values() if isinstance(v, torch.Tensor)} or {None}
        ).pop()
        for symb, val in input_args.items():
            if isinstance(val, numbers.Number):
                input_args[symb] = torch.tensor(
                    val,
                    dtype=(torch.float64 if isinstance(val, numbers.Real) else torch.complex128),
                    device=device,
                )
            elif not isinstance(val, torch.Tensor):
                raise ValueError(
                    f"the argument {symb} has to be a number or a torch tensor, "
                    f"not a {val.__class__.__name__}"
                )

        # evaluation cst tree
        cst_args = self._cst_tree_func(**input_args) # no modification inplace for cst tree
        cst_args = {f"_cst_{i}": arg for i, arg in enumerate(cst_args)}

        # safe copy
        for symb in self._tree["dyn_copy"]:
            symb = str(symb)
            if symb in cst_args:
                cst_args[symb] = cst_args[symb].clone()
            elif self._copy:
                input_args[symb] = input_args[symb].clone()

        # evaluation dyn tree
        input_args = input_args | cst_args
        try:
            out = self._tree["dyn_func"](**input_args)
        except BackendCompilerFailed as err: # case complex for example
            logging.warning(err)
            out = None
            for symb, expr in self._tree["dyn_tree"]:
                out = _dyn_eval(expr, input_args, str(symb))
        except Exception as err:
            raise RuntimeError(
                "failed to run the compiled code:", self._tree["dyn_func"].code
            ) from err

        # cast
        def sub_cast(item):
            if isinstance(item, numbers.Integral):
                return torch.tensor(item, dtype=torch.float32)
            if isinstance(item, numbers.Number):
                return torch.tensor(item)
            return item
        return self._cast(map(sub_cast, out)) if self._cast is not None else sub_cast(out)


    def _cst_tree_func(self, **input_args: dict[str, torch.Tensor]) -> tuple[torch.Tensor]:
        """
        ** Dynamic evaluation of the constant tree. **

        This function is cached once.

        Parameters
        ----------
        input_args : dict[str, torch.Tensor]
            For each symbol name present in the original equation, associate the numerical tensor.

        Returns
        -------
        tuple[torch.Tensor]
            The differents usefull constants for the main compiled main function.
        """
        # compute args hash
        args_hash = sorted(input_args)
        args_hash.extend([
            hash((input_args[a].shape, input_args[a].numpy(force=True).tobytes()))
            for a in args_hash
        ])
        args_hash = hash(tuple(args_hash))

        # computational bloc
        if self._cst_cache is None or self._cst_cache[0] != args_hash: # if cache has to be updated

            # safe copy, obliged even if self._copy is False for prevention again
            # _cst_i is f(input_arg) for avoid uncontroled behavour with pointers
            input_args = input_args.copy() # avoid changing argment inplace
            for symb in self._tree["cst_copy"]:
                symb = str(symb)
                input_args[symb] = input_args[symb].clone()

            # dynamic evaluation
            out = None
            for new_var, expr in self._tree["cst_tree"]:
                out = _dyn_eval(expr, input_args, str(new_var))

            self._cst_cache = (args_hash, out)

        # restitution
        return self._cst_cache[1]
