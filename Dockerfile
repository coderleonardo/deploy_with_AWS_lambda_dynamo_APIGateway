FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt  ./

RUN  pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY linear_model.bin ${LAMBDA_TASK_ROOT}
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler 
CMD [ "lambda_function.lambda_handler" ] 

# To build the image run: docker build -t aws-example .
# To start the docker image if needed: docker run -p 9000:8000 aws-example