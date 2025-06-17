FROM python:3.13

ARG INSTALL_TEST_DEPENDENCIES=0

COPY . .

RUN if [ $INSTALL_TEST_DEPENDENCIES -eq 1 ]; then \
    pip install --no-cache -r ./requirements-test.txt; \
    fi

RUN pip install --no-cache -r ./requirements.txt

CMD ["fastapi", "run", "main.py", "--port", "80"]