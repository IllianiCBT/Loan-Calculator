from math import ceil  # how many imports from single module before just importing module?
from math import floor
from math import log
from math import pow
from sys import argv
import argparse


# gather initial input from user, via terminal.
# check input to ensure it meets correct parameters
def check_initial_input():
    parser = argparse.ArgumentParser(description='Loan calculator')
    parser.add_argument('-t', '--type', metavar='', help='Specify type of loan: diff or annuity')
    parser.add_argument('-v', '--principal', type=float, metavar='', help='Value of loan principal')
    parser.add_argument('-m', '--periods', type=int, metavar='', help='Loan duration, in months')
    parser.add_argument('-i', '--interest', type=float, metavar='', help='Monthly interest')
    parser.add_argument('-p', '--payments', type=float, metavar='', help='Value of each payment made. Annuity only')
    args = parser.parse_args()

    if len(argv) < 5:
        print("Incorrect parameters: fewer than 4 arguments filled")
        print(len(argv))
        print(argv)
        quit()

    if args.type is None:  # I'd prefer to just make this a required argument
        print("Incorrect parameters: no type")
        quit()

    if args.principal is not None:
        if args.principal < 0:
            print("Incorrect parameters: negative principal")
            quit()

    if args.periods is not None:
        if args.periods < 0:
            print("Incorrect parameters: negative periods")
            quit()

    if args.interest is None or args.interest < 0:
        print("Incorrect parameters: missing or negative interest")
        quit()

    if args.payments is not None:
        if args.payments < 0:
            print("Incorrect parameters: negative payments")
            quit()

    if args.type == "diff":
        if args.payments is not None:
            print("Incorrect parameters: diff/payments illegal combo")
            quit()

    return args.type, args.interest, args.payments, args.periods, args.principal


# calculate length of differential loan
def diff_calculator(principal, interest, periods):
    month = 0  # counter
    total_paid = 0

    nominal_interest = (interest / 100) / 12

    while month < periods:
        month += 1

        diff = ceil(principal / periods + nominal_interest * (principal - (principal * (month - 1)) / periods))
        total_paid += diff

        print(f"Month {month}: payment is {diff}")

    print(f"\nOverpayment = {int(total_paid - principal)}")


# establish correct syntax for feedback to user
def syntax(months):
    # calculate years and establish syntax
    if months > 12:
        years = floor(months / 12)
        months -= years * 12
        if years == 1:
            years_syntax = f' {years} year'
        else:
            years_syntax = f' {years} years'
    else:
        years = 0
        years_syntax = " "

    # calculate remaining months and establish syntax
    if months == 0:
        months_syntax = ""
    elif months == 1:
        months_syntax = f'{months} month'
    else:
        months_syntax = f'{months} months'

    # determine whether conjunctions are required
    if months > 0 and years > 0:
        conjunction = " and "
    else:
        conjunction = ""

    return years_syntax, conjunction, months_syntax


# if principal, monthly payments & interest known; calculate loan duration
def duration_calculator(principal, payments, interest):
    nominal_interest = (interest / 100) / 12

    # calculate the number of months needed to complete the loan
    month_calc = ceil(log((payments / (payments - nominal_interest * principal)), 1 + nominal_interest))

    # determine the correct syntax to feedback to the user
    years, conjunction, months = syntax(month_calc)

    # print repayment statement
    print(f'It will take{years}{conjunction}{months} to repay this loan!')

    overpayment = payments * month_calc - principal
    print(f"\nOverpayment = {overpayment}")


# if principal, periods & interest known; calculate monthly payments
def payments_calculator(principal, periods, interest):
    nominal_interest = (interest / 100) / 12

    upper_calculation = nominal_interest * pow((nominal_interest + 1), periods)
    lower_calculation = pow((nominal_interest + 1), periods) - 1
    annuity_payment = ceil(principal * (upper_calculation / lower_calculation))

    print(f'Your monthly payment = {annuity_payment}!')

    overpayment = annuity_payment * periods - principal
    print(f"\nOverpayment = {overpayment}")


# if monthly payments, periods & interest known; calculate loan principle
def principal_calculator(payments, periods, interest):
    nominal_interest = (interest / 100) / 12

    upper_calculation = nominal_interest * pow((1 + nominal_interest), periods)
    lower_calculation = pow((1 + nominal_interest), periods) - 1

    principal = float(payments / (upper_calculation / lower_calculation))

    print(f'Your loan principal = {principal}!')

    overpayment = payments * periods - principal
    print(f"\nOverpayment = {overpayment}")


# main
def main():
    type_selected, interest, payments, periods, principal = check_initial_input()

    if type_selected == "diff":
        diff_calculator(principal, interest, periods)

    if type_selected == "annuity":
        if periods is None:
            duration_calculator(principal, payments, interest)
        elif payments is None:
            payments_calculator(principal, periods, interest)
        else:
            principal_calculator(payments, periods, interest)


if __name__ == '__main__':
    main()
