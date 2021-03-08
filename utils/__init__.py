"""
data: dataframe com colunas Data, Vacinados e Delta
stdev_outlier: valor de desvios padrões a partir do qual um dado é outlier (default = 2)
"""
def wrangle_data(data, stdev_outlier=2):
    # Eliminando nulos e valores onde a diferença do anterior é menor que 0
    # por que as vezes o site do vacinometro reporta valores errados
    data = data.dropna()
    data = data.drop(data.query("Delta <= 0").index)
    """
    Vamos remover todas as entradas cuja a diferença
    da anterior (coluna delta) estiver acima de um certo número de
    desvios padrões da média (pelo mesmo motivo)
    usanmos a coluna delta pois é uma séire estacionária
    """
    std = data.Delta.std()
    mean = data.Delta.mean()
    data = data.drop(
        data.query(
            "Delta > @mean+@stdev_outlier*@std or Delta < @mean-@stdev_outlier*@std"
        ).index
    )
    # Para cada entrada, calcula em qual hora do ano ela foi computada (24*(dia_do_ano-1) + hora_do_dia)
    # Dia do ano - 1 por que o primeiro dia começa na hora 0
    data["HourOfYear"] = 24*(data.Data.dt.dayofyear-1) + data.Data.dt.hour
    # Agrupa registros q aconteceram dentro da mesma hora e soma todas as mudanças
    # e pega o máximo da coluna vacinados, já q o número de vacinados só cresce esse valor
    # reflete o número de vacinados total ao final daquela hora
    vacinados_hora = data.groupby("HourOfYear").max()["Vacinados"]
    return vacinados_hora
