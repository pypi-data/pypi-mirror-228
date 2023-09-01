#!/usr/bin/env python3

"""
** Basic casts between different video profiles. **
---------------------------------------------------
"""


import torch

from cutcutcodec.core.classes.frame_video import FrameVideo



def _get_alpha(frame: FrameVideo) -> torch.Tensor:
    """
    ** Get the alpha channel. **
    """
    if frame.shape[2] in {2, 4}:
        return torch.unsqueeze(frame[..., frame.shape[2]-1], 2)
    return torch.full(
        (frame.shape[0], frame.shape[1], 1),
        (1.0 if frame.dtype.is_floating_point else 255),
        dtype=frame.dtype,
        layout=frame.layout,
        device=frame.device
    )


def to_gray(frame: torch.Tensor) -> torch.Tensor:
    """
    ** Convert any video frame into a 1 gray channel frame. **

    Parameters
    ----------
    frame : torch.Tensor
        The input frame of any type.

    Returns
    -------
    frame
        The output 1 gray channel frame, the data can by shared.
        Type has to be floating point or uint8.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.filters.mix.video_cast import to_gray
    >>> _ = torch.manual_seed(0)
    >>> for dtype in (torch.uint8, torch.float16, torch.float32, torch.float64):
    ...     for channels in (1, 2, 3, 4):
    ...         if dtype == torch.uint8:
    ...             frame = torch.randint(0, 256, (480, 720, channels), dtype=torch.uint8)
    ...         else:
    ...             frame = torch.rand((480, 720, channels), dtype=dtype)
    ...         assert to_gray(frame).shape == (480, 720, 1)
    ...         assert to_gray(frame).dtype == dtype
    ...
    >>>
    """
    assert isinstance(frame, torch.Tensor), frame.__class__.__name__
    assert len(frame.shape) == 3, frame.shape

    if frame.shape[2] == 1:
        return frame
    if frame.shape[2] == 2:
        return torch.unsqueeze(frame[..., 0], 2)
    if frame.shape[2] == 3:
        if frame.dtype == torch.uint8:
            frame = to_gray(frame.to(dtype=torch.float32))
            return torch.round(frame, out=frame).to(dtype=torch.uint8)
        return torch.unsqueeze(.114*frame[..., 0] + 0.587*frame[..., 1] + 0.299*frame[..., 2], 2)
    if frame.shape[2] == 4:
        return to_gray(frame[..., :3])
    raise ValueError(f"only, 1, 2, 3, or 4 layers, not {frame.shape[2]}")


def to_gray_alpha(frame: torch.Tensor) -> torch.Tensor:
    """
    ** Convert any video frame into a 2 channels (gray, alpha) frame. **

    Parameters
    ----------
    frame : torch.Tensor
        The input frame of any type.

    Returns
    -------
    frame
        The output 2 gray alpha channels frame, the data can by shared.
        Type has to be floating point or uint8.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.filters.mix.video_cast import to_gray_alpha
    >>> _ = torch.manual_seed(0)
    >>> for dtype in (torch.uint8, torch.float16, torch.float32, torch.float64):
    ...     for channels in (1, 2, 3, 4):
    ...         if dtype == torch.uint8:
    ...             frame = torch.randint(0, 256, (480, 720, channels), dtype=torch.uint8)
    ...         else:
    ...             frame = torch.rand((480, 720, channels), dtype=dtype)
    ...         assert to_gray_alpha(frame).shape == (480, 720, 2)
    ...         assert to_gray_alpha(frame).dtype == dtype
    ...
    >>>
    """
    assert isinstance(frame, torch.Tensor), frame.__class__.__name__
    assert len(frame.shape) == 3, frame.shape

    if frame.shape[2] == 2:
        return frame
    if frame.shape[2] in {1, 3, 4}:
        return torch.cat([to_gray(frame), _get_alpha(frame)], 2)
    raise ValueError(f"only, 1, 2, 3, or 4 layers, not {frame.shape[2]}")


def to_bgr(frame: torch.Tensor) -> torch.Tensor:
    """
    ** Convert any video frame into a 3 channels (blue, green, red) frame. **

    Parameters
    ----------
    frame : torch.Tensor
        The input frame of any type.

    Returns
    -------
    frame
        The output 3 blue, green, red channels frame, the data can by shared.
        Type has to be floating point or uint8.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.filters.mix.video_cast import to_bgr
    >>> _ = torch.manual_seed(0)
    >>> for dtype in (torch.uint8, torch.float16, torch.float32, torch.float64):
    ...     for channels in (1, 2, 3, 4):
    ...         if dtype == torch.uint8:
    ...             frame = torch.randint(0, 256, (480, 720, channels), dtype=torch.uint8)
    ...         else:
    ...             frame = torch.rand((480, 720, channels), dtype=dtype)
    ...         assert to_bgr(frame).shape == (480, 720, 3)
    ...         assert to_bgr(frame).dtype == dtype
    ...
    >>>
    """
    assert isinstance(frame, torch.Tensor), frame.__class__.__name__
    assert len(frame.shape) == 3, frame.shape

    if frame.shape[2] == 1:
        return torch.cat((frame, frame, frame), 2)
    if frame.shape[2] == 2:
        return to_bgr(torch.unsqueeze(frame[..., 0], 2))
    if frame.shape[2] == 3:
        return frame
    if frame.shape[2] == 4:
        return frame[..., :3]
    raise ValueError(f"only, 1, 2, 3, or 4 layers, not {frame.shape[2]}")


def to_bgr_alpha(frame: torch.Tensor) -> torch.Tensor:
    """
    ** Convert any video frame into a 4 channels (blue, green, red, alpha) frame. **

    Parameters
    ----------
    frame : torch.Tensor
        The input frame of any type.

    Returns
    -------
    frame
        The output 4 blue, green, red alpha channels frame, the data can by shared.
        Type has to be floating point or uint8.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.filters.mix.video_cast import to_bgr_alpha
    >>> _ = torch.manual_seed(0)
    >>> for dtype in (torch.uint8, torch.float16, torch.float32, torch.float64):
    ...     for channels in (1, 2, 3, 4):
    ...         if dtype == torch.uint8:
    ...             frame = torch.randint(0, 256, (480, 720, channels), dtype=torch.uint8)
    ...         else:
    ...             frame = torch.rand((480, 720, channels), dtype=dtype)
    ...         assert to_bgr_alpha(frame).shape == (480, 720, 4)
    ...         assert to_bgr_alpha(frame).dtype == dtype
    ...
    >>>
    """
    assert isinstance(frame, torch.Tensor), frame.__class__.__name__
    assert len(frame.shape) == 3, frame.shape

    if frame.shape[2] == 4:
        return frame
    if frame.shape[2] in {1, 2, 3}:
        return torch.cat([to_bgr(frame), _get_alpha(frame)], 2)
    raise ValueError(f"only, 1, 2, 3, or 4 layers, not {frame.shape[2]}")
