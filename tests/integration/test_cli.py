import json

import pytest

from proteus.cli import main


class TestCLI:
    """Integration tests for the Proteus Command Line Interface."""

    def test_cli_help(self, capsys):
        """'proteus --help' prints usage information and exits 0."""
        with pytest.raises(SystemExit) as exc:
            main(["--help"])

        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert "Available commands" in captured.out
        assert "get" in captured.out
        assert "set" in captured.out

    def test_cli_get(self, tmp_path, capsys):
        """'proteus get <file> <key>' prints the value to stdout."""
        config_file = tmp_path / "app.json"
        config_file.write_text(json.dumps({"database": {"port": 5432}}))

        with pytest.raises(SystemExit) as exc:
            main(["get", str(config_file), "database.port"])

        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert captured.out.strip() == "5432"

    def test_cli_get_cast(self, tmp_path, capsys):
        """'proteus get' supports type casting."""
        config_file = tmp_path / "app.env"
        config_file.write_text("DEBUG=true\n")

        with pytest.raises(SystemExit) as exc:
            main(["get", str(config_file), "DEBUG", "--cast", "bool"])

        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert captured.out.strip() == "True"  # Python's str(True)

    def test_cli_set(self, tmp_path, capsys):
        """'proteus set <file> <key> <value>' updates the file."""
        config_file = tmp_path / "settings.yaml"
        config_file.write_text("app: old\n")

        with pytest.raises(SystemExit) as exc:
            main(["set", str(config_file), "app", "new"])

        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert "Successfully updated" in captured.out
        assert "app: new" in config_file.read_text()

    def test_cli_set_out(self, tmp_path):
        """'proteus set' can save to a different output file."""
        src = tmp_path / "in.json"
        src.write_text('{"v": 1}')
        dst = tmp_path / "out.json"

        with pytest.raises(SystemExit) as exc:
            main(["set", str(src), "v", "2", "--out", str(dst)])

        assert exc.value.code == 0
        assert json.loads(dst.read_text()) == {"v": "2"}
        assert json.loads(src.read_text()) == {"v": 1}  # original unchanged

    def test_cli_merge(self, tmp_path):
        """'proteus merge <files> --out <dest>' combines configurations."""
        f1 = tmp_path / "base.json"
        f1.write_text('{"a": 1}')
        f2 = tmp_path / "override.yaml"
        f2.write_text("b: 2\n")
        out = tmp_path / "final.toml"

        with pytest.raises(SystemExit) as exc:
            main(["merge", str(f1), str(f2), "--out", str(out)])

        assert exc.value.code == 0
        # Verify content (reading back via Proteus logic is easiest)
        content = out.read_text()
        assert "a = 1" in content
        assert "b = 2" in content

    def test_cli_translate(self, tmp_path):
        """'proteus translate <in> <out>' converts formats."""
        src = tmp_path / "app.env"
        src.write_text("PORT=80\n")
        dst = tmp_path / "app.json"

        with pytest.raises(SystemExit) as exc:
            main(["translate", str(src), str(dst)])

        assert exc.value.code == 0
        assert json.loads(dst.read_text()) == {"PORT": "80"}

    def test_cli_view(self, tmp_path, capsys):
        """'proteus view <files>' prints the merged JSON config."""
        f1 = tmp_path / "base.json"
        f1.write_text('{"a": 1}')
        f2 = tmp_path / "extra.json"
        f2.write_text('{"b": 2}')

        with pytest.raises(SystemExit) as exc:
            main(["view", str(f1), str(f2)])

        assert exc.value.code == 0
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data == {"a": 1, "b": 2}

    def test_cli_view_empty(self, capsys):
        """'proteus view' with no files prints an empty JSON object."""
        with pytest.raises(SystemExit) as exc:
            main(["view"])
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert json.loads(captured.out) == {}

    def test_cli_list_files(self, tmp_path, capsys):
        """'proteus list-files <files>' prints absolute paths."""
        f1 = tmp_path / "a.json"
        f1.write_text("{}")

        with pytest.raises(SystemExit) as exc:
            main(["list-files", str(f1)])

        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert str(f1.resolve()) in captured.out

    def test_cli_set_no_out(self, tmp_path):
        """'proteus set' defaults to overwriting the input file."""
        f = tmp_path / "config.json"
        f.write_text('{"v": 1}')
        with pytest.raises(SystemExit) as exc:
            main(["set", str(f), "v", "2"])
        assert exc.value.code == 0
        assert json.loads(f.read_text()) == {"v": "2"}

    def test_cli_list_files_multiple(self, tmp_path, capsys):
        """'proteus list-files' can load and list multiple files."""
        f1 = tmp_path / "1.json"
        f1.write_text("{}")
        f2 = tmp_path / "2.yaml"
        f2.write_text("a: b")

        with pytest.raises(SystemExit) as exc:
            main(["list-files", str(f1), str(f2)])

        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert str(f1.resolve()) in captured.out
        assert str(f2.resolve()) in captured.out

    def test_cli_translate_file_not_found(self, capsys):
        """'proteus translate' handles missing files."""
        with pytest.raises(SystemExit) as exc:
            main(["translate", "missing.json", "out.yaml"])
        assert exc.value.code == 1
        assert "Error: File not found: missing.json" in capsys.readouterr().err

    def test_cli_get_no_cast(self, tmp_path, capsys):
        """'proteus get' works without --cast."""
        f = tmp_path / "t.json"
        f.write_text('{"a": 1}')
        with pytest.raises(SystemExit) as exc:
            main(["get", str(f), "a"])
        assert exc.value.code == 0
        assert capsys.readouterr().out.strip() == "1"

    def test_cli_error_returns_exit_1(self, tmp_path, capsys):
        """CLI returns exit code 1 and prints to stderr on failure."""
        with pytest.raises(SystemExit) as exc:
            main(["get", "nonexistent.json", "key"])

        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_cli_get_cast_int(self, tmp_path, capsys):
        """'proteus get' supports integer casting."""
        f = tmp_path / "app.json"
        f.write_text('{"port": "8080"}')
        with pytest.raises(SystemExit) as exc:
            main(["get", str(f), "port", "--cast", "int"])
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert captured.out.strip() == "8080"

    def test_cli_get_cast_float(self, tmp_path, capsys):
        """'proteus get' supports float casting."""
        f = tmp_path / "app.json"
        f.write_text('{"pi": "3.14"}')
        with pytest.raises(SystemExit) as exc:
            main(["get", str(f), "pi", "--cast", "float"])
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert captured.out.strip() == "3.14"

    def test_cli_value_error_handling(self, tmp_path, capsys):
        """CLI handles ValueError (e.g. malformed JSON) cleanly."""
        f = tmp_path / "bad.json"
        f.write_text("{invalid")
        with pytest.raises(SystemExit) as exc:
            main(["get", str(f), "key"])
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_cli_unexpected_error_handling(self, monkeypatch, capsys):
        """CLI handles unexpected exceptions cleanly."""
        from proteus.core import ConfigurationManager

        def mock_load(*args, **kwargs):
            raise RuntimeError("Boom")

        monkeypatch.setattr(ConfigurationManager, "load", mock_load)

        with pytest.raises(SystemExit) as exc:
            main(["get", "any.json", "key"])

        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "Unexpected error: Boom" in captured.err

    def test_cli_no_command_prints_help(self, capsys):
        """Running proteus with no command prints help and exits 0."""
        with pytest.raises(SystemExit) as exc:
            main([])
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert "Available commands" in captured.out

    def test_cli_invalid_key_error(self, tmp_path, capsys):
        """Malformed keys trigger a clean error message."""
        f = tmp_path / "t.json"
        f.write_text("{}")

        with pytest.raises(SystemExit) as exc:
            main(["get", str(f), "key..path"])

        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "Error: Key 'key..path' is not valid" in captured.err
