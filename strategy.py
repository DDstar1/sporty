# Balance = 7000
# stake_index = 0
# stakes = [10, 40, 140, 460,1460, 4540]
# # stakes = [100, 400, 1400, 4600, 14600, 45400]
# prices = db.get_all_numbers()
# # print(prices)
# consecutive_loss = 0
# loss_count = 0

# for index, i in enumerate(prices):
#     if(index<2972):
#         continue

#     try:
#         i = float(i)

#         if consecutive_loss == 2:
#             if i < 1.5:
#                 loss_count += 1
#                 if loss_count == 2:
#                     print(f"{stakes[stake_index]} at {index}")
#                     consecutive_loss = 0
#                     loss_count = 0
#                     stake_index = 0
                    
#             else:
#                 loss_count = 0

#             continue


#         if i < 1.5:
#             Balance -= stakes[stake_index]
#             stake_index += 1
#             consecutive_loss += 1
#             print(f"After loss baance was {Balance}")
#         else:
#             Balance += (stakes[stake_index] * 1.5)
#             consecutive_loss = 0
#             stake_index = 0

#         if(Balance < 1):
#             print(f"Balance dead at index {index}")
#             break
#     except Exception as e:
#         # print(i)
#         print(f"e at {index}")
#         # print(index)
#         break

# print(Balance)



# def max_consecutive_below_threshold(numbers, threshold=1.5):
#     max_consecutive = 0
#     max_index = 0
#     current_consecutive = 0
    
#     for index, number in enumerate(numbers):
#         try:
#             number = float(number)
#             if number < threshold:
#                 current_consecutive += 1
#                 if current_consecutive > max_consecutive:
#                     max_consecutive = current_consecutive
#                     max_index = index
#             else:
#                 current_consecutive = 0
#         except ValueError as e:
#             print(f"Invalid number '{number}': {e}")
    
#     return [max_consecutive, max_index]


# prices = db.get_all_numbers()
# max_streak = max_consecutive_below_threshold(prices)
# print(f"The maximum consecutive times it was less than 1.5: {max_streak[0]} at index {max_streak[1]}")



 