# 使用kunyoung92/cuda:10-7-devel18.04作為基礎映像檔
FROM kunyoung92/cuda:10-7-devel18.04

# 建立非特權用戶
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# 設定工作目錄
WORKDIR /app

# 複製當前目錄下的所有檔案到工作目錄
COPY . .

#RUN gpg --import DEB-GPG-KEY-NVIDIA-HPC-SDK
RUN apt-key add DEB-GPG-KEY-NVIDIA-HPC-SDK
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC

# 安裝Python 3.7.0
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.7 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1

# 安裝pipenv和其他Python套件
RUN apt-get install -y python3-pip && \
    python3 -m pip install pip==21.3.1 setuptools==59.6.0 && \
    pip3 install pipenv==2022.4.8


# 利用Docker的緩存和綁定安裝依賴項
#RUN --mount=type=cache,target=/root/.cache/pip

# 使用pipenv同步依賴項
RUN pipenv install

# 切換到非特權用戶運行應用程序
#USER appuser

# Expose the port that the application listens on.
EXPOSE 2701

# Run the application.
CMD python3
