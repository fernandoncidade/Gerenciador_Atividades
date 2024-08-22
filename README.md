# README

## Cadastro de Atividades Avaliativas

Este repositório contém um projeto em Python que implementa uma interface gráfica (GUI) para o gerenciamento de atividades avaliativas em ambientes educacionais. A interface foi desenvolvida utilizando o framework PySide6 e integra-se com dois módulos personalizados: `Gerenciador_Atividades` e `Banco_Dados`.

### Funcionalidades

- **Cadastro de Atividades:** Permite o registro de atividades avaliativas com informações detalhadas como curso, ementa, semestre, disciplina, turma, tipo de atividade, sequência e data.
- **Gerenciamento de Dados:** As atividades cadastradas são gerenciadas e podem ser visualizadas em uma caixa de texto dentro da GUI.
- **Exportação para PDF:** As definições das atividades podem ser exportadas para um arquivo PDF.
- **Limpeza de Entradas:** Funções para limpar as entradas do formulário, seja a última entrada ou todas as entradas.
- **Atualização Dinâmica:** Combinações e caixas de texto são atualizadas dinamicamente com base nas escolhas do usuário, integrando os dados fornecidos pelos módulos `Banco_Dados`.

### Estrutura do Projeto

- **InterfaceGerenciadorAtividades:** Classe principal que herda de `QMainWindow` e configura a interface gráfica, layout, e os widgets utilizados no aplicativo.
- **Gerenciador_Atividades:** Módulo personalizado responsável pelo gerenciamento das atividades, incluindo métodos para registro, limpeza e exportação de dados.
- **Banco_Dados:** Módulo que fornece as listas de cursos, turmas e tipos de avaliação disponíveis, utilizados para popular os componentes da interface.

### Dependências

- **Python 3.x**
- **PySide6:** Utilizado para criar a interface gráfica do usuário.
- **ReportLab:** Requerido para exportar os dados para PDF (assumido, embora não explicitado no código).

### Como Executar

1. Clone este repositório.
   ```bash
   git clone https://github.com/fernandoncidade/Gerenciador_Atividades
   cd Gerenciador_Atividades
   ```
2. Instale as dependências necessárias.
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o aplicativo.
   ```bash
   python Interface_Grafica.py
   ```

### Uso

Ao iniciar o aplicativo, você verá uma interface para o cadastro de atividades avaliativas. Selecione as opções desejadas para cada campo e clique em "Registrar Definições" para salvar as atividades. Utilize os botões para limpar entradas ou exportar os dados para PDF.

### Personalização

Se desejar modificar os cursos, turmas ou tipos de avaliação disponíveis, edite o módulo `Banco_Dados` conforme necessário. O mesmo se aplica às funcionalidades de gerenciamento no módulo `Gerenciador_Atividades`.

### Contribuição

Sinta-se à vontade para abrir issues ou pull requests caso tenha sugestões de melhorias ou correções.

### Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para obter mais informações.

---

Este README fornece uma visão geral do funcionamento do aplicativo, com instruções detalhadas para uso e personalização.
