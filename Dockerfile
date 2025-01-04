ARG PYTHON_VERSION=3.12
#
# Build poetry and export compiled dependecines as plain requirements.txt
#
FROM python:${PYTHON_VERSION}-slim-bookworm AS deps-compile

WORKDIR /
COPY poetry.lock pyproject.toml /

# Version is taken from poetry.lock, assuming it is generated with up-to-date version of poetry
RUN pip install --no-cache-dir poetry==$(cat poetry.lock |head -n1|awk -v FS='(Poetry |and)' '{print $2}')
RUN poetry export --format=requirements.txt > requirements.txt


FROM python:${PYTHON_VERSION}-slim-bookworm


RUN apt-get update && apt-get install -y --no-install-recommends adb dumb-init

COPY --from=deps-compile /requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /nonexistent && chown nobody:nogroup /nonexistent

VOLUME /nonexistent/.android

WORKDIR /src
COPY adb_prometheus_exporter /src/adb_prometheus_exporter

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
USER nobody
CMD ["python", "-m", "adb_prometheus_exporter.exporter"]
