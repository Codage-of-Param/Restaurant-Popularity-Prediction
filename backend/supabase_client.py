import os
from pathlib import Path
from typing import Union
from typing import Optional


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_supabase_client():
    """
    Creates a Supabase client using env vars:
      - SUPABASE_URL
      - SUPABASE_SERVICE_ROLE_KEY (preferred for server-side scripts) OR SUPABASE_ANON_KEY
    """
    try:
        from dotenv import load_dotenv  # type: ignore
        from pathlib import Path
        dotenv_path = Path(__file__).resolve().parent.parent / ".env"
        load_dotenv(dotenv_path)
    except Exception:
        pass

    from supabase import create_client  # type: ignore

    url = _require_env("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    if not key:
        raise RuntimeError(
            "Missing SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY environment variable."
        )
    return create_client(url, key)


def upload_file(
    *,
    bucket: str,
    remote_path: str,
    local_path: Union[str, Path],
    upsert: bool = True,
    content_type: Optional[str] = None,
) -> None:
    client = get_supabase_client()
    local_path = Path(local_path)
    if not local_path.exists():
        raise FileNotFoundError(str(local_path))

    with local_path.open("rb") as f:
        # Some versions of the Supabase library pass options directly to headers.
        # This causes 'Header value must be str or bytes, not <class 'bool'>' error.
        options = {"upsert": str(upsert).lower()}
        if content_type:
            options["content-type"] = content_type
        client.storage.from_(bucket).upload(path=remote_path, file=f, file_options=options)


def download_file(
    *,
    bucket: str,
    remote_path: str,
    local_path: Union[str, Path],
) -> None:
    client = get_supabase_client()
    local_path = Path(local_path)
    data = client.storage.from_(bucket).download(remote_path)
    local_path.write_bytes(data)
