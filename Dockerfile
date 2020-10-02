FROM continuumio/anaconda3:latest

ENV PROJ_LIB=/opt/conda/share/proj/ SRC=/usr/local/src/IceVarFigs

RUN apt-get update && \
    apt-get install -q -y \
    dvipng texlive texlive-fonts-recommended texlive-lang-cyrillic texlive-lang-english texlive-lang-european texlive-latex-extra

RUN mkdir -p $SRC

COPY requirements.txt $SRC

WORKDIR $SRC

RUN conda config --add channels conda-forge && \
    conda config --add channels esmvalgroup && \
    conda config --set channel_priority true && \
    conda install --file requirements.txt

RUN pip install python-i18n

ENTRYPOINT ["python"]