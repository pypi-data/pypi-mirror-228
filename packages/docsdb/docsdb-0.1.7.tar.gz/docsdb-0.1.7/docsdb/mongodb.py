import click
from typing import Tuple
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from urllib.parse import urlparse
from bson.son import SON
from datetime import datetime
from bson import json_util
import os
import shutil
from docsdb.utils.docs import create_docs_folder_structure, docs_yaml_to_json
from docsdb.include import DOCUMENTATION_INDEX_FILE_PATH

# irrelevant for docs generation
COLLECTION_STAT_ENTRIES_TO_REMOVE = [
    "wiredTiger",
    "indexDetails",
    "LSM",
    "block-manager",
    "btree",
    "cache",
    "cache_walk",
    "compression",
    "cursor",
    "reconciliation",
    "session",
    "transaction",
]

COLLECTIONS_TO_EXLUDE = {"system.views"}
DATABASES_TO_EXCLUDE = {"admin", "local", "config"}
COLLECTION_SAMPLE_SIZE = 2
RECENT_DOCUMENTS_TO_SELECT = 10
DB_STATS_KEY = "db_stats"
COLLECTIONS_KEY = "collections"
STARTED_AT_KEY = "started_at"
ENDED_AT_KEY = "ended_at"
META_KEY = "meta"
TARGET_DIR = "target"
CURRENT_DIR = os.getcwd()
OUTPUT_FILE_NAME = "metadata"
DOCS_OUTPUT_FILE_NAME = "docs_metadata"


def get_database_info(db: Database):
    db_stats = db.command(command=SON([("dbStats", None)]))
    return db_stats


def get_collection_info(coll: Collection, collection_info: dict):
    collection_type = collection_info["type"]
    info = dict()
    index_info = coll.index_information() if collection_type == "collection" else {}
    collection_stats = (
        coll.database.command(command=SON([("collStats", coll.name)]))
        if collection_type == "collection"
        else {}
    )
    info["collection_stats"] = collection_stats
    for key in COLLECTION_STAT_ENTRIES_TO_REMOVE:
        info["collection_stats"].pop(key, None)

    pipeline = [
        {"$limit": RECENT_DOCUMENTS_TO_SELECT},
        {"$sample": {"size": COLLECTION_SAMPLE_SIZE}},
    ]
    hint = {"$natural": -1}
    sampled_documents = list(
        coll.aggregate(
            pipeline=pipeline,
            hint=hint,
        )
    )
    info["index_information"] = index_info
    info["sampled_documents"] = sampled_documents
    info["collection_info"] = collection_info

    return info


@click.command()
@click.option(
    "--mongo-uri",
    multiple=True,
    help="""
        Specifies the resolvable URI connection string of the MongoDB deployments.
        Pass multiple URIs to generate documentations for multiple clusters
    """,
)
def mongodb(mongo_uri: Tuple[str]):
    metadata = {}
    metadata[META_KEY] = {}
    metadata[META_KEY][STARTED_AT_KEY] = datetime.utcnow()
    for uri in mongo_uri:
        client = MongoClient(uri)
        host = urlparse(uri).hostname
        click.echo(f"host={host}")
        metadata[host] = {}
        for database_name in client.list_database_names():
            if database_name in DATABASES_TO_EXCLUDE:
                click.echo(f"\t skipping database: {database_name}")
                continue
            click.echo(f"\t database_name={database_name}")
            db = client[database_name]
            db_stats = get_database_info(db=db)
            metadata[host][database_name] = {}
            metadata[host][database_name][DB_STATS_KEY] = db_stats
            metadata[host][database_name][COLLECTIONS_KEY] = {}
            for collection_info in db.list_collections():
                collection_name = collection_info["name"]
                if collection_name in COLLECTIONS_TO_EXLUDE:
                    click.echo(f"\t\t skipping collection: {collection_name}")
                    continue
                click.echo(f"\t\t collection_name={collection_name}")
                coll = db[collection_name]
                collection_info = get_collection_info(
                    coll=coll, collection_info=collection_info
                )
                metadata[host][database_name][COLLECTIONS_KEY][
                    collection_name
                ] = collection_info

    metadata[META_KEY][ENDED_AT_KEY] = datetime.utcnow()
    metadata_json = json_util.dumps(metadata)

    target_dir = os.path.join(CURRENT_DIR, TARGET_DIR)

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    target_file_path = os.path.join(target_dir, "index.html")
    shutil.copyfile(DOCUMENTATION_INDEX_FILE_PATH, target_file_path)

    with open(f"{CURRENT_DIR}/{TARGET_DIR}/{OUTPUT_FILE_NAME}.json", "w") as text_file:
        text_file.write(metadata_json)

    create_docs_folder_structure(metadata, docs_path="docs")

    docs_metadata = docs_yaml_to_json(docs_path="docs")
    docs_metadata_json = json_util.dumps(docs_metadata)

    with open(
        f"{CURRENT_DIR}/{TARGET_DIR}/{DOCS_OUTPUT_FILE_NAME}.json", "w"
    ) as text_file:
        text_file.write(docs_metadata_json)

    click.echo(f"export complete!")
