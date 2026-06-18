# Monitor Edictorum

Monitor automático de **editais e chamadas públicas** no Brasil, organizado por três eixos:

- **Inteligência Artificial**
- **Incentivo a Publicações**
- **Memória**

## Como funciona

- `coletar.py` busca o Google News RSS para cada palavra-chave dos eixos, filtra (ano mínimo e fontes portuguesas) e salva em `dados/noticias.csv`.
- `.github/workflows/monitor.yml` roda uma vez por dia via GitHub Actions e faz commit do CSV atualizado.
- `index.html` (GitHub Pages) lê o CSV com PapaParse e renderiza a interface.

## Antes do deploy

1. No `index.html`, troque `USUARIO = "SEU-USUARIO-GITHUB"` pelo seu usuário do GitHub.
2. Suba o repositório como **público** com o nome `monitor-editais`.
3. Ative **GitHub Pages** (branch `main`, raiz `/`).

Adaptado de [larissacodes/monitor-labiia](https://github.com/larissacodes/monitor-labiia).
