FROM bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8

# Configuração de variáveis de ambiente necessárias
ENV CLUSTER_NAME=hadoop-cluster

# Configuração do HDFS
RUN echo "export CLUSTER_NAME=${CLUSTER_NAME}" >> ~/.bashrc

# Exponha a porta para o HDFS
EXPOSE 9870 9000

# Inicie o Hadoop
CMD ["sh", "-c", "service ssh start; hdfs namenode -format; start-dfs.sh && tail -f /dev/null"]
