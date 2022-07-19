import math
import random
from fastapi.encoders import jsonable_encoder

def recommend_dog_size(dog_info):
    dog_info_json = jsonable_encoder(dog_info)
    breed = dog_info_json.get("dog_type")
    weight = dog_info_json.get("dog_weight")
    old = dog_info_json.get("dog_age")
    result = size(breed, weight, old)

    return {
        "dog_size_chest": result[0]+random.random()-0.5,
        "dog_size_neck": result[1]+random.random()-0.5,
        "dog_size_back": result[2]+random.random()-0.5,
        "dog_size_leg": result[3]+random.random()-0.5
    }


def size(breed,weight,old):

    breed_list = ['포메라니안', '말티즈', '푸들(토이)', '골든리트리버', '비숑', '치와와', '시츄', '진돗개', '푸들(미디엄미니어처)']

    # 사이즈 분류 (small:0,medium:1,large:2,Giant:3)
    legend_list = [0, 0, 0, 2, 0, 0, 0, 2, 0]
    #legend_group = [5, 6, 9, 1, 9, 6, 6, 4]

    # 기준 사이즈 비율 (small=포메(1.934497817,3.572052402),medium,large,Giant)
    weight_L_standard = [1.934497817, 0, 28.78205]
    weight_H_standard = [3.572052402, 0, 33.71794872]

    # 몸무게 데이터
    weight_L = [1.934497817, 1.7, 2.5, 28.78205, 3, 1.5, 5, 29, 2]
    weight_H = [3.572052402, 5.4, 4, 33.71794872, 10, 5, 8, 34, 9]

    # 가슴둘레 데이터
    height_L = [30, 30, 32, 71, 35, 27, 40, 71, 30]
    height_H = [40, 40, 41, 81, 50, 42, 50, 81, 50]

    #목둘레 데이터(neck_length/chest_length)
    neck_ratio=[0.5, 0.625, 0.6035, 0.617, 0.631, 0.66, 1, 0.7, 0.617, 0.6035]
    #등길이 데이터(back_length/chest_length)
    back_ratio = [0.9, 0.763, 0.917, 1, 0.842, 0.766, 0.821, 1, 0.917]
    # 다리길이 데이터(leg_length/chest_length)
    leg_ratio = [0.375, 0.4025, 0.552, 0.583, 0.45, 0.425, 0.30, 0.583, 0.552]
    # 기준 나이(small=포메,medium,large=골든리트리버,Giant)
    standard_age = [10, 1, 12]
    # 나이 조정(나이가 None 일때)
    if old == None:
        old = 24
    else:
        old = old / 1.5
    # weight_New_H 상수
    weight_New_H_Constant = [[0.0000628402, 0.0022481814, 0.0310363653, 0.1987837391, 0.4861198101, 0.5359060293],
                             [1, 1, 1, 1, 1, 1],
                             [0.0002131400, 0.0093804563, 0.1605051998, 1.2979481676, 4.3432809388, 1.7195670385]]
    # weight_New_L상수
    weight_New_L_Constant = [[0.0000484626, 0.0016899097, 0.0228000776, 0.1442781028, 0.3701682338, 0.1724625085],
                             [1, 1, 1, 1, 1, 1],
                             [0.0002312472, 0.0098911478, 0.1639884019, 1.2821824159, 4.1625782165, 1.2723093566]]

    # [가슴,목,배,다리]
    prediction_length=[0, 0, 0, 0]

    if breed == '믹스 소형견' or breed == '믹스 중형견' or breed == '믹스 대형견':
        
        return group_size(breed, weight)

    else:
        for i in range(0 , len(breed_list)):
            if breed == breed_list[i]:
                if old < standard_age[legend_list[i]]:

                    # 기준 사이즈 비율 (small=포메(1.934497817,3.572052402),medium,large,Giant)
                    weight_L_ratio = weight_L_standard[legend_list[i]]/weight_L[i]
                    weight_H_ratio = weight_H_standard[legend_list[i]]/weight_H[i]

                    # 나이별 몸무게 데이터
                    weight_New_L = float( weight_New_L_Constant[legend_list[i]][0] * old ** 6 - weight_New_L_Constant[legend_list[i]][1] * old ** 5 + weight_New_L_Constant[legend_list[i]][2] * old ** 4 - weight_New_L_Constant[legend_list[i]][3] * old ** 3 + weight_New_L_Constant[legend_list[i]][4] * old ** 2 + weight_New_L_Constant[legend_list[i]][5] * old)/ weight_L_ratio
                    weight_New_H = float( weight_New_H_Constant[legend_list[i]][0] * old ** 6 - weight_New_H_Constant[legend_list[i]][1] * old ** 5 + weight_New_H_Constant[legend_list[i]][2] * old ** 4 - weight_New_H_Constant[legend_list[i]][3] * old ** 3 + weight_New_H_Constant[legend_list[i]][4] * old ** 2 + weight_New_H_Constant[legend_list[i]][5] * old)/ weight_H_ratio

                    # 나이별 키 데이터
                    height_New_L = height_L[i]/(weight_L[i]** (1 / 3))*(weight_New_L** (1 / 3))
                    height_New_H = height_H[i]/(weight_H[i]** (1 / 3))*(weight_New_H** (1 / 3))

                    # 새로운 몸무게 비율
                    weight_New_ratio = float((weight ** (1 / 3) - weight_New_L ** (1 / 3)) / (weight_New_H ** (1 / 3) - weight_New_L ** (1 / 3)))

                    if weight_New_L <= weight and weight <= weight_New_H:
                        chest_prediction = weight_New_ratio * (height_New_H - height_New_L) + height_New_L
                        prediction_length[0] = chest_prediction
                        prediction_length[1] = chest_prediction * neck_ratio[i]
                        prediction_length[2] = chest_prediction * back_ratio[i]
                        prediction_length[3] = chest_prediction * leg_ratio[i]
                        return prediction_length

                    else:
                        return group_size(breed, weight)
                            #group_size(legend_group[i], weight, neck_ratio[i], leg_ratio[i], back_ratio[i]); #"나이 대비 크기 범위 밖"

                elif  weight_L[i] <= weight and weight <= weight_H[i]:

                    # 몸무게 비율
                    weight_ratio = float((weight ** (1 / 3) - weight_L[i] ** (1 / 3)) / (weight_H[i] ** (1 / 3) - weight_L[i] ** (1 / 3)))
                    chest_prediction = weight_ratio * (height_H[i] - height_L[i]) + height_L[i]
                    prediction_length[0] = chest_prediction
                    prediction_length[1] = chest_prediction * neck_ratio[i]
                    prediction_length[2] = chest_prediction * back_ratio[i]
                    prediction_length[3] = chest_prediction * leg_ratio[i]
                    return prediction_length

                else:
                    return group_size(breed, weight)
                        #group_size(legend_group[i], weight, neck_ratio[i], leg_ratio[i], back_ratio[i]); #"크기 범위 밖"

def group_size(breed, weight):
        
        prediction_length1 = [0 for _ in range(4)]
        #그룹별 범위
        neck_mix_R= [0.628675577]
        leg_mix_R= [0.457990663]
        back_mix_R= [0.857543007]

        group = group_num(breed)
        if group == 1:
            chest_prediction= 25.675 * math.log( weight) + 11.173
        if group == 2:
            chest_prediction= 24.526 * math.log( weight) + 2.9444
        if group == 3:
            chest_prediction= 7.4059 * math.log( weight) + 22.938
        if group == 4:
            chest_prediction= 22.278 * math.log( weight) + 5.48
        if group == 5:
            chest_prediction= 12.342 * math.log( weight) + 22.099
        if group == 6:
            chest_prediction= 12.219 * math.log( weight) + 21.227
        if group == 7:
            chest_prediction= 14.183 * math.log( weight) + 19.293
        if group == 8:
            chest_prediction= 14.183 * math.log( weight) + 19.293
        if group == 9:
            chest_prediction = 14.147 * math.log( weight) + 19.256
        if group == 10:
            chest_prediction = 14.183 * math.log( weight) + 19.293
        if group == 11:
            chest_prediction = 13.431 * math.log( weight)  + 18.234
        if group == 12:
            chest_prediction = 12.039 * math.log( weight) + 19.583
        if group == 13:
            chest_prediction = 14.183 * math.log( weight) + 19.293

        prediction_length1[0] = chest_prediction
        prediction_length1[1] = chest_prediction * neck_mix_R[0]
        prediction_length1[2] = chest_prediction * back_mix_R[0]
        prediction_length1[3] = chest_prediction * leg_mix_R[0]

        return prediction_length1

# 어떤 그룹에 속하는지 보여주는 함수
def group_num(breed):
    
    group =[
     [],
     ['골든 리트리버', '그레이트 피레니즈', '노바 스코셔 덕 톨링 레트리버','라지 문스터랜더','래브라도 리트리버','러프 콜리','오스트레일리안 캐틀 독','버니즈 마운틴 독','벨지안 셰퍼드','보더콜리','센트럴 아시안 셰퍼드독','셔틀랜드 쉽독','스무스 콜리','아이리시 워터 스파니엘','오스트레일리안 셰퍼드','체사피크베이 리트리버','체코슬로바키안 울프독','컬리 코티드 리트리버','콜리','파슨 러셀 테리어','플랫-코티드 리트리버'],
     ['나폴리탄 마스티프','도사견','로트와일러','마스티프','보더 테리어','보스턴 테리어','불독','불마스티프','세인트 버나드','스태퍼드셔 불테리어','아메리칸 에스키모','아메리칸 코카 스파니엘','차이니즈 샤페이','카네코르소','코카시안 셰퍼드독','코카시안 오프차카','크럼버 스파니엘','티벳탄 마스티프','퍼그','페로 드 프레사 카나리오','프렌치 불독','필라 브라질레이로'],
     ['그레이트 데인','레이크랜드 테리어','맨체스터 테리어','미니어처 불 테리어','미니어처 슈나우저','베들링턴 테리어','부비에 데 플랑드르','불 테리어','스코티쉬 테리어','실리함 테리어','아이리시 테리어','에어데일 테리어','오스트레일리안 테리어','와이어 폭스 테리어','요크셔 테리어','웨스트 하일랜드 화이트 테리어','웰시 테리어','자이언트 슈나우저','저먼 헌팅 테리어','케리 블루 테리어','케언 테리어'],
     ['닥스훈트','댄디 딘몬트 테리어','스카이 테리어','웰시 코기'],
     ['기슈','노르웨이언 엘크하운드','뉴펀들랜드','레온베르거','사모예드','시바 이누', '시베리안 라이카','시베리안 허스키','시코쿠','아메리칸 아키타','아키타','알라스칸 말라뮤트','진돗개','포메라니안','풍산개','홋카이도견','재패니즈 스피츠'],
     ['노르위치 테리어', '노퍽 테리어','말티즈','말티푸','시츄','아펜핀셔','재패니즈 친'],
     ['달마시안', '도고 아르헨티노','도베르만 핀셔','로디지안 리즈백','미니어처 핀셔','바센지','바셋하운드','바이마라너','복서','브리타니 스파니엘','블랙 앤 탄 쿤 하운드','블러드 하운드','비글','비즐라','아이리시 세터','타이 리지백 독','타이완 독','와이어헤어드 포인팅 그리폰','잉글리시 세터','잉글리시 포인터','잭 러셀 테리어','저먼 쇼트헤어드 포인터','저먼 와이어 헤어드 포인팅 독','포인터'],
     ['비어디드 콜리','쁘띠 바셋 그리펀 벤딘','사우스 러시안 오브차카','삽살개', '올드 잉글리시 쉽독','차우차우','코몬도르','키스혼드','티벳탄 테리어','포르투기즈 워터 독','풀리'],
     ['라사 압소','리틀 라이언 독','브뤼셀 그리펀','비숑 프리제','서섹스 스파니엘','잉글리시 스프링거 스파니엘','잉글리시 코카 스파니엘','킹 찰스 스파니엘','티벳탄 스파니엘','파피용빠삐용','필드 스파니엘'],
     ['그레이하운드','디어하운드','보르조이','살루키','아이리시 울프하운드','아자왁','아프간하운드','파라오 하운드','페키니즈','휘핏'],
     ['차이니즈 크레스티드 독','치와와'],
     ['푸들 미디엄미니어처', '푸들스탠다드', '푸들토이'],
     ['믹스 소형견', '믹스 중형견', '믹스 대형견']
     ]
    
    for i in range(14):
        for j in range(len(group[i])):
            if group[i][j] == breed:
                return i
'''
#small:0, mideum:1, large:2, giant:3
def size_group_size(size_group, weight):
    prediction_length2 = [0, 0, 0, 0]
    # 그룹별 범위
    neck_mix_R = [1, 1, 2]
    back_mix_R = [1, 3, 6]
    leg_mix_R = [1, 2, 4]

    if size_group == 0:
        chest_prediction = 14.183 * math.log(weight) + 19.293
    if size_group == 1:
        chest_prediction = 14.183 * math.log(weight) + 19.293
    if size_group == 2:
        chest_prediction = 14.183 * math.log(weight) + 19.293

    prediction_length2[0] = chest_prediction
    prediction_length2[1] = chest_prediction * neck_mix_R[size_group]
    prediction_length2[2] = chest_prediction * back_mix_R[size_group]
    prediction_length2[3] = chest_prediction * leg_mix_R[size_group]


    return prediction_length2
'''
"""
file = open('data.json', 'r', encoding='utf-8')
jsonString = json.load(file)
# 종
a = jsonString.get("dog_type")
# kg
b = float(jsonString.get("dog_weight"))
# 생후 몇 개월
c = jsonString.get("dog_age")
# 그룹
d = 1
# 성별
e = 0

print("[가슴둘레,            목둘레,              등길이,              다리길이            ]")
print(size(a, b, c, d, e))

"""