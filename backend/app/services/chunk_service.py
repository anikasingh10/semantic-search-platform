import re


def sentence_split(text: str) -> list[str]:
    normalized = re.sub(r'\s+', ' ', text).strip()
    if not normalized:
        return []
    return re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])', normalized)


def chunk_text(text: str, chunk_size_words: int, overlap_words: int) -> list[str]:
    sentences = sentence_split(text)
    if not sentences:
        return []

    chunks: list[str] = []
    current_sentences: list[str] = []
    current_word_count = 0

    for sentence in sentences:
        sentence_words = sentence.split()
        sentence_len = len(sentence_words)

        if current_word_count + sentence_len > chunk_size_words and current_sentences:
            chunks.append(' '.join(current_sentences).strip())

            if overlap_words > 0:
                overlap_acc: list[str] = []
                overlap_count = 0
                for prev_sentence in reversed(current_sentences):
                    prev_words = prev_sentence.split()
                    overlap_acc.insert(0, prev_sentence)
                    overlap_count += len(prev_words)
                    if overlap_count >= overlap_words:
                        break
                current_sentences = overlap_acc
                current_word_count = sum(len(s.split()) for s in current_sentences)
            else:
                current_sentences = []
                current_word_count = 0

        current_sentences.append(sentence)
        current_word_count += sentence_len

    if current_sentences:
        chunks.append(' '.join(current_sentences).strip())

    return [chunk for chunk in chunks if chunk]
