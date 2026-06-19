# Monitor Edictorum

Monitor automático de **editais e chamadas públicas** no Brasil, organizado por três eixos:

- **Inteligência Artificial**
- **Incentivo a Publicações**
- **Memória**

🔗 **Acesse online:** https://valantien.github.io/monitor-editais/

## Como funciona

- `coletar.py` busca o Google News RSS para cada palavra-chave dos eixos, filtra (ano mínimo e fontes portuguesas) e salva em `dados/noticias.csv`.
- `.github/workflows/monitor.yml` roda uma vez por dia via GitHub Actions e faz commit do CSV atualizado.
- `index.html` (GitHub Pages) lê o CSV com PapaParse e renderiza a interface.

## Deploy (já publicado)

Site no ar em **https://valantien.github.io/monitor-editais/** · repositório público: [valantien/monitor-editais](https://github.com/valantien/monitor-editais).

Como foi publicado (passos para reproduzir num outro fork):

1. ✅ No `index.html`, `USUARIO` está definido como `valantien` (linha `const USUARIO = "valantien";`).
2. ✅ Repositório subido como **público** com o nome `monitor-editais`.
3. ✅ **GitHub Pages** ativado (branch `main`, raiz `/`).

Adaptado de [larissacodes/monitor-labiia](https://github.com/larissacodes/monitor-labiia).
