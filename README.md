# Expense Tracker

## Required Features
1. User must be able to enter an Expense
2. Data captured for each expense are
* Expenditure name (e.g. "Pay for bills" or "Bought grocery")
* Date of Expenditure
* Type (debit or credit)
* Checkbox for whether it is reconciled

3. Use a normal form to create an expenditure. Set its reconciled to false

4. Use a route to display all expenditures. Use a checkbox to show if an expenditure is reconciled

5. Allow the user to check on the checkbox to reconcile the expenditure using AJAX

6. Display relevant alerts (for example, when creating an expenditure)

7. Display toastr when using AJAX to modify the reconcile

# Find all transactions reconciled
In mongo
```
db.expenses.find({
    'reconciled': true
})
```