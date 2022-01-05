# Kogi

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Contributors](#contributors)

## Background

This repository is for testing KoGPT-2 with four different application.

1. *Question Generation*,
this application is to generate questions with a body of text and keywords. It generates questions which match each keywords as answer.

2. *Article Summarization*,
this application is to summarize aritcle. It generates a single line of summary.

3. *Tale Generation*,
this application is to generate fairy tale. It can generate a sentence or a word which follows the body you wrote

4. *Review Generation*,
this application is to generate review. It can generate a sentence or a word which follows the body you wrote

You can also test it through this [website](http://14.49.45.139:80/)

## Install

For Backend - uses [pytorch](https://pytorch.org/), [transformers](https://github.com/huggingface/transformers), [tokenizers](https://github.com/huggingface/tokenizers), [mysql](https://www.mysql.com/).

```sh
cd backend
pip install -r requirements.txt
```

For Frontend - uses [node](https://nodejs.org/)

```sh
cd frontend
npm install
```

For downloading models - *Very Important*

1. Download all models from this [Google Drive URL](https://drive.google.com/drive/folders/17j-VoWHdLsTWvLSaCR0iiJRiDt1SslZT)
2. Put all models into '/backend/models' folder

## Usage

For Backend - should be in '/backend'

```sh
python app.py
```

For Frontend - should be in '/frontend'

```sh
npm start
```

Enter http://localhost:9999/.

### Contributors

[@homin025](https://github.com/homin025)
[@binyf](https://github.com/binyf)
[@KIMKEUNHA](https://github.com/KIMKEUNHA).
