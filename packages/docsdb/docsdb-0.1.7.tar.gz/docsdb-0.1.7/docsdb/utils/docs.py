import os
import yaml
from docsdb.utils.system import load_file_contents_as_string
from docsdb.utils.yaml_utils import load_yaml_from_text


def create_docs_folder_structure(node, docs_path="docs"):
    if not os.path.exists(docs_path):
        os.mkdir(docs_path)

    for cluster, dbs in node.items():
        if cluster in {"meta", "started_at", "ended_at"}:
            continue
        cluster_path = os.path.join(docs_path, cluster)
        if not os.path.exists(cluster_path):
            os.mkdir(cluster_path)

        for dbName, db in dbs.items():
            db_path = os.path.join(cluster_path, dbName)
            if not os.path.exists(db_path):
                os.mkdir(db_path)

            db_yml_file = os.path.join(db_path, f"{dbName}.yml")
            if not os.path.exists(db_yml_file):
                model = f"{cluster}${dbName}"
                model_dict = {"model": model, "depends_on": None, "doc": None}
                with open(db_yml_file, "w") as outfile:
                    yaml.dump(model_dict, outfile, default_flow_style=False)

            collection_path = os.path.join(db_path, "collections")
            if not os.path.exists(collection_path):
                os.mkdir(collection_path)

            for collection in db.get("collections", []):
                file_name = f"{collection}.yml"
                # $ is an invalid character. so it's safe to use as a separator
                model = f"{cluster}${dbName}${collection}"
                model_dict = {"model": model, "depends_on": None, "doc": None}
                collection_yml_file = os.path.join(collection_path, file_name)
                if not os.path.exists(collection_yml_file):
                    with open(collection_yml_file, "w") as outfile:
                        yaml.dump(model_dict, outfile, default_flow_style=False)


def docs_yaml_to_json(docs_path="docs"):
    docs_metadata = {}
    if not os.path.exists(docs_path):
        return docs_metadata
    for cluster in os.listdir(docs_path):
        cluster_path = os.path.join(docs_path, cluster)
        if os.path.exists(cluster_path) and os.path.isdir(cluster_path):
            docs_metadata[cluster] = {}
            for dbName in os.listdir(cluster_path):
                db_path = os.path.join(cluster_path, dbName)
                db_yml_file = os.path.join(db_path, f"{dbName}.yml")
                if not os.path.exists(db_yml_file):
                    continue
                contents = load_file_contents_as_string(db_yml_file, strip=False)
                db_docs = load_yaml_from_text(contents)
                docs_metadata[cluster][dbName] = {}
                docs_metadata[cluster][dbName]["db"] = db_docs
                docs_metadata[cluster][dbName]["collections"] = {}
                if os.path.exists(db_path) and os.path.isdir(db_path):
                    collection_path = os.path.join(db_path, "collections")
                    if not os.path.exists(collection_path):
                        continue
                    for collection_yml in os.listdir(collection_path):
                        arr = collection_yml.split(".")
                        if len(arr) <= 1:
                            continue
                        collection, file_ext = ".".join(arr[0:-1]), arr[-1]
                        if file_ext not in {"yml"}:
                            continue
                        collection_yml_file = os.path.join(
                            collection_path, collection_yml
                        )
                        if not os.path.exists(collection_yml_file):
                            continue
                        contents = load_file_contents_as_string(
                            collection_yml_file, strip=False
                        )
                        collection_docs = load_yaml_from_text(contents)
                        docs_metadata[cluster][dbName]["collections"][
                            collection
                        ] = collection_docs
    return docs_metadata
