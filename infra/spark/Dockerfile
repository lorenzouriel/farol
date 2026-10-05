FROM apache/spark:3.5.6-scala2.12-java17-python3-ubuntu

USER root

ARG MAVEN=https://repo1.maven.org/maven2
ARG ICEBERG=1.9.2
ARG NESSIE=0.104.2
ARG SPARK=3.5.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends gettext-base curl \
    && rm -rf /var/lib/apt/lists/* \
    && cd /opt/spark/jars \
    && curl -fsSLO ${MAVEN}/org/apache/spark/spark-connect_2.12/${SPARK}/spark-connect_2.12-${SPARK}.jar \
    && curl -fsSLO ${MAVEN}/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/${ICEBERG}/iceberg-spark-runtime-3.5_2.12-${ICEBERG}.jar \
    && curl -fsSLO ${MAVEN}/org/apache/iceberg/iceberg-aws-bundle/${ICEBERG}/iceberg-aws-bundle-${ICEBERG}.jar \
    && curl -fsSLO ${MAVEN}/org/projectnessie/nessie-integrations/nessie-spark-extensions-3.5_2.12/${NESSIE}/nessie-spark-extensions-3.5_2.12-${NESSIE}.jar

COPY spark-defaults.conf /opt/spark/conf/spark-defaults.conf.template
COPY entrypoint.sh /opt/lakehouse/entrypoint.sh
RUN chmod 0755 /opt/lakehouse/entrypoint.sh && chown -R spark:spark /opt/spark/conf

USER spark
EXPOSE 15002 4040
ENTRYPOINT ["/opt/lakehouse/entrypoint.sh"]
