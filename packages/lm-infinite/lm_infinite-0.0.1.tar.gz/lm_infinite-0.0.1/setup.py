# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['infinite']

package_data = \
{'': ['*']}

modules = \
['__init__']
setup_kwargs = {
    'name': 'lm-infinite',
    'version': '0.0.1',
    'description': 'Paper - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Paper-Implementation-Template\nLM-Infinite is a solution proposed by Chi Han, Qifan Wang, Wenhan Xiong, Yu Chen, Heng Ji, and Sinong Wang to address the length generalization failure of Large Language Models (LLMs) on long sequences. LLMs, such as Transformer-based models, have shown impressive performance in various domains but struggle when it comes to longer reasoning processes or understanding larger contexts. Current pre-training schemes truncate training sequences to a fixed length, and even with relative positional encoding, LLMs struggle to generate coherent texts or perform downstream tasks after longer contexts.\n\nThe authors investigate the main out-of-distribution factors contributing to this problem and propose LM-Infinite as an efficient solution. LM-Infinite only requires a Λ-shaped attention mask and a distance limit, without any parameter updates or learning. It can be applied to different LLMs using relative-position encoding methods. LM-Infinite demonstrates consistent fluency and generation quality for sequences as long as 32k tokens on datasets like ArXiv and OpenWebText2, with a decoding speedup of 2.72x. Furthermore, it continues to perform well on inputs much longer than training lengths in downstream tasks like passkey retrieval, where vanilla models fail immediately.\n\nPaper Link\n\n# Appreciation\n* Lucidrains\n* Agorians\n\n\n\n# Install\n\n\n# Usage\n\n# Architecture\n\n# Todo\n\n\n# License\nMIT\n\n# Citations\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/LM-Infinite',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
