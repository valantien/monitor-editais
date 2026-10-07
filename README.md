# Monitor Edictorum

Monitor automático de **editais e chamadas públicas** no Brasil, organizado por três eixos:

- **Inteligência Artificial**
- **Incentivo a Publicações**
- **Memória**

🔗 **Acesse online:** https://valantien.github.io/monitor-editais/

## Como funciona

- `coletar.py` busca o Google News RSS para cada palavra-chave dos eixos, filtra (descarta itens com mais de 6 meses e fontes portuguesas), classifica Agência e Tipo pelo título e salva em `dados/noticias.csv`.
- `.github/workflows/monitor.yml` roda uma vez por dia via GitHub Actions e faz commit do CSV atualizado.
- `index.html` (GitHub Pages) lê o CSV com PapaParse e renderiza a interface.

## Deploy (já publicado)

Site no ar em **https://valantien.github.io/monitor-editais/** · repositório público: [valantien/monitor-editais](https://github.com/valantien/monitor-editais).

Como foi publicado (passos para reproduzir num outro fork):

1. ✅ No `index.html`, `USUARIO` está definido como `valantien` (linha `const USUARIO = "valantien";`).
2. ✅ Repositório subido como **público** com o nome `monitor-editais`.
3. ✅ **GitHub Pages** ativado (branch `main`, raiz `/`).

## Origem e citação do projeto original

Este projeto é uma adaptação de **Monitor de Notícias - IA e Eleições**, de **Larissa Diniz Aguiar**
([LABIIA](https://github.com/labiia-lab)), repositório [labiia-lab/monitor-labiia](https://github.com/labiia-lab/monitor-labiia).
O código e o acervo do original estão sob a licença [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.pt_BR):
é permitido copiar e adaptar, desde que se cite a autoria, se indiquem as mudanças e não se use para fins comerciais.
Este monitor segue os mesmos termos: **uso não comercial**.

**Alterações feitas no Monitor Edictorum:** novo tema (editais e chamadas públicas, em vez de IA nas eleições),
três eixos próprios (Inteligência Artificial, Incentivo a Publicações, Memória), subgrupo e chip fundido,
classificação por Agência e Tipo, validade de 6 meses, coleta uma vez por dia e nova identidade visual.

**Como citar o original**

ABNT
Aguiar, Larissa Diniz. Monitor de Notícias - IA e Eleições. LABIIA, 2026. Software. Disponível em: https://github.com/labiia-lab/monitor-labiia.

APA
Aguiar, L. D. (2026). *Monitor de Notícias - IA e Eleições* [Software]. LABIIA. https://github.com/labiia-lab/monitor-labiia
