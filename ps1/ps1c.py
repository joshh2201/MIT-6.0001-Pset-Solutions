annual_salary = float(input('Enter your annual salary:'))

# initial variables
semi_annual_raise = 0.07
r = 0.04
down_payment = 0.25 * 1000000
low = 0
high = 10000
current_savings = 0
steps = 0

# calculate number of months
while True:
    # reset variables for each bisection search iteration
    savings_rate = (low+high) / 2
    current_savings = 0
    monthly_salary = annual_salary / 12
    
    # calculate amount saved in 36 months
    for i in range(36):
        current_savings = current_savings + float(monthly_salary*savings_rate/10000) + current_savings*r/12
        # apply salary increase if number of months is divisible by 6
        if i % 6 == 0:
            monthly_salary = monthly_salary * (1+semi_annual_raise)
    
    # check if tolerance has been met or to change bounds for bisection search
    if abs(current_savings - down_payment) < 100:
        print('Best savings rate:',savings_rate/10000)
        print('Steps in bisection search:',steps)
        break
    elif abs(current_savings - down_payment) > 100 and current_savings > down_payment:
        high = savings_rate
    elif abs(current_savings - down_payment) > 100 and current_savings < down_payment:
        low = savings_rate
    
    # case that return can't be found 
    if high == low:
        print('Not possible to pay down payment')
        break
    steps += 1


