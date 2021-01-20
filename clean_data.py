import pandas as pd
import getopt, sys

# Processa os parametros do script
# -f arquivo.csv indica qual arquivo processar
# -p prefixo indica o prefixo a usar
opts, args = getopt.getopt(sys.argv[1:], "f:p:d:")
# Transforma os parametros em um dicionário
arg_dict = {k:v for (k,v) in opts}

# Carrega o nome do arquivo a processar a partir do dicinário de paramêtros, valor padrão: vacinados.csv
data_file=arg_dict.get("-f", "vacinados.csv")
# Prefixo do arquivo com os dados limpos, valor padrão: clean
prefix = arg_dict.get("-p", "clean")
# Diretório onde salvar o arquivo, valor padrão: data
data_dir = arg_dict.get("-d", "data")

# Lê o arquivo com o pandas
data = pd.read_csv(data_file)
# Remove linhas cujo a data de atualização estão duplicadas
data = data.drop_duplicates("Data")
# Converte coluna de Data para formato DateTime
data.Data = data.Data.astype("datetime64[ns]")

# Salva com o nome "original_clean.csv"
data.to_csv(f"{data_dir}/{data_file.split('.')[0]}_{prefix}.csv", index=False)
