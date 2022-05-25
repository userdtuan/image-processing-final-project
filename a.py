    if activeGray:
        if(change == True):
            temp = image
            if(grayValue.isnumeric()):
                window['-ActiveGray-'].update(True)
                temp = cat_lat_mat_xam(pil2cv(temp), grayValue)
                temp = cv2pil(temp)

                image = temp
                backup_cat_lat_mat_xam = image

                check_cat_lat_mat_xam = True
                change = False
                print("gray")
            else:
                window['-ActiveGray-'].update(False)
                sg.popup('Gray value is invalid!!!!')
        elif(check_cat_lat_mat_xam != True):
            temp = image
            if(grayValue.isnumeric()):
                window['-ActiveGray-'].update(True)
                temp = cat_lat_mat_xam(pil2cv(temp), grayValue)
                temp = cv2pil(temp)

                image = temp
                backup_cat_lat_mat_xam = image

                check_cat_lat_mat_xam = True
                change = True
                print("gray")
            else:
                window['-ActiveGray-'].update(False)
                sg.popup('Gray value is invalid!!!!')
        else:
            image = backup_cat_lat_mat_xam
    else:
        if(check_cat_lat_mat_xam == True):
            check_cat_lat_mat_xam = False
            change = True
