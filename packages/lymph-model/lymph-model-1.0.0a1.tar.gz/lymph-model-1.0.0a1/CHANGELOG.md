# Changelog

All notable changes to this project will be documented in this file.


<a name="unreleased"></a>
## [Unreleased]


<a name="1.0.0.a1"></a>
## [1.0.0.a1] - 2023-08-30

Second alpha release, aimed at testing the all new implementation. See these [issues](https://github.com/rmnldwg/lymph/milestone/1) for an idea of what this tries to address.

### Bug Fixes
- (**matrix**) Wrong shape of observation matrix for trinary model

### Documentation
- Fix wrong python version in rtd config file
- Remove outdated sampling tutorial
- Remove deprecated read-the-docs config
- Tell read-the-docs to install extra requirements
- Execute quickstart notebook

### Testing
- Check correct shapes for trinary model matrices


<a name="1.0.0.a0"></a>
## [1.0.0.a0] - 2023-08-15

This alpha release is a reimplementation most of the package's API. It aims to solve some [issues](https://github.com/rmnldwg/lymph/milestone/1) that accumulated for a while.

### Features
- parameters can now be assigned centrally via a `assign_params()` method, either using args or keyword arguments. This resolves [#46]
- expensive operations generally look expensive now, and do not just appear as if they were attribute assignments. Fixes [#40]
- computations around the the likelihood and risk predictions are now more modular. I.e., several conditional and joint probability vectors/matrices can now be computed conveniently and are not burried in large methods. Resolves isse [#41]
- support for the trinary model was added. This means lymph node levels (LNLs) can be in one of three states (healthy, microscopic involvement, macroscopic metatsasis), instead of only two (healthy, involved). Resolves [#45]

### Documentation
- module, class, method, and attribute docstrings should now be more detailed and helpful. We switched from strictly adhering to Numpy-style docstrings to something more akin to Python's core library docstrings. I.e., parameters and behaviour are explained in natural language.
- quickstart guide has been adapted to the new API

### Code Refactoring
- all matrices related to the underlying hidden Markov model (HMM) have been decoupled from the `Unilateral` model class
- the representation of the directed acyclic graph (DAG) that determined the directions of spread from tumor to and among the LNLs has been implemented in a separate class of which an instance provides access to it as an attribute of `Unilateral`
- access to all parameters of the graph (i.e., the edges) is bundled in a descriptor holding a `UserDict`

### BREAKING CHANGES
Almost the entire API has changed. I'd therefore recommend to have a look at the [quickstart guide](https://lymph-model.readthedocs.io/en/1.0.0.a0/quickstart.html) to see how the new model is used. Although most of the core concepts are still the same.

<a name="0.4.3"></a>
## [0.4.3] - 2022-09-02

### Bug Fixes
- incomplete involvement for unilateral risk method does not raise KeyError anymore. Fixes issue [#38]

<a name="0.4.2"></a>
## [0.4.2] - 2022-08-24

### Documentation
- fix the issue of docs failing to build
- remove outdated line in install instructions
- move conf.py back into source dir
- bundle sphinx requirements
- update the quickstart & sampling notebooks
- more stable sphinx-build & update old index

### Maintenance
- fine-tune git-chglog settings to my needs
- start with a CHANGELOG
- add description to types of allowed commits


<a name="0.4.1"></a>
## [0.4.1] - 2022-08-23
### Bug Fixes
- pyproject.toml referenced wrong README & LICENSE


<a name="0.4.0"></a>
## [0.4.0] - 2022-08-23
### Code Refactoring
- delete unnecessary utils

### Maintenance
- fix pyproject.toml typo
- add pre-commit hook to check commit msg


[Unreleased]: https://github.com/rmnldwg/lymph/compare/1.0.0.a1...HEAD
[1.0.0.a1]: https://github.com/rmnldwg/lymph/compare/1.0.0.a0...1.0.0.a1
[1.0.0.a0]: https://github.com/rmnldwg/lymph/compare/0.4.3...1.0.0.a0
[0.4.3]: https://github.com/rmnldwg/lymph/compare/0.4.2...0.4.3
[0.4.2]: https://github.com/rmnldwg/lymph/compare/0.4.1...0.4.2
[0.4.1]: https://github.com/rmnldwg/lymph/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/rmnldwg/lymph/compare/0.3.10...0.4.0

[#46]: https://github.com/rmnldwg/lymph/issues/46
[#45]: https://github.com/rmnldwg/lymph/issues/45
[#41]: https://github.com/rmnldwg/lymph/issues/41
[#40]: https://github.com/rmnldwg/lymph/issues/40
[#38]: https://github.com/rmnldwg/lymph/issues/38
