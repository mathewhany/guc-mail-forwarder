# Microservices GUC Mail Scrapper

This project is a backend system built to practice and learn more about Microservices, Kafka, Redis, and Scalable Distributed Systems. The main goal is to forward mails sent to a GUC email to a Gmail account, consolidating all emails in one place.

## Technologies Used

- Python: Used for building the microservices, leveraging the Beautiful Soup library for web scraping.
- Microservices: The system is divided into three microservices: mail-authenticator, mail-poller, and mail-forwarder.
- Kafka: Used as a messaging system to pass mail IDs between microservices.
- Redis: Used to keep track of forwarded mails and avoid duplication.
- Kubernetes: Intended for deployment (later on)

## Project Structure

- `mail-authenticator`: Retrieves cookies for logging into the mail website.
- `mail-poller`: Runs periodically (using a cron job) to check the GUC mail website for new mails. It adds the IDs of these mails to a Kafka topic and a Redis set to track forwarded mails.
- `mail-forwarder`: Consumes mail IDs produced by the mail-poller and forwards the corresponding mails using the existing forward button in Outlook.

## Why Kafka and Microservices?

While Kafka, Microservices, and other technologies may seem like overkill for such a simple system, the purpose of this project is to practice and apply these concepts in a practical and useful manner. By building a real-world project, you can gain hands-on experience and deepen your understanding of these topics.

## Getting Started

# Running locally

1. Clone the repository: `git clone https://github.com/mathewhany/guc-mail-forwarder.git`
2. Configure the necessary environment variables by adding `.env` file in the root directory. You can use the `.env.example` file as a template.
3. Run using Docker Compose: `docker-compose up -d`
