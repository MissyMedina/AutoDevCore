#!/usr/bin/env python3
"""
Async File I/O Optimization Utilities
Implements async file operations, batch processing, and efficient serialization.
"""

import asyncio
import json
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import aiofiles
import aiofiles.os
from concurrent.futures import ThreadPoolExecutor
import gzip
import lz4.frame

class AsyncFileManager:
    """Async file operations manager with optimization."""

    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._file_cache = {}
        self._compression_cache = {}

    async def read_file(
        self, file_path: Union[str, Path], encoding: str = "utf-8"
    ) -> str:
        """Async file reading with caching."""
        file_path = Path(file_path)

        # Check cache first
        cache_key = f"{file_path}:{encoding}"
        if cache_key in self._file_cache:
            return self._file_cache[cache_key]

        async with aiofiles.open(file_path, "r", encoding=encoding) as f:
            content = await f.read()

        # Cache small files (< 1MB)
        if len(content) < 1024 * 1024:
            self._file_cache[cache_key] = content

        return content

    async def write_file(
        self,
        file_path: Union[str, Path],
        content: str,
        encoding: str = "utf-8",
        create_dirs: bool = True,
    ) -> None:
        """Async file writing with directory creation."""
        file_path = Path(file_path)

        if create_dirs:
            await aiofiles.os.makedirs(file_path.parent, exist_ok=True)

        async with aiofiles.open(file_path, "w", encoding=encoding) as f:
            await f.write(content)

        # Update cache
        cache_key = f"{file_path}:{encoding}"
        if len(content) < 1024 * 1024:
            self._file_cache[cache_key] = content

    async def read_json(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Async JSON reading with error handling."""
        try:
            content = await self.read_file(file_path)
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {e}")
        except FileNotFoundError:
            return {}

    async def write_json(
        self,
        file_path: Union[str, Path],
        data: Dict[str, Any],
        indent: int = 2,
        create_dirs: bool = True,
    ) -> None:
        """Async JSON writing with formatting."""
        content = json.dumps(data, indent=indent, ensure_ascii=False)
        await self.write_file(file_path, content, create_dirs=create_dirs)

    async def read_binary(self, file_path: Union[str, Path]) -> bytes:
        """Async binary file reading."""
        async with aiofiles.open(file_path, "rb") as f:
            return await f.read()

    async def write_binary(
        self, file_path: Union[str, Path], data: bytes, create_dirs: bool = True
    ) -> None:
        """Async binary file writing."""
        file_path = Path(file_path)

        if create_dirs:
            await aiofiles.os.makedirs(file_path.parent, exist_ok=True)

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(data)

    async def batch_read_files(self, file_paths: List[Union[str, Path]]) -> List[str]:
        """Read multiple files concurrently."""
        tasks = [self.read_file(path) for path in file_paths]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def batch_write_files(
        self, file_data: List[tuple[Union[str, Path], str]]
    ) -> None:
        """Write multiple files concurrently."""
        tasks = [self.write_file(path, content) for path, content in file_data]
        await asyncio.gather(*tasks)

    async def compress_file(
        self, file_path: Union[str, Path], compression: str = "gzip"
    ) -> Path:
        """Compress a file asynchronously."""
        file_path = Path(file_path)

        if compression == "gzip":
            compressed_path = file_path.with_suffix(file_path.suffix + ".gz")

            def compress_sync():
                with open(file_path, "rb") as f_in:
                    with gzip.open(compressed_path, "wb") as f_out:
                        f_out.writelines(f_in)
                return compressed_path

            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self.executor, compress_sync)

        elif compression == "lz4":
            compressed_path = file_path.with_suffix(file_path.suffix + ".lz4")

            def compress_sync():
                with open(file_path, "rb") as f_in:
                    with lz4.frame.open(compressed_path, "wb") as f_out:
                        f_out.write(f_in.read())
                return compressed_path

            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self.executor, compress_sync)

        else:
            raise ValueError(f"Unsupported compression: {compression}")

    async def decompress_file(self, compressed_path: Union[str, Path]) -> Path:
        """Decompress a file asynchronously."""
        compressed_path = Path(compressed_path)

        if compressed_path.suffix == ".gz":
            output_path = compressed_path.with_suffix("")

            def decompress_sync():
                with gzip.open(compressed_path, "rb") as f_in:
                    with open(output_path, "wb") as f_out:
                        f_out.write(f_in.read())
                return output_path

            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self.executor, decompress_sync)

        elif compressed_path.suffix == ".lz4":
            output_path = compressed_path.with_suffix("")

            def decompress_sync():
                with lz4.frame.open(compressed_path, "rb") as f_in:
                    with open(output_path, "wb") as f_out:
                        f_out.write(f_in.read())
                return output_path

            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self.executor, decompress_sync)

        else:
            raise ValueError(f"Unsupported compressed file: {compressed_path}")

    def clear_cache(self) -> None:
        """Clear file cache."""
        self._file_cache.clear()
        self._compression_cache.clear()

    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            "cached_files": len(self._file_cache),
            "cache_size_mb": sum(
                len(content.encode()) for content in self._file_cache.values()
            )
            / (1024 * 1024),
        }

class BatchProcessor:
    """Batch processing for efficient I/O operations."""

    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
        self.file_manager = AsyncFileManager()

    async def process_files_in_batches(
        self,
        file_paths: List[Union[str, Path]],
        processor_func,
        output_dir: Optional[Union[str, Path]] = None,
    ) -> List[Any]:
        """Process files in batches to manage memory usage."""
        results = []

        for i in range(0, len(file_paths), self.batch_size):
            batch = file_paths[i : i + self.batch_size]

            # Read batch
            batch_contents = await self.file_manager.batch_read_files(batch)

            # Process batch
            batch_results = []
            for j, content in enumerate(batch_contents):
                if isinstance(content, Exception):
                    batch_results.append(f"Error reading {batch[j]}: {content}")
                else:
                    result = await processor_func(content, batch[j])
                    batch_results.append(result)

            # Write results if output directory specified
            if output_dir:
                output_dir = Path(output_dir)
                write_tasks = []
                for j, result in enumerate(batch_results):
                    if not isinstance(result, str) or not result.startswith("Error"):
                        output_path = output_dir / f"processed_{batch[j].name}"
                        write_tasks.append((output_path, str(result)))

                if write_tasks:
                    await self.file_manager.batch_write_files(write_tasks)

            results.extend(batch_results)

            # Optional: Force garbage collection between batches
            import gc

            gc.collect()

        return results

class EfficientSerializer:
    """Efficient serialization with compression options."""

    @staticmethod
    async def serialize_json_compressed(
        data: Any, file_path: Union[str, Path], compression: str = "gzip"
    ) -> None:
        """Serialize data to compressed JSON."""
        json_data = json.dumps(data, ensure_ascii=False).encode("utf-8")

        if compression == "gzip":
            compressed_data = gzip.compress(json_data)
        elif compression == "lz4":
            compressed_data = lz4.frame.compress(json_data)
        else:
            compressed_data = json_data

        file_manager = AsyncFileManager()
        await file_manager.write_binary(file_path, compressed_data)

    @staticmethod
    async def deserialize_json_compressed(
        file_path: Union[str, Path], compression: str = "gzip"
    ) -> Any:
        """Deserialize data from compressed JSON."""
        file_manager = AsyncFileManager()
        compressed_data = await file_manager.read_binary(file_path)

        if compression == "gzip":
            json_data = gzip.decompress(compressed_data)
        elif compression == "lz4":
            json_data = lz4.frame.decompress(compressed_data)
        else:
            json_data = compressed_data

        return json.loads(json_data.decode("utf-8"))

    @staticmethod
    async def serialize_pickle_compressed(
        data: Any, file_path: Union[str, Path], compression: str = "gzip"
    ) -> None:
        """Serialize data to compressed pickle."""
        pickle_data = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)

        if compression == "gzip":
            compressed_data = gzip.compress(pickle_data)
        elif compression == "lz4":
            compressed_data = lz4.frame.compress(pickle_data)
        else:
            compressed_data = pickle_data

        file_manager = AsyncFileManager()
        await file_manager.write_binary(file_path, compressed_data)

# Global instances
async_file_manager = AsyncFileManager()
batch_processor = BatchProcessor()
efficient_serializer = EfficientSerializer()

# Convenience functions
async def read_file_async(file_path: Union[str, Path]) -> str:
    """Convenience function for async file reading."""
    return await async_file_manager.read_file(file_path)

async def write_file_async(file_path: Union[str, Path], content: str) -> None:
    """Convenience function for async file writing."""
    await async_file_manager.write_file(file_path, content)

async def read_json_async(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Convenience function for async JSON reading."""
    return await async_file_manager.read_json(file_path)

async def write_json_async(file_path: Union[str, Path], data: Dict[str, Any]) -> None:
    """Convenience function for async JSON writing."""
    await async_file_manager.write_json(file_path, data)
