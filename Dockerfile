FROM zerefdragoneel/cog-conda-cuda11-7-base
ENV PATH /opt/conda/envs/py38/bin:$PATH
ENV CONDA_DEFAULT_ENV py38
WORKDIR /app
COPY requirements.txt requirements.txt
COPY . .
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/opt/conda/envs/py38/x86_64-conda-linux-gnu/lib
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# RUN conda run --no-capture-output -n py38 python api.py
RUN echo $LD_LIBRARY_PATH
RUN export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/conda/envs/py38/x86_64-conda-linux-gnu/lib &&  conda run --no-capture-output -n py38 python -m pip install -r requirements.txt
RUN cp /opt/conda/envs/py38/lib/libstdc++.so.6.0.29 /usr/lib/x86_64-linux-gnu/libstdc++.so.6
EXPOSE 7777
ENTRYPOINT [ "/bin/bash", "-l", "-c" ]
CMD  ["conda run --no-capture-output -n py38 python async_server.py"]


# FROM zerefdragoneel/spritesheet-api:latest
# WORKDIR /app
# RUN cp /opt/conda/envs/py38/lib/libstdc++.so.6.0.29 /usr/lib/x86_64-linux-gnu/libstdc++.so.6
# ENTRYPOINT [ "/bin/bash", "-l", "-c" ]
# CMD  ["conda run --no-capture-output -n py38 python server.py"]