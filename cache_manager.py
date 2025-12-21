# Cache Manager dengan DuckDB dan Multi-Layer Caching
import streamlit as st
import duckdb
import pandas as pd
import hashlib
import pickle
import os
from pathlib import Path
from datetime import datetime, timedelta
from functools import wraps
import pyarrow.parquet as pq
from cachetools import TTLCache, LRUCache
import threading

class CacheManager:
    """
    Advanced caching system dengan 3 layers:
    1. Memory Cache (LRU) - fastest, limited size
    2. DuckDB Persistent Cache - fast, unlimited size
    3. Remote Source - slowest, but always available
    """

    def __init__(self, cache_dir=".cache", max_memory_cache_size=100, ttl_seconds=21600):
        """
        Initialize Cache Manager

        Args:
            cache_dir: Directory untuk menyimpan cache files
            max_memory_cache_size: Maksimum items dalam memory cache
            ttl_seconds: Time to live untuk cache dalam detik (default 6 jam)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

        # Layer 1: Memory cache dengan LRU eviction
        self.memory_cache = LRUCache(maxsize=max_memory_cache_size)
        self.cache_lock = threading.Lock()

        # Layer 2: DuckDB persistent cache
        self.db_path = self.cache_dir / "duckdb_cache.db"
        self.ttl_seconds = ttl_seconds

        # Initialize DuckDB connection pool
        self._init_duckdb_cache()

    def _init_duckdb_cache(self):
        """Initialize DuckDB cache tables"""
        con = duckdb.connect(str(self.db_path))

        # Create cache metadata table
        con.execute("""
            CREATE TABLE IF NOT EXISTS cache_metadata (
                cache_key VARCHAR PRIMARY KEY,
                url VARCHAR,
                created_at TIMESTAMP,
                expires_at TIMESTAMP,
                row_count INTEGER,
                file_size INTEGER
            )
        """)

        # Create cache data directory for parquet files
        self.cache_data_dir = self.cache_dir / "parquet"
        self.cache_data_dir.mkdir(exist_ok=True)

        con.close()

    def _generate_cache_key(self, url, params=None):
        """Generate unique cache key dari URL dan parameters"""
        key_string = f"{url}_{params}" if params else url
        return hashlib.md5(key_string.encode()).hexdigest()

    def _get_cache_path(self, cache_key):
        """Get path untuk cache file"""
        return self.cache_data_dir / f"{cache_key}.parquet"

    def get_cached_data(self, url, params=None):
        """
        Retrieve data dari cache (memory -> DuckDB -> None)

        Returns:
            DataFrame jika ada di cache dan masih valid, None jika tidak
        """
        cache_key = self._generate_cache_key(url, params)

        # Layer 1: Check memory cache
        with self.cache_lock:
            if cache_key in self.memory_cache:
                return self.memory_cache[cache_key].copy()

        # Layer 2: Check DuckDB cache
        con = duckdb.connect(str(self.db_path), read_only=True)

        result = con.execute("""
            SELECT cache_key, expires_at
            FROM cache_metadata
            WHERE cache_key = ? AND expires_at > CURRENT_TIMESTAMP
        """, [cache_key]).fetchone()

        con.close()

        if result:
            # Cache hit di DuckDB - load parquet file
            cache_path = self._get_cache_path(cache_key)
            if cache_path.exists():
                df = pd.read_parquet(cache_path)

                # Promote to memory cache
                with self.cache_lock:
                    self.memory_cache[cache_key] = df.copy()

                return df

        return None

    def set_cached_data(self, url, df, params=None):
        """
        Save data ke cache (memory + DuckDB)

        Args:
            url: Source URL
            df: DataFrame to cache
            params: Additional parameters untuk cache key
        """
        cache_key = self._generate_cache_key(url, params)
        cache_path = self._get_cache_path(cache_key)

        # Save to parquet (compressed)
        df.to_parquet(
            cache_path,
            engine='pyarrow',
            compression='snappy',
            index=False
        )

        # Update metadata di DuckDB
        con = duckdb.connect(str(self.db_path))

        expires_at = datetime.now() + timedelta(seconds=self.ttl_seconds)
        file_size = cache_path.stat().st_size

        con.execute("""
            INSERT OR REPLACE INTO cache_metadata
            (cache_key, url, created_at, expires_at, row_count, file_size)
            VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?, ?)
        """, [cache_key, url, expires_at, len(df), file_size])

        con.close()

        # Save to memory cache
        with self.cache_lock:
            self.memory_cache[cache_key] = df.copy()

    def clear_expired_cache(self):
        """Hapus expired cache entries"""
        con = duckdb.connect(str(self.db_path))

        # Get expired cache keys
        expired_keys = con.execute("""
            SELECT cache_key
            FROM cache_metadata
            WHERE expires_at < CURRENT_TIMESTAMP
        """).fetchall()

        # Delete expired entries
        for (cache_key,) in expired_keys:
            cache_path = self._get_cache_path(cache_key)
            if cache_path.exists():
                cache_path.unlink()

            con.execute("DELETE FROM cache_metadata WHERE cache_key = ?", [cache_key])

        con.close()

        return len(expired_keys)

    def get_cache_stats(self):
        """Get cache statistics"""
        con = duckdb.connect(str(self.db_path), read_only=True)

        stats = con.execute("""
            SELECT
                COUNT(*) as total_entries,
                SUM(row_count) as total_rows,
                SUM(file_size) as total_size_bytes,
                COUNT(CASE WHEN expires_at > CURRENT_TIMESTAMP THEN 1 END) as active_entries
            FROM cache_metadata
        """).fetchone()

        con.close()

        return {
            'total_entries': stats[0],
            'total_rows': stats[1],
            'total_size_mb': stats[2] / (1024 * 1024) if stats[2] else 0,
            'active_entries': stats[3],
            'memory_cache_size': len(self.memory_cache)
        }


# Global cache manager instance
@st.cache_resource
def get_cache_manager():
    """Get atau create global cache manager instance"""
    return CacheManager(
        cache_dir=".cache",
        max_memory_cache_size=100,
        ttl_seconds=21600  # 6 hours
    )


# DuckDB Connection Pool untuk query performa
class DuckDBConnectionPool:
    """Connection pool untuk DuckDB queries"""

    def __init__(self, pool_size=5):
        self.pool_size = pool_size
        self.connections = []
        self.lock = threading.Lock()

        # Pre-create connections
        for _ in range(pool_size):
            self.connections.append(duckdb.connect(database=':memory:'))

    def get_connection(self):
        """Get connection dari pool"""
        with self.lock:
            if self.connections:
                return self.connections.pop()
            else:
                # Create new connection if pool is empty
                return duckdb.connect(database=':memory:')

    def return_connection(self, con):
        """Return connection to pool"""
        with self.lock:
            if len(self.connections) < self.pool_size:
                self.connections.append(con)
            else:
                con.close()


@st.cache_resource
def get_duckdb_pool():
    """Get global DuckDB connection pool"""
    return DuckDBConnectionPool(pool_size=5)


def cached_read_parquet(url, params=None, force_refresh=False):
    """
    Read parquet dengan intelligent caching

    Args:
        url: URL to parquet file
        params: Additional parameters
        force_refresh: Force refresh dari source

    Returns:
        DataFrame
    """
    cache_mgr = get_cache_manager()

    # Check cache jika tidak force refresh
    if not force_refresh:
        cached_df = cache_mgr.get_cached_data(url, params)
        if cached_df is not None:
            return cached_df

    # Cache miss - load dari remote
    try:
        # Use DuckDB untuk fast parquet loading
        con = duckdb.connect(database=':memory:')
        df = con.execute(f"SELECT * FROM read_parquet('{url}')").df()
        con.close()

        # Save to cache
        cache_mgr.set_cached_data(url, df, params)

        return df

    except Exception as e:
        st.error(f"Error loading data dari {url}: {str(e)}")
        raise


def cached_query(df, query, cache_key=None):
    """
    Execute DuckDB query dengan caching hasil

    Args:
        df: Input DataFrame atau nama table
        query: SQL query
        cache_key: Optional cache key untuk hasil query

    Returns:
        Query result sebagai DataFrame
    """
    if cache_key:
        cache_mgr = get_cache_manager()
        cached_result = cache_mgr.get_cached_data(cache_key)
        if cached_result is not None:
            return cached_result

    # Execute query
    pool = get_duckdb_pool()
    con = pool.get_connection()

    try:
        if isinstance(df, pd.DataFrame):
            result = con.execute(query).df()
        else:
            result = con.execute(query).df()

        # Cache result jika ada cache_key
        if cache_key:
            cache_mgr.set_cached_data(cache_key, result)

        return result

    finally:
        pool.return_connection(con)


# Auto cleanup expired cache saat startup
def cleanup_expired_cache():
    """Cleanup expired cache entries"""
    cache_mgr = get_cache_manager()
    expired_count = cache_mgr.clear_expired_cache()
    return expired_count
