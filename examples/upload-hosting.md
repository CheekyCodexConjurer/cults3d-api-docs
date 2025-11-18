# Hosting file links for createCreation

1. Gerar o arquivo final (ZIP ou PNG) localmente.
2. Escolher o host temporário:
   - transfer.sh (grava até 10GB; link expira em 14 dias)
   - tmpfiles.org (limite seguro ~200 MB por upload; expira em ~7 dias)
3. Para tmpfiles, usar a API `POST https://tmpfiles.org/api/v1/upload` (multipart/form-data).
4. O JSON de resposta contém `data.url` e `data.download_url`. Usar sempre o link direto `https://tmpfiles.org/dl/<id>/<arquivo.extensão>`.
5. O link inserido em `fileUrls`/`imageUrls` DEVE terminar com a extensão (`.zip`, `.png`, etc.) para que os validadores aceitem o arquivo.
6. Se o ZIP exceder o limite do tmpfiles, dividir em partes menores (`<nome>-Part1.zip`, `<nome>-Part2.zip`) e enviar cada parte separadamente.
7. Preencher `fileUrls` com até 10 links de ZIPs e `imageUrls` com até 10 renders. Cada URL deve ser publicamente acessível.

