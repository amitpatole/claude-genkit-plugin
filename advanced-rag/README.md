# Advanced RAG Patterns for Genkit

Production-ready Retrieval-Augmented Generation patterns for building intelligent AI applications.

## 🎯 Overview

This directory contains advanced RAG (Retrieval-Augmented Generation) patterns that go beyond basic vector search, providing production-ready solutions for complex information retrieval scenarios.

## 📚 RAG Patterns

### 1. **Hybrid Search** (Semantic + Keyword)
Combine vector similarity with keyword matching for better results.

### 2. **Hierarchical RAG** (Multi-Level Retrieval)
Search at multiple granularities (documents → sections → paragraphs).

### 3. **Conversational RAG** (Context-Aware)
Maintain conversation history for contextual retrieval.

### 4. **Multi-Query RAG** (Query Expansion)
Generate multiple queries from user input for comprehensive results.

### 5. **Self-Querying RAG** (Metadata Filtering)
Extract filters from queries to narrow search space.

### 6. **Parent-Child RAG** (Document Chunking)
Store chunks but retrieve full documents for better context.

### 7. **Corrective RAG** (Self-Correction)
Evaluate relevance and re-query if needed.

### 8. **Adaptive RAG** (Dynamic Strategy)
Choose retrieval strategy based on query complexity.

## 🚀 Quick Start

```typescript
import {  hybridSearchRAG } from './advanced-rag/patterns/hybrid-search';

// Use hybrid search RAG
const result = await hybridSearchRAG({
  query: "How do I deploy Genkit to production?",
  topK: 5,
  hybridWeight: 0.7, // 70% semantic, 30% keyword
});
```

## 📁 Directory Structure

```
advanced-rag/
├── README.md (this file)
├── patterns/
│   ├── hybrid-search.ts
│   ├── hierarchical-rag.ts
│   ├── conversational-rag.ts
│   ├── multi-query-rag.ts
│   ├── self-querying-rag.ts
│   ├── parent-child-rag.ts
│   ├── corrective-rag.ts
│   └── adaptive-rag.ts
├── examples/
│   ├── simple-rag.ts
│   ├── production-rag.ts
│   └── advanced-use-cases.ts
└── templates/
    ├── vector-store-setup.ts
    ├── embedding-strategies.ts
    └── reranking.ts
```

## 🔧 Prerequisites

```bash
npm install @genkit-ai/ai @genkit-ai/anthropic
npm install @genkit-ai/googleai  # For embeddings
npm install @pinecone-database/pinecone  # Or your vector DB
```

## 📊 Pattern Comparison

| Pattern | Complexity | Latency | Accuracy | Use Case |
|---------|-----------|---------|----------|----------|
| Basic RAG | Low | Fast | Good | Simple Q&A |
| Hybrid Search | Medium | Fast | Better | Mixed queries |
| Hierarchical | Medium | Medium | Better | Long documents |
| Conversational | Medium | Fast | Better | Chat apps |
| Multi-Query | High | Slow | Best | Complex queries |
| Self-Querying | Medium | Fast | Better | Filtered search |
| Parent-Child | Medium | Medium | Better | Context preservation |
| Corrective | High | Slow | Best | High accuracy needs |
| Adaptive | High | Variable | Best | General purpose |

## 🎯 Pattern Details

### 1. Hybrid Search RAG

**Problem:** Pure semantic search misses exact matches; keyword search misses context.

**Solution:** Combine both approaches with weighted scoring.

**Benefits:**
- Better recall and precision
- Handles both semantic and exact matches
- Configurable weighting

**Use Cases:**
- Technical documentation
- Product search
- Legal documents

### 2. Hierarchical RAG

**Problem:** Large documents lose context when chunked.

**Solution:** Create multi-level index (doc → section → chunk).

**Benefits:**
- Better context preservation
- Efficient for long documents
- Progressive retrieval

**Use Cases:**
- Research papers
- Technical manuals
- Books

### 3. Conversational RAG

**Problem:** Follow-up questions lack context.

**Solution:** Include conversation history in retrieval.

**Benefits:**
- Context-aware responses
- Better user experience
- Handles pronouns and references

**Use Cases:**
- Customer support
- Chat applications
- Interactive tutorials

### 4. Multi-Query RAG

**Problem:** Single query may miss relevant documents.

**Solution:** Generate multiple query variations.

**Benefits:**
- Higher recall
- Better coverage
- Robust to query phrasing

**Use Cases:**
- Research assistance
- Complex information needs
- Ambiguous queries

### 5. Self-Querying RAG

**Problem:** User queries contain implicit filters.

**Solution:** Extract metadata filters from natural language.

**Benefits:**
- More precise results
- Reduced search space
- Better performance

**Use Cases:**
- E-commerce search
- Filtered databases
- Multi-attribute search

### 6. Parent-Child RAG

**Problem:** Small chunks lack context; large chunks have low relevance.

**Solution:** Retrieve chunks, return parent documents.

**Benefits:**
- Best of both worlds
- Full context available
- Precise retrieval

**Use Cases:**
- Code documentation
- Academic papers
- Technical specs

### 7. Corrective RAG

**Problem:** Retrieved documents may be irrelevant.

**Solution:** Evaluate relevance, re-query if needed.

**Benefits:**
- Higher accuracy
- Self-correcting
- Reduced hallucinations

**Use Cases:**
- Critical applications
- High-stakes decisions
- Fact-checking

### 8. Adaptive RAG

**Problem:** Different queries need different strategies.

**Solution:** Choose strategy based on query analysis.

**Benefits:**
- Optimal for each query
- Balances speed and accuracy
- Production-ready

**Use Cases:**
- General-purpose RAG
- Mixed workloads
- Unknown query types

## 💡 Best Practices

### Chunking Strategies
```typescript
// Semantic chunking
const chunks = await semanticChunking(document, {
  maxTokens: 512,
  overlap: 50,
  preserveSentences: true,
});

// Hierarchical chunking
const hierarchy = await hierarchicalChunking(document, {
  levels: ['document', 'section', 'paragraph'],
  maxTokensPerLevel: [2048, 512, 128],
});
```

### Embedding Strategies
```typescript
// Use appropriate embedding model
const embeddings = await embed({
  model: 'text-embedding-004',  // Latest Gemini
  texts: chunks,
  batchSize: 100,
});
```

### Reranking
```typescript
// Rerank retrieved documents
const reranked = await rerank({
  query,
  documents,
  model: claude35Sonnet,
  topK: 5,
});
```

## 🔍 Evaluation Metrics

### Retrieval Metrics
- **Recall@K:** Percentage of relevant docs in top K
- **Precision@K:** Percentage of retrieved docs that are relevant
- **MRR:** Mean Reciprocal Rank
- **NDCG:** Normalized Discounted Cumulative Gain

### End-to-End Metrics
- **Answer Relevance:** Is the answer relevant to the query?
- **Faithfulness:** Is the answer grounded in retrieved docs?
- **Context Precision:** Are retrieved docs relevant?
- **Context Recall:** Are all relevant docs retrieved?

### Implementation
```typescript
import { evaluateRAG } from './templates/evaluation';

const metrics = await evaluateRAG({
  queries: testQueries,
  groundTruth: testAnswers,
  ragSystem: myRAGSystem,
});
```

## 🎨 Customization

### Custom Vector Store
```typescript
import { VectorStore } from './templates/vector-store-setup';

class MyVectorStore extends VectorStore {
  async search(query: string, topK: number) {
    // Your implementation
  }

  async insert(documents: Document[]) {
    // Your implementation
  }
}
```

### Custom Reranker
```typescript
import { Reranker } from './templates/reranking';

class MyReranker extends Reranker {
  async rerank(query: string, docs: Document[]) {
    // Your implementation
  }
}
```

## 📈 Performance Optimization

### Caching
```typescript
import { cacheEmbeddings } from './templates/caching';

// Cache embeddings
const cached = await cacheEmbeddings(chunks, {
  ttl: 3600,
  storage: 'redis',
});
```

### Batch Processing
```typescript
// Process queries in batches
const results = await batchRAG(queries, {
  batchSize: 10,
  parallel: true,
});
```

### Streaming
```typescript
// Stream results as they arrive
for await (const result of streamRAG(query)) {
  console.log(result);
}
```

## 🔐 Security Considerations

### Access Control
```typescript
// Filter results by user permissions
const filtered = await ragWithACL(query, {
  userId,
  permissions,
});
```

### Data Privacy
```typescript
// Anonymize sensitive data
const safe = await anonymizeRAG(query, {
  piiDetection: true,
  redaction: true,
});
```

## 📚 Resources

- [RAG Survey Paper](https://arxiv.org/abs/2312.10997)
- [LangChain RAG Guide](https://python.langchain.com/docs/use_cases/question_answering/)
- [Pinecone RAG Guide](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [Genkit Documentation](https://genkit.dev/docs/rag/)

## 🆘 Troubleshooting

### Low Recall
- Increase topK
- Improve embeddings
- Try hybrid search

### Low Precision
- Add reranking
- Improve chunking
- Filter metadata

### High Latency
- Cache embeddings
- Use batch processing
- Optimize vector DB

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/amitpatole/claude-genkit-plugin/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/amitpatole/claude-genkit-plugin/discussions)
- 📧 **Email**: amit.patole@gmail.com

---

**Build intelligent RAG systems!** Choose your pattern and start retrieving. 🚀
