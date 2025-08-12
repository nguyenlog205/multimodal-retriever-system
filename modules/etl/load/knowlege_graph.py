from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL
from rdflib.namespace import XSD

def init_graph(namespace: str = "http://example.org/multimedia#"):
    g = Graph()
    ns = Namespace(namespace)
    g.bind("ex", ns)
    return g, ns

def declare_base_ontology(g: Graph, ns: Namespace):
    # basic classes
    g.add((ns.MultimediaFile, RDF.type, OWL.Class))
    for cls in ["Image", "Video", "Audio", "TextFile", "Thumbnail", "FeatureVector"]:
        g.add((getattr(ns, cls), RDF.type, OWL.Class))

    # basic datatype properties (a minimal set)
    props = [
        "hasFileURI", "hasFileName", "hasFormat", "hasSizeBytes", "hasWidth", "hasHeight",
        "hasDurationSeconds", "hasFrameRate", "hasSampleRate", "hasChannels", "hasCaption",
        "hasFeatureID", "hasThumbURI"
    ]
    for p in props:
        g.add((getattr(ns, p), RDF.type, OWL.DatatypeProperty))


def create_kg_entry(g: Graph, ns: Namespace, entity_id: str, kind: str, metadata: dict):
    subj = ns[entity_id]
    kind_map = {"image": ns.Image, "video": ns.Video, "audio": ns.Audio, "text": ns.TextFile}
    g.add((subj, RDF.type, kind_map.get(kind, ns.MultimediaFile)))

    def add(pname, value, dtype=XSD.string):
        if value is None:
            return
        g.add((subj, getattr(ns, pname), Literal(value, datatype=dtype)))

    add("hasFileURI", metadata.get("file_path"), XSD.anyURI)
    add("hasFileName", metadata.get("file_name"), XSD.string)
    add("hasFormat", metadata.get("format"), XSD.string)
    if metadata.get("size") is not None:
        add("hasSizeBytes", int(metadata.get("size")), XSD.integer)
    if metadata.get("width") is not None:
        add("hasWidth", int(metadata.get("width")), XSD.integer)
    if metadata.get("height") is not None:
        add("hasHeight", int(metadata.get("height")), XSD.integer)
    if metadata.get("duration") is not None:
        add("hasDurationSeconds", float(metadata.get("duration")), XSD.decimal)
    if metadata.get("framerate") is not None:
        add("hasFrameRate", float(metadata.get("framerate")), XSD.decimal)
    if metadata.get("sample_rate") is not None:
        add("hasSampleRate", int(metadata.get("sample_rate")), XSD.integer)
    if metadata.get("channels") is not None:
        add("hasChannels", int(metadata.get("channels")), XSD.integer)
    if metadata.get("caption") is not None:
        add("hasCaption", metadata.get("caption"), XSD.string)
    if metadata.get("feature_id") is not None:
        add("hasFeatureID", metadata.get("feature_id"), XSD.string)
    if metadata.get("thumb_path") is not None:
        add("hasThumbURI", metadata.get("thumb_path"), XSD.anyURI)


def save_kg(g: Graph, path):
    g.serialize(destination=str(path), format="turtle")

if __name__ == "__main__":
    graph, namespace = init_graph()
    declare_base_ontology(graph, namespace)
    # Add multimedia entries
    # "hasFileURI", "hasFileName", "hasFormat", "hasSizeBytes", "hasWidth", "hasHeight",
    # "hasDurationSeconds", "hasFrameRate", "hasSampleRate", "hasChannels", "hasCaption",
    # "hasFeatureID", "hasThumbURI"
    create_kg_entry(graph, namespace, "example_image_1", "image", {
        "file_path": "http://example.org/files/image1.jpg",
        "file_name": "image1.jpg",
        "format": "JPEG",
        "size": 204800,
        "width": 1920,
        "height": 1080,
        "caption": "An example image"
    })
    save_kg(graph, "modules/etl/load/multimedia_kg.owl")