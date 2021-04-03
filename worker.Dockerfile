FROM rq-worker

RUN echo "worker build started"

CMD ["python3", "main.py"]
RUN echo "worker build succeded"