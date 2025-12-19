# Credit Card Statement Parser (OCR-Aware)

## Overview

This project is a credit card statement parser designed to extract **key summary information** from both **normal PDFs** and **scanned PDFs**.

In the real world, bank statements are often inconsistent:

* some are clean text PDFs
* some are scanned images
* some lose structure during OCR

This system is built to handle that reality safely and predictably.

---

## What the parser extracts

The parser extracts **only 5 essential fields**:

* Total Amount Due
* Minimum Amount Due
* Payment Due Date
* Whether Interest Was Charged
* Credit Limit

The output is always structured and deterministic.
If a value cannot be reliably identified, it is returned as `null`.

---

## Design philosophy

This project prioritizes **correctness over guessing**.

Key principles:

* The parser works purely on text
* OCR is only a fallback to obtain text when PDFs are image-based
* Context-based extraction is used instead of rigid regex
* If data is not confidently present, it is not inferred

This mirrors how real fintech systems handle imperfect documents.

---

## How the system works (conceptually)

1. The system checks whether the PDF contains selectable text
2. If text exists, it is extracted directly
3. If not, OCR is applied to extract text from images
4. The extracted text is normalized to handle OCR noise
5. The parser extracts financial values using labels and safe heuristics

The parser logic remains the same regardless of where the text comes from.

---

## OCR behavior

OCR is automatically triggered only when required.

Because OCR accuracy depends on document quality:

* If readable text is extracted, values are parsed normally
* If OCR fails to capture reliable information, the system returns `null` values instead of guessing

This is intentional and ensures financial correctness.

---

## About Minimum Amount Due

Some credit card statements display the minimum amount due only as a **visual table value**, without a textual label.

In such cases:

* OCR may not preserve the label
* The parser cannot reliably identify the value

When this happens, the system **returns `null`** for minimum due.
This is a deliberate design decision to avoid incorrect financial data.

---

## Output example

A typical output looks like:

* total_amount_due: 4221.64
* minimum_due: null
* due_date: 16/11/2023
* interest_charged: true
* credit_limit: 39000.0

Returning `null` indicates missing or unreliable information, not a system error.

---

## Why this approach

Financial systems must be:

* explainable
* deterministic
* safe

Guessing values is worse than returning no value.
This project demonstrates **engineering judgment**, not brute-force extraction.

---

## Limitations

* The project focuses only on summary-level credit card data
* Transaction-level parsing is out of scope
* OCR accuracy depends on input quality

These limitations are intentional and documented.

---

## Future improvements

* Region-based OCR for summary sections
* Confidence scoring for extracted values
* Support for additional bank-specific layouts

---

## Final note

This project was built to reflect **real-world fintech constraints**, not idealized documents.

It demonstrates:

* practical problem-solving
* handling of noisy data
* safe failure modes
* clear design reasoning

---
