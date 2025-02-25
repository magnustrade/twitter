# Stock Signal Scraper and Email Notifier

This project scrapes stock signal data from a configurable URL and sends daily email notifications with signals from the last 3 business days (excluding weekends) to multiple recipients in an HTML table format.

## Features
- **Data Scraping**: Fetches stock signals from a URL defined in `SCRAPE_URL` (GitHub Secrets).
- **Business Day Filter**: Includes signals only from the last 3 business days (Monday to Friday).
- **Dynamic Stock List**: Loads stock symbols from `data/stock.txt`.
- **Multiple Recipients**: Sends emails to multiple recipients specified in `TO_EMAIL`.
- **HTML Email**: Formats signals in a styled HTML table.
- **Error Handling**: Validates email addresses and handles file/secret errors.

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
