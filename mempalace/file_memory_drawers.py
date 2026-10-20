"""File MEMORY.md once per hall. Skip a section whose text is already kept."""
import os
import re
import sys

os.environ["MEMPALACE_PALACE_PATH"] = r"C:\Users\trngs\.cursor\mempalace\palace"

from mempalace.miner import _build_drawer_metadata, make_drawer_id_from_chunk
from mempalace.palace import get_collection

WORKSPACE = r"c:\Users\trngs\Desktop\tarangnsharma\MEMORY.md"
GLOBAL = r"C:\Users\trngs\.cursor\MEMORY.md"


def split_sections(text: str) -> dict:
    parts = re.split(r"\n(?=## )", text.strip())
    sections = {"Standing preferences": parts[0].strip()}
    for part in parts[1:]:
        heading = part.splitlines()[0][3:].strip()
        sections[heading] = part.strip()
    return sections


def episodic_line(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("- **Episodic memory.**"):
            return line
    raise SystemExit("episodic memory line missing")


def main():
    workspace_text = open(WORKSPACE, encoding="utf-8").read()
    global_text = open(GLOBAL, encoding="utf-8").read()
    workspace = split_sections(workspace_text)
    global_md = split_sections(global_text)

    # One original section each. The other file's copy is the overlap.
    drawers = [
        (
            "wing_global",
            "preferences",
            "hall_preferences",
            GLOBAL,
            [
                global_md["Standing preferences"],
                workspace["Spoken pace"],
                global_md["Check memory first"],
                workspace["Do not ask Tarang to start over"],
                workspace["Dynamic memory"],
                global_md["Links to files and folders"],
                global_md["Keep quiet"],
                workspace["Infographic style"],
                global_md["Voice calls: links and volume"],
            ],
        ),
        (
            "wing_global",
            "voice-pipeline",
            "hall_advice",
            GLOBAL,
            [
                global_md["Voice prompt pipeline"],
                global_md["Token efficiency"],
                global_md["Git commit discipline"],
            ],
        ),
        (
            "wing_tarangnsharma",
            "memory",
            "hall_facts",
            WORKSPACE,
            [
                workspace["Table of contents"],
                global_md["Lessons"],
                global_md["Act immediately"],
            ],
        ),
        (
            "wing_tarangnsharma",
            "memory",
            "hall_events",
            WORKSPACE,
            [episodic_line(workspace_text)],
        ),
        (
            "wing_tarangnsharma",
            "infographics",
            "hall_discoveries",
            WORKSPACE,
            [global_md["Infographic visual QA"]],
        ),
    ]

    collection = get_collection(os.environ["MEMPALACE_PALACE_PATH"], create=True)
    existing = collection.get(include=[])
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    ids = []
    documents = []
    metadatas = []
    chunk_for = {}
    for wing, room, hall, source, parts in drawers:
        content = "\n\n".join(parts)
        key = (wing, room, source)
        chunk_index = chunk_for.get(key, 0)
        chunk_for[key] = chunk_index + 1
        drawer_id = make_drawer_id_from_chunk(wing, room, source, chunk_index)
        try:
            source_mtime = os.path.getmtime(source)
        except OSError:
            source_mtime = None
        metadata = _build_drawer_metadata(
            wing, room, source, chunk_index, "tarang-memory-file", content, source_mtime
        )
        metadata["hall"] = hall
        ids.append(drawer_id)
        documents.append(content)
        metadatas.append(metadata)

    collection.upsert(documents=documents, ids=ids, metadatas=metadatas)

    got = collection.get(include=["documents", "metadatas"])
    by_id = {item_id: (doc, meta) for item_id, doc, meta in zip(got["ids"], got["documents"], got["metadatas"])}
    if len(by_id) != 5:
        print(f"expected 5 drawers, found {len(by_id)}")
        return 1
    halls = []
    for drawer_id, content, meta in zip(ids, documents, metadatas):
        stored, stored_meta = by_id[drawer_id]
        if stored != content or stored_meta.get("hall") != meta["hall"]:
            print("mismatch", drawer_id)
            return 1
        halls.append(stored_meta["hall"])
        print(f"{stored_meta['wing']}\t{stored_meta['room']}\t{stored_meta['hall']}\t{len(stored)}")
    if len(set(halls)) != 5:
        print("a hall was written more than once", halls)
        return 1
    print("ok", collection.count())
    return 0


if __name__ == "__main__":
    sys.exit(main())
