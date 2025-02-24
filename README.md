# Stock Signal Scraper and Email Notifier

This project scrapes stock signal data from a specified website and sends daily email notifications with signals from the last 3 business days (excluding weekends) to multiple recipients.

## Features
- **Data Scraping**: Fetches stock signals from `https://www.matematikrehberim.com/dipavcisi/agresifhissesignal.php`.
- **Business Day Filter**: Filters signals to include only the last 3 business days (Monday to Friday), excluding Saturdays and Sundays.
- **Multiple Recipients**: Sends emails to multiple recipients specified in the `TO_EMAIL` environment variable.
- **Error Handling**: Validates email addresses and skips invalid ones, ensuring robust email delivery.

## Prerequisites
- Python 3.11+
- Required Python packages:
  - `requests`
  - `beautifulsoup4`
- A Gmail account with an **App Password** (if using Gmail SMTP).

## Setup
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

The charts shared here are notes to myself and are definitely not investment advice.📍
