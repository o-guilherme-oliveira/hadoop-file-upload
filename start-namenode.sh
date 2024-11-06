#!/bin/bash
# Script para configurar permissões e iniciar o NameNode

# Inicia o Hadoop usando o entrypoint padrão
/entrypoint.sh /run.sh

# Configura o diretório /uploads no HDFS com as permissões apropriadas
hdfs dfs -mkdir -p /uploads
hdfs dfs -chown hadoop_user /uploads
hdfs dfs -chmod 770 /uploads

# Mantém o contêiner em execução
tail -f /dev/null
