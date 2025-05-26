# flet-todos

## 프로젝트 구동

### 필요한 프로그램

1. [bun](https://bun.sh) 설치

```sh
powershell -c "irm bun.sh/install.ps1 | iex" # 윈도우
curl -fsSL https://bun.sh/install | bash     # 리눅스/맥
```

2. [uv](https://docs.astral.sh/uv/) 설치

```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" # 윈도우
https://docs.astral.sh/uv/ # 리눅스/맥
```

### 프로젝트 설정

1. 프로젝트 받기

```sh
git clone https://github.com/sesac-namu/euntaek-flet-todos flet-todos
cd flet-todos
```

2. 패키지 설치

```sh
bun i
cd apps/frontend
uv sync
cd ../..
```

### 개발 서버 (웹)

```sh
bun run dev:web
```
