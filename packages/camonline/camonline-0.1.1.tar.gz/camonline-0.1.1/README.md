![](https://img.shields.io/github/license/wh1isper/camonline)
![](https://img.shields.io/github/v/release/wh1isper/camonline)
![](https://img.shields.io/pypi/dm/camonline)
![](https://img.shields.io/github/last-commit/wh1isper/camonline)
![](https://img.shields.io/pypi/pyversions/camonline)

# camonline

Make your computer camera a monitor

## Install

`pip install camonline`

## Usage

```bash
docker run -d --restart always \
--name camonline \
--device=/dev/video0:/dev/video0 \
-v ~/.camonline:/root/.camonline \
wh1isper/camonline
```

## Develop

Install pre-commit before commit

```
pip install pre-commit
pre-commit install
```

Install package locally

```
pip install -e .[test]
```

Run unit-test before PR, **ensure that new features are covered by unit tests**

```
pytest -v
```
