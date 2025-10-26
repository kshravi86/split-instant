# Top 10 Features of Splitwise

## 1. Easy Expense Tracking

**Explanation:** This is the core function, allowing users to quickly log shared expenses. It replaces the need for manual spreadsheets or keeping physical receipts.

**Diagram: Expense Entry Flow**
```
[User] --> [Add Expense Button]
  |
  v
[Enter Amount, Description, Group]
  |
  v
[Select Who Paid & Who Owes]
  |
  v
[Expense Logged & Balances Updated]
```

## 2. Group Creation

**Explanation:** Users can create dedicated groups for specific contexts (e.g., "Roommates," "Bali Trip 2025," "Family"). This keeps expenses organized and separate.

**Diagram: Group Structure**
```
[Group: Bali Trip]
  |
  +-- [Member: Alice]
  +-- [Member: Bob]
  +-- [Member: Charlie]
  +-- [Expense Log]
```

## 3. Flexible Bill Splitting

**Explanation:** Splitwise offers various ways to divide a bill beyond just splitting equally. Options include splitting by exact amounts, percentages, or shares (e.g., one person pays double).

**Diagram: Splitting Options**
```
$100 Dinner Bill
  |
  +-- Equal Split: $33.33 each (Alice, Bob, Charlie)
  +-- Percentage Split: 50% (Alice), 25% (Bob), 25% (Charlie)
  +-- Shares Split: 2 Shares (Alice), 1 Share (Bob), 1 Share (Charlie)
```

## 4. Debt Simplification

**Explanation:** The app uses an algorithm to minimize the total number of transactions required to settle all debts within a group. Instead of A paying B, B paying C, and C paying A, it might suggest A pays C directly.

**Diagram: Simplification Example**
```
Before Simplification:
Alice owes Bob $20
Bob owes Charlie $10

After Simplification:
Alice pays Bob $10
Alice pays Charlie $10 (Bob is removed as an intermediary)
```

## 5. Multi-Currency Support

**Explanation:** This feature allows users to log expenses in different currencies, which is essential for international travel. The app handles the conversion and maintains balances in a base currency.

**Diagram: Currency Conversion**
```
[Expense: 100 EUR] -> [Conversion Rate] -> [Base Currency: 110 USD]
```

## 6. Payment Integrations

**Explanation:** Splitwise integrates with popular payment platforms (like Venmo, PayPal) to make settling balances easy. Users can initiate a payment directly from the app.

**Diagram: Payment Flow**
```
[User sees "Bob owes Alice $50"]
  |
  v
[Click "Settle Up"]
  |
  v
[Select Payment Method: Venmo/PayPal]
  |
  v
[Redirect to Payment App]
```

## 7. Offline Entry

**Explanation:** Users can add expenses even without an internet connection. The data is stored locally and automatically syncs to the cloud once the device reconnects.

**Diagram: Sync Process**
```
[Device Offline] -> [Expense Added Locally]
  |
  v (Internet Reconnects)
[Local Data] <--> [Splitwise Server]
```

## 8. Notifications and Activity Feed

**Explanation:** The app keeps all group members updated with real-time notifications about new expenses, payments, edits, and reminders, ensuring transparency.

**Diagram: Activity Feed Snippet**
```
[Activity Feed]
- Alice added "Dinner" ($50)
- Bob paid Charlie $25
- Charlie edited "Groceries"
```

## 9. Recurring Expenses

**Explanation:** For regular shared costs like rent, utilities, or subscriptions, users can set up recurring expenses that are automatically added at specified intervals (e.g., monthly).

**Diagram: Recurring Setup**
```
[Expense: Rent $1000]
  |
  v
[Frequency: Monthly]
  |
  v
[Start Date: Oct 1]
  |
  v
[Auto-added on 1st of every month]
```

## 10. Expense Categorization

**Explanation:** Every expense can be assigned a category (e.g., Food, Travel, Housing). This helps users analyze their spending patterns and generate reports.

**Diagram: Category Breakdown**
```
[Total Spending: $500]
  |
  +-- Food: $200 (40%)
  +-- Travel: $150 (30%)
  +-- Housing: $100 (20%)
  +-- Other: $50 (10%)
```
