# Optional Quran corpus lookup utility

`q.py` is the generated verse lookup/search utility used in the separate Lighthouse framework. The lookup paths are now relative to this directory rather than `/home/user`.

The four downloaded JSON corpora are third-party sources and are **not** part of the generated-artifact Git snapshot. To populate them with an internet connection:

```sh
python3 quran/download_corpus.py
python3 quran/q.py 2:255 42:11
```

Source endpoint: `https://api.alquran.cloud/v1/quran/{edition}`, editions `quran-simple`, `en.sahih`, `en.arberry`, `en.pickthall`. Source attribution and translation rights remain with the corpus providers/translators. Retrieval does not establish any interpretation: the framework's text/context/tafsir and governance requirements are independent of a string search.
