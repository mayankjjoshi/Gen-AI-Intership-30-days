import chromadb

client = chromadb.Client()

collection = client.create_collection(name="doc_genai")

documents = ['PRELYTIX PVT LTD - EMPLOYEE POLICY SUMMARY Company Location: Bakrol, Anand, Gujarat', 

'1. Working HoursEmployees are expected to follow the working hours communicated by the company and maintain regular attendance.2. Leave PolicyEmployees should request leave in advance whenever possible. Emergency or sick leave should be communicated to the reporting manager as soon as possible.',

'5. Company Assets Company laptops, accounts, software, documents, and other assets must be used responsibly and returned when requested or when employment ends. 6. Data SecurityEmployees must protect passwords and credentials and must not provide unauthorized access to company systems or client information.7. Work Quality Employees are expected to complete assigned work responsibly, communicate project progress, and meet agreed deadlines. 8. Resignation Employees who resign must follow the applicable notice period and complete proper handover of assigned work, documents, credentials, and company assets.Note:This is a sample document created for RAG/vector database testing. It is not an official Prelytix Pvt Ltd employee policy and should not be treated as an HR or legal document.']

collection.add(
    ids=["1","2","3"],
    documents=documents
)

result = collection.query(
    query_texts=["What does the policy say about confidential information?"],
    n_results=4
)

print(result)
