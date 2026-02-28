from utils import bake_in_temp_dir


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project_path.is_dir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert 'inituser' in found_toplevel_files
        assert 'etc' in found_toplevel_files
        etc_path = result.project_path / "etc"
        assert etc_path.is_dir()
        etc_files = [f.name for f in etc_path.iterdir()]
        assert 'zope.conf' in etc_files
        assert 'zope.ini' in etc_files
        assert 'site.zcml' in etc_files


def test_bake_with_pgjsonb(cookies):
    """Bake with pgjsonb storage and verify generated zope.conf."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "pgjsonb",
            "db_pgjsonb_dsn": "dbname=zodb host=localhost port=5433",
        },
    ) as result:
        assert result.exit_code == 0
        assert result.exception is None

        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "%import zodb_pgjsonb" in zope_conf
        assert "<pgjsonb>" in zope_conf
        assert "dsn dbname=zodb host=localhost port=5433" in zope_conf
        assert "</pgjsonb>" in zope_conf
        # relstorage files should be removed
        assert not (result.project_path / "etc" / "relstorage-pack.conf").exists()


def test_bake_with_pgjsonb_s3(cookies):
    """Bake with pgjsonb + S3 and verify S3 params render."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "pgjsonb",
            "db_pgjsonb_dsn": "dbname=zodb",
            "db_pgjsonb_s3_bucket_name": "my-blobs",
            "db_pgjsonb_s3_endpoint_url": "http://localhost:9000",
            "db_pgjsonb_s3_use_ssl": "false",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "s3-bucket-name my-blobs" in zope_conf
        assert "s3-endpoint-url http://localhost:9000" in zope_conf
        assert "s3-use-ssl false" in zope_conf


def test_bake_with_pgjsonb_history_preserving(cookies):
    """Bake with history-preserving mode enabled."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "pgjsonb",
            "db_pgjsonb_dsn": "dbname=zodb",
            "db_pgjsonb_history_preserving": "true",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "history-preserving true" in zope_conf


def test_bake_with_pgjsonb_all_options(cookies):
    """Bake with all pgjsonb options set."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "pgjsonb",
            "db_pgjsonb_dsn": "dbname=zodb host=db",
            "db_pgjsonb_name": "mydb",
            "db_pgjsonb_history_preserving": "true",
            "db_pgjsonb_cache_local_mb": "64",
            "db_pgjsonb_pool_size": "5",
            "db_pgjsonb_pool_max_size": "20",
            "db_pgjsonb_pool_timeout": "60.0",
            "db_pgjsonb_s3_bucket_name": "blobs",
            "db_pgjsonb_s3_prefix": "myapp/",
            "db_pgjsonb_s3_endpoint_url": "http://minio:9000",
            "db_pgjsonb_s3_region": "us-east-1",
            "db_pgjsonb_s3_access_key": "minioadmin",
            "db_pgjsonb_s3_secret_key": "minioadmin",
            "db_pgjsonb_s3_use_ssl": "false",
            "db_pgjsonb_blob_threshold": "2MB",
            "db_pgjsonb_blob_cache_dir": "var/blobcache",
            "db_pgjsonb_blob_cache_size": "5GB",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "name mydb" in zope_conf
        assert "history-preserving true" in zope_conf
        assert "cache-local-mb 64" in zope_conf
        assert "pool-size 5" in zope_conf
        assert "pool-max-size 20" in zope_conf
        assert "pool-timeout 60.0" in zope_conf
        assert "s3-bucket-name blobs" in zope_conf
        assert "s3-prefix myapp/" in zope_conf
        assert "s3-region us-east-1" in zope_conf
        assert "s3-access-key minioadmin" in zope_conf
        assert "s3-secret-key minioadmin" in zope_conf
        assert "s3-use-ssl false" in zope_conf
        assert "blob-threshold 2MB" in zope_conf
        assert "blob-cache-dir" in zope_conf
        assert "blob-cache-size 5GB" in zope_conf


def test_bake_with_pgjsonb_no_dsn_fails(cookies):
    """Bake with pgjsonb but no DSN should fail in the pre-gen hook."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "pgjsonb",
        },
    ) as result:
        assert result.exit_code != 0


# =============================================================================
# z3blobs (S3 blob wrapper) tests
# =============================================================================


def test_bake_with_z3blobs_disabled_default(cookies):
    """Default bake should have no s3blobstorage wrapper."""
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "s3blobstorage" not in zope_conf
        assert "zodb_s3blobs" not in zope_conf


def test_bake_with_z3blobs_direct(cookies):
    """z3blobs wrapping filestorage: wrapper present, blob-dir suppressed."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "direct",
            "db_z3blobs_enabled": "true",
            "db_z3blobs_bucket_name": "my-blobs",
            "db_z3blobs_cache_dir": "var/s3cache",
        },
    ) as result:
        assert result.exit_code == 0
        assert result.exception is None

        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "%import zodb_s3blobs" in zope_conf
        assert "<s3blobstorage>" in zope_conf
        assert "bucket-name my-blobs" in zope_conf
        assert "cache-dir" in zope_conf
        assert "</s3blobstorage>" in zope_conf
        assert "<filestorage>" in zope_conf
        # blob-dir should be suppressed inside filestorage
        # (only appears inside s3blobstorage as cache-dir)
        lines = zope_conf.split("\n")
        in_filestorage = False
        for line in lines:
            stripped = line.strip()
            if "<filestorage>" in stripped:
                in_filestorage = True
            elif "</filestorage>" in stripped:
                in_filestorage = False
            elif in_filestorage and stripped.startswith("blob-dir"):
                raise AssertionError("blob-dir found inside <filestorage> when z3blobs active")


def test_bake_with_z3blobs_relstorage(cookies):
    """z3blobs wrapping relstorage: wrapper present, blob settings suppressed."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "relstorage",
            "db_z3blobs_enabled": "true",
            "db_z3blobs_bucket_name": "my-blobs",
            "db_z3blobs_cache_dir": "var/s3cache",
            "db_relstorage_postgresql_dsn": "dbname=zodb",
        },
    ) as result:
        assert result.exit_code == 0
        assert result.exception is None

        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "%import zodb_s3blobs" in zope_conf
        assert "<s3blobstorage>" in zope_conf
        assert "<relstorage>" in zope_conf
        # blob settings should be suppressed inside relstorage
        lines = zope_conf.split("\n")
        in_relstorage = False
        for line in lines:
            stripped = line.strip()
            if "<relstorage>" in stripped:
                in_relstorage = True
            elif "</relstorage>" in stripped:
                in_relstorage = False
            elif in_relstorage:
                assert not stripped.startswith("shared-blob-dir"), \
                    "shared-blob-dir found inside <relstorage> when z3blobs active"
                assert not stripped.startswith("blob-dir"), \
                    "blob-dir found inside <relstorage> when z3blobs active"


def test_bake_with_z3blobs_all_options(cookies):
    """All z3blobs parameters should render in zope.conf."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "direct",
            "db_z3blobs_enabled": "true",
            "db_z3blobs_bucket_name": "prod-blobs",
            "db_z3blobs_s3_prefix": "site1/",
            "db_z3blobs_s3_endpoint_url": "https://s3.example.com",
            "db_z3blobs_s3_region": "eu-west-1",
            "db_z3blobs_s3_access_key": "AKIAIOSFODNN7EXAMPLE",
            "db_z3blobs_s3_secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            "db_z3blobs_s3_use_ssl": "true",
            "db_z3blobs_s3_addressing_style": "path",
            "db_z3blobs_s3_sse_customer_key": "c2VjcmV0",
            "db_z3blobs_cache_dir": "var/s3cache",
            "db_z3blobs_cache_size": "10GB",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "bucket-name prod-blobs" in zope_conf
        assert "s3-prefix site1/" in zope_conf
        assert "s3-endpoint-url https://s3.example.com" in zope_conf
        assert "s3-region eu-west-1" in zope_conf
        assert "s3-access-key AKIAIOSFODNN7EXAMPLE" in zope_conf
        assert "s3-secret-key wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" in zope_conf
        assert "s3-use-ssl true" in zope_conf
        assert "s3-addressing-style path" in zope_conf
        assert "s3-sse-customer-key c2VjcmV0" in zope_conf
        assert "cache-size 10GB" in zope_conf


def test_bake_with_z3blobs_no_bucket_fails(cookies):
    """z3blobs enabled without bucket_name should fail in pre-gen hook."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_z3blobs_enabled": "true",
            "db_z3blobs_cache_dir": "var/s3cache",
        },
    ) as result:
        assert result.exit_code != 0


def test_bake_with_z3blobs_no_cache_dir_fails(cookies):
    """z3blobs enabled without cache_dir should fail in pre-gen hook."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_z3blobs_enabled": "true",
            "db_z3blobs_bucket_name": "my-blobs",
        },
    ) as result:
        assert result.exit_code != 0


def test_bake_with_locale(cookies):
    """Setting locale should render in zope.conf."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "locale": "de_DE.UTF-8",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "locale de_DE.UTF-8" in zope_conf


def test_bake_without_locale(cookies):
    """Default bake should have no locale directive."""
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "locale " not in zope_conf


def test_bake_with_deprecated_db_blobs_location(cookies):
    """Deprecated db_blobs_location should still render in zope.conf."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_blobs_location": "/custom/blobs/path",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "blob-dir /custom/blobs/path" in zope_conf


def test_bake_with_deprecated_db_blobs_mode(cookies):
    """Deprecated db_blobs_mode should still render in zope.conf."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "relstorage",
            "db_blobs_mode": "cache",
            "db_relstorage_postgresql_dsn": "dbname=plone",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "shared-blob-dir false" in zope_conf


def test_bake_with_z3blobs_pgjsonb_fails(cookies):
    """z3blobs + pgjsonb should fail (pgjsonb handles blobs natively)."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "pgjsonb",
            "db_pgjsonb_dsn": "dbname=zodb",
            "db_z3blobs_enabled": "true",
            "db_z3blobs_bucket_name": "my-blobs",
            "db_z3blobs_cache_dir": "var/s3cache",
        },
    ) as result:
        assert result.exit_code != 0


# =============================================================================
# Bug fix tests
# =============================================================================


def test_bake_with_relstorage_oracle(cookies):
    """Oracle relstorage should render driver, user, password, dsn."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "relstorage",
            "db_relstorage": "oracle",
            "db_relstorage_oracle_user": "scott",
            "db_relstorage_oracle_password": "tiger",
            "db_relstorage_oracle_dsn": "orcl",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "<oracle>" in zope_conf
        assert "driver cx_Oracle" in zope_conf
        assert "user scott" in zope_conf
        assert "password tiger" in zope_conf
        assert "dsn orcl" in zope_conf


def test_bake_with_form_part_limit(cookies):
    """Default bake should include form-part-limit in dos_protection."""
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "form-part-limit 1024" in zope_conf


# =============================================================================
# Zope-level settings tests
# =============================================================================


def test_bake_with_trusted_proxy(cookies):
    """trusted_proxy should render multiple trusted-proxy lines."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "trusted_proxy": "10.0.0.1,10.0.0.2",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "trusted-proxy 10.0.0.1" in zope_conf
        assert "trusted-proxy 10.0.0.2" in zope_conf


def test_bake_without_trusted_proxy(cookies):
    """Default bake should have no trusted-proxy directive."""
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "trusted-proxy" not in zope_conf


def test_bake_with_product_config(cookies):
    """product_config dict should render <product-config> sections."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "product_config": {
                "my_addon": {"setting1": "value1", "setting2": "value2"},
            },
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "<product-config my_addon>" in zope_conf
        assert "setting1 value1" in zope_conf
        assert "setting2 value2" in zope_conf
        assert "</product-config>" in zope_conf


def test_bake_with_datetime_format(cookies):
    """datetime_format should render datetime-format directive."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "datetime_format": "international",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "datetime-format international" in zope_conf


# =============================================================================
# Database common settings tests
# =============================================================================


def test_bake_with_pool_timeout(cookies):
    """db_pool_timeout should render pool-timeout in zodb_db."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_pool_timeout": "600",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "pool-timeout 600" in zope_conf


# =============================================================================
# FileStorage settings tests
# =============================================================================


def test_bake_with_filestorage_create_false(cookies):
    """db_filestorage_create should render create directive."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_filestorage_create": "false",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "create false" in zope_conf


def test_bake_with_filestorage_read_only(cookies):
    """db_filestorage_read_only should render read-only directive."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_filestorage_read_only": "true",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "read-only true" in zope_conf


# =============================================================================
# RelStorage settings tests
# =============================================================================


def test_bake_with_relstorage_name(cookies):
    """db_relstorage_name should render name directive."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "relstorage",
            "db_relstorage_name": "main",
            "db_relstorage_postgresql_dsn": "dbname=plone",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "name main" in zope_conf


def test_bake_with_relstorage_pack_gc(cookies):
    """db_relstorage_pack_gc should render pack-gc directive."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "relstorage",
            "db_relstorage_pack_gc": "false",
            "db_relstorage_postgresql_dsn": "dbname=plone",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "pack-gc false" in zope_conf


# =============================================================================
# ZEO settings tests
# =============================================================================


def test_bake_with_zeo_client_label(cookies):
    """db_zeo_client_label should render client-label directive."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "zeo",
            "db_zeo_client_label": "web1",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "client-label web1" in zope_conf


def test_bake_with_zeo_storage(cookies):
    """db_zeo_storage should render storage directive."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "zeo",
            "db_zeo_storage": "main",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "storage main" in zope_conf


def test_bake_with_zeo_wait(cookies):
    """db_zeo_wait should render wait directive."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "zeo",
            "db_zeo_wait": "false",
        },
    ) as result:
        assert result.exit_code == 0
        zope_conf = (result.project_path / "etc" / "zope.conf").read_text()
        assert "wait false" in zope_conf


# =============================================================================
# Generic zodb-convert config tests
# =============================================================================


def test_bake_default_no_convert_files(cookies):
    """Default bake (filestorage) should NOT have convert-*.conf files."""
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0
        assert not (result.project_path / "etc" / "convert-import.conf").exists()
        assert not (result.project_path / "etc" / "convert-export.conf").exists()


def test_bake_pgjsonb_has_convert_files(cookies):
    """PGJsonb with db_convert_* settings should generate convert configs."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "pgjsonb",
            "db_pgjsonb_dsn": "dbname=zodb host=localhost port=5433",
            "db_convert_import_filestorage_location": "var/import/Data.fs",
            "db_convert_import_blobs_location": "var/import/blobs",
            "db_convert_export_filestorage_location": "var/export/Data.fs",
            "db_convert_export_blobs_location": "var/export/blobs",
        },
    ) as result:
        assert result.exit_code == 0

        import_conf = (result.project_path / "etc" / "convert-import.conf").read_text()
        assert "<filestorage source>" in import_conf
        assert "<pgjsonb destination>" in import_conf
        assert "</pgjsonb destination>" in import_conf
        assert "dsn dbname=zodb host=localhost port=5433" in import_conf

        export_conf = (result.project_path / "etc" / "convert-export.conf").read_text()
        assert "<pgjsonb source>" in export_conf
        assert "</pgjsonb source>" in export_conf
        assert "<filestorage destination>" in export_conf


def test_bake_relstorage_has_both_convert_and_legacy(cookies):
    """RelStorage should have BOTH old relstorage-*.conf AND new convert-*.conf."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "relstorage",
            "db_relstorage_postgresql_dsn": "dbname=plone",
            "db_relstorage_import_filestorage_location": "var/rs-import/Data.fs",
            "db_relstorage_import_blobs_location": "var/rs-import/blobs",
            "db_convert_import_filestorage_location": "var/import/Data.fs",
            "db_convert_import_blobs_location": "var/import/blobs",
            "db_convert_export_filestorage_location": "var/export/Data.fs",
            "db_convert_export_blobs_location": "var/export/blobs",
        },
    ) as result:
        assert result.exit_code == 0
        # Legacy relstorage files should exist
        assert (result.project_path / "etc" / "relstorage-import.conf").exists()
        assert (result.project_path / "etc" / "relstorage-pack.conf").exists()
        # New generic convert files should also exist
        import_conf = (result.project_path / "etc" / "convert-import.conf").read_text()
        assert "<relstorage destination>" in import_conf
        export_conf = (result.project_path / "etc" / "convert-export.conf").read_text()
        assert "<relstorage source>" in export_conf


def test_bake_zeo_has_convert_files(cookies):
    """ZEO with db_convert_* settings should generate convert configs."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "zeo",
            "db_convert_import_filestorage_location": "var/import/Data.fs",
            "db_convert_import_blobs_location": "var/import/blobs",
            "db_convert_export_filestorage_location": "var/export/Data.fs",
            "db_convert_export_blobs_location": "var/export/blobs",
        },
    ) as result:
        assert result.exit_code == 0

        import_conf = (result.project_path / "etc" / "convert-import.conf").read_text()
        assert "<filestorage source>" in import_conf
        assert "<zeoclient destination>" in import_conf
        assert "</zeoclient destination>" in import_conf

        export_conf = (result.project_path / "etc" / "convert-export.conf").read_text()
        assert "<zeoclient source>" in export_conf
        assert "</zeoclient source>" in export_conf
        assert "<filestorage destination>" in export_conf


def test_bake_pgjsonb_no_convert_settings(cookies):
    """PGJsonb without db_convert_* settings should have fallback comment."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "db_storage": "pgjsonb",
            "db_pgjsonb_dsn": "dbname=zodb",
        },
    ) as result:
        assert result.exit_code == 0
        # Files should exist but with the "missing settings" fallback
        import_conf = (result.project_path / "etc" / "convert-import.conf").read_text()
        assert "Missing db_convert_import_*" in import_conf
        assert "<pgjsonb" not in import_conf


# =============================================================================
# WSGI settings tests
# =============================================================================


def test_bake_with_wsgi_channel_timeout(cookies):
    """wsgi_channel_timeout should render channel_timeout in zope.ini."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "wsgi_channel_timeout": "60",
        },
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "channel_timeout = 60" in zope_ini
