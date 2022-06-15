def function1():
    input1_list = ['1', '2', '3', '4', 'x']
    user_input1 = input("Enter '1' for binary thresholding: \n"\
                    "Enter '2' for segmenting white groups: \n"\
                    "Enter '3' for quantifying fats from white groups: \n"\
                    "Enter '4' for validating identified fats w.r.t. manual tagged fats: \n"\
                    "Enter 'x' to exit the tool: \n")
    print('')
    flag1 = 0
    if input1_list.__contains__(user_input1) == True:
        flag1 = 1
    while (flag1 == 0):
        if input1_list.__contains__(user_input1) == True:
            user_input1 = input("Enter '1' for binary thresholding: \n"\
                            "Enter '2' for segmenting white groups: \n"\
                            "Enter '3' for quantifying fats from white groups: \n"\
                            "Enter '4' for validating identified fats w.r.t. manual tagged fats: \n"\
                            "Enter 'x' to exit the tool: \n")
            if input1_list.__contains__(user_input1) == True:
                flag1 = 1
            print('')
    if user_input1 == 'x':
        #quit()
        pass
    elif user_input1 == '1':
        user_input2 = input("Enter '1' for binary thresholding of raw image: \n"\
                        "Enter '2' for thresholding of image with manual tagged fats: \n"\
                        "Enter 'b' to go back to main menu: \n")
        flag1 = 0
        if ((user_input2 == '1') or (user_input2 == '2') or (user_input2 == 'b')):
            flag1 = 1
        while (flag1 == 0):
            if ((user_input2 != '1') or (user_input2 == '2') or (user_input2 == 'b')):
                user_input2 = input("Enter '1' for binary thresholding of raw image: \n"\
                        "Enter '2' for thresholding of image with manual tagged fats: \n"\
                        "Enter 'b' to go back to main menu: \n")
                if ((user_input2 == '1') or (user_input2 == '2') or (user_input2 == 'b')):
                    flag1 = 1
                print('')
        if user_input2 == '1':
            exec(open('E:/Annie Madam/Biology/Pancreas/fat_parameter_test/threshold_image.py').read())
            print('\nTask completed')
        elif user_input2 == '2':
            exec(open('E:/Annie Madam/Biology/Pancreas/fat_parameter_test/threshold_manual_image.py').read())
            print('\nTask completed')
        elif user_input2 == 'b':
            pass
        print('')
    elif user_input1 == '2':
        exec(open('E:/Annie Madam/Biology/Pancreas/fat_parameter_test/white_groups.py').read())
        print('\nTask completed')
    elif user_input1 == '3':
        exec(open('E:/Annie Madam/Biology/Pancreas/fat_parameter_test/fat_from_groups.py').read())
        print('\nTask completed')
    elif user_input1 == '4':
        exec(open('E:/Annie Madam/Biology/Pancreas/fat_parameter_test/fat_results_compare.py').read())
        print('\nTask completed')
    return user_input1
    
# files not included: image_open_human, fat_results_compare

return_value = function1()
while (return_value != 'x'):
    return_value = function1()