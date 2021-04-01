# Copyright © 2021 Markus W Mahlberg
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.
FROM python:3-alpine
# Unlikely to change, so we leverage caching
COPY _requirements.txt /tmp/
RUN pip install -r /tmp/_requirements.txt 
COPY app.py /usr/local/lib/app/
COPY templates/ /usr/local/lib/app/templates/
EXPOSE 8080
ENV APP_HOST=0.0.0.0
ENV APP_PORT=8080
ENV MINIO=localhost:9000
CMD ["python","/usr/local/lib/app/app.py"]