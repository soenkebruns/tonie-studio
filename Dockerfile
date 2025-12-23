# Dockerfile for tonie-podcast-sync
# Provides ffmpeg for audio conversion to Tonie format

FROM alpine:latest

# Install ffmpeg
RUN apk add --no-cache ffmpeg

# Set working directory
WORKDIR /data

# Default command shows ffmpeg version
CMD ["ffmpeg", "-version"]
