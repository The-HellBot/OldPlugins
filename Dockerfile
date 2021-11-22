FROM teamvaders/hellbot:latest

RUN git clone https://github.com/HellBoy-OP/Plugins.git /root/hellbot

WORKDIR /root/hellbot

RUN pip3 install -U -r requirements.txt

ENV PATH="/home/hellbot/bin:$PATH"

CMD ["python3", "-m", "hellbot"]
