from langchain_community.embeddings import

embeddings = BedrockEmbeddings(
    credentials_profile_name="default", region_name="us-east-1"
)

print(embeddings("Hi testing."))
