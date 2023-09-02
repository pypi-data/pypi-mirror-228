"""Utilities for reading samples from test suites."""
import csv
import dataclasses
import gzip
import itertools
import json
import logging
import os
import urllib
from functools import partial

import blobfile as bf
import lz4.frame
import pydantic
import pyzstd

logger = logging.getLogger(__name__)


def gzip_open(filename: str, mode: str = "rb", openhook = open) -> gzip.GzipFile:
    """Wrap the given openhook in gzip."""
    if mode and "b" not in mode:
        mode += "b"

    return gzip.GzipFile(fileobj=openhook(filename, mode), mode=mode)


def lz4_open(filename: str, mode: str = "rb", openhook = open) -> lz4.frame.LZ4FrameFile:
    if mode and "b" not in mode:
        mode += "b"

    return lz4.frame.LZ4FrameFile(openhook(filename, mode), mode=mode)


def zstd_open(filename: str, mode: str = "rb", openhook = open) -> pyzstd.ZstdFile:
    if mode and "b" not in mode:
        mode += "b"

    return pyzstd.ZstdFile(openhook(filename, mode), mode=mode)


def open_by_file_pattern(filename: str, mode: str = "r", **kwargs):
    """Can read/write to files on gcs/local with or without gzipping. If file
    is stored on gcs, streams with blobfile. Otherwise use vanilla python open. If
    filename endswith gz, then zip/unzip contents on the fly (note that gcs paths and
    gzip are compatible)"""
    open_fn = partial(bf.BlobFile, **kwargs)
    try:
        if filename.endswith(".gz"):
            return gzip_open(filename, openhook=open_fn, mode=mode)
        elif filename.endswith(".lz4"):
            return lz4_open(filename, openhook=open_fn, mode=mode)
        elif filename.endswith(".zst"):
            return zstd_open(filename, openhook=open_fn, mode=mode)
        else:
            scheme = urllib.parse.urlparse(filename).scheme
            if scheme == "" or scheme == "file":
                return open_fn(
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), "registry", "data", filename
                    ),
                    mode=mode,
                )
            else:
                return open_fn(filename, mode=mode)
    except Exception as e:
        raise RuntimeError(f"Failed to open: {filename}") from e


def _decode_json(line, path, line_number):
    try:
        return json.loads(line)
    except json.JSONDecodeError as e:
        custom_error_message = f"Error parsing JSON on line {line_number}: {e.msg} at {path}:{line_number}:{e.colno}"
        logger.error(custom_error_message)
        raise ValueError(custom_error_message) from None


def _get_jsonl_file(path):
    logger.info(f"Fetching {path}")
    data = []
    with open_by_file_pattern(path, mode="r") as f:
        return [_decode_json(line, path, i + 1) for i, line in enumerate(f)]


def get_jsonl(path: str) -> list[dict]:
    """
    Extract json lines from the given path.
    If the path is a directory, look in subpaths recursively.

    Return all lines from all jsonl files as a single list.
    """
    if bf.isdir(path):
        result = []
        for filename in bf.listdir(path):
            if filename.endswith(".jsonl"):
                result += get_jsonl(os.path.join(path, filename))
        return result
    return _get_jsonl_file(path)

