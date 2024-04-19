# Use an official minimal Miniconda image as a parent image
FROM continuumio/miniconda3:latest

# Set the working directory
WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y git redis-server

# Clone the repository on build (you can change this to clone on run, if preferred)
RUN git clone https://github.com/devbrones/magisim.git
# Set up the Conda environment
RUN conda env create -f /app/magisim/environment.yml
# Make RUN commands use the new environment:
RUN echo "conda activate myenv" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]
# Copy the startup script into the container
RUN chmod +x /app/magisim/src/ui/start-docker.sh
# Set up Redis to run automatically
#RUN sed -i 's/supervised no/supervised systemd/' /etc/redis/redis.conf
#RUN systemctl enable redis-server

# Expose the port Redis listens on
EXPOSE 6379
# Expose the port our gradio app listens on
EXPOSE 8000
WORKDIR /app/magisim/src/ui
# Run the initialization script when the container launches
CMD ["sh", "start-docker.sh"]
