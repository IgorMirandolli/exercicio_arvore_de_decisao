# Exercício: ID3 com a coluna Salario

Este exercício adiciona a coluna `Salario` ao conjunto de dados original e
recalcula a árvore de decisão usando entropia, que é o critério associado ao
algoritmo ID3.

## Como executar

No Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python exercicio_id3_salario.py
```

No Linux:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python exercicio_id3_salario.py
```

## Resultado esperado

Com os dados usados no script, os ganhos de informação são:

```text
NivelSatisfacao: 0.4591
NumeroProjetos: 0.4591
Salario: 0.9183
```

Assim, o atributo escolhido na raiz da árvore é `Salario`.

## Reflexão

Sim, nesta tabela o salário foi mais importante que a satisfação para o
algoritmo.

Isso aconteceu porque `Salario` separou perfeitamente os exemplos de treino:
todos os funcionários com `Salario = Baixo` saíram, enquanto todos os
funcionários com `Salario = Alto` não saíram. Depois dessa pergunta, a entropia
dos grupos fica igual a zero.

Já `NivelSatisfacao` ainda deixa mistura em um dos grupos. Entre os funcionários
com satisfação baixa, existem dois casos de saída e um caso de permanência. Por
isso a desordem não desaparece completamente, e o ganho de informação fica
menor.

Em outras palavras, o ID3 não entende causalidade. Ele apenas procura a pergunta
que mais reduz a incerteza naquele conjunto de dados. Se a tabela diz que o
salário separa melhor os casos, o algoritmo vai tratar `Salario` como a melhor
variável, mesmo que em uma empresa real a decisão de sair também dependa de
cultura, liderança, carreira, saúde, mercado e outros fatores que não aparecem
no conjunto de treino.
