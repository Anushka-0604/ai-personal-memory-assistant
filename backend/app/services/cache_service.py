import hashlib


class CacheService:

    def __init__(self):
        self.embedding_cache = {}
        self.search_cache = {}
        self.prompt_cache = {}

    def _key(self, text: str) -> str:
        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

    def get_embedding(self, text: str):
        return self.embedding_cache.get(
            self._key(text)
        )

    def set_embedding(
        self,
        text: str,
        embedding,
    ):
        self.embedding_cache[
            self._key(text)
        ] = embedding

    def get_search(self, query: str):
        return self.search_cache.get(
            self._key(query)
        )

    def set_search(
        self,
        query: str,
        results,
    ):
        self.search_cache[
            self._key(query)
        ] = results

    def get_prompt(self, prompt: str):
        return self.prompt_cache.get(
            self._key(prompt)
        )

    def set_prompt(
        self,
        prompt: str,
        response,
    ):
        self.prompt_cache[
            self._key(prompt)
        ] = response


cache_service = CacheService()