import re


class UniversalParser:
    def __init__(self):
        self.lexicon = {
            "total_amount_due": [
                "total amount due",
                "amount due",
                "new balance",
                "total outstanding",
                "closing balance",
                "current balance"
            ],
            "minimum_due": [
                "minimum amount",
                "minimum due",
                "min amount",
                "mad"
            ],
            "credit_limit": [
                "credit limit",
                "total credit limit",
                "credit line"
            ],
            "interest": [
                "interest",
                "finance charge",
                "finance charges",
                "finance fee",
                "interest charged"
            ]
        }

    # --------------------------------------------------
    # NORMALIZE OCR / PDF TEXT
    # --------------------------------------------------
    def normalize_text(self, text):
        text = text.lower()

        # remove junk but keep numbers, dates
        text = re.sub(r'[^a-z0-9\s\.,:/\-]', ' ', text)

        # fix OCR broken numbers: "24 ,560 .75" → "24,560.75"
        text = re.sub(r'\s*,\s*', ',', text)
        text = re.sub(r'\s*\.\s*', '.', text)

        # collapse spaces
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    # --------------------------------------------------
    # EXTRACT AMOUNT NEAR LABEL (OCR SAFE)
    # --------------------------------------------------
    def extract_amount_near_label(self, text, labels):
        for label in labels:
            idx = text.find(label)
            if idx != -1:
                # large context window (OCR breaks layout)
                context = text[idx: idx + 250]

                match = re.search(r'(\d[\d,]*\.?\d*)', context)
                if match:
                    try:
                        return float(match.group(1).replace(',', ''))
                    except:
                        pass
        return None
    
    def fallback_minimum_due(self, text, result):
     if result["minimum_due"] is not None:
        return result

    # Only try if minimum-related words exist
     if not any(word in text for word in ["minimum", "min", "mad"]):
        return result

     nums = re.findall(r'\d{1,3}(?:,\d{3})*(?:\.\d{2})', text)
     nums = [float(n.replace(',', '')) for n in nums]

     if not nums:
        return result

     total_due = result.get("total_amount_due")

    # Filter candidates:
    # - > 50 (minimum due is never ₹1 or ₹2)
    # - < total amount due
     candidates = []
     for n in nums:
        if n >= 50:
            if total_due is None or n < total_due:
                candidates.append(n)

     if candidates:
        # minimum due is the smallest reasonable candidate
        result["minimum_due"] = min(candidates)

     return result


    # --------------------------------------------------
    # EXTRACT DUE DATE
    # --------------------------------------------------
    def extract_due_date(self, text):
        patterns = [
            r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
            r'\d{1,2}[-/](?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[-/]\d{2,4}'
        ]

        for p in patterns:
            m = re.search(p, text)
            if m:
                return m.group(0).title()

        return None

    # --------------------------------------------------
    # DETECT INTEREST
    # --------------------------------------------------
    def detect_interest(self, text):
        if "no interest" in text or "interest free" in text:
            return False

        return any(word in text for word in self.lexicon["interest"])

    # --------------------------------------------------
    # FALLBACK: NO LABELS (AXIS / AIRTEL STYLE)
    # --------------------------------------------------
    def fallback_from_numbers(self, text, result):
        nums = re.findall(r'\d{1,3}(?:,\d{3})*(?:\.\d{2})', text)
        nums = [float(n.replace(',', '')) for n in nums]

        if not nums:
            return result

        # Heuristic rules
        if result["total_amount_due"] is None:
            result["total_amount_due"] = nums[0]

        if result["credit_limit"] is None:
            result["credit_limit"] = max(nums)

        return result

    # --------------------------------------------------
    # MAIN PARSE FUNCTION (ONLY 5 FIELDS)
    # --------------------------------------------------
    def parse(self, raw_text):
        text = self.normalize_text(raw_text)

        result = {
            "total_amount_due": self.extract_amount_near_label(
                text, self.lexicon["total_amount_due"]
            ),
            "minimum_due": self.extract_amount_near_label(
                text, self.lexicon["minimum_due"]
            ),
            "due_date": self.extract_due_date(text),
            "interest_charged": self.detect_interest(text),
            "credit_limit": self.extract_amount_near_label(
                text, self.lexicon["credit_limit"]
            )
        }

        # fallback for unlabeled summaries
        result = self.fallback_from_numbers(text, result)
        result = self.fallback_minimum_due(text, result)


        return result
