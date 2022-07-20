# 현재 가슴, 등, 목 길이 기준으로 코딩
# 목은 모두 범위 데이터
from input_types import ProductRecommendInput
from fastapi.encoders import jsonable_encoder

def preprocessing(recommend_input: ProductRecommendInput):
    dog_data_json = jsonable_encoder(recommend_input.dog_info)
    clothes_data_json = jsonable_encoder(recommend_input.product_info)
    clothes_data_detail_json = jsonable_encoder(recommend_input.product_details)

    important_size = clothes_data_json.get("important_size") #기준 사이즈

    #list로 편집
    #clothes_data_list=[[1번 사이즈 정보],[2번 사이즈 정보]]
    #사이즈 정보 = "XL","가슴둘레", "등길이", "목둘레", "다리길이", "사이즈 마진"
    clothes_data_list = [[0 for _ in range(5)] for _ in range(len(clothes_data_detail_json))]

    clothes_data_num = 0


    for i in range(len(clothes_data_detail_json)):
        flag = 0
        for j in range(len(clothes_data_detail_json)):
            if clothes_data_list[j][0]==clothes_data_detail_json[i].get("product_size"):
                flag+=1
        if flag == 0:
            clothes_data_list[clothes_data_num][0]=clothes_data_detail_json[i].get("product_size")
            clothes_data_list[clothes_data_num][1]=clothes_data_detail_json[i].get("size_chest")
            clothes_data_list[clothes_data_num][2]=clothes_data_detail_json[i].get("size_back")
            clothes_data_list[clothes_data_num][3]=clothes_data_detail_json[i].get("size_neck")
            clothes_data_list[clothes_data_num][4]=clothes_data_detail_json[i].get("size_leg")
            clothes_data_num += 1



    #오류 필터링

    nodata_size = [True for _ in range(len(clothes_data_detail_json))]
    nodata_part = [True for _ in range(4)] #[chest=> back=> neck => leg]

    for j in range(len(clothes_data_detail_json)):
        flag = 0
        if clothes_data_list[j][1] == -1:
            nodata_part[0] = False
            flag += 1
        if clothes_data_list[j][2] == -1:
            nodata_part[1] = False
            flag += 1
        if clothes_data_list[j][3] == -1:
            nodata_part[2] = False
            flag += 1
        if clothes_data_list[j][4] == -1:
            nodata_part[3] = False
            flag += 1
        if flag == 4:
            nodata_size[j] = False

    #list 정렬(사이즈 순서대로)
    #정렬 알고리즘 선택 현재 O(n^2)
    #정보가 없을 경우 chest=> back=> neck => leg으로 정렬
    flag_list=[0 for _ in range(6)]

    if nodata_part[0] == True:
        for i in range(clothes_data_num):
            flag = 0
            for j in range(i):

                if clothes_data_list[flag][1] > clothes_data_list[i][1]:
                    flag_list = clothes_data_list[i]
                    clothes_data_list[i] = clothes_data_list[flag]
                    clothes_data_list[flag] = flag_list
                    flag = i

    elif nodata_part[1] == True:
        for i in range(clothes_data_num):
            flag = 0
            for j in range(i):

                if clothes_data_list[flag][2] > clothes_data_list[i][2]:
                    flag_list = clothes_data_list[i]
                    clothes_data_list[i] = clothes_data_list[flag]
                    clothes_data_list[flag] = flag_list
                    flag = i

    elif nodata_part[2] == True:
        for i in range(clothes_data_num):
            flag = 0
            for j in range(i):

                if clothes_data_list[flag][3] > clothes_data_list[i][3]:
                    flag_list = clothes_data_list[i]
                    clothes_data_list[i] = clothes_data_list[flag]
                    clothes_data_list[flag] = flag_list
                    flag = i

    elif nodata_part[3] == True:
        for i in range(clothes_data_num):
            flag = 0
            for j in range(i):

                if clothes_data_list[flag][4] > clothes_data_list[i][4]:
                    flag_list = clothes_data_list[i]
                    clothes_data_list[i] = clothes_data_list[flag]
                    clothes_data_list[flag] = flag_list
                    flag = i

    error = 0

    # emptyc 사이즈 존재
    for i in range(len(clothes_data_detail_json)):
        if nodata_size[i] == False:
            error = 1
    # 중요사이즈 없을 경우
    if important_size == "size_chest":
        if clothes_data_json.get("category") == "하네스":
            if nodata_part[0] == False:
                error = 1

        elif clothes_data_json.get("category") == "상의" and clothes_data_json.get("category") == "원피스":
            if nodata_part[0] == False or nodata_part[2] == False:
                error = 1

        elif clothes_data_json.get("category") == "하의":
            if nodata_part[0] == False or nodata_part[3] == False:
                error = 1

    if important_size == "size_neck":
        if nodata_part[2] == False:
            error = 1

    if important_size == "size_back":
        if nodata_part[1] == False or nodata_part[2] == False:
            error = 1

    if important_size == "size_none":
        error = 1



#추천 알고리즘
#def size_recommend(error):

    if error==1:
        return "none","none"

    recommend_size = "none" #적당함, 슬림핏
    recommend_size2 = "failed" #오버핏
    # 강아지 정보
    dog_size_neck = dog_data_json.get("dog_size_neck")
    dog_size_chest = dog_data_json.get("dog_size_chest")
    dog_size_leg = dog_data_json.get("dog_size_leg")
    dog_size_back = dog_data_json.get("dog_size_back")


    # 의류 정보
    size_name = [clothes_data_list[i][0] for i in range(clothes_data_num)]
    chest_size_middle = [clothes_data_list[i][1] for i in range(clothes_data_num)]
    back_size_middle = [clothes_data_list[i][2] for i in range(clothes_data_num)]
    neck_size_middle =[clothes_data_list[i][3] for i in range(clothes_data_num)]
    leg_size_count_middle = [clothes_data_list[i][4] for i in range(clothes_data_num)]

    # 마진 값
    margin = clothes_data_json.get("size_margin")

    # 마진 계산 사이즈 설정
    chest_size_count_middle = [0 for _ in range(clothes_data_num)]
    back_size_count_middle = [0 for _ in range(clothes_data_num)]
    neck_size_count_middle = [0 for _ in range(clothes_data_num)]

    for t in range(0, len(size_name)):
        if important_size == "size_chest":
            if len(chest_size_count_middle) != 0:
                chest_size_count_middle[t] = chest_size_middle[t] - margin
                back_size_count_middle[t] = back_size_middle[t]- margin
                neck_size_count_middle[t] = neck_size_middle[t] - margin *2/3
        if important_size == "size_back":
            if len(back_size_count_middle) != 0:
                chest_size_count_middle[t] = chest_size_middle[t] - margin
                back_size_count_middle[t] = back_size_middle[t] - margin
                neck_size_count_middle[t] = neck_size_middle[t] - margin *2/3
        if  important_size == "size_neck":
            if len(neck_size_count_middle) != 0:
                neck_size_count_middle[t] = neck_size_middle[t] - margin *2/3

    # 사이즈 추천 시작
    for i in range(0 , len(size_name)):
        if important_size == "size_chest":
            neck_ok = [0 for _ in range(clothes_data_num)]
            leg_ok = [0 for _ in range(clothes_data_num)]

            if len(neck_size_count_middle) != 0:
                    for j in range(0, len(size_name)):
                        if dog_size_neck > neck_size_count_middle[j]:
                            neck_ok[j] = 1
                        else:
                            neck_ok[j] = 0


            if len(leg_size_count_middle)!=0:
                    for j in range(0, len(size_name)):
                        if dog_size_leg < leg_size_count_middle[j]:
                            leg_ok[j] = 1
                        else:
                            leg_ok[j] = 0

            for k in range(0, len(size_name)-1):
                    if leg_ok[k] != 1 and neck_ok[k] != 1:
                        if k == 0:

                            if len(size_name)!=1:
                                if dog_size_chest>=chest_size_count_middle[0] and dog_size_chest<(chest_size_count_middle[1]+chest_size_count_middle[0])/2:
                                    recommend_size = size_name[1]
                                else :
                                    if dog_size_chest<chest_size_count_middle[1] and dog_size_chest>=(chest_size_count_middle[1]+chest_size_count_middle[0])/2:
                                        recommend_size = size_name[1]
                                        if len(size_name)>=2:
                                            recommend_size2 = size_name[2]
                                        else :
                                            recommend_size2 = 'none'
                                    else:
                                        if dog_size_chest< chest_size_count_middle[0] and dog_size_chest >= (2*chest_size_count_middle[0]-chest_size_count_middle[1]):
                                            recommend_size = size_name[0]

                        else :
                            if k != len(size_name) :
                                if dog_size_chest>=chest_size_count_middle[k] and  dog_size_chest<(chest_size_count_middle[k]+chest_size_count_middle[k+1])/2:
                                    recommend_size = size_name[k+1]
                                    if len(size_name)>= k+3:
                                        recommend_size2 = size_name[k + 2]
                                    else :
                                        recommend_size2 = 'none'
                                else :
                                    if dog_size_chest>=(chest_size_count_middle[k]+chest_size_count_middle[k+1])/2 and dog_size_chest<chest_size_count_middle[k+1]:
                                        recommend_size = size_name[k + 1]

        if important_size == "size_neck":

            for k in range(0, len(size_name) - 1):
                if k == 0:
                    if len(size_name) != 1:
                        if dog_size_neck >= neck_size_count_middle[0] and dog_size_neck < (neck_size_count_middle[1] + neck_size_count_middle[0]) / 2:
                            recommend_size = size_name[1]
                        else:
                            if dog_size_neck < neck_size_count_middle[1] and dog_size_neck >= (neck_size_count_middle[1] + neck_size_count_middle[0]) / 2:
                                recommend_size = size_name[1]
                                if len(size_name) >= 2:
                                    recommend_size2 = size_name[2]
                                else :
                                    recommend_size2 = 'none'

                            else:
                                if dog_size_neck < neck_size_count_middle[0] and dog_size_neck > (2 * neck_size_count_middle[0] - neck_size_count_middle[1]):
                                    recommend_size = size_name[0]

                else:
                    if k != len(size_name):
                        if dog_size_neck >= neck_size_count_middle[k] and dog_size_neck < (neck_size_count_middle[k] + neck_size_count_middle[k + 1]) / 2:
                            recommend_size = size_name[k + 1]
                            if len(size_name) >= k + 3:
                                recommend_size2 = size_name[k + 2]
                            else :
                                recommend_size2 = 'none'
                        else:
                            if dog_size_neck >= (neck_size_count_middle[k] + neck_size_count_middle[k + 1]) / 2 and dog_size_neck < neck_size_count_middle[k + 1]:
                                recommend_size = size_name[k + 1]


        if important_size == "size_back":

                chest_ok = [0 for _ in range(clothes_data_num)]
                neck_ok = [0 for _ in range(clothes_data_num)]
                leg_ok = [0 for _ in range(clothes_data_num)]

                if len(neck_size_count_middle) != 0:
                        for j in range(0, len(size_name)):
                            if dog_size_neck > neck_size_count_middle[j]:
                                neck_ok[j] = 1
                            else:
                                neck_ok[j] = 0

                if len(chest_size_count_middle) != 0:
                        for j in range(0, len(size_name)):
                            if dog_size_neck > chest_size_count_middle[j]:
                                chest_ok[j] = 1
                            else:
                                chest_ok[j] = 0

                if len(leg_size_count_middle) != 0:
                        for j in range(0, len(size_name)):
                            if dog_size_leg < leg_size_count_middle[j]:
                                leg_ok[j] = 1
                            else:
                                leg_ok[j] = 0

                for k in range(0, len(size_name) - 1):
                        if leg_ok[k] != 1 and neck_ok[k] != 1 and chest_ok[k] != 1:
                            if k == 0:
                                if len(size_name) != 1:
                                    if dog_size_back >= back_size_count_middle[0] and dog_size_back < (back_size_count_middle[1] + back_size_count_middle[0]) / 2:
                                        recommend_size = size_name[1]
                                    else:
                                        if dog_size_back < back_size_count_middle[1] and dog_size_back >= (back_size_count_middle[1] + back_size_count_middle[0]) / 2:
                                            recommend_size = size_name[1]
                                            if len(size_name) >= 2:
                                                recommend_size2 = size_name[2]
                                            else :
                                                recommend_size2 = 'none'
                                        else:
                                            if dog_size_back < back_size_count_middle[0] and dog_size_back > (2 * back_size_count_middle[0] - back_size_count_middle[1]):
                                                recommend_size = size_name[0]

                            else:
                                if k != len(size_name):
                                    if dog_size_back >= back_size_count_middle[k] and dog_size_back < (back_size_count_middle[k] + back_size_count_middle[k + 1]) / 2:
                                        recommend_size = size_name[k + 1]
                                        if len(size_name) >= k + 3:
                                            recommend_size2 = size_name[k + 2]
                                        else :
                                            recommend_size2 = 'none'
                                    else:
                                        if dog_size_back >= (back_size_count_middle[k] + back_size_count_middle[k + 1]) / 2 and dog_size_back < back_size_count_middle[k + 1]:
                                            recommend_size = size_name[k + 1]

        return recommend_size, recommend_size2

#################################################################################################################################################################################################



#    print(size_recommend(error))

# 결과값 ('XL','failed') => 추천 사이즈 XL
# 결과값 ('XL','none') => 슬림핏 XL
# 결과값 ('XL','2XL') => 슬림핏 XL 오버핏 2XL
# 결과값 ('none','none') => 추천 X
# 결과값 ('none','failed') => 추천 X