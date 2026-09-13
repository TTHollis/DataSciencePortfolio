#DSC 510
#Week 4
#Programming Assignment 4.1
#Author: Tim Hollis
#10/1/2025
#===========================Change Control Log:===========================
#Change#:1
#Change: Removed prior change logs, changed made prior to publishing
#Date of Change: 09/24/2025
#Author: Tim Hollis
#Change Approved by: Tim Hollis
#Date Moved to Production: 09/24/2025

#Change#:2
#Change: Enabled timestamp display in receipt output
#        to reflect date and time of transaction
#Lines Affected: 72-76
#Date of Change: 09/24/2025
#Author: Tim Hollis
#Change Approved by: Tim Hollis
#Date Moved to Production: 09/24/2025

#Change#:3
#Change: Replaced flat rate pricing ($0.95/ft) from previous assignment
#        to reflect volume-based discounts and tiered pricing
#Lines Impacted: 85-93
#Date of Change: 09/24/2025
#Author: Tim Hollis
#Change Approved by: Tim Hollis
#Date Moved to Production: 09/24/2025

#Change#:4
#Change: Added proximity alert logic to notify users
#        when they are within 10% of the next pricing tier
#Lines Impacted: 97-115
#Date of Change: 09/24/2025
#Author: Tim Hollis
#Change Approved by: Tim Hollis
#Date Moved to Production: 09/24/2025

#Change#:5
#Change: Wrapped feet input and pricing logic in a loop
#        to allow users to revise their purchase amount before payment
#Lines Impacted: 135-155
#Date of Change: 09/24/2025
#Author: Tim Hollis
#Change Approved by: Tim Hollis
#Date Moved to Production: 09/24/2025

#Change#:6
#Change: Added input validation loop to ensure user response
#        to proximity upgrade prompt is limited to 'y' or 'n'
#Lines Affected: 146-151
#Date of Change: 09/24/2025
#Author: Tim Hollis
#Change Approved by: Tim Hollis
#Date Moved to Production: 09/24/2025

#Change#:7
#Change: Defined main function, moved all code to run inside function
#Lines Affected: 77-195
#Date of Change: 10/1/2025
#Author: Tim Hollis
#Change Approved by: Tim Hollis
#Date Moved to Production: 10/1/2025

#Change#:8
#Change: Edited feet to length in functions to be consistent
#Lines Affected: 77-195
#Date of Change: 10/1/2025
#Author: Tim Hollis
#Change Approved by: Tim Hollis
#Date Moved to Production: 10/1/2025
#=======================================================================


#Importing Datetime
from datetime import datetime

#-----Function: tiered_pricing-----

def tiered_pricing(length):
    """Defines bulk discount and tiered pricing based on length purchased"""
    if length <= 100:
        return 0.95
    elif length <= 250:
        return 0.85
    elif length <= 500:
        return 0.75
    else:
        return 0.55

#----Function: check_proximity-----

def check_proximity(length):
    """Provides proximity to price reduction for lengths within 10% of next pricing"""
    tiers=[
        (100,0.95),
        (250,0.85),
        (500,0.75),
        (float('inf'),0.55)
    ]

    for i,(threshold,price) in enumerate(tiers):
        if length<=threshold:
            if i < len(tiers) - 1:
                next_threshold,next_price=tiers[i+1]
                next_tier_start=threshold+1
                feet_needed=next_tier_start-length
                trigger_zone=threshold*0.10
                if 0<feet_needed<=trigger_zone:
                    return f'If you add {feet_needed:.2f} feet you will only pay (${next_price}/ft)'
            break
    return None

#-----Function: calculate_cost------

def calculate_cost(length, price_per_foot):
    """Calculate total installation cost based on length and price per foot"""
    return length*price_per_foot

#------------Main Program-----------

def main():
    print('='*62)
    print('Welcome to the Fierce and Fabulous Fiber Optic Cost Calculator')
    print('='*62)

    company_name=input('Please enter your company name: ')

    while True:
        try:
            length_requested=float(input("Enter fiber optic cable length needed in feet: "))
            if length_requested<=0:
                print('Sorry, I cannot sell you that amount, please enter a value above zero')
            else:
                break # Valid input-exit the loop
        except ValueError:
            print('Invalid response, please enter a numeric value.')

    while True:
        cost_per_foot=tiered_pricing(length_requested)
        total_cost=calculate_cost(length_requested, cost_per_foot)
        print(f'\nPrice per foot: ${cost_per_foot:.2f}')
        print(f'Total for {length_requested} feet is ${total_cost:.2f}')

        proximity_message=check_proximity(length_requested)
        if proximity_message:
            print(proximity_message)
            while True:
                revise=input('Would you like to add to your purchase today? (y/n):'
                             ).strip().lower()
                if revise in ['y','n']:
                    break
                print('Please enter y for yes, or n for no.')
            if revise=='y':
                length_requested=float(input('Enter new amount of cable needed in feet: '))
                continue #Allow user to edit the amount they are purchasing
        break #exit the loop if no revision

    while True:
        try:
            cash_rendered=float(input('Enter cash amount rendered: '))
            if cash_rendered<total_cost:
                print('Sorry, insufficient amount to cover the purchase cost')
            else:
                break # Acceptable amount input-exit the loop
        except ValueError:
            print('Invalid response, please enter a numeric value.')

    change_given=cash_rendered-total_cost
    timestamp=datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
    standard_price=0.95
    standard_total=length_requested*standard_price
    savings=standard_total-total_cost if length_requested>100 else 0

    print('\n'+'-'*50)
    print('Installation Receipt'.center(50))
    print(f'Date and Time: {timestamp}')
    print(f'Company Name: {company_name}')
    print(f'Length of Fiber Optic Cable Purchased: {length_requested:.2f} feet')
    print(f'Price per foot: ${cost_per_foot:.2f}')
    print(f'Total Cost of Installation: ${total_cost:.2f}')
    print(f'Cash Rendered: ${cash_rendered:.2f}')
    print(f'Change Given: ${change_given:.2f}')
    if length_requested>100:
        print(f'By purchasing {length_requested:.2f} feet you saved ${savings:.2f}')
    print('-'*50)
    print('Thank you for your payment!')
    print('Your Fabulous Fiber Fantasy is now a reality!')

#------------------Entry Point------------------

if __name__ == '__main__':
    main()
