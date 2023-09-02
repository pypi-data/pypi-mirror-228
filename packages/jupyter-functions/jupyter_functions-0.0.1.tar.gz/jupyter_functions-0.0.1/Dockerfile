# Copyright (c) Datalayer, Inc. https://datalayer.io
# Distributed under the terms of the MIT License.

FROM python:3.11

RUN mkdir /opt/jupyter-functions

WORKDIR /opt/jupyter-functions

RUN pip install kazoo

COPY jupyter_functions /opt/jupyter_functions
RUN pip install -e ./jupyter_functions

# COPY frontplane/dist.html /opt/jupyter-functions/index.html

WORKDIR /opt/jupyter-functions/editor

EXPOSE 9300

CMD ["python", "-m", "jupyter_functions"]
