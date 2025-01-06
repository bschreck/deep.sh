
from python:3.11
RUN pip install --upgrade pip && pip install \
  prompt-toolkit==3.0.47 \
   \
  pygments
RUN mkdir /deepsh
WORKDIR /deepsh
ADD ./ ./
RUN python setup.py install
