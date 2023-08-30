import yaml

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader  # type: ignore  # noqa: F401


def load_yaml_from_text(contents):
    try:
        return yaml.load(contents, Loader=SafeLoader)
    except (yaml.scanner.ScannerError, yaml.YAMLError) as e:
        error = str(e)

        raise ValueError(error)
