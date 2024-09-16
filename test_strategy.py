import traceback
import db
from datetime import datetime, timedelta

Balance = float(500)
stake_index = 0
stakes = [10]

rows = db.get_all_numbers_and_date(True)
consecutive_loss = 0
loss_count = 0

# Convert the string date to datetime object
rows = [(datetime.strptime(g[0], '%Y-%m-%d %H:%M:%S.%f'), float(g[1])) for g in rows]

skip_until = None

total_trade = 0

for index, (date, i) in enumerate(rows):

    # Skip iterations if we're still within the skip period
    if skip_until and date < skip_until:
        # print(date)
        continue
    
    try:
        # if consecutive_loss == 2:
        #     if i < 1.2:
        #         loss_count += 1
        #         if loss_count == 3:
        #             consecutive_loss = 0
        #             loss_count = 0
        #     else:
        #         loss_count = 0
        #     continue

        if i < 1.1:
            Balance -= stakes[stake_index]
            
            stake_index += 1
            total_trade +=1
            print(f"Loss: {stakes[stake_index]} at index {index}")
        
            skip_until = date + timedelta(seconds=7)  # Skip next 5 minutes
            # consecutive_loss += 1
        else:
            Balance += stakes[stake_index] * 1.1
            consecutive_loss = 0
            stake_index = 0
            total_trade +=1


        if Balance < 1:
            print(f"Balance dead at index {index}")
            break

    except Exception as e:
        print(f"Exception at index {index}: {e}")
        # input('broke here')
        stake_index = 0
        

print(Balance)
print(db.get_results())
print(total_trade)





def max_consecutive_below_threshold(numbers, threshold=4):
    max_consecutive = 0
    max_index = 0
    current_consecutive = 0
    
    for index, number in enumerate(numbers):
        try:
            number = float(number)
            if number < threshold:
                current_consecutive += 1
                if current_consecutive > max_consecutive:
                    max_consecutive = current_consecutive
                    max_index = index
            else:
                current_consecutive = 0
        except ValueError as e:
            print(f"Invalid number '{number}': {e}")
    
    return [max_consecutive, max_index]


prices = db.get_all_numbers(True)
max_streak = max_consecutive_below_threshold(prices,threshold=1.3)
print(f"The maximum consecutive times it was less than 1.2: {max_streak[0]} at index {max_streak[1]}")

# def count_numbers_less_than(numbers, threshold):
#     count = 0
#     for number in numbers:
#         if number < threshold:
#             count += 1
#     return count

# count = count_numbers_less_than(prices, 1.2)

# print(f"Numbers less than 1.2 appear {count} times.")


# # db.get_all_numbers_and_date




# # profit = 0
# # for i in db.get_results():
# #     profit += i
# #     print(i)

# # print(f'Balance is {profit}')
 