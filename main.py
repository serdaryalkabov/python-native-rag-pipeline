from openai import OpenAI
from anthropic import Anthropic
import chromadb
from pypdf import PdfReader

anth_client = Anthropic(timeout = 60.0)
openai_client = OpenAI(timeout = 60.0)
chroma_client = chromadb.Client()

def get_embedding(text):
	response = openai_client.embeddings.create(
			model = 'text-embedding-3-small',
			input = text
		)

	return response.data[0].embedding

def chunk_text(text, size = 500, overlap = 100):
	chunks = []
	start = 0
	while start < len(text):
		end = start+size
		chunks.append(text[start:end])
		start = end-overlap

	return chunks


def extract_text_organize(path):
	reader = PdfReader(path)
	pages = []
	for page_num, page in enumerate(reader.pages):
		pages.append({
				'page_num': page_num+1,
				'content': page.extract_text()
			})

	return pages

path = 'linearalgebra.pdf'

collection = chroma_client.get_or_create_collection('pdfbaase')

chunk_id = 0

pages = extract_text_organize(path)

for page in pages:
	chunks = chunk_text(page['content'])
	for chunk in chunks:
		if (len(chunk.strip()) < 50):
			continue
		collection.add(
			documents = [chunk],
			embeddings = [get_embedding(chunk)],
			metadatas = [{
				'page_num': page['page_num'],
				'source': path
			}],
			ids = [f'chunk_{chunk_id}']
			)
		chunk_id+=1

def ask_question(question):
	query_embedding = get_embedding(question)
	results = collection.query(
			query_embeddings = [query_embedding],
			n_results = 3
		)
	context_parts = []

	for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
		context_parts.append(f"PAGE: {metadata['page_num']}\nCONTENT: {doc}")

	context = '\n\n\n'.join(context_parts)

	prompt = f"""
	BASED ON THE FOLLOWING EXCERPTS FROM THE DOCUMENTS:

	{context}

	ANSWER THIS QUESTION: {question}
	"""

	response = anth_client.messages.create(
			model = 'claude-haiku-4-5',
			max_tokens = 200,
			messages = [{'role': 'user', 'content': prompt}]
		)

	return response.content[0].text

question = 'How to multiply matrices?'
answer = ask_question(question)
print(f"QUESTION: {question}")
print(f"ANSWER: {answer}")