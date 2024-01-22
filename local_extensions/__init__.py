from jinja2.ext import Extension
from jinja2.ext import pass_context
from pathlib import Path


class AbsPathExtension(Extension):
    def __init__(self, environment):
        super(AbsPathExtension, self).__init__(environment)
        environment.filters["abspath"] = AbsPathExtension.abspath

    @pass_context
    def abspath(context, path, append_path=""):
        try:
            _context_cookiecutter = context.get("cookiecutter")
            if _context_cookiecutter:
                _output_dir = _context_cookiecutter.get("_output_dir")
                if _output_dir:
                    new_path = Path(_output_dir, path, append_path).resolve().as_posix()
                else:
                    raise ValueError("No _output_dir in cookiecutter context")
            else:
                raise ValueError("No cookiecutter context")
        except Exception as e:
            raise Exception(f"Failed to filter {context.name}") from e

        return f"{new_path}"
