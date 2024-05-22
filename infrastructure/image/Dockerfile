FROM python
ENV region=us-east-1
ENV secret_name=secret
RUN echo "The Default environment value for region variable is $region, and for the secret_name variable value is $secret_name"
ADD . /code
WORKDIR /code
RUN pip install pymysql cryptography
RUN pip install boto3

COPY rds.py /
CMD ["/bin/bash", "-c", "echo FIRST COMMAND;ls -ltr;python /rds.py"]
