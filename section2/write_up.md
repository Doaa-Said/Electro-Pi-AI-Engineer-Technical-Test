# Write-up

If the answer quality on longer documents were poor, I would first improve the chunking strategy. In this project, I used fixed-size chunks with overlap, which works well for small documents but may split related information across multiple chunks. For larger documents, I would use semantic or structure-aware chunking, where chunks are created based on headings, paragraphs, or sections instead of a fixed number of characters. This helps preserve context and improves retrieval accuracy.

I would also experiment with different chunk sizes and overlaps. Smaller chunks usually improve retrieval precision because they contain more focused information, while larger chunks provide more context but may include irrelevant text. Choosing the right balance depends on the type of documents being indexed.

For retrieval, I would replace pure vector search with hybrid search, which combines dense vector embeddings with traditional keyword-based search such as BM25. Hybrid search performs better when users ask questions containing specific names, numbers, or technical terms that semantic embeddings may not retrieve effectively.

Another improvement would be adding a re-ranking model. Instead of sending the retrieved documents directly to the language model, a cross-encoder re-ranker could score the retrieved chunks and reorder them according to their relevance. This ensures that the most useful context is placed first, reducing the chance of the model using irrelevant information.

For very long documents, I would also retrieve more candidate chunks (for example, the top 10) and then use a re-ranker to select the best 3–5 chunks before passing them to the language model. This approach increases recall while keeping the final context concise.

Overall, if answer quality decreased on larger documents, my priorities would be: (1) improve chunking, (2) use hybrid search, (3) add a re-ranking stage, and (4) tune retrieval parameters such as chunk size, overlap, and the number of retrieved documents.** These improvements would likely produce more accurate and reliable answers while reducing irrelevant context.
