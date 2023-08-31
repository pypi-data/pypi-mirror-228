# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sylloge']

package_data = \
{'': ['*']}

install_requires = \
['dask>=2022.01.0',
 'moviegraphbenchmark>=1.0.1,<2.0.0',
 'pandas>=1.0',
 'pyarrow',
 'pystow>=0.4.6,<0.5.0',
 'python-slugify>=7.0.0']

extras_require = \
{'docs': ['Sphinx>=5.0.0,<6.0.0',
          'insegel>=1.3.1,<2.0.0',
          'sphinx-automodapi>=0.14.1,<0.15.0',
          'sphinx-autodoc-typehints>=1.19.2,<2.0.0']}

setup_kwargs = {
    'name': 'sylloge',
    'version': '0.2.0',
    'description': 'Small library to simplify collecting and loading of entity alignment benchmark datasets',
    'long_description': '<p align="center">\n<img src="https://github.com/dobraczka/sylloge/raw/main/docs/logo.png" alt="sylloge logo", width=200/>\n</p>\n\n<h2 align="center">sylloge</h2>\n\n<p align="center">\n<a href="https://github.com/dobraczka/sylloge/actions/workflows/main.yml"><img alt="Actions Status" src="https://github.com/dobraczka/sylloge/actions/workflows/main.yml/badge.svg?branch=main"></a>\n<a href=\'https://sylloge.readthedocs.io/en/latest/?badge=latest\'><img src=\'https://readthedocs.org/projects/sylloge/badge/?version=latest\' alt=\'Documentation Status\' /></a>\n<a href="https://pypi.org/project/sylloge"/><img alt="Stable python versions" src="https://img.shields.io/pypi/pyversions/sylloge"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\nThis simple library aims to collect entity-alignment benchmark datasets and make them easily available.\n\nUsage\n=====\nLoad benchmark datasets:\n```\n>>> from sylloge import OpenEA\n>>> ds = OpenEA()\n>>> ds\nOpenEA(backend=pandas, graph_pair=D_W, size=15K, version=V1, rel_triples_left=38265, rel_triples_right=42746, attr_triples_left=52134, attr_triples_right=138246, ent_links=15000, folds=5)\n>>> ds.rel_triples_right.head()\n                                       head                             relation                                    tail\n0   http://www.wikidata.org/entity/Q6176218   http://www.wikidata.org/entity/P27     http://www.wikidata.org/entity/Q145\n1   http://www.wikidata.org/entity/Q212675  http://www.wikidata.org/entity/P161  http://www.wikidata.org/entity/Q446064\n2   http://www.wikidata.org/entity/Q13512243  http://www.wikidata.org/entity/P840      http://www.wikidata.org/entity/Q84\n3   http://www.wikidata.org/entity/Q2268591   http://www.wikidata.org/entity/P31   http://www.wikidata.org/entity/Q11424\n4   http://www.wikidata.org/entity/Q11300470  http://www.wikidata.org/entity/P178  http://www.wikidata.org/entity/Q170420\n>>> ds.attr_triples_left.head()\n                                  head                                          relation                                               tail\n0  http://dbpedia.org/resource/E534644                http://dbpedia.org/ontology/imdbId                                            0044475\n1  http://dbpedia.org/resource/E340590               http://dbpedia.org/ontology/runtime  6480.0^^<http://www.w3.org/2001/XMLSchema#double>\n2  http://dbpedia.org/resource/E840454  http://dbpedia.org/ontology/activeYearsStartYear     1948^^<http://www.w3.org/2001/XMLSchema#gYear>\n3  http://dbpedia.org/resource/E971710       http://purl.org/dc/elements/1.1/description                          English singer-songwriter\n4  http://dbpedia.org/resource/E022831       http://dbpedia.org/ontology/militaryCommand                     Commandant of the Marine Corps\n>>> ds.ent_links.head()\n                                  left                                    right\n0  http://dbpedia.org/resource/E123186    http://www.wikidata.org/entity/Q21197\n1  http://dbpedia.org/resource/E228902  http://www.wikidata.org/entity/Q5909974\n2  http://dbpedia.org/resource/E718575   http://www.wikidata.org/entity/Q707008\n3  http://dbpedia.org/resource/E469216  http://www.wikidata.org/entity/Q1471945\n4  http://dbpedia.org/resource/E649433  http://www.wikidata.org/entity/Q1198381\n```\n\nYou can get a canonical name for a dataset instance to use e.g. to create folders to store experiment results:\n\n```\n   >>> ds.canonical_name\n   \'openea_d_w_15k_v1\'\n```\n\nCreate id-mapped dataset for embedding-based methods:\n\n```\n>>> from sylloge import IdMappedEADataset\n>>> id_mapped_ds = IdMappedEADataset.from_ea_dataset(ds)\n>>> id_mapped_ds\nIdMappedEADataset(rel_triples_left=38265, rel_triples_right=42746, attr_triples_left=52134, attr_triples_right=138246, ent_links=15000, entity_mapping=30000, rel_mapping=417, attr_rel_mapping=990, attr_mapping=138836, folds=5)\n>>> id_mapped_ds.rel_triples_right\n[[26048   330 16880]\n [19094   293 23348]\n [16554   407 29192]\n ...\n [16480   330 15109]\n [18465   254 19956]\n [26040   290 28560]]\n```\n\nYou can use [dask](https://www.dask.org/) as backend for larger datasets:\n```\n>>> ds = OpenEA(backend="dask")\n>>> ds\nOpenEA(backend=dask, graph_pair=D_W, size=15K, version=V1, rel_triples_left=38265, rel_triples_right=42746, attr_triples_left=52134, attr_triples_right=138246, ent_links=15000, folds=5)\n```\nWhich replaces pandas DataFrames with dask DataFrames.\n\nDatasets can be written/read as parquet via `to_parquet` or `read_parquet`.\nAfter the initial read datasets are cached using this format. The `cache_path` can be explicitly set and caching behaviour can be disable via `use_cache=False`, when initalizing a dataset.\n\nSome datasets come with pre-determined splits:\n\n```bash\ntree ~/.data/sylloge/open_ea/cached/D_W_15K_V1 \n├── attr_triples_left_parquet\n├── attr_triples_right_parquet\n├── dataset_names.txt\n├── ent_links_parquet\n├── folds\n│\xa0\xa0 ├── 1\n│\xa0\xa0 │\xa0\xa0 ├── test_parquet\n│\xa0\xa0 │\xa0\xa0 ├── train_parquet\n│\xa0\xa0 │\xa0\xa0 └── val_parquet\n│\xa0\xa0 ├── 2\n│\xa0\xa0 │\xa0\xa0 ├── test_parquet\n│\xa0\xa0 │\xa0\xa0 ├── train_parquet\n│\xa0\xa0 │\xa0\xa0 └── val_parquet\n│\xa0\xa0 ├── 3\n│\xa0\xa0 │\xa0\xa0 ├── test_parquet\n│\xa0\xa0 │\xa0\xa0 ├── train_parquet\n│\xa0\xa0 │\xa0\xa0 └── val_parquet\n│\xa0\xa0 ├── 4\n│\xa0\xa0 │\xa0\xa0 ├── test_parquet\n│\xa0\xa0 │\xa0\xa0 ├── train_parquet\n│\xa0\xa0 │\xa0\xa0 └── val_parquet\n│\xa0\xa0 └── 5\n│\xa0\xa0     ├── test_parquet\n│\xa0\xa0     ├── train_parquet\n│\xa0\xa0     └── val_parquet\n├── rel_triples_left_parquet\n└── rel_triples_right_parquet\n```\nsome don\'t:\n```bash\ntree ~/.data/sylloge/oaei/cached/starwars_swg\n├── attr_triples_left_parquet\n│\xa0\xa0 └── part.0.parquet\n├── attr_triples_right_parquet\n│\xa0\xa0 └── part.0.parquet\n├── dataset_names.txt\n├── ent_links_parquet\n│\xa0\xa0 └── part.0.parquet\n├── rel_triples_left_parquet\n│\xa0\xa0 └── part.0.parquet\n└── rel_triples_right_parquet\n    └── part.0.parquet\n```\n\n\nInstallation\n============\n```bash\npip install sylloge \n```\n\nDatasets\n========\n| Dataset family name | Year | # of Datasets | Sources | References |\n|:--------------------|:----:|:-------------:|:-------:|:----------|\n| [OpenEA](https://sylloge.readthedocs.io/en/latest/source/datasets.html#sylloge.OpenEA) | 2020 | 16 | DBpedia, Yago, Wikidata |  [Paper](http://www.vldb.org/pvldb/vol13/p2326-sun.pdf), [Repo](https://github.com/nju-websoft/OpenEA#dataset-overview) |\n| [MovieGraphBenchmark](https://sylloge.readthedocs.io/en/latest/source/datasets.html#sylloge.MovieGraphBenchmark) | 2022 | 3 | IMDB, TMDB, TheTVDB | [Paper](http://ceur-ws.org/Vol-2873/paper8.pdf), [Repo](https://github.com/ScaDS/MovieGraphBenchmark) |\n| [OAEI](https://sylloge.readthedocs.io/en/latest/source/datasets.html#sylloge.OAEI) | 2022 | 5 | Fandom wikis | [Paper](https://ceur-ws.org/Vol-3324/oaei22_paper0.pdf), [Website](http://oaei.ontologymatching.org/2022/knowledgegraph/index.html) |\n',
    'author': 'Daniel Obraczka',
    'author_email': 'obraczka@informatik.uni-leipzig.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dobraczka/sylloge',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
