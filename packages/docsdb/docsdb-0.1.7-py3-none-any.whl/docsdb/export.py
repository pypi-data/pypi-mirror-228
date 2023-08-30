import os
import shutil
import click
from docsdb.mongodb import CURRENT_DIR, TARGET_DIR, DOCS_OUTPUT_FILE_NAME
from docsdb.include import DOCUMENTATION_INDEX_FILE_PATH
from docsdb.utils.docs import docs_yaml_to_json
from bson import json_util


@click.command()
def export():
    """
    This helps export the static index.html required to run.
    Useful in cases when you want have the target/ folder generated with index.html
    So you can copy your artefacts {metadata.json, docs.json} manually
    """
    target_dir = os.path.join(CURRENT_DIR, TARGET_DIR)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    target_file_path = os.path.join(target_dir, "index.html")
    shutil.copyfile(DOCUMENTATION_INDEX_FILE_PATH, target_file_path)

    # if metadata exists, generate documentation
    docs_metadata = docs_yaml_to_json(docs_path="docs")
    docs_metadata_json = json_util.dumps(docs_metadata)

    with open(
        f"{CURRENT_DIR}/{TARGET_DIR}/{DOCS_OUTPUT_FILE_NAME}.json", "w"
    ) as text_file:
        text_file.write(docs_metadata_json)

    click.echo("target/ folder created with the index.html")
    click.echo(
        'copy your artefact {metadata.json} and run "docsdb serve" to view your documentation!'
    )
