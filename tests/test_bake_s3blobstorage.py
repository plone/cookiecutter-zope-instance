from utils import bake_in_temp_dir


def test_bake_s3blobstorage_with_filestorage(cookies):
    extra_context = {
        "db_storage": "s3blobstorage",
        "db_s3blobs_base_storage": "direct",
        "db_s3blobs_bucket_name": "test-bucket",
    }
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:
        assert result.exit_code == 0, result.exception
        assert result.exception is None

        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()

        # S3 wrapper present
        assert "%import zodb_s3blobs" in zope_conf
        assert "<s3blobstorage>" in zope_conf
        assert "</s3blobstorage>" in zope_conf
        assert "bucket-name test-bucket" in zope_conf
        assert "s3blobs-cache" in zope_conf

        # Inner filestorage present
        assert "<filestorage>" in zope_conf
        assert "</filestorage>" in zope_conf
        assert "pack-keep-old" in zope_conf

        # blob-dir must NOT appear inside filestorage (s3 handles blobs)
        assert "blob-dir" not in zope_conf

        # s3blobs-cache directory created by post-gen hook
        cache_dir = result.project_path / "var" / "s3blobs-cache"
        assert cache_dir.is_dir()

        # filestorage directory created
        filestorage_dir = result.project_path / "var" / "filestorage"
        assert filestorage_dir.is_dir()


def test_bake_s3blobstorage_with_relstorage(cookies):
    extra_context = {
        "db_storage": "s3blobstorage",
        "db_s3blobs_base_storage": "relstorage",
        "db_s3blobs_bucket_name": "test-bucket",
        "db_s3blobs_s3_endpoint_url": "https://minio:9000",
    }
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:
        assert result.exit_code == 0, result.exception
        assert result.exception is None

        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()

        # S3 wrapper with relstorage inside
        assert "<s3blobstorage>" in zope_conf
        assert "<relstorage>" in zope_conf
        assert "s3-endpoint-url https://minio:9000" in zope_conf
        assert "%import relstorage" in zope_conf

        # blob settings must NOT appear inside relstorage
        assert "shared-blob-dir" not in zope_conf
        assert "blob-dir" not in zope_conf
        assert "blob-cache-size" not in zope_conf

        # relstorage utility files should be cleaned up
        etc_path = result.project_path / "etc"
        etc_files = [f.name for f in etc_path.iterdir()]
        assert "relstorage-pack.conf" not in etc_files
        assert "relstorage-import.conf" not in etc_files
        assert "relstorage-export.conf" not in etc_files


def test_bake_s3blobstorage_with_zeo(cookies):
    extra_context = {
        "db_storage": "s3blobstorage",
        "db_s3blobs_base_storage": "zeo",
        "db_s3blobs_bucket_name": "test-bucket",
    }
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:
        assert result.exit_code == 0, result.exception
        assert result.exception is None

        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()

        # S3 wrapper with zeoclient inside
        assert "<s3blobstorage>" in zope_conf
        assert "<zeoclient>" in zope_conf

        # blob settings must NOT appear inside zeoclient
        assert "shared-blob-dir" not in zope_conf
        assert "blob-dir" not in zope_conf


def test_bake_s3blobstorage_optional_params(cookies):
    extra_context = {
        "db_storage": "s3blobstorage",
        "db_s3blobs_base_storage": "direct",
        "db_s3blobs_bucket_name": "my-bucket",
        "db_s3blobs_s3_prefix": "myprefix",
        "db_s3blobs_s3_region": "eu-west-1",
        "db_s3blobs_s3_access_key": "TESTKEY_NOT_REAL_0001",
        "db_s3blobs_s3_secret_key": "testsecret/NOT_A_REAL_KEY_FOR_TESTING",
        "db_s3blobs_s3_use_ssl": "false",
        "db_s3blobs_s3_addressing_style": "path",
        "db_s3blobs_cache_size": "2GB",
    }
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:
        assert result.exit_code == 0, result.exception
        assert result.exception is None

        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()

        assert "bucket-name my-bucket" in zope_conf
        assert "s3-prefix myprefix" in zope_conf
        assert "s3-region eu-west-1" in zope_conf
        assert "s3-access-key TESTKEY_NOT_REAL_0001" in zope_conf
        assert "s3-secret-key testsecret/NOT_A_REAL_KEY_FOR_TESTING" in zope_conf
        assert "s3-use-ssl false" in zope_conf
        assert "s3-addressing-style path" in zope_conf
        assert "cache-size 2GB" in zope_conf


def test_bake_s3blobstorage_missing_bucket_name_fails(cookies):
    extra_context = {
        "db_storage": "s3blobstorage",
        "db_s3blobs_base_storage": "direct",
        "db_s3blobs_bucket_name": "",
    }
    result = cookies.bake(extra_context=extra_context)
    assert result.exit_code != 0


def test_bake_defaults_unchanged(cookies):
    """Regression test: default bake still uses filestorage with blob-dir."""
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0
        assert result.exception is None

        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()

        assert "<filestorage>" in zope_conf
        assert "blob-dir" in zope_conf
        # s3blobstorage should not appear in defaults
        assert "s3blobstorage" not in zope_conf
        assert "zodb_s3blobs" not in zope_conf
