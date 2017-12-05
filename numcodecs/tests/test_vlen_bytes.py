# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division


import numpy as np
import nose
from nose.tools import assert_raises


try:
    from numcodecs.vlen import VLenBytes
except ImportError:  # pragma: no cover
    raise nose.SkipTest("vlen-bytes not available")
from numcodecs.tests.common import (check_config, check_repr, check_encode_decode_array,
                                    check_backwards_compatibility, greetings)


greetings_bytes = [g.encode('utf-8') for g in greetings]


arrays = [
    np.array([b'foo', b'bar', b'baz'] * 300, dtype=object),
    np.array(greetings_bytes * 100, dtype=object),
    np.array([b'foo', b'bar', b'baz'] * 300, dtype=object).reshape(90, 10),
    np.array(greetings_bytes * 1000, dtype=object).reshape(len(greetings_bytes), 100, 10,
                                                           order='F'),
]


def test_encode_decode():
    for arr in arrays:
        codec = VLenBytes()
        check_encode_decode_array(arr, codec)


def test_config():
    codec = VLenBytes()
    check_config(codec)


def test_repr():
    check_repr("VLenBytes()")


def test_backwards_compatibility():
    check_backwards_compatibility(VLenBytes.codec_id, arrays, [VLenBytes()])


def test_encode_errors():
    codec = VLenBytes()
    with assert_raises(TypeError):
        codec.encode(1234)
    with assert_raises(TypeError):
        codec.encode([1234, 5678])
    with assert_raises(TypeError):
        codec.encode(np.zeros(10, dtype='i4'))


def test_decode_errors():
    codec = VLenBytes()
    with assert_raises(TypeError):
        codec.decode(u'foo')
    with assert_raises(TypeError):
        codec.decode(1234)
    # these should look like corrupt data
    with assert_raises(ValueError):
        codec.decode(b'foo')
    with assert_raises(ValueError):
        codec.decode(np.arange(2, dtype='i4'))
    with assert_raises(ValueError):
        codec.decode(np.arange(10, dtype='i4'))

    # test out parameter
    enc = codec.encode(arrays[0])
    with assert_raises(TypeError):
        codec.decode(enc, out=b'foo')
    with assert_raises(TypeError):
        codec.decode(enc, out=u'foo')
    with assert_raises(TypeError):
        codec.decode(enc, out=123)
    with assert_raises(ValueError):
        codec.decode(enc, out=np.zeros(10, dtype='i4'))