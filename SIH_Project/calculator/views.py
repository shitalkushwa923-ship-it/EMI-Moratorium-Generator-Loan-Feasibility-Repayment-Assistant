from django.shortcuts import render


def calculator(request):
    result = None
    schedule = []

    if request.method == "POST":

        # User inputs
        margin = float(request.POST.get("margin"))
        tenure_years = float(request.POST.get("tenure"))
        moratorium_months = int(request.POST.get("moratorium"))

        # Sample scheme rules
        margin_percent = 10
        loan_percent = 90
        annual_interest = 6.0

        # Maximum feasible project cost
        max_project_cost = margin / (margin_percent / 100)

        # Maximum eligible loan
        max_loan = max_project_cost * (loan_percent / 100)

        # Tenure calculation
        total_months = int(tenure_years * 12)
        repayment_months = total_months - moratorium_months

        # Number of quarterly installments
        n = repayment_months // 3

        # Quarterly interest rate
        r = annual_interest / (4 * 100)

        # Quarterly EMI
        if n <= 0:
            quarterly_installment = 0
        elif r == 0:
            quarterly_installment = max_loan / n
        else:
            quarterly_installment = (
                max_loan * r * (1 + r) ** n
                / ((1 + r) ** n - 1)
            )

        # Repayment schedule
        balance = max_loan

        for quarter in range(1, n + 1):

            opening_balance = balance

            interest = opening_balance * r

            principal = quarterly_installment - interest

            closing_balance = opening_balance - principal

            if closing_balance < 0:
                closing_balance = 0

            schedule.append({
                "quarter": quarter,
                "opening": opening_balance,
                "interest": interest,
                "principal": principal,
                "installment": quarterly_installment,
                "closing": closing_balance,
            })

            balance = closing_balance

               # Total calculations
        total_repayment = quarterly_installment * n
        total_interest = total_repayment - max_loan

       
 

        result = {
            "margin": margin,
            "max_project_cost": max_project_cost,
            "max_loan": max_loan,
            "scheme": "Concessional Enterprise Loan",
            "interest": annual_interest,
            "moratorium": moratorium_months,
            "tenure": tenure_years,
            "repayment_months": repayment_months,
            "quarters": n,
            "quarterly_installment": quarterly_installment,
            "total_interest": total_interest,
            "total_repayment": total_repayment,"quarterly_rate": r,
            "formula_n": n,
            "formula_loan": max_loan,
            
        }

    return render(
        request,
        "calculator/calculator.html",
        {
            "result": result,
            "schedule": schedule,
        }
    )
