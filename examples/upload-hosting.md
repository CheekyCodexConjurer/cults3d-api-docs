# Hosting file links for createCreation (Google Drive)

1. Gere o arquivo final (ZIP ou PNG) localmente.
2. Envie os arquivos para uma pasta no Google Drive (via UI ou API).
3. Marque cada arquivo como "qualquer pessoa com o link pode visualizar".
4. Construa o link direto usando o `fileId` do Drive:
   - `https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&confirm=t&filename=<nome.extensao>`
   - Alternativa: `https://drive.google.com/uc?export=download&id=<FILE_ID>&filename=<nome.extensao>`
5. Os links em `fileUrls`/`imageUrls` DEVEM expor a extensao (`.zip`, `.png`, etc.) para evitar nomes "Unknown" no dashboard.
6. Cada campo aceita ate 10 URLs; combine renders ou ZIPs extras em menos links se precisar.
7. Mantenha os arquivos publicos durante o consumo do upload pela API; depois ajuste permissoes conforme sua politica.
