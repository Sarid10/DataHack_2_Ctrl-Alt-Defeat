import pinecone, os   

pinecone.init(      
	api_key="51a4ed09-15b8-4222-8e46-e9d5a67c78fa",      
	environment='gcp-starter'      
)      
index = pinecone.Index('lawyer-info')

def insert(name, vector):
  index.upsert([
    
    (name, vector)

  ])

def get(vector):
  return index.query(
    vector=[vector],
    top_k=3,
    include_values=True
    )
  

# insert("Anay Ahluwalia", [0.45547258853912354])
# print(get([0.8994727969169617]))