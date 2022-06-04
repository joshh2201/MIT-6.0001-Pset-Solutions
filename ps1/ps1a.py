# user inputs
annual_salary = float(input('Enter your annual salary:'))
portion_saved = float(input('Enter the percent of yor salary to save, as a decimal:'))
total_cost = float(input('Enter the cost of your dream home:'))

# calculating variables
portion_down_payment = 0.25 * total_cost
current_savings = 0
r = 0.04
monthly_salary = annual_salary / 12
months = 0

# calculate number of months
while current_savings <= portion_down_payment:
    current_savings = current_savings + monthly_salary*portion_saved + current_savings*(r/12)
    months += 1

# output
print('Number of months:',months)