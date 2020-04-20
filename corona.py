import random
import numpy as np

communities = {}
residential_area = {}
public_places = {}
transports = {}
hospitals = {}
g_rate = {}
economy = {'C1': 0.2, 'C2': 0.2, 'C3': 0.2, 'C4': 0.2}
total_virus_prsnt = {'C1': 0, 'C2': 0, 'C3': 0, 'C4': 0}
lockdown = {'C1': 0, 'C2': 0, 'C3': 0, 'C4': 0}
pp_virus_total = {'C1': 0, 'C2': 0, 'C3': 0, 'C4': 0}
tv_virus_total = {'C1': 0, 'C2': 0, 'C3': 0, 'C4': 0}
alert = {'C1': 0, 'C2': 0, 'C3': 0, 'C4': 0}
wheel = {
    1: 'Sanitizer', 2: 'Stupids Being Stupid',
    3: 'Charity Funds', 4: 'Vaccine'
}

for i in range(1, 5):
    communities['C'+str(i)] = np.arange(100*(i-1)+1, (100*i)+1)

# for i in range(1, 5):
#     residential_area['C'+str(i)] = communities['C'+str(i)][100*(i-1):50*i]

# for i in range(1, 5):
#     public_places['C'+str(i)] = communities['C'+str(i)][50*i:80*i]

# for i in range(1, 5):
#     transports['C'+str(i)] = communities['C'+str(i)][80*i:90*i]

# for i in range(1, 5):
#     hospitals['C'+str(i)] = communities['C'+str(i)][90*i:100*i]

for i in range(1, 5):
    economy['C'+str(i)] = 0.5


def generate_virus(total_virus_prsnt, growth_rate, infected_C, tp=1, First=False):
    virus_positions = {'C1': set(), 'C2': set(), 'C3': set(), 'C4': set()}
    new_virus_at = {}
    if First:
        infected_C = 2
        for i in [1, 2]:
            com = 'C'+str(random.randint(1, 4))
            new_virus_at = np.random.randint(1, 101, 4)
            for j in new_virus_at:
                virus_positions[com].add(j)
    else:
        for C in communities.keys():
            if tp[C] == 1:
                temp = random.choice(list(communities.keys()))
                for i in range(20):
                    if temp not in infected_C:
                        infected_C.append(temp)
                        break
                    else:
                        temp = random.choice(list(communities.keys()))
                total_virus_prsnt[temp] = tv_virus_total[C]*8
        for C in infected_C:
            new_virus_no = int(
                (total_virus_prsnt[C] * g_rate[C])
            )
            new_virus_at[C] = np.random.randint(0, 100, new_virus_no)
            for j in new_virus_at[C]:
                virus_positions[C].add(j)
    return virus_positions


def vaccine(infected_C, total_virus_prsnt):
    for C in infected_C:
        max_count = int(total_virus_prsnt[C] * 0.25)
        count = 0
        pos = np.squeeze(np.where(communities[C] == -999)) + 1
        Hs = int(list(C)[1])
        for i in pos:
            if count < max_count:
                communities[C][i] = 100*(Hs-1) + (i+1)
            count += 1


def update_virus_positions(virus_positions, communities):
    for C in communities.keys():
        if len(virus_positions[C]) > 0:
            for i in virus_positions[C]:
                communities[C][i-1] = -999
        residential_area[C] = communities[C][0:50]
        public_places[C] = communities[C][50:80]
        transports[C] = communities[C][80:90]
        hospitals[C] = communities[C][90:100]


def infected_communities(communities):
    infected_C = []
    for C in communities.keys():
        if -999 in communities[C]:
            infected_C.append(C)
    return infected_C


def check_public_places(C, ppv):
    ppv = 0
    for i in public_places[C]:
        if i == -999:
            ppv += 1
    return ppv


def check_transport(C, tv):
    tv = 0
    for i in transports[C]:
        if i == -999:
            tv += 1
    return tv


def growth_rate(wheel_value, pp=0, lockdown=0):
    if lockdown == 1:
        gr = 0.05
    else:
        gr = 0.25
        if pp == 1:
            gr = gr*4
    if wheel_value == 1:
        gr = 0
    elif wheel_value == 2:
        gr = gr*2
    return gr


def spinning_wheel():
    availabe_wheel_values = [1, 2, 3, 4]
    return random.choice(availabe_wheel_values)


def wheel_detail(wheel_value):
    if wheel_value == 1:
        print('''\nSanitizer will keep the corona virus at bay.
                growth rate is decresed\n''')
    elif wheel_value == 2:
        print('\nWe are the reson for our own downfall\n')
    elif wheel_value == 3:
        print('\nfunds will strenthen the economy to survive these difficult times\n')
    else:
        print('\nVaccine will be provided to the people who needs it the most\n')


def total_virus_present(communities, total_virus_prsnt):
    total_virus_prsnt = 0
    for i in communities:
        if i == -999:
            total_virus_prsnt += 1
    return total_virus_prsnt


def economic_growth(economy, lockdown, wheel_value):
    e = 0.05
    if lockdown == 0:
        if wheel_value == 3:
            economy += 2*e
        else:
            economy += e
    else:
        economy -= 2*e
    return min(round(economy, 2), 1)


def play_game():
    new_virus_positions = generate_virus(1, 1, 1, First=True)
    update_virus_positions(new_virus_positions, communities)
    infected_C = infected_communities(communities)
    iterations = 0
    print('Welcome!!!\n')
    print(f'Initial Economic State : {economy}\n')
    while(True):
        try:
            input_char = input('Enter P to spin the wheel , Q to quit , L to control lockdwon :\n')
            if (ord(input_char) == 81 or ord(input_char) == 113):
                print('Game Ended')
                break
            if (ord(input_char) == 76 or ord(input_char) == 108):
                x = input(
                    '''Input community(C1/C2/C3/C4)\n'''
                )
                lockdown[x] = int(input(
                    '''Enter 1 to impose lockdown or 0 to continue:\n'''
                ))
            elif (ord(input_char) == 80 or ord(input_char) == 112):
                pp = {'C1': 0, 'C2': 0, 'C3': 0, 'C4': 0}
                tp = {'C1': 0, 'C2': 0, 'C3': 0, 'C4': 0}
                print(f'Economic State : {economy}\n\n')
                wheel_value = spinning_wheel()
                print('wheel_stopped at -> ' + str(wheel[wheel_value]))
                wheel_detail(wheel_value)
                if wheel_value == 4:
                    vaccine(infected_C, total_virus_prsnt)
                for C in communities.keys():
                    economy[C] = economic_growth(economy[C], lockdown[C], wheel_value)
                    if economy[C] < 0.2:
                        raise Exception('Economic Breakdown\n\n')
                    pp_virus_new = check_public_places(C, pp_virus_total[C])
                    if pp_virus_new > pp_virus_total[C]:
                        pp[C] = 1
                    else:
                        pp[C] = 0
                    pp_virus_total[C] = pp_virus_new
                    if pp[C] == 1 and lockdown[C] == 0:
                        print(
                            f'A virus is encountered at a public place in {C}.\nConsider a lockdown\n\n')
                    tv_virus_new = check_transport(C, tv_virus_total[C])
                    if tv_virus_new > tv_virus_total[C] and lockdown[C] == 0:
                        print(
                            f'A virus is encountered at transports in {C}.\nConsider a lockdown as it puts other comm at risk\n\n')
                        tp[C] = 1
                    tv_virus_total[C] = tv_virus_new
                    g_rate[C] = growth_rate(wheel_value, lockdown=lockdown[C], pp=pp[C])
                    total_virus_prsnt[C] = total_virus_present(communities[C], total_virus_prsnt[C])
#                 print(total_virus_prsnt)
                new_virus_positions = generate_virus(
                    total_virus_prsnt, g_rate,
                    infected_C, tp=tp
                )
                update_virus_positions(new_virus_positions, communities)
                infected_C = infected_communities(communities)
                for C in communities.keys():
                    total_virus_prsnt[C] = total_virus_present(communities[C], total_virus_prsnt[C])
                    if total_virus_prsnt[C] > 20:
                        if alert[C] == 0:
                            print(
                                f'''Corona Virus Alert in {C} ,Social Distancing Action is adviced before next round\n\n'''
                            )
                            alert[C] = 1
                        else:
                            print(f'No of viruses present in {C}:{total_virus_prsnt[C]}\n\n')
                            print(f'Position of Virus : {communities[C]}\n\n')
                            print(f'growth rate of virus in {C} is : {g_rate[C]}\n\n')
#                 print(total_virus_prsnt)
#                 print(g_rate)
#                 print(communities)
                iterations += 1
            else:
                print('''Invalid Input, please Enter P to
                        Spin the wheel and Q to quit.\n''')
        except Exception:
            print('Game Over!!\n')
            break


play_game()
