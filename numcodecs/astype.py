# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division

import numpy as np

from .abc import Codec
from .compat import buffer_copy, ndarray_from_buffer


class AsType(Codec):
    """Filter to convert data between different types.

    Parameters
    ----------
    encode_dtype : dtype
        Data type to use for encoded data.
    decode_dtype : dtype, optional
        Data type to use for decoded data.

    Notes
    -----
    If `encode_dtype` is of lower precision than `decode_dtype`, please be
    aware that data loss can occur by writing data to disk using this filter.
    No checks are made to ensure the casting will work in that direction and
    data corruption will occur.

    Examples
    --------
    >>> import numcodecs
    >>> import numpy as np
    >>> x = np.arange(100, 120, 2, dtype=np.int8)
    >>> x
    array([100, 102, 104, 106, 108, 110, 112, 114, 116, 118], dtype=int8)
    >>> f = numcodecs.AsType(encode_dtype=x.dtype, decode_dtype=np.int64)
    >>> y = f.decode(x)
    >>> y
    array([100, 102, 104, 106, 108, 110, 112, 114, 116, 118])
    >>> z = f.encode(y)
    >>> z
    array([100, 102, 104, 106, 108, 110, 112, 114, 116, 118], dtype=int8)

    """

    codec_id = 'astype'

    def __init__(self, encode_dtype, decode_dtype):
        self.encode_dtype = np.dtype(encode_dtype)
        self.decode_dtype = np.dtype(decode_dtype)

    def encode(self, buf):

        # view input data as 1D array
        arr = ndarray_from_buffer(buf, self.decode_dtype)

        # convert and copy
        enc = arr.astype(self.encode_dtype)

        return enc

    def decode(self, buf, out=None):

        # view encoded data as 1D array
        enc = ndarray_from_buffer(buf, self.encode_dtype)

        # convert and copy
        dec = enc.astype(self.decode_dtype)

        # handle output
        out = buffer_copy(dec, out)

        return out

    def get_config(self):
        config = dict()
        config['id'] = self.codec_id
        config['encode_dtype'] = self.encode_dtype.str
        config['decode_dtype'] = self.decode_dtype.str
        return config

    def __repr__(self):
        return (
            '%s(encode_dtype=%r, decode_dtype=%r)' % (
                type(self).__name__,
                self.encode_dtype.str,
                self.decode_dtype.str
            )
        )
