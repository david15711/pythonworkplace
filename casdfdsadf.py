attack_points = 0
crit_points = 0
total_points = 100

while total_points > 0:
    # 현재 상태에서의 전체 공격력 증가량 계산
    attack_increase = (1300+1208+10*(attack_points+1)) * (1.5 + 0.01 * crit_points)
    crit_increase = (1300+1208+10*attack_points) * (1.5 + 0.01 * (crit_points + 1))

    print("현재 공격력:", attack_increase)


    # 더 높은 공격력 증가량을 갖는 포인트에 1 포인트 투자
    if attack_increase >= crit_increase:
        attack_points += 1
    else:
        crit_points += 1

    total_points -= 1

print("투자한 공격력 포인트:", attack_points)
print("투자한 치명타 배수 포인트:", crit_points)
