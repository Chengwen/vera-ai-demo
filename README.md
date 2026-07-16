# Vera AI · Buy Decision Agent

Streamlit demo for an AI wardrobe purchase decision engine.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Demo story

User sees a new clothing item in store or online, uploads a photo/link, and asks:

> Vera, should I buy this?

The demo analyzes:

- duplication with the user's existing wardrobe
- predicted dust risk / low-use probability
- fit and style match
- occasion gap match
- final decision: buy, cautious, or don't buy

