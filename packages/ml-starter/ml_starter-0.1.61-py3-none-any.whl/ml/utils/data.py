# mypy: disable-error-code="import"
"""Some common utilities for datasets and data loaders."""

import hashlib
import itertools
import logging
import math
import shutil
import struct
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Callable, Collection, Iterator, Sequence, TypeVar

from torch.utils.data.dataloader import get_worker_info as _get_worker_info_base
from torch.utils.data.datapipes._decorator import functional_datapipe
from torch.utils.data.datapipes.datapipe import IterDataPipe, MapDataPipe
from torch.utils.data.datapipes.utils.common import StreamWrapper

from ml.core.env import get_data_dir, get_s3_data_bucket
from ml.core.state import Phase
from ml.utils.distributed import get_rank, get_world_size
from ml.utils.timer import Timer, spinnerator

try:
    import boto3
except ImportError:
    boto3 = None

logger = logging.getLogger(__name__)

T = TypeVar("T")

MAGIC = b"SDS\n"
PRE_HEADER_SIZE = len(MAGIC) + 8


@dataclass
class WorkerInfo:
    worker_id: int
    num_workers: int
    in_worker: bool


def get_worker_info() -> WorkerInfo:
    """Gets a typed worker info object which always returns a value.

    Returns:
        The typed worker info object
    """
    if (worker_info := _get_worker_info_base()) is None:
        return WorkerInfo(
            worker_id=0,
            num_workers=1,
            in_worker=False,
        )

    return WorkerInfo(
        worker_id=worker_info.id,
        num_workers=worker_info.num_workers,
        in_worker=True,
    )


def split_n_items_across_workers(n: int, worker_id: int, num_workers: int) -> tuple[int, int]:
    """Splits N items across workers.

    This returns the start and end indices for the items to be processed by the
    given worker. The end index is exclusive.

    Args:
        n: The number of items to process.
        worker_id: The ID of the current worker.
        num_workers: The total number of workers.
    """
    assert n >= num_workers, f"n ({n}) must be >= num_workers ({num_workers})"
    assert 0 <= worker_id < num_workers, f"worker_id ({worker_id}) must be >= 0 and < num_workers ({num_workers})"

    # The number of items to process per worker.
    items_per_worker = math.ceil(n / num_workers)

    # The start and end indices for the items to process.
    start = worker_id * items_per_worker
    end = min(start + items_per_worker, n)

    return start, end


def get_dataset_splits(
    items: Sequence[T],
    valid: float | int,
    test: float | int,
) -> tuple[Sequence[T], Sequence[T], Sequence[T]]:
    """Splits a list of items into three sub-lists for train, valid, and test.

    Args:
        items: The list of items to split.
        valid: If a value between 0 and 1, the fraction of items to use for
            the validation set, otherwise the number of items to use for the
            validation set.
        test: If a value between 0 and 1, the fraction of items to use for
            the test set, otherwise the number of items to use for the test
            set.

    Returns:
        A tuple of three lists, one for each phase.

    Raises:
        ValueError: If the split sizes would be invalid.
    """
    num_items = len(items)

    # Converts a fraction to an integer number of items.
    if isinstance(valid, float):
        if 0 > valid or valid > 1:
            raise ValueError(f"Valid fraction must be between 0 and 1, got {valid}")
        valid = int(num_items * valid)
    if isinstance(test, float):
        if 0 > test or test > 1:
            raise ValueError(f"Test fraction must be between 0 and 1, got {test}")
        test = int(num_items * test)

    if valid + test > num_items:
        raise ValueError(f"Invalid number of items: {num_items}, valid: {valid}, test: {test}")

    train_items = items[: num_items - valid - test]
    valid_items = items[num_items - valid - test : num_items - test]
    test_items = items[num_items - test :]

    return train_items, valid_items, test_items


def get_dataset_split_for_phase(
    items: Sequence[T],
    phase: Phase,
    valid: float | int,
    test: float | int,
) -> Sequence[T]:
    """Gets the items for a given phase.

    Args:
        items: The list of items to split.
        phase: The phase to get the items for.
        valid: If a value between 0 and 1, the fraction of items to use for
            the validation set, otherwise the number of items to use for the
            validation set.
        test: If a value between 0 and 1, the fraction of items to use for
            the test set, otherwise the number of items to use for the test
            set.

    Returns:
        The items for the given phase.

    Raises:
        ValueError: If the phase is not valid.
    """
    train_items, valid_items, test_items = get_dataset_splits(items, valid, test)

    match phase:
        case "train":
            return train_items
        case "valid":
            return valid_items
        case "test":
            return test_items
        case _:
            raise ValueError(f"Invalid phase: {phase}")


def check_md5(file_path: str | Path, hash_str: str | None, chunk_size: int = 2**16) -> bool:
    """Checks the MD5 of the downloaded file.

    Args:
        file_path: Path to the downloaded file.
        hash_str: Expected MD5 of the file; if None, return True.
        chunk_size: Size of the chunks to read from the file.

    Returns:
        True if the MD5 matches, False otherwise.
    """
    if hash_str is None:
        return True

    md5 = hashlib.md5()

    with open(file_path, "rb") as f:
        for chunk in spinnerator(iter(lambda: f.read(chunk_size), b"")):
            md5.update(chunk)

    return md5.hexdigest() == hash_str


def check_sha256(file_path: str | Path, hash_str: str | None, chunk_size: int = 2**16) -> bool:
    """Checks the SHA256 of the downloaded file.

    Args:
        file_path: Path to the downloaded file.
        hash_str: Expected SHA256 of the file; if None, return True.
        chunk_size: Size of the chunks to read from the file.

    Returns:
        True if the SHA256 matches, False otherwise.
    """
    if hash_str is None:
        return True

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in spinnerator(iter(lambda: f.read(chunk_size), b"")):
            sha256.update(chunk)

    return sha256.hexdigest() == hash_str


def _get_files_to_compress(
    input_dir: Path,
    only_extension_set: set[str] | None,
    exclude_extension_set: set[str] | None,
) -> list[tuple[str, int]]:
    file_chunks: list[tuple[str, int]] = []
    for file_path in input_dir.rglob("*"):
        if not file_path.is_file():
            continue
        if only_extension_set is not None and file_path.suffix not in only_extension_set:
            continue
        if exclude_extension_set is not None and file_path.suffix in exclude_extension_set:
            continue
        num_bytes = file_path.stat().st_size
        file_chunks.append((str(file_path.relative_to(input_dir)), num_bytes))
    return sorted(file_chunks)


@dataclass
class Header:
    files: list[tuple[str, int]]
    init_offset: int = 0

    def encode(self) -> bytes:
        file_lengths = [num_bytes for _, num_bytes in self.files]
        names_bytes = [file_path.encode("utf-8") for file_path, _ in self.files]
        names_bytes_lengths = [len(n) for n in names_bytes]

        def get_byte_enc_and_dtype(n: int) -> tuple[int, str]:
            if n < 2**8:
                return 1, "B"
            elif n < 2**16:
                return 2, "H"
            elif n < 2**32:
                return 4, "I"
            else:
                return 8, "Q"

        file_lengths_dtype_int, file_lengths_dtype = get_byte_enc_and_dtype(max(file_lengths))
        name_lengths_dtype_int, name_lengths_dtype = get_byte_enc_and_dtype(max(names_bytes_lengths))

        return b"".join(
            [
                struct.pack("B", file_lengths_dtype_int),
                struct.pack("B", name_lengths_dtype_int),
                struct.pack("Q", len(self.files)),
                struct.pack(f"<{len(file_lengths)}{file_lengths_dtype}", *file_lengths),
                struct.pack(f"<{len(names_bytes)}{name_lengths_dtype}", *names_bytes_lengths),
                *names_bytes,
            ],
        )

    def write(self, fp: IO[bytes]) -> None:
        encoded = self.encode()
        fp.write(struct.pack("Q", len(encoded)))
        fp.write(encoded)

    @classmethod
    def decode(cls, b: bytes) -> "Header":
        def get_dtype_from_int(n: int) -> str:
            if n == 1:
                return "B"
            elif n == 2:
                return "H"
            elif n == 4:
                return "I"
            elif n == 8:
                return "Q"
            else:
                raise ValueError(f"Invalid dtype int: {n}")

        (file_lengths_dtype_int, name_lengths_dtype_int), b = struct.unpack("BB", b[:2]), b[2:]
        file_lengths_dtype = get_dtype_from_int(file_lengths_dtype_int)
        name_lengths_dtype = get_dtype_from_int(name_lengths_dtype_int)

        (num_files,), b = struct.unpack("Q", b[:8]), b[8:]

        fl_bytes = num_files * struct.calcsize(file_lengths_dtype)
        nl_bytes = num_files * struct.calcsize(name_lengths_dtype)
        file_lengths, b = struct.unpack(f"<{num_files}{file_lengths_dtype}", b[:nl_bytes]), b[nl_bytes:]
        names_bytes_lengths, b = struct.unpack(f"<{num_files}{name_lengths_dtype}", b[:fl_bytes]), b[fl_bytes:]

        names = []
        for name_bytes_length in names_bytes_lengths:
            name_bytes, b = b[:name_bytes_length], b[name_bytes_length:]
            names.append(name_bytes.decode("utf-8"))

        assert len(b) == 0, f"Bytes left over: {len(b)}"

        return cls(list(zip(names, file_lengths)))

    @classmethod
    def read(cls, fp: IO[bytes]) -> tuple["Header", int]:
        (num_bytes,) = struct.unpack("Q", fp.read(8))
        return cls.decode(fp.read(num_bytes)), num_bytes

    def shard(self, shard_id: int, total_shards: int) -> "Header":
        num_files = len(self.files)
        num_files_per_shard = math.ceil(num_files / total_shards)
        start = shard_id * num_files_per_shard
        end = min((shard_id + 1) * num_files_per_shard, num_files)
        shard_offset = sum(num_bytes for _, num_bytes in self.files[:start])
        return Header(self.files[start:end], self.init_offset + shard_offset)

    def offsets(self, header_size: int) -> list[int]:
        return [
            offset + header_size + self.init_offset
            for offset in itertools.accumulate((num_bytes for _, num_bytes in self.files), initial=0)
        ]


def compress_folder_to_sds(
    input_dir: str | Path,
    output_path: str | Path,
    only_extensions: Collection[str] | None = None,
    exclude_extensions: Collection[str] | None = None,
) -> None:
    """Compresses a given folder to a streamable dataset (SDS).

    Args:
        input_dir: The directory to compress.
        output_path: The root directory to write the shards to.
        only_extensions: If not None, only files with these extensions will be
            included.
        exclude_extensions: If not None, files with these extensions will be
            excluded.
    """
    only_extension_set = set(only_extensions) if only_extensions is not None else None
    exclude_extension_set = set(exclude_extensions) if exclude_extensions is not None else None
    input_dir, output_path = Path(input_dir).resolve(), Path(output_path).resolve()

    # Compresses each of the files.
    with Timer("getting files to compress", spinner=True):
        file_paths = _get_files_to_compress(input_dir, only_extension_set, exclude_extension_set)
    header = Header(file_paths)
    output_path.parent.mkdir(exist_ok=True, parents=True)
    with open(output_path, "wb") as f:
        # Writes the header.
        f.write(MAGIC)
        header.write(f)

        # Writes each of the files.
        for file_path, _ in spinnerator(file_paths):
            with open(input_dir / file_path, "rb") as f_in:
                shutil.copyfileobj(f_in, f)


class Streamer(ABC):
    @abstractmethod
    def __iter__(self) -> Iterator[bytes]:
        """Returns an iterator over the bytes of the stream."""

    @abstractmethod
    def __next__(self) -> bytes:
        """Returns the next chunk of bytes from the stream."""


class ClippedStreamWrapper(StreamWrapper, Streamer):
    def __init__(
        self,
        file_obj: IO[bytes],
        length: int,
        parent_stream: StreamWrapper | None = None,
        name: str | None = None,
    ) -> None:
        super().__init__(file_obj, parent_stream, name)

        self.cur_bytes = 0
        self.length = length

    def __iter__(self) -> Iterator[bytes]:
        for chunk in super().__iter__():
            if self.cur_bytes + len(chunk) > self.length:
                chunk = chunk[: self.length - self.cur_bytes]
            self.cur_bytes += len(chunk)
            yield chunk

    def __next__(self) -> bytes:
        chunk = super().__next__()
        if self.cur_bytes + len(chunk) > self.length:
            chunk = chunk[: self.length - self.cur_bytes]
        self.cur_bytes += len(chunk)
        return chunk

    def __repr__(self) -> str:
        if self.name is None:
            return f"ClippedStreamWrapper<{self.file_obj!r},{self.cur_bytes},{self.length}>"
        else:
            return f"ClippedStreamWrapper<{self.name},{self.file_obj!r},{self.cur_bytes}, {self.length}>"

    def __getstate__(self) -> tuple[IO[bytes], int, int]:
        return self.file_obj, self.length, self.cur_bytes

    def __setstate__(self, state: tuple[IO[bytes], int, int]) -> None:
        self.file_obj, self.length, self.cur_bytes = state


class Reader:
    def __init__(self, streamer_fn: Callable[[int, int], Streamer], length: int, offset: int) -> None:
        self.streamer_fn = streamer_fn
        self.length = length
        self.offset = offset

    def read(self, start: int = 0, length: int | None = None) -> Streamer:
        offset = self.offset + start
        if length is None:
            length = self.length - start
        return self.streamer_fn(offset, length)

    def __len__(self) -> int:
        return self.length


class SdsBaseReaderDataPipe(ABC):
    """Defines a base reader for streamable datasets.

    Different readers just need to implement the ``open`` method, in a way that
    mirrors the ``open`` method for reading files from a local disk.

    Parameters:
        shard_id: The index of the current reader shard. If not specified, will
            default to the current rank.
        total_shards: The total number of reader shards. If not specified, will
            default to the world size.
    """

    def __init__(self) -> None:
        super().__init__()

        self.shard_id = get_rank()
        self.total_shards = get_world_size()

        # Shards the header using the given shard parameters.
        header, header_num_bytes = self.get_header_and_offsets()

        self.header = header.shard(self.shard_id, self.total_shards)
        self.offsets = self.header.offsets(PRE_HEADER_SIZE + header_num_bytes)

    def get_header_and_offsets(self) -> tuple[Header, int]:
        init_bytes = self.read(0, PRE_HEADER_SIZE)
        assert init_bytes[: len(MAGIC)] == MAGIC, "Invalid magic number."
        header_num_bytes = struct.unpack("Q", init_bytes[len(MAGIC) :])[0]

        header_bytes = self.read(PRE_HEADER_SIZE, header_num_bytes)
        header = Header.decode(header_bytes)

        return header, header_num_bytes

    @abstractmethod
    def open(self, start: int, length: int) -> Streamer:
        """Returns a streamer for reading some bytes from somewhere.

        This interface is only expected to yield some bytes from somewhere.
        This means you can stream bytes from a local disk or from a remote
        file system.

        Args:
            start: The starting offset to read from.
            length: The number of bytes to read.
        """

    def read(self, start: int, length: int) -> bytes:
        return b"".join(self.open(start, length))

    def __len__(self) -> int:
        worker_info = get_worker_info()
        worker_id, num_workers = worker_info.worker_id, worker_info.num_workers
        start, end = split_n_items_across_workers(len(self.header.files), worker_id, num_workers)
        return end - start


class SdsFileReaderDataPipe(SdsBaseReaderDataPipe, ABC):
    @abstractmethod
    def path(self) -> str | Path:
        """Returns the path to read from."""

    def open(self, start: int, length: int) -> Streamer:
        f = open(self.path(), "rb")
        f.seek(start)
        return ClippedStreamWrapper(f, length)


class SdsHttpReaderDataPipe(SdsBaseReaderDataPipe, ABC):
    @abstractmethod
    def url(self) -> str:
        """Returns the URL to read from."""

    def open(self, start: int, length: int) -> Streamer:
        req = urllib.request.Request(self.url(), headers={"Range": f"bytes={start}-{start + length - 1}"})
        return ClippedStreamWrapper(urllib.request.urlopen(req), length)


class SdsS3ReaderDataPipe(SdsBaseReaderDataPipe, ABC):
    @abstractmethod
    def bucket(self) -> str:
        """Returns the S3 bucket to read from."""

    @abstractmethod
    def key(self) -> str:
        """Returns the S3 key to read from."""

    def open(self, start: int, length: int) -> Streamer:
        assert boto3 is not None

        s3 = boto3.client("s3")
        s3_obj = s3.get_object(Bucket=self.bucket(), Key=self.key(), Range=f"bytes={start}-{start + length - 1}")
        return ClippedStreamWrapper(s3_obj["Body"], length)


class SdsBaseMapReaderDataPipe(MapDataPipe[tuple[str, Reader]], SdsBaseReaderDataPipe):
    def __getitem__(self, index: int) -> tuple[str, Reader]:
        worker_info = get_worker_info()
        worker_id, num_workers = worker_info.worker_id, worker_info.num_workers
        start, _ = split_n_items_across_workers(len(self.header.files), worker_id, num_workers)
        (name, length), offset = self.header.files[index + start], self.offsets[index + start]
        return name, Reader(self.open, length, offset)


@functional_datapipe("sds_file_map_reader")
class SdsFileMapReaderDataPipe(SdsFileReaderDataPipe, SdsBaseMapReaderDataPipe):
    def __init__(self, path: str | Path) -> None:
        self._path = path

        super().__init__()

    def path(self) -> str | Path:
        return self._path


@functional_datapipe("sds_http_map_reader")
class SdsHttpMapReaderDataPipe(SdsHttpReaderDataPipe, SdsBaseMapReaderDataPipe):
    def __init__(self, url: str) -> None:
        self._url = url

        super().__init__()

    def url(self) -> str:
        return self._url


@functional_datapipe("sds_s3_map_reader")
class SdsS3MapReaderDataPipe(SdsS3ReaderDataPipe, SdsBaseMapReaderDataPipe):
    def __init__(self, name: str, prefix: str | None = None, bucket: str | None = None) -> None:
        assert boto3 is not None, "boto3 must be installed to read from S3: `pip install boto3`"
        if bucket is None:
            bucket = get_s3_data_bucket()
        self._key = name if prefix is None else f"{prefix}/{name}"
        self._bucket = bucket
        super().__init__()

    def key(self) -> str:
        return self._key

    def bucket(self) -> str:
        return self._bucket


class SdsBaseIterReaderDataPipe(IterDataPipe[tuple[str, int, Reader]], SdsBaseReaderDataPipe):
    """Defines a base class for reading a dataset iteratively.

    This dataset is useful for streaming data from a remote file system, since
    it caches the per-worker read data as it is being read to avoid downloading
    multiple times. It also allows setting a maximum number of bytes to store
    in the disk cache to avoid exceeding available disk space.

    Parameters:
        key: A unique key for this dataset, which is used for caching.
        max_bytes: The maximum number of bytes to store in the disk cache.
            If None, no limit is set.
        data_dir: The root directory for storing cached data. If None, the
            default data directory is used.
    """

    def __init__(
        self,
        key: str,
        *,
        max_bytes: int | None = None,
        data_dir: str | Path | None = None,
    ) -> None:
        # Root directory for storing cached data.
        self.root_dir = (get_data_dir() / "sds-cache" if data_dir is None else Path(data_dir)) / key
        self.root_dir.mkdir(parents=True, exist_ok=True)
        self.max_bytes = max_bytes
        self.max_bytes_per_worker: int | None = None
        self.worker_cache_path = self.root_dir / "uninitialized"
        self.worker_cache_path_tmp: Path | None = None

        # Iteration variables.
        self.fp_in: Streamer | None = None
        self.fp_out: IO[bytes] | None = None
        self.index = 0
        self.start = 0
        self.end = 0
        self.num_bytes_downloaded = 0

        super().__init__()

    def get_header_and_offsets(self) -> tuple[Header, int]:
        header_path = self.root_dir / "header.sds"

        if header_path.exists():
            with open(header_path, "rb") as f:
                assert f.read(len(MAGIC)) == MAGIC, "Invalid magic number."
                header, header_num_bytes = Header.read(f)
            return header, header_num_bytes

        header, header_num_bytes = super().get_header_and_offsets()
        with open(header_path, "wb") as f:
            f.write(MAGIC)
            header.write(f)

        return header, header_num_bytes

    def __iter__(self) -> Iterator[tuple[str, int, Reader]]:
        worker_info = get_worker_info()
        worker_id, num_workers = worker_info.worker_id, worker_info.num_workers

        # If not provided, sets the maximum number of bytes to download to
        # 80% of the available disk space.
        if self.max_bytes is None:
            root_dir_free_space = shutil.disk_usage(self.root_dir.parent).free
            self.max_bytes_per_worker = round((root_dir_free_space / num_workers) * 0.8)
        else:
            self.max_bytes_per_worker = self.max_bytes // num_workers

        # If the complete worker file has already been written, then we can
        # just read from the disk instead of downloading the file. We check
        # this by comparing the size of the file in the disk with the size
        # of the file in the header.
        self.worker_cache_path = self.root_dir / f"worker_{worker_id}.sds"

        self.num_bytes_downloaded = 0

        start, end = split_n_items_across_workers(len(self.header.files), worker_id, num_workers)
        self.start, self.end = start, end

        if self.worker_cache_path.exists():
            self.worker_cache_path_tmp = None
            self.fp_in = None
            self.fp_out = None
            self.index = start

        else:
            self.worker_cache_path_tmp = self.worker_cache_path.with_suffix(".tmp")
            start_off, end_off, end_len = self.offsets[start], self.offsets[end - 1], self.header.files[end - 1][1]
            self.fp_in = self.open(start_off, end_len + (end_off - start_off))
            self.fp_out = open(self.worker_cache_path_tmp, "wb")
            self.index = start

        return self

    def read_from_cache(self, start: int, length: int) -> Streamer:
        cache_path = self.worker_cache_path if self.worker_cache_path_tmp is None else self.worker_cache_path_tmp
        f = open(cache_path, "rb")
        f.seek(start)
        return ClippedStreamWrapper(f, length)

    def __next__(self) -> tuple[str, int, Reader]:
        assert self.max_bytes_per_worker is not None
        assert self.worker_cache_path is not None

        if self.index >= self.end:
            if self.worker_cache_path_tmp is not None:
                assert self.fp_out is not None
                self.fp_out.flush()
                self.fp_out.close()
                self.worker_cache_path_tmp.rename(self.worker_cache_path)
            raise StopIteration

        index = self.index
        name, length = self.header.files[index]
        offset = self.offsets[index] - self.offsets[self.start]
        self.index += 1

        if self.fp_in is not None:
            # There's some weird logic that needs to be complied with here.
            # It's too late at night for me to figure this out though.
            assert self.fp_out is not None
            while self.num_bytes_downloaded < offset + length:
                bts = next(self.fp_in)
                self.fp_out.write(bts)
                self.num_bytes_downloaded += len(bts)
                if self.num_bytes_downloaded > offset + length:
                    break
            self.fp_out.flush()

        return name, index, Reader(self.read_from_cache, length, offset)


@functional_datapipe("sds_file_iter_reader")
class SdsFileIterReaderDataPipe(SdsBaseIterReaderDataPipe, SdsFileReaderDataPipe):
    def __init__(
        self,
        path: str | Path,
        *,
        max_bytes: int | None = None,
        data_dir: str | Path | None = None,
    ) -> None:
        self._path = path
        key = f"path-{hash(path)}"
        super().__init__(key, max_bytes=max_bytes, data_dir=data_dir)

    def path(self) -> str | Path:
        return self._path


@functional_datapipe("sds_http_iter_reader")
class SdsHttpIterReaderDataPipe(SdsBaseIterReaderDataPipe, SdsHttpReaderDataPipe):
    def __init__(self, url: str, *, max_bytes: int | None = None, data_dir: str | Path | None = None) -> None:
        self._url = url
        key = f"url-{hash(url)}"
        super().__init__(key, max_bytes=max_bytes, data_dir=data_dir)

    def url(self) -> str:
        return self._url


@functional_datapipe("sds_s3_iter_reader")
class SdsS3IterReaderDataPipe(SdsBaseIterReaderDataPipe, SdsS3ReaderDataPipe):
    def __init__(
        self,
        name: str,
        prefix: str | None = None,
        bucket: str | None = None,
        *,
        max_bytes: int | None = None,
        data_dir: str | Path | None = None,
    ) -> None:
        assert boto3 is not None, "boto3 must be installed to read from S3: `pip install boto3`"
        if bucket is None:
            bucket = get_s3_data_bucket()
        self._key = name if prefix is None else f"{prefix}/{name}"
        self._bucket = bucket
        key = f"s3-{self._bucket}-{self._key.replace('/', '-')}"
        super().__init__(key, max_bytes=max_bytes, data_dir=data_dir)

    def key(self) -> str:
        return self._key

    def bucket(self) -> str:
        return self._bucket


def upload_data_to_s3(
    file_path: str | Path,
    prefix: str | None = None,
    name: str | None = None,
    bucket: str | None = None,
) -> None:
    """Uploads a data file to S3.

    Args:
        file_path: The path to the file to upload.
        prefix: The prefix to use for the uploaded file, if requested.
        name: The name to use for the uploaded file. If not specified, will
            default to the name of the file.
        bucket: The bucket to upload to. If not specified, will default to the
            bucket specified by ``get_s3_data_bucket``.
    """
    assert boto3 is not None, "boto3 must be installed to read from S3: `pip install boto3`"

    if name is None:
        name = Path(file_path).name
    key = name if prefix is None else f"{prefix}/{name}"

    if bucket is None:
        bucket = get_s3_data_bucket()

    s3 = boto3.client("s3")
    s3.upload_file(str(file_path), bucket, key)
