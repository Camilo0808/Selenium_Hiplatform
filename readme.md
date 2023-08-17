---

# Projeto de Automação de Atualização de Relatórios HSM

Este projeto Python oferece uma solução eficiente e automatizada para a extração e atualização diária dos dados do relatório HSM (Histórico de Mensagens) do site Hiplatform. Utilizando as bibliotecas Selenium, Pandas, SQLAlchemy e Numpy, este projeto simplifica o processo de obtenção de informações essenciais do relatório HSM e a integração desses dados ao seu banco de dados.

## Visão Geral

A extração e análise de dados de relatórios HSM podem ser um processo complexo e demorado, especialmente quando feito manualmente. Este projeto oferece uma abordagem automatizada para:

- Acessar o site Hiplatform utilizando o Selenium, garantindo uma interação controlada com a interface.
- Efetuar login com as credenciais fornecidas e navegar até o relatório HSM.
- Extrair os dados relevantes do relatório HSM, incluindo remetente, destinatário, datas de envio, entrega e leitura, mensagens de erro e muito mais.
- Utilizar a biblioteca Pandas para organizar e estruturar os dados extraídos em um DataFrame de fácil manipulação.
- Integrar os dados ao banco de dados escolhido, atualizando-o diariamente com as informações mais recentes.

## Como Usar

1. Clone este repositório para o seu ambiente local.
2. Defina as credenciais de login para o site Hiplatform e as credenciais para a conexão ao banco de dados relacional. Para isso crie o seu arquivo `.env`.
3. Configure e carregue as variáveis de ambiente no arquivo 'settings.py'.
4. Configure a conexão com o banco de dados no arquivo `connection.py`.
5. Ajuste o caminho até o diretório que contenha o projeto, na variável project_home, no arquivo 'export_hsm_report.py'.
6. Instale a versão do Docker compatível com o seu sistema operacional.
7. Execute o script principal para iniciar o processo de extração e atualização:

   ```bash
   docker build -t hsm-report-app .
   docker run -it --rm hsm-report-app
   ```

8. O script irá automatizar o login no site Hiplatform, extrair os dados do relatório HSM e atualizar o banco de dados com as informações mais recentes.

## Observações

- Certifique-se de manter suas credenciais e informações de conexão ao banco de dados no arquivo .env e não as compartilhe publicamente.
- Este projeto é projetado para funcionar com o site Hiplatform e pode precisar de ajustes para se adequar a outras plataformas ou sites.

Sinta-se à vontade para contribuir, ajustar ou estender este projeto conforme necessário para atender às suas necessidades específicas. Se tiver alguma dúvida ou feedback, por favor, abra uma nova issue neste repositório.

---
