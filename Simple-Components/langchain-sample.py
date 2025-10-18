from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.parsers import RapidOCRBlobParser


loader = PyPDFLoader(
    "data/monopoly.pdf",
    mode="page",
)

print(loader.load())
