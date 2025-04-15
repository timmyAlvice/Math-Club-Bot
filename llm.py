import os, asyncio
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from openai import OpenAI
from pathlib import Path
from sentence_transformers import SentenceTransformer
from utils import SYS_PROMPT

DEEP_SEEK_TOKEN = os.getenv("DEEP_SEEK_TOKEN")

class LLM:

    def __init__(
        self,
        context_file: str = "retriever_test.txt",
        persist_dir: str = "knowlage_base",
        rewrite_knwolage_base: bool = False
    ):

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=DEEP_SEEK_TOKEN,
        )

        self.embedder = SentenceTransformer(
            'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'
        )

        self.persist_dir = Path(persist_dir)
        self.index_path = self.persist_dir / "faiss_index"

        if not self.load_vector_store() or rewrite_knwolage_base:
            print("Making new knowlage base...")
            self._create_vector_store(context_file)
            self.save_vector_store()

    def _create_vector_store(self, context_file):
        try:
            loader = TextLoader(context_file)
            documents = loader.load()

            print("TEXT SPLITTING BY CHUNKS")
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = text_splitter.split_documents(documents)
            texts = [doc.page_content for doc in chunks]

            print("COMPUTING EMBEDDINGS")
            embeddings = self.embedder.encode(texts)

            print("BUILDING GRAPH")
            self.vector_store = FAISS.from_embeddings(
                text_embeddings=zip(texts, embeddings),
                embedding=self.embedder
            )
        except Exception as e:
            raise RuntimeError(f"Ошибка создания базы знаний: {str(e)}")

    def load_vector_store(self) -> bool:
        try:
            if not (self.index_path / "index.faiss").exists():
                return False

            print(f"Loading knowlage base from {self.index_path}")
            self.vector_store = FAISS.load_local(
                folder_path=str(self.index_path),
                embeddings=self.embedder,
                allow_dangerous_deserialization=True
            )
            return True
        except Exception as e:
            print(f"Ошибка загрузки базы: {str(e)}")
            return False

    def save_vector_store(self):
        try:
            self.persist_dir.mkdir(parents=True, exist_ok=True)
            self.vector_store.save_local(str(self.index_path))
            print(f"База знаний сохранена в {self.index_path}")
        except Exception as e:
            raise RuntimeError(f"Ошибка сохранения базы: {str(e)}")

    async def generate_text(self, prompt: str, k=3) -> str:
        prompt_embedding = self.embedder.encode(prompt)
        retrieved_docs = self.vector_store.similarity_search_by_vector(
            prompt_embedding, k=k
        )

        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        augmented_prompt = f"""Контекстная информация:
{context}

Вопрос: {prompt}
"""

        completion = self.client.chat.completions.create(
            model="deepseek/deepseek-r1-distill-llama-70b:free",
            messages=[
                {"role": "system", "content": SYS_PROMPT},
                {"role": "user", "content": augmented_prompt}
            ],
            temperature=0.3,
            top_p=0.95
        )

        return completion.choices[0].message.content

llm = LLM()