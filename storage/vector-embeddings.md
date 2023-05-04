If you are at the beginning of your machine learning studies, you probably already read the term "vector embeddings" together with NLP (Natural Language Processing). But what is this?

## Vector? Which kind of vector?

The term "vector" can be quite ambiguous, as it has various meanings depending on the context. In physics, vectors describe quantities with both magnitude and direction within a 3D space. In programming, vectors are often synonymous with arrays while in mathematics, vectors have their own unique definition. There are even vectors in biology, and the list goes on.

**For our purposes in machine learning, we need to focus on the mathematical and programming vectors**, and we'll see how they are closely interconnected.

&nbsp;

## Mathematical vectors

Mathematical vectors were inherited from physics, so they are values with direction, sense and magnitude.

![1D Vectors](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4zbhbgej8tiuau1e00we.png)

`i`  and `j` are 1D (one dimensional) vectors with the same magnitude, but with different directions.

We also have the 2D and 3D vectors:

![2D and 3D vectors](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/c93d6gw4e477xob1kh8q.png)

### So... what's the difference between a math vector and a physics vector?

While a physics vector is used to represent and analyze real-word physical quantities, a math vector is arbitrary and not necessarily represent (and respect😶) physical properties and rules. For example, OpenAI's generated vector embeddings have 1536 dimensions.

[See more about OpenAI vector embeddings](https://platform.openai.com/docs/guides/embeddings/use-cases)

### How can a vector have 1536 dimensions?

How is this possible? We only have 3 dimensions, right? **RIGHT!**

But as I said earlier, math vectors are arbitrary, so their dimensions are not necessarily related to the real physical world. A vector dimension in math is more like an aspect, a characteristic or a feature of the data. For example, as you may know, ChatGPT is a NLP model, so its vector embeddings need to have many dimensions to capture the meaning of so many words, getting contexts, interpretation, sentiment analysis and so on... they are called **high-dimensional vectors**.

&nbsp;

## What are vector embeddings?

Vector embeddings are numerical representations of words or sentences, used in Natural Language Processing (NLP) to facilitate efficient analysis and manipulation of text data. By converting text into vector embeddings, NLP models can easily perform tasks such as querying, classification, and applying machine learning algorithms on textual data. So a vector embedding is nothing more than a mathematical vector generated to be used in machine-learning tasks.

&nbsp;

## How a sentence is converted into a vector?

![OpenAI embedding example](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/my8cchkbwxwoad736zzv.png)

There are multiple techniques to convert a sentence into a vector. One popular method is using word embeddings algorithms, such as Word2Vec, GloVe, or FastText, and then aggregating the word embeddings to form a sentence-level vector representation. Another common approach is to use pre-trained language models, like BERT or GPT, which can provide contextualized embeddings for entire sentences.

Using word embedding algorithms and then aggregating it to the sentence may not capture the nuances of word order or complex structures. More advanced techniques, like using pre-trained language models (e.g., BERT or GPT), can provide better contextualized embeddings for sentences. These models are based on deep learning architectures such as Transformers, which can capture the contextual information and relationships between words in a sentence more effectively.

&nbsp;

## Conclusion

In conclusion, vector embeddings are a crucial component of modern Natural Language Processing (NLP) and machine learning. By representing words or sentences as high-dimensional mathematical vectors, NLP models can efficiently process and analyze textual data for various tasks, such as querying, classification, and sentiment analysis. While the concept of vectors spans multiple disciplines, it's essential to understand that mathematical vectors are not limited by the physical world's dimensions.
