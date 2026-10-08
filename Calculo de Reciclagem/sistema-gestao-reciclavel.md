# Sistema de Gestão Reciclável

Construir uma interface de linha de comando (CLI) interativa é o passo fundamental para transformar um modelo matemático abstrato em uma **ferramenta de trabalho real e utilitária** para os operadores da cooperativa.

Para garantir que o programa seja amigável, seguro e imune a erros de digitação (como um operador digitar letras onde deveriam entrar números), implementaremos **funções auxiliares com tratamento de exceções (`try-except`)** para validação contínua da entrada de dados.

---

### 🛠️ 1. Solução em Código (Python)

```python
class CooperativaReciclagem:
    """Modela e automatiza os cálculos de eficiência de reciclagem da cooperativa."""

    def __init__(
        self,
        lixo_domiciliar_aterro: float,
        caminhoes_aterro: int,
        outros_residuos_aterro: float = 0.0,
        caminhoes_cooperativa_dia: int = 3,
        dias_uteis: int = 5,
        coleta_seletiva_semanal: float = 0.0,
        total_vendas_reciclados: float = 0.0,
    ) -> None:
        """Inicializa os parâmetros operacionais com validação defensiva."""
        if lixo_domiciliar_aterro < 0 or outros_residuos_aterro < 0:
            raise ValueError("Valores de entrada de lixo não podem ser negativos.")
        if caminhoes_aterro <= 0:
            raise ValueError("O total de caminhões no aterro deve ser maior que zero.")
        if caminhoes_cooperativa_dia < 0 or dias_uteis < 0:
            raise ValueError("Dias e caminhões por dia não podem ser negativos.")
        if coleta_seletiva_semanal < 0 or total_vendas_reciclados < 0:
            raise ValueError("Valores de vendas e coleta seletiva não podem ser negativos.")

        self.lixo_domiciliar_aterro = lixo_domiciliar_aterro
        self.caminhoes_aterro = caminhoes_aterro
        self.outros_residuos_aterro = outros_residuos_aterro
        self.caminhoes_cooperativa_dia = caminhoes_cooperativa_dia
        self.dias_uteis = dias_uteis
        self.coleta_seletiva_semanal = coleta_seletiva_semanal
        self.total_vendas_reciclados = total_vendas_reciclados

    def calcular_peso_medio_caminhao(self) -> float:
        """Calcula o peso médio estimado por caminhão que entra no aterro."""
        total_lixo = self.lixo_domiciliar_aterro + self.outros_residuos_aterro
        return total_lixo / self.caminhoes_aterro

    def calcular_descarregamento_cooperativa(self) -> float:
        """Calcula o volume médio descarregado semanalmente na cooperativa."""
        peso_medio = self.calcular_peso_medio_caminhao()
        total_caminhoes_coop = self.caminhoes_cooperativa_dia * self.dias_uteis
        return total_caminhoes_coop * peso_medio

    def calcular_porcentagens_reciclagem(self) -> tuple[float, float]:
        """Calcula as razões percentuais de reciclagem domiciliar e total."""
        descarregamento_coop = self.calcular_descarregamento_cooperativa()
        if descarregamento_coop == 0.0:
            raise ZeroDivisionError("O descarregamento na cooperativa resultou em zero.")

        reciclado_domiciliar = self.total_vendas_reciclados - self.coleta_seletiva_semanal
        razao_domiciliar = (reciclado_domiciliar / descarregamento_coop) * 100
        razao_total = (self.total_vendas_reciclados / descarregamento_coop) * 100

        return razao_domiciliar, razao_total


def obter_numero_valido(
    mensagem_prompt: str, tipo: type = float, valor_padrao: float | None = None
) -> float | int:
    """Solicita a entrada do usuário repetidamente até obter um valor numérico válido.

    Args:
        mensagem_prompt (str): O texto explicativo para o usuário.
        tipo (type): O tipo de dado esperado (int ou float).
        valor_padrao (float | int | None): Valor assumido se o usuário apenas pressionar Enter.

    Returns:
        float | int: O número digitado e validado.
    """
    while True:
        entrada = input(mensagem_prompt).strip()

        # Se o usuário não digitar nada e houver valor padrão disponível
        if entrada == "" and valor_padrao is not None:
            return valor_padrao

        try:
            valor = tipo(entrada.replace(",", "."))  # Permite o uso de vírgula decimal
            if valor < 0:
                print("   ⚠️  [Erro]: O valor não pode ser negativo. Tente novamente.")
                continue
            return valor
        except ValueError:
            print(f"   ⚠️  [Erro de Entrada]: Digite um número {tipo.__name__} válido!")


def executar_sistema_interativo() -> None:
    """Conduz a interface interativa de coleta de dados e exibição de relatórios."""
    print("=" * 65)
    print(" ♻️   SISTEMA DE AUTOMAÇÃO E DIAGNÓSTICO DA COOPERATIVA (COOTERAT) ")
    print("=" * 65)

    while True:
        print("\n--- 📋 INSIRA OS DADOS DA SEMANA ---")

        lixo_domiciliar = obter_numero_valido("► Lixo domiciliar no Aterro (kg): ")
        outros_residuos = obter_numero_valido(
            "► Outros resíduos no Aterro (kg) [Pressione Enter para 0]: ", valor_padrao=0.0
        )
        total_caminhoes = obter_numero_valido(
            "► Total de caminhões que entraram no Aterro: ", tipo=int
        )
        caminhoes_dia = obter_numero_valido(
            "► Caminhões descarregados/dia na Cooperativa [Padrão: 3]: ", tipo=int, valor_padrao=3
        )
        dias_uteis = obter_numero_valido(
            "► Dias úteis trabalhados na semana [Padrão: 5]: ", tipo=int, valor_padrao=5
        )
        coleta_seletiva = obter_numero_valido("► Entrada de Coleta Seletiva na Cooperativa (kg): ")
        vendas_totais = obter_numero_valido("► Total de resíduos reciclados vendidos na semana (kg): ")

        try:
            cooperativa = CooperativaReciclagem(
                lixo_domiciliar_aterro=lixo_domiciliar,
                caminhoes_aterro=total_caminhoes,
                outros_residuos_aterro=outros_residuos,
                caminhoes_cooperativa_dia=caminhoes_dia,
                dias_uteis=dias_uteis,
                coleta_seletiva_semanal=coleta_seletiva,
                total_vendas_reciclados=vendas_totais,
            )

            peso_medio = cooperativa.calcular_peso_medio_caminhao()
            descarregamento = cooperativa.calcular_descarregamento_cooperativa()
            raz_dom, raz_tot = cooperativa.calcular_porcentagens_reciclagem()

            print("\n" + "=" * 65)
            print(" 📊 RELATÓRIO DE DESEMPENHO SEMANAL DA RECICLAGEM")
            print("=" * 65)
            print(f" Média de peso por caminhão:         {peso_medio:>12.2f} kg/caminhão")
            print(f" Descarregamento semanal na Coop.:  {descarregamento:>12.2f} kg")
            print(f" Resíduos Reciclados Domiciliares:  {(vendas_totais - coleta_seletiva):>12.2f} kg")
            print(f" Resíduos de Coleta Seletiva:       {coleta_seletiva:>12.2f} kg")
            print("-" * 65)
            print(f" 🟢 Razão Reciclado / Lixo Domiciliar:  {raz_dom:>10.2f} %")
            print(f" 🔵 Razão Reciclado / Lixo Total:       {raz_tot:>10.2f} %")
            print("=" * 65)

        except (ValueError, ZeroDivisionError) as erro:
            print(f"\n❌ Erro no processamento dos cálculos: {erro}")

        opcao = input("\n🔄 Deseja calcular outra semana? (S/N): ").strip().lower()
        if opcao != "s":
            print("\nEncerrando o programa. Bom trabalho na cooperativa! 🌿")
            break


# Ponto de entrada do script
if __name__ == "__main__":
    executar_sistema_interativo()
```

---

### 🧠 2. Explicação Didática (Anatomia do Código)

* **Analogia Estruturada (O Inspecionador de Catraca):** Imagine uma catraca automatizada na entrada da cooperativa. Se uma pessoa tentar passar um bilhete amassado ou rasgado (dados incorretos, como letras em campos numéricos), a catraca não quebra; ela simplesmente emite um sinal sonoro, recusa a passagem e solicita que a pessoa insira um bilhete válido. A nossa função `obter_numero_valido` atua exatamente como essa catraca de segurança inteligente.
* **Passo a Passo do Fluxo de Execução Interativo:**
  1. **Captura com `input()`:** O comando `input()` pausa a execução do programa e aguarda o operador digitar um texto.
  2. **Tratamento de Strings (`replace` e `strip`):** O operador brasileiro costuma usar vírgulas para decimais (ex: 14210,5). Substituímos a vírgula por ponto (`.replace(',', '.')`) para ser aceito pelo padrão computacional.
  3. **Bloco `try-except` Repetitivo:** Tentamos converter a string tratada usando `float()` ou `int()`. Se o operador digitar letras, o Python dispara uma exceção `ValueError`. Em vez de travar o programa, capturamos o erro e repetimos o prompt dentro do loop `while True`.
  4. **Valores Padrão (Teclado Rápido):** Para acelerar a rotina, adicionamos suporte a valores padrão (ex: pressionar Enter para assumir 5 dias úteis ou 0 kg em outros resíduos).
  5. **Exibição Formatada de Resultados:** Usamos *f-strings* avançadas com formatação como `{peso_medio:>12.2f}`. Isso alinha todos os números à direita ocupando 12 espaços com 2 casas decimais, criando uma tabela profissional limpa no terminal.

---

### 🚀 3. Exemplo de Uso Prático

Abaixo está uma simulação real de como o operador visualizará e interagirá com o console no terminal:

```text
=================================================================
 ♻️   SISTEMA DE AUTOMAÇÃO E DIAGNÓSTICO DA COOPERATIVA (COOTERAT)
=================================================================

--- 📋 INSIRA OS DADOS DA SEMANA ---
► Lixo domiciliar no Aterro (kg): 454400
► Outros resíduos no Aterro (kg) [Pressione Enter para 0]: 6970
► Total de caminhões que entraram no Aterro: 68
► Caminhões descarregados/dia na Cooperativa [Padrão: 3]: 3
► Dias úteis trabalhados na semana [Padrão: 5]: 5
► Entrada de Coleta Seletiva na Cooperativa (kg): 4590
► Total de resíduos reciclados vendidos na semana (kg): 14210

=================================================================
 📊 RELATÓRIO DE DESEMPENHO SEMANAL DA RECICLAGEM
=================================================================
 Média de peso por caminhão:              6784.85 kg/caminhão
 Descarregamento semanal na Coop.:      101772.79 kg
 Resíduos Reciclados Domiciliares:        9620.00 kg
 Resíduos de Coleta Seletiva:             4590.00 kg
-----------------------------------------------------------------
 🟢 Razão Reciclado / Lixo Domiciliar:        9.45 %
 🔵 Razão Reciclado / Lixo Total:            13.96 %
=================================================================

🔄 Deseja calcular outra semana? (S/N): n

Encerrando o programa. Bom trabalho na cooperativa! 🌿
```

---

### 📝 4. Desafio Prático (Fixação)

Para exercitar a modificação de software e controle de fluxo interativo:

> **O Desafio:** Como você adicionaria uma opção no relatório final para **salvar automaticamente os resultados formatados em um arquivo de texto de histórico (`relatorio_semanal.txt`)** usando o modo de anexação (`"a"`) do Python, garantindo que os dados das semanas anteriores não sejam apagados?
>
> *Dica pedagógica:* Lembre-se do uso do gerenciador de contexto `with open("relatorio_semanal.txt", "a", encoding="utf-8") as arquivo:`.

---

💡 **Próximo Passo:** Se desejar, podemos criar uma rotina para exportar esses históricos para uma planilha em Excel (`.xlsx`) com gráficos automáticos da evolução da taxa de reciclagem semana a semana!
