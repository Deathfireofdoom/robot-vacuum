# First stage: Rust build environment
FROM rust:1.63 as rust-build

WORKDIR /usr/src/rust-implementation
COPY rust-implementation/ .

RUN cargo build --release

# Second stage: Python environment
FROM python:3.11

WORKDIR /usr/src/app

# Copy the compiled Rust shared library from the first stage
COPY --from=rust-build /usr/src/rust-implementation/target/release/librust_memory.so /usr/src/app/rust/rust_memory.so

WORKDIR /usr/src/app

COPY src/ ./src/
COPY app.py .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

EXPOSE 5000

CMD ["flask", "run"]