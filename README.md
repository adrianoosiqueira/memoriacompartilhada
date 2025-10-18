# 📦 Sistema de Pedidos com Memória Compartilhada (IPC)

## Visão Geral

Este projeto demonstra a Comunicação Interprocessos (IPC) em Python através do uso de **Memória Compartilhada**. O sistema simula uma central de pedidos, onde processos distintos (Produtores e Consumidores) interagem e modificam dados simultaneamente, garantindo a integridade dos dados por meio de técnicas de sincronização.

O monitoramento do sistema é feito em tempo real por meio de uma interface gráfica simples desenvolvida em Tkinter.

## ⚙️ Descrição do Cenário e Arquitetura

O sistema é baseado no modelo Produtor-Consumidor e segue a seguinte estrutura:

### 1. Processos

| Processo | Função Principal | Status Inicial |
| :--- | :--- | :--- |
| **Produtor** | Cria novos pedidos em intervalos aleatórios e os insere na memória. | "Em preparo" |
| **Consumidor** | Seleciona pedidos "Em preparo" aleatoriamente e finaliza o processo. | Altera para "Pronto" |

### 2. Memória Compartilhada e Dados

* **Tecnologia:** Implementada utilizando `multiprocessing.shared_memory.SharedMemory`.
* **Formato dos Dados:** Os pedidos são armazenados como uma lista de dicionários serializada em **JSON**, facilitando a manipulação estruturada.

### 3. Sincronização

Para evitar **condições de corrida** e garantir a atomicidade das operações de leitura e escrita:

* **Semaphore:** Controla o acesso global à seção crítica (a memória compartilhada).
* **Lock:** Impede conflitos de escrita simultânea dentro da seção crítica.

---

## 🖥️ Interface Gráfica (Tkinter)

A GUI fornece monitoramento em tempo real do status do sistema:

| Elemento | Função | Destaque Visual |
| :--- | :--- | :--- |
| **TreeView** | Exibe todos os pedidos com ID e Status. | Atualiza a cada segundo. |
| **Contadores** | Exibe o número total de pedidos criados e o total de pedidos prontos. | Localizado no topo da interface. |
| **Coloração** | **Laranja** ➡️ Pedido "Em preparo". | **Verde** ➡️ Pedido "Pronto". |

### 📸 Evidências da Interface

**(Aqui você inseriria a imagem real do seu sistema em funcionamento)**

| Lista de Pedidos (Exemplo Visual) | Contadores (Exemplo Visual) |
| :---: | :---: |
| *(Imagem da TreeView mostrando pedidos Laranja e Verde)* | *(Imagem dos contadores de Criados e Prontos)* |

---

## ✅ Justificativa e Resultados

### Decisões Técnicas

* A **Memória Compartilhada** foi escolhida para alta velocidade de comunicação, eliminando a dependência de I/O de arquivos ou banco de dados.
* A combinação de **Semaphore e Lock** garante a integridade dos dados, sendo essencial para a robustez do sistema em ambientes de multiprocessamento.
* O **JSON serializado** facilitou a passagem de estruturas de dados complexas (`list` de `dict`) para a área de memória bruta.

### Testes Realizados

Os testes confirmaram o comportamento esperado: a criação e alteração de status ocorrem de forma assíncrona, as cores na interface gráfica mudam corretamente, e os contadores são atualizados em tempo real, **sem a ocorrência de *deadlocks* ou condições de corrida**.

### Nota sobre o Auxílio de IA

A implementação da interface gráfica (Tkinter) e de funcionalidades visuais específicas, como a coloração dinâmica dos itens na `TreeView`, contou com o auxílio de ferramentas de Inteligência Artificial para a **descoberta de métodos e a forma correta de utilização** dessa biblioteca.

---

## 🎯 Conclusão

O projeto demonstra com sucesso a comunicação IPC utilizando memória compartilhada e sincronização em Python, oferecendo uma base funcional para sistemas de monitoramento e coordenação de tarefas distribuídas. O sistema é robusto e está aberto para expansão, como a inclusão de prioridades ou múltiplos processos de cada tipo.
